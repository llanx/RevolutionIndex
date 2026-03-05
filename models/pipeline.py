"""
Data pipeline: fetch from APIs, load cached manual data, align frequencies via LOCF,
produce unified DataFrame for model consumption.

Pipeline is idempotent: running it twice produces the same output.

Usage:
    $ export FRED_API_KEY=your_key_here
    $ python pipeline.py

Obtain a free FRED API key at: https://fred.stlouisfed.org/docs/api/api_key.html
"""
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import pandas as pd
import numpy as np

from config import (
    VARIABLES,
    FRESHNESS_CONFIG,
    EVIDENCE_WEIGHTS,
    DOMAIN_WEIGHTS,
    NORMALIZATION_CONFIG,
    Variable,
    SourceType,
    NormDirection,
    Domain,
    get_variables_by_domain,
)
from normalize import normalize_variable
from fetchers import try_auto_fetch


# ---------------------------------------------------------------------------
# Data directories (relative to this file's location)
# ---------------------------------------------------------------------------

_BASE_DIR = Path(__file__).resolve().parent.parent
_CACHE_DIR = _BASE_DIR / FRESHNESS_CONFIG["cache_dir"]
_FRED_CACHE_DIR = _CACHE_DIR / "fred"
_FRESHNESS_FILE = _BASE_DIR / FRESHNESS_CONFIG["freshness_file"]


def _ensure_dirs() -> None:
    """Create cache directories if they do not exist."""
    _FRED_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    _FRESHNESS_FILE.parent.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# FRED API fetching
# ---------------------------------------------------------------------------

def fetch_fred_series(
    series_id: str,
    api_key: str,
    start_date: str = "1947-01-01",
) -> pd.Series:
    """
    Fetch a single FRED series. Returns pd.Series with DatetimeIndex.

    Uses the fredapi library. Caches to data/raw/fred/{series_id}.csv to avoid
    re-fetching on subsequent runs.

    Parameters
    ----------
    series_id : str
        FRED series identifier (e.g., "UNRATE").
    api_key : str
        FRED API key.
    start_date : str
        Earliest date to fetch (ISO format).

    Returns
    -------
    pd.Series
        Time series with DatetimeIndex and float values.
    """
    _ensure_dirs()
    cache_path = _FRED_CACHE_DIR / f"{series_id}.csv"

    # Check if cached and fresh
    if cache_path.exists():
        freshness = get_freshness()
        source_key = f"fred_{series_id}"
        if source_key in freshness:
            last_fetch = datetime.fromisoformat(freshness[source_key])
            age_days = (datetime.now(timezone.utc) - last_fetch).days
            if age_days < FRESHNESS_CONFIG["stale_threshold_days"]:
                cached = pd.read_csv(
                    cache_path, index_col=0, parse_dates=True
                ).squeeze("columns")
                return cached

    # Fetch from FRED API
    from fredapi import Fred

    fred = Fred(api_key=api_key)
    series = fred.get_series(series_id, observation_start=start_date)
    series.name = series_id
    series.index.name = "date"

    # Cache to CSV
    series.to_csv(cache_path, header=True)

    # Update freshness
    update_freshness(f"fred_{series_id}")

    return series


# ---------------------------------------------------------------------------
# Manual source loading
# ---------------------------------------------------------------------------

def load_manual_source(variable: Variable) -> Optional[pd.Series]:
    """
    Load a manually-downloaded data file from data/raw/{source_name}/.

    Supports CSV and Excel (.xlsx) formats. The file must have a date column
    and a value column. The pipeline expects the user to place downloaded
    files in the appropriate data/raw/ subdirectory.

    Parameters
    ----------
    variable : Variable
        Variable configuration object with manual_source metadata.

    Returns
    -------
    pd.Series or None
        Time series with DatetimeIndex, or None if file not found.
    """
    _ensure_dirs()

    # Look for cached data files matching the catalog number
    var_dir = _CACHE_DIR / f"var_{variable.catalog_number}"
    if not var_dir.exists():
        return None

    # Try CSV files first, then Excel
    for pattern in ["*.csv", "*.xlsx"]:
        files = list(var_dir.glob(pattern))
        if files:
            fpath = files[0]  # Use the first matching file
            if fpath.suffix == ".csv":
                df = pd.read_csv(fpath, parse_dates=[0])
            else:
                df = pd.read_excel(fpath, parse_dates=[0])

            # Assume first column is date, second is value
            df.columns = ["date", "value"]
            df = df.set_index("date").sort_index()
            series = df["value"].astype(float)
            series.name = str(variable.catalog_number)

            update_freshness(f"manual_{variable.catalog_number}")
            return series

    return None


