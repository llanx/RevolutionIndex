# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-03-01)

**Core value:** Produce a defensible, data-backed revolution probability score from freely available data -- one number that synthesizes what academic research says matters.
**Current focus:** Phase 2 in progress: Literature Mining (Wave 1 domain reviews complete, Wave 2 next).

## Current Position

Phase: 2 of 5 (Literature Mining) -- IN PROGRESS
Plan: 4 of 6 in current phase (4 complete -- Wave 1 domain reviews + variable catalog)
Status: Phase 2 In Progress -- Variable Catalog Complete, Framework Assessment Next
Last activity: 2026-03-04 -- Variable catalog (Plan 04) complete. 45 ranked variables from 6 domain reviews.

Progress: [█████░░░░░] 50%

## Performance Metrics

**Velocity:**
- Total plans completed: 7
- Average duration: 11min
- Total execution time: 1.30 hours

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 1 - Prior Work Validation | 3 | 43min | 14min |
| 2 - Literature Mining | 4 | 35min | 9min |

**Recent Trend:**
- Last 5 plans: 02-04 (9min), 02-01 (9min), 02-02 (9min), 02-03 (8min), 01-03 (14min)
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
- [02-01]: Georgescu (2023) education-job mismatch identified as potentially better EMP proxy than top 1% income share for US context
- [02-01]: Affective polarization (not ideological) is the most consistently cited predictor of democratic backsliding across 16 comparative cases
- [02-01]: No post-2023 Turchin PSI operationalization update found -- Phase 1 Open Question #1 resolved
- [02-01]: PITF regime type predictor now directly debated for the US (Walter 2022 vs. Svolik 2019) -- included as Tier 2 applicability
- [02-01]: State-level disaggregation (Grumbach) captures US democratic variation that national-level measures miss
- [02-01]: 40 variables extracted across revolution prediction (20) and democratic backsliding (20) domains for variable catalog
- [02-02]: Military loyalty (strongest global revolution predictor) classified as Not Applicable for US -- stable civilian control
- [02-02]: Housing affordability identified as US analog to food price triggers in historical revolutions
- [02-02]: Funke et al. (2016) confirmed as strongest empirical economic-to-political transmission mechanism (financial crisis -> 30% far-right vote increase, 5-10 year lag)
- [02-02]: Rolling z-scores recommended over min-max normalization for trending US macroeconomic series
- [02-02]: 33 variables extracted across both reviews (13 historical + 20 economic) for variable catalog
- [02-04]: 45 concept-level variables cataloged from ~95 raw discoveries, with evidence ratings (14 Strong, 21 Moderate, 10 Weak) and data availability tags (18 fed-data, 21 other-data, 6 unknown)
- [02-04]: 4 variables marked Contested: Income/Wealth Inequality, State Fiscal Distress, Regime Type, and several media/information variables
- [02-04]: 5 theoretically important variables excluded by measurability filter; 7 excluded as not applicable to US
- [02-04]: Wealth Concentration (Top 0.1%) treated as separate from general inequality -- captures qualitatively different elite capture dynamics
- [02-04]: Housing affordability included as standalone variable -- US analog to historical food price triggers
- [02-04]: Data availability without MCP: tags assigned from domain review knowledge and 02-RESEARCH.md coverage map; to be verified in Phase 3

### Pending Todos

None yet.

### Blockers/Concerns

- User needs a FRED API key (free) before data pipeline work in Phase 4
- Literature mining (Phase 2) may significantly change the model landscape -- Phases 3-5 plans should not be detailed until Phase 2 completes

## Session Continuity

Last session: 2026-03-04
Stopped at: Completed 02-04-PLAN.md (Variable Catalog). 45 ranked variables cataloged. Plans 05 (Framework Assessment) and 06 (Synthesis) remain in Phase 2.
Resume file: None
