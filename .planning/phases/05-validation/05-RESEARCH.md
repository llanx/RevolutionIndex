# Phase 5: Validation - Research

**Researched:** 2026-03-04
**Domain:** Model validation, backtesting, sensitivity analysis for composite political stress indicators
**Confidence:** HIGH

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- Use the 5 calibration anchors (2008, 2020, mid-1990s, 2001, 2011) as "in-sample" validation targets
- Add out-of-sample hold-out episodes that the model was NOT calibrated against:
  - 1960s urban unrest / civil rights era (expect Elevated Tension, 26-50)
  - Watergate / Nixon resignation 1973-74 (expect Elevated Tension or low Crisis, 40-60)
  - Late 1980s stability / end of Cold War (expect Stable, 0-25)
  - 2016 election aftermath (expect Elevated Tension, 35-50)
  - January 6, 2021 (expect Crisis Territory, 51-75)
- Out-of-sample episodes are the real test; in-sample anchors just confirm calibration isn't broken
- If data coverage is too thin for early episodes (1960s), note it but don't fail the model for missing data
- Zone accuracy: passes if at least 75% of test episodes land in the correct zone
- Monotonic ordering: all crisis-labeled episodes must score strictly higher than all stability-labeled episodes (hard gate)
- Calibration anchor residuals: each of 5 anchors within 10 points of target. Warn if >10, fail if >15.
- Overall verdict: PASS requires zone accuracy >= 75% AND monotonic ordering holds AND no anchor residual > 15
- Leave-one-out cross-validation (LOOCV): for each of 5 calibration anchors, refit calibration using the other 4, score the held-out episode. Flag overfitting if held-out score deviates by more than 1 full zone (25 points) from target.
- Weight sensitivity analysis: perturb each MODEL_WEIGHTS entry by +/-20% (renormalize to sum=1.0), rerun ensemble for current score. If any single perturbation shifts score by more than 1 zone, the model is fragile.
- Spurious trend detection: check that historical time series doesn't exhibit implausible patterns (monotonic increase, sudden jumps at data boundary years). Visual inspection checklist, not automated.
- Primary output: models/VALIDATION.md with episode-by-episode results, LOOCV table, sensitivity table, overall pass/fail verdict
- Console output: summary pass/fail and key statistics
- Script: models/validate.py runnable via `python models/validate.py`
- Internal-only: not displayed on the website

### Claude's Discretion
- Exact implementation of the validation script structure
- Whether to use matplotlib for diagnostic plots (optional, not required)
- How to handle episodes where data coverage is < 50% of variables
- Console output formatting and verbosity level

### Deferred Ideas (OUT OF SCOPE)
None. Discussion stayed within phase scope.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| TEST-01 | Backtest against historical episodes (1968, 1970, 1992, 2001, 2008, 2020) and verify detection | Episode backtest framework: extract scores from history at episode dates, compare to expected zone. Existing `_build_raw_history()` + `calibrate()` pipeline already produces dated scores. CONTEXT.md refines to 10 episodes (5 in-sample + 5 out-of-sample). |
| TEST-02 | Backtest against quiet periods (1990s stability) and verify low scores | Mid-1990s is already an in-sample anchor (target 20). Add late-1980s as out-of-sample quiet period. Verify scores fall in Stable zone (0-25). |
| TEST-03 | Compute bootstrap confidence intervals on all scores | Already implemented in `calibrate.py::compute_bootstrap_ci()` with n=1000, 90% CI. Validation script should verify CIs are narrow enough that crisis and stability episodes don't overlap. |
| TEST-04 | Sensitivity analysis across plausible parameter ranges | Weight perturbation: +/-20% on MODEL_WEIGHTS, renormalize, rerun. PARAMETERS.md already classifies sensitivity of all 30+ parameters. Focus on HIGH-sensitivity parameters. |
| TEST-05 | Check for spurious upward trends (detrended analysis, placebo tests) | Spurious trend checklist: monotonic increase check, data boundary jump detection, visual inspection criteria. Not automated per user decision. |
| TEST-06 | If multi-model: check inter-model correlation (flag if >0.85) | 5 models exist. Compute pairwise Pearson correlation of historical model scores. Flag any pair > 0.85 as redundant. |
| TEST-07 | Produce validation report with pass/fail assessment and methodology documentation | Generate models/VALIDATION.md with structured sections: episode results, LOOCV table, sensitivity table, inter-model correlation, trend checklist, overall verdict. |
</phase_requirements>