# ---------------------------------------------------------------------------
# Constructed variable proxies
# ---------------------------------------------------------------------------

def construct_proxy(
    variable: Variable,
    raw_data: dict[str, pd.Series],
) -> Optional[pd.Series]:
    """
    Construct a proxy variable from component series.

    Reads construction_recipe from variable config and applies the appropriate
    calculation. For constructed variables that depend on FRED series, those
    component series should be pre-fetched and passed in raw_data.

    Parameters
    ----------
    variable : Variable
        Variable configuration with construction_recipe.
    raw_data : dict[str, pd.Series]
        Dictionary of already-fetched raw series, keyed by series ID or
        catalog number string.

    Returns
    -------
    pd.Series or None
        Constructed proxy series, or None if required components are missing.
    """
    cat_num = variable.catalog_number

    # #14: Relative Deprivation (UMCSENT - GDP gap)
    if cat_num == 14:
        umcsent = raw_data.get("UMCSENT")
        gdp = raw_data.get("A191RL1Q225SBEA")
        if umcsent is None or gdp is None:
            return None
        # Align to common index
        umcsent_m = umcsent.resample("ME").last().ffill()
        gdp_m = gdp.resample("ME").last().ffill()
        common = umcsent_m.index.intersection(gdp_m.index)
        if len(common) == 0:
            return None
        # Compute z-scores for each component (10-year window = 120 months)
        from normalize import rolling_zscore
        sent_z = rolling_zscore(umcsent_m.loc[common], window=120)
        gdp_z = rolling_zscore(gdp_m.loc[common], window=120)
        gap = sent_z - gdp_z  # positive = expectations above reality
        gap.name = str(cat_num)
        return gap

    # #40: Cost of Living Pressure (weighted CPI components)
    if cat_num == 40:
        shelter = raw_data.get("CUSR0000SAH1")
        food = raw_data.get("CPIFABSL")
        energy = raw_data.get("CPIENGSL")
        medical = raw_data.get("CPIMEDSL")
        if any(s is None for s in [shelter, food, energy, medical]):
            return None
        # Compute YoY growth for each component
        components = {
            "shelter": shelter.pct_change(periods=12) * 100,
            "food": food.pct_change(periods=12) * 100,
            "energy": energy.pct_change(periods=12) * 100,
            "medical": medical.pct_change(periods=12) * 100,
        }
        # Budget weights (approximate median household)
        weights = {"shelter": 0.33, "food": 0.13, "energy": 0.07, "medical": 0.09}
        # Normalize weights to sum to 1.0
        w_sum = sum(weights.values())
        weights = {k: v / w_sum for k, v in weights.items()}
        # Combine
        combined = pd.DataFrame(components)
        common = combined.dropna()
        if len(common) == 0:
            return None
        pressure = sum(common[k] * weights[k] for k in weights)
        pressure.name = str(cat_num)
        return pressure

    # #19: Intra-Elite Wealth Gap (ratio within top 1%)
    if cat_num == 19:
        top01 = raw_data.get("WFRBSTP1300")     # Top 0.1% net worth share
        top1 = raw_data.get("WFRBST01134")       # Top 1% net worth share
        if top01 is None or top1 is None:
            return None
        # Align to common quarterly index
        top01_q = top01.resample("QE").last().dropna()
        top1_q = top1.resample("QE").last().dropna()
        common = top01_q.index.intersection(top1_q.index)
        if len(common) == 0:
            return None
        top01_aligned = top01_q.loc[common]
        top1_aligned = top1_q.loc[common]
        # Ratio: top 0.1% share / (top 1% share - top 0.1% share)
        # Denominator is the "rest of the top 1%" (0.1%-1%)
        denominator = top1_aligned - top01_aligned
        # Avoid division by zero or negative
        denominator = denominator.clip(lower=0.01)
        ratio = top01_aligned / denominator
        ratio.name = str(cat_num)
        return ratio

    # #8: Elite Overproduction (education-job mismatch)
    # This requires Census ACS and BLS JOLTS data that must be manually loaded
    if cat_num == 8:
        return load_manual_source(variable)

    # #11: Elite Factionalism (intra-party DW-NOMINATE SD)
    if cat_num == 11:
        result = try_auto_fetch(variable)
        if result is not None:
            return result
        return load_manual_source(variable)

    # #36: Protest Diffusion (ACLED-derived)
    if cat_num == 36:
        result = try_auto_fetch(variable)
        if result is not None:
            return result
        return load_manual_source(variable)

    # #37: Prior Protest Experience (ACLED-derived)
    if cat_num == 37:
        result = try_auto_fetch(variable)
        if result is not None:
            return result
        return load_manual_source(variable)

    return None


