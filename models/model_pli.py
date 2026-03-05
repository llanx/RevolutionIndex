"""
Prospect Theory Perceived Loss Index (PLI).

Applies Kahneman-Tversky prospect theory to measure perceived losses across
economic domains relative to recent peaks. The core behavioral insight: losses
hurt ~2.25x more than equivalent gains (loss aversion), and people evaluate
conditions relative to what they recently experienced, not in absolute terms.

Phase 1 math fixes applied:
  - Corrected K constants (reduced by 10x from original spec to prevent
    saturation at 100 during any ordinary recession; critical review A2)
  - Additive bonus structure for breadth and velocity (not multiplicative,
    to prevent runaway amplification; critical review A2)
  - Proper velocity computation using rate-of-change (fixes implementation
    review A2: magnitude was being used as proxy for velocity)

Source: Kahneman & Tversky (1979) Prospect Theory;
        Tversky & Kahneman (1992) Advances in Prospect Theory;
        Davies (1962) Toward a Theory of Revolution (J-Curve).

Domain structure:
  Wage/Income: labor share, middle-class income share
  Employment: unemployment, youth unemployment
  Cost-of-Living: housing affordability, inflation, cost of living composite
  Financial: financial stress, household debt
"""
from datetime import datetime, timezone
from typing import Optional

import numpy as np
import pandas as pd

from models.models import ComponentScore, ModelOutput, register_model
from models.config import VARIABLES, EVIDENCE_WEIGHTS, EvidenceRating, NormDirection


# ---------------------------------------------------------------------------
# Prospect theory parameters (Tversky & Kahneman 1992)
# ---------------------------------------------------------------------------
LAMBDA = 2.25   # Loss aversion coefficient
ALPHA = 0.88    # Diminishing sensitivity exponent

# ---------------------------------------------------------------------------
# Domain definitions with corrected K constants (spec K / 10)
# K scales the raw prospect-theory value to a 0-100 score domain.
# ---------------------------------------------------------------------------

PLI_DOMAINS = {
    "wage_income": {
        "name": "Wage/Income",
        "variables": [2, 20],    # labor share, middle-class income share
        "K": 50.0,               # corrected from 500 (spec A2 fix)
    },
    "employment": {
        "name": "Employment",
        "variables": [9, 26],    # unemployment, youth unemployment
        "K": 3.5,                # corrected from 35 (spec A2 fix)
    },
    "cost_of_living": {
        "name": "Cost-of-Living",
        "variables": [16, 17, 40],  # housing affordability, inflation, composite
        "K": 10.0,               # corrected from 100 (spec A2 fix)
    },
    "financial": {
        "name": "Financial",
        "variables": [6, 27],    # financial stress, household debt
        "K": 1.0,                # corrected from 10 (spec A2 fix)
    },
}

# Breadth bonus parameters
MAX_BREADTH_BONUS = 20.0   # Maximum additive breadth bonus
NUM_DOMAINS = len(PLI_DOMAINS)

# Velocity bonus parameters
MAX_VELOCITY_BONUS = 15.0  # Maximum additive velocity bonus
VELOCITY_LOOKBACK = 12     # Number of periods to compute rate-of-change

# Prospect theory adaptation-level: people evaluate conditions relative to
# what they recently experienced, not the all-time average. A 5-year window
# (60 months) captures the adaptation-level reference point.
REFERENCE_WINDOW = 60


def _variable_lookup():
    """Build a dict of catalog_number -> Variable for quick access."""
    return {v.catalog_number: v for v in VARIABLES}


