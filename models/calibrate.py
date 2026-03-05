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

from models.config import VARIABLES


# ---------------------------------------------------------------------------
# Default anchor targets
#
# Anchors map known historical events to expected calibrated scores.
# Used for least-squares linear fit: calibrated = a * raw + b.
# More anchors = better constrained fit (degrees of freedom = N - 2).
# ---------------------------------------------------------------------------

DEFAULT_ANCHORS = [
    # (date_spec, target_score, label)
    # date_spec: "YYYY-MM" for a single month, or ("YYYY-MM", "YYYY-MM") for average over range
    {"date": "2008-10", "target": 65.0, "label": "Financial crisis peak"},
    {"date": "2020-06", "target": 65.0, "label": "COVID + BLM peak"},
    {"date": ("1994-01", "1997-12"), "target": 20.0, "label": "Mid-1990s stability"},
    {"date": "2001-09", "target": 42.0, "label": "Post-9/11 + dot-com recession"},
    {"date": "2011-08", "target": 47.0, "label": "Debt ceiling crisis + credit downgrade + Occupy"},
]


def _get_anchor_raw_score(
    raw_scores: pd.Series,
    date_spec,
) -> Optional[float]:
    """
    Get the raw score for an anchor point.

    date_spec can be:
    - "YYYY-MM": single month (finds nearest within 3 months)
    - ("YYYY-MM", "YYYY-MM"): average over date range
    """
    if isinstance(date_spec, tuple):
        start_date = pd.Timestamp(date_spec[0] + "-01")
        end_date = pd.Timestamp(date_spec[1] + "-01")
        mask = (raw_scores.index >= start_date) & (raw_scores.index <= end_date)
        values = raw_scores[mask]
        if values.empty:
            return None
        return float(values.mean())
    else:
        target_date = pd.Timestamp(date_spec + "-01")
        if target_date in raw_scores.index:
            return float(raw_scores.loc[target_date])
        # Find nearest within 3 months
        diffs = abs(raw_scores.index - target_date)
        nearest_idx = diffs.argmin()
        nearest_date = raw_scores.index[nearest_idx]
        if abs((nearest_date - target_date).days) <= 92:
            return float(raw_scores.iloc[nearest_idx])
        return None


def _fit_calibration(
    raw_scores: pd.Series,
    anchors: list[dict] = None,
) -> tuple[float, float, list[dict]]:
    """
    Fit a linear calibration using least-squares across all available anchors.

    Returns (a, b, residuals) where calibrated = a * raw + b,
    and residuals is a list of dicts with anchor label, target, actual, and error.
    Falls back to identity (1.0, 0.0) if fewer than 2 anchors match data.
    """
    if anchors is None:
        anchors = DEFAULT_ANCHORS

    if not isinstance(raw_scores.index, pd.DatetimeIndex):
        raw_scores = raw_scores.copy()
        raw_scores.index = pd.to_datetime(raw_scores.index)

    # Collect (raw_value, target_value) pairs from available anchors
    raw_vals = []
    target_vals = []
    anchor_labels = []

    for anchor in anchors:
        raw_val = _get_anchor_raw_score(raw_scores, anchor["date"])
        if raw_val is not None:
            raw_vals.append(raw_val)
            target_vals.append(anchor["target"])
            anchor_labels.append(anchor["label"])

    if len(raw_vals) < 2:
        return 1.0, 0.0, []

    # Least-squares fit: target = a * raw + b
    raw_arr = np.array(raw_vals)
    target_arr = np.array(target_vals)

    # np.polyfit with degree 1 returns [a, b]
    coeffs = np.polyfit(raw_arr, target_arr, 1)
    a, b = float(coeffs[0]), float(coeffs[1])

    # Compute residuals at each anchor
    residuals = []
    for i, label in enumerate(anchor_labels):
        fitted = a * raw_vals[i] + b
        error = fitted - target_vals[i]
        residuals.append({
            "label": label,
            "target": target_vals[i],
            "raw": round(raw_vals[i], 2),
            "fitted": round(fitted, 2),
            "error": round(error, 2),
        })
        if abs(error) > 10:
            print(f"  WARNING: Calibration anchor '{label}' deviates by "
                  f"{error:.1f} points (target={target_vals[i]}, fitted={fitted:.1f})")

    return a, b, residuals


def calibrate(
    raw_scores: pd.Series,
    anchors: list[dict] = None,
) -> pd.Series:
    """
    Calibrate raw ensemble scores using least-squares fit to anchor points.

    Method:
    1. Extract raw scores at each anchor date
    2. Fit a linear transformation via least-squares: calibrated = a * raw + b
    3. Clamp to 0-100

    Parameters
    ----------
    raw_scores : pd.Series
        Raw composite scores indexed by date string or DatetimeIndex.
    anchors : list[dict], optional
        Custom anchors. Each dict has "date", "target", "label".

    Returns
    -------
    pd.Series
        Calibrated scores clamped to 0-100.
    """
    if raw_scores.empty:
        return raw_scores.copy()

    a, b, residuals = _fit_calibration(raw_scores, anchors)

    if not isinstance(raw_scores.index, pd.DatetimeIndex):
        raw_scores = raw_scores.copy()
        raw_scores.index = pd.to_datetime(raw_scores.index)

    calibrated = a * raw_scores + b
    calibrated = calibrated.clip(0, 100)

    return calibrated


