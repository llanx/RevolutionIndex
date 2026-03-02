# Requirements: Revolution Probability Tracker

**Defined:** 2026-03-01
**Core Value:** Produce a defensible, data-backed political stress score from freely available data -- one number that synthesizes what academic research says matters into something actionable and understandable.

## v1 Requirements

Requirements for initial release. V1 delivers validated research and working models. Dashboard deferred to v2.

### Prior Work Validation

- [ ] **VAL-01**: Review Turchin PSI model specification against academic source material and confirm or revise component definitions (MMP, EMP, SFD)
- [ ] **VAL-02**: Review Prospect Theory PLI specification and confirm or revise domain loss functions and K constants
- [ ] **VAL-03**: Review Financial Stress Pathway specification and confirm or revise the 2-stage transmission model
- [ ] **VAL-04**: Apply mathematical fixes from critical review (geometric mean for PSI, K constant correction, additive bonuses for PLI, LOCF over interpolation)
- [x] **VAL-05**: Audit all 18 data series (17 FRED + 1 WID) for current availability, series continuity, and definition changes
- [ ] **VAL-06**: Produce a validation report documenting what was confirmed, revised, or flagged for further investigation

### Literature Mining

- [ ] **LIT-01**: Conduct exhaustive LLM-assisted review of revolution prediction literature across political science, economics, sociology, and conflict studies
- [ ] **LIT-02**: Conduct exhaustive LLM-assisted review of democratic backsliding and state failure literature
- [ ] **LIT-03**: Conduct exhaustive LLM-assisted review of historical revolution case studies and precondition analysis
- [ ] **LIT-04**: Produce a ranked variable catalog with evidence strength ratings, source papers, and theoretical justification for each variable
- [ ] **LIT-05**: Identify candidate models/frameworks from literature that may supplement or replace the existing 3 models
- [ ] **LIT-06**: Identify candidate training/validation datasets (NAVCO, PITF, UCDP, etc.) for model evaluation
- [ ] **LIT-07**: Produce a synthesis document mapping discovered variables to theoretical frameworks and identifying gaps

### Data Sourcing

- [ ] **DATA-01**: For each variable in the catalog, determine if a freely available, regularly-updated online data source exists
- [ ] **DATA-02**: For viable data sources, document API endpoints, series IDs, update frequency, historical coverage, and access method
- [ ] **DATA-03**: Classify each variable as: available (free API), available (manual download), partially available (proxy needed), or unavailable
- [ ] **DATA-04**: Produce a final data source inventory mapping viable variables to specific data endpoints
- [ ] **DATA-05**: Identify fallback/proxy variables for critical inputs that lack ideal data sources

### Model Building

- [ ] **MOD-01**: Select final model architecture(s) based on literature mining findings and data availability
- [ ] **MOD-02**: Implement data pipeline: fetch from APIs, LOCF frequency alignment, derived series, freshness tracking
- [ ] **MOD-03**: Implement selected model(s) as stateless pure functions returning structured ModelOutput
- [ ] **MOD-04**: Implement ensemble/composite scoring if multiple models are used
- [ ] **MOD-05**: Implement score interpretation labels mapping 0-100 to severity tiers

### Validation

- [ ] **TEST-01**: Backtest model(s) against historical episodes (1968, 1970, 1992, 2001, 2008, 2020) and verify detection
- [ ] **TEST-02**: Backtest model(s) against quiet periods (1990s stability) and verify low scores
- [ ] **TEST-03**: Compute bootstrap confidence intervals on all scores
- [ ] **TEST-04**: Run sensitivity analysis across plausible parameter ranges
- [ ] **TEST-05**: Check for spurious upward trends (detrended analysis, placebo tests)
- [ ] **TEST-06**: If multi-model: check inter-model correlation (flag if >0.85)
- [ ] **TEST-07**: Produce a validation report with pass/fail assessment and methodology documentation

## v2 Requirements

Deferred to future milestone. Tracked but not in current roadmap.

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

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| VAL-01 | Phase 1 | Pending |
| VAL-02 | Phase 1 | Pending |
| VAL-03 | Phase 1 | Pending |
| VAL-04 | Phase 1 | Pending |
| VAL-05 | Phase 1 | Complete |
| VAL-06 | Phase 1 | Pending |
| LIT-01 | Phase 2 | Pending |
| LIT-02 | Phase 2 | Pending |
| LIT-03 | Phase 2 | Pending |
| LIT-04 | Phase 2 | Pending |
| LIT-05 | Phase 2 | Pending |
| LIT-06 | Phase 2 | Pending |
| LIT-07 | Phase 2 | Pending |
| DATA-01 | Phase 3 | Pending |
| DATA-02 | Phase 3 | Pending |
| DATA-03 | Phase 3 | Pending |
| DATA-04 | Phase 3 | Pending |
| DATA-05 | Phase 3 | Pending |
| MOD-01 | Phase 4 | Pending |
| MOD-02 | Phase 4 | Pending |
| MOD-03 | Phase 4 | Pending |
| MOD-04 | Phase 4 | Pending |
| MOD-05 | Phase 4 | Pending |
| TEST-01 | Phase 5 | Pending |
| TEST-02 | Phase 5 | Pending |
| TEST-03 | Phase 5 | Pending |
| TEST-04 | Phase 5 | Pending |
| TEST-05 | Phase 5 | Pending |
| TEST-06 | Phase 5 | Pending |
| TEST-07 | Phase 5 | Pending |

**Coverage:**
- v1 requirements: 30 total
- Mapped to phases: 30
- Unmapped: 0

---
*Requirements defined: 2026-03-01*
*Last updated: 2026-03-01 after roadmap creation*
