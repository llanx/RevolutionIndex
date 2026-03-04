---
phase: 02-literature-mining
plan: 01
subsystem: research
tags: [literature-review, revolution-prediction, democratic-backsliding, variable-extraction, political-science]

# Dependency graph
requires:
  - phase: 01-prior-work-validation
    provides: "Validation report with 7 open questions, 3 model assessments, and 18 data series audit"
provides:
  - "Revolution prediction literature review with 20 extracted variables and 45 sources"
  - "Democratic backsliding literature review with 20 extracted variables and 42 sources"
  - "Phase 1 Open Question #1 addressed (Turchin PSI operationalizations since End Times)"
  - "4 candidate frameworks identified for Plan 05 assessment (PITF, V-Dem ERT, FSI, Grumbach)"
affects: [02-04-variable-catalog, 02-05-framework-assessment, 02-06-synthesis]

# Tech tracking
tech-stack:
  added: []
  patterns: [domain-literature-review-pattern, author-year-citation-style, us-applicability-three-tier-assessment]

key-files:
  created:
    - literature/01-revolution-prediction.md
    - literature/02-democratic-backsliding.md
  modified: []

key-decisions:
  - "Georgescu (2023) education-job mismatch may be better EMP proxy than top 1% income share for US context"
  - "PITF model regime type predictor becoming relevant to US as scholars debate anocracy classification"
  - "Affective polarization (not ideological) is the most consistently cited predictor of democratic backsliding"
  - "State-level analysis (Grumbach) captures US democratic variation that national-level measures miss"
  - "No post-2023 Turchin PSI operationalization update found; simplified 3-proxy approach remains current"

patterns-established:
  - "Pattern 1 Domain Literature Review: Scope -> Foundational Works -> Core Empirical Studies -> Recent Developments -> Variables Discovered -> Key Debates -> US Applicability -> Bibliography"
  - "Three-tier US applicability: directly applicable, applicable with adaptation, not applicable"
  - "Variables Discovered table format: Variable | Measurement/Proxy | Studies | Direction | Notes"

requirements-completed: [LIT-01, LIT-02]

# Metrics
duration: 9min
completed: 2026-03-04
---

# Phase 2 Plan 01: Core Domain Literature Reviews Summary

**Exhaustive literature reviews for revolution prediction (5 generations, 45 sources, 20 variables) and democratic backsliding (state failure models, democratic erosion theory, 42 sources, 20 variables) with US applicability assessments and candidate framework identification**

## Performance

- **Duration:** 9 min
- **Started:** 2026-03-04T01:13:39Z
- **Completed:** 2026-03-04T01:23:34Z
- **Tasks:** 2
- **Files created:** 2

## Accomplishments

- Revolution prediction literature review covering all 5 generations of revolution studies (1920s-2025), from Brinton's natural histories through Turchin's structural-demographic theory to Korotayev's 5th-generation ML approaches, extracting 20 measurable variables with direction of effect and US applicability classification
- Democratic backsliding literature review covering institutional erosion theory (Linz, Bermeo, Levitsky-Ziblatt), quantitative state failure models (PITF, V-Dem ERT, FSI), and US-specific research (Grumbach state-level backsliding, McCoy-Somer pernicious polarization), extracting 20 measurable variables
- Phase 1 Open Question #1 definitively addressed: no post-End Times PSI operationalization update found; Georgescu (2023) is the most relevant technical extension
- Four candidate frameworks surfaced for Plan 05 detailed assessment: PITF global forecasting model, V-Dem Episodes of Regime Transformation, Fragile States Index methodology, Grumbach state-level democracy index

## Task Commits

Each task was committed atomically:

1. **Task 1: Revolution prediction literature review** - `cbd4896` (feat)
2. **Task 2: Democratic backsliding and state failure literature review** - `d848b2d` (feat)

## Files Created/Modified

- `literature/01-revolution-prediction.md` - Structured review of revolution prediction research across political science, economics, sociology, and conflict studies; 350 lines, 45 bibliography entries, 20 extracted variables
- `literature/02-democratic-backsliding.md` - Structured review of democratic backsliding and state failure literature; 411 lines, 42 bibliography entries, 20 extracted variables

## Decisions Made

1. **Georgescu (2023) operationalization noted as potential EMP improvement:** The education-job mismatch proxy for elite overproduction (graduate degree holders per professional job opening) may be more theoretically faithful than the current top 1% income share proxy in the codebase. Flagged for Plan 05 framework assessment.

2. **PITF regime type predictor included despite US-applicability debate:** The PITF model's strongest predictor (partial democracy with factionalism) is becoming directly debated for the US (Walter 2022 vs. Svolik 2019). Included as Tier 2 (applicable with adaptation) rather than dismissing it.

3. **Affective polarization prioritized over ideological polarization:** The literature converges on affective polarization (partisan antipathy, social distance) as the dangerous form, while ideological polarization is a normal feature of democracy. This distinction should inform variable selection in Plan 04.

4. **State-level disaggregation identified as critical:** Grumbach's finding that US democratic quality varies enormously across states suggests that national-level measures alone may miss the most important variation. Plan 04 should consider state-level variables.

5. **No new Turchin PSI specification found:** Addressed Phase 1 Open Question #1 -- End Times (2023) was a popular-science book, not a technical update. The 3-proxy PSI-Simple approach remains the most current operationalization available.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- **Plan 02 (Historical case studies + Economic preconditions):** Ready. These domain reviews follow the same Pattern 1 structure established here and will add variables that overlap with/complement the revolution prediction and democratic backsliding variables.
- **Plan 04 (Variable catalog):** Partially ready. The 40 variables extracted across these two reviews (with some overlap) provide the first major input to the ranked catalog. Plans 02 and 03 will complete the variable discovery.
- **Plan 05 (Framework assessment):** Partially ready. Four candidate frameworks (PITF, V-Dem ERT, FSI, Grumbach) are explicitly identified for detailed assessment. Additional frameworks will emerge from Plans 02-03.

## Self-Check: PASSED

- FOUND: literature/01-revolution-prediction.md
- FOUND: literature/02-democratic-backsliding.md
- FOUND: .planning/phases/02-literature-mining/02-01-SUMMARY.md
- FOUND: cbd4896 (Task 1 commit)
- FOUND: d848b2d (Task 2 commit)

---
*Phase: 02-literature-mining*
*Completed: 2026-03-04*
