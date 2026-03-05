"""
Georgescu SDT (Structural-Demographic Theory) for Industrialized Societies.

Operationalizes Turchin's structural-demographic theory with modern proxies
specifically designed for developed economies:

  - Education-job mismatch for elite overproduction (not income concentration
    like PSI; captures the "frustrated aspirant" mechanism more directly)
  - Cost-of-living adjusted wage stagnation for mass immiseration (not
    subsistence crisis; in industrialized societies, immiseration manifests
    through cost-of-living pressure)
  - Government debt trajectory for state fiscal distress

Unlike PSI, uses a weighted average (not multiplicative) combination per
Georgescu's empirical approach for developed economies. This is a correlation-
based aggregation rather than strict multiplicative interaction.

Component weights (from Georgescu 2023):
  Elite Overproduction: 0.35 (strongest correlation in developed economies)
  Mass Immiseration: 0.40 (most variable component in developed economies)
  State Fiscal Distress: 0.25 (persistent but slow-moving)

Source: Georgescu (2023) "Structural-Demographic Theory Revisited: Evidence
        from Industrialized Societies." PLoS ONE 18(11): e0293672.
"""
from datetime import datetime, timezone

import numpy as np
import pandas as pd

from models.models import ComponentScore, ModelOutput, register_model
from models.config import VARIABLES, EVIDENCE_WEIGHTS, EvidenceRating


# ---------------------------------------------------------------------------
# Component weights (Georgescu 2023 empirical approach)
# ---------------------------------------------------------------------------
COMPONENT_WEIGHTS = {
    "elite_overproduction": 0.35,
    "mass_immiseration": 0.40,
    "state_fiscal_distress": 0.25,
}
# Sum = 1.00

# ---------------------------------------------------------------------------
# Component variable mappings
# ---------------------------------------------------------------------------

# Elite Overproduction (modern proxy): education-job mismatch ratio
# This is the key differentiator from PSI, which uses income concentration.
# Georgescu argues that in industrialized societies, elite overproduction
# manifests as too many credential-holders competing for too few positions,
# not as raw wealth inequality.
ELITE_OVERPRODUCTION_VARS = [8]  # Variable #8: Education-Job Mismatch

# Mass Immiseration (modern proxy): cost-of-living adjusted wage stagnation
# In industrialized societies, immiseration manifests through cost-of-living
# pressure rather than subsistence crisis. Workers may maintain nominal
# employment but experience declining purchasing power.
MASS_IMMISERATION_VARS = [2, 16, 17, 40]
# Variable #2:  Real Wage Growth / Labor Share (PRS85006173)
# Variable #16: Housing Affordability (FIXHAI, inverted)
# Variable #17: Inflation Rate (CPIAUCSL)
# Variable #40: Cost of Living Composite

# State Fiscal Distress: government debt trajectory
# Same conceptual dimension as PSI-SFD but normalized independently.
STATE_FISCAL_DISTRESS_VARS = [5]  # Variable #5: Debt/GDP (GFDEGDQ188S)


def _variable_lookup():
    """Build a dict of catalog_number -> Variable for quick access."""
    return {v.catalog_number: v for v in VARIABLES}


def _compute_component(
    unified_df: pd.DataFrame,
    var_numbers: list[int],
    var_lookup: dict,
) -> tuple[float, list[str]]:
    """
    Compute a single Georgescu SDT component as an evidence-weighted
    average of its constituent normalized variables.

    Returns (component_score_0_to_1, list_of_variable_names_used).
    """
    weighted_sum = 0.0
    total_weight = 0.0
    variables_used = []

    for vnum in var_numbers:
        col = f"var_{vnum}"
        if col not in unified_df.columns:
            continue

        series = unified_df[col].dropna()
        if series.empty:
            continue

        latest = float(series.iloc[-1])
        if np.isnan(latest):
            continue

        var_info = var_lookup.get(vnum)
        if var_info is None:
            continue

        weight = EVIDENCE_WEIGHTS[var_info.evidence_rating]
        weighted_sum += latest * weight
        total_weight += weight
        variables_used.append(var_info.name)

    if total_weight == 0.0:
        return 0.0, variables_used

    return weighted_sum / total_weight, variables_used


