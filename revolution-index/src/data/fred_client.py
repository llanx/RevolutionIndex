"""
FRED API client with local file caching.

Downloads economic time series from the Federal Reserve Economic Data (FRED)
API and caches them locally as CSV files. Handles rate limiting and provides
data freshness metadata.

Usage:
    client = FREDClient()  # reads FRED_API_KEY from .env
    df = client.get_series("UNRATE")
    all_data = client.get_all_configured_series()
"""

import os
import time
import logging
from pathlib import Path
from datetime import datetime, timedelta

import pandas as pd
from fredapi import Fred
from dotenv import load_dotenv

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from config import FRED_SERIES, RAW_FRED_DIR, FETCH_START

logger = logging.getLogger(__name__)


class FREDClient:
    """Fetches and caches FRED time series data."""

    # FRED allows 120 requests/minute with an API key
    _MIN_REQUEST_INTERVAL = 0.6  # seconds between requests (safe margin)

    def __init__(self, api_key: str | None = None, cache_dir: Path | None = None):
        load_dotenv()
        key = api_key or os.getenv("FRED_API_KEY")
        if not key or key == "your_api_key_here":
            raise ValueError(
                "FRED API key not found. Set FRED_API_KEY in .env file.\n"
                "Get a free key at: https://fred.stlouisfed.org/docs/api/api_key.html"
            )
        self.fred = Fred(api_key=key)
        self.cache_dir = cache_dir or RAW_FRED_DIR
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._last_request_time = 0.0

    def _rate_limit(self):
        """Enforce minimum interval between API requests."""
        elapsed = time.time() - self._last_request_time
        if elapsed < self._MIN_REQUEST_INTERVAL:
            time.sleep(self._MIN_REQUEST_INTERVAL - elapsed)
        self._last_request_time = time.time()

    def _cache_path(self, series_id: str) -> Path:
        return self.cache_dir / f"{series_id}.csv"

    def _is_cache_fresh(self, series_id: str, max_age_hours: int = 24) -> bool:
        """Check if cached file exists and is less than max_age_hours old."""
        path = self._cache_path(series_id)
        if not path.exists():
            return False
        mtime = datetime.fromtimestamp(path.stat().st_mtime)
        return datetime.now() - mtime < timedelta(hours=max_age_hours)

    def get_series(
        self,
        series_id: str,
        start: str | None = None,
        end: str | None = None,
        use_cache: bool = True,
        max_cache_age_hours: int = 24,
    ) -> pd.DataFrame:
        """
        Fetch a single FRED series, returning a DataFrame with columns:
        - date (DatetimeIndex)
        - value (float)
        - series_id (str, for identification when merging)

        Caches to CSV locally. Returns cached version if fresh enough.
        """
        start = start or FETCH_START

        # Try cache first
        cache_path = self._cache_path(series_id)
        if use_cache and self._is_cache_fresh(series_id, max_cache_age_hours):
            logger.info(f"Using cached data for {series_id}")
            df = pd.read_csv(cache_path, parse_dates=["date"], index_col="date")
            return df

        # Fetch from API
        logger.info(f"Fetching {series_id} from FRED API...")
        self._rate_limit()
        try:
            raw = self.fred.get_series(series_id, observation_start=start, observation_end=end)
        except Exception as e:
            # If API fails but cache exists (even stale), use cache
            if cache_path.exists():
                logger.warning(f"API failed for {series_id}, using stale cache: {e}")
                return pd.read_csv(cache_path, parse_dates=["date"], index_col="date")
            raise RuntimeError(f"Failed to fetch {series_id} and no cache exists: {e}") from e

        # Convert to DataFrame
        df = pd.DataFrame({"value": raw})
        df.index.name = "date"
        df["series_id"] = series_id

        # Drop NaN values (FRED sometimes returns "." as missing)
        df = df.dropna(subset=["value"])

        # Cache to disk
        df.to_csv(cache_path)
        logger.info(f"Cached {series_id}: {len(df)} observations, {df.index.min()} to {df.index.max()}")

        return df

    def get_series_metadata(self, series_id: str) -> dict:
        """Fetch metadata for a FRED series (title, frequency, last updated)."""
        self._rate_limit()
        info = self.fred.get_series_info(series_id)
        return {
            "series_id": series_id,
            "title": info.get("title", ""),
            "frequency": info.get("frequency", ""),
            "last_updated": str(info.get("last_updated", "")),
            "observation_start": str(info.get("observation_start", "")),
            "observation_end": str(info.get("observation_end", "")),
        }

    def get_all_configured_series(
        self, use_cache: bool = True
    ) -> dict[str, pd.DataFrame]:
        """
        Download all series defined in config.FRED_SERIES.
        Returns dict of {series_id: DataFrame}.
        """
        results = {}
        total = len(FRED_SERIES)
        for i, series_id in enumerate(FRED_SERIES, 1):
            desc = FRED_SERIES[series_id]["description"]
            logger.info(f"[{i}/{total}] {series_id}: {desc}")
            try:
                results[series_id] = self.get_series(series_id, use_cache=use_cache)
            except Exception as e:
                logger.error(f"Failed to fetch {series_id}: {e}")
                continue
        return results

    def get_catalog_summary(self) -> pd.DataFrame:
        """Return a summary of all cached series with date ranges and observation counts."""
        rows = []
        for series_id, meta in FRED_SERIES.items():
            cache_path = self._cache_path(series_id)
            if cache_path.exists():
                df = pd.read_csv(cache_path, parse_dates=["date"], index_col="date")
                rows.append({
                    "series_id": series_id,
                    "description": meta["description"],
                    "frequency": meta["frequency"],
                    "model": meta["model"],
                    "component": meta["component"],
                    "observations": len(df),
                    "start": str(df.index.min().date()) if len(df) > 0 else None,
                    "end": str(df.index.max().date()) if len(df) > 0 else None,
                    "cached": True,
                })
            else:
                rows.append({
                    "series_id": series_id,
                    "description": meta["description"],
                    "frequency": meta["frequency"],
                    "model": meta["model"],
                    "component": meta["component"],
                    "observations": 0,
                    "start": None,
                    "end": None,
                    "cached": False,
                })
        return pd.DataFrame(rows)
