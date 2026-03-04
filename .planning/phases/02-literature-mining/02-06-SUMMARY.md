---
phase: 02-literature-mining
plan: 06
subsystem: research
tags: [synthesis, variable-framework-mapping, gap-identification, open-questions, phase-recommendations, composite-indicators]

# Dependency graph
requires:
  - phase: 02-literature-mining (plans 01-05)
    provides: "6 domain literature reviews, 45-variable ranked catalog, 9-framework assessment, 13-dataset inventory"
  - phase: 01-prior-work-validation
    provides: "Validation report with 7 open questions, 3-model assessments, data series audit"
provides:
  - "Variable-to-framework mapping matrix covering 45 variables across 12 frameworks (3 existing + 9 candidates)"
  - "Three-level gap identification: 5 theory gaps, 6 data gaps, 5 coverage gaps"
  - "Explicit responses to all 7 Phase 1 open questions with resolution status"
  - "Actionable recommendations for Phases 3 (prioritized variable sourcing), 4 (framework integration, normalization strategy), and 5 (multi-source validation strategy)"
  - "Cross-domain variable categories organizing 45 variables into 6 thematic dimensions"
  - "Evidence strength and data availability analysis with category-level breakdowns"
affects: [03-data-sourcing, 04-model-building, 05-validation]

# Tech tracking
tech-stack:
  added: []
  patterns: [variable-framework-mapping, three-level-gap-identification, multi-source-validation-strategy, morris-sobol-sensitivity-protocol]

key-files:
  created:
    - literature/synthesis.md
  modified: []

key-decisions:
  - "Existing 3 models cover only 12 of 45 variables (27%) -- institutional/democratic quality dimension entirely uncovered; Phase 4 should add this dimension"
  - "Georgescu SDT education-job mismatch proxy recommended as more theoretically faithful elite overproduction measure than top 1% income share"
  - "Morris screening + Sobol indices recommended as 3-step sensitivity analysis protocol for 50+ parameter composite indicators"
  - "Multi-source validation strategy: sub-crisis backtesting, cross-national threshold calibration, financial crisis calibration, attitudinal corroboration"
  - "Information/media variables have widest gap between perceived importance and empirical evidence (all 6 variables Weak-rated or Contested)"
  - "Economic variables have strongest evidence (7 of 13 Strong) and best data availability (11 of 13 fed-data)"

patterns-established:
  - "Synthesis document format: executive summary, variable-framework matrix, evidence/data overviews, gaps, open question responses, phased recommendations, cross-domain categories, limitations, bibliography"
  - "Three-level gap identification: theory gaps (unmeasurable concepts), data gaps (measurable but no US source), coverage gaps (literature areas that may have been missed)"
  - "Multi-source validation protocol for zero-event constraint: 4 complementary approaches replacing standard ML metrics"

requirements-completed: [LIT-07]

# Metrics
duration: 6min
completed: 2026-03-04
---

# Phase 2 Plan 06: Literature Mining Synthesis Summary

**Capstone synthesis mapping 45 variables to 12 frameworks, identifying 16 gaps across three levels, resolving all 7 Phase 1 open questions, and delivering prioritized recommendations for Phases 3-5 including a Morris/Sobol sensitivity analysis protocol**

## Performance

- **Duration:** 6 min
- **Started:** 2026-03-04T01:42:24Z
- **Completed:** 2026-03-04T01:48:30Z
- **Tasks:** 1
- **Files created:** 1

## Accomplishments

