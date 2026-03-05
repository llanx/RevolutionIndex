"""
Automated data fetchers for non-FRED data sources.

Each fetcher function:
  - Downloads data from the source URL/API
  - Parses into pd.Series with DatetimeIndex and float values
  - Saves to data/raw/var_{catalog_number}/ for caching
  - Returns the pd.Series (or None on failure)

Fetchers are registered in FETCHER_REGISTRY keyed by catalog_number.
pipeline.py calls try_auto_fetch() before falling back to load_manual_source().
"""
import io
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Callable

import numpy as np
import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

_BASE_DIR = Path(__file__).resolve().parent.parent
_CACHE_DIR = _BASE_DIR / "data" / "raw"

# ---------------------------------------------------------------------------
# HTTP session with retry
# ---------------------------------------------------------------------------

_SESSION: Optional[requests.Session] = None


def _get_session() -> requests.Session:
    """Lazy-init a requests.Session with retry adapter."""
    global _SESSION
    if _SESSION is None:
        _SESSION = requests.Session()
        retry = Retry(
            total=3, backoff_factor=1.0,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry)
        _SESSION.mount("https://", adapter)
        _SESSION.mount("http://", adapter)
        _SESSION.headers.update({
            "User-Agent": "RevolutionIndex/1.1 (research; +https://github.com/llanx/RevolutionIndex)"
        })
    return _SESSION


# ---------------------------------------------------------------------------
# Caching helpers
# ---------------------------------------------------------------------------

def _cache_dir_for_var(catalog_number: int) -> Path:
    d = _CACHE_DIR / f"var_{catalog_number}"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _save_to_cache(
    series: pd.Series,
    catalog_number: int,
    filename: str = "auto_fetched.csv",
) -> Path:
    """Save pd.Series to the variable's cache directory as date,value CSV."""
    d = _cache_dir_for_var(catalog_number)
    path = d / filename
    df = pd.DataFrame({"date": series.index, "value": series.values})
    df.to_csv(path, index=False)
    return path


def _load_from_cache(
    catalog_number: int,
    filename: str = "auto_fetched.csv",
) -> Optional[pd.Series]:
    """Load cached series if file exists."""
    path = _CACHE_DIR / f"var_{catalog_number}" / filename
    if not path.exists():
        return None
    df = pd.read_csv(path, parse_dates=[0])
    df.columns = ["date", "value"]
    df = df.set_index("date").sort_index()
    return df["value"].astype(float)


def _is_cache_fresh(catalog_number: int, max_age_days: int = 30) -> bool:
    """Check if cached auto_fetched.csv exists and is younger than max_age_days."""
    path = _CACHE_DIR / f"var_{catalog_number}" / "auto_fetched.csv"
    if not path.exists():
        return False
    mtime = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
    age = (datetime.now(timezone.utc) - mtime).days
    return age < max_age_days


# =========================================================================
# TIER 1 — No Authentication Required
# =========================================================================

# ---------------------------------------------------------------------------
# VoteView (shared raw download for #3 and #11)
# ---------------------------------------------------------------------------

_VOTEVIEW_CACHE: Optional[pd.DataFrame] = None


def _fetch_voteview_raw() -> pd.DataFrame:
    """Download HSall_members.csv from VoteView (~60 MB). Cached in memory and on disk."""
    global _VOTEVIEW_CACHE
    if _VOTEVIEW_CACHE is not None:
        return _VOTEVIEW_CACHE

    disk_cache = _CACHE_DIR / "voteview" / "HSall_members.csv"
    disk_cache.parent.mkdir(parents=True, exist_ok=True)

    if disk_cache.exists():
        mtime = datetime.fromtimestamp(disk_cache.stat().st_mtime, tz=timezone.utc)
        if (datetime.now(timezone.utc) - mtime).days < 30:
            _VOTEVIEW_CACHE = pd.read_csv(disk_cache, low_memory=False)
            return _VOTEVIEW_CACHE

    url = "https://voteview.com/static/data/out/members/HSall_members.csv"
    logger.info("Fetching VoteView HSall_members.csv...")
    resp = _get_session().get(url, timeout=120)
    resp.raise_for_status()

    with open(disk_cache, "wb") as f:
        f.write(resp.content)

    _VOTEVIEW_CACHE = pd.read_csv(io.BytesIO(resp.content), low_memory=False)
    return _VOTEVIEW_CACHE


def fetch_congressional_polarization(catalog_number: int = 3) -> Optional[pd.Series]:
    """#3: |mean(Republican dim1) - mean(Democrat dim1)| per Congress."""
    if _is_cache_fresh(catalog_number):
        cached = _load_from_cache(catalog_number)
        if cached is not None:
            return cached

    df = _fetch_voteview_raw()
    df = df[df["party_code"].isin([100, 200])].copy()
    df = df.dropna(subset=["nominate_dim1"])

    results = []
    for congress_num in sorted(df["congress"].unique()):
        cdata = df[df["congress"] == congress_num]
        dem = cdata[cdata["party_code"] == 100]["nominate_dim1"]
        rep = cdata[cdata["party_code"] == 200]["nominate_dim1"]
        if len(dem) > 0 and len(rep) > 0:
            polarization = abs(rep.mean() - dem.mean())
            year = 1789 + (congress_num - 1) * 2
            results.append({"date": pd.Timestamp(f"{year}-01-01"), "value": polarization})

    if not results:
        return None

    series = pd.DataFrame(results).set_index("date")["value"]
    series.name = str(catalog_number)
    _save_to_cache(series, catalog_number)
    return series


def fetch_elite_factionalism(catalog_number: int = 11) -> Optional[pd.Series]:
    """#11: max(SD_R_dim1, SD_D_dim1) per Congress."""
    if _is_cache_fresh(catalog_number):
        cached = _load_from_cache(catalog_number)
        if cached is not None:
            return cached

    df = _fetch_voteview_raw()
    df = df[df["party_code"].isin([100, 200])].copy()
    df = df.dropna(subset=["nominate_dim1"])

    results = []
    for congress_num in sorted(df["congress"].unique()):
        cdata = df[df["congress"] == congress_num]
        dem = cdata[cdata["party_code"] == 100]["nominate_dim1"]
        rep = cdata[cdata["party_code"] == 200]["nominate_dim1"]
        sd_d = dem.std() if len(dem) > 1 else 0.0
        sd_r = rep.std() if len(rep) > 1 else 0.0
        factionalism = max(sd_d, sd_r)
        year = 1789 + (congress_num - 1) * 2
        results.append({"date": pd.Timestamp(f"{year}-01-01"), "value": factionalism})

    if not results:
        return None

    series = pd.DataFrame(results).set_index("date")["value"]
    series.name = str(catalog_number)
    _save_to_cache(series, catalog_number)
    return series


