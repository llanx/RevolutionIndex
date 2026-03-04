"""
End-to-end pipeline: fetch data -> normalize -> run models -> ensemble -> calibrate -> write JSON.

Usage:
    python models/run.py                    # full pipeline (fetches data)
    python models/run.py --cached-only      # skip API fetch, use cached data only
    python models/run.py --dry-run          # compute scores but don't write JSON

Requires FRED_API_KEY environment variable (free key from https://fred.stlouisfed.org/docs/api/api_key.html)

Run from the project root directory:
    cd /path/to/RevolutionIndex
    python models/run.py
"""
import argparse
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# Ensure both project root and models/ are on sys.path for imports
_SCRIPT_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _SCRIPT_DIR.parent

if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import pandas as pd


def main():
    parser = argparse.ArgumentParser(description="Revolution Index Pipeline")
    parser.add_argument(
        "--cached-only", action="store_true",
        help="Skip API fetching, use cached data only",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Compute scores but don't write JSON output",
    )
    args = parser.parse_args()

    print("=" * 70)
    print("Revolution Index Pipeline")
    print("=" * 70)
    print()

    # 1. Get FRED API key
    api_key = os.environ.get("FRED_API_KEY", "")
    if not api_key and not args.cached_only:
        print("ERROR: FRED_API_KEY environment variable not set.")
        print("Get a free key at: https://fred.stlouisfed.org/docs/api/api_key.html")
        print()
        print("Options:")
        print("  export FRED_API_KEY=your_key_here  # then re-run")
        print("  python models/run.py --cached-only  # use cached data")
        sys.exit(1)

    # 2. Fetch and prepare data
    from models.pipeline import fetch_all, compute_domain_scores
    print("Phase 1: Fetching data...")
    unified_df = fetch_all(api_key=api_key, start_year=1947)

    if unified_df.empty:
        print("\nERROR: Pipeline produced no data. Check errors above.")
        sys.exit(1)

    print(f"\nPhase 2: Computing domain scores...")
    domain_scores_df = compute_domain_scores(unified_df)
    print(f"  Domain scores: {domain_scores_df.shape[0]} months x "
          f"{domain_scores_df.shape[1]} domains")

    # 3. Run all models via ensemble
    print(f"\nPhase 3: Running ensemble models...")
    from models.ensemble import compute_ensemble
    ensemble_result = compute_ensemble(unified_df)

    print(f"  Composite (uncalibrated): {ensemble_result['composite_score']:.1f}")
    print(f"  Models: {', '.join(ensemble_result['model_outputs'].keys())}")

    # 4. Calibrate scores
    print(f"\nPhase 4: Calibrating scores...")
    from models.calibrate import calibrate, compute_bootstrap_ci, score_to_zone

    raw_history = pd.Series(
        {row["date"]: row["score"] for row in ensemble_result["history"]}
    )
    calibrated_history = calibrate(raw_history)

    print(f"  Raw range: {raw_history.min():.1f} - {raw_history.max():.1f}")
    print(f"  Calibrated range: {calibrated_history.min():.1f} - "
          f"{calibrated_history.max():.1f}")

    # 5. Compute bootstrap CI for current score
    print(f"\nPhase 5: Computing bootstrap confidence intervals...")
    bootstrap_ci = compute_bootstrap_ci(unified_df)

    # 6. Determine current values
    current_score = int(round(float(calibrated_history.iloc[-1])))
    current_score = max(0, min(100, current_score))
    current_zone = score_to_zone(current_score)
    timestamp = datetime.now(timezone.utc).isoformat()

    # 7. Print summary
    print()
    print("=" * 70)
    print("Pipeline Results")
    print("=" * 70)
    print(f"  Composite Score: {current_score}")
    print(f"  Zone: {current_zone}")
    print(f"  Bootstrap 90% CI: "
          f"[{bootstrap_ci['ci_lower']:.1f}, {bootstrap_ci['ci_upper']:.1f}]")
    print(f"  Models run: {len(ensemble_result['model_outputs'])}")
    print()
    print("  Domain scores:")
    for domain_id, score in ensemble_result["domain_scores"].items():
        direction = ensemble_result["factor_directions"].get(domain_id, "neutral")
        arrow = {"up": "^", "down": "v", "neutral": "="}[direction]
        print(f"    {domain_id}: {score:.3f} [{arrow}]")
    print()
    print("  Model sub-scores:")
    for model_id, output in ensemble_result["model_outputs"].items():
        from models.config import MODEL_WEIGHTS
        weight = MODEL_WEIGHTS.get(model_id, 0.0)
        print(f"    {output.model_name} ({model_id}): "
              f"{output.score:.1f} (weight={weight})")

    # 8. Write JSON output
    if not args.dry_run:
        print(f"\nPhase 6: Writing JSON output...")
        from models.output import (
            write_current_json,
            write_history_json,
            write_factors_json,
        )
        from models.config import DOMAIN_WEIGHTS as DW, Domain

        # Build domain weights dict with string keys
        domain_weights = {d.value: w for d, w in DW.items()}

        write_current_json(
            composite_score=current_score,
            zone=current_zone,
            domain_scores=ensemble_result["domain_scores"],
            domain_directions=ensemble_result["factor_directions"],
            domain_weights=domain_weights,
            timestamp=timestamp,
            bootstrap_ci=bootstrap_ci,
        )

        # Build history for JSON (sample annually pre-2000, quarterly post-2000)
        history_entries = build_history_entries(calibrated_history)
        write_history_json(history_entries)

        # Build factor history for sparklines
        write_factors_json(
            domain_scores=ensemble_result["domain_scores"],
            domain_history=build_domain_history(domain_scores_df),
        )

        print(f"\n  JSON files written to public/data/")
    else:
        print(f"\n  --dry-run: JSON output not written.")

    # Data freshness summary
    from models.pipeline import get_freshness
    freshness = get_freshness()
    print(f"\n  Data freshness: {len(freshness)} sources tracked")
    print()
    print("Pipeline complete.")


