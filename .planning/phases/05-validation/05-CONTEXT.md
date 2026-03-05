# Phase 5: Validation - Context

**Gathered:** 2026-03-04
**Status:** Ready for planning

<domain>
## Phase Boundary

Determine whether the model(s) produce meaningful signal by testing against historical ground truth. Backtest against historical episodes, quantify uncertainty, test for overfitting and spurious trends, produce pass/fail assessment. This phase does NOT add new models, change weights, or modify the scoring pipeline. It tests what exists.

</domain>

<decisions>
## Implementation Decisions

### Ground Truth Episodes
- Use the 5 calibration anchors (2008, 2020, mid-1990s, 2001, 2011) as "in-sample" validation targets
- Add out-of-sample hold-out episodes that the model was NOT calibrated against:
  - 1960s urban unrest / civil rights era (expect Elevated Tension, 26-50)
  - Watergate / Nixon resignation 1973-74 (expect Elevated Tension or low Crisis, 40-60)
  - Late 1980s stability / end of Cold War (expect Stable, 0-25)
  - 2016 election aftermath (expect Elevated Tension, 35-50)
  - January 6, 2021 (expect Crisis Territory, 51-75)
- Out-of-sample episodes are the real test; in-sample anchors just confirm calibration isn't broken
- If data coverage is too thin for early episodes (1960s), note it but don't fail the model for missing data

### Pass/Fail Criteria
- **Zone accuracy**: Model passes if at least 75% of test episodes (in-sample + out-of-sample combined) land in the correct zone
- **Monotonic ordering**: All crisis-labeled episodes must score strictly higher than all stability-labeled episodes. This is a hard pass/fail gate.
- **Calibration anchor residuals**: Each of the 5 calibration anchors should be within 10 points of target. Warn if >10, fail if >15.
- **Overall verdict**: PASS requires zone accuracy >= 75% AND monotonic ordering holds AND no anchor residual > 15

### Overfitting Safeguards
- **Leave-one-out cross-validation (LOOCV)**: For each of the 5 calibration anchors, refit calibration using the other 4, score the held-out episode. If the held-out score deviates by more than 1 full zone (25 points) from its target, flag overfitting concern.
- **Weight sensitivity analysis**: Perturb each MODEL_WEIGHTS entry by +/-20% (renormalize to sum=1.0), rerun ensemble for current score. If any single perturbation shifts the score by more than 1 zone, the model is fragile.
- **Spurious trend detection**: Check that the historical time series doesn't exhibit implausible patterns (e.g., monotonic increase across all decades, sudden jumps at data boundary years where new variables begin coverage). Visual inspection checklist, not automated.

### Validation Output
- Primary output: a markdown report (`models/VALIDATION.md`) with episode-by-episode results, LOOCV table, sensitivity analysis table, and overall pass/fail verdict
- Console output during run: summary pass/fail and key statistics
- Internal-only: not displayed on the website
- Script: `models/validate.py` runnable via `python models/validate.py` (uses same pipeline as run.py)

### Claude's Discretion
- Exact implementation of the validation script structure
- Whether to use matplotlib for any diagnostic plots (optional, not required)
- How to handle episodes where data coverage is < 50% of variables
- Console output formatting and verbosity level

</decisions>

<specifics>
## Specific Ideas

- The validation should answer one question clearly: "Should we trust this score?"
- The LOOCV on calibration anchors is the strongest overfitting test since the model was explicitly built around those anchors
- Weight sensitivity is important because with only 5 models, small weight changes could have outsized effects
- The out-of-sample episodes should be ones where there's reasonable historical consensus about the level of instability

</specifics>

<code_context>
## Existing Code Insights

### Reusable Assets
- `calibrate.py`: `_fit_calibration()` already does least-squares anchor fitting, can be reused for LOOCV by passing different anchor subsets
- `calibrate.py`: `compute_bootstrap_ci()` already implements the bootstrap, can verify CI coverage
- `ensemble.py`: `compute_ensemble()` returns full history, model outputs, domain scores, everything needed for validation
- `ensemble.py`: `_build_raw_history()` generates the historical time series to test against episodes
- `calibrate.py`: `score_to_zone()` maps scores to zone labels for zone-accuracy checks
- `config.py`: `MODEL_WEIGHTS` dict can be programmatically perturbed for sensitivity analysis
- `run.py`: full pipeline already works end-to-end, validation script can reuse the same data loading

### Established Patterns
- Models follow a registry pattern (`MODEL_REGISTRY` with `@register_model` decorators)
- All scoring goes through `_run_models_on_slice()` for consistency
- Calibration uses `DEFAULT_ANCHORS` list of dicts with date/target/label
- Output files go to `public/data/`, but validation report should go to `models/`

### Integration Points
- `validate.py` will import from `ensemble`, `calibrate`, `pipeline`, `config` (same as `run.py`)
- Can reuse `fetch_all()` with `--cached-only` mode to avoid API calls during validation
- Validation results don't feed into the website; this is a developer-facing quality check

</code_context>

<deferred>
## Deferred Ideas

None. Discussion stayed within phase scope.

</deferred>

---

*Phase: 05-validation*
*Context gathered: 2026-03-04*
