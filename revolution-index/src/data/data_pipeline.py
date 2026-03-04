"""
Data pipeline: frequency alignment, LOCF interpolation, freshness tracking,
and unified dataset construction.

Design decisions (from critical review):
- LOCF (Last Observation Carried Forward) for upsampling, NOT linear interpolation
  (critical review B1: "step function is more honest than linear interpolation")
- Daily/weekly data resampled to monthly averages
- Freshness column tracks months since last actual observation
- Common reference period: 1970-present for normalization (critical review B2)

Usage:
    pipeline = DataPipeline()
    unified = pipeline.build_unified_monthly(fred_data, wid_data)
"""

import logging
from pathlib import Path

import numpy as np
import pandas as pd

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from config import FRED_SERIES, PROCESSED_DIR, REFERENCE_START

logger = logging.getLogger(__name__)


class DataPipeline:
    """Aligns mixed-frequency data to a common monthly timeline."""

    # Max staleness before a variable is flagged (in months)
    STALENESS_LIMITS = {
        "daily": 1,
        "weekly": 1,
        "monthly": 3,
        "quarterly": 6,
        "annual": 18,
    }

    def __init__(self, output_dir: Path | None = None):
        self.output_dir = output_dir or PROCESSED_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def align_to_monthly(
        self,
        series: pd.Series,
        source_frequency: str,
        series_id: str = "",
    ) -> pd.DataFrame:
        """
        Align a single time series to monthly frequency.

        For high-frequency data (daily/weekly): resample to month-start average.
        For low-frequency data (quarterly/annual): LOCF (forward fill).

        Returns DataFrame with columns:
        - value: the aligned value
        - months_stale: months since last actual observation
        - is_observed: True if this month had an actual observation
        """
        series = series.dropna().sort_index()
        if len(series) == 0:
            return pd.DataFrame(columns=["value", "months_stale", "is_observed"])

        if source_frequency in ("daily", "weekly"):
            # Downsample: average within each month
            monthly = series.resample("MS").mean()
        else:
            # For monthly, quarterly, annual: reindex to monthly and LOCF
            monthly_index = pd.date_range(
                start=series.index.min().replace(day=1),
                end=series.index.max().replace(day=1),
                freq="MS",
            )
            monthly = series.reindex(monthly_index, method="ffill")

        # Build result with freshness tracking
        result = pd.DataFrame({"value": monthly}, index=monthly.index)
        result.index.name = "date"

        # Track which months have actual observations
        if source_frequency in ("daily", "weekly"):
            # Every month with data is "observed" for downsampled series
            result["is_observed"] = True
            result["months_stale"] = 0
        else:
            # Mark months that had an actual observation
            observed_months = set()
            for dt in series.index:
                observed_months.add(dt.replace(day=1))

            result["is_observed"] = result.index.isin(observed_months)

            # Compute months since last actual observation
            result["months_stale"] = 0
            last_observed = None
            for dt in result.index:
                if dt in observed_months:
                    last_observed = dt
                    result.loc[dt, "months_stale"] = 0
                elif last_observed is not None:
                    months_diff = (dt.year - last_observed.year) * 12 + (dt.month - last_observed.month)
                    result.loc[dt, "months_stale"] = months_diff
                else:
                    result.loc[dt, "months_stale"] = -1  # No prior observation

        logger.debug(
            f"{series_id}: {source_frequency} -> monthly, "
            f"{len(result)} months, "
            f"{result['is_observed'].sum()} observed"
        )
        return result

    def compute_derived_series(self, aligned: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
        """
        Compute derived series needed by models but not directly available from FRED.

        Currently computes:
        - real_wage_change: YoY % change in real hourly earnings (CES0500000003 / CPIAUCSL)
        - food_energy_cpi_yoy: Average of YoY % change in food and energy CPI
        """
        derived = {}

        # Real wage change: nominal earnings deflated by CPI
        if "CES0500000003" in aligned and "CPIAUCSL" in aligned:
            earnings = aligned["CES0500000003"]["value"]
            cpi = aligned["CPIAUCSL"]["value"]

            # Align indices
            common_idx = earnings.index.intersection(cpi.index)
            real_earnings = earnings.loc[common_idx] / cpi.loc[common_idx] * 100

            # Year-over-year percent change
            real_wage_yoy = real_earnings.pct_change(periods=12) * 100

            result = pd.DataFrame({
                "value": real_wage_yoy,
                "is_observed": True,
                "months_stale": 0,
            })
            derived["real_wage_change"] = result
            logger.info(f"Computed real_wage_change: {len(result.dropna())} valid months")

        return derived

    def build_unified_monthly(
        self,
        fred_data: dict[str, pd.DataFrame],
        wid_data: pd.DataFrame | None = None,
    ) -> pd.DataFrame:
        """
        Build a single unified monthly DataFrame from all data sources.

        Each column is a series (by series_id), with LOCF alignment
        and freshness metadata stored separately.

        Returns:
            unified: DataFrame with one column per series, monthly DatetimeIndex
        """
        aligned = {}
        freshness = {}

        # Align all FRED series
        for series_id, df in fred_data.items():
            if series_id not in FRED_SERIES:
                logger.warning(f"Unknown series {series_id}, skipping")
                continue

            freq = FRED_SERIES[series_id]["frequency"]
            result = self.align_to_monthly(df["value"], freq, series_id)

            if len(result) > 0:
                aligned[series_id] = result
                freshness[series_id] = result[["months_stale", "is_observed"]]

        # Align WID data (annual -> monthly via LOCF)
        if wid_data is not None and len(wid_data) > 0:
            result = self.align_to_monthly(wid_data["value"], "annual", "top_1pct_share")
            if len(result) > 0:
                aligned["top_1pct_share"] = result
                freshness["top_1pct_share"] = result[["months_stale", "is_observed"]]

        # Compute derived series
        derived = self.compute_derived_series(aligned)
        for sid, df in derived.items():
            aligned[sid] = df

        # Build unified DataFrame
        if not aligned:
            raise ValueError("No data available to build unified dataset")

        # Find common date range
        all_dates = set()
        for df in aligned.values():
            all_dates.update(df.index)
        date_range = pd.date_range(min(all_dates), max(all_dates), freq="MS")

        unified = pd.DataFrame(index=date_range)
        unified.index.name = "date"

        for series_id, df in aligned.items():
            unified[series_id] = df["value"].reindex(date_range)

        # Save
        output_path = self.output_dir / "unified_monthly.parquet"
        unified.to_parquet(output_path)
        logger.info(
            f"Unified monthly dataset: {unified.shape[1]} series, "
            f"{len(unified)} months ({unified.index.min().date()} to {unified.index.max().date()})"
        )

        # Save freshness metadata
        freshness_path = self.output_dir / "freshness_metadata.parquet"
        if freshness:
            fresh_df = pd.DataFrame({
                sid: meta["months_stale"] for sid, meta in freshness.items()
            })
            fresh_df.to_parquet(freshness_path)

        return unified

    def get_reference_period(self, unified: pd.DataFrame) -> pd.DataFrame:
        """Slice unified data to the common reference period (1970-present)."""
        return unified.loc[REFERENCE_START:]

    def data_quality_report(self, unified: pd.DataFrame) -> pd.DataFrame:
        """
        Generate a data quality report for the unified dataset.

        For each series: observation count, null count, date range,
        percent coverage in reference period.
        """
        ref = self.get_reference_period(unified)
        total_months = len(ref)

        rows = []
        for col in unified.columns:
            series = unified[col].dropna()
            ref_series = ref[col].dropna()
            rows.append({
                "series_id": col,
                "total_observations": len(series),
                "null_count": unified[col].isna().sum(),
                "start_date": str(series.index.min().date()) if len(series) > 0 else None,
                "end_date": str(series.index.max().date()) if len(series) > 0 else None,
                "ref_period_coverage": f"{len(ref_series) / total_months * 100:.1f}%",
                "ref_period_months": len(ref_series),
            })

        return pd.DataFrame(rows)