def get_calibration_coefficients(
    raw_scores: pd.Series,
    anchors: list[dict] = None,
) -> tuple[float, float]:
    """
    Extract the linear calibration coefficients (a, b) such that
    calibrated = a * raw + b.

    Uses least-squares fit across all available anchor points.
    Returns (a, b). If calibration cannot be computed, returns (1.0, 0.0).
    """
    if raw_scores.empty:
        return 1.0, 0.0

    a, b, _residuals = _fit_calibration(raw_scores, anchors)
    return a, b


# ---------------------------------------------------------------------------
# Bootstrap confidence intervals
# ---------------------------------------------------------------------------

def compute_bootstrap_ci(
    unified_df: pd.DataFrame,
    calibration_coeffs: tuple[float, float] = (1.0, 0.0),
    n_bootstrap: int = 1000,
    ci_width: float = 0.90,
    raw_df: pd.DataFrame = None,
) -> dict:
    """
    Bootstrap confidence intervals for the calibrated composite score.

    Method:
    1. Resample variables (columns) within each domain with replacement
    2. For each resample, run all 5 model functions on the perturbed
       FULL DataFrame using _run_models_on_slice (same path as point
       estimate and history), ensuring the bootstrap answers the same
       question as the point estimate
    3. Apply the calibration transform (a*raw + b) to each bootstrap score
    4. Extract ci_width percentile interval

    Parameters
    ----------
    unified_df : pd.DataFrame
        Unified DataFrame from pipeline with columns = catalog numbers
        (as strings), values in 0.0-1.0.
    calibration_coeffs : tuple[float, float]
        (a, b) from get_calibration_coefficients(). Calibrated = a*raw + b.
    n_bootstrap : int
        Number of bootstrap iterations (default 1000).
    ci_width : float
        Confidence interval width (default 0.90 for 90% CI).

    Returns
    -------
    dict with:
    - "ci_lower": float (lower bound of calibrated CI)
    - "ci_upper": float (upper bound of calibrated CI)
    - "n_bootstrap": int
    - "ci_width": float
    """
    from models.ensemble import (
        _ensure_models_registered, _rename_columns_for_models,
        _run_models_on_slice,
    )

    _ensure_models_registered()

    rng = np.random.default_rng(42)  # Fixed seed for reproducibility
    a, b = calibration_coeffs

    # Build a mapping of which columns belong to which domain
    var_by_domain: dict[str, list[str]] = {}
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

    # Prepare model-ready DataFrames
    model_df = _rename_columns_for_models(unified_df)
    raw_model_df = _rename_columns_for_models(raw_df) if raw_df is not None else None

    # Bootstrap: resample variables within each domain, run models
    # using _run_models_on_slice (same invocation path as point estimate).
    # Both normalized and raw DataFrames are perturbed identically so the
    # V-Dem model receives raw data for rate-of-change computation,
    # matching the point estimate code path.
    bootstrap_scores = []
    for _ in range(n_bootstrap):
        # Generate swap mapping ONCE, apply to BOTH DataFrames so that
        # models receiving both normalized and raw data (e.g., V-Dem)
        # get consistent perturbations.
        swaps = _generate_domain_swaps(var_by_domain, rng)
        perturbed = _apply_domain_swaps(
            model_df, var_by_domain, swaps,
        )
        raw_perturbed = _apply_domain_swaps(
            raw_model_df, var_by_domain, swaps,
        ) if raw_model_df is not None else None
        # Use _run_models_on_slice matching the point estimate path
        score = _run_models_on_slice(perturbed, raw_df_slice=raw_perturbed)
        if score is None:
            score = 50.0
        # Apply calibration transform to raw bootstrap score
        calibrated = max(0.0, min(100.0, a * score + b))
        bootstrap_scores.append(calibrated)

    bootstrap_arr = np.array(bootstrap_scores)
    alpha = (1.0 - ci_width) / 2.0
    ci_lower = float(np.percentile(bootstrap_arr, alpha * 100))
    ci_upper = float(np.percentile(bootstrap_arr, (1.0 - alpha) * 100))

    return {
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "n_bootstrap": n_bootstrap,
        "ci_width": ci_width,
    }


def _generate_domain_swaps(
    var_by_domain: dict[str, list[str]],
    rng: np.random.Generator,
) -> dict[str, list[str]]:
    """
    Generate a swap mapping for bootstrap perturbation.

    Returns a dict of domain_id -> resampled column list. The same
    mapping must be applied to both normalized and raw DataFrames
    so that models receiving both (e.g., V-Dem) get consistent data.
    """
    swaps = {}
    for domain_id, cols in var_by_domain.items():
        if not cols:
            continue
        swaps[domain_id] = list(rng.choice(cols, size=len(cols), replace=True))
    return swaps


def _apply_domain_swaps(
    model_df: pd.DataFrame,
    var_by_domain: dict[str, list[str]],
    swaps: dict[str, list[str]],
) -> pd.DataFrame:
    """
    Apply a pre-generated swap mapping to a DataFrame.

    The perturbation swaps column data within each domain. For example,
    if economic_stress has columns ['1', '2', '5'], a resample might
    produce ['2', '2', '1'], meaning var_1 gets var_2's data, var_2
    keeps its data, and var_5 gets var_1's data.
    """
    perturbed = model_df.copy()
    for domain_id, cols in var_by_domain.items():
        if domain_id not in swaps:
            continue
        resampled_cols = swaps[domain_id]
        for i, orig_col in enumerate(cols):
            var_col = f"var_{orig_col}"
            source_col = f"var_{resampled_cols[i]}"
            if var_col in perturbed.columns and source_col in perturbed.columns:
                perturbed[var_col] = model_df[source_col].values
    return perturbed


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
