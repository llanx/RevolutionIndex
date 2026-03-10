"""
Score calibration: map raw ensemble output to the 0-100 scale using
historical anchor points.

Anchor points (locked decision from CONTEXT.md):
- 2008 financial crisis: should score in Crisis Territory (51-75)
- 2020 (COVID + social unrest): should score in Crisis Territory (51-75)
- Mid-1990s (stability period): should score in Stable (0-25)

Calibration method: piecewise linear interpolation through anchor points.
Uses np.interp for exact pass-through at every anchor (zero residual),
with linear extrapolation beyond the anchor range.

Also provides:
- Velocity overlay: adjusts raw scores by domain-level rate of change
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
# Piecewise linear interpolation passes exactly through every anchor.
# ---------------------------------------------------------------------------

DEFAULT_ANCHORS = [
    # (date_spec, target_score, label)
    # date_spec: "YYYY-MM" for a single month, or ("YYYY-MM", "YYYY-MM") for average over range
    {"date": "2008-10", "target": 65.0, "label": "Financial crisis peak"},
    {"date": "2020-06", "target": 65.0, "label": "COVID + BLM peak"},
    {"date": ("1994-01", "1997-12"), "target": 20.0, "label": "Mid-1990s stability"},
    {"date": "2001-09", "target": 42.0, "label": "Post-9/11 + dot-com recession"},
    # 2011-08 anchor removed: the acute anomaly from 2008 aftermath makes
    # it score higher than 2020 in adjusted space, creating non-monotonic
    # calibration. The remaining 4 anchors are monotonic and produce
    # well-spread calibration breakpoints.
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
) -> tuple[np.ndarray, np.ndarray, list[dict]]:
    """
    Build piecewise linear breakpoints from anchor points.

    Returns (raw_breakpoints, target_breakpoints, residuals) as numpy arrays.
    np.interp(x, raw_breakpoints, target_breakpoints) gives the calibrated score.
    Residuals are always zero for piecewise (exact pass-through).
    Falls back to identity mapping if fewer than 2 anchors match data.

    Note: The calibration mapping may be non-monotonic when anchor raw
    scores do not follow the same ordering as their target scores. This
    occurs because structural trend variables (debt, polarization) can
    make nominally "stable" periods score higher in raw terms than mild
    recessions. This is a documented limitation of the current model.
    """
    if anchors is None:
        anchors = DEFAULT_ANCHORS

    if not isinstance(raw_scores.index, pd.DatetimeIndex):
        raw_scores = raw_scores.copy()
        raw_scores.index = pd.to_datetime(raw_scores.index)

    # Collect (raw_value, target_value) pairs from available anchors
    pairs = []
    anchor_labels = []

    for anchor in anchors:
        raw_val = _get_anchor_raw_score(raw_scores, anchor["date"])
        if raw_val is not None:
            pairs.append((raw_val, anchor["target"]))
            anchor_labels.append(anchor["label"])

    if len(pairs) < 2:
        return np.array([0.0, 100.0]), np.array([0.0, 100.0]), []

    # Sort by raw value (required by np.interp)
    pairs.sort(key=lambda p: p[0])

    # Handle duplicate raw values by averaging targets
    deduped = {}
    for raw_val, target_val in pairs:
        key = round(raw_val, 6)
        if key not in deduped:
            deduped[key] = []
        deduped[key].append(target_val)

    raw_bp = np.array(sorted(deduped.keys()))
    target_bp = np.array([np.mean(deduped[k]) for k in sorted(deduped.keys())])

    # Build residuals (always zero for piecewise, but include for reporting)
    residuals = []
    for i, label in enumerate(anchor_labels):
        raw_val, target_val = pairs[i]
        fitted = float(np.interp(raw_val, raw_bp, target_bp))
        error = fitted - target_val
        residuals.append({
            "label": label,
            "target": target_val,
            "raw": round(raw_val, 2),
            "fitted": round(fitted, 2),
            "error": round(error, 2),
        })

    return raw_bp, target_bp, residuals


def _extend_breakpoints(
    raw_bp: np.ndarray,
    target_bp: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Extend breakpoints for linear extrapolation beyond the anchor range.

    Uses the slope of the nearest segment to extrapolate to 0 and 100
    on the target scale.
    """
    if len(raw_bp) < 2:
        return raw_bp, target_bp

    # Extrapolate left: use slope of first segment
    left_slope = (target_bp[1] - target_bp[0]) / max(raw_bp[1] - raw_bp[0], 1e-9)
    # Find raw value that maps to target=0
    if target_bp[0] > 0 and left_slope > 0:
        raw_at_zero = raw_bp[0] - target_bp[0] / left_slope
        extended_raw = [raw_at_zero]
        extended_target = [0.0]
    else:
        extended_raw = [raw_bp[0] - 10.0]
        extended_target = [0.0]

    # Add original breakpoints
    extended_raw.extend(raw_bp.tolist())
    extended_target.extend(target_bp.tolist())

    # Extrapolate right: use slope of last segment, but ensure gradual
    # approach to 100. When the last segment is flat (both anchors at
    # same target), use a gentle slope spread over 50 raw points to
    # avoid sharp jumps to Revolution Territory.
    right_slope = (target_bp[-1] - target_bp[-2]) / max(raw_bp[-1] - raw_bp[-2], 1e-9)
    if target_bp[-1] < 100 and right_slope > 0:
        raw_at_100 = raw_bp[-1] + (100.0 - target_bp[-1]) / right_slope
        extended_raw.append(raw_at_100)
        extended_target.append(100.0)
    else:
        # Gentle right extension: spread the 65→100 gap over 50 raw units
        # so only truly extreme events reach Revolution Territory
        extended_raw.append(raw_bp[-1] + 50.0)
        extended_target.append(100.0)

    return np.array(extended_raw), np.array(extended_target)


