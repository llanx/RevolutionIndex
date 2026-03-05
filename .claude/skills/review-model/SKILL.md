---
name: review-model
description: Review Revolution Index model code for theory-to-code translation bugs, methodological issues, and implementation correctness. Use when model outputs look wrong, after adding new variables/models, or before validation runs.
---

Review all model code in `models/` for theory-to-code translation bugs. These are not syntax errors or linting issues. They are cases where the code does not correctly operationalize the academic theory it claims to implement.

Run all 8 checks below systematically. For each, scan the relevant files, compare code against theory, and report findings.

If the user includes `--fix` in their invocation, apply fixes directly after reporting. Otherwise, report only.

## Files to Review

- `models/config.py` (variable definitions, weights, evidence ratings)
- `models/model_psi.py` (Turchin PSI)
- `models/model_pli.py` (Prospect Theory PLI)
- `models/model_fsp.py` (Financial Stress Pathway)
- `models/model_georgescu.py` (Georgescu SDT)
- `models/model_vdem.py` (V-Dem ERT)
- `models/ensemble.py` (ensemble scoring, bootstrap CIs)
- `models/pipeline.py` (data fetching, normalization, construct_proxy)
- `models/calibrate.py` (calibration anchors)

## Check 1: Variable Identity

**Pattern**: Two variables sharing the same FRED `series_id`, or a CONSTRUCTED variable with no matching `construct_proxy` case in `pipeline.py`.

**Why**: If two config entries pull the same series, one variable is double-counted. If a CONSTRUCTED variable has no proxy builder, it silently produces NaN.

**How to check**:
1. In `config.py`, collect all `series_id` values where `series_id is not None`. Flag any duplicates.
2. For each variable with `source_type=CONSTRUCTED`, verify `pipeline.py:construct_proxy()` has a matching `catalog_number` case.
3. Verify each variable's `source_type` matches how the pipeline actually retrieves it (FRED_API variables must have a `series_id`, MANUAL_DOWNLOAD must have `manual_source`).

**Fix**: Remove duplicate series, add missing construct_proxy cases, correct source_type mismatches.

## Check 2: Normalization Layer Violations

**Pattern**: Computing rate-of-change, differences, derivatives, or rolling z-scores on data that has already been CDF-mapped or percentile-ranked (i.e., normalized to 0-1).

**Why**: CDF mapping compresses the distribution. A change from 0.80 to 0.85 in normalized space may represent a huge or tiny raw change depending on where it falls on the original distribution. Rate-of-change analysis requires raw values.

**How to check**:
1. In `model_vdem.py`, verify that rate-of-change (5-year rolling difference) is computed on raw V-Dem scores, not on CDF-mapped values.
2. In any model file, look for patterns where `.diff()`, `.pct_change()`, or rolling window differences are applied after normalization functions have already been called.
3. Check `pipeline.py` normalization order: raw data should be available to models before any CDF/percentile transformation.

**Fix**: Ensure models receive raw values for trajectory analysis. Apply CDF mapping only to the final stress score, not to intermediate rate-of-change calculations.

## Check 3: Aggregation Method vs Theory

**Pattern**: Using `max(score, epsilon)` or similar floors in geometric mean calculations, which conflates "no data available" with "low stress."

**Why**: Geometric mean is theoretically correct for PSI (simultaneous co-occurrence of MMP x EMP x SFD). But if a component is missing, substituting a small epsilon (e.g., 0.01) claims "this dimension has near-zero stress" rather than "we don't know." This biases the composite downward.

**How to check**:
1. In `model_psi.py`, check how missing components are handled in the geometric mean calculation.
2. Look for `max(score, epsilon)`, `max(score, 0.01)`, or similar patterns.
3. Verify that models using weighted average (Georgescu SDT) properly handle missing components by adjusting weights to sum to 1.0 over available components only.

**Fix**: For geometric mean models, use adaptive dimensionality: take geometric mean over available components only. For weighted average models, renormalize weights over available components.

## Check 4: Reference Points and Baselines

**Pattern**: Using all-time `series.mean()` as a reference point in a prospect theory context, where theory requires a recent adaptation-level reference.

**Why**: Kahneman-Tversky prospect theory says people evaluate outcomes relative to their recent experience (adaptation level), not relative to a historical average they have never experienced. Using all-time mean as the reference point would mean someone in 2024 perceives loss relative to conditions in 1960, which is psychologically wrong.

**How to check**:
1. In `model_pli.py`, find the reference point calculation. It should use a rolling window of recent values (e.g., trailing 3-5 year peak), not `series.mean()` over the entire history.
2. Check that the rolling window length matches the theory's timescale for adaptation. Prospect theory adaptation is typically 2-5 years.
3. Check rate-of-change windows in other models: do they match the theoretical mechanism's timescale?

**Fix**: Replace all-time mean references with rolling-window recent peaks. Use theoretically justified window lengths.

## Check 5: Causal Direction in Ratios

**Pattern**: A simple ratio `A/B` that becomes unstable or meaningless when B approaches zero, or that encodes the causal direction backwards.

**Why**: If the theory says "financial stress causes economic pain," the code should measure the strength of that causal link (e.g., lagged correlation), not a simple ratio of stress/pain levels. A ratio can be high simply because the denominator is small, regardless of any causal connection.

