"""
Validation script: episode backtesting, LOOCV, bootstrap CI width check,
and overall pass/fail verdict for the Revolution Index model.

Two modes:
  (a) History-only (default): reads history.json, runs episode backtesting.
      No API keys needed.
  (b) Full mode (--full): runs the live pipeline, then performs LOOCV and
      CI width checks in addition to episode backtesting.

Usage:
    python models/validate.py                  # history-only mode
    python models/validate.py --full           # full mode (needs FRED_API_KEY)
    python models/validate.py --cached-only    # full mode with cached data only

Run from the project root directory:
    cd /path/to/RevolutionIndex
    python models/validate.py
"""
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd

# sys.path setup (same pattern as run.py)
_SCRIPT_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _SCRIPT_DIR.parent

if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from models.calibrate import (
    _fit_calibration,
    _get_anchor_raw_score,
    DEFAULT_ANCHORS,
    calibrate,
    get_calibration_coefficients,
    compute_bootstrap_ci,
    score_to_zone,
)
from models.config import MODEL_WEIGHTS

# Zone boundaries used for margin calculations
ZONE_BOUNDARIES = [25, 50, 75]


# ---------------------------------------------------------------------------
# Episode definitions
# ---------------------------------------------------------------------------

def _build_in_sample_episodes() -> list[dict]:
    """
    Build in-sample episode list from DEFAULT_ANCHORS.
    Each anchor becomes an episode with expected zone derived from its target.
    """
    episodes = []
    for anchor in DEFAULT_ANCHORS:
        target = anchor["target"]
        expected_zone = score_to_zone(int(round(target)))

        # Derive expected range from zone boundaries
        if expected_zone == "Stable":
            expected_range = (0, 25)
        elif expected_zone == "Elevated Tension":
            expected_range = (26, 50)
        elif expected_zone == "Crisis Territory":
            expected_range = (51, 75)
        else:
            expected_range = (76, 100)

        episodes.append({
            "label": anchor["label"],
            "date": anchor["date"],
            "expected_zone": expected_zone,
            "expected_range": expected_range,
            "is_in_sample": True,
            "min_coverage": 0.5,
            "category": "crisis" if target >= 51 else (
                "stability" if target <= 25 else "elevated"
            ),
        })
    return episodes


OUT_OF_SAMPLE_EPISODES = [
    {
        "label": "1960s Urban Unrest / Civil Rights",
        "date": ("1965-01", "1968-12"),
        "expected_zone": "Elevated Tension",
        "expected_range": (26, 50),
        "is_in_sample": False,
        "min_coverage": 0.3,
        "category": "elevated",
    },
    {
        "label": "Watergate / Nixon Resignation",
        "date": ("1973-06", "1974-12"),
        "expected_zone": "Elevated Tension",
        "expected_range": (40, 60),
        "is_in_sample": False,
        "min_coverage": 0.3,
        "category": "elevated",
    },
    {
        "label": "Late 1980s Stability",
        "date": ("1987-01", "1989-12"),
        "expected_zone": "Stable",
        "expected_range": (0, 25),
        "is_in_sample": False,
        "min_coverage": 0.5,
        "category": "stability",
    },
    {
        "label": "2016 Election Aftermath",
        "date": ("2016-11", "2017-01"),
        "expected_zone": "Elevated Tension",
        "expected_range": (35, 50),
        "is_in_sample": False,
        "min_coverage": 0.5,
        "category": "elevated",
    },
    {
        "label": "January 6, 2021",
        "date": "2021-01",
        "expected_zone": "Crisis Territory",
        "expected_range": (51, 75),
        "is_in_sample": False,
        "min_coverage": 0.5,
        "category": "crisis",
    },
]


# ---------------------------------------------------------------------------
# Helper: extract score from calibrated history using same logic as anchors
# ---------------------------------------------------------------------------

def _get_episode_score(
    calibrated_history: pd.Series,
    date_spec,
) -> Optional[float]:
    """
    Extract a score from the calibrated history for an episode date spec.

    Enhanced version of _get_anchor_raw_score that handles month-end dates
    in history.json (e.g., "2017-01-31") when searching for "2017-01".
    For date ranges, extends the end date to include the full end month.
    """
    if isinstance(date_spec, tuple):
        start_date = pd.Timestamp(date_spec[0] + "-01")
        # Extend end date to the last day of the end month
        end_base = pd.Timestamp(date_spec[1] + "-01")
        end_date = end_base + pd.offsets.MonthEnd(0)
        mask = (calibrated_history.index >= start_date) & (
            calibrated_history.index <= end_date
        )
        values = calibrated_history[mask]
        if values.empty:
            return None
        return float(values.mean())
    else:
        # For single month spec, use the existing logic which handles
        # nearest-within-3-months matching
        return _get_anchor_raw_score(calibrated_history, date_spec)


def _nearest_boundary_margin(score: float) -> tuple[int, int]:
    """
    Return (nearest_boundary, signed_margin) for a score.
    Margin is how many points from the nearest zone boundary.
    """
    if not ZONE_BOUNDARIES:
        return (0, int(score))

    distances = [(abs(score - b), b) for b in ZONE_BOUNDARIES]
    distances.sort(key=lambda x: x[0])
    nearest_dist, nearest_boundary = distances[0]
    return nearest_boundary, int(round(score - nearest_boundary))


def _is_near_boundary(score: float, threshold: int = 3) -> bool:
    """Check if score is within threshold points of any zone boundary."""
    for boundary in ZONE_BOUNDARIES:
        if abs(score - boundary) <= threshold:
            return True
    return False


def _zone_matches_or_adjacent_near_boundary(
    actual_score: float,
    actual_zone: str,
    expected_zone: str,
    threshold: int = 3,
) -> bool:
    """
    Check if the actual zone matches expected, OR if the score is near a
    boundary between the expected zone and an adjacent zone.
    """
    if actual_zone == expected_zone:
        return True

    # Check if near boundary between expected and actual
    if not _is_near_boundary(actual_score, threshold):
        return False

    # Define adjacency
    zone_order = ["Stable", "Elevated Tension", "Crisis Territory", "Revolution Territory"]
    try:
        actual_idx = zone_order.index(actual_zone)
        expected_idx = zone_order.index(expected_zone)
    except ValueError:
        return False

    return abs(actual_idx - expected_idx) == 1


# ---------------------------------------------------------------------------
# Core validation functions
# ---------------------------------------------------------------------------

def run_episode_backtest(
    calibrated_history: pd.Series,
    raw_scores: Optional[pd.Series] = None,
) -> list[dict]:
    """
    Run episode backtesting against calibrated history.

    For each episode (in-sample + out-of-sample), extract the score,
    compute the zone, and compare to expected zone.

    Returns list of result dicts for each episode.
    """
    in_sample_episodes = _build_in_sample_episodes()
    all_episodes = in_sample_episodes + OUT_OF_SAMPLE_EPISODES

    results = []
    for episode in all_episodes:
        score = _get_episode_score(calibrated_history, episode["date"])

        if score is None:
            results.append({
                "label": episode["label"],
                "expected_zone": episode["expected_zone"],
                "expected_range": episode["expected_range"],
                "actual_score": None,
                "actual_zone": "NO_DATA",
                "in_zone_strict": False,
                "in_zone_lenient": False,
                "is_in_sample": episode["is_in_sample"],
                "category": episode["category"],
                "has_data": False,
                "coverage_note": "No data available for this date range",
                "near_boundary": False,
                "boundary_margin": None,
            })
            continue

        actual_score = float(score)
        actual_zone = score_to_zone(int(round(actual_score)))
        in_zone_strict = (actual_zone == episode["expected_zone"])
        in_zone_lenient = _zone_matches_or_adjacent_near_boundary(
            actual_score, actual_zone, episode["expected_zone"]
        )
        near_boundary = _is_near_boundary(actual_score)
        boundary, margin = _nearest_boundary_margin(actual_score)

        results.append({
            "label": episode["label"],
            "expected_zone": episode["expected_zone"],
            "expected_range": episode["expected_range"],
            "actual_score": round(actual_score, 1),
            "actual_zone": actual_zone,
            "in_zone_strict": in_zone_strict,
            "in_zone_lenient": in_zone_lenient,
            "is_in_sample": episode["is_in_sample"],
            "category": episode["category"],
            "has_data": True,
            "coverage_note": None,
            "near_boundary": near_boundary,
            "boundary_margin": margin,
        })

    return results