def apply_velocity_overlay(
    raw_history: pd.Series,
    domain_scores_df: pd.DataFrame,
    anomaly_scale: float = 150.0,
    ema_span: int = 120,
    **kwargs,
) -> pd.Series:
    """
    Adjust raw scores using domain-level anomaly from long-term baseline.

    Replaces the noisy velocity (derivative) approach with anomaly
    (deviation from trend). This solves the structural ordering problem
    because:
    - Calm periods: domains near their 10-year EMA → anomaly ≈ 0 →
      adjusted ≈ EMA baseline (tracks slow structural drift)
    - Crisis periods: domains spike above their EMA → large positive
      anomaly → adjusted pushed well above baseline

    The gap between calm and crisis now depends on domain DEVIATIONS,
    not absolute levels (which are trend-contaminated).

    Formula:
        baseline = raw_history.ewm(ema_span).mean()
        domain_anomaly = domain_score - domain_score.ewm(ema_span).mean()
        max_anomaly = max(domain_anomaly across domains, clipped >= 0)
        adjusted = baseline + max_anomaly * anomaly_scale

    Parameters
    ----------
    raw_history : pd.Series
        Raw (uncalibrated) composite scores with DatetimeIndex or date strings.
    domain_scores_df : pd.DataFrame
        Domain-level scores (0-1) with DatetimeIndex, columns = domain IDs.
    anomaly_scale : float
        Scales weighted domain anomaly (typically ±0.05) to score units.
        Default 300.0 maps a +0.10 anomaly to +30 score points.
    ema_span : int
        Span for exponential moving average baseline (months).
        Default 120 (10 years).

    Returns
    -------
    pd.Series
        Adjusted scores combining structural baseline with anomaly signal.
    """
    from models.config import DOMAIN_WEIGHTS, Domain

    if raw_history.empty or domain_scores_df.empty:
        return raw_history.copy()

    # Ensure DatetimeIndex on both
    history = raw_history.copy()
    if not isinstance(history.index, pd.DatetimeIndex):
        history.index = pd.to_datetime(history.index)

    domain_df = domain_scores_df.copy()
    if not isinstance(domain_df.index, pd.DatetimeIndex):
        domain_df.index = pd.to_datetime(domain_df.index)

    # Build domain weight mapping (string keys)
    dw = {d.value: w for d, w in DOMAIN_WEIGHTS.items()}
    total_weight = sum(dw.get(col, 0) for col in domain_df.columns if col in dw)
    if total_weight == 0:
        return history

    # 1. Structural baseline: EMA of raw composite scores
    #    Tracks the slow structural drift (polarization, inequality trends)
    baseline = history.ewm(span=ema_span, min_periods=12).mean()

    # 2. Domain anomalies: deviation from each domain's own 10-year EMA
    domain_ema = domain_df.ewm(span=ema_span, min_periods=12).mean()
    domain_anomaly = domain_df - domain_ema

    # 3. Max anomaly from CRISIS-RESPONSIVE domains only.
    #    Trend domains (polarization, institutional quality, media) rise
    #    monotonically and are always above their EMA, creating persistent
    #    false anomalies. Crisis-responsive domains (economic stress,
    #    social mobilization) spike during actual crises then revert.
    acute_domains = ['economic_stress', 'social_mobilization']
    acute_cols = [c for c in acute_domains if c in domain_anomaly.columns]
    if not acute_cols:
        return history

    max_anomaly = domain_anomaly[acute_cols].max(axis=1).clip(lower=0)
    # Smooth with 3-month rolling average to reduce single-month spikes
    max_anomaly = max_anomaly.rolling(window=3, min_periods=1).mean()

    # 4. Combine baseline + scaled max anomaly
    adjusted = history.copy()
    for date_idx in history.index:
        if date_idx in baseline.index and date_idx in max_anomaly.index:
            b = baseline.loc[date_idx]
            a = max_anomaly.loc[date_idx]
            if not np.isnan(b) and not np.isnan(a):
                adjusted.loc[date_idx] = b + a * anomaly_scale

    return adjusted


