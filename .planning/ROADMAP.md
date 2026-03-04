# Roadmap: Revolution Probability Tracker

## Overview

This roadmap delivers a validated, data-backed political stress scoring system for the United States. The work flows through five phases that follow the natural dependency chain: first validate what prior research got right and wrong, then exhaustively mine academic literature for predictive variables, then source free data for those variables, then build models from what is actually available, and finally validate that those models produce meaningful signal. V1 delivers validated research and working models -- the dashboard is v2.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [x] **Phase 1: Prior Work Validation** - Audit the existing 250 pages of theory and 18 data series to establish what holds up and what needs revision
- [x] **Phase 2: Literature Mining** - Exhaustive AI-assisted review across political science, economics, sociology, and conflict studies to discover predictive variables and candidate frameworks
- [x] **Phase 3: Data Sourcing** - Map every discovered variable to freely available data sources, classify availability, and identify proxies for gaps (completed 2026-03-04)
- [ ] **Phase 4: Model Building** - Select architecture(s) informed by literature findings and data availability, implement data pipeline and scoring models (gap closure in progress)
- [ ] **Phase 5: Validation** - Backtest against historical episodes, quantify uncertainty, test for overfitting and spurious trends, produce pass/fail assessment

## Phase Details

### Phase 1: Prior Work Validation
**Goal**: Establish a rigorous baseline understanding of what prior research got right, what needs fixing, and what remains uncertain -- so literature mining starts from solid ground rather than unchecked assumptions
**Depends on**: Nothing (first phase)
**Requirements**: VAL-01, VAL-02, VAL-03, VAL-04, VAL-05, VAL-06
**Success Criteria** (what must be TRUE):
  1. Each of the 3 prior models (Turchin PSI, Prospect Theory PLI, Financial Stress Pathway) has a documented assessment stating what is confirmed, what is revised, and what is flagged as questionable
  2. All mathematical fixes from the critical review are either applied with documented rationale or explicitly rejected with documented reasoning
  3. Each of the 18 data series has a current availability status (active, discontinued, changed definition) verified against the actual source
  4. A validation report exists that a new reader could use to understand the state of prior work without reading the original 250 pages
**Plans**: 3 plans

Plans:
- [x] 01-01-PLAN.md — Model assessments for PSI, PLI, and FSP with mathematical fix checklist
- [x] 01-02-PLAN.md — Data series audit for all 18 series (17 FRED + 1 WID)
- [x] 01-03-PLAN.md — Consolidated validation report synthesizing all findings

### Phase 2: Literature Mining
**Goal**: Produce a comprehensive, evidence-ranked catalog of variables that predict revolution/instability, along with candidate theoretical frameworks -- so model selection is driven by the full weight of academic evidence rather than three pre-chosen models. Variables are cross-referenced against federal data APIs during cataloging to give Phase 3 a running start on data availability
**Depends on**: Phase 1
**Requirements**: LIT-01, LIT-02, LIT-03, LIT-04, LIT-05, LIT-06, LIT-07
**Success Criteria** (what must be TRUE):
  1. Literature review covers at minimum four domains: revolution prediction, democratic backsliding/state failure, historical case studies, and economic preconditions -- with source papers cited for each variable discovered
  2. A ranked variable catalog exists where every variable has an evidence strength rating (strong/moderate/weak) and at least one source paper citation
  3. Candidate models/frameworks beyond the original 3 are identified and assessed for applicability to US context
  4. Candidate training/validation datasets (NAVCO, PITF, UCDP, etc.) are identified with documented coverage and access methods
  5. A synthesis document maps variables to theoretical frameworks and explicitly identifies gaps where theory suggests a variable matters but no measurement approach is obvious
  6. Each variable in the catalog has a preliminary data availability tag (fed-data/other-data/unknown) based on cross-referencing against the US Government Open Data MCP's 37 federal APIs
**Plans**: 6 plans

Plans:
- [x] 02-01-PLAN.md — Core domain literature reviews: revolution prediction + democratic backsliding (Wave 1)
- [x] 02-02-PLAN.md — Core domain literature reviews: historical case studies + economic preconditions (Wave 1)
- [x] 02-03-PLAN.md — Adjacent domain literature reviews: social movement theory + media/information ecosystem (Wave 1)
- [x] 02-04-PLAN.md — Ranked variable catalog with MCP data availability cross-referencing (Wave 2)
- [x] 02-05-PLAN.md — Framework assessment + training/validation dataset inventory (Wave 2)
- [x] 02-06-PLAN.md — Synthesis document: variable-framework mapping, gap identification, Phase 1 open question responses (Wave 3)

