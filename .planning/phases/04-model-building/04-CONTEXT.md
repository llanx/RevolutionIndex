# Phase 4: Model Building - Context

**Gathered:** 2026-03-04
**Status:** Ready for planning

<domain>
## Phase Boundary

Produce working model(s) that compute a 0-100 political stress score from the sourced data, with interpretable factor breakdowns and an automated data pipeline. Models are stateless pure functions. Output conforms to the existing data.ts JSON schema. This phase builds the computational engine; validation is Phase 5's job.

</domain>

<decisions>
## Implementation Decisions

### Model Selection
- Implement all 5 models: the 3 existing (PSI, PLI, FSP) with Phase 1 mathematical fixes applied, plus 2 new frameworks (Georgescu SDT, V-Dem ERT)
- Each model produces its own 0-100 sub-score exposed in the output (supports v2 DASH-04 per-model comparison and Phase 5 validation diagnostics)
- Ensemble method: evidence-weighted average, with weights derived from literature evidence strength and validation track record (PSI and Georgescu SDT likely weighted higher for developed-democracy applicability)
- Document the ensemble weight rationale explicitly

### Data Pipeline Design
- Language: Python
- Pipeline output: overwrite `public/data/current.json`, `public/data/history.json`, `public/data/factors.json` directly, matching the existing `src/lib/data.ts` schema
- Manual-download sources (20 of 45 variables): cache locally in `data/raw/` directory, pipeline reads from cache, user updates files periodically
- Track data freshness: record last-fetch timestamps per source, output freshness metadata (supports v2 DASH-05)
- Frequency alignment: LOCF (last observation carried forward) as specified in requirements

### Factor Grouping
- Use the 5 domains from Phase 3 data inventory as the 5 dashboard factors:
  1. Economic Stress (13 variables)
  2. Political Polarization (8 variables)
  3. Institutional Quality (8 variables)
  4. Social Mobilization (11 variables)
  5. Information/Media (4 variables)
- Rename factor IDs to: `economic_stress`, `political_polarization`, `institutional_quality`, `social_mobilization`, `information_media`
- Update `src/lib/data.ts` BenchmarkFactorId type and related interfaces to match new IDs
- Intra-domain weighting: evidence-strength weighted (Strong > Moderate > Weak per variable catalog ratings)
- Inter-domain weighting: literature-derived, based on Strong-variable count per domain and cross-framework reference frequency

### Score Calibration
- Calibration strategy: historical anchor points. Known crisis periods (2008, 2020) should score in Crisis Territory (51-75), quiet periods (mid-1990s) should score in Stable (0-25)
- Zone boundaries stay fixed at existing quartiles (0-25, 26-50, 51-75, 76-100). Model output calibrated to fit within them
- Include bootstrap confidence intervals in v1 model output (required by Phase 5 TEST-03, supports v2 DASH-01 CI display)
- Historical time series back to ~1960 to cover all 6 Phase 5 validation episodes (1968, 1970, 1992, 2001, 2008, 2020)

### Claude's Discretion
- Python package choices (pandas, numpy, scipy, etc.)
- Pipeline directory structure and module organization
- Bootstrap resampling parameters (number of iterations, CI width)
- Exact normalization approach for mapping raw variables to 0.0-1.0
- LOCF implementation details and edge case handling
- How to handle the 4 unavailable and 6 partially-available variables (use proxies from Phase 3 gap analysis or drop)

</decisions>

<specifics>
## Specific Ideas

- Each model must be a stateless pure function: accepts unified dataset, returns structured output with score, component scores, and factor contributions (per MOD-03)
- The existing `data.ts` schema is the binding contract. Pipeline JSON must match `CurrentData`, `HistoryData`, and `FactorsData` interfaces exactly
- Factor weights in `current.json` must sum to 1.0 (existing schema constraint)
- The data source inventory (`data-sources/data-source-inventory.md`, 2,251 lines) is the authoritative reference for all API endpoints, series IDs, frequencies, and access methods
- The variable catalog (`literature/variable-catalog.md`) provides evidence ratings used for weighting
- The framework assessment (`literature/framework-assessment.md`) provides model specifications for Georgescu SDT and V-Dem ERT

</specifics>

<code_context>
## Existing Code Insights

### Reusable Assets
- `src/lib/data.ts`: Complete TypeScript schema defining all JSON output interfaces (CurrentData, HistoryData, FactorsData, Factor, ZoneConfig, etc.). Pipeline must produce JSON matching these interfaces
- `public/data/*.json`: Placeholder files (current.json, history.json, factors.json, benchmarks.json, factions.json, policies.json) that the pipeline will overwrite
- `ZONES` constant in data.ts: Zone boundaries and colors already defined, pipeline scores must align

### Established Patterns
- Astro static site: all data consumed at build time from JSON files in `public/data/`
- Factor IDs are join keys across current.json and factors.json
- All factor values normalized to 0.0-1.0, composite score 0-100 integer
- History entries in ascending chronological order with ISO 8601 dates

### Integration Points
- Pipeline output goes directly to `public/data/*.json`
- `BenchmarkFactorId` type in data.ts needs updating to match new domain-based factor IDs
- `FactionFactorAlignment` and `FactorPolicies` interfaces reference `BenchmarkFactorId`, so those JSON files (factions.json, policies.json) will need factor ID updates too
- Benchmarks.json factors need updating to new IDs

</code_context>

<deferred>
## Deferred Ideas

None. Discussion stayed within phase scope.

</deferred>

---

*Phase: 04-model-building*
*Context gathered: 2026-03-04*
