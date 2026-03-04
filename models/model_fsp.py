"""
Financial Stress Pathway (FSP).

Two-stage model capturing the causal chain from financial system stress
through economic hardship to political grievance:

    Financial Stress (t) -> Economic Pain (t + lag) -> Political Stress

Stage 1 (Financial Trigger): Financial system stress as measured by STLFSI4.
Stage 2 (Economic Transmission): Unemployment, labor share, inflation,
    household debt as channels through which financial stress reaches households.

The transmission coefficient models the lagged relationship between financial
crisis and economic hardship (5-10 year lag per Funke et al. 2016).

CSCICP03USM665S handling (locked decision from Phase 3):
  - CSCICP03USM665S (OECD consumer confidence) is DISCONTINUED.
  - Its weight is dropped and redistributed across remaining ETI components.
  - UMCSENT is NOT used as replacement (preserves zero-overlap design with PLI).
  - Conference Board CCI is NOT used (paywalled).

Source: Funke, Schularick & Trebesch (2016) Going to Extremes;
        Reinhart & Rogoff (2009) This Time Is Different;
        Mian, Sufi & Trebbi (2014) Resolving Debt Overhang.
"""
from datetime import datetime, timezone

import numpy as np
import pandas as pd

from models.models import ComponentScore, ModelOutput, register_model
from models.config import VARIABLES, EVIDENCE_WEIGHTS, EvidenceRating


# ---------------------------------------------------------------------------
# Stage 1: Financial System Stress Index (FSSI)
#
# Single-variable stage using the St. Louis Fed Financial Stress Index
# (Variable #6, STLFSI4). This is already a composite of 18 financial
# market indicators, so it serves as a robust trigger signal.
# ---------------------------------------------------------------------------

FSSI_VARIABLE = 6  # Financial Crisis / Systemic Stress (STLFSI4)

# ---------------------------------------------------------------------------
# Stage 2: Economic Transmission Index (ETI)
#
# Variables through which financial stress reaches households.
# CSCICP03USM665S (OECD consumer confidence) is DISCONTINUED.
# Weight redistributed to remaining components.
#
# Original code weights (with CSCICP03USM665S at 0.35):
#   UNRATE: 0.25, IC4WSA: 0.20, real_wage_change: 0.20, CSCICP03USM665S: 0.35
#
# After dropping CSCICP03USM665S, redistribute proportionally:
#   Variable #9  (unemployment):   0.25 -> 0.385 (0.25/0.65)
#   Variable #2  (labor share):    0.20 -> 0.308 (0.20/0.65)
#   Variable #17 (inflation):      0.15 -> 0.231 (new, takes partial CSCICP weight)
#   Variable #27 (household debt): 0.05 -> 0.077 (new, captures debt burden channel)
#
# Rounded to sum to 1.0:
# ---------------------------------------------------------------------------

ETI_VARIABLES = {
    9:  0.38,   # Unemployment Rate (UNRATE)
    2:  0.30,   # Real Wage Growth / Labor Share (PRS85006173)
    17: 0.22,   # Inflation Rate (CPIAUCSL)
    27: 0.10,   # Household Debt Service Ratio (TDSP)
}
# Sum = 1.00

# Transmission lag window (months) for cross-correlation analysis
TRANSMISSION_LAG_MONTHS = 60  # 5 years (Funke et al. 2016: 5-10 year lag)


def _variable_lookup():
    """Build a dict of catalog_number -> Variable for quick access."""
    return {v.catalog_number: v for v in VARIABLES}


def _compute_fssi(unified_df: pd.DataFrame, var_lookup: dict) -> tuple[float, list[str]]:
    """
    Stage 1: Financial System Stress Index.

    Uses Variable #6 (STLFSI4) normalized stress value directly.
    STLFSI4 is already a composite index, so a single variable suffices.

    Returns (fssi_score_0_to_1, variables_used_names).
    """
    col = f"var_{FSSI_VARIABLE}"
    if col not in unified_df.columns:
        return 0.0, []

    series = unified_df[col].dropna()
    if series.empty:
        return 0.0, []

    latest = float(series.iloc[-1])
    var_info = var_lookup.get(FSSI_VARIABLE)
    var_name = var_info.name if var_info else f"Variable #{FSSI_VARIABLE}"

    return max(0.0, min(1.0, latest)), [var_name]


def _compute_eti(
    unified_df: pd.DataFrame,
    var_lookup: dict,
) -> tuple[float, list[str]]:
    """
    Stage 2: Economic Transmission Index.

    Weighted composite of economic hardship variables that channel
    financial stress to households.

    CSCICP03USM665S is excluded (discontinued). Its weight has been
    redistributed across remaining ETI components proportionally.

    Returns (eti_score_0_to_1, variables_used_names).
    """
    weighted_sum = 0.0
    total_weight = 0.0
    variables_used = []

    for vnum, weight in ETI_VARIABLES.items():
        col = f"var_{vnum}"
        if col not in unified_df.columns:
            continue

        series = unified_df[col].dropna()
        if series.empty:
            continue

        latest = float(series.iloc[-1])
        if np.isnan(latest):
            continue

        weighted_sum += latest * weight
        total_weight += weight

        var_info = var_lookup.get(vnum)
        if var_info:
            variables_used.append(var_info.name)

    if total_weight == 0.0:
        return 0.0, variables_used

    # Renormalize if some variables were missing
    eti_score = weighted_sum / total_weight
    return max(0.0, min(1.0, eti_score)), variables_used


