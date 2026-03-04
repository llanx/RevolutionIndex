"""
Revolution Index — Global Configuration

All FRED series IDs, model parameters, date ranges, and constants
are defined here. No magic numbers in model code.
"""

from pathlib import Path

# ─── Paths ───────────────────────────────────────────────────────────────────

PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_FRED_DIR = DATA_DIR / "raw" / "fred"
RAW_WID_DIR = DATA_DIR / "raw" / "wid"
PROCESSED_DIR = DATA_DIR / "processed"
METADATA_DIR = DATA_DIR / "metadata"

# ─── Date Ranges ─────────────────────────────────────────────────────────────

# Common reference period for percentile normalization (critical review B2)
REFERENCE_START = "1970-01-01"

# Fetch data as far back as available for each series
FETCH_START = "1947-01-01"

# ─── FRED Series ─────────────────────────────────────────────────────────────
# Each entry: series_id -> {description, frequency, model, component, invert}
# invert=True means higher raw values indicate LESS stress (must flip for scoring)

FRED_SERIES = {
    # === Turchin PSI ===
    "W270RE1A156NBEA": {
        "description": "Labor share of GDP (nonfarm business sector)",
        "frequency": "annual",
        "model": "turchin_psi",
        "component": "MMP",
        "invert": True,  # Lower labor share = higher mass mobilization potential
    },
    "GFDEGDQ188S": {
        "description": "Federal debt held by public as % of GDP",
        "frequency": "quarterly",
        "model": "turchin_psi",
        "component": "SFD",
        "invert": False,  # Higher debt/GDP = higher state fiscal distress
    },

    # === Prospect Theory PLI ===
    "MEHOINUSA672N": {
        "description": "Real median household income (2023 CPI-U-RS adjusted dollars)",
        "frequency": "annual",
        "model": "prospect_theory",
        "component": "wages",
        "invert": False,
    },
    "FIXHAI": {
        "description": "Housing Affordability Index (composite)",
        "frequency": "monthly",
        "model": "prospect_theory",
        "component": "housing",
        "invert": False,
    },
    "SPDYNLE00INUSA": {
        "description": "Life expectancy at birth (years)",
        "frequency": "annual",
        "model": "prospect_theory",
        "component": "health",
        "invert": False,
    },
    "LNS12300060": {
        "description": "Employment-population ratio, 25-54 years (prime age)",
        "frequency": "monthly",
        "model": "prospect_theory",
        "component": "employment",
        "invert": False,
    },
    "UMCSENT": {
        "description": "University of Michigan Consumer Sentiment Index",
        "frequency": "monthly",
        "model": "prospect_theory",
        "component": "security",
        "invert": False,
    },

    # === Financial Stress Pathway — Stage 1 (FSSI) ===
    "STLFSI4": {
        "description": "St. Louis Fed Financial Stress Index",
        "frequency": "weekly",
        "model": "financial_stress",
        "component": "fssi",
        "invert": False,  # Higher = more financial stress
    },
    "T10Y2Y": {
        "description": "10-Year minus 2-Year Treasury yield spread",
        "frequency": "daily",
        "model": "financial_stress",
        "component": "fssi",
        "invert": True,  # Lower/negative spread = more stress (yield curve inversion)
    },
    "VIXCLS": {
        "description": "CBOE Volatility Index (VIX)",
        "frequency": "daily",
        "model": "financial_stress",
        "component": "fssi",
        "invert": False,  # Higher VIX = more stress
    },
    "BAMLH0A0HYM2": {
        "description": "ICE BofA US High Yield Option-Adjusted Spread",
        "frequency": "daily",
        "model": "financial_stress",
        "component": "fssi",
        "invert": False,  # Higher spread = more stress
    },
    "DRSFRMACBS": {
        "description": "Delinquency rate on single-family residential mortgages",
        "frequency": "quarterly",
        "model": "financial_stress",
        "component": "fssi",
        "invert": False,  # Higher = more stress
    },

    # === Financial Stress Pathway — Stage 2 (ETI) ===
    "UNRATE": {
        "description": "Civilian unemployment rate",
        "frequency": "monthly",
        "model": "financial_stress",
        "component": "eti",
        "invert": False,  # Higher unemployment = more economic pain
    },
    "IC4WSA": {
        "description": "4-week moving average of initial claims",
        "frequency": "weekly",
        "model": "financial_stress",
        "component": "eti",
        "invert": False,  # Higher claims = more pain
    },
    "CES0500000003": {
        "description": "Average hourly earnings of all employees, total private",
        "frequency": "monthly",
        "model": "financial_stress",
        "component": "eti",
        "invert": False,  # Used with CPIAUCSL to compute real wage change
    },
    "CPIAUCSL": {
        "description": "Consumer Price Index for All Urban Consumers (all items)",
        "frequency": "monthly",
        "model": "financial_stress",
        "component": "eti",
        "invert": False,  # Deflator for real wage computation
    },
    "CSCICP03USM665S": {
        "description": "Consumer Confidence Index (OECD, normalized)",
        "frequency": "monthly",
        "model": "financial_stress",
        "component": "eti",
        "invert": True,  # Higher confidence = LESS stress
    },
}

