"""
Score calibration: map raw ensemble output to the 0-100 scale using
historical anchor points.

Anchor points (locked decision from CONTEXT.md):
- 2008 financial crisis: should score in Crisis Territory (51-75)
- 2020 (COVID + social unrest): should score in Crisis Territory (51-75)
- Mid-1990s (stability period): should score in Stable (0-25)

Calibration method: linear rescaling based on anchor percentiles.

Also provides:
- Bootstrap confidence intervals (required by Phase 5 TEST-03)
- Score-to-zone mapping matching data.ts boundaries
"""
import numpy as np
import pandas as pd
from typing import Optional

from models.config import DOMAIN_WEIGHTS, Domain, VARIABLES, EVIDENCE_WEIGHTS


# ---------------------------------------------------------------------------
# Default anchor targets
# ---------------------------------------------------------------------------

DEFAULT_ANCHORS = {
    "crisis_target": 65.0,      # mid Crisis Territory for 2008-10 and 2020-06
    "stable_target": 20.0,      # mid Stable for 1994-1997 average
    "crisis_dates": ["2008-10", "2020-06"],
    "stable_range": ("1994-01", "1997-12"),
}


def calibrate(
    raw_scores: pd.Series,
    anchor_scores: Optional[dict[str, float]] = None,
) -> pd.Series:
    """
    Calibrate raw ensemble scores to fit anchor-point expectations.

    Default anchors (if not provided):
    - The score at 2008-10 (peak of financial crisis) should be ~65 (mid Crisis Territory)
    - The score at 2020-06 (peak COVID + BLM) should be ~65 (mid Crisis Territory)
    - The average score for 1994-1997 should be ~20 (mid Stable)

    Method:
    1. Compute the raw scores at anchor dates
    2. Fit a linear transformation: calibrated = a * raw + b
       such that anchor dates map to target values
    3. Clamp to 0-100

    Parameters
    ----------
    raw_scores : pd.Series
        Raw composite scores indexed by date string or DatetimeIndex.
        Values typically in 0-100 range (domain-weighted average * 100).
    anchor_scores : dict, optional
        Custom anchor targets. Keys: "crisis_raw", "stable_raw",
        "crisis_target", "stable_target".

    Returns
    -------
    pd.Series
        Calibrated scores clamped to 0-100.
    """
    if raw_scores.empty:
        return raw_scores.copy()

    # Ensure index is DatetimeIndex for date-based lookups
    if not isinstance(raw_scores.index, pd.DatetimeIndex):
        raw_scores = raw_scores.copy()
        raw_scores.index = pd.to_datetime(raw_scores.index)

    if anchor_scores is not None:
        crisis_raw = anchor_scores.get("crisis_raw")
        stable_raw = anchor_scores.get("stable_raw")
        crisis_target = anchor_scores.get("crisis_target", DEFAULT_ANCHORS["crisis_target"])
        stable_target = anchor_scores.get("stable_target", DEFAULT_ANCHORS["stable_target"])
    else:
        # Extract raw scores at anchor dates
        crisis_raw = _get_crisis_anchor_raw(raw_scores)
        stable_raw = _get_stable_anchor_raw(raw_scores)
        crisis_target = DEFAULT_ANCHORS["crisis_target"]
        stable_target = DEFAULT_ANCHORS["stable_target"]

    # If we can't find anchor points (data too short), return unclamped
    if crisis_raw is None or stable_raw is None:
        return raw_scores.clip(0, 100)

    # Avoid division by zero if anchors are at the same raw level
    if abs(crisis_raw - stable_raw) < 1e-6:
        return raw_scores.clip(0, 100)

    # Fit linear transformation: calibrated = a * raw + b
    # From two points: (stable_raw, stable_target) and (crisis_raw, crisis_target)
    a = (crisis_target - stable_target) / (crisis_raw - stable_raw)
    b = stable_target - a * stable_raw

    calibrated = a * raw_scores + b
    calibrated = calibrated.clip(0, 100)

    return calibrated