def _compute_transmission_coefficient(
    unified_df: pd.DataFrame,
) -> float:
    """
    Compute the transmission coefficient between FSSI and ETI.

    Uses the lagged relationship: how much does financial stress (Stage 1)
    predict subsequent economic hardship (Stage 2)?

    The coefficient is estimated by comparing current ETI to lagged FSSI.
    A high coefficient means financial stress is actively transmitting
    to economic hardship (the causal chain is active).

    Returns a multiplier in [0.5, 1.5]:
      - 0.5 = financial stress is NOT transmitting (decoupled)
      - 1.0 = normal transmission
      - 1.5 = amplified transmission (economic pain exceeds financial trigger)
    """
    fssi_col = f"var_{FSSI_VARIABLE}"
    if fssi_col not in unified_df.columns:
        return 1.0

    fssi_series = unified_df[fssi_col].dropna()

    # Compute aggregate ETI series for correlation
    eti_values = []
    for vnum, weight in ETI_VARIABLES.items():
        col = f"var_{vnum}"
        if col in unified_df.columns:
            eti_values.append(unified_df[col].ffill() * weight)

    if not eti_values or len(fssi_series) < TRANSMISSION_LAG_MONTHS:
        return 1.0

    eti_series = sum(eti_values)

    # Compare current ETI to lagged FSSI
    if len(fssi_series) > TRANSMISSION_LAG_MONTHS:
        lagged_fssi = float(fssi_series.iloc[-TRANSMISSION_LAG_MONTHS - 1])
        current_eti = float(eti_series.dropna().iloc[-1]) if not eti_series.dropna().empty else 0.0

        if lagged_fssi > 0.01:
            ratio = current_eti / lagged_fssi
            # Clamp to [0.5, 1.5]
            return max(0.5, min(1.5, ratio))

    return 1.0


@register_model("fsp")
def compute_fsp(unified_df: pd.DataFrame) -> ModelOutput:
    """
    Financial Stress Pathway.
    Two-stage: financial crisis trigger -> economic hardship transmission.

    FSP = trigger_intensity * transmission_coefficient * 100

    The score reflects both the current level of financial stress and
    the degree to which that stress has transmitted to household-level
    economic hardship.

    CSCICP03USM665S handling: dropped (discontinued), weight redistributed
    across remaining ETI components. UMCSENT is NOT used (zero-overlap
    design with PLI preserved).

    Parameters
    ----------
    unified_df : pd.DataFrame
        DataFrame with columns named "var_{catalog_number}" containing
        normalized 0.0-1.0 stress values. Index is DatetimeIndex.

    Returns
    -------
    ModelOutput
        FSP score (0-100), stage breakdown, domain contributions.
    """
    var_lookup = _variable_lookup()

    # Stage 1: Financial trigger
    fssi_score, fssi_vars = _compute_fssi(unified_df, var_lookup)

    # Stage 2: Economic transmission
    eti_score, eti_vars = _compute_eti(unified_df, var_lookup)

    # Transmission coefficient: how actively is financial stress becoming
    # economic hardship?
    transmission = _compute_transmission_coefficient(unified_df)

    # FSP composite: weighted combination of trigger and transmission
    # Using max-based leading indicator approach for 2 stages:
    # The higher of FSSI and ETI determines the "leading edge" of the
    # causal chain, modulated by the transmission coefficient
    leading_edge = max(fssi_score, eti_score)
    trailing_edge = min(fssi_score, eti_score)

    # Weighted: 60% leading edge + 40% trailing edge
    # This captures early warning (high FSSI, low ETI) better than simple average
    composite = (0.6 * leading_edge + 0.4 * trailing_edge) * transmission
    fsp_score = max(0.0, min(100.0, composite * 100.0))

    # Components
    components = [
        ComponentScore(
            name="FSSI (Financial Trigger)",
            value=fssi_score,
            variables_used=fssi_vars,
        ),
        ComponentScore(
            name="ETI (Economic Transmission)",
            value=eti_score,
            variables_used=eti_vars,
        ),
        ComponentScore(
            name="Transmission Coefficient",
            value=max(0.0, min(1.0, transmission / 1.5)),  # normalize to 0-1
            variables_used=[],
        ),
    ]

    # Domain contributions
    all_var_nums = [FSSI_VARIABLE] + list(ETI_VARIABLES.keys())
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
        model_id="fsp",
        model_name="Financial Stress Pathway",
        score=round(fsp_score, 2),
        components=components,
        domain_contributions=domain_contributions,
        timestamp=datetime.now(timezone.utc).isoformat(),
        variables_used=sorted(set(all_var_nums)),
    )