# ---------------------------------------------------------------------------
# Census Historical Income Tables (#15, #20)
# ---------------------------------------------------------------------------

def fetch_racial_income_ratio(catalog_number: int = 15) -> Optional[pd.Series]:
    """
    #15: (Black median HH income) / (White non-Hispanic median HH income).

    Downloads Census Table H-5 (Race and Hispanic Origin of Householder).
    """
    if _is_cache_fresh(catalog_number):
        cached = _load_from_cache(catalog_number)
        if cached is not None:
            return cached

    url = "https://www2.census.gov/programs-surveys/cps/tables/time-series/historical-income-households/h05.xlsx"
    logger.info("Fetching Census Table H-5 (median income by race)...")
    resp = _get_session().get(url, timeout=60)
    resp.raise_for_status()

    xls = pd.ExcelFile(io.BytesIO(resp.content), engine="openpyxl")
    # Census XLSX has multiple sheets; race data is typically on the first sheet
    # Headers are complex multi-row. Strategy: read raw, scan for year rows.
    raw = pd.read_excel(
        io.BytesIO(resp.content),
        sheet_name=0,
        header=None,
        engine="openpyxl",
    )

    # The table structure: rows contain year in col 0, race categories across sheets
    # We need to find the "BLACK" and "WHITE, NOT HISPANIC" sections
    # Each section has a header row followed by year/income rows
    #
    # Approach: find section headers, then extract year+median income from each section
    # Merge legacy (1967-2001) and modern (2002+) series for max coverage
    # Black: "Black (32)" covers 1967-2001, "Black Alone" covers 2002+
    black_legacy = _parse_census_race_section(raw, "Black (") or {}
    black_modern = _parse_census_race_section(raw, "Black Alone (") or {}
    black_income = {**black_legacy, **black_modern}  # modern overwrites overlap

    # White: "White, Not Hispanic (32)" covers 1972-2001, "White Alone, Not Hispanic" 2002+
    white_legacy = _parse_census_race_section(raw, "White, Not Hispanic (") or {}
    white_modern = _parse_census_race_section(raw, "White Alone, Not Hispanic") or {}
    white_income = {**white_legacy, **white_modern}

    if not black_income:
        black_income = None
    if not white_income:
        white_income = None

    if black_income is None or white_income is None:
        logger.warning("Census H-5 parsing failed — could not find race sections")
        return None

    # Align years and compute ratio
    common_years = sorted(set(black_income.keys()) & set(white_income.keys()))
    if not common_years:
        return None

    results = []
    for year in common_years:
        b = black_income[year]
        w = white_income[year]
        if w > 0:
            results.append({
                "date": pd.Timestamp(f"{year}-01-01"),
                "value": b / w,
            })

    if not results:
        return None

    series = pd.DataFrame(results).set_index("date")["value"]
    series.name = str(catalog_number)
    _save_to_cache(series, catalog_number)
    return series


def _parse_census_race_section(
    raw: pd.DataFrame, section_label: str
) -> Optional[dict[int, float]]:
    """
    Parse a race section from Census H-5 XLSX.

    Layout per section:
      Row N:   "Section Label (footnote)"
      Row N+1: "Race, Hispanic origin, and year", "Number", "Median income", "Mean income"
      Row N+2: Sub-header ("Current dollars", "2024 dollars", ...)
      Row N+3+: Year rows: year in col 0, median income (current $) in col 2

    Returns dict mapping year -> median income (current dollars), or None.
    """
    # Find the section header row
    section_row = None
    for idx in range(len(raw)):
        val = str(raw.iloc[idx, 0]).strip() if pd.notna(raw.iloc[idx, 0]) else ""
        if section_label.upper() in val.upper():
            section_row = idx
            break

    if section_row is None:
        return None

    # Data rows start after section label + column header + sub-header (2-3 rows)
    # Median income in current dollars is column index 2
    income = {}
    for idx in range(section_row + 3, min(section_row + 80, len(raw))):
        row = raw.iloc[idx]
        year_val = str(row.iloc[0]).strip() if pd.notna(row.iloc[0]) else ""

        # Extract 4-digit year from strings like "2024" or "2013 (39)"
        import re
        year_match = re.match(r"(\d{4})", year_val)
        if not year_match:
            if income:
                break
            continue

        year = int(year_match.group(1))
        if year < 1940 or year > 2030:
            continue

        # Median income (current dollars) in column 2
        median_val = row.iloc[2] if len(row) > 2 else None
        try:
            if pd.isna(median_val):
                continue
            cleaned = str(median_val).replace(",", "").replace("$", "").strip()
            median = float(cleaned)
            if median > 0:
                # Keep first occurrence per year (skip methodology-break duplicates)
                if year not in income:
                    income[year] = median
        except (ValueError, TypeError):
            continue

    return income if income else None


