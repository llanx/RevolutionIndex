---
phase: 04-model-building
plan: 01
subsystem: model-infrastructure
tags: [python, pipeline, normalization, fred-api, ensemble-model, data-contract]

# Dependency graph
requires:
  - phase: 02-literature-mining
    provides: Variable catalog (45 vars), framework assessment (9 frameworks), synthesis recommendations
  - phase: 03-data-sourcing
    provides: Data source inventory (41 measurable variables with series IDs, frequencies, coverage windows)
provides:
  - Architecture selection document explaining 5-model evidence-weighted ensemble
  - Variable-to-source config mapping all 41 measurable variables to FRED/manual/constructed sources
  - Rolling z-score normalization functions (avoiding min-max pinning bug)
  - Data pipeline with FRED fetch, LOCF alignment, caching, and freshness tracking
  - Updated BenchmarkFactorId type with 5-domain factor IDs across all data files
affects: [04-02-PLAN, 04-03-PLAN, model-validation, pipeline-automation]

# Tech tracking
tech-stack:
  added: [pandas, numpy, scipy, fredapi, openpyxl]
  patterns: [rolling-zscore-normalization, evidence-weighted-aggregation, LOCF-frequency-alignment, domain-based-factor-grouping]

key-files:
  created:
    - models/README.md
    - models/config.py
    - models/pipeline.py
    - models/normalize.py
    - models/requirements.txt
  modified:
    - src/lib/data.ts
    - public/data/benchmarks.json
    - public/data/factions.json
    - public/data/policies.json
    - public/data/current.json
    - public/data/factors.json
    - src/pages/index.astro
    - src/pages/history.astro

key-decisions:
  - "Rolling z-score (20yr window) chosen over min-max normalization to avoid pinning bug from Phase 1 PSI assessment"
  - "Variable #39 (Neighborhood/Diffusion Effects) assigned to INSTITUTIONAL_QUALITY domain as it uses V-Dem allied democracies data"
  - "current.json and factors.json factor IDs updated alongside BenchmarkFactorId for cross-reference consistency, even though plan said pipeline-generated (demo data must match for build to pass)"
  - "Evidence-weighted domain aggregation: Strong=3, Moderate=2, Weak=1 within each domain"
  - "Domain weights: Economic Stress 0.30, Political Polarization 0.22, Institutional Quality 0.20, Social Mobilization 0.18, Information & Media 0.10"

patterns-established:
  - "Domain-based factor grouping: all 5 factor IDs (economic_stress, political_polarization, institutional_quality, social_mobilization, information_media) used consistently across data.ts, all JSON files, and Astro pages"
  - "Pipeline config pattern: dataclass-based Variable definitions in config.py with validation at import time"
  - "Normalization pattern: rolling z-score with CDF mapping to 0.0-1.0, percentile-rank fallback for short series"

requirements-completed: [MOD-01, MOD-02]

# Metrics
duration: 45min
completed: 2026-03-04
---

# Phase 04 Plan 01: Architecture Selection and Pipeline Infrastructure Summary

**5-model evidence-weighted ensemble architecture with 41-variable data pipeline using rolling z-score normalization and FRED API integration, plus full factor ID migration to 5-domain taxonomy**

## Performance

- **Duration:** ~45 min (across two sessions due to context limit)
- **Started:** 2026-03-04T01:00:00Z
- **Completed:** 2026-03-04T01:47:00Z
- **Tasks:** 2/2
- **Files modified:** 13

## Accomplishments
- Created complete model architecture selection document (MOD-01) documenting why the 5-model ensemble was chosen, with literature-backed rationale tying to Phase 2 findings
- Implemented full data pipeline infrastructure: 41-variable config, FRED API fetching, LOCF alignment, rolling z-score normalization, evidence-weighted domain aggregation
- Migrated all factor IDs across the entire codebase from old names (economic_inequality, protest_intensity, institutional_trust, unemployment_stress) to new 5-domain taxonomy (economic_stress, social_mobilization, institutional_quality, information_media)

## Task Commits

Each task was committed atomically:

1. **Task 1: Create architecture selection document, pipeline config, and Python infrastructure** - `c340d14` (feat)
2. **Task 2: Update data.ts BenchmarkFactorId and all downstream JSON/Astro files** - `8d6f60e` (feat)

