"""
V-Dem ERT (Episodes of Regime Transformation) Institutional Quality Model.

Tracks democratic erosion via rate-of-change analysis on V-Dem indices.

Key insight: For near-ceiling US scores, trends matter more than absolute
levels. The US Liberal Democracy Index declined from ~0.89 to ~0.72
(2015-2022), which is significant even though the absolute level remains
"high" by global standards. Using absolute levels alone would always show
"low stress," masking real institutional deterioration.

Rate-of-change methodology:
  For each V-Dem indicator:
    1. Compute 5-year rolling difference (current year minus 5 years ago)
    2. Negative change = deterioration = higher stress
    3. Map the rate of change to 0.0-1.0 stress using CDF mapping

  For institutional level indicators (state capacity, voter access):
    Use normalized level directly (these are not near-ceiling for the US)

Component weights (by democratic dimension importance):
  Liberal Democracy:         0.25  (primary composite measure)
  Judicial Independence:     0.20  (rule of law backbone)
  Freedom of Expression:     0.15  (information environment)
  Legislative Constraints:   0.15  (checks on executive)
  Electoral Integrity:       0.15  (procedural democracy)
  Executive Aggrandizement:  0.10  (executive overreach)

Additionally includes institutional level indicators:
  State Capacity (WGI GE.EST): weighted at 0.10 of total
  Voter Access (Grumbach SDI): weighted at 0.05 of total

Source: V-Dem Institute (2023); Coppedge et al. (2023) V-Dem Codebook v13;
        Luhrmann & Lindberg (2019) "A Third Wave of Autocratization."
"""
from datetime import datetime, timezone

import numpy as np
import pandas as pd

from models.models import ComponentScore, ModelOutput, register_model
from models.config import VARIABLES, EVIDENCE_WEIGHTS, EvidenceRating


# ---------------------------------------------------------------------------
# Rate-of-change V-Dem indicators with dimension weights
# These use 5-year rolling difference: negative change = higher stress
# ---------------------------------------------------------------------------

VDEM_ROC_INDICATORS = {
    13: {
        "name": "Liberal Democracy Trajectory",
        "v_dem_indicator": "v2x_libdem",
        "weight": 0.25,
    },
    21: {
        "name": "Judicial Independence Trajectory",
        "v_dem_indicator": "v2x_jucon",
        "weight": 0.20,
    },
    22: {
        "name": "Freedom of Expression Trajectory",
        "v_dem_indicator": "v2x_freexp_altinf",
        "weight": 0.15,
    },
    23: {
        "name": "Legislative Constraints Trajectory",
        "v_dem_indicator": "v2xlg_legcon",
        "weight": 0.15,
    },
    24: {
        "name": "Electoral Integrity Trajectory",
        "v_dem_indicator": "v2xel_frefair",
        "weight": 0.15,
    },
    32: {
        "name": "Executive Aggrandizement Trajectory",
        "v_dem_indicator": "v2exrescon",
        "weight": 0.10,
    },
}

# Total weight for ROC indicators
ROC_TOTAL_WEIGHT = sum(d["weight"] for d in VDEM_ROC_INDICATORS.values())

# ---------------------------------------------------------------------------
# Institutional level indicators (not rate-of-change)
# These are not near-ceiling for the US, so levels are informative
# ---------------------------------------------------------------------------

LEVEL_INDICATORS = {
    38: {
        "name": "State Capacity (WGI GE.EST)",
        "weight": 0.10,
    },
    29: {
        "name": "Voter Access (Grumbach SDI)",
        "weight": 0.05,
    },
}

LEVEL_TOTAL_WEIGHT = sum(d["weight"] for d in LEVEL_INDICATORS.values())

# Combined total weight (should sum to approximately 1.15 before normalization)
COMBINED_TOTAL = ROC_TOTAL_WEIGHT + LEVEL_TOTAL_WEIGHT

# 5-year window for rate-of-change computation
ROC_WINDOW = 5  # years (or periods in the DataFrame)


def _variable_lookup():
    """Build a dict of catalog_number -> Variable for quick access."""
    return {v.catalog_number: v for v in VARIABLES}


def _compute_rate_of_change_stress(
    series: pd.Series,
    window: int = ROC_WINDOW,
) -> float:
    """
    Compute stress from rate of change in a V-Dem indicator.

    For variables where lower_is_worse (democratic quality):
      - Declining values = deterioration = higher stress
      - The 5-year difference captures the trajectory

    Maps the rate of change to a 0.0-1.0 stress score:
      - Large negative change (decline) -> stress near 1.0
      - Zero change (stable) -> stress near 0.5
      - Positive change (improvement) -> stress near 0.0

    Uses a sigmoid-like mapping calibrated to V-Dem index scales
    where changes of 0.05-0.20 are significant for developed democracies.
    """
    valid = series.dropna()

    if len(valid) <= window:
        # Not enough data for rate-of-change; return neutral
        return 0.5

    current = float(valid.iloc[-1])
    past = float(valid.iloc[-window - 1]) if len(valid) > window else float(valid.iloc[0])

    # Change: positive = improvement, negative = deterioration
    change = current - past

    # Map change to stress using scaled sigmoid
    # V-Dem indices are 0-1 scale; changes of 0.05 are notable,
    # changes of 0.15+ are dramatic for developed democracies
    # Scale factor calibrated so that:
    #   change = -0.17 (US 2015-2022 decline) -> stress ~ 0.85
    #   change = 0 -> stress = 0.5
    #   change = +0.10 -> stress ~ 0.25
    scale_factor = 10.0
    stress = 1.0 / (1.0 + np.exp(scale_factor * change))

    return float(max(0.0, min(1.0, stress)))


