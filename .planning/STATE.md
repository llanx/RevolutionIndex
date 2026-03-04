# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-03-01)

**Core value:** Produce a defensible, data-backed revolution probability score from freely available data -- one number that synthesizes what academic research says matters.
**Current focus:** Phase 2 in progress: Literature Mining (adjacent domain reviews complete).

## Current Position

Phase: 2 of 5 (Literature Mining) -- IN PROGRESS
Plan: 3 of 6 in current phase (3 complete)
Status: Phase 2 In Progress
Last activity: 2026-03-04 -- Completed 02-03-PLAN.md (Adjacent Domain Literature Reviews)

Progress: [████░░░░░░] 33%

## Performance Metrics

**Velocity:**
- Total plans completed: 4
- Average duration: 13min
- Total execution time: 0.85 hours

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 1 - Prior Work Validation | 3 | 43min | 14min |
| 2 - Literature Mining | 1 | 8min | 8min |

**Recent Trend:**
- Last 5 plans: 02-03 (8min), 01-03 (14min), 01-02 (4min), 01-01 (25min)
- Trend: stable

*Updated after each plan completion*

## Accumulated Context

### Decisions

Decisions are logged in PROJECT.md Key Decisions table.
Recent decisions affecting current work:

- [Roadmap]: V1 scope is research + validated models, NOT dashboard (dashboard deferred to v2)
- [Roadmap]: Models are not locked in -- literature mining in Phase 2 may change which models get built
- [Roadmap]: 5-phase structure follows natural dependency chain: validate -> mine literature -> source data -> build models -> validate models
- [01-03]: PLI identified as most validated model; FSP most novel theory but weakest implementation; PSI most critical bug (normalization pinning)
- [01-03]: 3-model selection confirmed as still valid -- no issues fundamentally invalidate any model
- [01-03]: All three models implement significantly fewer variables than spec (pragmatic FRED-only constraint)
- [01-03]: 5 honest limitations of validation documented (no models run, no data downloaded, no academic verification, no backtesting, single reviewer)
- [01-02]: CSCICP03USM665S classified as DISCONTINUED -- needs replacement in Phase 3, recommended against UMCSENT to preserve zero-overlap design
- [01-02]: DRSFRMACBS classified as CHANGED due to 2023 MBA methodology revision -- level adjustment may be needed in Phase 4
- [01-02]: WID sptinc992j classified as UNVERIFIED (method risk, not data risk) -- API test needed in Phase 3
- [01-01]: Min-max normalization bug (impl A1) is the most critical open issue -- pins 2 of 3 PSI components near 1.0
- [01-01]: PLI has undocumented sqrt+*10 transformation beyond critical review scope -- needs empirical backtesting
- [01-01]: FSP config/code ETI weight divergence (6 config vs. 4 code series) is a maintenance hazard
- [01-01]: Of 27 total critical review issues: 4 resolved, 18 open (Phase 4), 5 deferred (non-selected models)
- [02-03]: Protest frequency and union density identified as most directly measurable US mobilization variables (ACLED, BLS)
- [02-03]: DW-NOMINATE congressional polarization identified as strongest media/info domain variable -- exceptional data quality (1789-present)
- [02-03]: Survey problem flagged -- most media/information variables are periodic surveys, not continuous time-series, limiting backtesting utility
- [02-03]: 22 adjacent-domain variables discovered (12 social movement + 10 media/info) for variable catalog

### Pending Todos

None yet.

### Blockers/Concerns

- User needs a FRED API key (free) before data pipeline work in Phase 4
- Literature mining (Phase 2) may significantly change the model landscape -- Phases 3-5 plans should not be detailed until Phase 2 completes

## Session Continuity

Last session: 2026-03-04
Stopped at: Completed 02-03-PLAN.md (Adjacent Domain Literature Reviews). Phase 2 plans 01-03 in parallel Wave 1.
Resume file: None
