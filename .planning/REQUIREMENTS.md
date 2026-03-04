# Requirements: Revolution Probability Tracker

**Defined:** 2026-03-01
**Milestone:** v1.1 Build & Validate
**Core Value:** Produce a defensible, data-backed political stress score from freely available data -- one number that synthesizes what academic research says matters into something actionable and understandable.

## Validated Requirements (v1.0)

Shipped and confirmed valuable in milestone v1.0 (Phases 1-3).

### Prior Work Validation (Phase 1)

- [x] **VAL-01**: Review Turchin PSI model specification against academic source material and confirm or revise component definitions (MMP, EMP, SFD) -- Phase 1
- [x] **VAL-02**: Review Prospect Theory PLI specification and confirm or revise domain loss functions and K constants -- Phase 1
- [x] **VAL-03**: Review Financial Stress Pathway specification and confirm or revise the 2-stage transmission model -- Phase 1
- [x] **VAL-04**: Apply mathematical fixes from critical review (geometric mean for PSI, K constant correction, additive bonuses for PLI, LOCF over interpolation) -- Phase 1
- [x] **VAL-05**: Audit all 18 data series (17 FRED + 1 WID) for current availability, series continuity, and definition changes -- Phase 1
- [x] **VAL-06**: Produce a validation report documenting what was confirmed, revised, or flagged for further investigation -- Phase 1

### Literature Mining (Phase 2)

- [x] **LIT-01**: Conduct exhaustive LLM-assisted review of revolution prediction literature across political science, economics, sociology, and conflict studies -- Phase 2
- [x] **LIT-02**: Conduct exhaustive LLM-assisted review of democratic backsliding and state failure literature -- Phase 2
- [x] **LIT-03**: Conduct exhaustive LLM-assisted review of historical revolution case studies and precondition analysis -- Phase 2
- [x] **LIT-04**: Produce a ranked variable catalog with evidence strength ratings, source papers, and theoretical justification for each variable -- Phase 2
- [x] **LIT-05**: Identify candidate models/frameworks from literature that may supplement or replace the existing 3 models -- Phase 2
- [x] **LIT-06**: Identify candidate training/validation datasets (NAVCO, PITF, UCDP, etc.) for model evaluation -- Phase 2
- [x] **LIT-07**: Produce a synthesis document mapping discovered variables to theoretical frameworks and identifying gaps -- Phase 2

### Data Sourcing (Phase 3)

- [x] **DATA-01**: For each variable in the catalog, determine if a freely available, regularly-updated online data source exists -- Phase 3
- [x] **DATA-02**: For viable data sources, document API endpoints, series IDs, update frequency, historical coverage, and access method -- Phase 3
- [x] **DATA-03**: Classify each variable as: available (free API), available (manual download), partially available (proxy needed), or unavailable -- Phase 3
- [x] **DATA-04**: Produce a final data source inventory mapping viable variables to specific data endpoints -- Phase 3
- [x] **DATA-05**: Identify fallback/proxy variables for critical inputs that lack ideal data sources -- Phase 3

## v1.1 Requirements

Requirements for milestone v1.1 Build & Validate. Each maps to roadmap phases.

### Model Architecture

- [ ] **ARCH-01**: Document final model architecture selection with explicit rationale tied to literature mining findings and data availability constraints -- Phase 4
- [ ] **ARCH-02**: Address the 27% coverage gap -- incorporate institutional, social mobilization, and information domain variables where API data exists -- Phase 4
- [ ] **ARCH-03**: Use rolling z-scores for normalization instead of min-max (per Phase 2 recommendation to handle trending US macroeconomic series) -- Phase 4

### Data Pipeline

- [ ] **PIPE-01**: Fetch data from all 15 free API sources (FRED, BLS, Census, BEA, Treasury, HUD, World Bank, etc.) with caching and rate limiting -- Phase 4
- [ ] **PIPE-04**: LOCF frequency alignment to produce a unified time-indexed dataset from mixed-frequency inputs (daily through annual) -- Phase 4

### Model Implementation

- [ ] **IMPL-01**: Implement scoring model(s) as stateless pure functions accepting unified dataset and returning 0-100 score, component scores, and factor contributions -- Phase 4
- [ ] **IMPL-02**: Implement ensemble/composite scoring with documented weighting rationale (if multiple models are used) -- Phase 4
- [ ] **IMPL-03**: Map 0-100 scores to severity tiers (low/moderate/elevated/high/crisis) with empirically-informed thresholds -- Phase 4

### Validation