## Summary

Phase 5 validates the 5-model ensemble scoring pipeline built in Phase 4 by answering one question: "Should we trust this score?" The validation consists of four complementary analyses, all runnable from a single `models/validate.py` script:

1. **Episode backtesting** against 10 historical episodes (5 in-sample calibration anchors + 5 out-of-sample hold-outs), checking zone accuracy, monotonic ordering, and calibration residuals.
2. **Leave-one-out cross-validation (LOOCV)** on the 5 calibration anchors to detect overfitting, where each anchor is held out and the remaining 4 are used to refit calibration.
3. **Weight sensitivity analysis** perturbing MODEL_WEIGHTS by +/-20% to test for fragility.
4. **Diagnostic checks** including inter-model correlation, spurious trend detection, and bootstrap CI width verification.

The existing codebase provides all necessary building blocks: `_fit_calibration()` accepts custom anchor subsets (enabling LOOCV), `_build_raw_history()` + `calibrate()` produce the historical score series for episode extraction, `compute_bootstrap_ci()` handles uncertainty quantification, and `MODEL_WEIGHTS` in config.py can be programmatically perturbed. The validation script needs to orchestrate these existing functions into a structured test harness, not reimplement scoring logic.

**Primary recommendation:** Build `models/validate.py` as a thin orchestration layer over existing ensemble/calibrate functions, with a structured report generator that writes `models/VALIDATION.md`. No new libraries needed; numpy, pandas, and the existing models/ package provide everything.

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| numpy | (existing) | Array operations, polyfit for LOOCV calibration refitting | Already in project, `_fit_calibration` uses `np.polyfit` |
| pandas | (existing) | Time series indexing, historical score extraction | Already in project, all pipeline data flows through pd.DataFrame |
| scipy.stats | (existing) | Pearson correlation for inter-model analysis | Already imported in normalize.py |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| matplotlib | 3.x | Diagnostic plots (optional) | Only if user wants visual trend inspection; Claude's discretion says optional |
| SALib | 1.5+ | Morris screening / Sobol indices for formal sensitivity analysis | NOT needed: user specified simpler +/-20% weight perturbation approach, which is implementable with plain numpy |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Manual +/-20% perturbation | SALib Morris/Sobol | SALib is more rigorous but massive overkill for 5 weights; user explicitly chose simple perturbation |
| numpy.polyfit LOOCV | sklearn LeaveOneOut | sklearn adds a dependency for something trivially implementable as a for-loop over 5 anchors |

**Installation:**
No new dependencies required. All functionality uses numpy, pandas, scipy already in the project.

## Architecture Patterns

### Recommended Project Structure
```
models/
  validate.py          # Main validation script (new)
  VALIDATION.md        # Generated validation report (new)
  calibrate.py         # Existing: _fit_calibration(), compute_bootstrap_ci()
  ensemble.py          # Existing: compute_ensemble(), _run_models_on_slice()
  config.py            # Existing: MODEL_WEIGHTS, VARIABLES
  pipeline.py          # Existing: fetch_all(), compute_domain_scores()
```

### Pattern 1: Reuse _fit_calibration() for LOOCV

**What:** The existing `_fit_calibration(raw_scores, anchors)` already accepts a custom anchor list. LOOCV simply calls it 5 times, each time with one anchor removed.