# ---------------------------------------------------------------------------
# Frequency alignment
# ---------------------------------------------------------------------------

def align_to_monthly(series: pd.Series, native_freq: str) -> pd.Series:
    """
    Align any frequency to monthly using LOCF (last observation carried forward).

    - Monthly: pass through
    - Weekly/daily: resample to month-end, take last observation
    - Quarterly: forward-fill to monthly
    - Annual: forward-fill to monthly
    - Biennial/irregular: forward-fill to monthly

    No interpolation is used. Only ffill() for LOCF.

    Parameters
    ----------
    series : pd.Series
        Time series with DatetimeIndex.
    native_freq : str
        One of: "daily", "weekly", "monthly", "quarterly", "annual",
        "biennial", "irregular".

    Returns
    -------
    pd.Series
        Monthly-frequency series (month-end dates).
    """
    if series.empty:
        return series

    # Ensure DatetimeIndex
    if not isinstance(series.index, pd.DatetimeIndex):
        series.index = pd.to_datetime(series.index)

    if native_freq in ("daily", "weekly"):
        # Downsample: take last observation of each month
        monthly = series.resample("ME").last()
    elif native_freq == "monthly":
        # Already monthly, just ensure month-end alignment
        monthly = series.resample("ME").last()
    elif native_freq in ("quarterly", "annual", "biennial", "irregular"):
        # Upsample: resample to month-end, then forward-fill (LOCF)
        monthly = series.resample("ME").last().ffill()
    else:
        # Default: resample and forward-fill
        monthly = series.resample("ME").last().ffill()

    return monthly


# ---------------------------------------------------------------------------
# Freshness tracking
# ---------------------------------------------------------------------------

def update_freshness(source_id: str, timestamp: Optional[datetime] = None) -> None:
    """
    Record last-fetch timestamp for a data source.

    Parameters
    ----------
    source_id : str
        Identifier for the data source (e.g., "fred_UNRATE").
    timestamp : datetime or None
        Fetch timestamp. Defaults to current UTC time.
    """
    _ensure_dirs()
    freshness = get_freshness()
    if timestamp is None:
        timestamp = datetime.now(timezone.utc)
    freshness[source_id] = timestamp.isoformat()

    with open(_FRESHNESS_FILE, "w") as f:
        json.dump(freshness, f, indent=2)


