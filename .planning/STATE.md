---
gsd_state_version: 1.0
milestone: v1.0
milestone_name: milestone
status: unknown
last_updated: "2026-03-05T02:51:45.482Z"
progress:
  total_phases: 5
  completed_phases: 5
  total_plans: 19
  completed_plans: 19
---

---
gsd_state_version: 1.0
milestone: v1.0
milestone_name: milestone
status: in-progress
last_updated: "2026-03-05T01:59:00Z"
progress:
  total_phases: 5
  completed_phases: 4
  total_plans: 19
  completed_plans: 18
---

# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-03-01)

**Core value:** Produce a defensible, data-backed revolution probability score from freely available data -- one number that synthesizes what academic research says matters.
**Current focus:** Phase 5 IN PROGRESS (2/3 plans complete). Core validation and diagnostic analyses complete. Next: Plan 05-03 (validation report generation).

## Current Position

Phase: 5 of 5 (Model Validation) -- IN PROGRESS
Plan: 2 of 3 in current phase (Diagnostic Analyses complete)
Status: Plan 05-02 COMPLETE. Weight sensitivity, inter-model correlation, spurious trend detection added to validate.py. History-only mode works. Next: 05-03 report generation.
Last activity: 2026-03-05 -- Diagnostic analyses: weight sensitivity, inter-model correlation, spurious trend detection.

Progress: [█████████░] 95%

## Performance Metrics

**Velocity:**
- Total plans completed: 17
- Average duration: 12min
- Total execution time: 3.01 hours

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 1 - Prior Work Validation | 3 | 43min | 14min |
| 2 - Literature Mining | 6 | 51min | 9min |
| 3 - Data Sourcing | 3 | 24min | 8min |
| 4 - Model Building | 4/4 | 64min | 16min |
| 5 - Validation | 2/3 | 8min | 4min |

**Recent Trend:**
- Last 5 plans: 05-02 (4min), 05-01 (4min), 04-04 (2min), 04-03 (9min), 04-02 (8min)
- Trend: Phase 5 plans fast -- extending standalone validation script

*Updated after each plan completion*
| Phase 03 P01 | 1 | 1 tasks | 1 files |
| Phase 03 P02 | 1 | 2 tasks | 1 files |
| Phase 03 P03 | 1 | 2 tasks | 1 files |
| Phase 04 P01 | 1 | 2 tasks | 13 files |
| Phase 04 P02 | 1 | 2 tasks | 6 files |
| Phase 04 P03 | 1 | 2 tasks | 8 files |
| Phase 04 P04 | 1 | 1 tasks | 3 files |
| Phase 05 P01 | 1 | 2 tasks | 1 files |
| Phase 05 P02 | 1 | 2 tasks | 1 files |

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
- [04-01]: 5-model evidence-weighted ensemble selected: PSI 0.25, PLI 0.20, FSP 0.15, Georgescu SDT 0.25, V-Dem ERT 0.15
- [04-01]: Rolling z-score normalization (20yr window) chosen over min-max to avoid Phase 1 pinning bug
- [04-01]: Domain weights: Economic Stress 0.30, Political Polarization 0.22, Institutional Quality 0.20, Social Mobilization 0.18, Information & Media 0.10
- [04-01]: Variable #39 (Neighborhood/Diffusion Effects) assigned to INSTITUTIONAL_QUALITY domain
- [04-01]: Factor IDs migrated across entire codebase to 5-domain taxonomy: economic_stress, political_polarization, institutional_quality, social_mobilization, information_media
- [04-01]: current.json and factors.json demo data IDs updated for cross-reference consistency (Astro pages join on factor ID across benchmark and current data)
- [04-02]: PSI uses geometric mean (MMP*EMP*SFD)^(1/3) per Phase 1 critical review A1 fix
- [04-02]: PLI K constants reduced 10x with additive bonuses; velocity bug fixed with actual rate-of-change computation
- [04-02]: FSP drops CSCICP03USM665S, redistributes weight to unemployment 0.38, labor share 0.30, inflation 0.22, household debt 0.10
- [04-02]: FSP uses max-based leading-edge aggregation (60/40) instead of simple average for better early warning
- [04-02]: Georgescu SDT uses weighted average (not multiplicative) per Georgescu 2023 empirical approach for developed economies
- [04-02]: V-Dem ERT uses sigmoid-mapped 5-year rate-of-change for near-ceiling US institutional indicators
- [04-03]: Linear calibration using two anchor classes: crisis (2008/2020 avg -> 65) and stable (1994-1997 avg -> 20)
- [04-03]: Bootstrap CIs resample variables within each domain (not composite perturbation) for correct uncertainty propagation
- [04-03]: History sampling: annual pre-2000, quarterly post-2000 for manageable file size covering all 6 Phase 5 validation episodes
- [04-03]: Column naming bridge in ensemble.py handles pipeline-to-model column format difference
- [04-04]: MIN_DOMAINS_REQUIRED=2 chosen as threshold for _build_raw_history() -- at least 2 of 5 domains must have valid data
- [04-04]: Leading zeros (1960-1978) removed from history.json; interior zeros left as-is for next real pipeline run
- [04-04]: Bootstrap CI n updated from 100 to 1000 in committed JSON -- data artifact from test run, not code bug
- [Phase 04]: Model building complete -- 5 models, ensemble scoring, calibration, bootstrap CIs, JSON output all automated via `python models/run.py`. Gap closure (04-04) fixed bootstrap n and history zeros.
- [05-01]: History-only validation mode reads history.json directly (no pipeline run needed), enabling validation without FRED API keys
- [05-01]: Strict vs lenient zone accuracy: 50% strict (4/8 correct zone), 87.5% lenient (7/8 within 3 points of correct boundary)
- [05-01]: All zone misses are near-boundary (within 3-4 points), suggesting calibration refinement rather than fundamental model issues
- [05-01]: 2016 election scores 54 (Crisis Territory, expected Elevated Tension): genuine model finding, not a bug
- [05-02]: Weight sensitivity in history-only mode reports theoretical max bounds (too conservative to trigger 25-point threshold), actual re-run requires --full mode
- [05-02]: Spurious trend detection found 1989 data boundary jump (+12.7 points when WFRBSTP1300 starts) and 1982 score saturation at 0 (known data availability artifacts)
- [05-02]: Inter-model correlation analysis skipped in history-only mode since per-model scores require the full pipeline

### Pending Todos

None yet.

### Blockers/Concerns

- User needs a FRED API key (free) before data pipeline work in Phase 4
- Phase 2 complete -- Phases 3-5 can now be planned based on synthesis recommendations

## Session Continuity

Last session: 2026-03-05
Stopped at: Completed 05-02-PLAN.md (Diagnostic Analyses). Phase 5 in progress (2/3 plans). Next: 05-03 (Validation Report).
Resume file: None
