---
gsd_state_version: 1.0
milestone: v1.1
milestone_name: Build & Validate
status: in-progress
last_updated: "2026-03-03T00:00:00Z"
progress:
  total_phases: 0
  completed_phases: 0
  total_plans: 0
  completed_plans: 0
---

# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-03-03)

**Core value:** Produce a defensible, data-backed revolution probability score from freely available data -- one number that synthesizes what academic research says matters.
**Current focus:** Milestone v1.1 started -- defining requirements for model building and validation.

## Current Position

Phase: Not started (defining requirements)
Plan: —
Status: Defining requirements
Last activity: 2026-03-03 — Milestone v1.1 started

## Performance Metrics

**Velocity:**
- Total plans completed: 12
- Average duration: 10min
- Total execution time: 1.88 hours

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 1 - Prior Work Validation | 3 | 43min | 14min |
| 2 - Literature Mining | 6 | 51min | 9min |
| 3 - Data Sourcing | 3 | 24min | 8min |

**Recent Trend:**
- Last 5 plans: 03-03 (11min), 03-02 (8min), 03-01 (5min), 02-06 (6min), 02-05 (10min)
- Trend: stable (data sourcing averaging 8min/plan)

*Updated after each plan completion*
| Phase 03 P01 | 1 | 1 tasks | 1 files |
| Phase 03 P02 | 1 | 2 tasks | 1 files |
| Phase 03 P03 | 1 | 2 tasks | 1 files |

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
- [02-05]: Georgescu SDT and V-Dem ERT strongly recommended for Phase 4 -- best data availability and US applicability among 9 candidate frameworks
- [02-05]: Collier-Hoeffler greed/grievance model not recommended -- core mechanism (resource financing) inapplicable to US
- [02-05]: Phase 1 Open Questions #6 (frameworks beyond 3 models) and #7 (sensitivity analysis methods) definitively addressed
- [02-05]: V-Dem ranked as #1 dataset for project utility (1789-present, 483 indicators, comprehensive US coding)
- [02-05]: ACLED ranked as #2 for real-time US monitoring (2020-present, 30K+ events); ANES #3 for attitudinal validation
- [02-05]: Zero-event constraint requires multi-source validation strategy: sub-crisis backtesting, cross-national thresholds, financial crisis calibration, attitudinal corroboration
- [02-05]: COINr sensitivity analysis (Morris screening + Sobol indices) recommended for composite indicators with 50+ parameters
- [02-06]: Existing 3 models cover only 12 of 45 variables (27%) -- institutional/democratic quality dimension entirely uncovered; Phase 4 should add this dimension
- [02-06]: Georgescu SDT education-job mismatch proxy recommended as more theoretically faithful elite overproduction measure than top 1% income share
- [02-06]: Morris screening + Sobol indices recommended as 3-step sensitivity analysis protocol for 50+ parameter composite indicators
- [02-06]: Multi-source validation strategy formalized: sub-crisis backtesting (7 episodes), cross-national thresholds, financial crisis calibration, attitudinal corroboration
- [02-06]: Information/media variables have widest gap between perceived importance and empirical evidence (all 6 Weak-rated or Contested)
- [02-06]: Economic variables have strongest evidence (7/13 Strong) and best data availability (11/13 fed-data)
- [Phase 02]: Existing 3 models cover only 27% of 45 discovered variables -- institutional/democratic quality dimension entirely uncovered
- [03-01]: CSCICP03USM665S handling: drop weight from FSP ETI and redistribute (not UMCSENT to preserve zero-overlap, not Conference Board CCI which is paid)
- [03-01]: PRS85006173 recommended for labor share (nonfarm business sector, more commonly cited than GDP-based W270RE1A156NBEA)
- [03-01]: TDSP recommended for household debt (debt service ratio 1980-present, measures burden not just level, better than HDTGPDUSQ163N which starts 2005)
- [03-01]: Georgescu education-job mismatch proxy documented with construction recipe; WID top 1% income share as fallback with longer history
- [03-01]: FIXHAI recommended for housing affordability (composite of prices, rates, and income in single index)
- [03-01]: STLFSI4 confirmed as correct financial stress index version (STLFSI/2/3 superseded, TEDRATE discontinued)
- [03-02]: VoteView DW-NOMINATE party mean distance recommended as gold standard for congressional polarization (#3, 1789-present)
- [03-02]: ANES feeling thermometer difference (VCF0218/VCF0224) recommended for affective polarization (#4) despite biennial frequency
- [03-02]: Intra-party DW-NOMINATE SD recommended as constructible proxy for elite factionalism (#11)
- [03-02]: Fed DFA (WFRBSTP1300/WFRBST01134) recommended over WID for intra-elite wealth gap (#19) due to quarterly frequency
- [03-02]: Anti-system party vote share (#31) requires Phase 4 coding decision -- no pre-built anti-system classification dataset exists
- [03-02]: V-Dem v2x_libdem recommended as primary institutional quality measure with rate-of-change analysis for near-ceiling US context
- [03-02]: V-Dem near-ceiling limitation documented for all institutional variables -- trends more informative than absolute levels
- [03-02]: World Bank WGI Government Effectiveness (GE.EST) recommended for state capacity (#38) via MCP tool
- [03-02]: Polity V explicitly excluded as deprecated (final version 2018) -- V-Dem v15 is current standard
- [03-03]: ANES VCF0604 recommended as primary government trust measure (#7) over Pew -- most standardized methodology
- [03-03]: ACLED US data as primary protest source (#12) with explicit 2020-present coverage limitation
- [03-03]: BLS annual news release as primary union membership source (#25) -- no API series exists
- [03-03]: BLS LNS14000012/LNS14000036 recommended for youth unemployment (#26) -- monthly frequency, 1948-present
- [03-03]: 4 variables classified Unavailable (#33, #35, #43, #44) -- all weak-rated, genuine measurement gaps
- [03-03]: Inventory complete: 15 free API + 20 manual download + 6 proxy needed + 4 unavailable = 45 total
- [03-03]: 25 unique data sources cataloged; all unavailable variables are weak-rated (no strong variable lacks data)
- [Phase 03]: Data source inventory complete -- all 45 variables mapped, 91% measurable, ready for Phase 4

### Pending Todos

None yet.

### Blockers/Concerns

- User needs a FRED API key (free) before data pipeline work in Phase 4
- Phase 2 complete -- Phases 3-5 can now be planned based on synthesis recommendations

## Session Continuity

Last session: 2026-03-04
Stopped at: Completed 03-03-PLAN.md (Social/Information Domains + Inventory Completion). Phase 3 complete -- all 45 variables sourced, inventory finalized with Availability Matrix, Gap Analysis, and Source Registry. Ready for Phase 4 planning.
Resume file: None
