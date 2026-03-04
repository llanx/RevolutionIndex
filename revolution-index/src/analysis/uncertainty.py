"""
Uncertainty quantification via bootstrap parameter perturbation.

Every model has tunable parameters (normalization windows, weights, K constants).
None are empirically calibrated (critical review D2). This module quantifies
how sensitive the output is to those parameter choices.

Approach: sample parameter values from plausible ranges, recompute the model
N times, and report the median + 95% confidence interval.
"""

import numpy as np
import pandas as pd

from src.models.base_model import BaseModel, ModelOutput
from src.models.turchin_psi import TurchinPSI
from src.models.prospect_theory import ProspectTheoryPLI
from src.models.financial_stress import FinancialStressPathway
from config import PSI_PARAMS, PLI_PARAMS


def bootstrap_psi(
    data: pd.DataFrame,
    date: pd.Timestamp,
    n_samples: int = 500,
) -> tuple[float, float, float]:
    """
    Bootstrap confidence interval for Turchin PSI.

    Varies: reference period start (1965-1975).
    """
    scores = []
    starts = pd.date_range(
        PSI_PARAMS["reference_start_range"][0],
        PSI_PARAMS["reference_start_range"][1],
        freq="YS",
    )

    for _ in range(n_samples):
        ref_start = str(np.random.choice(starts).date())
        model = TurchinPSI(reference_start=ref_start)
        try:
            output = model.compute(data, date)
            scores.append(output.score)
        except (KeyError, ValueError):
            continue

    if not scores:
        return 50.0, 0.0, 100.0

    return (
        float(np.percentile(scores, 50)),
        float(np.percentile(scores, 2.5)),
        float(np.percentile(scores, 97.5)),
    )


def bootstrap_pli(
    data: pd.DataFrame,
    date: pd.Timestamp,
    n_samples: int = 500,
) -> tuple[float, float, float]:
    """
    Bootstrap confidence interval for Prospect Theory PLI.

    Varies: lambda (2.0-2.5), K scale factor (0.5-2.0).
    """
    scores = []
    lambda_range = PLI_PARAMS["lambda_range"]
    k_range = PLI_PARAMS["K_scale_range"]
    base_K = PLI_PARAMS["domain_K"]

    for _ in range(n_samples):
        lambda_ = np.random.uniform(*lambda_range)
        k_scale = np.random.uniform(*k_range)
        scaled_K = {k: v * k_scale for k, v in base_K.items()}

        model = ProspectTheoryPLI(lambda_=lambda_, domain_K=scaled_K)
        try:
            output = model.compute(data, date)
            scores.append(output.score)
        except (KeyError, ValueError):
            continue

    if not scores:
        return 50.0, 0.0, 100.0

    return (
        float(np.percentile(scores, 50)),
        float(np.percentile(scores, 2.5)),
        float(np.percentile(scores, 97.5)),
    )


def bootstrap_all_models(
    data: pd.DataFrame,
    date: pd.Timestamp,
    n_samples: int = 500,
) -> dict[str, tuple[float, float, float]]:
    """
    Compute bootstrap CIs for all models at a single date.

    Returns dict of {model_name: (median, ci_lower, ci_upper)}.
    """
    results = {}

    results["turchin_psi"] = bootstrap_psi(data, date, n_samples)
    results["prospect_theory"] = bootstrap_pli(data, date, n_samples)

    # Financial stress: vary rolling window (15-25 years)
    scores = []
    for _ in range(n_samples):
        window = np.random.randint(15, 26)
        model = FinancialStressPathway(rolling_window_years=window)
        try:
            output = model.compute(data, date)
            scores.append(output.score)
        except (KeyError, ValueError):
            continue

    if scores:
        results["financial_stress"] = (
            float(np.percentile(scores, 50)),
            float(np.percentile(scores, 2.5)),
            float(np.percentile(scores, 97.5)),
        )
    else:
        results["financial_stress"] = (50.0, 0.0, 100.0)

    return results