- Created comprehensive synthesis document (694 lines) that integrates all Phase 2 deliverables (6 domain reviews, variable catalog, framework assessment, dataset inventory) into an actionable reference for downstream phases
- Built a variable-framework mapping matrix showing which of 45 variables are used by each of 12 frameworks (3 existing + 9 candidates), revealing that the existing models cover only 27% of discovered variables and entirely miss the institutional/democratic quality dimension
- Provided explicit, documented responses to all 7 Phase 1 open questions, with resolution status for each: all 7 resolved with specific evidence and recommendations
- Identified 16 gaps across three levels: 5 theory gaps (unmeasurable concepts like revolutionary consciousness and preference falsification), 6 data gaps (measurable but no US source, e.g., security force loyalty indicators), and 5 coverage gaps (literature areas potentially underrepresented)
- Delivered actionable, specific recommendations for Phase 3 (3 priority tiers for variable sourcing based on evidence strength + data availability), Phase 4 (framework integration strategy, normalization method comparison, architecture decisions evidence does/does not support), and Phase 5 (multi-source validation strategy with 7 backtesting episodes and 7 specific dataset assignments)

## Task Commits

Each task was committed atomically:

1. **Task 1: Variable-to-framework mapping and gap identification** - `0f596cc` (feat)

## Files Created/Modified

- `literature/synthesis.md` - Capstone synthesis with 12 major sections: executive summary, variable-framework map, evidence strength overview, data availability overview, identified gaps, Phase 1 open question responses, Phase 3/4/5 recommendations, cross-domain variable categories, limitations and caveats, bibliography. 694 lines.

## Decisions Made

1. **Existing models cover only 27% of variables:** The three existing models (PSI + PLI + FSP) collectively reference 12 of 45 cataloged variables. The institutional/democratic quality dimension (judicial independence, legislative constraints, electoral integrity, executive aggrandizement, voter access) is entirely uncovered -- a significant gap given V-Dem and PITF research identifies these as central to instability risk. Recommended adding a fourth dimension in Phase 4.

2. **Morris/Sobol sensitivity analysis protocol adopted:** For the project's 50+ parameters, recommended a three-step protocol: (1) Morris screening for initial parameter reduction, (2) Sobol indices for the influential parameters identified by Morris, (3) bootstrap confidence intervals for the final composite score. This is based on the COINr methodology used for composite indicator construction.

3. **Multi-source validation strategy formalized:** Given the zero-event constraint (no US revolutions to validate against), formalized a four-part validation approach: sub-crisis backtesting against 7 US stress episodes (1965-2021), cross-national threshold calibration from NAVCO/PITF/V-Dem, financial crisis calibration from Reinhart-Rogoff, and attitudinal corroboration from ANES/WVS. This replaces standard ML evaluation metrics.

4. **Information/media variables flagged as weakest category:** All 6 information/media variables are Weak-rated or Contested, with 3 of 6 having no identified data source. The gap between perceived importance and empirical evidence is the widest in the entire catalog. Recommended treating these as future research targets rather than immediate model inputs.

5. **Economic variables confirmed as strongest foundation:** 7 of 13 economic variables rated Strong, 11 of 13 have federal data sources. The economic dimension can be built almost entirely from automated FRED/BLS/BEA/Census pipelines, providing the most reliable foundation for the model.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- **Phase 2 complete.** All 6 plans executed. The synthesis document serves as the single entry point for understanding the full academic evidence base on US political instability prediction.
- **Phase 3 (Data Sourcing):** Ready. The synthesis provides three priority tiers for variable sourcing with specific series IDs and action items. Key Phase 3 tasks identified: verify OECD KSTEI replacement, test WID API, assess Georgescu education-job mismatch constructibility, download V-Dem v14, register for ACLED access.
- **Phase 4 (Model Building):** Informed. The synthesis recommends enhancing PSI with Georgescu operationalization, adding an institutional health dimension, retaining FSP with FST calibration, and standardizing normalization methods across models.
- **Phase 5 (Validation):** Informed. The multi-source validation strategy with 7 backtesting episodes and 7 dataset assignments provides a concrete starting point.

## Self-Check: PASSED

- FOUND: literature/synthesis.md
- FOUND: .planning/phases/02-literature-mining/02-06-SUMMARY.md
- FOUND: 0f596cc (Task 1 commit)

---
*Phase: 02-literature-mining*
*Completed: 2026-03-04*
