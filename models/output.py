"""
JSON output generation for the Astro frontend.
Produces current.json, history.json, and factors.json matching
src/lib/data.ts interfaces exactly.
"""
import json
from datetime import datetime, timezone
from pathlib import Path

from models.config import DOMAIN_WEIGHTS, Domain


OUTPUT_DIR = Path(__file__).resolve().parent.parent / "public" / "data"

# Domain display names and descriptions
DOMAIN_META = {
    "economic_stress": {
        "name": "Economic Stress",
        "description": (
            "Measures economic pressures that academic research links to "
            "political instability, including wage stagnation, inequality, "
            "unemployment, inflation, housing costs, and financial system stress."
        ),
    },
    "political_polarization": {
        "name": "Political Polarization",
        "description": (
            "Tracks partisan division at both elite (congressional voting) "
            "and mass (public attitudes) levels, including affective "
            "polarization and anti-system sentiment."
        ),
    },
    "institutional_quality": {
        "name": "Institutional Quality",
        "description": (
            "Monitors the health of democratic institutions including judicial "
            "independence, legislative constraints on executive power, electoral "
            "integrity, and freedom of expression."
        ),
    },
    "social_mobilization": {
        "name": "Social Mobilization",
        "description": (
            "Measures collective action capacity and social trust, including "
            "protest activity, organizational density, government trust, and "
            "democratic commitment."
        ),
    },
    "information_media": {
        "name": "Information & Media",
        "description": (
            "Tracks media trust levels and partisan media consumption gaps "
            "that academic research associates with democratic resilience."
        ),
    },
}


def write_current_json(
    composite_score: int,
    zone: str,
    domain_scores: dict,
    domain_directions: dict,
    domain_weights: dict,
    timestamp: str,
    bootstrap_ci: dict = None,
) -> None:
    """
    Write public/data/current.json matching CurrentData interface.

    Factor array is ordered highest-weight-first.
    All weights must sum to 1.0.

    Parameters
    ----------
    composite_score : int
        Composite score 0-100.
    zone : str
        Zone label (one of the four ZoneLabel values).
    domain_scores : dict
        Domain ID -> current score (0.0-1.0).
    domain_directions : dict
        Domain ID -> direction ("up", "down", "neutral").
    domain_weights : dict
        Domain ID -> weight (0.0-1.0). Must sum to 1.0.
    timestamp : str
        ISO 8601 timestamp with timezone.
    bootstrap_ci : dict, optional
        Bootstrap confidence interval dict (ci_lower, ci_upper, etc.).
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Build factors array
    factors = []
    for domain_id in domain_scores:
        meta = DOMAIN_META.get(domain_id, {})
        factors.append({
            "id": domain_id,
            "name": meta.get("name", domain_id),
            "value": round(float(domain_scores.get(domain_id, 0.5)), 4),
            "direction": domain_directions.get(domain_id, "neutral"),
            "weight": float(domain_weights.get(domain_id, 0.0)),
        })

    # Sort by weight descending
    factors.sort(key=lambda f: f["weight"], reverse=True)

    # Verify weights sum to 1.0
    weight_sum = sum(f["weight"] for f in factors)
    if abs(weight_sum - 1.0) > 0.01:
        # Normalize weights to sum to exactly 1.0
        for f in factors:
            f["weight"] = round(f["weight"] / weight_sum, 4)
        # Fix rounding to ensure exact 1.0 sum
        remainder = 1.0 - sum(f["weight"] for f in factors)
        factors[0]["weight"] = round(factors[0]["weight"] + remainder, 4)

    data = {
        "_schema": "src/lib/data.ts#CurrentData",
        "score": int(composite_score),
        "timestamp": timestamp,
        "zone": zone,
        "factors": factors,
    }

    # Add bootstrap CI as metadata if available
    if bootstrap_ci:
        data["_bootstrap_ci"] = {
            "lower": round(bootstrap_ci["ci_lower"], 1),
            "upper": round(bootstrap_ci["ci_upper"], 1),
            "width": bootstrap_ci["ci_width"],
            "n": bootstrap_ci["n_bootstrap"],
        }

    output_path = OUTPUT_DIR / "current.json"
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"  Wrote {output_path} (score={composite_score}, zone={zone})")


def write_history_json(history: list[dict]) -> None:
    """
    Write public/data/history.json matching HistoryData interface.

    Parameters
    ----------
    history : list of dict
        Each dict has "date" (ISO 8601 date only) and "score" (int 0-100).
        Must be ascending chronological order.
        Must contain at least 12 entries.
        Score variation must be at least 10 points across series.
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Validate minimum entries
    if len(history) < 12:
        raise ValueError(
            f"history.json requires at least 12 entries, got {len(history)}"
        )

    # Ensure ascending chronological order
    history = sorted(history, key=lambda e: e["date"])

    # Ensure scores are integers in 0-100 range
    entries = []
    for entry in history:
        score = int(round(max(0, min(100, entry["score"]))))
        # Ensure date has no time component
        date_str = entry["date"][:10]
        entries.append({
            "date": date_str,
            "score": score,
        })

    # Validate score variation
    scores = [e["score"] for e in entries]
    score_range = max(scores) - min(scores)
    if score_range < 10:
        raise ValueError(
            f"history.json requires at least 10 points of score variation, "
            f"got range of {score_range} (min={min(scores)}, max={max(scores)})"
        )

    data = {
        "_schema": "src/lib/data.ts#HistoryData",
        "entries": entries,
    }

    output_path = OUTPUT_DIR / "history.json"
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"  Wrote {output_path} ({len(entries)} entries, "
          f"{entries[0]['date']} to {entries[-1]['date']})")


def write_factors_json(
    domain_scores: dict,
    domain_history: dict,
) -> None:
    """
    Write public/data/factors.json matching FactorsData interface.

    Parameters
    ----------
    domain_scores : dict
        Domain ID -> current value (0.0-1.0).
    domain_history : dict
        Domain ID -> list of {"date": str, "value": float}.
        At least 3 entries per domain per data.ts requirement.
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    factors = []
    for domain_id in domain_scores:
        meta = DOMAIN_META.get(domain_id, {})
        current_value = round(float(domain_scores.get(domain_id, 0.5)), 4)
        history = domain_history.get(domain_id, [])

        # Ensure at least 3 historical entries
        if len(history) < 3:
            # Pad with current value if insufficient history
            while len(history) < 3:
                history.append({
                    "date": "2024-01-01",
                    "value": current_value,
                })

        # Sort ascending chronological and format
        history = sorted(history, key=lambda e: e["date"])
        formatted_history = [
            {
                "date": entry["date"][:10],
                "value": round(float(max(0.0, min(1.0, entry["value"]))), 4),
            }
            for entry in history
        ]

        factors.append({
            "id": domain_id,
            "name": meta.get("name", domain_id),
            "description": meta.get("description", ""),
            "current_value": current_value,
            "historical": formatted_history,
        })

    data = {
        "_schema": "src/lib/data.ts#FactorsData",
        "factors": factors,
    }

    output_path = OUTPUT_DIR / "factors.json"
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"  Wrote {output_path} ({len(factors)} factors)")