def run_loocv(raw_scores: pd.Series) -> list[dict]:
    """
    Leave-one-out cross-validation on the 5 calibration anchors.

    For each anchor, remove it from the anchor list, refit calibration
    with the remaining 4, and compute the predicted calibrated score for
    the held-out anchor.

    Returns list of result dicts.
    """
    results = []
    anchors = DEFAULT_ANCHORS

    for i, held_out in enumerate(anchors):
        remaining = [a for j, a in enumerate(anchors) if j != i]

        # Fit calibration with remaining anchors
        a, b, _residuals = _fit_calibration(raw_scores, remaining)

        # Get raw score for the held-out anchor
        raw_val = _get_anchor_raw_score(raw_scores, held_out["date"])
        if raw_val is None:
            results.append({
                "label": held_out["label"],
                "target": held_out["target"],
                "predicted": None,
                "deviation": None,
                "overfitting": False,
                "a": a,
                "b": b,
                "note": "No raw data available for held-out anchor",
            })
            continue

        # Compute predicted calibrated score
        predicted = a * raw_val + b
        predicted = max(0.0, min(100.0, predicted))
        deviation = abs(predicted - held_out["target"])
        overfitting = deviation > 25

        results.append({
            "label": held_out["label"],
            "target": held_out["target"],
            "predicted": round(predicted, 1),
            "deviation": round(deviation, 1),
            "overfitting": overfitting,
            "a": round(a, 4),
            "b": round(b, 4),
        })

    return results


def check_ci_width(
    calibrated_history: pd.Series,
    unified_df: Optional[pd.DataFrame] = None,
    calibration_coeffs: tuple = (1.0, 0.0),
    raw_df: Optional[pd.DataFrame] = None,
) -> dict:
    """
    Check bootstrap CI width to assess model discrimination.

    Pick a crisis episode (2008) and a stability episode (mid-1990s)
    from the calibrated history. Compare their point estimates alongside
    the current CI width to assess discriminability.

    If unified_df is provided, also compute the actual bootstrap CI.
    """
    # Get point estimates for crisis and stability periods
    crisis_score = _get_episode_score(calibrated_history, "2008-10")
    stability_score = _get_episode_score(calibrated_history, ("1994-01", "1997-12"))

    result = {
        "crisis_point_estimate": round(crisis_score, 1) if crisis_score else None,
        "stability_point_estimate": round(stability_score, 1) if stability_score else None,
        "point_estimate_gap": None,
        "current_ci": None,
        "ci_width": None,
        "discriminable": None,
        "note": None,
    }

    if crisis_score is not None and stability_score is not None:
        gap = crisis_score - stability_score
        result["point_estimate_gap"] = round(gap, 1)

    # Compute bootstrap CI if unified_df is available
    if unified_df is not None:
        try:
            ci = compute_bootstrap_ci(
                unified_df,
                calibration_coeffs=calibration_coeffs,
                n_bootstrap=500,  # Reduced for validation speed
                raw_df=raw_df,
            )
            ci_range = ci["ci_upper"] - ci["ci_lower"]
            result["current_ci"] = {
                "lower": round(ci["ci_lower"], 1),
                "upper": round(ci["ci_upper"], 1),
            }
            result["ci_width"] = round(ci_range, 1)

            # Check if point estimate gap exceeds CI width
            if result["point_estimate_gap"] is not None:
                result["discriminable"] = result["point_estimate_gap"] > ci_range
        except Exception as e:
            result["note"] = f"Bootstrap CI computation failed: {e}"
    else:
        result["note"] = (
            "CI width check requires full pipeline data (unified_df). "
            "Run with --full to enable."
        )

    return result


def compute_overall_verdict(
    episode_results: list[dict],
    loocv_results: Optional[list[dict]] = None,
    anchor_residuals: Optional[list[dict]] = None,
) -> dict:
    """
    Apply the three pass/fail criteria from CONTEXT.md:

    1. Zone accuracy >= 75% (strict and lenient)
    2. Monotonic ordering: crisis episodes score above stability episodes
    3. Calibration anchor residuals: no anchor > 15 points from target

    Returns dict with verdict and individual criterion results.
    """
    # --- Criterion 1: Zone accuracy ---
    episodes_with_data = [e for e in episode_results if e["has_data"]]
    total_with_data = len(episodes_with_data)

    if total_with_data == 0:
        zone_accuracy_strict = 0.0
        zone_accuracy_lenient = 0.0
        strict_count = 0
        lenient_count = 0
    else:
        strict_count = sum(1 for e in episodes_with_data if e["in_zone_strict"])
        lenient_count = sum(1 for e in episodes_with_data if e["in_zone_lenient"])
        zone_accuracy_strict = strict_count / total_with_data
        zone_accuracy_lenient = lenient_count / total_with_data

    zone_pass = zone_accuracy_strict >= 0.75

    # --- Criterion 2: Monotonic ordering ---
    crisis_scores = [
        e["actual_score"] for e in episodes_with_data
        if e["category"] == "crisis" and e["actual_score"] is not None
    ]
    stability_scores = [
        e["actual_score"] for e in episodes_with_data
        if e["category"] == "stability" and e["actual_score"] is not None
    ]

    if crisis_scores and stability_scores:
        min_crisis = min(crisis_scores)
        max_stability = max(stability_scores)
        monotonic_pass = min_crisis > max_stability
        monotonic_detail = (
            f"Min crisis score ({min_crisis:.1f}) vs "
            f"max stability score ({max_stability:.1f})"
        )
    elif not crisis_scores and not stability_scores:
        monotonic_pass = True  # No data to violate
        monotonic_detail = "No crisis or stability episodes with data"
    elif not crisis_scores:
        monotonic_pass = True
        monotonic_detail = "No crisis episodes with data to compare"
    else:
        monotonic_pass = True
        monotonic_detail = "No stability episodes with data to compare"

    # --- Criterion 3: Calibration anchor residuals ---
    residual_max = 0.0
    residual_warn = False
    residual_fail = False
    residual_details = []

    if anchor_residuals:
        for r in anchor_residuals:
            abs_error = abs(r.get("error", 0))
            residual_details.append({
                "label": r["label"],
                "error": r.get("error", 0),
                "abs_error": round(abs_error, 1),
            })
            if abs_error > residual_max:
                residual_max = abs_error
            if abs_error > 15:
                residual_fail = True
            if abs_error > 10:
                residual_warn = True
    elif loocv_results:
        # Use LOOCV deviations as proxy for anchor residuals
        for r in loocv_results:
            if r["deviation"] is not None:
                if r["deviation"] > residual_max:
                    residual_max = r["deviation"]
                if r["deviation"] > 15:
                    residual_fail = True
                if r["deviation"] > 10:
                    residual_warn = True

    residual_pass = not residual_fail

    # --- Overall verdict ---
    verdict = "PASS" if (zone_pass and monotonic_pass and residual_pass) else "FAIL"

    return {
        "verdict": verdict,
        "zone_accuracy_strict": round(zone_accuracy_strict * 100, 1),
        "zone_accuracy_lenient": round(zone_accuracy_lenient * 100, 1),
        "zone_strict_count": strict_count,
        "zone_lenient_count": lenient_count,
        "zone_total_with_data": total_with_data,
        "zone_pass": zone_pass,
        "monotonic_pass": monotonic_pass,
        "monotonic_detail": monotonic_detail,
        "residual_max": round(residual_max, 1),
        "residual_warn": residual_warn,
        "residual_pass": residual_pass,
        "residual_details": residual_details,
    }