def _compute_domain_loss(
    unified_df: pd.DataFrame,
    var_numbers: list[int],
    K: float,
    var_lookup: dict,
    raw_df: Optional[pd.DataFrame] = None,
) -> tuple[float, float, list[str]]:
    """
    Compute the prospect-theory loss score for a single domain.

    For each variable in the domain:
    1. Find the reference point (trailing 5-year trough as the
       adaptation-level baseline per Kahneman-Tversky: people anchor
       to the best conditions they recently experienced)
    2. Compute deviation from baseline (current vs best recent)
    3. Apply prospect theory value function for losses

    When raw_df is available, uses raw values for reference/deviation
    computation (avoids CDF compression of perceived loss magnitudes).
    Falls back to normalized stress values when raw data is unavailable.

    Returns (loss_score, deviation_magnitude, variables_used).
    """
    weighted_loss = 0.0
    total_weight = 0.0
    deviation_sum = 0.0
    deviation_count = 0
    variables_used = []

    for vnum in var_numbers:
        col = f"var_{vnum}"
        if col not in unified_df.columns:
            continue

        var_info = var_lookup.get(vnum)
        if var_info is None:
            continue

        # Use raw values for reference/deviation when available
        using_raw = raw_df is not None and col in raw_df.columns
        series = (raw_df[col] if using_raw else unified_df[col]).dropna()

        if len(series) < 2:
            continue

        # Reference point: best recent experience (5-year window trough).
        # Kahneman-Tversky adaptation-level: people anchor to the best
        # conditions they recently experienced, not the average.
        window = series.iloc[-REFERENCE_WINDOW:] if len(series) > REFERENCE_WINDOW else series

        if using_raw and var_info.norm_direction == NormDirection.LOWER_IS_WORSE:
            # Raw LOWER_IS_WORSE (e.g., labor share): best = highest value
            reference = float(window.max())
        else:
            # Normalized (higher=worse): best = minimum stress
            # Raw HIGHER_IS_WORSE (e.g., unemployment): best = lowest value
            reference = float(window.min())

        current = float(series.iloc[-1])

        # Deviation: positive means conditions are worse than reference
        if abs(reference) < 1e-10:
            deviation = 0.0
        elif using_raw and var_info.norm_direction == NormDirection.LOWER_IS_WORSE:
            # Deterioration = current below best (reference - current)
            deviation = (reference - current) / abs(reference)
        else:
            # Deterioration = current above best (current - reference)
            deviation = (current - reference) / abs(reference)

        deviation_sum += deviation
        deviation_count += 1

        # Prospect theory value function: only losses (deviation > 0) matter
        if deviation > 0:
            # V = -lambda * |deviation|^alpha (loss domain)
            abs_dev = abs(deviation)
            V = -LAMBDA * (abs_dev ** ALPHA)
            # Loss score: additive scaling with K constant
            # Avoids undocumented sqrt compression from original code
            loss_score = min(100.0, max(0.0, -V * K))
        else:
            loss_score = 0.0

        weight = EVIDENCE_WEIGHTS[var_info.evidence_rating]
        weighted_loss += loss_score * weight
        total_weight += weight
        variables_used.append(var_info.name)

    if total_weight == 0.0:
        return 0.0, 0.0, variables_used

    avg_loss = weighted_loss / total_weight
    avg_deviation = deviation_sum / max(deviation_count, 1)

    return avg_loss, avg_deviation, variables_used


def _compute_velocity(
    unified_df: pd.DataFrame,
    var_numbers: list[int],
    raw_df: Optional[pd.DataFrame] = None,
    var_lookup: Optional[dict] = None,
) -> float:
    """
    Compute actual rate-of-change velocity for domain variables.

    Velocity = average 12-period change across domain variables.
    Positive velocity means stress is increasing (conditions
    deteriorating faster). Uses raw values when available to avoid
    CDF compression of velocity magnitudes.

    Fixes implementation review A2: uses actual rate of change instead
    of deviation magnitude.
    """
    velocities = []

    for vnum in var_numbers:
        col = f"var_{vnum}"

        using_raw = raw_df is not None and col in raw_df.columns
        source_df = raw_df if using_raw else unified_df
        if col not in source_df.columns:
            continue

        series = source_df[col].dropna()
        if len(series) <= VELOCITY_LOOKBACK:
            continue

        current = float(series.iloc[-1])
        past = float(series.iloc[-VELOCITY_LOOKBACK - 1])
        velocity = (current - past) / VELOCITY_LOOKBACK

        # For raw LOWER_IS_WORSE: invert so positive = worsening
        if using_raw and var_lookup:
            var_info = var_lookup.get(vnum)
            if var_info and var_info.norm_direction == NormDirection.LOWER_IS_WORSE:
                velocity = -velocity

        velocities.append(velocity)

    if not velocities:
        return 0.0

    return float(np.mean(velocities))


