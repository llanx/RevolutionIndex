---
phase: 05-validation
plan: 02
subsystem: testing
tags: [validation, sensitivity-analysis, correlation, spurious-trends, diagnostics]

# Dependency graph
requires:
  - phase: 05-validation plan 01
    provides: "Core validate.py with episode backtesting, LOOCV, CI width check"
  - phase: 04-model-building
    provides: "5 model ensemble, MODEL_WEIGHTS config, history.json"
provides:
  - "Weight sensitivity analysis (theoretical bounds in history-only, actual in --full)"
  - "Inter-model correlation check (--full mode only)"
  - "Spurious trend detection (monotonic, boundary jumps, saturation, decade summary)"
  - "validation_results dict with all diagnostic keys for report generation"
affects: [05-validation plan 03]

# Tech tracking
tech-stack:
  added: []
  patterns: ["History-only vs full-mode diagnostic pattern", "Theoretical bound computation for weight perturbation"]

key-files:
  created: []
  modified: [models/validate.py]

key-decisions:
  - "Weight sensitivity in history-only mode reports theoretical max shift bounds, labeled as SKIPPED since bounds are too conservative to be meaningful"
  - "Inter-model correlation gracefully skips in history-only mode since per-model scores are unavailable"
  - "Data boundary jump threshold set at 10 points within 2-year window"
  - "Score saturation threshold set at > 3 consecutive entries at 0 or 100"

patterns-established:
  - "Diagnostic functions return structured dicts for programmatic report generation"
  - "Print functions separated from logic functions for testability"

requirements-completed: [TEST-04, TEST-05, TEST-06]

# Metrics
duration: 4min
completed: 2026-03-05
---

# Phase 5 Plan 02: Diagnostic Analyses Summary

**Weight sensitivity, inter-model correlation, and spurious trend detection added to validate.py with history-only and --full mode support**

## Performance

- **Duration:** 4 min
- **Started:** 2026-03-05T02:04:06Z
- **Completed:** 2026-03-05T02:07:43Z
- **Tasks:** 2
- **Files modified:** 1

## Accomplishments
- Weight sensitivity analysis computes theoretical max shift bounds in history-only mode and actual perturbed scores in --full mode
- Inter-model correlation check compares all 10 pairwise model score combinations in --full mode
- Spurious trend detection performs 4 automated checks: monotonic increase, data boundary jumps, score saturation, decade-level summary
- All diagnostic results stored in validation_results dict with keys for Plan 05-03 report generation
- Spurious trend detection found 2 flags: 1989 data boundary jump (+12.7 points) and score saturation at 0 in 1982

## Task Commits

Each task was committed atomically:

1. **Task 1: Add weight sensitivity, inter-model correlation, and spurious trend detection** - `a259cd8` (feat)
2. **Task 2: Run full validation and verify diagnostic output** - verification only, no code changes

## Files Created/Modified
- `models/validate.py` - Added 3 diagnostic functions (run_weight_sensitivity, check_inter_model_correlation, check_spurious_trends), 3 print functions, updated main() to call all diagnostics

## Decisions Made
- Weight sensitivity in history-only mode uses theoretical maximum shift formula: |S * (f-1) * w_M / (1 + (f-1)*w_M)|. Labeled as SKIPPED since the theoretical ceiling (~3-4 points) is too small to ever trigger the 25-point fragility threshold.
- Inter-model correlation skipped in history-only mode with clear message, since per-model scores require the full pipeline.
- Data boundary years from RESEARCH.md (1989, 1993, 2000, 2005, 2017, 2020) used as detection points.
- Overall concern level uses 3-tier system: none (0 flags), minor (1-2 flags), major (3+ flags).

## Deviations from Plan

None. Plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None. No external service configuration required.

## Next Phase Readiness
- validate.py now contains the complete validation battery: episode backtesting, LOOCV, CI width, weight sensitivity, inter-model correlation, spurious trend detection
- validation_results dict is fully structured for Plan 05-03 report generation
- Spurious trend detection found expected results: 1989 data boundary jump and early-1980s saturation at 0 are known artifacts of data availability, not bugs

---
*Phase: 05-validation*
*Completed: 2026-03-05*