def get_freshness() -> dict:
    """Load freshness metadata from data/freshness.json."""
    if _FRESHNESS_FILE.exists():
        with open(_FRESHNESS_FILE) as f:
            return json.load(f)
    return {}


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def fetch_all(api_key: str, start_year: int = 1947) -> pd.DataFrame:
    """
    Main pipeline entry point.

    1. For each variable in VARIABLES:
       a. If FRED_API: fetch via fredapi, cache to data/raw/fred/
       b. If MANUAL_DOWNLOAD: load from data/raw/ cache
       c. If CONSTRUCTED: build from available component series
    2. Align all series to monthly frequency via LOCF
    3. Normalize each series to 0.0-1.0 stress intensity
    4. Combine into unified DataFrame with columns = variable catalog numbers
    5. Update freshness metadata

    Parameters
    ----------
    api_key : str
        FRED API key.
    start_year : int
        Earliest year to fetch (default 1947 for maximum backtesting coverage).

    Returns
    -------
    pd.DataFrame
        Unified DataFrame with DatetimeIndex (monthly), columns named by
        catalog number (as string), values in 0.0-1.0 range (stress intensity).
    """
    _ensure_dirs()
    start_date = f"{start_year}-01-01"

    # Phase 1: Fetch all FRED series first (needed for constructed variables)
    raw_data: dict[str, pd.Series] = {}
    fred_vars = [v for v in VARIABLES if v.source_type == SourceType.FRED_API]

    print(f"Fetching {len(fred_vars)} FRED series...")
    for var in fred_vars:
        try:
            series = fetch_fred_series(var.series_id, api_key, start_date)
            raw_data[var.series_id] = series
            print(f"  [{var.catalog_number}] {var.series_id}: "
                  f"{len(series)} observations")
        except Exception as e:
            print(f"  [{var.catalog_number}] {var.series_id}: FAILED - {e}")

    # Also fetch component series needed for constructed variables
    component_series = [
        # CPI components for constructed variable #40
        "CUSR0000SAH1", "CPIFABSL", "CPIENGSL", "CPIMEDSL",
        # Top 1% wealth share for constructed variable #19 (intra-elite ratio)
        "WFRBST01134",
    ]
    for sid in component_series:
        if sid not in raw_data:
            try:
                raw_data[sid] = fetch_fred_series(sid, api_key, start_date)
                print(f"  [component] {sid}: "
                      f"{len(raw_data[sid])} observations")
            except Exception as e:
                print(f"  [component] {sid}: FAILED - {e}")

    # Phase 2: Load manual download data (try auto-fetch first)
    manual_vars = [v for v in VARIABLES if v.source_type == SourceType.MANUAL_DOWNLOAD]
    print(f"\nLoading {len(manual_vars)} manual download variables...")
    for var in manual_vars:
        # Try automated fetcher first
        series = try_auto_fetch(var)
        if series is not None:
            raw_data[str(var.catalog_number)] = series
            print(f"  [{var.catalog_number}] {var.name}: "
                  f"{len(series)} observations (auto-fetched)")
            continue

        # Fall back to manually-placed cached file
        series = load_manual_source(var)
        if series is not None:
            raw_data[str(var.catalog_number)] = series
            print(f"  [{var.catalog_number}] {var.name}: "
                  f"{len(series)} observations (cached)")
        else:
            print(f"  [{var.catalog_number}] {var.name}: "
                  f"NOT AVAILABLE (auto-fetch failed, no cache in "
                  f"data/raw/var_{var.catalog_number}/)")

    # Phase 3: Construct proxy variables
    constructed_vars = [
        v for v in VARIABLES if v.source_type == SourceType.CONSTRUCTED
    ]
    print(f"\nConstructing {len(constructed_vars)} proxy variables...")
    for var in constructed_vars:
        series = construct_proxy(var, raw_data)
        if series is not None:
            raw_data[str(var.catalog_number)] = series
            print(f"  [{var.catalog_number}] {var.name}: "
                  f"{len(series)} observations")
        else:
            print(f"  [{var.catalog_number}] {var.name}: "
                  f"MISSING COMPONENTS")

    # Phase 4: Align all series to monthly and normalize
    print("\nAligning to monthly frequency and normalizing...")
    normalized: dict[str, pd.Series] = {}
    raw_aligned: dict[str, pd.Series] = {}
    window = NORMALIZATION_CONFIG["rolling_window_months"]

    for var in VARIABLES:
        # Determine the key used in raw_data
        if var.source_type == SourceType.FRED_API:
            key = var.series_id
        else:
            key = str(var.catalog_number)

        if key not in raw_data:
            print(f"  [{var.catalog_number}] SKIPPED (no data)")
            continue

        series = raw_data[key]

        # Align to monthly
        monthly = align_to_monthly(series, var.frequency)

        # Store raw aligned series (pre-normalization) for models that
        # need original values (e.g., V-Dem rate-of-change computation)
        raw_aligned[str(var.catalog_number)] = monthly

        # Normalize to 0.0-1.0 stress intensity
        direction = var.norm_direction.value
        stress = normalize_variable(monthly, direction=direction, window=window)

        normalized[str(var.catalog_number)] = stress
        valid_count = stress.dropna().shape[0]
        print(f"  [{var.catalog_number}] {var.name}: "
              f"{valid_count} normalized observations")

    # Phase 5: Combine into unified DataFrame
    if not normalized:
        print("\nWARNING: No variables were successfully processed.")
        return pd.DataFrame(), pd.DataFrame()

    unified = pd.DataFrame(normalized)
    unified = unified.sort_index()

    raw_unified = pd.DataFrame(raw_aligned)
    raw_unified = raw_unified.sort_index()

    print(f"\nUnified DataFrame: {unified.shape[0]} months x "
          f"{unified.shape[1]} variables")
    print(f"Date range: {unified.index.min()} to {unified.index.max()}")

    return unified, raw_unified