@register_model("pli")
def compute_pli(
    unified_df: pd.DataFrame,
    raw_df: Optional[pd.DataFrame] = None,
) -> ModelOutput:
    """
    Prospect Theory Political Stress Index.
    Applies loss aversion weighting to economic deterioration.

    Phase 1 fixes applied:
    - Corrected K constants (10x reduction from spec)
    - Additive bonus structure for extreme values
    - Proper velocity computation (rate-of-change, not magnitude)

    Parameters
    ----------
    unified_df : pd.DataFrame
        DataFrame with columns named "var_{catalog_number}" containing
        normalized 0.0-1.0 stress values. Index is DatetimeIndex.
    raw_df : pd.DataFrame, optional
        Pre-normalized raw aligned data. Used for reference/deviation
        computation to avoid CDF compression of perceived losses.

    Returns
    -------
    ModelOutput
        PLI score (0-100), domain breakdown, domain contributions.
    """
    var_lookup = _variable_lookup()

    domain_scores = []
    all_variables_used = []
    all_var_nums = []
    n_domains_in_loss = 0
    components = []

    for domain_id, domain_def in PLI_DOMAINS.items():
        var_nums = domain_def["variables"]
        K = domain_def["K"]
        domain_name = domain_def["name"]

        loss_score, deviation, vars_used = _compute_domain_loss(
            unified_df, var_nums, K, var_lookup, raw_df=raw_df,
        )

        domain_scores.append(loss_score)
        all_variables_used.extend(vars_used)
        all_var_nums.extend(var_nums)

        if loss_score > 0:
            n_domains_in_loss += 1

        components.append(ComponentScore(
            name=domain_name,
            value=min(1.0, loss_score / 100.0),
            variables_used=vars_used,
        ))

    # Mean loss across domains
    mean_loss = float(np.mean(domain_scores)) if domain_scores else 0.0

    # Additive breadth bonus (critical review A2 fix):
    # More domains simultaneously in loss = compounding perceived crisis
    if n_domains_in_loss > 1:
        breadth_bonus = min(
            MAX_BREADTH_BONUS,
            (n_domains_in_loss - 1) * (MAX_BREADTH_BONUS / (NUM_DOMAINS - 1)),
        )
    else:
        breadth_bonus = 0.0

    # Additive velocity bonus: rate of change across all domain variables
    all_domain_vars = []
    for d in PLI_DOMAINS.values():
        all_domain_vars.extend(d["variables"])

    avg_velocity = _compute_velocity(
        unified_df, all_domain_vars, raw_df=raw_df, var_lookup=var_lookup,
    )
    # Only positive velocity (increasing stress) contributes a bonus
    if avg_velocity > 0:
        velocity_bonus = min(MAX_VELOCITY_BONUS, avg_velocity * 100.0)
    else:
        velocity_bonus = 0.0

    # Additive aggregation (critical review A2 fix)
    pli_raw = mean_loss + breadth_bonus + velocity_bonus
    pli_score = max(0.0, min(100.0, pli_raw))

    # Domain contributions by source domain
    domain_contributions = {}
    for vnum in set(all_var_nums):
        var_info = var_lookup.get(vnum)
        if var_info:
            did = var_info.domain.value
            domain_contributions[did] = domain_contributions.get(did, 0.0) + 1.0

    total = sum(domain_contributions.values())
    if total > 0:
        for k in domain_contributions:
            domain_contributions[k] /= total

    return ModelOutput(
        model_id="pli",
        model_name="Prospect Theory PLI",
        score=round(pli_score, 2),
        components=components,
        domain_contributions=domain_contributions,
        timestamp=datetime.now(timezone.utc).isoformat(),
        variables_used=sorted(set(all_var_nums)),
    )