@register_model("georgescu_sdt")
def compute_georgescu(unified_df: pd.DataFrame) -> ModelOutput:
    """
    Georgescu SDT for Industrialized Societies.
    Operationalizes structural-demographic theory with modern proxies:
    - Education-job mismatch for elite overproduction
    - Cost-of-living adjusted wages for mass immiseration
    - Government debt trajectory for fiscal distress

    Unlike PSI, uses weighted average (not multiplicative) per Georgescu's
    empirical approach for developed economies.

    Parameters
    ----------
    unified_df : pd.DataFrame
        DataFrame with columns named "var_{catalog_number}" containing
        normalized 0.0-1.0 stress values. Index is DatetimeIndex.

    Returns
    -------
    ModelOutput
        Georgescu SDT score (0-100), component breakdown, domain contributions.
    """
    var_lookup = _variable_lookup()

    # Compute each component
    elite_score, elite_vars = _compute_component(
        unified_df, ELITE_OVERPRODUCTION_VARS, var_lookup,
    )
    immis_score, immis_vars = _compute_component(
        unified_df, MASS_IMMISERATION_VARS, var_lookup,
    )
    fiscal_score, fiscal_vars = _compute_component(
        unified_df, STATE_FISCAL_DISTRESS_VARS, var_lookup,
    )

    # Weighted average (NOT multiplicative like PSI)
    # Georgescu's empirical approach for developed economies uses
    # correlation-based weighting rather than strict multiplicative interaction.
    # Renormalize weights over available components only, so missing data
    # (score=0.0 from _compute_component with no variables) does not drag
    # the composite down. With CDF normalization, a component with actual
    # data will never be exactly 0.0 (CDF(z)>0 for all finite z).
    component_results = {
        "elite_overproduction": (elite_score, elite_vars),
        "mass_immiseration": (immis_score, immis_vars),
        "state_fiscal_distress": (fiscal_score, fiscal_vars),
    }
    available_weight_sum = 0.0
    weighted_composite = 0.0
    for key, (score, vars_used) in component_results.items():
        if vars_used:  # component has data
            w = COMPONENT_WEIGHTS[key]
            weighted_composite += w * score
            available_weight_sum += w

    if available_weight_sum > 0:
        composite = weighted_composite / available_weight_sum
    else:
        composite = 0.0

    # Scale to 0-100 and clamp
    georgescu_score = max(0.0, min(100.0, composite * 100.0))

    # Build component scores
    components = [
        ComponentScore(
            name="Elite Overproduction (Education-Job Mismatch)",
            value=elite_score,
            variables_used=elite_vars,
        ),
        ComponentScore(
            name="Mass Immiseration (Cost-of-Living Adjusted)",
            value=immis_score,
            variables_used=immis_vars,
        ),
        ComponentScore(
            name="State Fiscal Distress",
            value=fiscal_score,
            variables_used=fiscal_vars,
        ),
    ]

    # Domain contributions
    all_var_nums = (
        ELITE_OVERPRODUCTION_VARS
        + MASS_IMMISERATION_VARS
        + STATE_FISCAL_DISTRESS_VARS
    )
    domain_contributions = {}
    for vnum in all_var_nums:
        var_info = var_lookup.get(vnum)
        if var_info:
            did = var_info.domain.value
            domain_contributions[did] = domain_contributions.get(did, 0.0) + 1.0

    total = sum(domain_contributions.values())
    if total > 0:
        for k in domain_contributions:
            domain_contributions[k] /= total

    return ModelOutput(
        model_id="georgescu_sdt",
        model_name="Georgescu SDT",
        score=round(georgescu_score, 2),
        components=components,
        domain_contributions=domain_contributions,
        timestamp=datetime.now(timezone.utc).isoformat(),
        variables_used=sorted(set(all_var_nums)),
    )