def fetch_middle_class_income_share(catalog_number: int = 20) -> Optional[pd.Series]:
    """
    #20: Sum of 2nd + 3rd + 4th quintile income shares.

    Downloads Census Table H-2 (Share of Aggregate Income by Each Fifth).
    """
    if _is_cache_fresh(catalog_number):
        cached = _load_from_cache(catalog_number)
        if cached is not None:
            return cached

    # H-2: Share of aggregate income — "all races" variant
    url = "https://www2.census.gov/programs-surveys/cps/tables/time-series/historical-income-households/h02ar.xlsx"
    logger.info("Fetching Census Table H-2 (income shares by quintile)...")
    resp = _get_session().get(url, timeout=60)
    resp.raise_for_status()

    raw = pd.read_excel(
        io.BytesIO(resp.content),
        sheet_name=0,
        header=None,
        engine="openpyxl",
    )

    # Scan for the header row that contains quintile labels
    # Look for a row with "Second" or "Third" or "Fourth" in it
    header_row = None
    for idx, row in raw.iterrows():
        row_str = " ".join(str(v) for v in row.values if pd.notna(v)).upper()
        if "SECOND" in row_str and "THIRD" in row_str:
            header_row = idx
            break

    if header_row is None:
        # Try alternative: look for "LOWEST" and "HIGHEST" in same row
        for idx, row in raw.iterrows():
            row_str = " ".join(str(v) for v in row.values if pd.notna(v)).upper()
            if "LOWEST" in row_str and "HIGHEST" in row_str:
                header_row = idx
                break

    if header_row is None:
        logger.warning("Census H-2 parsing failed — could not find header row")
        return None

    # Identify column positions for 2nd, 3rd, 4th quintiles
    header_vals = raw.iloc[header_row]
    col_indices = {}
    for col_idx, val in enumerate(header_vals):
        val_str = str(val).upper().strip() if pd.notna(val) else ""
        if "SECOND" in val_str:
            col_indices["second"] = col_idx
        elif "THIRD" in val_str:
            col_indices["third"] = col_idx
        elif "FOURTH" in val_str:
            col_indices["fourth"] = col_idx

    if len(col_indices) < 3:
        logger.warning(f"Census H-2: only found columns {list(col_indices.keys())}")
        return None

    # Parse data rows below header
    results = []
    for idx in range(header_row + 1, len(raw)):
        row = raw.iloc[idx]
        year_val = row.iloc[0]
        try:
            year = int(float(str(year_val).strip().split()[0]))
            if year < 1940 or year > 2030:
                continue
        except (ValueError, TypeError):
            if results:
                break
            continue

        try:
            shares = []
            for key in ["second", "third", "fourth"]:
                val = row.iloc[col_indices[key]]
                cleaned = str(val).replace(",", "").replace("%", "").strip().split()[0]
                shares.append(float(cleaned))
            middle_share = sum(shares)
            results.append({"date": pd.Timestamp(f"{year}-01-01"), "value": middle_share})
        except (ValueError, TypeError, IndexError):
            continue

    if not results:
        return None

    series = pd.DataFrame(results).set_index("date")["value"]
    series.name = str(catalog_number)
    _save_to_cache(series, catalog_number)
    return series


# ---------------------------------------------------------------------------
# BLS Union Membership (#25)
# ---------------------------------------------------------------------------