## Files Created/Modified
- `models/README.md` - Architecture selection document: 5-model ensemble rationale, variable coverage, domain groupings, calibration approach
- `models/config.py` - Variable configuration: 41 Variable entries with domain, source type, series ID, evidence rating, normalization direction
- `models/pipeline.py` - Data pipeline: FRED fetch, manual source loading, proxy construction, LOCF alignment, freshness tracking
- `models/normalize.py` - Normalization: rolling z-score (20yr window), CDF mapping, percentile-rank fallback
- `models/requirements.txt` - Python dependencies: pandas, numpy, scipy, requests, fredapi, openpyxl
- `src/lib/data.ts` - Updated BenchmarkFactorId to 5 new domain IDs
- `public/data/benchmarks.json` - Updated factor keys and notes for all 8 historical benchmarks
- `public/data/factions.json` - Updated factorAlignment primary/secondary for all 8 factions
- `public/data/policies.json` - Updated factor IDs and names for all 5 policy entries
- `public/data/current.json` - Updated factor IDs and names (deviation: demo data consistency)
- `public/data/factors.json` - Updated factor IDs, names, and descriptions (deviation: demo data consistency)
- `src/pages/index.astro` - Updated all factor ID references in comparison logic
- `src/pages/history.astro` - Updated factorMeta array and comparison logic

## Decisions Made
- **Rolling z-score over min-max:** Phase 1 PSI assessment identified min-max normalization as causing a "pinning bug" where extreme values distort the entire scale. Rolling z-score with CDF mapping avoids this.
- **Variable #39 domain assignment:** The data source inventory listed "Neighborhood/Diffusion Effects" as a standalone variable. Assigned to INSTITUTIONAL_QUALITY because it uses V-Dem data measuring democratic quality of allied nations, which is an institutional measurement.
- **Demo data ID update:** Plan said to leave current.json/factors.json unchanged (pipeline-generated), but index.astro cross-references benchmarks factor keys with current.json factor IDs. Updated demo data IDs so the build passes.
- **Evidence-weighted domain weights:** Economic Stress gets highest weight (0.30) due to 7 Strong-rated variables. Information & Media gets lowest (0.10) due to 0 Strong-rated variables and only 1 measurable variable after dropping 3 unavailable.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] config.py had 40 variables instead of 41**
- **Found during:** Task 1 (config.py creation)
- **Issue:** Variable #39 (Neighborhood/Diffusion Effects, Allied Democracies) was listed as "Standalone Variable" in the inventory, not assigned to any domain
- **Fix:** Added #39 to INSTITUTIONAL_QUALITY domain (uses V-Dem data measuring allied democracy quality)
- **Files modified:** models/config.py
- **Verification:** `python -c "import config; assert len(config.VARIABLES) == 41"` passes
- **Committed in:** c340d14 (Task 1 commit)

**2. [Rule 3 - Blocking] Astro pages referenced old factor IDs, breaking the build**
- **Found during:** Task 2 (after updating data.ts and JSON files)
- **Issue:** index.astro and history.astro contained hardcoded references to old factor IDs (economic_inequality, institutional_trust, protest_intensity, unemployment_stress) used for cross-referencing benchmarks with current data
- **Fix:** Updated both Astro pages to use new domain IDs. Also updated current.json and factors.json factor IDs for cross-reference consistency.
- **Files modified:** src/pages/index.astro, src/pages/history.astro, public/data/current.json, public/data/factors.json
- **Verification:** `npm run build` passes, `grep` confirms no old IDs remain
- **Committed in:** 8d6f60e (Task 2 commit)

---

**Total deviations:** 2 auto-fixed (1 bug, 1 blocking)
**Impact on plan:** Both fixes necessary for correctness. No scope creep. The domain assignment and ID consistency changes are required for the codebase to function.

## Issues Encountered
- Context window exhaustion required session continuation. All Task 1 work was committed before context limit. Task 2 was completed in the continuation session.

## User Setup Required
- **FRED API Key:** To run the pipeline, obtain a free API key from https://fred.stlouisfed.org/docs/api/api_key.html and set as environment variable `FRED_API_KEY`
- **Python dependencies:** Run `pip install -r models/requirements.txt` to install pipeline dependencies

## Next Phase Readiness
- Plan 02 (Model Implementation) can proceed: pipeline infrastructure is in place, config maps all 41 variables, normalization functions are ready
- Plan 03 (Pipeline Integration) can proceed: fetch_all() and compute_domain_scores() are implemented and ready to produce JSON output
- All 5 domain IDs are consistent across the entire codebase, so model output will integrate cleanly with the frontend

## Self-Check: PASSED

All created files exist (5/5). All modified files exist (8/8). Both task commits found (c340d14, 8d6f60e). SUMMARY.md exists.

---
*Phase: 04-model-building*
*Completed: 2026-03-04*
