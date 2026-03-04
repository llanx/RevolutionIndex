---
phase: 02-literature-mining
plan: 05
subsystem: research
tags: [framework-assessment, dataset-inventory, candidate-models, validation-data, political-instability, composite-indicators]

# Dependency graph
requires:
  - phase: 01-prior-work-validation
    provides: "Validation report with 7 open questions and existing 3-model assessments"
  - phase: 02-literature-mining (plans 01-03)
    provides: "6 domain reviews with 95+ variables and candidate framework references"
provides:
  - "9 candidate framework assessments with data availability evaluations (PITF, FSI, Collier-Hoeffler, V-Dem ERT, Korotayev-Medvedev ML, Funke-Schularick-Trebesch, Chenoweth Civil Resistance, Georgescu SDT, Grumbach State Democracy)"
  - "13-dataset validation inventory with US coverage and access documentation"
  - "Phase 1 Open Questions #6 (frameworks beyond 3 models) and #7 (sensitivity analysis methods) addressed"
  - "Data availability summary table mapping frameworks to US data sources"
  - "Dataset utility ranking for US-focused validation"
  - "Validation strategy implications given zero-event constraint"
affects: [02-06-synthesis, 03-data-sourcing, 04-model-building, 05-validation]

# Tech tracking
tech-stack:
  added: []
  patterns: [framework-assessment-pattern-3, dataset-inventory-template, zero-event-constraint-documentation]

key-files:
  created:
    - literature/framework-assessment.md
    - literature/dataset-inventory.md
  modified: []

key-decisions:
  - "Georgescu SDT and V-Dem ERT strongly recommended for Phase 4 -- best data availability and US applicability among candidate frameworks"
  - "Collier-Hoeffler greed/grievance model not recommended -- core mechanism (resource financing of rebellion) inapplicable to US"
  - "Zero-event constraint requires multi-source validation: sub-crisis backtesting, cross-national thresholds, financial crisis calibration, attitudinal corroboration"
  - "V-Dem ranked as #1 dataset for project utility (1789-present, 483 indicators, comprehensive US coding)"
  - "ACLED ranked as #2 for real-time US protest/violence monitoring (2020-present, 30K+ events)"
  - "COINr sensitivity analysis approach (Morris screening + Sobol indices) recommended for composite indicators with 50+ parameters"

patterns-established:
  - "Pattern 3 Framework Assessment: theoretical basis, required inputs, known limitations, validation track record, data availability for US, assessment"
  - "Dataset inventory template: full name/citation, coverage, key variables, access method, update status, US coverage, applicability assessment"
  - "Data availability as primary assessment criterion for all framework evaluations"
  - "Honest zero-event constraint documentation as standard practice for validation planning"

requirements-completed: [LIT-05, LIT-06]

# Metrics
duration: 10min
completed: 2026-03-04
---

# Phase 2 Plan 05: Framework Assessment and Dataset Inventory Summary

**9 candidate framework assessments with data-availability-focused evaluations (Georgescu SDT and V-Dem ERT as top recommendations) plus 13-dataset validation inventory with zero-event-aware validation strategy**

## Performance

- **Duration:** 10 min
- **Started:** 2026-03-04T01:28:08Z
- **Completed:** 2026-03-04T01:38:10Z
- **Tasks:** 2
- **Files created:** 2

## Accomplishments

- Framework assessment of 9 candidate models/frameworks beyond the existing 3 (PSI, PLI, FSP), each with full Pattern 3 documentation including theoretical basis, required inputs, known limitations, validation track record, data availability for US, and overall assessment
- Dataset inventory of 13 candidate training/validation datasets with documented coverage, access methods, US coverage, and applicability assessments including a ranked utility table
- Phase 1 Open Questions #6 (frameworks beyond 3 models) and #7 (sensitivity analysis methods) definitively addressed with documented evidence
- Honest documentation of the zero-US-revolution-event constraint and its implications for validation strategy, with a four-part validation approach proposed
- Cross-cutting data availability summary table mapping all 9 frameworks to their US data feasibility
- Sensitivity analysis methods cataloged across frameworks (bootstrap, Bayesian IRT, Monte Carlo, COINr, Shapley values, cross-validation)

## Task Commits

Each task was committed atomically:

1. **Task 1: Framework assessment for candidate models** - `09cb5d3` (feat)
2. **Task 2: Training and validation dataset inventory** - `807194e` (feat)

## Files Created/Modified

- `literature/framework-assessment.md` - 9 candidate framework assessments with data availability as primary criterion, cross-cutting sensitivity analysis methods table, and data availability summary matrix
- `literature/dataset-inventory.md` - 13 dataset entries with full documentation, summary table, zero-event problem discussion, ranked utility table, and validation strategy implications

## Decisions Made

1. **Georgescu SDT strongly recommended for Phase 4:** The education-job mismatch proxy for elite overproduction is constructible from federal data (Census + BLS JOLTS) and may provide better signal than the current top 1% income share proxy. This is the most directly relevant framework for the US case.

2. **V-Dem ERT strongly recommended for Phase 4:** Provides 483 indicators with comprehensive US coding from 1789 to present. The Liberal Democracy Index decline (0.89 to 0.72, 2015-2022) demonstrates the kind of within-democracy variation that other frameworks cannot detect.

3. **Grumbach state-level framework recommended for consideration:** Captures subnational democratic variation invisible to national-level measures. More labor-intensive to construct but fills a unique niche.

4. **Collier-Hoeffler not recommended:** Core mechanism (natural resource financing of rebellion) does not operate in wealthy democracies. Documented for completeness.

5. **V-Dem ranked as top-utility dataset:** Best combination of US coverage depth (1789-present), indicator breadth (483), and data quality for the project's needs. ACLED ranked #2 for real-time monitoring, ANES #3 for attitudinal validation.

6. **Multi-source validation strategy proposed:** Given zero US revolution events, validation must use: (a) sub-crisis backtesting against known US stress periods (1968, 2008, 2020), (b) cross-national threshold calibration from NAVCO/PITF, (c) financial crisis validation from Reinhart-Rogoff, (d) attitudinal corroboration from ANES/WVS.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- **Plan 06 (Synthesis):** Ready. The framework assessment provides the framework-to-variable mapping, and the dataset inventory provides the data source context needed for gap identification. All 6 domain reviews, the variable catalog (Plan 04), and now the framework/dataset deliverables feed into the synthesis.
- **Phase 4 (Model Building):** Informed. Georgescu SDT and V-Dem ERT are flagged as the strongest candidate frameworks for supplementing/adapting the existing 3 models. The sensitivity analysis recommendation (COINr approach) provides Phase 4 with a methodology for handling 50+ parameters.
- **Phase 5 (Validation):** Informed. The dataset inventory with ranked utility and the proposed multi-source validation strategy give Phase 5 a concrete starting point for validation planning.

## Self-Check: PASSED

- FOUND: literature/framework-assessment.md
- FOUND: literature/dataset-inventory.md
- FOUND: .planning/phases/02-literature-mining/02-05-SUMMARY.md
- FOUND: 09cb5d3 (Task 1 commit)
- FOUND: 807194e (Task 2 commit)

---
*Phase: 02-literature-mining*
*Completed: 2026-03-04*