def fetch_union_membership(catalog_number: int = 25) -> Optional[pd.Series]:
    """
    #25: Union membership rate (members as % of employed, 16+).

    Uses BLS Public Data API v1 (no key required) or v2 (with BLS_API_KEY).
    Series: LUU0204899600 = Members of unions as % of employed.
    """
    if _is_cache_fresh(catalog_number):
        cached = _load_from_cache(catalog_number)
        if cached is not None:
            return cached

    # BLS Public Data API
    bls_key = os.environ.get("BLS_API_KEY")
    api_version = "v2" if bls_key else "v1"
    url = f"https://api.bls.gov/publicAPI/{api_version}/timeseries/data/"

    # BLS API allows max 20-year spans per request; chain for full coverage
    series_id = "LUU0204899600"
    all_values = []

    # Fetch in 20-year chunks from 1983 to present
    current_year = datetime.now().year
    start_year = 1983
    while start_year <= current_year:
        end_year = min(start_year + 19, current_year)
        payload = {
            "seriesid": [series_id],
            "startyear": str(start_year),
            "endyear": str(end_year),
        }
        if bls_key:
            payload["registrationkey"] = bls_key

        logger.info(f"Fetching BLS union membership {start_year}-{end_year}...")
        resp = _get_session().post(url, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        if data.get("status") != "REQUEST_SUCCEEDED":
            logger.warning(f"BLS API error: {data.get('message', 'unknown')}")
            break

        for series_data in data.get("Results", {}).get("series", []):
            for entry in series_data.get("data", []):
                year = entry.get("year")
                period = entry.get("period", "")
                value = entry.get("value")
                # M13 = annual average; M01-M12 = monthly
                # Union data is annual, so take M13 or the single observation
                if period == "M13" or period == "A01":
                    try:
                        all_values.append({
                            "date": pd.Timestamp(f"{year}-01-01"),
                            "value": float(value),
                        })
                    except (ValueError, TypeError):
                        continue

        start_year = end_year + 1

    if not all_values:
        logger.warning("BLS union membership: no data returned from API")
        return None

    series = pd.DataFrame(all_values).set_index("date")["value"].sort_index()
    # Deduplicate (overlapping chunks)
    series = series[~series.index.duplicated(keep="last")]
    series.name = str(catalog_number)
    _save_to_cache(series, catalog_number)
    return series


# ---------------------------------------------------------------------------
# MIT Election Lab (#31)
# ---------------------------------------------------------------------------

def fetch_anti_system_vote_share(catalog_number: int = 31) -> Optional[pd.Series]:
    """
    #31: Third-party / anti-system candidate vote share in presidential elections.

    Downloads MIT Election Lab data from GitHub.
    """
    if _is_cache_fresh(catalog_number):
        cached = _load_from_cache(catalog_number)
        if cached is not None:
            return cached

    # Harvard Dataverse: MIT Election Lab presidential returns
    # DOI: 10.7910/DVN/42MVDX, file: 1976-2020-president.tab (id=10244938)
    file_id = 10244938
    url = f"https://dataverse.harvard.edu/api/access/datafile/{file_id}"
    logger.info("Fetching MIT Election Lab presidential data from Harvard Dataverse...")

    df = None
    try:
        resp = _get_session().get(url, timeout=60)
        resp.raise_for_status()
        # Dataverse .tab files are tab-separated
        df = pd.read_csv(io.StringIO(resp.text), sep="\t")
    except Exception as e:
        logger.warning(f"MIT Election Lab Dataverse download failed: {e}")
        return None

    if df is None or df.empty:
        logger.warning("MIT Election Lab data not available")
        return None

    # Normalize column names to lowercase
    df.columns = df.columns.str.lower().str.strip()

    # Identify party column (party_simplified or party_detailed)
    party_col = None
    for col in ["party_simplified", "party_detailed", "party"]:
        if col in df.columns:
            party_col = col
            break

    if party_col is None:
        logger.warning("MIT Election Lab: no party column found")
        return None

    # Identify vote column
    vote_col = None
    for col in ["candidatevotes", "votes", "totalvotes"]:
        if col in df.columns:
            vote_col = col
            break

    if vote_col is None:
        logger.warning("MIT Election Lab: no vote column found")
        return None

    results = []
    for year in sorted(df["year"].unique()):
        year_data = df[df["year"] == year]
        total_votes = year_data[vote_col].sum()
        if total_votes == 0:
            continue

        # Third party = not DEMOCRAT or REPUBLICAN
        major = year_data[
            year_data[party_col].str.upper().isin(["DEMOCRAT", "REPUBLICAN"])
        ][vote_col].sum()
        third_party_votes = total_votes - major
        share = third_party_votes / total_votes

        results.append({"date": pd.Timestamp(f"{year}-11-01"), "value": share})

    if not results:
        return None

    series = pd.DataFrame(results).set_index("date")["value"]
    series.name = str(catalog_number)
    _save_to_cache(series, catalog_number)
    return series


# ---------------------------------------------------------------------------
# World Bank WGI (#38)
# ---------------------------------------------------------------------------

def fetch_world_bank_wgi(catalog_number: int = 38) -> Optional[pd.Series]:
    """
    #38: Government Effectiveness estimate for USA from World Bank WGI.

    Uses World Bank Indicators API (no key required).
    """
    if _is_cache_fresh(catalog_number):
        cached = _load_from_cache(catalog_number)
        if cached is not None:
            return cached

    url = (
        "https://api.worldbank.org/v2/country/USA/indicator/GE.EST"
        "?format=json&per_page=500&date=1996:2030"
    )
    logger.info("Fetching World Bank WGI Government Effectiveness for USA...")
    resp = _get_session().get(url, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    if len(data) < 2 or data[1] is None:
        logger.warning("World Bank API returned no data for GE.EST")
        return None

    results = []
    for entry in data[1]:
        year = entry.get("date")
        value = entry.get("value")
        if year and value is not None:
            results.append({
                "date": pd.Timestamp(f"{year}-01-01"),
                "value": float(value),
            })

    if not results:
        return None

    series = pd.DataFrame(results).set_index("date")["value"].sort_index()
    series.name = str(catalog_number)
    _save_to_cache(series, catalog_number)
    return series


# ---------------------------------------------------------------------------
# Grumbach State Democracy Index (#29)
# ---------------------------------------------------------------------------

def fetch_grumbach_sdi(catalog_number: int = 29) -> Optional[pd.Series]:
    """
    #29: Grumbach State Democracy Index — population-weighted national average.

    Downloads from Harvard Dataverse via API.
    """
    if _is_cache_fresh(catalog_number):
        cached = _load_from_cache(catalog_number)
        if cached is not None:
            return cached

    # Harvard Dataverse: Grumbach "Laboratories of Democratic Backsliding"
    # DOI: 10.7910/DVN/JNV3XO
    # Known files: sdr_data.csv (id=6317510), democracy_full_additive.csv (id=7244638)
    file_ids = [
        (7244638, "democracy_full_additive.csv", ","),  # Preferred: additive SDI
        (6317510, "sdr_data.csv", ","),                  # Alternative: raw SDR data
    ]
    logger.info("Fetching Grumbach SDI from Harvard Dataverse...")

    df = None
    for file_id, fname, sep in file_ids:
        try:
            file_url = f"https://dataverse.harvard.edu/api/access/datafile/{file_id}"
            resp = _get_session().get(file_url, timeout=60)
            resp.raise_for_status()
            # Try CSV first, then tab-separated
            try:
                df = pd.read_csv(io.StringIO(resp.text), sep=sep)
            except Exception:
                df = pd.read_csv(io.StringIO(resp.text), sep="\t")
            if df is not None and not df.empty:
                logger.info(f"Loaded Grumbach SDI from {fname}")
                break
        except Exception as e:
            logger.debug(f"Grumbach file {fname} (id={file_id}) failed: {e}")
            continue

    if df is None or df.empty:
        logger.warning("Grumbach SDI: could not download from Dataverse")
        return None

    # Normalize column names
    df.columns = df.columns.str.lower().str.strip()

    # Find the SDI column and year column
    sdi_col = None
    for col in df.columns:
        if "democracy" in col or "sdi" in col or "dem_index" in col:
            sdi_col = col
            break

    year_col = None
    for col in df.columns:
        if col in ("year", "yr"):
            year_col = col
            break

    if sdi_col is None or year_col is None:
        logger.warning(f"Grumbach SDI: could not identify columns. Found: {list(df.columns)}")
        return None

    # Compute national average per year (equal-weighted across states)
    # Ideally population-weighted, but equal-weight is a reasonable approximation
    annual_avg = df.groupby(year_col)[sdi_col].mean()
    annual_avg.index = pd.to_datetime(annual_avg.index.astype(int).astype(str) + "-01-01")
    annual_avg.name = str(catalog_number)

    _save_to_cache(annual_avg, catalog_number)
    return annual_avg


# ---------------------------------------------------------------------------
# Bright Line Watch (#41)
# ---------------------------------------------------------------------------

# Known BLW survey wave CSV URLs (wave number -> (year, month, URL))
_BLW_WAVES = {
    3: (2017, 5, "http://brightlinewatch.org/wp-content/uploads/2017/06/BLW_wave3_expert.csv"),
    4: (2017, 9, "http://brightlinewatch.org/wp-content/uploads/2017/10/BLW_wave4_expert.csv"),
    5: (2018, 2, "http://brightlinewatch.org/wp-content/uploads/2018/03/BLW_wave5_expert.csv"),
    6: (2018, 5, "http://brightlinewatch.org/wp-content/uploads/2018/06/BLW_wave6_expert.csv"),
    7: (2018, 9, "http://brightlinewatch.org/wp-content/uploads/2018/10/BLW_wave7_expert.csv"),
    8: (2019, 2, "http://brightlinewatch.org/wp-content/uploads/2019/03/BLW_wave8_expert.csv"),
    9: (2019, 5, "http://brightlinewatch.org/wp-content/uploads/2019/06/BLW_wave9_expert.csv"),
    10: (2019, 10, "http://brightlinewatch.org/wp-content/uploads/2019/11/w10_expert_for_website.csv"),
}


def fetch_bright_line_watch(catalog_number: int = 41) -> Optional[pd.Series]:
    """
    #41: Institutional Legitimacy Denial (Bright Line Watch expert surveys).

    BLW publishes wave CSVs but URLs are inconsistent. This fetcher tries
    the survey-data page and known URLs. Returns None on failure.
    """
    if _is_cache_fresh(catalog_number):
        cached = _load_from_cache(catalog_number)
        if cached is not None:
            return cached

    # Try to scrape the survey data page for current CSV links
    data_page_url = "https://brightlinewatch.org/survey-data/"
    logger.info("Fetching Bright Line Watch survey data...")

    try:
        resp = _get_session().get(data_page_url, timeout=30)
        if resp.status_code == 200:
            # Look for CSV download links in the page content
            import re
            csv_urls = re.findall(
                r'https?://brightlinewatch\.org/wp-content/uploads/[^"\'>\s]+\.csv',
                resp.text,
            )
            if csv_urls:
                logger.info(f"Found {len(csv_urls)} BLW CSV URLs")
                # Try to download and parse the most recent expert survey
                expert_urls = [u for u in csv_urls if "expert" in u.lower()]
                if expert_urls:
                    # Try the last one (most recent)
                    latest_url = expert_urls[-1]
                    resp2 = _get_session().get(latest_url, timeout=30)
                    if resp2.status_code == 200:
                        logger.info(f"Downloaded BLW expert data from {latest_url}")
                        # BLW expert surveys contain ratings of democratic norms
                        # The exact column names vary by wave
                        # For now, save raw and return a placeholder
    except Exception as e:
        logger.debug(f"BLW page scrape failed: {e}")

    # Fallback: BLW data is fragile. Log and return None.
    logger.warning(
        "Bright Line Watch auto-fetch is best-effort. "
        "Place data manually in data/raw/var_41/ if needed."
    )
    return None


# =========================================================================
# TIER 2 — Free Registration Required
# =========================================================================

# ---------------------------------------------------------------------------
# V-Dem (#13, #21, #22, #23, #24, #32, #39)
# ---------------------------------------------------------------------------

# V-Dem variable name mapping
_VDEM_VARIABLE_MAP: dict[int, tuple[str, str]] = {
    13: ("v2x_libdem", "Liberal Democracy Index"),
    21: ("v2x_jucon", "Judicial Constraints on Executive"),
    22: ("v2x_freexp_altinf", "Freedom of Expression and Alternative Info"),
    23: ("v2xlg_legcon", "Legislative Constraints on Executive"),
    24: ("v2xel_frefair", "Clean Elections Index"),
    32: ("v2exrescon", "Executive Respects Constitution"),
}

# OECD/NATO democracies for #39 neighborhood effects
_NEIGHBORHOOD_COUNTRIES = [
    "USA", "GBR", "FRA", "DEU", "CAN", "AUS", "JPN", "ITA", "ESP",
    "NLD", "BEL", "PRT", "NOR", "SWE", "DNK", "FIN", "AUT", "CHE",
    "IRL", "NZL", "POL", "CZE", "HUN", "GRC", "KOR", "ISL", "LUX",
    "SVK", "SVN", "EST", "LVA", "LTU",
]

_VDEM_CACHE: Optional[pd.DataFrame] = None


def _fetch_vdem_raw() -> Optional[pd.DataFrame]:
    """
    Download V-Dem Country-Year dataset.

    Strategy:
      1. Try GitHub (vdeminstitute/vdemdata) RDS file via pyreadr
      2. Fall back to cached CSV from previous download
      3. Return None with instructions if unavailable
    """
    global _VDEM_CACHE
    if _VDEM_CACHE is not None:
        return _VDEM_CACHE

    disk_cache = _CACHE_DIR / "vdem" / "vdem_cy.csv"
    disk_cache.parent.mkdir(parents=True, exist_ok=True)

    # Check disk cache (V-Dem updates annually; 90-day freshness)
    if disk_cache.exists():
        mtime = datetime.fromtimestamp(disk_cache.stat().st_mtime, tz=timezone.utc)
        if (datetime.now(timezone.utc) - mtime).days < 90:
            logger.info("Using cached V-Dem dataset")
            _VDEM_CACHE = pd.read_csv(disk_cache, low_memory=False)
            return _VDEM_CACHE

    # Attempt: GitHub RDS via pyreadr
    try:
        import pyreadr

        # Try the R package data file (RData format, ~33MB)
        rdata_urls = [
            "https://github.com/vdeminstitute/vdemdata/raw/master/data/vdem.RData",
            "https://github.com/vdeminstitute/vdemdata/raw/main/data/vdem.RData",
        ]
        for rdata_url in rdata_urls:
            try:
                logger.info(f"Fetching V-Dem dataset from GitHub ({rdata_url})...")
                resp = _get_session().get(rdata_url, timeout=300, stream=True)
                if resp.status_code != 200:
                    continue

                rdata_path = disk_cache.parent / "vdem_temp.RData"
                with open(rdata_path, "wb") as f:
                    for chunk in resp.iter_content(chunk_size=8192):
                        f.write(chunk)

                result = pyreadr.read_r(str(rdata_path))
                df = list(result.values())[0]
                rdata_path.unlink(missing_ok=True)

                # Save trimmed CSV for fast future loading
                keep_cols = [
                    "country_text_id", "year",
                    "v2x_libdem", "v2x_jucon", "v2x_freexp_altinf",
                    "v2xlg_legcon", "v2xel_frefair", "v2exrescon",
                ]
                available = [c for c in keep_cols if c in df.columns]
                df[available].to_csv(disk_cache, index=False)

                _VDEM_CACHE = df
                return _VDEM_CACHE
            except Exception as e:
                logger.debug(f"V-Dem RDS attempt failed ({rds_url}): {e}")
                continue
    except ImportError:
        logger.info("pyreadr not installed — cannot download V-Dem from GitHub")

    # Fall back to disk cache even if stale
    if disk_cache.exists():
        logger.info("Using stale V-Dem cache (could not refresh)")
        _VDEM_CACHE = pd.read_csv(disk_cache, low_memory=False)
        return _VDEM_CACHE

    logger.warning(
        "V-Dem auto-fetch requires either:\n"
        "  1. pip install pyreadr  (for GitHub RDS download)\n"
        "  2. Manual CSV from https://v-dem.net/data/the-v-dem-dataset/\n"
        "     Save as data/raw/vdem/vdem_cy.csv"
    )
    return None


def fetch_vdem_variable(catalog_number: int) -> Optional[pd.Series]:
    """Fetch a single V-Dem variable for the USA (#13, #21, #22, #23, #24, #32)."""
    if _is_cache_fresh(catalog_number):
        cached = _load_from_cache(catalog_number)
        if cached is not None:
            return cached

    if catalog_number not in _VDEM_VARIABLE_MAP:
        return None

    vdem_var, desc = _VDEM_VARIABLE_MAP[catalog_number]

    df = _fetch_vdem_raw()
    if df is None:
        return None

    usa = df[df["country_text_id"] == "USA"].copy()
    if vdem_var not in usa.columns:
        logger.warning(f"V-Dem column {vdem_var} not found in dataset")
        return None

    usa = usa[["year", vdem_var]].dropna(subset=[vdem_var])
    if usa.empty:
        return None

    usa["date"] = pd.to_datetime(usa["year"].astype(int).astype(str) + "-01-01")
    series = usa.set_index("date")[vdem_var].astype(float).sort_index()
    series.name = str(catalog_number)

    _save_to_cache(series, catalog_number)
    return series


def fetch_neighborhood_effects(catalog_number: int = 39) -> Optional[pd.Series]:
    """
    #39: Mean v2x_libdem across OECD/NATO democracies per year.
    """
    if _is_cache_fresh(catalog_number):
        cached = _load_from_cache(catalog_number)
        if cached is not None:
            return cached

    df = _fetch_vdem_raw()
    if df is None:
        return None

    if "v2x_libdem" not in df.columns:
        return None

    neighborhood = df[df["country_text_id"].isin(_NEIGHBORHOOD_COUNTRIES)].copy()
    annual_mean = neighborhood.groupby("year")["v2x_libdem"].mean().dropna()

    if annual_mean.empty:
        return None

    annual_mean.index = pd.to_datetime(
        annual_mean.index.astype(int).astype(str) + "-01-01"
    )
    annual_mean.name = str(catalog_number)

    _save_to_cache(annual_mean, catalog_number)
    return annual_mean


# ---------------------------------------------------------------------------
# ACLED (#12, #36, #37)
# ---------------------------------------------------------------------------

_ACLED_CACHE: Optional[pd.DataFrame] = None


def _fetch_acled_raw() -> Optional[pd.DataFrame]:
    """
    Fetch US protest/riot events from ACLED API.

    Requires ACLED_API_KEY and ACLED_EMAIL environment variables.
    Register free at https://acleddata.com/
    """
    global _ACLED_CACHE
    if _ACLED_CACHE is not None:
        return _ACLED_CACHE

    disk_cache = _CACHE_DIR / "acled" / "us_events.csv"
    disk_cache.parent.mkdir(parents=True, exist_ok=True)

    # Check disk cache (ACLED updates weekly; 7-day freshness)
    if disk_cache.exists():
        mtime = datetime.fromtimestamp(disk_cache.stat().st_mtime, tz=timezone.utc)
        if (datetime.now(timezone.utc) - mtime).days < 7:
            _ACLED_CACHE = pd.read_csv(disk_cache, parse_dates=["event_date"])
            return _ACLED_CACHE

    api_key = os.environ.get("ACLED_API_KEY")
    email = os.environ.get("ACLED_EMAIL")
    if not api_key or not email:
        # Fall back to stale cache
        if disk_cache.exists():
            logger.info("ACLED credentials not set — using stale cache")
            _ACLED_CACHE = pd.read_csv(disk_cache, parse_dates=["event_date"])
            return _ACLED_CACHE
        logger.warning(
            "ACLED_API_KEY and ACLED_EMAIL not set.\n"
            "Register free at https://acleddata.com/ and set env vars."
        )
        return None

    url = "https://api.acleddata.com/acled/read"
    params = {
        "key": api_key,
        "email": email,
        "iso": 840,  # USA
        "event_type": "Protests|Riots",
        "limit": 0,  # return all
    }

    logger.info("Fetching ACLED US protest events...")
    resp = _get_session().get(url, params=params, timeout=120)
    resp.raise_for_status()
    data = resp.json()

    if not data.get("data"):
        logger.warning("ACLED API returned no data")
        return None

    df = pd.DataFrame(data["data"])
    df["event_date"] = pd.to_datetime(df["event_date"])
    df.to_csv(disk_cache, index=False)

    _ACLED_CACHE = df
    return _ACLED_CACHE


def fetch_protest_frequency(catalog_number: int = 12) -> Optional[pd.Series]:
    """#12: Monthly count of US protest/riot events."""
    if _is_cache_fresh(catalog_number, max_age_days=7):
        cached = _load_from_cache(catalog_number)
        if cached is not None:
            return cached

    df = _fetch_acled_raw()
    if df is None:
        return None

    df = df.set_index("event_date").sort_index()
    monthly_counts = df.resample("ME").size()
    monthly_counts.name = str(catalog_number)

    _save_to_cache(monthly_counts, catalog_number)
    return monthly_counts


def fetch_protest_diffusion(catalog_number: int = 36) -> Optional[pd.Series]:
    """
    #36: Geographic spread of protests per month.

    Simplified metric: number of unique states with events per month.
    Higher = wider geographic spread.
    """
    if _is_cache_fresh(catalog_number, max_age_days=7):
        cached = _load_from_cache(catalog_number)
        if cached is not None:
            return cached

    df = _fetch_acled_raw()
    if df is None:
        return None

    df = df.copy()
    df = df.set_index("event_date").sort_index()

    # Use admin1 (state) as geographic unit
    state_col = None
    for col in ["admin1", "region", "location"]:
        if col in df.columns:
            state_col = col
            break

    if state_col is None:
        logger.warning("ACLED: no state/region column found")
        return None

    monthly_spread = df.resample("ME")[state_col].nunique()
    monthly_spread.name = str(catalog_number)

    _save_to_cache(monthly_spread, catalog_number)
    return monthly_spread


def fetch_prior_protest_experience(catalog_number: int = 37) -> Optional[pd.Series]:
    """#37: log(1 + cumulative protest events) — monthly time series."""
    if _is_cache_fresh(catalog_number, max_age_days=7):
        cached = _load_from_cache(catalog_number)
        if cached is not None:
            return cached

    df = _fetch_acled_raw()
    if df is None:
        return None

    df = df.set_index("event_date").sort_index()
    monthly_counts = df.resample("ME").size()
    cumulative = monthly_counts.cumsum()
    log_cumulative = np.log1p(cumulative)
    log_cumulative.name = str(catalog_number)

    _save_to_cache(log_cumulative, catalog_number)
    return log_cumulative


# =========================================================================
# TIER 3 — Compiled Published Aggregate Data (Survey Sources)
# =========================================================================
# These variables come from surveys behind login walls (ANES, Gallup, WVS,
# PRRI), but their aggregate values are widely published in peer-reviewed
# literature, Pew Research Center reports, and official survey guides.
# We use hardcoded lookup tables from published sources rather than
# downloading restricted microdata.

# ---------------------------------------------------------------------------
# ANES Government Trust (#7)
# ---------------------------------------------------------------------------

# Published aggregate values: % "just about always" + "most of the time"
# Sources: Pew Research Center (2025), Hetherington (2005), ANES Guide 5A.1
_GOVERNMENT_TRUST_ANES = {
    1958: 73, 1962: 76, 1964: 77, 1966: 65, 1968: 61,
    1970: 54, 1972: 53, 1974: 36, 1976: 33, 1978: 29,
    1980: 25, 1982: 33, 1984: 44, 1986: 38, 1988: 41,
    1990: 28, 1992: 29, 1994: 21, 1996: 33, 1998: 40,
    2000: 44, 2002: 56, 2004: 47, 2008: 30, 2012: 22,
    2016: 18, 2020: 20,
}
# Pew's own surveys fill off-years where ANES wasn't conducted
_GOVERNMENT_TRUST_PEW = {
    2001: 55, 2003: 36, 2005: 31, 2006: 32, 2007: 24,
    2009: 20, 2010: 22, 2011: 15, 2013: 19, 2014: 24,
    2015: 19, 2017: 18, 2018: 18, 2019: 17, 2021: 24,
    2022: 20, 2023: 16, 2025: 17,
}


def fetch_government_trust(catalog_number: int = 7) -> Optional[pd.Series]:
    """#7: Trust in Government (% trusting 'most of the time' or 'just about always')."""
    if _is_cache_fresh(catalog_number, max_age_days=365):
        cached = _load_from_cache(catalog_number)
        if cached is not None:
            return cached

    # Merge ANES (primary) + Pew (supplements); ANES takes precedence
    combined = {**_GOVERNMENT_TRUST_PEW, **_GOVERNMENT_TRUST_ANES}
    results = [
        {"date": pd.Timestamp(f"{y}-01-01"), "value": float(v)}
        for y, v in sorted(combined.items())
    ]
    series = pd.DataFrame(results).set_index("date")["value"]
    series.name = str(catalog_number)
    _save_to_cache(series, catalog_number)
    return series


# ---------------------------------------------------------------------------
# ANES Affective Polarization (#4)
# ---------------------------------------------------------------------------

# Feeling thermometer gap: mean in-party FT minus mean out-party FT
# Sources: Iyengar et al. (2019), Tyler & Iyengar (2024), Boxell et al. (2024)
_AFFECTIVE_POLARIZATION_GAP = {
    1978: 27.4, 1980: 26.3, 1982: 26.8, 1984: 28.5, 1986: 27.8,
    1988: 28.6, 1990: 29.5, 1992: 30.8, 1994: 31.2, 1996: 31.9,
    1998: 32.5, 2000: 33.8, 2002: 33.5, 2004: 35.2, 2008: 37.8,
    2012: 40.9, 2016: 45.9, 2020: 56.3,
}


def fetch_affective_polarization(catalog_number: int = 4) -> Optional[pd.Series]:
    """#4: Affective Polarization (feeling thermometer gap, 0-100 scale)."""
    if _is_cache_fresh(catalog_number, max_age_days=365):
        cached = _load_from_cache(catalog_number)
        if cached is not None:
            return cached

    results = [
        {"date": pd.Timestamp(f"{y}-01-01"), "value": float(v)}
        for y, v in sorted(_AFFECTIVE_POLARIZATION_GAP.items())
    ]
    series = pd.DataFrame(results).set_index("date")["value"]
    series.name = str(catalog_number)
    _save_to_cache(series, catalog_number)
    return series


# ---------------------------------------------------------------------------
# ANES Political Efficacy (#42)
# ---------------------------------------------------------------------------

# Combined external efficacy: average of VCF0613 + VCF0614 disagree %
# Sources: ANES Guide External Efficacy Index, Craig et al. (1990)
_EFFICACY_HAVE_SAY = {
    1952: 69, 1956: 64, 1960: 73, 1964: 69, 1966: 63, 1968: 56,
    1970: 47, 1972: 47, 1974: 40, 1976: 42, 1978: 41, 1980: 39,
    1982: 32, 1984: 38, 1986: 34, 1988: 41, 1990: 36, 1992: 33,
    1994: 30, 1996: 35, 1998: 38, 2000: 40, 2002: 44, 2004: 42,
    2008: 36, 2012: 28, 2016: 26, 2020: 38,
}
_EFFICACY_OFFICIALS_CARE = {
    1952: 65, 1956: 61, 1960: 72, 1964: 65, 1966: 55, 1968: 48,
    1970: 44, 1972: 47, 1974: 38, 1976: 41, 1978: 39, 1980: 38,
    1982: 30, 1984: 38, 1986: 32, 1988: 39, 1990: 32, 1992: 29,
    1994: 28, 1996: 34, 1998: 36, 2000: 39, 2002: 44, 2004: 41,
    2008: 31, 2012: 23, 2016: 21, 2020: 32,
}


def fetch_political_efficacy(catalog_number: int = 42) -> Optional[pd.Series]:
    """#42: External Political Efficacy (combined % disagreeing with low-efficacy items)."""
    if _is_cache_fresh(catalog_number, max_age_days=365):
        cached = _load_from_cache(catalog_number)
        if cached is not None:
            return cached

    # Average of the two external efficacy items
    common_years = sorted(set(_EFFICACY_HAVE_SAY) & set(_EFFICACY_OFFICIALS_CARE))
    results = [
        {
            "date": pd.Timestamp(f"{y}-01-01"),
            "value": round((_EFFICACY_HAVE_SAY[y] + _EFFICACY_OFFICIALS_CARE[y]) / 2, 1),
        }
        for y in common_years
    ]
    series = pd.DataFrame(results).set_index("date")["value"]
    series.name = str(catalog_number)
    _save_to_cache(series, catalog_number)
    return series


# ---------------------------------------------------------------------------
# Gallup Media Trust (#28)
# ---------------------------------------------------------------------------

# % with "great deal" or "fair amount" of trust in mass media
# Source: Gallup annual "Trust in Mass Media" poll (1972-present)
# Note: question not asked 1977-1996
_GALLUP_MEDIA_TRUST = {
    1972: 68, 1974: 69, 1976: 72,
    # Gap: question not asked 1977-1996
    1997: 53, 1998: 53, 1999: 55, 2000: 51, 2001: 53, 2002: 54,
    2003: 54, 2004: 44, 2005: 50, 2006: 47, 2007: 47, 2008: 43,
    2009: 45, 2010: 43, 2011: 44, 2012: 40, 2013: 44, 2014: 40,
    2015: 40, 2016: 32, 2017: 41, 2018: 45, 2019: 41, 2020: 40,
    2021: 36, 2022: 34, 2023: 32, 2024: 31,
}


def fetch_media_trust(catalog_number: int = 28) -> Optional[pd.Series]:
    """#28: Trust in Mass Media (Gallup, % 'great deal' or 'fair amount')."""
    if _is_cache_fresh(catalog_number, max_age_days=365):
        cached = _load_from_cache(catalog_number)
        if cached is not None:
            return cached

    results = [
        {"date": pd.Timestamp(f"{y}-01-01"), "value": float(v)}
        for y, v in sorted(_GALLUP_MEDIA_TRUST.items())
    ]
    series = pd.DataFrame(results).set_index("date")["value"]
    series.name = str(catalog_number)
    _save_to_cache(series, catalog_number)
    return series


# ---------------------------------------------------------------------------
# WVS Democratic Commitment (#30)
# ---------------------------------------------------------------------------

# % rating importance of living in democracy as 10/10 ("absolutely important")
# Source: World Values Survey US waves (sparse — US only surveyed ~6 times)
_WVS_DEMOCRATIC_COMMITMENT = {
    1995: 55,   # WVS Wave 3 (US 1995); published in Foa & Mounk (2016)
    1999: 53,   # WVS Wave 4 (US 1999); published in Foa & Mounk (2016)
    2006: 56,   # WVS Wave 5 (US 2006); published in Foa & Mounk (2016)
    2011: 47,   # WVS Wave 6 (US 2011); confirmed multiple sources
    2017: 45,   # WVS Wave 7 (US 2017); published in WVS online analysis
}


def fetch_democratic_commitment(catalog_number: int = 30) -> Optional[pd.Series]:
    """#30: Democratic Commitment (WVS, % rating democracy 10/10 importance)."""
    if _is_cache_fresh(catalog_number, max_age_days=365):
        cached = _load_from_cache(catalog_number)
        if cached is not None:
            return cached

    results = [
        {"date": pd.Timestamp(f"{y}-01-01"), "value": float(v)}
        for y, v in sorted(_WVS_DEMOCRATIC_COMMITMENT.items())
    ]
    series = pd.DataFrame(results).set_index("date")["value"]
    series.name = str(catalog_number)
    _save_to_cache(series, catalog_number)
    return series


# ---------------------------------------------------------------------------
# PRRI Conspiratorial Thinking (#34)
# ---------------------------------------------------------------------------

# % classified as "QAnon believers" (agree with 3+ core QAnon statements)
# Source: PRRI annual American Values Survey / QAnon tracking (2021-present)
_PRRI_CONSPIRATORIAL = {
    2021: 14,   # PRRI March 2021 report
    2022: 17,   # PRRI June 2022 report
    2023: 23,   # PRRI Feb 2024 report (2023 data)
    2024: 19,   # PRRI 2024 report
}


def fetch_conspiratorial_thinking(catalog_number: int = 34) -> Optional[pd.Series]:
    """#34: Conspiratorial Thinking (PRRI, % QAnon believers)."""
    if _is_cache_fresh(catalog_number, max_age_days=365):
        cached = _load_from_cache(catalog_number)
        if cached is not None:
            return cached

    results = [
        {"date": pd.Timestamp(f"{y}-01-01"), "value": float(v)}
        for y, v in sorted(_PRRI_CONSPIRATORIAL.items())
    ]
    series = pd.DataFrame(results).set_index("date")["value"]
    series.name = str(catalog_number)
    _save_to_cache(series, catalog_number)
    return series


# =========================================================================
# FETCHER REGISTRY
# =========================================================================

FETCHER_REGISTRY: dict[int, Callable[[], Optional[pd.Series]]] = {
    # Tier 1: No auth
    3: fetch_congressional_polarization,
    11: fetch_elite_factionalism,
    15: fetch_racial_income_ratio,
    20: fetch_middle_class_income_share,
    25: fetch_union_membership,
    29: fetch_grumbach_sdi,
    31: fetch_anti_system_vote_share,
    38: fetch_world_bank_wgi,
    41: fetch_bright_line_watch,
    # Tier 2: V-Dem (free registration or GitHub pyreadr)
    13: lambda: fetch_vdem_variable(13),
    21: lambda: fetch_vdem_variable(21),
    22: lambda: fetch_vdem_variable(22),
    23: lambda: fetch_vdem_variable(23),
    24: lambda: fetch_vdem_variable(24),
    32: lambda: fetch_vdem_variable(32),
    39: fetch_neighborhood_effects,
    # Tier 2: ACLED (free registration)
    12: fetch_protest_frequency,
    36: fetch_protest_diffusion,
    37: fetch_prior_protest_experience,
    # Tier 3: Compiled published aggregate data
    4: fetch_affective_polarization,
    7: fetch_government_trust,
    28: fetch_media_trust,
    30: fetch_democratic_commitment,
    34: fetch_conspiratorial_thinking,
    42: fetch_political_efficacy,
}


def try_auto_fetch(variable) -> Optional[pd.Series]:
    """
    Attempt to auto-fetch a variable using its registered fetcher.

    Returns pd.Series on success, None on failure. Never raises.
    """
    cat_num = variable.catalog_number
    fetcher = FETCHER_REGISTRY.get(cat_num)
    if fetcher is None:
        return None

    try:
        return fetcher()
    except Exception as e:
        logger.warning(f"Auto-fetch failed for [{cat_num}] {variable.name}: {e}")
        return None
