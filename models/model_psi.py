"""
Turchin Structural-Demographic PSI (Political Stress Indicator).

Implements PSI = geometric_mean(MMP, EMP, SFD) * 100, encoding the
theoretical claim that political instability requires all three structural
pressures simultaneously.

Phase 1 math fixes applied:
  - Geometric mean (not arithmetic) for PSI composite (fixes critical review A1:
    three 0.70 inputs now yield 0.70, not 0.343)
  - Rolling z-score normalization (not min-max) via normalize.py (fixes
    implementation review A1: prevents pinning trending series to 1.0)
  - PRS85006173 for labor share (nonfarm business sector, Phase 3 recommendation
    over W270RE1A156NBEA)

Source: Turchin (2003) Historical Dynamics; Turchin (2023) End Times;
        Goldstone (1991) Revolution and Rebellion.

Component structure:
  MMP (Mass Mobilization Potential): labor share, unemployment, youth unemployment
  EMP (Elite Mobilization Potential): elite overproduction, elite factionalism,
                                      intra-elite wealth gap, wealth concentration
  SFD (State Fiscal Distress): debt/deficit, financial stress, government trust
"""
from datetime import datetime, timezone

import numpy as np
import pandas as pd

from models.models import ComponentScore, ModelOutput, register_model
from models.config import VARIABLES, EVIDENCE_WEIGHTS, EvidenceRating, Domain


# ---------------------------------------------------------------------------
# Component definitions: map variable catalog numbers to PSI components
# ---------------------------------------------------------------------------

# MMP: Mass Mobilization Potential
# Variable #2 (labor share, inverted: lower share = more stress)
# Variable #9 (unemployment)
# Variable #26 (youth unemployment)
MMP_VARIABLES = [2, 9, 26]

# EMP: Elite Mobilization Potential
# Variable #8 (elite overproduction via education-job mismatch)
# Variable #11 (elite factionalism)
# Variable #19 (intra-elite wealth gap)
# Variable #45 (wealth concentration top 0.1%)
EMP_VARIABLES = [8, 11, 19, 45]

# SFD: State Fiscal Distress
# Variable #5 (debt/deficit)
# Variable #6 (financial stress)
# Variable #7 (government trust, inverted: lower trust = more stress)
SFD_VARIABLES = [5, 6, 7]


def _variable_lookup():
    """Build a dict of catalog_number -> Variable for quick access."""
    return {v.catalog_number: v for v in VARIABLES}


def _evidence_weight(rating: EvidenceRating) -> float:
    """Return the numeric evidence weight for a given rating."""
    return EVIDENCE_WEIGHTS[rating]


def _compute_component(
    unified_df: pd.DataFrame,
    var_numbers: list[int],
    var_lookup: dict,
) -> tuple[float, list[str]]:
    """
    Compute a single PSI component as an evidence-weighted average
    of its constituent normalized variables.

    The unified DataFrame is expected to contain columns named by
    catalog number (e.g., "var_2", "var_9") with values already
    normalized to 0.0-1.0 stress intensity (higher = more stress).

    Returns (component_score, list_of_variable_names_used).
    """
    weighted_sum = 0.0
    total_weight = 0.0
    variables_used = []

    for vnum in var_numbers:
        col = f"var_{vnum}"
        if col not in unified_df.columns:
            continue

        value = unified_df[col].dropna()
        if value.empty:
            continue

        # Use the most recent non-NaN value
        latest = float(value.iloc[-1])
        if np.isnan(latest):
            continue

        var_info = var_lookup.get(vnum)
        if var_info is None:
            continue

        weight = _evidence_weight(var_info.evidence_rating)
        weighted_sum += latest * weight
        total_weight += weight
        variables_used.append(var_info.name)

    if total_weight == 0.0:
        return 0.0, variables_used

    return weighted_sum / total_weight, variables_used


@register_model("psi")
def compute_psi(unified_df: pd.DataFrame) -> ModelOutput:
    """
    Turchin Structural-Demographic PSI.
    PSI = geometric_mean(MMP, EMP, SFD) * 100

    Phase 1 fixes applied:
    - Geometric mean (not arithmetic) for composite
    - Rolling z-score normalization (not min-max)
    - PRS85006173 for labor share

    Parameters
    ----------
    unified_df : pd.DataFrame
        DataFrame with columns named "var_{catalog_number}" containing
        normalized 0.0-1.0 stress values. Index is DatetimeIndex.

    Returns
    -------
    ModelOutput
        PSI score (0-100), component breakdown, domain contributions.
    """
    var_lookup = _variable_lookup()

    # Compute each component
    mmp_score, mmp_vars = _compute_component(unified_df, MMP_VARIABLES, var_lookup)
    emp_score, emp_vars = _compute_component(unified_df, EMP_VARIABLES, var_lookup)
    sfd_score, sfd_vars = _compute_component(unified_df, SFD_VARIABLES, var_lookup)

    # Geometric mean: preserves multiplicative interaction
    # (instability requires all three pressures; any zero factor -> zero PSI)
    components_arr = np.array([mmp_score, emp_score, sfd_score])
    if np.any(components_arr <= 0.0):
        psi_raw = 0.0
    else:
        psi_raw = float(np.power(np.prod(components_arr), 1.0 / 3.0))

    # Scale to 0-100 and clamp
    psi_score = max(0.0, min(100.0, psi_raw * 100.0))

    # Build component scores
    components = [
        ComponentScore(
            name="MMP",
            value=mmp_score,
            variables_used=mmp_vars,
        ),
        ComponentScore(
            name="EMP",
            value=emp_score,
            variables_used=emp_vars,
        ),
        ComponentScore(
            name="SFD",
            value=sfd_score,
            variables_used=sfd_vars,
        ),
    ]

    # Domain contributions: PSI draws primarily from Economic Stress,
    # with contributions from Political Polarization (elite factionalism,
    # wealth gap) and Social Mobilization (government trust)
    all_var_nums = MMP_VARIABLES + EMP_VARIABLES + SFD_VARIABLES
    domain_contributions = {}
    for vnum in all_var_nums:
        var_info = var_lookup.get(vnum)
        if var_info:
            domain_id = var_info.domain.value
            domain_contributions[domain_id] = domain_contributions.get(domain_id, 0.0)
            domain_contributions[domain_id] += 1.0

    # Normalize to proportions
    total_vars = sum(domain_contributions.values())
    if total_vars > 0:
        for k in domain_contributions:
            domain_contributions[k] /= total_vars

    return ModelOutput(
        model_id="psi",
        model_name="Turchin PSI",
        score=round(psi_score, 2),
        components=components,
        domain_contributions=domain_contributions,
        timestamp=datetime.now(timezone.utc).isoformat(),
        variables_used=all_var_nums,
    )