def _get_crisis_anchor_raw(raw_scores: pd.Series) -> Optional[float]:
    """
    Get the average raw score at the crisis anchor dates (2008-10, 2020-06).
    Uses the nearest available dates if exact matches are not found.
    """
    crisis_values = []

    for date_str in DEFAULT_ANCHORS["crisis_dates"]:
        target_date = pd.Timestamp(date_str + "-01")

        # Find the nearest date in the index
        if target_date in raw_scores.index:
            crisis_values.append(float(raw_scores.loc[target_date]))
        else:
            # Find nearest available date within 3 months
            diffs = abs(raw_scores.index - target_date)
            nearest_idx = diffs.argmin()
            nearest_date = raw_scores.index[nearest_idx]
            if abs((nearest_date - target_date).days) <= 92:
                crisis_values.append(float(raw_scores.iloc[nearest_idx]))

    if not crisis_values:
        return None

    return float(np.mean(crisis_values))


def _get_stable_anchor_raw(raw_scores: pd.Series) -> Optional[float]:
    """
    Get the average raw score during the stable period (1994-1997).
    """
    start_str, end_str = DEFAULT_ANCHORS["stable_range"]
    start_date = pd.Timestamp(start_str + "-01")
    end_date = pd.Timestamp(end_str + "-01")

    mask = (raw_scores.index >= start_date) & (raw_scores.index <= end_date)
    stable_values = raw_scores[mask]

    if stable_values.empty:
        return None

    return float(stable_values.mean())


# ---------------------------------------------------------------------------
# Bootstrap confidence intervals
# ---------------------------------------------------------------------------

def compute_bootstrap_ci(
    unified_df: pd.DataFrame,
    n_bootstrap: int = 1000,
    ci_width: float = 0.90,
) -> dict:
    """
    Bootstrap confidence intervals for the composite score.

    Method:
    1. Resample variables (columns) with replacement n_bootstrap times
    2. For each resample, recompute domain scores and ensemble composite
    3. Extract ci_width percentile interval

    This captures uncertainty from both variable selection and evidence
    weighting. Resampling at the variable level propagates uncertainty
    correctly (not just perturbing the composite directly).

    Parameters
    ----------
    unified_df : pd.DataFrame
        Unified DataFrame from pipeline with columns = catalog numbers
        (as strings), values in 0.0-1.0.
    n_bootstrap : int
        Number of bootstrap iterations (default 1000, sufficient for
        90% CI stability).
    ci_width : float
        Confidence interval width (default 0.90 for 90% CI).

    Returns
    -------
    dict with:
    - "point_estimate": float (composite score from original data)
    - "ci_lower": float (lower bound of CI)
    - "ci_upper": float (upper bound of CI)
    - "n_bootstrap": int
    - "ci_width": float

    Required by Phase 5 TEST-03.
    """
    rng = np.random.default_rng(42)  # Fixed seed for reproducibility

    # Build a mapping of which columns belong to which domain
    var_by_domain: dict[str, list[str]] = {}
    var_evidence: dict[str, float] = {}
    var_lookup = {v.catalog_number: v for v in VARIABLES}

    for col in unified_df.columns:
        try:
            cat_num = int(col)
        except ValueError:
            continue

        var_info = var_lookup.get(cat_num)
        if var_info is None:
            continue

        domain_id = var_info.domain.value
        if domain_id not in var_by_domain:
            var_by_domain[domain_id] = []
        var_by_domain[domain_id].append(col)
        var_evidence[col] = EVIDENCE_WEIGHTS[var_info.evidence_rating]

    # Compute point estimate: current composite from original data
    point_estimate = _compute_composite_from_latest(
        unified_df, var_by_domain, var_evidence,
    )

    # Bootstrap: resample variables within each domain
    bootstrap_scores = []
    for _ in range(n_bootstrap):
        resampled_composite = _bootstrap_one_iteration(
            unified_df, var_by_domain, var_evidence, rng,
        )
        bootstrap_scores.append(resampled_composite)

    bootstrap_arr = np.array(bootstrap_scores)
    alpha = (1.0 - ci_width) / 2.0
    ci_lower = float(np.percentile(bootstrap_arr, alpha * 100))
    ci_upper = float(np.percentile(bootstrap_arr, (1.0 - alpha) * 100))

    return {
        "point_estimate": point_estimate,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "n_bootstrap": n_bootstrap,
        "ci_width": ci_width,
    }


