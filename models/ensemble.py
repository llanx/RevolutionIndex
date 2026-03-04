"""
Ensemble scoring: combine 5 model outputs into a single composite score
using evidence-weighted average.

Weight rationale (from models/README.md):
- PSI 0.25: Strong evidence, longest validation history (Turchin 2003-2023)
- PLI 0.20: Well-validated prospect theory framework for economic stress
- FSP 0.15: Narrower scope (financial crises only) but strongest empirical mechanism (Funke et al. 2016)
- Georgescu SDT 0.25: Most directly applicable to developed democracies (Georgescu 2023)
- V-Dem ERT 0.15: Primarily diagnostic (not predictive), but covers institutional dimension no other model captures
"""
import pandas as pd
import numpy as np
from datetime import datetime, timezone

from models.models import ModelOutput, MODEL_REGISTRY
from models.config import (
    MODEL_WEIGHTS,
    DOMAIN_WEIGHTS,
    Domain,
    VARIABLES,
    EVIDENCE_WEIGHTS,
    get_variables_by_domain,
)
from models.pipeline import compute_domain_scores


def _ensure_models_registered() -> None:
    """Import all model modules to trigger @register_model decorators."""
    import models.model_psi       # noqa: F401
    import models.model_pli       # noqa: F401
    import models.model_fsp       # noqa: F401
    import models.model_georgescu  # noqa: F401
    import models.model_vdem      # noqa: F401


def _rename_columns_for_models(unified_df: pd.DataFrame) -> pd.DataFrame:
    """
    Rename pipeline columns from catalog number strings (e.g., '9')
    to the format expected by model functions (e.g., 'var_9').

    The pipeline produces columns named by catalog number as strings,
    but model functions expect 'var_{catalog_number}' format.
    """
    rename_map = {}
    for col in unified_df.columns:
        # Only rename numeric string columns
        try:
            int(col)
            rename_map[col] = f"var_{col}"
        except ValueError:
            pass
    return unified_df.rename(columns=rename_map)


def compute_ensemble(unified_df: pd.DataFrame) -> dict:
    """
    Run all registered models and combine their outputs.

    Parameters
    ----------
    unified_df : pd.DataFrame
        Unified DataFrame from pipeline.fetch_all() with columns named
        by catalog number (string) and values in 0.0-1.0 stress range.

    Returns
    -------
    dict with:
    - "composite_score": float (0-100, uncalibrated)
    - "model_outputs": dict[str, ModelOutput]
    - "domain_scores": dict[str, float] (0.0-1.0 per domain)
    - "factor_directions": dict[str, str] (domain_id -> "up"/"down"/"neutral")
    - "history": list[dict] with date and score for each time point
    """
    _ensure_models_registered()

    # Rename columns for model consumption
    model_df = _rename_columns_for_models(unified_df)

    # --- Run all registered models ---
    model_outputs: dict[str, ModelOutput] = {}
    for model_id, model_fn in MODEL_REGISTRY.items():
        try:
            output = model_fn(model_df)
            model_outputs[model_id] = output
        except Exception as e:
            print(f"  WARNING: Model '{model_id}' failed: {e}")
            continue

    # --- Compute evidence-weighted ensemble composite ---
    if not model_outputs:
        composite_score = 0.0
    else:
        weighted_sum = 0.0
        total_weight = 0.0
        for model_id, output in model_outputs.items():
            weight = MODEL_WEIGHTS.get(model_id, 0.0)
            weighted_sum += output.score * weight
            total_weight += weight
        composite_score = weighted_sum / total_weight if total_weight > 0 else 0.0

    # --- Compute domain-level scores ---
    domain_scores_df = compute_domain_scores(unified_df)
    current_domain_scores = {}
    for domain in Domain:
        domain_id = domain.value
        if domain_id in domain_scores_df.columns:
            valid = domain_scores_df[domain_id].dropna()
            if not valid.empty:
                current_domain_scores[domain_id] = float(valid.iloc[-1])
            else:
                current_domain_scores[domain_id] = 0.5
        else:
            current_domain_scores[domain_id] = 0.5

    # --- Determine factor directions ---
    # Compare current domain score to 12-month-ago score
    factor_directions = {}
    for domain in Domain:
        domain_id = domain.value
        if domain_id not in domain_scores_df.columns:
            factor_directions[domain_id] = "neutral"
            continue

        valid = domain_scores_df[domain_id].dropna()
        if len(valid) < 13:
            factor_directions[domain_id] = "neutral"
            continue

        current = float(valid.iloc[-1])
        past = float(valid.iloc[-13])

        if current > past + 0.02:
            factor_directions[domain_id] = "up"
        elif current < past - 0.02:
            factor_directions[domain_id] = "down"
        else:
            factor_directions[domain_id] = "neutral"

    # --- Build historical time series ---
    history = _build_raw_history(unified_df, domain_scores_df)

    return {
        "composite_score": composite_score,
        "model_outputs": model_outputs,
        "domain_scores": current_domain_scores,
        "factor_directions": factor_directions,
        "history": history,
    }


def _build_raw_history(
    unified_df: pd.DataFrame,
    domain_scores_df: pd.DataFrame,
) -> list[dict]:
    """
    Build historical time series of composite scores.

    For each month in the domain_scores DataFrame, compute the weighted
    composite score using DOMAIN_WEIGHTS. This is the uncalibrated raw
    history that will be calibrated later by calibrate.py.

    For months where some domains lack data, compute from available
    domains only (exclude missing, don't treat as zero).

    Minimum coverage: at least 2 domains must have valid data for a month
    to be included. This prevents misleading near-zero scores for early
    years (pre-1979) when most variables lack data coverage.
    """
    MIN_DOMAINS_REQUIRED = 2  # At least 2 of 5 domains must have data

    history = []

    for date_idx in domain_scores_df.index:
        row = domain_scores_df.loc[date_idx]
        weighted_sum = 0.0
        total_weight = 0.0
        valid_domain_count = 0

        for domain in Domain:
            domain_id = domain.value
            if domain_id in row.index and not pd.isna(row[domain_id]):
                weight = DOMAIN_WEIGHTS[domain]
                weighted_sum += float(row[domain_id]) * weight
                total_weight += weight
                valid_domain_count += 1

        if total_weight > 0 and valid_domain_count >= MIN_DOMAINS_REQUIRED:
            # Scale domain scores (0.0-1.0) to composite (0-100)
            composite = (weighted_sum / total_weight) * 100.0
            date_str = date_idx.strftime("%Y-%m-%d")
            history.append({
                "date": date_str,
                "score": composite,
            })

    return history
