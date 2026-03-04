---
phase: 03-data-sourcing
plan: 02
subsystem: data-sourcing
tags: [voteview, dw-nominate, anes, wid, v-dem, freedom-house, grumbach, political-polarization, institutional-quality, data-inventory]

# Dependency graph
requires:
  - phase: 02-literature-mining
    provides: "45-variable ranked catalog with evidence ratings and data availability tags"
  - phase: 03-data-sourcing plan 01
    provides: "Data source inventory document with methodology and Economic Stress domain (13 variables)"
provides:
  - "Political Polarization & Elite Dynamics domain (8 variables) in data source inventory"
  - "Institutional / Democratic Quality domain (8 variables) in data source inventory"
  - "V-Dem common documentation block for institutional variables"
  - "Construction recipes for derived measures (party polarization, elite factionalism, intra-elite ratio, middle-class share)"
affects: [03-03-PLAN, 04-model-building]

# Tech tracking
tech-stack:
  added: []
  patterns: [v-dem-common-documentation, state-level-aggregation-recipe, non-mcp-source-verification]

key-files:
  created: []
  modified:
    - data-sources/data-source-inventory.md

key-decisions:
  - "VoteView DW-NOMINATE party mean distance recommended as gold standard for congressional polarization (#3)"
  - "ANES partisan feeling thermometer difference (VCF0218/VCF0224) recommended for affective polarization (#4) despite biennial frequency"
  - "Intra-party DW-NOMINATE SD recommended as constructible proxy for elite factionalism (#11)"
  - "Fed DFA (WFRBSTP1300/WFRBST01134) recommended over WID for intra-elite wealth gap (#19) due to quarterly frequency"
  - "Anti-system party vote share (#31) requires Phase 4 coding decision -- data sources provide raw returns, not classification"
  - "V-Dem v2x_libdem recommended as primary institutional quality measure with rate-of-change analysis for US context"
  - "V-Dem near-ceiling limitation documented -- absolute levels less informative than trends for US"
  - "World Bank WGI Government Effectiveness (GE.EST) recommended for state capacity via MCP tool"
  - "No Polity V references -- explicitly excluded as deprecated"

patterns-established:
  - "V-Dem common documentation block: shared download URL, file format, license, and US limitations for all V-Dem variables"
  - "State-level aggregation recipe: population-weighted national average from Grumbach SDI or similar state-level measures"
  - "Non-MCP source verification: web research confirmation of access method, format, and current version for academic datasets"

requirements-completed: [DATA-01, DATA-02, DATA-03, DATA-05]

# Metrics
duration: 8min
completed: 2026-03-04
---

# Phase 3 Plan 2: Political Polarization & Institutional Quality Data Source Inventory Summary

**16 variables sourced across Political Polarization (VoteView DW-NOMINATE, ANES thermometers, Fed DFA wealth shares, Census racial income, MIT Election Lab) and Institutional Quality (V-Dem v15 for 6 of 8 variables, World Bank WGI, Grumbach SDI, Freedom House) domains with construction recipes for 5 derived measures**

## Performance

- **Duration:** 8 min
- **Started:** 2026-03-04T04:39:50Z
- **Completed:** 2026-03-04T04:48:04Z
- **Tasks:** 2
- **Files modified:** 1

## Accomplishments
- Sourced and documented 8 Political Polarization & Elite Dynamics variables with VoteView, ANES, Fed DFA, WID, Census, MIT Election Lab, and FEC data sources
- Sourced and documented 8 Institutional / Democratic Quality variables with V-Dem v15, Freedom House, RSF, Grumbach SDI, Electoral Integrity Project, Bright Line Watch, and World Bank WGI
- Created V-Dem common documentation block establishing shared access details for all V-Dem variables (download URL, file format, license, US limitations)
- Provided construction recipes for 5 derived measures: party polarization from DW-NOMINATE, elite factionalism from intra-party SD, intra-elite concentration ratio, middle-class income share, and national aggregation from state-level data
- Domain summaries with coverage assessments: Domain 2 at 88% available (3 API + 4 download + 1 constructible), Domain 3 at 100% available (1 API + 7 download)

## Task Commits

Each task was committed atomically:

1. **Task 1: Source Political Polarization and Elite Dynamics domain (8 variables)** - `a398fbd` (feat)
2. **Task 2: Source Institutional / Democratic Quality domain (8 variables)** - `0faabc4` (feat)

## Files Created/Modified
- `data-sources/data-source-inventory.md` - Added Domain 2 (Political Polarization, 8 variables) and Domain 3 (Institutional / Democratic Quality, 8 variables) with standardized metadata, measures tables, recommended picks, construction recipes, and domain summaries

## Decisions Made

1. **VoteView DW-NOMINATE as polarization standard (#3):** Party mean distance on 1st dimension is the standard operationalization (McCarty et al. 2006). CSV download from voteview.com/data -- not an API.

2. **ANES feeling thermometers for affective polarization (#4):** VCF0218 (in-party) minus VCF0224 (out-party) from the cumulative data file. Biennial/quadrennial frequency requires LOCF alignment.

3. **Intra-party DW-NOMINATE SD for elite factionalism (#11):** Constructible from same VoteView data as polarization but measures within-party dispersion. Captures ideological factionalism but not all forms (patronage, generational).

4. **Fed DFA over WID for intra-elite wealth gap (#19):** WFRBSTP1300/WFRBST01134 on FRED provides quarterly frequency (vs. WID annual) for the concentration ratio. WID retained as long-history supplement (1913-present).

5. **Anti-system party coding deferred to Phase 4 (#31):** MIT Election Lab provides standardized election returns, but defining "anti-system" requires an explicit coding scheme that does not exist in any pre-built dataset. FEC provides financial data, not vote totals.

6. **V-Dem rate-of-change recommendation for US:** All V-Dem indices are near ceiling for US. Year-over-year change and sub-indicator decomposition recommended over absolute levels. This applies to 6 of 8 institutional domain variables.

7. **World Bank WGI for state capacity (#38):** Government Effectiveness (GE.EST) accessible via MCP `wb_indicator` tool. Provides standardized cross-national governance scores from 1996.

8. **Polity V explicitly excluded:** Deprecated since 2018. V-Dem v15 (March 2025) is the current standard.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness
- 21 of 45 variables now sourced across 3 domains (Economic Stress: 13, Political Polarization: 8, completed; Institutional: 8, completed)
- Plan 03 will complete remaining domains: Social Mobilization & Trust, Information / Media Ecosystem, plus Availability Summary Matrix and Gap Analysis
- Three critical gaps documented for Phase 4: anti-system party coding decision, V-Dem rate-of-change methodology, electoral fraud perception vs. structural integrity gap
- V-Dem single-source dependency noted for institutional domain (6 of 8 variables) -- non-V-Dem alternatives documented for robustness

## Self-Check: PASSED

- [x] data-sources/data-source-inventory.md exists
- [x] .planning/phases/03-data-sourcing/03-02-SUMMARY.md exists
- [x] Commit a398fbd (Task 1) exists
- [x] Commit 0faabc4 (Task 2) exists
- [x] Domain 2: 8 variable entries
- [x] Domain 3: 8 variable entries
- [x] V-Dem variable codes present
- [x] ANES variable codes present
- [x] VoteView CSV files documented
- [x] WID indicator codes present
- [x] World Bank WGI codes present

---
*Phase: 03-data-sourcing*
*Completed: 2026-03-04*
