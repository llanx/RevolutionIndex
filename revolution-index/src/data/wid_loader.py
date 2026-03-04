"""
World Inequality Database (WID.world) data loader.

Downloads the top 1% pre-tax income share for the United States,
which is the key EMP (Elite Mobilization Potential) input for the
Turchin PSI model.

WID.world provides a public API and bulk CSV downloads.
This module uses the CSV download approach for reliability.

Usage:
    loader = WIDLoader()
    df = loader.get_top1_income_share()
"""

import logging
from pathlib import Path

import pandas as pd
import requests

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from config import RAW_WID_DIR, FETCH_START

logger = logging.getLogger(__name__)

# WID.world API endpoint for specific indicators
WID_API_URL = "https://api.wid.world/api/country-series/piinc_p99p100_992_t/US"
# Fallback: direct download URL for top 1% pre-tax national income share
WID_BULK_URL = "https://wid.world/data/"


class WIDLoader:
    """Loads World Inequality Database data for the United States."""

    def __init__(self, cache_dir: Path | None = None):
        self.cache_dir = cache_dir or RAW_WID_DIR
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._cache_path = self.cache_dir / "us_top1_income_share.csv"

    def get_top1_income_share(self, use_cache: bool = True) -> pd.DataFrame:
        """
        Get the top 1% pre-tax national income share for the US (1913-present).

        Returns DataFrame with:
        - date (DatetimeIndex, annual, Jan 1 of each year)
        - value (float, proportion 0-1, e.g. 0.20 = 20%)
        - series_id (str, "top_1pct_share")
        """
        if use_cache and self._cache_path.exists():
            logger.info("Using cached WID data")
            df = pd.read_csv(self._cache_path, parse_dates=["date"], index_col="date")
            return df

        # Try the WID API first
        try:
            df = self._fetch_from_api()
            df.to_csv(self._cache_path)
            logger.info(f"Cached WID data: {len(df)} observations")
            return df
        except Exception as e:
            logger.warning(f"WID API fetch failed: {e}")

        # If API fails and cache exists, use stale cache
        if self._cache_path.exists():
            logger.warning("Using stale WID cache")
            return pd.read_csv(self._cache_path, parse_dates=["date"], index_col="date")

        raise RuntimeError(
            "Failed to fetch WID data. Please download manually:\n"
            "1. Go to https://wid.world/data/\n"
            "2. Select: Country=USA, Indicator='Pre-tax national income', "
            "Percentile='Top 1%'\n"
            "3. Download CSV and save to: " + str(self._cache_path)
        )

    def _fetch_from_api(self) -> pd.DataFrame:
        """Fetch top 1% income share from WID API."""
        logger.info("Fetching top 1% income share from WID API...")
        resp = requests.get(
            "https://api.wid.world/api/country-series/sptinc_p99p100_992j_t/US",
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()

        # Parse API response into DataFrame
        rows = []
        for entry in data:
            year = entry.get("year")
            value = entry.get("value")
            if year and value is not None:
                rows.append({
                    "date": pd.Timestamp(f"{year}-01-01"),
                    "value": float(value),
                })

        if not rows:
            raise ValueError("WID API returned no data")

        df = pd.DataFrame(rows).set_index("date").sort_index()
        df["series_id"] = "top_1pct_share"
        return df

    def load_from_csv(self, filepath: str | Path) -> pd.DataFrame:
        """
        Load manually downloaded WID CSV file.

        Use this if the API is unavailable. Download from wid.world/data/
        and provide the file path.
        """
        raw = pd.read_csv(filepath)

        # WID CSVs typically have columns: Country, Percentile, Year, Value
        # Normalize column names
        raw.columns = [c.lower().strip() for c in raw.columns]

        year_col = next((c for c in raw.columns if "year" in c), None)
        value_col = next((c for c in raw.columns if "value" in c), None)

        if not year_col or not value_col:
            raise ValueError(
                f"Cannot parse WID CSV. Expected 'year' and 'value' columns, "
                f"got: {list(raw.columns)}"
            )

        df = pd.DataFrame({
            "date": pd.to_datetime(raw[year_col].astype(int).astype(str) + "-01-01"),
            "value": raw[value_col].astype(float),
        }).set_index("date").sort_index()
        df["series_id"] = "top_1pct_share"

        # Cache it
        df.to_csv(self._cache_path)
        logger.info(f"Loaded and cached WID CSV: {len(df)} observations")
        return df