**How to check**:
1. In `model_fsp.py`, verify the transmission coefficient between financial stress and economic transmission. It should use lagged correlation or a similar causal measure, not a simple ratio.
2. Check any ratio calculations across all model files for division-by-zero guards and whether the ratio captures the intended causal claim.
3. In `config.py`, check constructed variable #8 (Elite Overproduction): the ratio of degree holders to job openings should handle near-zero openings.

**Fix**: Prefer correlation-based or regression-based transmission measures over simple ratios. Add proper guards for near-zero denominators with theoretically motivated fallbacks.

## Check 6: Bootstrap/CI Consistency

**Pattern**: Bootstrap confidence intervals computed using a different code path than the point estimate, so the CI bounds answer a different question than the point estimate.

**Why**: The CI should represent uncertainty in the same quantity as the point estimate. If the point estimate uses model weights but the bootstrap resamples raw variables, they measure different things.

**How to check**:
1. In `ensemble.py`, find the bootstrap CI computation.
2. Verify that each bootstrap iteration runs the identical model pipeline as the point estimate (same normalization, same model functions, same ensemble weighting).
3. Check that perturbation happens at the input level (adding noise to raw data), not by running a different model path.
4. Verify both point estimate and CI reference the same time point.

**Fix**: Ensure bootstrap iterations call exactly the same code path as the point estimate, with perturbation only at the input data level.

## Check 7: Calibration Circularity

**Pattern**: Calibration anchors that force known historical episodes to predetermined scores, which can mask genuinely novel patterns.

**Why**: If the calibration says "2008 must score 75-85," then any model change that would have scored 2008 differently gets overridden. This means the model cannot discover that its raw (uncalibrated) estimate for 2008 was wrong, because it never sees the discrepancy.

**How to check**:
1. In `calibrate.py`, identify all calibration anchor episodes and their forced score ranges.
2. Verify that raw (pre-calibration) scores are preserved and accessible for comparison.
3. Check whether the calibration is a simple linear rescaling (acceptable) or a nonlinear warping that could distort relative magnitudes between non-anchor periods.
4. Verify that the number of anchor points is small relative to the number of scored periods.

**Fix**: Always output both raw and calibrated scores. Use linear rescaling between anchors. Flag when raw vs calibrated scores diverge significantly, as this indicates model-theory mismatch.

## Check 8: Domain Weight and Evidence Weight Integrity

**Pattern**: Weight sets that don't sum to 1.0, or evidence weight labels that don't match the variable catalog's stated ratings.

**Why**: If MODEL_WEIGHTS don't sum to 1.0, the ensemble over- or under-weights the total. If a variable is labeled "Strong" in the catalog but gets a "Moderate" weight in code, the implementation contradicts the evidence assessment.

**How to check**:
1. In `config.py`, verify `DOMAIN_WEIGHTS` sums to 1.0 and `MODEL_WEIGHTS` sums to 1.0.
2. For each variable in `VARIABLES`, verify its `evidence_rating` matches what the variable catalog (`literature/variable-catalog.md`) states.
3. In each model file, verify that component weight dictionaries sum to 1.0.
4. Verify `EVIDENCE_WEIGHTS` mapping: Strong=3, Moderate=2, Weak=1.
5. Check that `MODEL_WEIGHTS` is used for scoring and `DOMAIN_WEIGHTS` is used only for display.

**Fix**: Correct any weight sums. Align evidence ratings with the catalog. Add assertions if missing.

## Theoretical Frameworks Reference

Use this reference to verify operationalizations in each model file:

**PSI (Turchin)**: Political Stress = simultaneous MMP x EMP x SFD. Geometric mean is the correct aggregation (all three pressures must co-occur for instability). Source: Turchin (2003, 2023), Goldstone (1991).

**PLI (Kahneman-Tversky)**: Losses from recent peak hurt 2.25x more than equivalent gains. Reference point = recent adaptation level (trailing peak), NOT all-time average. lambda=2.25, alpha=0.88. Source: Kahneman & Tversky (1979), Tversky & Kahneman (1992).

**FSP (Funke et al.)**: Financial stress transmits to political grievance with 5-10 year lag. Transmission should be measured via lagged correlation, not a simple ratio. Source: Funke, Schularick & Trebesch (2016).

**Georgescu SDT**: Weighted average (not multiplicative) for industrialized societies. Elite overproduction = credential surplus / job mismatch (education-job gap), not income concentration. Weights: Elite 0.35, Immiseration 0.40, Fiscal 0.25. Source: Georgescu (2023).

**V-Dem ERT**: For near-ceiling US scores (0.7-0.9 on liberal democracy), trajectory matters more than absolute level. Rate-of-change must use raw (pre-normalized) V-Dem values. A 0.89-to-0.72 decline is significant even though 0.72 is "high" globally. Source: V-Dem Institute, Luhrmann & Lindberg (2019).

## Output Format

Produce a structured report with this format:

```
## Model Review Report

### CRITICAL Issues
(Issues that produce incorrect scores or violate core theory)
- **[Check N: Check Name]** `file.py:line` - Description of what the theory requires vs what the code does. Fix: specific code change needed.

### SERIOUS Issues
(Issues that degrade score quality or introduce systematic bias)
- ...

### MODERATE Issues
(Issues that could cause problems in edge cases or reduce interpretability)
- ...

### No Issues Found
(List checks that passed cleanly)
- Check N: Check Name - passed
```

If no issues are found across all checks, state: "All 8 checks passed. No theory-to-code translation issues detected."