def build_history_entries(calibrated: pd.Series) -> list[dict]:
    """
    Sample history at appropriate frequency:
    - Annual (January) for pre-2000
    - Quarterly (Jan, Apr, Jul, Oct) for post-2000
    Keep file size manageable while providing sufficient resolution.

    Parameters
    ----------
    calibrated : pd.Series
        Calibrated composite scores with DatetimeIndex or date string index.

    Returns
    -------
    list[dict]
        List of {"date": "YYYY-MM-DD", "score": int} entries.
    """
    if calibrated.empty:
        return []

    # Ensure DatetimeIndex
    if not isinstance(calibrated.index, pd.DatetimeIndex):
        calibrated = calibrated.copy()
        calibrated.index = pd.to_datetime(calibrated.index)

    entries = []
    for date_idx, score in calibrated.items():
        year = date_idx.year
        month = date_idx.month

        # Pre-2000: annual (January only)
        if year < 2000:
            if month == 1:
                entries.append({
                    "date": date_idx.strftime("%Y-%m-%d"),
                    "score": int(round(max(0, min(100, float(score))))),
                })
        else:
            # Post-2000: quarterly (Jan, Apr, Jul, Oct)
            if month in (1, 4, 7, 10):
                entries.append({
                    "date": date_idx.strftime("%Y-%m-%d"),
                    "score": int(round(max(0, min(100, float(score))))),
                })

    # Always include the latest entry if not already included
    last_date = calibrated.index[-1]
    if entries and entries[-1]["date"] != last_date.strftime("%Y-%m-%d"):
        entries.append({
            "date": last_date.strftime("%Y-%m-%d"),
            "score": int(round(max(0, min(100, float(calibrated.iloc[-1]))))),
        })

    return entries


def build_domain_history(domain_scores_df: pd.DataFrame) -> dict:
    """
    Build domain-level historical entries for factors.json sparklines.
    Last 10 years, annual frequency (at least 3 entries per data.ts requirement).

    Parameters
    ----------
    domain_scores_df : pd.DataFrame
        DataFrame with domain columns and DatetimeIndex.

    Returns
    -------
    dict
        Domain ID -> list of {"date": str, "value": float}.
    """
    if domain_scores_df.empty:
        return {}

    result = {}

    for col in domain_scores_df.columns:
        series = domain_scores_df[col].dropna()
        if series.empty:
            result[col] = []
            continue

        # Last 10 years, annual (January)
        cutoff = series.index.max() - pd.DateOffset(years=10)
        recent = series[series.index >= cutoff]

        entries = []
        seen_years = set()
        for date_idx, value in recent.items():
            year = date_idx.year
            month = date_idx.month

            # Take January data point for each year
            if month == 1 and year not in seen_years:
                seen_years.add(year)
                entries.append({
                    "date": date_idx.strftime("%Y-%m-%d"),
                    "value": round(float(max(0.0, min(1.0, value))), 4),
                })

        # Always include the most recent data point
        if recent.index[-1].month != 1 or recent.index[-1].year in seen_years:
            last_date = recent.index[-1]
            entries.append({
                "date": last_date.strftime("%Y-%m-%d"),
                "value": round(float(max(0.0, min(1.0, float(recent.iloc[-1])))), 4),
            })

        # Sort chronologically
        entries = sorted(entries, key=lambda e: e["date"])

        result[col] = entries

    return result


if __name__ == "__main__":
    main()