# ─── WID.world Series ────────────────────────────────────────────────────────

WID_SERIES = {
    "sptinc992j": {
        "description": "Top 1% pre-tax national income share",
        "frequency": "annual",
        "model": "turchin_psi",
        "component": "EMP",
        "country": "US",
        "invert": False,  # Higher top-1% share = higher elite mobilization potential
    },
}

# ─── Model Parameters ────────────────────────────────────────────────────────

# Turchin PSI
PSI_PARAMS = {
    "aggregation": "geometric_mean",  # Fix from critical review A1
    # Plausible ranges for bootstrap uncertainty
    "reference_start_range": ("1965-01-01", "1975-01-01"),
}

# Prospect Theory PLI
# K constants reduced by 10x from original spec (critical review A2)
PLI_PARAMS = {
    "lambda_loss_aversion": 2.25,  # Kahneman & Tversky
    "alpha_diminishing_sensitivity": 0.88,
    "reference_window_years": 10,  # Trailing peak as reference point
    "domain_K": {
        "wages": 50.0,       # Original: 500
        "housing": 10.0,     # Original: 100
        "health": 150.0,     # Original: 1500
        "employment": 3.5,   # Original: 35
        "security": 1.0,     # Original: 10
    },
    "max_breadth_bonus": 20.0,
    "max_velocity_bonus": 20.0,
    # Plausible ranges for bootstrap
    "lambda_range": (2.0, 2.5),
    "K_scale_range": (0.5, 2.0),  # Multiply all K by this factor
}

# Financial Stress Pathway
FSP_PARAMS = {
    "rolling_window_years": 20,  # Z-score window
    "fssi_weights": {
        "STLFSI4": 0.25,
        "T10Y2Y": 0.20,
        "VIXCLS": 0.20,
        "BAMLH0A0HYM2": 0.20,
        "DRSFRMACBS": 0.15,
    },
    "eti_weights": {
        "UNRATE": 0.20,
        "IC4WSA": 0.15,
        "real_wage_change": 0.15,  # Computed: CES0500000003 deflated by CPIAUCSL
        "CSCICP03USM665S": 0.20,
        "debt_service": 0.15,     # TDSP if added later; omit for now
        "food_energy_cpi": 0.15,  # Computed: average of food + energy CPI YoY change
    },
    "max_lag_months": 24,  # For cross-correlation analysis
}

# ─── Ensemble ────────────────────────────────────────────────────────────────

ENSEMBLE_PARAMS = {
    "weights": {
        "turchin_psi": 1 / 3,
        "prospect_theory": 1 / 3,
        "financial_stress": 1 / 3,
    },
    "divergence_alert_threshold": 20.0,  # Points difference between models
}

# ─── Backtesting Episodes ────────────────────────────────────────────────────

HISTORICAL_EPISODES = {
    "1968_unrest": {
        "label": "Vietnam / Civil Rights / Assassinations",
        "start": "1967-01-01",
        "peak": "1968-06-01",
        "end": "1970-12-01",
    },
    "1979_stagflation": {
        "label": "Stagflation / Oil Shock",
        "start": "1978-01-01",
        "peak": "1980-06-01",
        "end": "1982-12-01",
    },
    "1992_la_riots": {
        "label": "LA Riots / Recession / Perot",
        "start": "1990-07-01",
        "peak": "1992-06-01",
        "end": "1993-06-01",
    },
    "2001_dotcom_911": {
        "label": "Dot-com Bust / 9-11 / Iraq",
        "start": "2000-03-01",
        "peak": "2001-09-01",
        "end": "2003-06-01",
    },
    "2008_gfc": {
        "label": "Global Financial Crisis / Tea Party / Occupy",
        "start": "2007-08-01",
        "peak": "2009-03-01",
        "end": "2012-06-01",
    },
    "2020_covid": {
        "label": "COVID / BLM / Jan 6",
        "start": "2020-03-01",
        "peak": "2021-01-01",
        "end": "2021-12-01",
    },
}

QUIET_PERIODS = {
    "clinton_prosperity": {
        "label": "Clinton-era Prosperity",
        "start": "1995-01-01",
        "end": "1999-12-01",
    },
    "post_gfc_recovery": {
        "label": "Post-GFC Recovery / Pre-COVID",
        "start": "2013-01-01",
        "end": "2018-12-01",
    },
}

# ─── Scoring Interpretation ──────────────────────────────────────────────────

SCORE_THRESHOLDS = {
    "low": (0, 25),
    "moderate": (25, 45),
    "elevated": (45, 65),
    "high": (65, 80),
    "crisis": (80, 100),
}