**When to use:** For each held-out anchor, pass the remaining 4 anchors to `_fit_calibration()`, get new (a, b) coefficients, then compute the held-out score as `a * raw_value + b`.

**Example:**
```python
from models.calibrate import _fit_calibration, _get_anchor_raw_score, DEFAULT_ANCHORS

def run_loocv(raw_scores: pd.Series) -> list[dict]:
    """Leave-one-out cross-validation on calibration anchors."""
    results = []
    for i, held_out in enumerate(DEFAULT_ANCHORS):
        remaining = [a for j, a in enumerate(DEFAULT_ANCHORS) if j != i]
        a, b, _residuals = _fit_calibration(raw_scores, remaining)

        raw_val = _get_anchor_raw_score(raw_scores, held_out["date"])
        if raw_val is None:
            results.append({"anchor": held_out["label"], "status": "NO_DATA"})
            continue

        predicted = max(0, min(100, a * raw_val + b))
        deviation = abs(predicted - held_out["target"])
        results.append({
            "anchor": held_out["label"],
            "target": held_out["target"],
            "predicted": round(predicted, 1),
            "deviation": round(deviation, 1),
            "overfitting": deviation > 25,  # >1 zone deviation
        })
    return results
```

### Pattern 2: Weight Perturbation via MODEL_WEIGHTS Modification

**What:** Perturb each of 5 MODEL_WEIGHTS entries by +/-20%, renormalize to sum=1.0, rerun ensemble scoring for current time slice.

**When to use:** Sensitivity analysis. Tests whether the composite score is fragile (shifts >25 points / 1 zone from a single 20% weight change).

**Example:**
```python
from models.config import MODEL_WEIGHTS
from models.ensemble import _run_models_on_slice, _rename_columns_for_models

def run_weight_sensitivity(unified_df: pd.DataFrame, raw_df=None) -> list[dict]:
    """Perturb MODEL_WEIGHTS +/-20% and measure score shift."""
    # Get baseline score
    model_df = _rename_columns_for_models(unified_df)
    raw_model_df = _rename_columns_for_models(raw_df) if raw_df is not None else None
    baseline = _run_models_on_slice(model_df, raw_df_slice=raw_model_df)

    results = []
    for target_model in MODEL_WEIGHTS:
        for direction, factor in [("+20%", 1.20), ("-20%", 0.80)]:
            # Create perturbed weights
            perturbed = dict(MODEL_WEIGHTS)
            perturbed[target_model] *= factor
            # Renormalize to sum=1.0
            total = sum(perturbed.values())
            perturbed = {k: v / total for k, v in perturbed.items()}

            # Temporarily patch MODEL_WEIGHTS, run models, restore
            # (Implementation detail: safer to pass weights as parameter)
            score = _run_models_with_weights(model_df, perturbed, raw_model_df)
            shift = abs(score - baseline)

            results.append({
                "model": target_model,
                "perturbation": direction,
                "baseline": round(baseline, 1),
                "perturbed_score": round(score, 1),
                "shift": round(shift, 1),
                "fragile": shift > 25,
            })
    return results
```

### Pattern 3: Episode Score Extraction from History

**What:** Extract calibrated scores at specific historical dates from the existing history time series, then compare to expected zone classifications.

**When to use:** For backtesting against the 10 defined episodes.

**Example:**
```python
def extract_episode_score(calibrated_history: pd.Series, date_spec) -> float:
    """Extract score nearest to episode date from calibrated history."""
    # Reuse _get_anchor_raw_score logic from calibrate.py
    # but operating on calibrated (not raw) scores
    from models.calibrate import _get_anchor_raw_score
    return _get_anchor_raw_score(calibrated_history, date_spec)
```

### Pattern 4: Markdown Report Generation

**What:** Programmatically generate VALIDATION.md with tables, pass/fail badges, and methodology notes.

**When to use:** Final output step of validate.py.

