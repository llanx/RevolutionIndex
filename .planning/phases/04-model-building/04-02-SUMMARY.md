---
phase: 04-model-building
plan: 02
subsystem: model-scoring
tags: [python, prospect-theory, structural-demographic, vdem, geometric-mean, loss-aversion, rate-of-change]

# Dependency graph
requires:
  - phase: 04-model-building
    provides: Pipeline config (41 variables), normalization functions (rolling z-score), ModelOutput contract
  - phase: 02-literature-mining
    provides: Framework assessment (Georgescu SDT, V-Dem ERT), variable catalog (45 vars with evidence ratings)
  - phase: 01-prior-work-validation
    provides: Math fix checklist (geometric mean for PSI, K constant correction for PLI, CSCICP03USM665S discontinuation)
provides:
  - 5 stateless scoring model functions (PSI, PLI, FSP, Georgescu SDT, V-Dem ERT)
  - ModelOutput dataclass and ComponentScore dataclass (shared contract)
  - MODEL_REGISTRY dict with register_model decorator for model discovery
  - Phase 1 mathematical corrections applied (geometric mean, K/10, additive bonuses)
  - CSCICP03USM665S weight redistribution (zero-overlap preserved)
affects: [04-03-PLAN, model-validation, pipeline-integration, ensemble-scoring]

# Tech tracking
tech-stack:
  added: []
  patterns: [geometric-mean-composite, prospect-theory-value-function, rate-of-change-analysis, evidence-weighted-component-averaging, model-registry-decorator]

key-files:
  created:
    - models/models.py
    - models/model_psi.py
    - models/model_pli.py
    - models/model_fsp.py
    - models/model_georgescu.py
    - models/model_vdem.py
  modified: []

key-decisions:
  - "PSI uses geometric mean (MMP*EMP*SFD)^(1/3) per Phase 1 critical review A1 fix"
  - "PLI K constants reduced by 10x with additive (not multiplicative) breadth/velocity bonuses per critical review A2"
  - "PLI velocity computed as actual 12-period rate-of-change (fixes implementation review A2 magnitude bug)"
  - "FSP drops CSCICP03USM665S, redistributes weight proportionally: unemployment 0.38, labor share 0.30, inflation 0.22, household debt 0.10"
  - "FSP uses max-based leading-edge aggregation (60% leading + 40% trailing) instead of simple average"
  - "Georgescu SDT uses weighted average (not multiplicative) per Georgescu 2023 empirical approach"
  - "V-Dem ERT uses sigmoid-mapped 5-year rate-of-change for near-ceiling US institutional indicators"

patterns-established:
  - "Model function contract: single pd.DataFrame argument, returns ModelOutput, no side effects"
  - "Component scoring pattern: evidence-weighted average of constituent variables within each component"
  - "Model registry pattern: @register_model('id') decorator populates MODEL_REGISTRY dict"

requirements-completed: [MOD-03]

# Metrics
duration: 8min
completed: 2026-03-04
---

# Phase 04 Plan 02: Model Implementation Summary

**5 stateless scoring models (PSI, PLI, FSP, Georgescu SDT, V-Dem ERT) with Phase 1 mathematical corrections, prospect theory loss aversion, and V-Dem rate-of-change institutional erosion detection**

## Performance

- **Duration:** ~8 min
- **Started:** 2026-03-04T09:52:47Z
- **Completed:** 2026-03-04T10:01:00Z
- **Tasks:** 2/2
- **Files modified:** 6

## Accomplishments
- Implemented all 5 scoring models as stateless pure functions conforming to shared ModelOutput interface
- Applied all Phase 1 mathematical corrections: geometric mean for PSI, corrected K constants for PLI, CSCICP03USM665S weight redistribution for FSP
- Created two new models from Phase 2 literature mining: Georgescu SDT (education-job mismatch elite overproduction proxy) and V-Dem ERT (rate-of-change institutional erosion detection)
- All models verified with synthetic data, producing scores in valid 0-100 range with component breakdowns

## Task Commits

Each task was committed atomically:

1. **Task 1: Create ModelOutput dataclass and implement PSI, PLI, FSP models with Phase 1 fixes** - `ab11678` (feat)
2. **Task 2: Implement Georgescu SDT and V-Dem ERT models** - `faa78db` (feat)

## Files Created/Modified
- `models/models.py` - ModelOutput/ComponentScore dataclasses, MODEL_REGISTRY dict, register_model decorator
- `models/model_psi.py` - Turchin PSI with geometric mean composite and rolling z-score normalization
- `models/model_pli.py` - Prospect Theory PLI with corrected K constants (10x reduction) and additive bonus structure
- `models/model_fsp.py` - Financial Stress Pathway with CSCICP03USM665S dropped and weight redistributed
- `models/model_georgescu.py` - Georgescu SDT using education-job mismatch for elite overproduction (not income concentration)
- `models/model_vdem.py` - V-Dem ERT using 5-year rate-of-change analysis on 6 democratic quality dimensions

## Decisions Made
- **PSI geometric mean:** Applied `(MMP * EMP * SFD)^(1/3)` per critical review A1. Three components at 0.70 now yield 0.70, not 0.343.
- **PLI K constant correction:** Uniform 10x reduction preserves relative domain weighting while preventing saturation. Removed undocumented sqrt compression from original code. Loss score formula is now clean `-V * K` (spec-aligned).
- **PLI velocity fix:** Implemented actual 12-period rate-of-change instead of deviation magnitude proxy (fixes implementation review A2).
- **FSP weight redistribution:** After dropping CSCICP03USM665S (discontinued), redistributed its 0.35 weight proportionally across remaining ETI components (unemployment, labor share, inflation, household debt). Added inflation and household debt as new ETI channels.
- **FSP leading-edge aggregation:** Changed from simple average `(FSSI + ETI) / 2` to max-based leading edge `0.6 * max + 0.4 * min`, improving early-warning capability during financial stress onset.
- **Georgescu weighted average:** Uses correlation-based additive weighting (0.35 elite, 0.40 immiseration, 0.25 fiscal) per Georgescu 2023, not multiplicative like PSI.
- **V-Dem rate-of-change:** Uses sigmoid mapping with scale factor 10.0 calibrated so US 2015-2022 Liberal Democracy decline (~0.17 points) maps to ~0.85 stress.

## Deviations from Plan

None. Plan executed exactly as written.

## Issues Encountered
- Python dependencies (pandas, numpy, scipy) were not installed globally. Installed via pip during execution. Not a blocking issue since models/requirements.txt already documented these dependencies from Plan 01.

## User Setup Required
None beyond what Plan 01 already requires (FRED API key for data pipeline).

## Next Phase Readiness
- Plan 03 (Pipeline Integration) can proceed: all 5 models are registered in MODEL_REGISTRY and accept the unified DataFrame from the pipeline
- All models produce consistent ModelOutput with identical structure, ready for ensemble aggregation
- Domain contributions are tracked per model, enabling the inter-model correlation analysis planned for Phase 5 validation

## Self-Check: PASSED

All created files exist (6/6). Both task commits found (ab11678, faa78db). SUMMARY.md exists.

---
*Phase: 04-model-building*
*Completed: 2026-03-04*