def _compute_composite_from_latest(
    df: pd.DataFrame,
    var_by_domain: dict[str, list[str]],
    var_evidence: dict[str, float],
) -> float:
    """Compute composite score from latest values, using domain weights."""
    domain_scores = {}

    for domain in Domain:
        domain_id = domain.value
        cols = var_by_domain.get(domain_id, [])
        if not cols:
            continue

        weighted_sum = 0.0
        total_weight = 0.0
        for col in cols:
            series = df[col].dropna()
            if series.empty:
                continue
            latest = float(series.iloc[-1])
            weight = var_evidence.get(col, 1.0)
            weighted_sum += latest * weight
            total_weight += weight

        if total_weight > 0:
            domain_scores[domain_id] = weighted_sum / total_weight

    # Weighted composite
    composite_sum = 0.0
    composite_weight = 0.0
    for domain in Domain:
        domain_id = domain.value
        if domain_id in domain_scores:
            w = DOMAIN_WEIGHTS[domain]
            composite_sum += domain_scores[domain_id] * w
            composite_weight += w

    if composite_weight > 0:
        return (composite_sum / composite_weight) * 100.0
    return 50.0


def _bootstrap_one_iteration(
    df: pd.DataFrame,
    var_by_domain: dict[str, list[str]],
    var_evidence: dict[str, float],
    rng: np.random.Generator,
) -> float:
    """
    One bootstrap iteration: resample variables within each domain
    with replacement, recompute domain scores and composite.
    """
    domain_scores = {}

    for domain in Domain:
        domain_id = domain.value
        cols = var_by_domain.get(domain_id, [])
        if not cols:
            continue

        # Resample columns with replacement
        resampled_cols = rng.choice(cols, size=len(cols), replace=True)

        weighted_sum = 0.0
        total_weight = 0.0
        for col in resampled_cols:
            series = df[col].dropna()
            if series.empty:
                continue
            latest = float(series.iloc[-1])
            weight = var_evidence.get(col, 1.0)
            weighted_sum += latest * weight
            total_weight += weight

        if total_weight > 0:
            domain_scores[domain_id] = weighted_sum / total_weight

    # Weighted composite
    composite_sum = 0.0
    composite_weight = 0.0
    for domain in Domain:
        domain_id = domain.value
        if domain_id in domain_scores:
            w = DOMAIN_WEIGHTS[domain]
            composite_sum += domain_scores[domain_id] * w
            composite_weight += w

    if composite_weight > 0:
        return (composite_sum / composite_weight) * 100.0
    return 50.0


# ---------------------------------------------------------------------------
# Score interpretation
# ---------------------------------------------------------------------------

def score_to_zone(score: int) -> str:
    """
    Map a 0-100 integer score to zone label.

    Uses the ZONES constant boundaries from data.ts:
      0-25:  "Stable"
      26-50: "Elevated Tension"
      51-75: "Crisis Territory"
      76-100: "Revolution Territory"

    Parameters
    ----------
    score : int
        Composite score in 0-100 range.

    Returns
    -------
    str
        Zone label string matching data.ts ZoneLabel type.
    """
    if score <= 25:
        return "Stable"
    elif score <= 50:
        return "Elevated Tension"
    elif score <= 75:
        return "Crisis Territory"
    else:
        return "Revolution Territory"