def calibrate(
    raw_scores: pd.Series,
    anchors: list[dict] = None,
) -> pd.Series:
    """
    Calibrate raw ensemble scores using piecewise linear interpolation
    through anchor points.

    Method:
    1. Extract raw scores at each anchor date
    2. Build piecewise linear mapping via np.interp
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

    raw_bp, target_bp, residuals = _fit_calibration(raw_scores, anchors)

    if not isinstance(raw_scores.index, pd.DatetimeIndex):
        raw_scores = raw_scores.copy()
        raw_scores.index = pd.to_datetime(raw_scores.index)

    # Extend breakpoints for extrapolation
    ext_raw, ext_target = _extend_breakpoints(raw_bp, target_bp)

    calibrated_vals = np.interp(raw_scores.values, ext_raw, ext_target)
    calibrated = pd.Series(calibrated_vals, index=raw_scores.index)
    calibrated = calibrated.clip(0, 100)

    return calibrated


def get_calibration_coefficients(
    raw_scores: pd.Series,
    anchors: list[dict] = None,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Extract the piecewise linear calibration breakpoints.

    Returns (raw_breakpoints, target_breakpoints) arrays.
    Use np.interp(score, raw_bp, target_bp) to calibrate.
    If calibration cannot be computed, returns identity mapping.
    """
    if raw_scores.empty:
        return np.array([0.0, 100.0]), np.array([0.0, 100.0])

    raw_bp, target_bp, _residuals = _fit_calibration(raw_scores, anchors)
    return raw_bp, target_bp


# ---------------------------------------------------------------------------
# Bootstrap confidence intervals
# ---------------------------------------------------------------------------

def compute_bootstrap_ci(
    unified_df: pd.DataFrame,
    calibration_coeffs: tuple[np.ndarray, np.ndarray] = None,
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
    3. Apply the piecewise calibration transform to each bootstrap score
    4. Extract ci_width percentile interval

    Parameters
    ----------
    unified_df : pd.DataFrame
        Unified DataFrame from pipeline with columns = catalog numbers
        (as strings), values in 0.0-1.0.
    calibration_coeffs : tuple[np.ndarray, np.ndarray]
        (raw_bp, target_bp) from get_calibration_coefficients().
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

    # Default to identity mapping
    if calibration_coeffs is None:
        calibration_coeffs = (np.array([0.0, 100.0]), np.array([0.0, 100.0]))

    raw_bp, target_bp = calibration_coeffs
    # Extend for extrapolation
    ext_raw, ext_target = _extend_breakpoints(raw_bp, target_bp)

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
    bootstrap_scores = []
    for _ in range(n_bootstrap):
        swaps = _generate_domain_swaps(var_by_domain, rng)
        perturbed = _apply_domain_swaps(
            model_df, var_by_domain, swaps,
        )
        raw_perturbed = _apply_domain_swaps(
            raw_model_df, var_by_domain, swaps,
        ) if raw_model_df is not None else None
        score = _run_models_on_slice(perturbed, raw_df_slice=raw_perturbed)
        if score is None:
            score = 50.0
        # Apply piecewise calibration
        calibrated = float(np.interp(score, ext_raw, ext_target))
        calibrated = max(0.0, min(100.0, calibrated))
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