**Example:**
```python
def write_validation_report(
    episode_results: list[dict],
    loocv_results: list[dict],
    sensitivity_results: list[dict],
    correlation_matrix: dict,
    trend_checklist: dict,
    overall_verdict: str,
) -> None:
    """Write models/VALIDATION.md with full validation results."""
    lines = ["# Validation Report", ""]
    lines.append(f"**Generated:** {datetime.now().isoformat()}")
    lines.append(f"**Overall Verdict:** {overall_verdict}")
    # ... structured section generation ...
```

### Anti-Patterns to Avoid
- **Re-running the full data pipeline inside validate.py:** The validation script should call `fetch_all()` once (or with `--cached-only`) and reuse the resulting DataFrames for all tests. Do not fetch data multiple times.
- **Modifying global state for weight perturbation:** Do not monkey-patch `MODEL_WEIGHTS` in config.py. Instead, pass custom weights as parameters to a scoring function, or use a temporary copy.
- **Hardcoding episode dates that duplicate calibrate.py anchors:** Import `DEFAULT_ANCHORS` from calibrate.py rather than re-specifying them. Only the out-of-sample episodes should be defined fresh in validate.py.
- **Testing against episodes outside the history data range:** The current history starts at 1979. The 1960s and early 1970s episodes may have no data. Handle gracefully with coverage annotations rather than errors.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Calibration curve fitting | Custom regression | `calibrate._fit_calibration()` | Already tested, uses np.polyfit, handles edge cases |
| Score-to-zone mapping | Manual if/elif | `calibrate.score_to_zone()` | Already tested, matches data.ts boundaries exactly |
| Historical score computation | New scoring loop | `ensemble._build_raw_history()` + `calibrate.calibrate()` | Ensures validation uses identical methodology to production |
| Bootstrap CIs | Custom resampler | `calibrate.compute_bootstrap_ci()` | Already implements domain-level resampling with n=1000 |
| Model registry iteration | Hardcoded model list | `MODEL_REGISTRY` from models.py | Auto-discovers all @register_model functions |

**Key insight:** Phase 4 already built all the scoring, calibration, and uncertainty quantification machinery. The validation script is purely an orchestration and reporting layer, not a reimplementation.

## Common Pitfalls

### Pitfall 1: LOOCV with Only 5 Anchors Is Low-Power
**What goes wrong:** With only 5 calibration anchors, leaving one out leaves only 4 for refitting. The least-squares fit with 4 points and 2 parameters (a, b) has only 2 degrees of freedom. The resulting calibration may be poorly constrained.
**Why it happens:** This is inherent to the problem size, not a coding error. The model was deliberately calibrated on a small number of well-understood episodes.
**How to avoid:** Do not over-interpret LOOCV deviations. The 25-point threshold (1 zone) is generous precisely because the test is low-power. Report the results but frame them as "no evidence of gross overfitting" rather than "proven not overfit." A deviation of 15-20 points should be noted but not treated as failure.
**Warning signs:** If removing any single anchor causes the calibration to produce nonsensical results (negative a coefficient, scores outside 0-100), the anchor set may be poorly distributed.

### Pitfall 2: History Data Gaps for Early Episodes
**What goes wrong:** The current history.json starts at 1979. Out-of-sample episodes in the 1960s and early 1970s (civil rights era, Watergate) will have no model scores to evaluate.
**Why it happens:** Rolling z-score normalization with a 240-month window produces NaN for the first ~20 years of data. Many variables (especially non-FRED manual sources) start well after 1960.
**How to avoid:** The user's CONTEXT.md explicitly states: "If data coverage is too thin for early episodes (1960s), note it but don't fail the model for missing data." Implement a coverage check: count how many of 41 variables have data at the episode date. If < 50% (Claude's discretion threshold), flag as "insufficient coverage" and exclude from pass/fail calculation but still report.
**Warning signs:** Episodes scoring exactly 0 or showing no variation across episodes likely indicate data gaps, not model quality issues.

