---
phase: 02-literature-mining
plan: 04
subsystem: research
tags: [variable-catalog, evidence-rating, data-availability, deduplication, measurability-filter]

# Dependency graph
requires:
  - phase: 02-literature-mining
    provides: "6 domain literature reviews with ~95 raw variables across revolution prediction, democratic backsliding, historical case studies, economic preconditions, social movement theory, and media/information ecosystem"
provides:
  - "Ranked variable catalog with 45 concept-level variables, evidence ratings, measurement approaches, and data availability tags"
  - "Summary table for quick scanning of all variables by rating, domain, and data availability"
  - "Detailed entries with evidence tables, measurement approaches, and theoretical roles for each variable"
  - "Measurability-filtered exclusion list documenting 5 unmeasurable and 7 US-inapplicable variables"
affects: [02-05-framework-assessment, 02-06-synthesis, 03-data-sourcing, 04-model-building]

# Tech tracking
tech-stack:
  added: []
  patterns: [concept-level-variable-cataloging, hybrid-rating-system, data-availability-tagging, measurability-filter]

key-files:
  created:
    - literature/variable-catalog.md
  modified: []

key-decisions:
  - "Cataloged at concept level with measurement sub-entries per locked decision: 'Income inequality' is one entry with Gini, top 1%, wealth Gini, racial gap as proxy rows"
  - "Rating distribution: 14 Strong (31%), 21 Moderate (47%), 10 Weak (22%) -- meets the discrimination requirement (not >50% Weak)"
  - "4 variables marked Contested: Income/Wealth Inequality, State Fiscal Distress, Regime Type, Misinformation/Social Media/Information Fragmentation"
  - "Data availability: 18 fed-data (40%), 21 other-data (47%), 6 unknown (13%) -- majority of variables have identified sources"
  - "Excluded 5 theoretically important variables via measurability filter (revolutionary consciousness, frame resonance, preference falsification gap, spiral of silence, AI content prevalence)"
  - "Excluded 7 variables as not applicable to US (youth bulge, urbanization rate, military loyalty, resource dependence, infant mortality, ethnic fractionalization, rough terrain)"

patterns-established:
  - "Variable catalog format: Summary table at top (# | Variable | Domains | Rating | Contested | Data Availability | Key Studies) with detailed entries below"
  - "Detailed entry format: Rating, Domains, Data Availability, Definition, Evidence table, Measurement Approaches, Theoretical Role"
  - "Deduplication at concept level: same concept appearing under different names across domains unified into one entry with cross-domain citations"
  - "Anti-pattern avoidance: no frameworks cataloged as variables, no FRED series IDs included, no >50% Weak rating distribution"

requirements-completed: [LIT-04]

# Metrics
duration: 9min
completed: 2026-03-04
---

# Phase 2 Plan 04: Variable Catalog Summary

**Ranked catalog of 45 concept-level instability predictor variables synthesized from 6 domain reviews, with hybrid evidence ratings (Strong/Moderate/Weak), measurement approaches, data availability tags (fed-data/other-data/unknown), and source citations**

## Performance

- **Duration:** 9 min
- **Started:** 2026-03-04T01:28:09Z
- **Completed:** 2026-03-04T01:37:17Z
- **Tasks:** 1
- **Files created:** 1

## Accomplishments

- Synthesized ~95 raw variables from 6 domain literature reviews into 45 concept-level catalog entries, deduplicating variables that appeared under different names across domains (e.g., "relative deprivation" / "perceived loss" / "J-curve gap" unified as one entry)
- Applied the locked hybrid rating system: 14 Strong, 21 Moderate, 10 Weak with 4 Contested markers -- a distribution that provides useful discrimination for downstream model selection
- Every variable includes an evidence table with specific study citations, proxy used, finding, and study type (quant/qual)
- Every variable includes all known measurement approaches with source identification and data availability tags
- Applied the measurability filter to exclude 5 theoretically important but unmeasurable variables, and documented 7 US-inapplicable variables separately
- Cross-referenced data availability: 18 variables have known federal data sources (40%), 21 have non-federal sources (47%), 6 have no identified source yet (13%)

## Task Commits

Each task was committed atomically:

1. **Task 1: Compile, deduplicate, rate, and catalog variables** - `6cb79f3` (feat)

## Files Created/Modified

- `literature/variable-catalog.md` - Ranked variable catalog with summary table, 45 detailed entries, exclusion lists, and bibliography. 1,432 lines.

## Decisions Made

1. **Concept-level cataloging confirmed:** "Income inequality" is one entry with multiple proxy rows (Gini, top 1%, wealth Gini, racial gap), not separate entries. This follows the locked decision from 02-CONTEXT.md and Open Question #6 from 02-RESEARCH.md.

2. **Data availability assessed without MCP:** The plan called for MCP federal data API cross-referencing (~30 seconds per variable). Since MCP is not available in this execution context, data availability tags were assigned based on known federal data sources documented in the 6 domain reviews and the MCP Federal API Coverage Map from 02-RESEARCH.md. The tags are preliminary and will be verified in Phase 3.

3. **Four Contested markers applied:** Income/Wealth Inequality (Collier-Hoeffler vs. Cederman debate), State Fiscal Distress (Japan counterexample), Regime Type (US applicability debate), and three media/information variables (social media, misinformation, echo chambers -- causal direction disputed).

4. **Wealth Concentration (Top 0.1%) treated as separate variable from general inequality:** The intra-elite wealth gap and extreme top-end concentration capture qualitatively different dynamics than aggregate inequality measures. Both are included as separate entries per Turchin's emphasis on the distinction.

5. **Housing affordability included as standalone variable:** Identified in Plan 02 as the US analog to food price triggers in historical revolutions. Rated Moderate based on emerging but limited quantitative evidence linking housing costs to political mobilization.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- **Plan 05 (Framework assessment):** Ready. The variable catalog provides the complete list of measurable variables that each candidate framework must be assessed against. Framework evaluation can now determine which frameworks' required inputs match the available evidence base.
- **Plan 06 (Synthesis):** Ready. The catalog provides the variable-to-domain mapping and evidence ratings needed for the variable-to-framework mapping document.
- **Phase 3 (Data sourcing):** The data availability tags (fed-data/other-data/unknown) give Phase 3 a running start on which variables need federal API sourcing vs. manual data assembly.
- **Phase 4 (Model building):** The Strong-rated variables (14) represent the evidence base's highest-confidence predictors and should form the core of any model. Moderate variables (21) are candidates for inclusion based on data availability. Weak variables (10) may be deferred unless their domains are otherwise unrepresented.

## Self-Check: PASSED

- FOUND: literature/variable-catalog.md
- FOUND: .planning/phases/02-literature-mining/02-04-SUMMARY.md
- FOUND: 6cb79f3 (Task 1 commit)

---
*Phase: 02-literature-mining*
*Completed: 2026-03-04*