def _compute_roc_components(
    unified_df: pd.DataFrame,
    var_lookup: dict,
) -> tuple[list[ComponentScore], float, list[str], list[int]]:
    """
    Compute rate-of-change stress for all V-Dem trajectory indicators.

    Returns (component_scores, weighted_average, variables_used_names, var_nums).
    """
    components = []
    weighted_sum = 0.0
    total_weight = 0.0
    variables_used = []
    var_nums = []

    for vnum, indicator in VDEM_ROC_INDICATORS.items():
        col = f"var_{vnum}"
        weight = indicator["weight"]

        if col not in unified_df.columns:
            # Missing variable: create component with neutral score
            components.append(ComponentScore(
                name=indicator["name"],
                value=0.5,
                variables_used=[],
            ))
            continue

        series = unified_df[col].dropna()
        if series.empty:
            components.append(ComponentScore(
                name=indicator["name"],
                value=0.5,
                variables_used=[],
            ))
            continue

        # For V-Dem variables in the unified_df, the values are already
        # normalized to 0-1 stress. We need the underlying trajectory
        # (rate of change) rather than the absolute level.
        #
        # The stress normalization already accounts for direction, but
        # for rate-of-change analysis we compute the 5-year rolling
        # difference in the normalized stress values.
        stress = _compute_rate_of_change_stress(series, ROC_WINDOW)

        var_info = var_lookup.get(vnum)
        var_name = var_info.name if var_info else f"Variable #{vnum}"
        variables_used.append(var_name)
        var_nums.append(vnum)

        weighted_sum += stress * weight
        total_weight += weight

        components.append(ComponentScore(
            name=indicator["name"],
            value=round(stress, 4),
            variables_used=[var_name],
        ))

    avg = weighted_sum / total_weight if total_weight > 0 else 0.5
    return components, avg, variables_used, var_nums


def _compute_level_components(
    unified_df: pd.DataFrame,
    var_lookup: dict,
) -> tuple[list[ComponentScore], float, list[str], list[int]]:
    """
    Compute institutional level stress for non-trajectory indicators.

    These variables (state capacity, voter access) are not near-ceiling
    for the US, so their absolute level is informative.

    Returns (component_scores, weighted_average, variables_used_names, var_nums).
    """
    components = []
    weighted_sum = 0.0
    total_weight = 0.0
    variables_used = []
    var_nums = []

    for vnum, indicator in LEVEL_INDICATORS.items():
        col = f"var_{vnum}"
        weight = indicator["weight"]

        if col not in unified_df.columns:
            components.append(ComponentScore(
                name=indicator["name"],
                value=0.5,
                variables_used=[],
            ))
            continue

        series = unified_df[col].dropna()
        if series.empty:
            components.append(ComponentScore(
                name=indicator["name"],
                value=0.5,
                variables_used=[],
            ))
            continue

        # Use latest normalized stress value directly
        latest = float(series.iloc[-1])

        var_info = var_lookup.get(vnum)
        var_name = var_info.name if var_info else f"Variable #{vnum}"
        variables_used.append(var_name)
        var_nums.append(vnum)

        weighted_sum += latest * weight
        total_weight += weight

        components.append(ComponentScore(
            name=indicator["name"],
            value=round(max(0.0, min(1.0, latest)), 4),
            variables_used=[var_name],
        ))

    avg = weighted_sum / total_weight if total_weight > 0 else 0.5
    return components, avg, variables_used, var_nums


@register_model("vdem_ert")
def compute_vdem(unified_df: pd.DataFrame) -> ModelOutput:
    """
    V-Dem ERT Institutional Quality Model.
    Tracks democratic erosion via rate-of-change analysis on V-Dem indices.

    Key insight: For near-ceiling US scores, trends matter more than levels.
    Negative 5-year change in any V-Dem dimension signals institutional stress.

    Parameters
    ----------
    unified_df : pd.DataFrame
        DataFrame with columns named "var_{catalog_number}" containing
        normalized 0.0-1.0 stress values. Index is DatetimeIndex.

    Returns
    -------
    ModelOutput
        V-Dem ERT score (0-100), dimension breakdown, domain contributions.
    """
    var_lookup = _variable_lookup()

    # Rate-of-change components (6 V-Dem trajectory indicators)
    roc_components, roc_avg, roc_vars, roc_nums = _compute_roc_components(
        unified_df, var_lookup,
    )

    # Level components (state capacity, voter access)
    level_components, level_avg, level_vars, level_nums = _compute_level_components(
        unified_df, var_lookup,
    )

    # Combine: ROC indicators weighted more heavily than level indicators
    # (ROC captures the core ERT insight about trajectory vs. level)
    roc_proportion = ROC_TOTAL_WEIGHT / COMBINED_TOTAL
    level_proportion = LEVEL_TOTAL_WEIGHT / COMBINED_TOTAL

    composite = roc_avg * roc_proportion + level_avg * level_proportion

    # Scale to 0-100 and clamp
    vdem_score = max(0.0, min(100.0, composite * 100.0))

    # Combine all components
    all_components = roc_components + level_components

    # Domain contributions
    all_var_nums = roc_nums + level_nums
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
        model_id="vdem_ert",
        model_name="V-Dem ERT",
        score=round(vdem_score, 2),
        components=all_components,
        domain_contributions=domain_contributions,
        timestamp=datetime.now(timezone.utc).isoformat(),
        variables_used=sorted(set(all_var_nums)),
    )