# ---------------------------------------------------------------------------
# Domain score aggregation
# ---------------------------------------------------------------------------

def compute_domain_scores(unified_df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate variable-level scores into domain-level scores using
    evidence-strength weighted averages within each domain.

    For each domain and each month, computes the weighted average of all
    available variable scores. Variables with NaN for a given month are
    excluded from that month's average (not treated as zero).

    Parameters
    ----------
    unified_df : pd.DataFrame
        Unified DataFrame from fetch_all() with columns = catalog numbers
        (as strings) and values in 0.0-1.0 range.

    Returns
    -------
    pd.DataFrame
        DataFrame with columns for each domain (using Domain enum values)
        and values in 0.0-1.0 range.
    """
    domain_scores: dict[str, pd.Series] = {}

    for domain in Domain:
        domain_vars = get_variables_by_domain(domain)

        # Map catalog numbers to evidence weights
        var_weights = {}
        for var in domain_vars:
            col = str(var.catalog_number)
            if col in unified_df.columns:
                var_weights[col] = EVIDENCE_WEIGHTS[var.evidence_rating]

        if not var_weights:
            continue

        # Compute weighted average per month, excluding NaN
        domain_df = unified_df[list(var_weights.keys())]
        weights = pd.Series(var_weights)

        # For each row, compute weighted average of non-NaN values
        def weighted_mean(row):
            valid = row.dropna()
            if len(valid) == 0:
                return np.nan
            w = weights.loc[valid.index]
            return (valid * w).sum() / w.sum()

        domain_scores[domain.value] = domain_df.apply(weighted_mean, axis=1)

    return pd.DataFrame(domain_scores)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    """Run the full pipeline from the command line."""
    api_key = os.environ.get("FRED_API_KEY")
    if not api_key:
        print("ERROR: FRED_API_KEY environment variable not set.")
        print("Get a free key at: https://fred.stlouisfed.org/docs/api/api_key.html")
        print("Then: export FRED_API_KEY=your_key_here")
        sys.exit(1)

    print("=" * 70)
    print("Revolution Index Data Pipeline")
    print("=" * 70)
    print()

    unified, _raw = fetch_all(api_key)

    if unified.empty:
        print("\nPipeline produced no data. Check errors above.")
        sys.exit(1)

    # Compute domain scores
    print("\nComputing domain scores...")
    domains = compute_domain_scores(unified)
    print(f"Domain scores: {domains.shape[0]} months x {domains.shape[1]} domains")

    # Save outputs
    output_dir = _BASE_DIR / "data"
    output_dir.mkdir(parents=True, exist_ok=True)

    unified_path = output_dir / "unified_variables.csv"
    unified.to_csv(unified_path)
    print(f"\nSaved unified variables to: {unified_path}")

    domains_path = output_dir / "domain_scores.csv"
    domains.to_csv(domains_path)
    print(f"Saved domain scores to: {domains_path}")

    # Summary statistics
    print("\n" + "=" * 70)
    print("Pipeline Summary")
    print("=" * 70)
    print(f"Total variables configured: {len(VARIABLES)}")
    print(f"Variables with data: {unified.shape[1]}")
    print(f"Date range: {unified.index.min()} to {unified.index.max()}")
    print(f"Domains computed: {domains.shape[1]}")
    for col in domains.columns:
        latest = domains[col].dropna().iloc[-1] if not domains[col].dropna().empty else "N/A"
        print(f"  {col}: latest = {latest:.3f}" if isinstance(latest, float) else f"  {col}: {latest}")
    print()
    print("Domain weights:")
    for domain, weight in DOMAIN_WEIGHTS.items():
        print(f"  {domain.value}: {weight:.2f}")


if __name__ == "__main__":
    main()
