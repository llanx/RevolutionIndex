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
from typing import Optional

import pandas as pd

from models.models import ModelOutput, MODEL_REGISTRY
from models.config import (
    MODEL_WEIGHTS,
    DOMAIN_WEIGHTS,
    Domain,
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


def compute_ensemble(
    unified_df: pd.DataFrame,
    raw_df: Optional[pd.DataFrame] = None,
) -> dict:
    """
    Run all registered models and combine their outputs.

    Parameters
    ----------
    unified_df : pd.DataFrame
        Unified DataFrame from pipeline.fetch_all() with columns named
        by catalog number (string) and values in 0.0-1.0 stress range.
    raw_df : pd.DataFrame, optional
        Pre-normalized raw aligned data. Passed to models that need
        original values (e.g., V-Dem rate-of-change computation).

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
    raw_model_df = _rename_columns_for_models(raw_df) if raw_df is not None else None

    # --- Run all registered models ---
    model_outputs: dict[str, ModelOutput] = {}
    for model_id, model_fn in MODEL_REGISTRY.items():
        try:
            output = model_fn(model_df, raw_df=raw_model_df)
            model_outputs[model_id] = output
        except TypeError:
            # Model doesn't accept raw_df kwarg, call without it
            try:
                output = model_fn(model_df)
                model_outputs[model_id] = output
            except Exception as e:
                print(f"  WARNING: Model '{model_id}' failed: {e}")
                continue
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
    history = _build_raw_history(unified_df, domain_scores_df, raw_df=raw_df)

    # Compute effective weights (after renormalization for any failed models)
    effective_weights = {}
    if model_outputs:
        total_w = sum(MODEL_WEIGHTS.get(mid, 0.0) for mid in model_outputs)
        if total_w > 0:
            for mid in model_outputs:
                effective_weights[mid] = MODEL_WEIGHTS.get(mid, 0.0) / total_w

    return {
        "composite_score": composite_score,
        "model_outputs": model_outputs,
        "domain_scores": current_domain_scores,
        "factor_directions": factor_directions,
        "history": history,
        "models_expected": list(MODEL_REGISTRY.keys()),
        "effective_weights": effective_weights,
    }


def _run_models_on_slice(
    model_df_slice: pd.DataFrame,
    raw_df_slice: Optional[pd.DataFrame] = None,
) -> Optional[float]:
    """
    Run all registered models on a DataFrame slice and combine with MODEL_WEIGHTS.

    Returns the uncalibrated composite score (0-100), or None if no models succeed.
    """
    model_outputs = {}
    for model_id, model_fn in MODEL_REGISTRY.items():
        try:
            output = model_fn(model_df_slice, raw_df=raw_df_slice)
            model_outputs[model_id] = output
        except TypeError:
            try:
                output = model_fn(model_df_slice)
                model_outputs[model_id] = output
            except Exception:
                continue
        except Exception:
            continue

    if not model_outputs:
        return None

    weighted_sum = 0.0
    total_weight = 0.0
    for model_id, output in model_outputs.items():
        weight = MODEL_WEIGHTS.get(model_id, 0.0)
        weighted_sum += output.score * weight
        total_weight += weight

    if total_weight <= 0:
        return None

    return weighted_sum / total_weight


def _build_raw_history(
    unified_df: pd.DataFrame,
    domain_scores_df: pd.DataFrame,
    raw_df: Optional[pd.DataFrame] = None,
) -> list[dict]:
    """
    Build historical time series of composite scores using the same
    5-model ensemble used for the current score.

    For each time point, slices unified_df up to that date, runs all 5
    model functions on the slice, and combines with MODEL_WEIGHTS. This
    ensures history, bootstrap CI, and current score all use identical
    methodology.

    Performance optimization: pre-2000 uses quarterly sampling (Jan, Apr,
    Jul, Oct), post-2000 uses monthly. The domain_scores_df index is used
    only to determine which dates to evaluate.
    """
    _ensure_models_registered()

    # Rename columns once for model consumption
    model_df = _rename_columns_for_models(unified_df)
    raw_model_df = _rename_columns_for_models(raw_df) if raw_df is not None else None

    history = []
    dates = domain_scores_df.index

    for date_idx in dates:
        year = date_idx.year
        month = date_idx.month

        # Pre-2000: quarterly only (performance optimization)
        if year < 2000 and month not in (1, 4, 7, 10):
            continue

        # Slice up to this date (inclusive)
        slice_df = model_df.loc[:date_idx]
        if slice_df.empty:
            continue

        # Need at least some data columns with values
        non_null_cols = slice_df.iloc[-1].dropna()
        if len(non_null_cols) < 2:
            continue

        raw_slice = raw_model_df.loc[:date_idx] if raw_model_df is not None else None
        composite = _run_models_on_slice(slice_df, raw_df_slice=raw_slice)
        if composite is not None:
            history.append({
                "date": date_idx.strftime("%Y-%m-%d"),
                "score": composite,
            })

    return history