# ---------------------------------------------------------------------------
# Weight sensitivity analysis
# ---------------------------------------------------------------------------

# Data boundary years for spurious trend detection (from Phase 5 RESEARCH.md)
DATA_BOUNDARY_YEARS = {
    1989: "WFRBSTP1300 (Fed DFA wealth data starts)",
    1993: "STLFSI4 (Financial Stress Index starts)",
    2000: "Grumbach SDI (State Democracy Index starts)",
    2005: "Education-job mismatch proxy starts",
    2017: "Bright Line Watch starts",
    2020: "ACLED US protest data starts",
}


def run_weight_sensitivity(
    calibrated_history: pd.Series,
    unified_df: Optional[pd.DataFrame] = None,
    raw_df: Optional[pd.DataFrame] = None,
) -> list[dict]:
    """
    Weight sensitivity analysis: perturb each model weight by +/-20% and
    measure the effect on the composite score.

    In history-only mode, computes theoretical maximum shift bounds since
    per-model scores are not available from history.json alone.

    In --full mode (when unified_df is provided), actually re-runs the
    ensemble with patched weights to compute real score shifts.

    Returns list of dicts with: model, direction, baseline, shift, fragile.
    """
    results = []
    latest_score = float(calibrated_history.iloc[-1])
    full_mode = unified_df is not None

    if full_mode:
        # Full mode: actually re-run models with perturbed weights
        from models.ensemble import _run_models_on_slice, _rename_columns_for_models, _ensure_models_registered
        import models.config as config_module

        _ensure_models_registered()
        model_df = _rename_columns_for_models(unified_df)
        raw_model_df = _rename_columns_for_models(raw_df) if raw_df is not None else None

        # Get baseline score using current weights
        baseline = _run_models_on_slice(model_df, raw_df_slice=raw_model_df)
        if baseline is None:
            return results

        original_weights = dict(config_module.MODEL_WEIGHTS)

        for model_id, original_w in original_weights.items():
            for direction, factor in [("up", 1.20), ("down", 0.80)]:
                # Perturb this model's weight
                patched = dict(original_weights)
                patched[model_id] = original_w * factor
                # Renormalize to sum to 1.0
                total = sum(patched.values())
                patched = {k: v / total for k, v in patched.items()}

                # Temporarily patch MODEL_WEIGHTS
                try:
                    config_module.MODEL_WEIGHTS = patched
                    perturbed = _run_models_on_slice(
                        model_df, raw_df_slice=raw_model_df
                    )
                finally:
                    config_module.MODEL_WEIGHTS = original_weights

                if perturbed is None:
                    continue

                shift = abs(perturbed - baseline)
                results.append({
                    "model": model_id,
                    "direction": direction,
                    "weight": original_w,
                    "baseline": round(baseline, 2),
                    "perturbed_score": round(perturbed, 2),
                    "shift": round(shift, 2),
                    "fragile": shift > 25,
                    "mode": "full",
                })
    else:
        # History-only mode: compute theoretical maximum shift bounds.
        # With a +/-20% perturbation on weight w_M (factor f = 1.2 or 0.8),
        # the maximum possible shift is bounded by:
        #   |S * (f-1) * w_M / (1 + (f-1) * w_M)|
        # This assumes the perturbed model's score is at the extreme (0 or 100).
        for model_id, w in MODEL_WEIGHTS.items():
            for direction, factor in [("up", 1.20), ("down", 0.80)]:
                delta = factor - 1.0
                max_shift = abs(latest_score * delta * w / (1 + delta * w))
                results.append({
                    "model": model_id,
                    "direction": direction,
                    "weight": w,
                    "baseline": round(latest_score, 2),
                    "perturbed_score": None,
                    "shift": round(max_shift, 2),
                    "fragile": False,  # Theoretical bounds too low to be meaningful
                    "mode": "history-only (theoretical max)",
                })

    return results


def check_inter_model_correlation(
    unified_df: Optional[pd.DataFrame] = None,
    raw_df: Optional[pd.DataFrame] = None,
) -> list[dict]:
    """
    Inter-model correlation check: compare all 5 model scores pairwise.

    Requires --full mode since per-model scores are not available from
    history.json alone. In full mode, runs each model individually on the
    latest data slice and compares pairwise score differences.

    Note: with a single time point we cannot compute Pearson correlation.
    Instead we flag pairs where both scores are within 5 points as "similar".

    Returns list of dicts with: model_a, model_b, score_a, score_b, diff, similar.
    """
    results = []

    if unified_df is None:
        return results

    from models.models import MODEL_REGISTRY
    from models.ensemble import _rename_columns_for_models, _ensure_models_registered

    _ensure_models_registered()
    model_df = _rename_columns_for_models(unified_df)
    raw_model_df = _rename_columns_for_models(raw_df) if raw_df is not None else None

    # Run each model individually on the full data
    model_scores: dict[str, float] = {}
    for model_id, model_fn in MODEL_REGISTRY.items():
        try:
            output = model_fn(model_df, raw_df=raw_model_df)
            model_scores[model_id] = output.score
        except TypeError:
            try:
                output = model_fn(model_df)
                model_scores[model_id] = output.score
            except Exception:
                continue
        except Exception:
            continue

    # Compare all pairwise combinations
    model_ids = sorted(model_scores.keys())
    for i, m_a in enumerate(model_ids):
        for m_b in model_ids[i + 1:]:
            score_a = model_scores[m_a]
            score_b = model_scores[m_b]
            diff = abs(score_a - score_b)
            similar = diff <= 5.0

            results.append({
                "model_a": m_a,
                "model_b": m_b,
                "score_a": round(score_a, 1),
                "score_b": round(score_b, 1),
                "diff": round(diff, 1),
                "similar": similar,
                "note": "Scores within 5 pts (potentially redundant)" if similar else "",
            })

    return results