### Pitfall 3: Weight Sensitivity Conflation with Model Quality
**What goes wrong:** If perturbing one model's weight by 20% shifts the score significantly, the instinct is to call the model "bad." But this may simply mean that model is contributing meaningful, unique information.
**Why it happens:** High sensitivity to a weight means that model's score diverges from the ensemble average. This is expected behavior for a diverse ensemble, where each model captures different risk dimensions.
**How to avoid:** Interpret sensitivity results carefully. Only flag as "fragile" if a perturbation shifts the score by more than 1 full zone (25 points), as specified in CONTEXT.md. Report absolute shifts for all perturbations so the user can interpret relative sensitivity.
**Warning signs:** If ALL perturbations produce near-zero shifts, the models may be redundant (check inter-model correlation).

### Pitfall 4: Spurious Trend Detection False Positives
**What goes wrong:** A rising trend in the composite score over 1980-2025 gets flagged as "spurious" when it may reflect genuine structural changes (rising inequality, increasing polarization).
**Why it happens:** The spurious trend check is meant to catch artifacts (data boundary effects, normalization artifacts), not real secular trends.
**How to avoid:** Focus the spurious trend check on: (a) sudden jumps at years where new data sources begin coverage (e.g., STLFSI4 starts 1993, ACLED starts 2020), (b) monotonic increase across ALL decades without any dip (unrealistic for a stress indicator), (c) scores hitting 0 or 100 for extended periods (saturation artifacts). A gradually rising trend with dips during stability periods is plausible, not spurious.
**Warning signs:** Scores jumping sharply at exactly the year a major data source begins coverage.

### Pitfall 5: Ignoring the CI Width Requirement
**What goes wrong:** Bootstrap CIs are computed but never checked for whether they distinguish crisis from non-crisis periods. Wide CIs (spanning 2+ zones) make the score meaningless regardless of the point estimate.
**Why it happens:** The CI computation already works (TEST-03) but the validation must check that crisis-period CIs don't overlap with stability-period CIs.
**How to avoid:** Explicitly compute CI for both a crisis episode (e.g., 2008) and a stability episode (e.g., mid-1990s), then verify the intervals are non-overlapping. Report the gap or overlap in the validation report.
**Warning signs:** Current data shows CI of [36.6, 42.3] for a point estimate of 69, which suggests the CI is for a different time point or there's a centering issue. Validate that CI contains or is near the point estimate.

## Code Examples

### Episode Definition Structure
```python
# Out-of-sample episodes (not used in calibration)
OUT_OF_SAMPLE_EPISODES = [
    {
        "date": ("1965-01", "1968-12"),  # Range for civil rights era
        "expected_zone": "Elevated Tension",
        "expected_range": (26, 50),
        "label": "1960s Urban Unrest / Civil Rights Era",
        "min_coverage": 0.3,  # Lower threshold for early period
    },
    {
        "date": ("1973-06", "1974-12"),
        "expected_zone": "Elevated Tension",  # or low Crisis
        "expected_range": (40, 60),
        "label": "Watergate / Nixon Resignation",
        "min_coverage": 0.3,
    },
    {
        "date": ("1987-01", "1989-12"),
        "expected_zone": "Stable",
        "expected_range": (0, 25),
        "label": "Late 1980s Stability / End of Cold War",
        "min_coverage": 0.5,
    },
    {
        "date": ("2016-11", "2017-01"),
        "expected_zone": "Elevated Tension",
        "expected_range": (35, 50),
        "label": "2016 Election Aftermath",
        "min_coverage": 0.5,
    },
    {
        "date": "2021-01",
        "expected_zone": "Crisis Territory",
        "expected_range": (51, 75),
        "label": "January 6, 2021",
        "min_coverage": 0.5,
    },
]
```

