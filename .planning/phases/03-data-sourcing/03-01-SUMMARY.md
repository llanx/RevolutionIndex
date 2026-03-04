---
phase: 03-data-sourcing
plan: 01
subsystem: data-sourcing
tags: [fred, bls, bea, census, treasury, economic-variables, data-inventory]

# Dependency graph
requires:
  - phase: 02-literature-mining
    provides: "45-variable ranked catalog with evidence ratings and data availability tags"
provides:
  - "Data source inventory document with methodology and Economic Stress domain (13 variables)"
  - "Standardized variable entry template for subsequent domain sourcing"
  - "CSCICP03USM665S discontinuation handling recommendation"
  - "Construction recipes for derived variables (relative deprivation, cost of living, elite overproduction)"
affects: [03-02-PLAN, 03-03-PLAN, 04-model-building]

# Tech tracking
tech-stack:
  added: []
  patterns: [variable-entry-template, proxy-tier-classification, mcp-verification-workflow]

key-files:
  created:
    - data-sources/data-source-inventory.md
  modified: []

key-decisions:
  - "CSCICP03USM665S: Drop weight from FSP ETI and redistribute rather than introducing UMCSENT overlap or paid Conference Board CCI"
  - "PRS85006173 recommended over W270RE1A156NBEA for labor share (nonfarm business sector more commonly cited in labor economics)"
  - "TDSP recommended over HDTGPDUSQ163N for household debt (better coverage 1980 vs 2005, measures burden not level)"
  - "Georgescu education-job mismatch proxy documented as preferred elite overproduction measure with WID top 1% as fallback"
  - "FIXHAI recommended for housing affordability (composite of prices, rates, and income in single index)"
  - "STLFSI4 confirmed as primary financial stress measure (replaces older STLFSI/2/3 versions)"

patterns-established:
  - "Variable entry template: catalog number, rating, theoretical concept, availability, measures table, recommended, rate limits, license, known gaps, last verified"
  - "Two-tier proxy system: direct measure and strong proxy only (no weak/speculative)"
  - "Availability taxonomy: Available (free API), Available (manual download), Partially available (proxy needed), Unavailable"

requirements-completed: [DATA-01, DATA-02, DATA-03, DATA-05]

# Metrics
duration: 5min
completed: 2026-03-04
---

# Phase 3 Plan 1: Economic Stress Domain Data Source Inventory Summary

**Data source inventory with methodology framework and 13 economic stress variables verified against FRED/BLS/BEA/Treasury -- 10 available via free API, 3 constructible from components, CSCICP03USM665S discontinuation handled**

## Performance

- **Duration:** 5 min
- **Started:** 2026-03-04T04:30:28Z
- **Completed:** 2026-03-04T04:36:08Z
- **Tasks:** 1
- **Files modified:** 1

## Accomplishments
- Created comprehensive data source inventory document with methodology section defining proxy tiers, metadata schema (14 fields), verification approach, and multiple proxies/short series policies
- Sourced and documented 13 economic stress variables with verified series IDs, coverage windows, frequency, rate limits, and licensing
- Documented CSCICP03USM665S discontinuation with explicit handling recommendation (weight redistribution in FSP ETI)
- Provided construction recipes for 3 derived variables: Georgescu elite overproduction proxy, relative deprivation expectation-reality gap, and cost of living pressure composite
- Domain summary with coverage assessment showing 77% of economic variables available via free API

## Task Commits

Each task was committed atomically:

1. **Task 1: Create inventory document with methodology and Economic Stress domain entries** - `6b40285` (feat)

## Files Created/Modified
- `data-sources/data-source-inventory.md` - Complete methodology section + 13 economic stress variable entries with standardized metadata, measures tables, recommended picks, and known gaps

## Decisions Made

1. **CSCICP03USM665S handling:** Drop weight from FSP ETI and redistribute to remaining inputs. Using UMCSENT would violate zero-overlap design with PLI. Conference Board CCI requires paid subscription. This loses consumer confidence signal in FSP but UMCSENT captures it in PLI.

2. **Labor share series selection:** Recommended PRS85006173 (nonfarm business) over W270RE1A156NBEA (GDP-based) because it is more commonly cited in labor economics literature and excludes agriculture/government sectors for cleaner measurement.

3. **Household debt measure:** Recommended TDSP (debt service ratio, 1980-present) over HDTGPDUSQ163N (debt-to-GDP, 2005-present) because TDSP has 25 years more history and measures the burden dimension (household budget impact) rather than just the level.

4. **Elite overproduction proxy:** Documented Georgescu education-job mismatch construction recipe as theoretically preferred measure, with WID top 1% income share as fallback. The constructed proxy is tagged "short series" (2005-present).

5. **Housing affordability:** Recommended FIXHAI (Housing Affordability Index) as the primary measure because it is a composite that already combines prices, mortgage rates, and income into a single interpretable index.

6. **Financial stress index:** Confirmed STLFSI4 as the current/correct version. Documented that STLFSI/2/3 are superseded and TEDRATE is discontinued (LIBOR phase-out).

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness
- Methodology section and variable entry template established for Plans 02 and 03
- Economic stress domain complete -- Plans 02 and 03 will add Political/Institutional and Social/Information domains
- Three critical gaps documented for Phase 4 attention: CSCICP03USM665S weight redistribution, Georgescu proxy validation, DRSFRMACBS methodology break handling

---
*Phase: 03-data-sourcing*
*Completed: 2026-03-04*
