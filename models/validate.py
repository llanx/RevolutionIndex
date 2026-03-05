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

    # --- 4. Overall verdict ---
    verdict = compute_overall_verdict(
        episode_results,
        loocv_results=loocv_results,
        anchor_residuals=anchor_residuals,
    )
    all_results["verdict"] = verdict
    _print_verdict(verdict)

    # --- Store results for report generation (Plan 05-03) ---
    all_results["mode"] = mode
    all_results["history_entries"] = len(calibrated_history)
    all_results["date_range"] = {
        "start": calibrated_history.index[0].strftime("%Y-%m-%d"),
        "end": calibrated_history.index[-1].strftime("%Y-%m-%d"),
    }

    return all_results


if __name__ == "__main__":
    main()