### Inter-Model Correlation Check
```python
def check_inter_model_correlation(
    unified_df: pd.DataFrame,
    raw_df: pd.DataFrame = None,
    threshold: float = 0.85,
) -> list[dict]:
    """
    Compute pairwise correlation between model historical scores.
    Flag pairs exceeding threshold as potentially redundant.
    """
    from models.ensemble import _ensure_models_registered, _rename_columns_for_models
    from models.models import MODEL_REGISTRY
    _ensure_models_registered()

    model_df = _rename_columns_for_models(unified_df)
    raw_model_df = _rename_columns_for_models(raw_df) if raw_df is not None else None

    # Collect current scores from each model
    model_scores = {}
    for model_id, model_fn in MODEL_REGISTRY.items():
        try:
            output = model_fn(model_df, raw_df=raw_model_df)
            model_scores[model_id] = output.score
        except TypeError:
            try:
                output = model_fn(model_df)
                model_scores[model_id] = output.score
            except Exception:
                continue
        except Exception:
            continue

    # Note: for proper correlation, need historical scores per model
    # This requires running each model individually on historical slices
    # For current implementation, report current scores and note limitation

    results = []
    model_ids = list(model_scores.keys())
    for i in range(len(model_ids)):
        for j in range(i + 1, len(model_ids)):
            results.append({
                "model_a": model_ids[i],
                "model_b": model_ids[j],
                "score_a": model_scores[model_ids[i]],
                "score_b": model_scores[model_ids[j]],
                # Full correlation requires historical series per model
                "note": "Full temporal correlation requires per-model history",
            })

    return results
```

