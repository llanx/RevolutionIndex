"""
Model 3: Financial Stress Pathway (Stages 1-2)

Models the causal chain: Financial Shock -> Economic Pain
(Stages 3-4: Political Grievance -> Mobilization are deferred to Phase 2
because they require non-FRED data sources.)

Stage 1 (FSSI - Financial System Stress Index):
  Weighted z-score composite of financial stress indicators.

Stage 2 (ETI - Economic Transmission Index):
  Weighted z-score composite of economic pain indicators.

The model also computes cross-correlation between FSSI and ETI
to empirically measure the financial-to-economic transmission lag
(hypothesized at 3-12 months in the spec).

Reference: model-specifications.md lines 475-713
Fix: critical-review-model-specs.md C2 (lag structure based on N=2-3)
"""

import numpy as np
import pandas as pd

from src.models.base_model import BaseModel, ModelOutput
from src.analysis.normalization import rolling_zscore
from config import REFERENCE_START, FSP_PARAMS, FRED_SERIES


class FinancialStressPathway(BaseModel):
    """Financial Stress Pathway: FSSI (Stage 1) and ETI (Stage 2)."""

    name = "financial_stress"

    # Stage 1: Financial System Stress Index
    FSSI_SERIES = {
        "STLFSI4": 0.25,     # St. Louis Fed Financial Stress Index
        "T10Y2Y": 0.20,      # Yield curve (inverted = stress)
        "VIXCLS": 0.20,      # Volatility
        "BAMLH0A0HYM2": 0.20, # Credit spreads
        "DRSFRMACBS": 0.15,   # Mortgage delinquency
    }

    # Stage 2: Economic Transmission Index
    # real_wage_change is a derived series computed by the data pipeline
    ETI_SERIES = {
        "UNRATE": 0.25,
        "IC4WSA": 0.20,
        "real_wage_change": 0.20,
        "CSCICP03USM665S": 0.35,
    }

    # Series where higher values mean LESS stress (must invert)
    INVERT_SERIES = {"T10Y2Y", "CSCICP03USM665S"}

    def __init__(
        self,
        rolling_window_years: int | None = None,
        fssi_weights: dict | None = None,
        eti_weights: dict | None = None,
    ):
        self.window_years = rolling_window_years or FSP_PARAMS["rolling_window_years"]
        self.fssi_weights = fssi_weights or dict(self.FSSI_SERIES)
        self.eti_weights = eti_weights or dict(self.ETI_SERIES)

    def required_series(self) -> list[str]:
        series = list(self.FSSI_SERIES.keys()) + list(self.ETI_SERIES.keys())
        # real_wage_change is derived, not directly fetched
        # Also need the raw series it's computed from
        series.extend(["CES0500000003", "CPIAUCSL"])
        return list(set(series))

    def _compute_stage(
        self,
        data: pd.DataFrame,
        date: pd.Timestamp,
        series_weights: dict[str, float],
    ) -> tuple[float, dict[str, float]]:
        """
        Compute a single stage (FSSI or ETI) as weighted z-score composite.

        For each series:
        1. Compute rolling z-score (20-year window)
        2. Invert if needed (higher raw = less stress)
        3. Clip to [-3, 3] to prevent outlier domination
        4. Weighted average
        5. Convert to 0-100 scale via CDF

        Returns:
            (composite_score_0_100, component_dict)
        """
        components = {}
        weighted_sum = 0.0
        total_weight = 0.0

        for series_id, weight in series_weights.items():
            if series_id not in data.columns:
                continue

            series = data[series_id].dropna()
            if len(series) < 24:  # Need at least 2 years
                continue

            # Rolling z-score
            z_series = rolling_zscore(series, self.window_years)
            z_at_date = z_series.loc[:date].dropna()

            if z_at_date.empty:
                continue

            z_val = z_at_date.iloc[-1]

            # Invert if higher raw values mean less stress
            if series_id in self.INVERT_SERIES:
                z_val = -z_val

            # Clip extreme z-scores
            z_val = float(np.clip(z_val, -3.0, 3.0))

            components[series_id] = z_val
            weighted_sum += z_val * weight
            total_weight += weight

        if total_weight == 0:
            return 0.0, components

        # Weighted average z-score
        avg_z = weighted_sum / total_weight

        # Convert z-score to 0-100 scale using normal CDF
        # z=0 -> 50, z=2 -> ~97.7, z=-2 -> ~2.3
        from scipy import stats
        score = float(stats.norm.cdf(avg_z) * 100)

        return score, components

    def compute(self, data: pd.DataFrame, date: pd.Timestamp) -> ModelOutput:
        """Compute both FSSI and ETI for a single date."""
        fssi, fssi_components = self._compute_stage(data, date, self.fssi_weights)
        eti, eti_components = self._compute_stage(data, date, self.eti_weights)

        # Combined score: average of the two stages
        combined = (fssi + eti) / 2.0

        # Flags
        flags = []
        if fssi > 75:
            flags.append("HIGH_FINANCIAL_STRESS")
        if eti > 75:
            flags.append("HIGH_ECONOMIC_PAIN")
        if fssi > 70 and eti < 40:
            flags.append("FINANCIAL_STRESS_NOT_YET_TRANSMITTED")
        if fssi < 40 and eti > 70:
            flags.append("ECONOMIC_PAIN_WITHOUT_FINANCIAL_TRIGGER")

        return ModelOutput(
            score=combined,
            components={
                "FSSI": fssi,
                "ETI": eti,
                **{f"fssi_{k}": v for k, v in fssi_components.items()},
                **{f"eti_{k}": v for k, v in eti_components.items()},
            },
            flags=flags,
        )

    def compute_lag_analysis(
        self,
        data: pd.DataFrame,
        start: str | None = None,
        end: str | None = None,
        max_lag_months: int = 24,
    ) -> pd.DataFrame:
        """
        Compute cross-correlation between FSSI and ETI at various lags.

        This empirically tests the hypothesis that financial stress
        leads economic pain by 3-12 months.

        Returns DataFrame with lag (months) and correlation coefficient.
        """
        # Compute full historical FSSI and ETI
        historical = self.compute_historical(data, start, end)
        if historical.empty or "FSSI" not in historical.columns:
            return pd.DataFrame(columns=["lag_months", "correlation"])

        fssi_series = historical["FSSI"].dropna()
        eti_series = historical["ETI"].dropna()

        # Align
        common_idx = fssi_series.index.intersection(eti_series.index)
        if len(common_idx) < 24:
            return pd.DataFrame(columns=["lag_months", "correlation"])

        fssi_aligned = fssi_series.loc[common_idx]
        eti_aligned = eti_series.loc[common_idx]

        results = []
        for lag in range(0, max_lag_months + 1):
            if lag == 0:
                corr = fssi_aligned.corr(eti_aligned)
            else:
                # FSSI leads ETI by `lag` months
                shifted_eti = eti_aligned.shift(-lag)
                valid = ~(fssi_aligned.isna() | shifted_eti.isna())
                if valid.sum() < 12:
                    continue
                corr = fssi_aligned[valid].corr(shifted_eti[valid])

            results.append({"lag_months": lag, "correlation": corr})

        return pd.DataFrame(results)