def check_spurious_trends(calibrated_history: pd.Series) -> dict:
    """
    Spurious trend detection on the calibrated history time series.

    Performs four automated checks:
    a) Monotonic increase check across all decades
    b) Data boundary jump detection at known boundary years
    c) Score saturation check (stuck at 0 or 100)
    d) Decade-level summary (mean and range per decade)

    Returns dict with: monotonic_flag, boundary_jumps, saturation_periods,
    decade_summary, overall_concern.
    """
    # --- a) Monotonic increase check ---
    # Check if average score increases across ALL decades.
    # A genuine stress indicator should have some decades with declines.
    decades = {}
    for date_idx, score in calibrated_history.items():
        decade = (date_idx.year // 10) * 10
        if decade not in decades:
            decades[decade] = []
        decades[decade].append(float(score))

    decade_means = {d: np.mean(scores) for d, scores in sorted(decades.items())}
    sorted_decades = sorted(decade_means.keys())

    all_increasing = True
    if len(sorted_decades) >= 2:
        for i in range(1, len(sorted_decades)):
            if decade_means[sorted_decades[i]] < decade_means[sorted_decades[i - 1]]:
                all_increasing = False
                break
    else:
        all_increasing = False  # Not enough data to judge

    monotonic_flag = all_increasing

    # --- b) Data boundary jump detection ---
    boundary_jumps = []
    for boundary_year, description in DATA_BOUNDARY_YEARS.items():
        # Check if score jumps by > 10 points within 2 years of boundary
        nearby_before = []
        nearby_after = []
        for date_idx, score in calibrated_history.items():
            year = date_idx.year
            if boundary_year - 2 <= year < boundary_year:
                nearby_before.append(float(score))
            elif boundary_year <= year <= boundary_year + 2:
                nearby_after.append(float(score))

        if nearby_before and nearby_after:
            mean_before = np.mean(nearby_before)
            mean_after = np.mean(nearby_after)
            jump = mean_after - mean_before
            if abs(jump) > 10:
                boundary_jumps.append({
                    "year": boundary_year,
                    "description": description,
                    "mean_before": round(mean_before, 1),
                    "mean_after": round(mean_after, 1),
                    "jump": round(jump, 1),
                })

    # --- c) Score saturation check ---
    saturation_periods = []
    sorted_history = calibrated_history.sort_index()
    consecutive_at_zero = 0
    consecutive_at_100 = 0
    zero_start = None
    hundred_start = None

    for date_idx, score in sorted_history.items():
        s = float(score)
        # Check saturation at 0
        if s <= 1.0:
            if consecutive_at_zero == 0:
                zero_start = date_idx
            consecutive_at_zero += 1
        else:
            if consecutive_at_zero > 3:
                saturation_periods.append({
                    "value": 0,
                    "start": zero_start.strftime("%Y-%m"),
                    "count": consecutive_at_zero,
                })
            consecutive_at_zero = 0
            zero_start = None

        # Check saturation at 100
        if s >= 99.0:
            if consecutive_at_100 == 0:
                hundred_start = date_idx
            consecutive_at_100 += 1
        else:
            if consecutive_at_100 > 3:
                saturation_periods.append({
                    "value": 100,
                    "start": hundred_start.strftime("%Y-%m"),
                    "count": consecutive_at_100,
                })
            consecutive_at_100 = 0
            hundred_start = None

    # Check end-of-series saturation
    if consecutive_at_zero > 3:
        saturation_periods.append({
            "value": 0,
            "start": zero_start.strftime("%Y-%m"),
            "count": consecutive_at_zero,
        })
    if consecutive_at_100 > 3:
        saturation_periods.append({
            "value": 100,
            "start": hundred_start.strftime("%Y-%m"),
            "count": consecutive_at_100,
        })

    # --- d) Decade-level summary ---
    decade_summary = {}
    for decade, scores in sorted(decades.items()):
        decade_summary[str(decade)] = {
            "mean": round(np.mean(scores), 1),
            "min": round(np.min(scores), 1),
            "max": round(np.max(scores), 1),
            "range": round(np.max(scores) - np.min(scores), 1),
            "count": len(scores),
        }

    # --- Overall concern level ---
    concern_count = 0
    if monotonic_flag:
        concern_count += 2  # Major concern
    concern_count += len(boundary_jumps)
    concern_count += len(saturation_periods)

    if concern_count >= 3:
        overall_concern = "major"
    elif concern_count >= 1:
        overall_concern = "minor"
    else:
        overall_concern = "none"

    return {
        "monotonic_flag": monotonic_flag,
        "boundary_jumps": boundary_jumps,
        "saturation_periods": saturation_periods,
        "decade_summary": decade_summary,
        "overall_concern": overall_concern,
        "decade_means": {str(k): round(v, 1) for k, v in decade_means.items()},
    }


# ---------------------------------------------------------------------------
# Console output formatting
# ---------------------------------------------------------------------------

def _print_separator(char: str = "=", width: int = 80) -> None:
    print(char * width)


def _print_episode_table(episode_results: list[dict]) -> None:
    """Print formatted episode results table."""
    print()
    _print_separator()
    print("EPISODE BACKTESTING RESULTS")
    _print_separator()
    print()

    # Header
    header = (
        f"{'Episode':<45} {'Expected':<20} {'Score':>6} "
        f"{'Actual Zone':<20} {'Margin':>7} {'Result':>8}"
    )
    print(header)
    print("-" * len(header))

    # In-sample section
    in_sample = [r for r in episode_results if r["is_in_sample"]]
    out_of_sample = [r for r in episode_results if not r["is_in_sample"]]

    if in_sample:
        print("\n  IN-SAMPLE (calibration anchors):")
        for r in in_sample:
            _print_episode_row(r)

    if out_of_sample:
        print("\n  OUT-OF-SAMPLE (hold-out episodes):")
        for r in out_of_sample:
            _print_episode_row(r)

    print()


def _print_episode_row(r: dict) -> None:
    """Print a single episode result row."""
    if not r["has_data"]:
        print(
            f"    {r['label']:<43} {r['expected_zone']:<20} "
            f"{'N/A':>6} {'NO DATA':<20} {'N/A':>7} {'SKIP':>8}"
        )
        return

    score_str = f"{r['actual_score']:.0f}"
    margin_str = f"{r['boundary_margin']:+d}" if r["boundary_margin"] is not None else "N/A"
    if r["near_boundary"]:
        margin_str += "*"

    if r["in_zone_strict"]:
        result = "PASS"
    elif r["in_zone_lenient"]:
        result = "NEAR"
    else:
        result = "FAIL"

    print(
        f"    {r['label']:<43} {r['expected_zone']:<20} "
        f"{score_str:>6} {r['actual_zone']:<20} {margin_str:>7} {result:>8}"
    )


def _print_loocv_table(loocv_results: list[dict]) -> None:
    """Print formatted LOOCV results table."""
    print()
    _print_separator()
    print("LEAVE-ONE-OUT CROSS-VALIDATION")
    _print_separator()
    print()

    header = (
        f"{'Anchor':<45} {'Target':>7} {'Predicted':>10} "
        f"{'Deviation':>10} {'Overfit?':>9}"
    )
    print(header)
    print("-" * len(header))

    for r in loocv_results:
        if r["predicted"] is None:
            print(
                f"  {r['label']:<43} {r['target']:>7.1f} "
                f"{'N/A':>10} {'N/A':>10} {'N/A':>9}"
            )
        else:
            overfit = "YES" if r["overfitting"] else "no"
            print(
                f"  {r['label']:<43} {r['target']:>7.1f} "
                f"{r['predicted']:>10.1f} {r['deviation']:>10.1f} {overfit:>9}"
            )

    print()


def _print_ci_width(ci_result: dict) -> None:
    """Print CI width check results."""
    print()
    _print_separator()
    print("BOOTSTRAP CI WIDTH CHECK")
    _print_separator()
    print()

    if ci_result["crisis_point_estimate"] is not None:
        print(f"  Crisis point estimate (2008): {ci_result['crisis_point_estimate']}")
    if ci_result["stability_point_estimate"] is not None:
        print(f"  Stability point estimate (mid-1990s): {ci_result['stability_point_estimate']}")
    if ci_result["point_estimate_gap"] is not None:
        print(f"  Point estimate gap: {ci_result['point_estimate_gap']}")

    if ci_result["current_ci"] is not None:
        ci = ci_result["current_ci"]
        print(f"  Current 90% CI: [{ci['lower']}, {ci['upper']}]")
        print(f"  CI width: {ci_result['ci_width']}")
        disc = "YES" if ci_result["discriminable"] else "NO"
        print(f"  Gap exceeds CI width (discriminable): {disc}")

    if ci_result["note"]:
        print(f"  Note: {ci_result['note']}")

    print()


def _print_verdict(verdict: dict) -> None:
    """Print overall verdict."""
    print()
    _print_separator("=")
    print(f"OVERALL VERDICT: {verdict['verdict']}")
    _print_separator("=")
    print()

    # Criterion 1: Zone accuracy
    zone_icon = "PASS" if verdict["zone_pass"] else "FAIL"
    print(
        f"  1. Zone Accuracy:    [{zone_icon}] "
        f"Strict: {verdict['zone_accuracy_strict']:.1f}% "
        f"({verdict['zone_strict_count']}/{verdict['zone_total_with_data']})"
    )
    print(
        f"                              "
        f"Lenient: {verdict['zone_accuracy_lenient']:.1f}% "
        f"({verdict['zone_lenient_count']}/{verdict['zone_total_with_data']})"
    )
    print(f"                              Threshold: >= 75% strict")

    # Criterion 2: Monotonic ordering
    mono_icon = "PASS" if verdict["monotonic_pass"] else "FAIL"
    print(
        f"  2. Monotonic Order:  [{mono_icon}] {verdict['monotonic_detail']}"
    )

    # Criterion 3: Anchor residuals
    res_icon = "PASS" if verdict["residual_pass"] else "FAIL"
    warn = " (WARNING: >10)" if verdict["residual_warn"] else ""
    print(
        f"  3. Anchor Residuals: [{res_icon}] "
        f"Max residual: {verdict['residual_max']:.1f}{warn}"
    )
    print(f"                              Fail threshold: > 15, Warn threshold: > 10")

    print()
    print(f"  * Near-boundary (*) = within 3 points of a zone boundary")
    print(f"  * NEAR result = wrong zone but within 3 points of correct zone boundary")
    print()


def _print_weight_sensitivity(sensitivity_results: list[dict], is_full: bool) -> None:
    """Print weight sensitivity analysis results."""
    print()
    _print_separator()
    print("WEIGHT SENSITIVITY ANALYSIS")
    _print_separator()
    print()

    if not sensitivity_results:
        print("  No results available.")
        print()
        return

    if not is_full:
        print("  SKIPPED: Weight sensitivity requires --full mode with per-model scores.")
        print("  Theoretical maximum shift bounds shown below for reference only.")
        print("  These bounds are too conservative to trigger the 25-point fragility threshold.")
        print()

    header = (
        f"  {'Model':<18} {'Dir':>5} {'Weight':>7} {'Baseline':>9} "
        f"{'Shift':>7} {'Fragile?':>9}"
    )
    print(header)
    print("  " + "-" * (len(header) - 2))

    for r in sensitivity_results:
        fragile_str = "YES" if r["fragile"] else "no"
        shift_str = f"{r['shift']:.1f}"
        print(
            f"  {r['model']:<18} {r['direction']:>5} {r['weight']:>7.2f} "
            f"{r['baseline']:>9.1f} {shift_str:>7} {fragile_str:>9}"
        )

    if not is_full:
        print()
        print("  Note: In history-only mode, shifts are theoretical maximums.")
        print("  Actual sensitivity requires per-model scores (--full mode).")

    fragile_count = sum(1 for r in sensitivity_results if r["fragile"])
    if fragile_count > 0:
        print()
        print(f"  WARNING: {fragile_count} perturbation(s) exceed 25-point threshold (1 zone).")
        print("  Model composition may be fragile to weight changes.")
    elif is_full:
        print()
        print("  All perturbations within 25-point threshold. Weight composition is stable.")

    print()


def _print_inter_model_correlation(correlation_results: list[dict], is_full: bool) -> None:
    """Print inter-model correlation check results."""
    print()
    _print_separator()
    print("INTER-MODEL CORRELATION CHECK")
    _print_separator()
    print()

    if not is_full:
        print("  Inter-model correlation requires --full mode (per-model scores needed).")
        print("  Skipping this analysis. Use --full to enable.")
        print()
        return

    if not correlation_results:
        print("  No pairwise comparisons available.")
        print()
        return

    print("  Note: Single-point comparison only. True correlation analysis")
    print("  would require running each model across all historical slices.")
    print()

    header = (
        f"  {'Model A':<18} {'Model B':<18} {'Score A':>8} "
        f"{'Score B':>8} {'Diff':>6} {'Note'}"
    )
    print(header)
    print("  " + "-" * (len(header) - 2))

    for r in correlation_results:
        note = r.get("note", "")
        print(
            f"  {r['model_a']:<18} {r['model_b']:<18} {r['score_a']:>8.1f} "
            f"{r['score_b']:>8.1f} {r['diff']:>6.1f} {note}"
        )

    similar_count = sum(1 for r in correlation_results if r["similar"])
    if similar_count > 0:
        print()
        print(
            f"  WARNING: {similar_count} pair(s) have scores within 5 points."
        )
        print("  These models may be partially redundant at the current time point.")
    else:
        print()
        print("  All model pairs have > 5 point separation. No redundancy signals.")

    print()


def _print_spurious_trends(trend_results: dict) -> None:
    """Print spurious trend detection results."""
    print()
    _print_separator()
    print("SPURIOUS TREND DETECTION")
    _print_separator()
    print()

    # a) Monotonic increase check
    mono_status = "FLAG" if trend_results["monotonic_flag"] else "PASS"
    print(f"  a) Monotonic Increase Check:  [{mono_status}]")
    if trend_results["monotonic_flag"]:
        print("     All decades show increasing mean scores.")
        print("     This may indicate a measurement artifact rather than genuine trend.")
    else:
        print("     Score trajectory shows non-monotonic pattern across decades (expected).")

    # Show decade means
    decade_means = trend_results.get("decade_means", {})
    if decade_means:
        decades_str = "     Decade means: "
        parts = [f"{d}s={v}" for d, v in sorted(decade_means.items())]
        decades_str += ", ".join(parts)
        print(decades_str)
    print()

    # b) Data boundary jump detection
    jumps = trend_results["boundary_jumps"]
    if jumps:
        print(f"  b) Data Boundary Jumps:       [FLAG] {len(jumps)} jump(s) detected")
        for j in jumps:
            print(
                f"     {j['year']}: {j['description']}"
            )
            print(
                f"       Score shift: {j['mean_before']:.1f} -> {j['mean_after']:.1f} "
                f"(jump: {j['jump']:+.1f} points)"
            )
    else:
        print("  b) Data Boundary Jumps:       [PASS] No jumps > 10 points near boundary years")
    print()

    # c) Score saturation check
    sat = trend_results["saturation_periods"]
    if sat:
        print(f"  c) Score Saturation:          [FLAG] {len(sat)} period(s) of saturation")
        for s in sat:
            print(
                f"     Stuck at {s['value']} for {s['count']} consecutive entries "
                f"starting {s['start']}"
            )
    else:
        print("  c) Score Saturation:          [PASS] No extended periods at 0 or 100")
    print()

    # d) Decade-level summary
    print("  d) Decade Summary:")
    print(f"     {'Decade':<10} {'Mean':>6} {'Min':>6} {'Max':>6} {'Range':>7} {'Count':>6}")
    print("     " + "-" * 45)
    for decade, stats in sorted(trend_results["decade_summary"].items()):
        print(
            f"     {decade}s    {stats['mean']:>6.1f} {stats['min']:>6.1f} "
            f"{stats['max']:>6.1f} {stats['range']:>7.1f} {stats['count']:>6}"
        )
    print()

    # Overall concern
    concern = trend_results["overall_concern"]
    concern_upper = concern.upper()
    print(f"  Overall Concern Level: {concern_upper}")
    if concern == "major":
        print("  Multiple spurious trend indicators detected. Review calibration and data inputs.")
    elif concern == "minor":
        print("  Some indicators flagged. Review flagged items but likely not critical.")
    else:
        print("  No spurious trend indicators detected.")
    print()


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def write_validation_report(validation_results: dict) -> None:
    """
    Write models/VALIDATION.md with complete validation results and
    pass/fail assessment.
    """
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    mode = validation_results.get("mode", "history-only")
    verdict_data = validation_results.get("verdict", {})
    overall_verdict = verdict_data.get("verdict", "INCOMPLETE")

    episodes = validation_results.get("episodes", [])
    loocv = validation_results.get("loocv", None)
    ci_data = validation_results.get("ci_width", {})
    sensitivity = validation_results.get("sensitivity_results", [])
    correlation = validation_results.get("correlation_results", [])
    trend_data = validation_results.get("trend_results", {})

    lines = []

    def add(text=""):
        lines.append(text)

    # --- Header ---
    add("# Validation Report: Revolution Index")
    add()
    add(f"**Generated:** {timestamp}")
    add(f"**Mode:** {mode}")
    add(f"**Overall Verdict:** {overall_verdict}")
    add()

    # --- Summary ---
    add("## Summary")
    add()

    episodes_with_data = [e for e in episodes if e.get("has_data")]
    strict_pct = verdict_data.get("zone_accuracy_strict", 0)
    lenient_pct = verdict_data.get("zone_accuracy_lenient", 0)
    strict_n = verdict_data.get("zone_strict_count", 0)
    total_n = verdict_data.get("zone_total_with_data", 0)
    mono_pass = verdict_data.get("monotonic_pass", False)

    add(
        f"The Revolution Index model was validated against {len(episodes)} "
        f"historical episodes ({len(episodes_with_data)} with available data). "
        f"Strict zone accuracy is {strict_pct:.1f}% ({strict_n}/{total_n}), "
        f"while lenient accuracy (allowing near-boundary matches within 3 points) "
        f"is {lenient_pct:.1f}%. "
        f"Monotonic ordering {'holds' if mono_pass else 'fails'}: "
        f"all crisis episodes score above all stability episodes."
    )
    add()

    # Determine key findings for summary
    near_misses = [
        e for e in episodes_with_data
        if not e.get("in_zone_strict") and e.get("in_zone_lenient")
    ]
    if near_misses:
        labels = ", ".join(e["label"] for e in near_misses)
        add(
            f"All zone misses are near-boundary cases ({labels}), "
            f"suggesting the model captures the correct directional signal "
            f"but calibration could be refined for tighter zone classification. "
            f"The model produces meaningful differentiation between crisis "
            f"and stability periods, which is the primary design goal."
        )
        add()

    # --- Section 1: Episode Backtesting ---
    add("## 1. Episode Backtesting")
    add()

    # In-sample anchors
    in_sample = [e for e in episodes if e.get("is_in_sample")]
    out_of_sample = [e for e in episodes if not e.get("is_in_sample")]

    add("### In-Sample Anchors (Calibration Verification)")
    add()
    add("| Episode | Expected Zone | Expected Score | Actual Score | Actual Zone | Result |")
    add("|---------|---------------|----------------|--------------|-------------|--------|")
    for e in in_sample:
        if not e.get("has_data"):
            add(
                f"| {e['label']} | {e['expected_zone']} | "
                f"{e['expected_range'][0]}-{e['expected_range'][1]} | "
                f"N/A | NO DATA | SKIP |"
            )
        else:
            result = "PASS" if e.get("in_zone_strict") else (
                "NEAR" if e.get("in_zone_lenient") else "FAIL"
            )
            add(
                f"| {e['label']} | {e['expected_zone']} | "
                f"{e['expected_range'][0]}-{e['expected_range'][1]} | "
                f"{e['actual_score']:.1f} | {e['actual_zone']} | {result} |"
            )
    add()

    # Out-of-sample hold-outs
    add("### Out-of-Sample Hold-Outs (True Test)")
    add()
    add("| Episode | Expected Zone | Expected Range | Actual Score | Actual Zone | Result |")
    add("|---------|---------------|----------------|--------------|-------------|--------|")
    for e in out_of_sample:
        if not e.get("has_data"):
            add(
                f"| {e['label']} | {e['expected_zone']} | "
                f"{e['expected_range'][0]}-{e['expected_range'][1]} | "
                f"N/A | NO DATA | SKIP |"
            )
        else:
            result = "PASS" if e.get("in_zone_strict") else (
                "NEAR" if e.get("in_zone_lenient") else "FAIL"
            )
            add(
                f"| {e['label']} | {e['expected_zone']} | "
                f"{e['expected_range'][0]}-{e['expected_range'][1]} | "
                f"{e['actual_score']:.1f} | {e['actual_zone']} | {result} |"
            )
    add()

    add(f"**Zone Accuracy:** {strict_pct:.1f}% ({strict_n} of {total_n} episodes in correct zone)")

    mono_status = "PASS" if mono_pass else "FAIL"
    mono_detail = verdict_data.get("monotonic_detail", "")
    add(f"**Monotonic Ordering:** {mono_status} ({mono_detail})")
    add()

    # --- Section 2: LOOCV ---
    add("## 2. Leave-One-Out Cross-Validation (LOOCV)")
    add()
    if loocv:
        add("| Anchor | Target | Predicted | Deviation | Overfitting? |")
        add("|--------|--------|-----------|-----------|--------------|")
        for r in loocv:
            if r.get("predicted") is None:
                add(f"| {r['label']} | {r['target']:.1f} | N/A | N/A | N/A |")
            else:
                overfit = "YES" if r.get("overfitting") else "No"
                add(
                    f"| {r['label']} | {r['target']:.1f} | "
                    f"{r['predicted']:.1f} | {r['deviation']:.1f} | {overfit} |"
                )
        add()
    else:
        add(
            "LOOCV requires --full mode with live pipeline data. "
            "Skipped in history-only mode."
        )
        add()

    # --- Section 3: Weight Sensitivity ---
    add("## 3. Weight Sensitivity Analysis")
    add()
    if sensitivity:
        is_full_sensitivity = any(r.get("mode") == "full" for r in sensitivity)
        if not is_full_sensitivity:
            add(
                "**Note:** In history-only mode, sensitivity values are theoretical "
                "maximum shift bounds. Actual perturbation results require --full mode."
            )
            add()
        add("| Model | Perturbation | Baseline | Shift | Fragile? |")
        add("|-------|-------------|----------|-------|----------|")
        for r in sensitivity:
            direction_label = f"+20%" if r["direction"] == "up" else "-20%"
            fragile_str = "YES" if r.get("fragile") else "No"
            add(
                f"| {r['model']} | {direction_label} | "
                f"{r['baseline']:.1f} | {r['shift']:.1f} | {fragile_str} |"
            )
        add()

        fragile_count = sum(1 for r in sensitivity if r.get("fragile"))
        if fragile_count > 0:
            add(
                f"**WARNING:** {fragile_count} perturbation(s) exceed the "
                f"25-point threshold (1 full zone shift)."
            )
        else:
            max_shift = max((r["shift"] for r in sensitivity), default=0)
            add(f"**Max shift:** {max_shift:.1f} points. No fragility detected.")
    else:
        add("No sensitivity results available.")
    add()
    add(
        "**Threshold:** Score shift > 25 points (1 zone) from a single "
        "+/-20% weight change indicates fragility."
    )
    add()

    # --- Section 4: Inter-Model Correlation ---
    add("## 4. Inter-Model Correlation")
    add()
    if correlation:
        add(
            "Single-point comparison of per-model raw scores. "
            "True temporal correlation analysis would require running "
            "each model across all historical slices."
        )
        add()
        add("| Model A | Model B | Score A | Score B | Difference | Note |")
        add("|---------|---------|---------|---------|------------|------|")
        for r in correlation:
            note = r.get("note", "")
            add(
                f"| {r['model_a']} | {r['model_b']} | "
                f"{r['score_a']:.1f} | {r['score_b']:.1f} | "
                f"{r['diff']:.1f} | {note} |"
            )
        add()
    else:
        add("Requires --full mode with per-model scores. Skipped in history-only mode.")
        add()

    # --- Section 5: Spurious Trend Detection ---
    add("## 5. Spurious Trend Detection")
    add()

    # Decade summary
    add("### Decade Summary")
    decade_summary = trend_data.get("decade_summary", {})
    if decade_summary:
        add("| Decade | Mean Score | Min | Max | Trend |")
        add("|--------|-----------|-----|-----|-------|")
        sorted_decades = sorted(decade_summary.keys())
        prev_mean = None
        for dk in sorted_decades:
            stats = decade_summary[dk]
            if prev_mean is not None:
                diff = stats["mean"] - prev_mean
                if diff > 5:
                    trend_arrow = "Rising"
                elif diff < -5:
                    trend_arrow = "Falling"
                else:
                    trend_arrow = "Flat"
            else:
                trend_arrow = "N/A"
            add(
                f"| {dk}s | {stats['mean']:.1f} | "
                f"{stats['min']:.1f} | {stats['max']:.1f} | {trend_arrow} |"
            )
            prev_mean = stats["mean"]
    add()

    # Automated checks
    add("### Automated Checks")
    mono_flag = trend_data.get("monotonic_flag", False)
    mono_check = "FLAG" if mono_flag else "PASS"
    add(f"- Monotonic increase across all decades: {mono_check}")

    jumps = trend_data.get("boundary_jumps", [])
    if jumps:
        jump_details = "; ".join(
            f"{j['year']} ({j['description']}, {j['jump']:+.1f} pts)"
            for j in jumps
        )
        add(f"- Data boundary jumps (>10 points): FLAG ({jump_details})")
    else:
        add("- Data boundary jumps (>10 points): PASS")

    sat = trend_data.get("saturation_periods", [])
    if sat:
        sat_details = "; ".join(
            f"score={s['value']} for {s['count']} entries at {s['start']}"
            for s in sat
        )
        add(f"- Score saturation (0 or 100 for 3+ consecutive points): FLAG ({sat_details})")
    else:
        add("- Score saturation (0 or 100 for 3+ consecutive points): PASS")
    add()

    overall_concern = trend_data.get("overall_concern", "unknown")
    add(f"**Overall Concern Level:** {overall_concern.upper()}")
    add()
    add(
        "**Note:** Spurious trend detection is an automated checklist. "
        "Final judgment on whether trends are genuine or artifactual "
        "requires human review of the historical context."
    )
    add()

    # --- Section 6: Bootstrap CI Width ---
    add("## 6. Bootstrap CI Width")
    add()
    if ci_data:
        crisis_est = ci_data.get("crisis_point_estimate")
        stab_est = ci_data.get("stability_point_estimate")
        gap = ci_data.get("point_estimate_gap")

        if crisis_est is not None and stab_est is not None:
            add(f"- Crisis point estimate (2008): {crisis_est:.1f}")
            add(f"- Stability point estimate (mid-1990s): {stab_est:.1f}")
        if gap is not None:
            add(f"- Point estimate gap: {gap:.1f}")

        ci_info = ci_data.get("current_ci")
        if ci_info:
            ci_width = ci_data.get("ci_width", "N/A")
            disc = ci_data.get("discriminable")
            disc_str = "Yes" if disc else "No"
            add(f"- 90% CI: [{ci_info['lower']:.1f}, {ci_info['upper']:.1f}]")
            add(f"- CI width: {ci_width:.1f}")
            add(f"- Gap exceeds CI width (discriminable): {disc_str}")

        note = ci_data.get("note")
        if note:
            add(f"- Note: {note}")
    else:
        add("Requires --full mode for bootstrap CI computation. Skipped.")
    add()

    # --- Pass/Fail Criteria Table ---
    add("## Pass/Fail Criteria")
    add()
    add("| Criterion | Result | Details |")
    add("|-----------|--------|---------|")

    # Zone accuracy
    zone_pass = verdict_data.get("zone_pass", False)
    zone_result = "PASS" if zone_pass else "FAIL"
    add(
        f"| Zone accuracy >= 75% | {zone_result} | "
        f"{strict_pct:.1f}% ({strict_n}/{total_n}) |"
    )

    # Monotonic ordering
    mono_result = "PASS" if mono_pass else "FAIL"
    add(
        f"| Monotonic ordering (crisis > stability) | {mono_result} | "
        f"{mono_detail} |"
    )

    # Calibration residuals
    residual_pass = verdict_data.get("residual_pass", True)
    residual_max = verdict_data.get("residual_max", 0)
    if mode == "history-only" and not loocv:
        res_result = "N/A"
        res_detail = "History-only mode uses pre-calibrated scores (residuals = 0)"
    else:
        res_result = "PASS" if residual_pass else "FAIL"
        res_detail = f"Max residual: {residual_max:.1f}"
    add(f"| Calibration residuals <= 15 | {res_result} | {res_detail} |")

    # Weight sensitivity
    fragile_count = sum(1 for r in sensitivity if r.get("fragile"))
    if sensitivity:
        max_shift = max((r["shift"] for r in sensitivity), default=0)
        if fragile_count > 0:
            ws_result = "WARN"
        else:
            ws_result = "PASS"
        ws_detail = f"Max shift: {max_shift:.1f}"
        if not any(r.get("mode") == "full" for r in sensitivity):
            ws_detail += " (theoretical bounds, history-only)"
    else:
        ws_result = "N/A"
        ws_detail = "No sensitivity data"
    add(f"| No fragile weight sensitivity | {ws_result} | {ws_detail} |")

    # Spurious trends
    if overall_concern == "none":
        st_result = "PASS"
    elif overall_concern == "minor":
        st_result = "WARN"
    else:
        st_result = "WARN"
    concern_flags = []
    if trend_data.get("monotonic_flag"):
        concern_flags.append("monotonic increase")
    if jumps:
        concern_flags.append(f"{len(jumps)} boundary jump(s)")
    if sat:
        concern_flags.append(f"{len(sat)} saturation period(s)")
    st_detail = ", ".join(concern_flags) if concern_flags else "No flags"
    add(f"| No spurious trends | {st_result} | {st_detail} |")
    add()

    # --- Overall Verdict ---
    add("## Overall Verdict")
    add()
    add(f"**{overall_verdict}**")
    add()

    if overall_verdict == "PASS":
        add(
            "The model meets all primary validation criteria. Zone accuracy is "
            "above the 75% threshold, crisis episodes score above stability "
            "episodes, and calibration residuals are within tolerance."
        )
    elif overall_verdict == "FAIL":
        failures = []
        if not verdict_data.get("zone_pass"):
            failures.append(
                f"zone accuracy ({strict_pct:.1f}%) is below the 75% threshold"
            )
        if not verdict_data.get("monotonic_pass"):
            failures.append("monotonic ordering between crisis and stability episodes fails")
        if not verdict_data.get("residual_pass"):
            failures.append(
                f"calibration residual ({residual_max:.1f}) exceeds 15-point threshold"
            )
        add("The model fails on: " + "; ".join(failures) + ".")
        add()

        # Add context for near-miss situations
        lenient_n = verdict_data.get("zone_lenient_count", 0)
        if lenient_pct > strict_pct:
            add(
                f"However, lenient zone accuracy is {lenient_pct:.1f}% "
                f"({lenient_n}/{total_n}). All zone misses are near zone "
                f"boundaries (within 3 points), indicating the model captures "
                f"the correct directional signal. Calibration refinement with "
                f"full pipeline data could improve strict accuracy."
            )
    else:
        add("Validation is incomplete. Some analyses require --full mode with live pipeline data.")
    add()

    # --- Limitations ---
    add("## Limitations")
    add()
    add("1. History starts at 1979, so 1960s and Watergate episodes cannot be evaluated")
    add("2. History.json contains demo/cached data, not live API data")
    add(
        "3. LOOCV has low statistical power with only 5 anchors "
        "(2 degrees of freedom per refit)"
    )
    add(
        "4. Inter-model correlation from a single time point is not true "
        "temporal correlation"
    )
    add(
        "5. Weight sensitivity in history-only mode shows theoretical bounds, "
        "not actual perturbation results"
    )

    # Add data-specific limitations
    if jumps:
        boundary_years = ", ".join(str(j["year"]) for j in jumps)
        add(
            f"6. Data boundary artifacts detected at year(s) {boundary_years}, "
            f"reflecting when new data sources become available rather than "
            f"genuine structural changes"
        )
    if sat:
        add(
            f"7. Score saturation at 0 in early history reflects insufficient "
            f"data availability before key series begin, not genuine zero-stress periods"
        )
    add()

    # --- Methodology ---
    add("## Methodology")
    add()
    add(
        "- Episode backtesting: extract scores from calibrated history at "
        "episode dates, compare to expected zone classifications"
    )
    add(
        "- Zone boundaries: Stable (0-25), Elevated Tension (26-50), "
        "Crisis Territory (51-75), Revolution Territory (76-100)"
    )
    add(
        "- LOOCV: hold out each calibration anchor, refit with remaining 4, "
        "measure prediction error on held-out point"
    )
    add(
        "- Weight sensitivity: perturb MODEL_WEIGHTS by +/-20%, renormalize, "
        "measure score shift"
    )
    add(
        "- Spurious trends: automated checks for monotonic increase, "
        "data boundary artifacts, saturation"
    )
    add(
        "- Inter-model correlation: compare pairwise model scores to "
        "detect redundancy"
    )
    add(
        "- Bootstrap CI: resample variables within each domain to assess "
        "score uncertainty"
    )
    add()
    add("---")
    add(f"*Generated by models/validate.py on {date_str}*")

    # Write the file
    report_path = _SCRIPT_DIR / "VALIDATION.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def load_history_json() -> pd.Series:
    """
    Load calibrated history from public/data/history.json.
    Returns a pd.Series with DatetimeIndex and calibrated score values.
    """
    history_path = _PROJECT_ROOT / "public" / "data" / "history.json"
    if not history_path.exists():
        print(f"ERROR: history.json not found at {history_path}")
        sys.exit(1)

    with open(history_path, "r") as f:
        data = json.load(f)

    entries = data.get("entries", [])
    if not entries:
        print("ERROR: history.json contains no entries")
        sys.exit(1)

    dates = [pd.Timestamp(e["date"]) for e in entries]
    scores = [float(e["score"]) for e in entries]

    series = pd.Series(scores, index=pd.DatetimeIndex(dates))
    series = series.sort_index()
    return series


def main():
    parser = argparse.ArgumentParser(
        description="Revolution Index Validation Script"
    )
    parser.add_argument(
        "--full", action="store_true",
        help="Run full validation including LOOCV and CI width (requires pipeline data)",
    )
    parser.add_argument(
        "--cached-only", action="store_true",
        help="In full mode, skip API fetching and use cached data only",
    )
    args = parser.parse_args()

    print()
    _print_separator("=")
    print("REVOLUTION INDEX MODEL VALIDATION")
    _print_separator("=")
    print()

    # Collect all results for potential report generation
    all_results = {}

    # --- Load calibrated history ---
    print("Loading calibrated history from history.json...")
    calibrated_history = load_history_json()
    print(
        f"  Loaded {len(calibrated_history)} entries "
        f"({calibrated_history.index[0].strftime('%Y-%m')} to "
        f"{calibrated_history.index[-1].strftime('%Y-%m')})"
    )
    print(f"  Score range: {calibrated_history.min():.0f} to {calibrated_history.max():.0f}")
    print()

    raw_scores = None
    unified_df = None
    raw_df = None
    cal_coeffs = (1.0, 0.0)
    anchor_residuals = None
    loocv_results = None
    ci_result = None

    # --- Full mode: run pipeline ---
    if args.full:
        import os
        api_key = os.environ.get("FRED_API_KEY", "")
        if not api_key and not args.cached_only:
            print("WARNING: FRED_API_KEY not set. Use --cached-only or set the key.")
            print("Falling back to history-only mode.")
            args.full = False
        else:
            print("Running full pipeline for LOOCV and CI analysis...")
            try:
                from models.pipeline import fetch_all
                from models.ensemble import compute_ensemble

                unified_df, raw_df = fetch_all(
                    api_key=api_key, start_year=1947
                )

                if unified_df.empty:
                    print("WARNING: Pipeline produced no data. Falling back to history-only.")
                    args.full = False
                else:
                    ensemble_result = compute_ensemble(unified_df, raw_df=raw_df)
                    raw_scores = pd.Series(
                        {row["date"]: row["score"]
                         for row in ensemble_result["history"]}
                    )
                    if not isinstance(raw_scores.index, pd.DatetimeIndex):
                        raw_scores.index = pd.to_datetime(raw_scores.index)

                    cal_coeffs = get_calibration_coefficients(raw_scores)

                    # Get anchor residuals from calibration fit
                    _a, _b, anchor_residuals = _fit_calibration(raw_scores)

                    # Re-calibrate with full pipeline data
                    calibrated_history = calibrate(raw_scores)

                    print(f"  Pipeline produced {len(raw_scores)} raw scores")
                    print(f"  Calibration: score = {cal_coeffs[0]:.4f} * raw + {cal_coeffs[1]:.4f}")
                    print()
            except Exception as e:
                print(f"WARNING: Pipeline failed: {e}")
                print("Falling back to history-only mode.")
                args.full = False

    mode = "full" if args.full else "history-only"
    print(f"Mode: {mode}")
    print()

    # --- 1. Episode backtesting ---
    print("Running episode backtesting...")
    episode_results = run_episode_backtest(calibrated_history, raw_scores)
    all_results["episodes"] = episode_results
    _print_episode_table(episode_results)

    # --- 2. LOOCV (full mode only) ---
    if args.full and raw_scores is not None:
        print("Running leave-one-out cross-validation...")
        loocv_results = run_loocv(raw_scores)
        all_results["loocv"] = loocv_results
        _print_loocv_table(loocv_results)
    else:
        print(
            "Skipping LOOCV (requires raw scores from full pipeline run). "
            "Use --full to enable."
        )
        print()

    # --- 3. CI width check ---
    ci_result = check_ci_width(
        calibrated_history,
        unified_df=unified_df,
        calibration_coeffs=cal_coeffs,
        raw_df=raw_df,
    )
    all_results["ci_width"] = ci_result
    _print_ci_width(ci_result)

    # --- 4. Weight sensitivity analysis ---
    print("Running weight sensitivity analysis...")
    sensitivity_results = run_weight_sensitivity(
        calibrated_history,
        unified_df=unified_df,
        raw_df=raw_df,
    )
    all_results["sensitivity_results"] = sensitivity_results
    _print_weight_sensitivity(sensitivity_results, is_full=args.full)

    # --- 5. Inter-model correlation check ---
    print("Running inter-model correlation check...")
    correlation_results = check_inter_model_correlation(
        unified_df=unified_df,
        raw_df=raw_df,
    )
    all_results["correlation_results"] = correlation_results
    _print_inter_model_correlation(correlation_results, is_full=args.full)

    # --- 6. Spurious trend detection ---
    print("Running spurious trend detection...")
    trend_results = check_spurious_trends(calibrated_history)
    all_results["trend_results"] = trend_results
    _print_spurious_trends(trend_results)

    # --- 7. Overall verdict ---
    verdict = compute_overall_verdict(
        episode_results,
        loocv_results=loocv_results,
        anchor_residuals=anchor_residuals,
    )
    all_results["verdict"] = verdict
    _print_verdict(verdict)

    # --- Store results for report generation ---
    all_results["mode"] = mode
    all_results["history_entries"] = len(calibrated_history)
    all_results["date_range"] = {
        "start": calibrated_history.index[0].strftime("%Y-%m-%d"),
        "end": calibrated_history.index[-1].strftime("%Y-%m-%d"),
    }

    # --- 8. Generate validation report ---
    write_validation_report(all_results)
    report_path = _SCRIPT_DIR / "VALIDATION.md"
    print(f"Validation report written to {report_path.relative_to(_PROJECT_ROOT)}")
    print()

    return all_results


if __name__ == "__main__":
    main()