### Validation Script Main Structure
```python
"""
Model validation: backtest against historical episodes, test calibration
stability, analyze parameter sensitivity, produce pass/fail report.

Usage:
    python models/validate.py                 # full validation
    python models/validate.py --cached-only   # use cached data only
"""
import argparse
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Revolution Index Validation")
    parser.add_argument("--cached-only", action="store_true")
    args = parser.parse_args()

    # 1. Load data (reuses pipeline.fetch_all)
    # 2. Run ensemble to get raw history + calibrated history
    # 3. Episode backtesting (in-sample + out-of-sample)
    # 4. LOOCV on calibration anchors
    # 5. Weight sensitivity analysis
    # 6. Inter-model correlation check
    # 7. Spurious trend checklist
    # 8. CI width verification
    # 9. Compute overall verdict
    # 10. Write VALIDATION.md report
    # 11. Print console summary

    pass

if __name__ == "__main__":
    main()
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Min-max normalization | Rolling z-score + CDF | Phase 4 (2026-03) | Fixes pinning bug, enables valid backtesting |
| Simple anchor-based scale | Least-squares linear fit with 5 anchors | Phase 4 (2026-03) | More robust calibration with residual tracking |
| Single-model validation | 5-model ensemble cross-checking | Phase 4 (2026-03) | Inter-model correlation becomes a meaningful test |
| Manual parameter tuning | PARAMETERS.md with sensitivity classifications | Phase 4 (2026-03) | Structured sensitivity analysis possible |

**Deprecated/outdated:**
- Min-max normalization: replaced with rolling z-score in Phase 4 (Phase 1 review identified pinning bug)
- Polity V regime type indicator: replaced with V-Dem v15 (Polity V last updated 2018, deprecated)

## Open Questions

1. **1960s/1970s Data Coverage Adequacy**
   - What we know: History starts at 1979-01 in current history.json. Rolling z-score window is 240 months, so meaningful normalized scores only emerge ~20 years after variable start dates.
   - What's unclear: Whether enough FRED variables have data back to the 1960s to produce any meaningful score for the civil rights era and Watergate episodes.
   - Recommendation: Run the validation and report coverage percentage per episode. If 1960s episodes have < 30% coverage, mark as "insufficient data" in the report and exclude from the 75% zone accuracy calculation. This aligns with the user's instruction to "note it but don't fail the model."

2. **Inter-Model Historical Correlation Computation**
   - What we know: The current pipeline runs all 5 models together via `_run_models_on_slice()` but does not store per-model historical scores.
   - What's unclear: Whether computing per-model historical scores is feasible within acceptable runtime (need to run each model independently on each historical slice).
   - Recommendation: For the current-period correlation check, just compare the 5 model scores at the latest time point. For full historical correlation, add an option to `_build_raw_history()` that returns per-model scores. If this is too expensive, use the current-point comparison and note the limitation.

3. **Spurious Trend Detection Automation**
   - What we know: User specified "visual inspection checklist, not automated."
   - What's unclear: Whether to generate any automated statistics (e.g., Mann-Kendall trend test, data boundary detection) to support the visual inspection.
   - Recommendation: Generate simple automated flags (monotonic increase check, score jump detection at known data boundary years: 1989 for WFRBSTP1300, 1993 for STLFSI4, 2000 for Grumbach SDI, 2005 for education-job mismatch, 2017 for Bright Line Watch, 2020 for ACLED) and present them as a checklist in the report. The user performs the final visual judgment.

4. **Bootstrap CI Centering Issue**
   - What we know: Current data shows CI of [36.6, 42.3] with a point estimate of 69. The CI does not contain the point estimate, suggesting it may be for a different time point or the bootstrap is sampling from a different distribution than the point estimate.
   - What's unclear: Whether this is a data artifact from the demo/cached data or a genuine bug in the bootstrap implementation.
   - Recommendation: The validation script should explicitly verify that the bootstrap CI contains or is within 5 points of the calibrated point estimate. If not, flag this as a diagnostic issue in the report. This is a data quality check, not a code change.

## Detailed Technical Findings

### Finding 1: _fit_calibration() Already Supports LOOCV (HIGH confidence)
The existing `_fit_calibration(raw_scores, anchors)` function in calibrate.py (line 74) accepts a custom anchor list. This means LOOCV is implementable as a simple for-loop that calls `_fit_calibration()` with 4 of 5 anchors, without any code modification to calibrate.py. The function returns `(a, b, residuals)`, and `_get_anchor_raw_score()` (line 42) can extract the held-out raw score for computing the predicted calibrated value.

**Source:** Direct code inspection of `C:/Users/matts/RevolutionIndex/models/calibrate.py`

### Finding 2: Weight Perturbation Requires Careful Implementation (HIGH confidence)
`MODEL_WEIGHTS` is a module-level dict in config.py. Directly modifying it would corrupt global state for subsequent tests. The weight perturbation analysis needs to either: (a) create a temporary copy, modify it, and pass it to a scoring function that accepts custom weights, or (b) use a context manager that saves/restores the original weights. Option (a) is cleaner but requires a small modification to `_run_models_on_slice()` to accept custom weights as a parameter. Option (b) works with existing code but is fragile in case of exceptions.

**Recommended approach:** Create a helper function in validate.py that temporarily replaces `MODEL_WEIGHTS` in the config module, runs the scoring, and restores the original values, wrapped in a try/finally block. This avoids modifying any existing production code.

**Source:** Direct code inspection of `C:/Users/matts/RevolutionIndex/models/config.py` and `ensemble.py`

### Finding 3: History Coverage Limits Episode Testing (HIGH confidence)
The current history.json contains entries from 1979-01 to 2025-12, with annual frequency pre-2000 and quarterly post-2000 (126 entries total). This means:
- 1960s civil rights era: **NO DATA** (outside history range)
- Watergate 1973-74: **NO DATA** (outside history range)
- Late 1980s stability: **LIMITED DATA** (1987-1989 available but early in the score timeline, may have normalization artifacts)
- All other episodes: **DATA AVAILABLE**

Of the 5 out-of-sample episodes, only 3 have usable data. This does not invalidate the test design (user explicitly allows for data gaps) but the zone accuracy calculation will be based on a smaller denominator.

**Source:** Direct inspection of `C:/Users/matts/RevolutionIndex/public/data/history.json`

### Finding 4: Existing History Scores Show Plausible Patterns (HIGH confidence)
Inspecting current history.json values:
- 1990s (Stable period): scores range 1-30, mostly in Stable zone (correct)
- 2008 area: scores 57-81, peaking in Crisis/Revolution zone (correct direction)
- 2020 area: scores 56-94, peaking at 94 in January (higher than expected 65 target)
- 2011 area: scores 47-53, in Elevated Tension / borderline Crisis (correct)
- 2016: scores 57-66, in Crisis Territory (higher than expected 35-50 for out-of-sample)

Notable: The 2020-01 score of 94 and 2016 scores of 57-66 suggest the model may be running "hot" compared to expectations. This is a genuine finding that the validation report should document.

**Source:** Direct inspection of `C:/Users/matts/RevolutionIndex/public/data/history.json`

### Finding 5: SALib Is Available But Not Needed (MEDIUM confidence)
SALib (Sensitivity Analysis Library in Python) provides industrial-strength Morris screening and Sobol indices implementations. However, the user explicitly chose a simpler approach: +/-20% perturbation on 5 model weights. With only 5 parameters to test (10 perturbations total: 5 models x 2 directions), the analysis is trivially implementable without SALib. Using SALib would add a dependency and complexity with no material benefit for this use case.

**Source:** [SALib documentation](https://salib.readthedocs.io/), [SALib GitHub](https://github.com/SALib/SALib)

### Finding 6: COINr Methodology Is Relevant but R-Only (MEDIUM confidence)
The COINr package (R) provides a comprehensive framework for composite indicator sensitivity analysis, including Monte Carlo uncertainty analysis and global variance decomposition. Its methodology documentation at Chapter 14 provides excellent conceptual guidance for interpreting sensitivity results, even though we're implementing in Python. Key insight from COINr: sensitivity analysis of composite indicators should distinguish between "uncertainty in the indicator" (what the bootstrap CI captures) and "uncertainty due to construction choices" (what weight perturbation captures).

**Source:** [COINr Documentation Chapter 14](https://bluefoxr.github.io/COINrDoc/sensitivity-analysis.html)

## Sources

### Primary (HIGH confidence)
- Direct code inspection: models/calibrate.py, models/ensemble.py, models/config.py, models/run.py, models/pipeline.py, models/normalize.py, models/model_*.py, models/PARAMETERS.md
- Direct data inspection: public/data/history.json, public/data/current.json
- Project context: .planning/phases/05-validation/05-CONTEXT.md, .planning/REQUIREMENTS.md, .planning/STATE.md

### Secondary (MEDIUM confidence)
- [SALib documentation](https://salib.readthedocs.io/) - Python sensitivity analysis library capabilities
- [COINr Sensitivity Analysis Chapter](https://bluefoxr.github.io/COINrDoc/sensitivity-analysis.html) - Composite indicator validation methodology
- [NumPy polyfit documentation](https://numpy.org/doc/stable/reference/generated/numpy.polyfit.html) - Least-squares fitting behavior

### Tertiary (LOW confidence)
- [Fragile States Index Indicators](https://fragilestatesindex.org/indicators/) - General composite index validation patterns
- [CFA Backtesting and Simulation](https://www.cfainstitute.org/insights/professional-learning/refresher-readings/2026/backtesting-and-simulation) - Backtesting methodology concepts

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - No new libraries needed; all functionality uses existing numpy/pandas/scipy
- Architecture: HIGH - Direct code inspection confirms all reuse patterns; _fit_calibration(), _build_raw_history(), compute_bootstrap_ci() all accept the parameters needed for validation
- Pitfalls: HIGH - Identified from actual data inspection (history gaps, CI centering issue, score "hot" running in 2016/2020) not theoretical concerns

**Research date:** 2026-03-04
**Valid until:** 2026-04-04 (stable, no external dependency changes expected)