### Phase 3: Data Sourcing
**Goal**: Determine exactly which predictive variables can actually be measured with free data, building on Phase 2's preliminary data availability tags to produce a concrete inventory that constrains model building to what is empirically feasible
**Depends on**: Phase 2
**Requirements**: DATA-01, DATA-02, DATA-03, DATA-04, DATA-05
**Success Criteria** (what must be TRUE):
  1. Every variable in the ranked catalog from Phase 2 has a data availability classification: available (free API), available (manual download), partially available (proxy needed), or unavailable
  2. For each "available" variable, the specific API endpoint or download URL, series ID, update frequency, and historical coverage are documented
  3. For critical variables classified as "unavailable" or "partially available," at least one fallback/proxy variable is identified or the gap is explicitly documented as accepted
  4. A final data source inventory exists that a developer could use to implement data fetching without any additional research
**Plans**: 3 plans

Plans:
- [x] 03-01-PLAN.md — Methodology + Economic Stress domain sourcing (13 variables, MCP-verified)
- [x] 03-02-PLAN.md — Political Polarization & Elite Dynamics + Institutional/Democratic Quality domains (16 variables)
- [x] 03-03-PLAN.md — Social Mobilization & Trust + Information/Media domains + Availability Summary Matrix + Gap Analysis + Source Registry

### Phase 4: Model Building
**Goal**: Produce working model(s) that compute a 0-100 political stress score from the sourced data, with interpretable factor breakdowns and an automated data pipeline
**Depends on**: Phase 3
**Requirements**: MOD-01, MOD-02, MOD-03, MOD-04, MOD-05
**Success Criteria** (what must be TRUE):
  1. Final model architecture selection is documented with explicit rationale tying back to literature mining findings and data availability constraints
  2. Running the data pipeline fetches current data from all sources, aligns frequencies via LOCF, and produces a unified dataset without manual intervention
  3. Each model accepts the unified dataset and returns a structured output containing a 0-100 score, component scores, and factor contributions -- as a stateless pure function
  4. If multiple models are used, an ensemble/composite score is computed with documented weighting rationale
  5. Score interpretation labels map the 0-100 range to human-readable severity tiers (e.g., low/moderate/elevated/high/crisis)
**Plans**: 3 plans

**Plans**: 4 plans

Plans:
- [x] 04-01-PLAN.md — Architecture selection + data pipeline + schema update (Wave 1)
- [x] 04-02-PLAN.md — Implement 5 models (PSI, PLI, FSP, Georgescu SDT, V-Dem ERT) as pure functions (Wave 2)
- [x] 04-03-PLAN.md — Ensemble scoring, calibration, bootstrap CIs, JSON output (Wave 3)
- [ ] 04-04-PLAN.md — Gap closure: fix bootstrap n=1000 and history 1960-1978 zero entries (Wave 1, gap closure)

### Phase 5: Validation
**Goal**: Determine whether the model(s) produce meaningful signal by testing against historical ground truth -- answering the question "should we trust this score?"
**Depends on**: Phase 4
**Requirements**: TEST-01, TEST-02, TEST-03, TEST-04, TEST-05, TEST-06, TEST-07
**Success Criteria** (what must be TRUE):
  1. Backtesting against historical crisis episodes (1968, 1970, 1992, 2001, 2008, 2020) shows the model detects at least 4 of 6 as elevated
  2. Backtesting against quiet periods (1990s stability) shows scores remain below the "elevated" threshold
  3. Bootstrap confidence intervals are computed for all scores, and the intervals are narrow enough to distinguish crisis from non-crisis periods
  4. Sensitivity analysis across plausible parameter ranges shows the model is not brittle -- conclusions hold across reasonable parameter variation
  5. A validation report exists with explicit pass/fail assessment, methodology documentation, and honest disclosure of limitations
**Plans**: TBD

Plans:
- [ ] 05-01: TBD
- [ ] 05-02: TBD
- [ ] 05-03: TBD

## Progress

**Execution Order:**
Phases execute in numeric order: 1 -> 2 -> 3 -> 4 -> 5

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Prior Work Validation | 3/3 | Complete    | 2026-03-02 |
| 2. Literature Mining | 6/6 | Complete    | 2026-03-04 |
| 3. Data Sourcing | 3/3 | Complete    | 2026-03-04 |
| 4. Model Building | 3/4 | Gap Closure | 2026-03-04 |
| 5. Validation | 0/3 | Not started | - |