- [ ] **VAL-01**: Backtest against 7 historical episodes (1968, 1970, 1992, 2001, 2008, 2011, 2020) -- detect at least 5 of 7 as elevated -- Phase 5
- [ ] **VAL-02**: Backtest against quiet periods (mid-1990s stability) -- scores remain below the "elevated" threshold -- Phase 5
- [ ] **VAL-03**: Bootstrap confidence intervals computed for all scores, narrow enough to distinguish crisis from non-crisis periods -- Phase 5
- [ ] **VAL-04**: Morris screening + Sobol sensitivity analysis across plausible parameter ranges -- model is not brittle -- Phase 5
- [ ] **VAL-05**: Spurious trend detection via detrended analysis and placebo tests -- Phase 5
- [ ] **VAL-06**: Inter-model correlation check if multi-model (flag if >0.85) -- Phase 5
- [ ] **VAL-07**: Short-series split validation -- post-2000 variables tested on recent episodes only, not full backtest -- Phase 5
- [ ] **VAL-08**: Validation report with explicit pass/fail assessment, methodology documentation, and honest disclosure of limitations -- Phase 5

## v2 Requirements

Deferred to future milestone. Tracked but not in current roadmap.

### Data Pipeline Expansion

- **PIPE-02**: Ingest manually downloaded datasets (V-Dem, VoteView, ACLED, WID, etc.) from local files
- **PIPE-03**: Construct 6 proxy/derived variables from raw inputs (e.g., education-job mismatch from Census+BLS)
- **PIPE-05**: Data freshness tracking -- flag stale series, log last-updated dates

### Dashboard

- **DASH-01**: Streamlit research dashboard with headline gauge (0-100 composite score with CI)
- **DASH-02**: Historical trend chart with crisis episode shading
- **DASH-03**: Factor breakdown showing what drives the score
- **DASH-04**: Per-model score comparison view
- **DASH-05**: Data freshness indicators surfaced in UI
- **DASH-06**: Methodology page with full model documentation
- **DASH-07**: Limitations disclosure section

### Scheduling

- **SCHED-01**: Weekly automated pipeline run (fetch, transform, compute, store)
- **SCHED-02**: Score persistence (latest.json + history.parquet)

### Enhancement

- **ENH-01**: Rate-of-change and trajectory analysis (first/second derivatives, J-curve)
- **ENH-02**: Annotated historical event overlay on trend charts
- **ENH-03**: Divergence alerts when models disagree >20 points
- **ENH-04**: Interactive sensitivity analysis with parameter sliders
- **ENH-05**: "What changed since last update" diff view
- **ENH-06**: Public-facing framing and responsible communication

## Out of Scope

Explicitly excluded. Documented to prevent scope creep.

| Feature | Reason |
|---------|--------|
| Multi-country comparison | US-only; cross-national models don't transfer to wealthy democracies (gap analysis section 13) |
| Real-time / daily updates | False precision from stale annual data; weekly cadence is honest |
| News / NLP sentiment integration | Noise that undermines structural signal; trigger events are unpredictable by definition |
| ML prediction framing | Zero labeled revolution events for US; calling it "ML prediction" implies statistical validity that doesn't exist |
| Public API | v1 is a personal research tool; API overhead is premature |
| Push notifications / alerts | No actionability for slowly-moving structural indicators |
| Paywalled data sources | Free data only constraint; skip variables behind paywalls |
| Crowdsourced expert assessments | Massive overhead, subjectivity, consensus bias; use published expert-coded datasets instead |
| Scenario modeling / what-if | Without calibrated parameters, scenarios are garbage in / garbage out |
| Manual download sources (v1.1) | Deferred to v2 to keep v1.1 scope focused on API-accessible data |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| ARCH-01 | Phase 4 | Pending |
| ARCH-02 | Phase 4 | Pending |
| ARCH-03 | Phase 4 | Pending |
| PIPE-01 | Phase 4 | Pending |
| PIPE-04 | Phase 4 | Pending |
| IMPL-01 | Phase 4 | Pending |
| IMPL-02 | Phase 4 | Pending |
| IMPL-03 | Phase 4 | Pending |
| VAL-01 | Phase 5 | Pending |
| VAL-02 | Phase 5 | Pending |
| VAL-03 | Phase 5 | Pending |
| VAL-04 | Phase 5 | Pending |
| VAL-05 | Phase 5 | Pending |
| VAL-06 | Phase 5 | Pending |
| VAL-07 | Phase 5 | Pending |
| VAL-08 | Phase 5 | Pending |

**Coverage:**
- v1.1 requirements: 16 total
- Mapped to phases: 16
- Unmapped: 0

---
*Requirements defined: 2026-03-01*
*Last updated: 2026-03-03 after v1.1 roadmap revision (4 phases condensed to 2)*
