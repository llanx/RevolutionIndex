# Roadmap: Revolution Probability Tracker

## Overview

This roadmap delivers a validated, data-backed political stress scoring system for the United States. Milestone v1.0 (Phases 1-3) established the research foundation: validating prior models, mining academic literature for 45 predictive variables, and sourcing free data for all of them. Milestone v1.1 (Phases 4-5) builds and validates the actual system: designing model architecture, constructing the data pipeline, implementing scoring models, and rigorously validating against historical episodes. The result is either a defensible political stress score or an honest report explaining why the data does not support one.

## Milestones

- [x] **v1.0 Research Foundation** - Phases 1-3 (completed 2026-03-04)
- [ ] **v1.1 Build & Validate** - Phases 4-5 (in progress)

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

<details>
<summary>v1.0 Research Foundation (Phases 1-3) - COMPLETED 2026-03-04</summary>

- [x] **Phase 1: Prior Work Validation** - Audit the existing 250 pages of theory and 18 data series to establish what holds up and what needs revision
- [x] **Phase 2: Literature Mining** - Exhaustive AI-assisted review across political science, economics, sociology, and conflict studies to discover predictive variables and candidate frameworks
- [x] **Phase 3: Data Sourcing** - Map every discovered variable to freely available data sources, classify availability, and identify proxies for gaps

</details>

### v1.1 Build & Validate (Phases 4-5)

- [ ] **Phase 4: Build** - Design model architecture, build data pipeline for 15 API sources with LOCF alignment and rolling z-scores, implement scoring models producing 0-100 scores with factor breakdowns and severity tiers
- [ ] **Phase 5: Validate** - Backtest against 7 historical episodes, quantify uncertainty, test for brittleness and spurious trends, produce pass/fail validation report

## Phase Details

<details>
<summary>v1.0 Research Foundation (Phases 1-3) - COMPLETED 2026-03-04</summary>

### Phase 1: Prior Work Validation
**Goal**: Establish a rigorous baseline understanding of what prior research got right, what needs fixing, and what remains uncertain -- so literature mining starts from solid ground rather than unchecked assumptions
**Depends on**: Nothing (first phase)
**Requirements**: VAL-01, VAL-02, VAL-03, VAL-04, VAL-05, VAL-06 (v1.0)
**Success Criteria** (what must be TRUE):
  1. Each of the 3 prior models (Turchin PSI, Prospect Theory PLI, Financial Stress Pathway) has a documented assessment stating what is confirmed, what is revised, and what is flagged as questionable
  2. All mathematical fixes from the critical review are either applied with documented rationale or explicitly rejected with documented reasoning
  3. Each of the 18 data series has a current availability status (active, discontinued, changed definition) verified against the actual source
  4. A validation report exists that a new reader could use to understand the state of prior work without reading the original 250 pages
**Plans**: 3 plans

Plans:
- [x] 01-01-PLAN.md -- Model assessments for PSI, PLI, and FSP with mathematical fix checklist
- [x] 01-02-PLAN.md -- Data series audit for all 18 series (17 FRED + 1 WID)
- [x] 01-03-PLAN.md -- Consolidated validation report synthesizing all findings

### Phase 2: Literature Mining
**Goal**: Produce a comprehensive, evidence-ranked catalog of variables that predict revolution/instability, along with candidate theoretical frameworks -- so model selection is driven by the full weight of academic evidence rather than three pre-chosen models. Variables are cross-referenced against federal data APIs during cataloging to give Phase 3 a running start on data availability
**Depends on**: Phase 1
**Requirements**: LIT-01, LIT-02, LIT-03, LIT-04, LIT-05, LIT-06, LIT-07 (v1.0)
**Success Criteria** (what must be TRUE):
  1. Literature review covers at minimum four domains: revolution prediction, democratic backsliding/state failure, historical case studies, and economic preconditions -- with source papers cited for each variable discovered
  2. A ranked variable catalog exists where every variable has an evidence strength rating (strong/moderate/weak) and at least one source paper citation
  3. Candidate models/frameworks beyond the original 3 are identified and assessed for applicability to US context
  4. Candidate training/validation datasets (NAVCO, PITF, UCDP, etc.) are identified with documented coverage and access methods
  5. A synthesis document maps variables to theoretical frameworks and explicitly identifies gaps where theory suggests a variable matters but no measurement approach is obvious
  6. Each variable in the catalog has a preliminary data availability tag (fed-data/other-data/unknown) based on cross-referencing against the US Government Open Data MCP's 37 federal APIs
**Plans**: 6 plans

Plans:
- [x] 02-01-PLAN.md -- Core domain literature reviews: revolution prediction + democratic backsliding (Wave 1)
- [x] 02-02-PLAN.md -- Core domain literature reviews: historical case studies + economic preconditions (Wave 1)
- [x] 02-03-PLAN.md -- Adjacent domain literature reviews: social movement theory + media/information ecosystem (Wave 1)
- [x] 02-04-PLAN.md -- Ranked variable catalog with MCP data availability cross-referencing (Wave 2)
- [x] 02-05-PLAN.md -- Framework assessment + training/validation dataset inventory (Wave 2)
- [x] 02-06-PLAN.md -- Synthesis document: variable-framework mapping, gap identification, Phase 1 open question responses (Wave 3)

### Phase 3: Data Sourcing
**Goal**: Determine exactly which predictive variables can actually be measured with free data, building on Phase 2's preliminary data availability tags to produce a concrete inventory that constrains model building to what is empirically feasible
**Depends on**: Phase 2
**Requirements**: DATA-01, DATA-02, DATA-03, DATA-04, DATA-05 (v1.0)
**Success Criteria** (what must be TRUE):
  1. Every variable in the ranked catalog from Phase 2 has a data availability classification: available (free API), available (manual download), partially available (proxy needed), or unavailable
  2. For each "available" variable, the specific API endpoint or download URL, series ID, update frequency, and historical coverage are documented
  3. For critical variables classified as "unavailable" or "partially available," at least one fallback/proxy variable is identified or the gap is explicitly documented as accepted
  4. A final data source inventory exists that a developer could use to implement data fetching without any additional research
**Plans**: 3 plans

Plans:
- [x] 03-01-PLAN.md -- Methodology + Economic Stress domain sourcing (13 variables, MCP-verified)
- [x] 03-02-PLAN.md -- Political Polarization & Elite Dynamics + Institutional/Democratic Quality domains (16 variables)
- [x] 03-03-PLAN.md -- Social Mobilization & Trust + Information/Media domains + Availability Summary Matrix + Gap Analysis + Source Registry

</details>

### Phase 4: Build
**Goal**: Design the model architecture, build the data pipeline, and implement scoring models -- taking the project from research artifacts to working software that ingests live data and produces interpretable political stress scores
**Depends on**: Phase 3
**Requirements**: ARCH-01, ARCH-02, ARCH-03, PIPE-01, PIPE-04, IMPL-01, IMPL-02, IMPL-03
**Success Criteria** (what must be TRUE):
  1. A model architecture document exists that specifies which of the 15 API-accessible variables are included, how they group into domains, how domain scores aggregate into a composite, and how the 27% coverage gap is addressed -- with every choice tied to a literature mining finding or data availability constraint
  2. Running the pipeline fetches data from all 15 free API sources (FRED, BLS, Census, BEA, Treasury, HUD, World Bank) without manual intervention -- a single command produces a unified dataset
  3. Mixed-frequency inputs (weekly STLFSI4, monthly UNRATE/CPI, quarterly GDP/DFA, annual Gini/WGI) are aligned to a common frequency using LOCF, and all series are normalized using rolling z-scores -- no linear interpolation, no min-max normalization
  4. Each scoring model is a stateless pure function: given the unified dataset, it returns a 0-100 composite score, per-domain component scores, and per-variable factor contributions -- no hidden state, no side effects
  5. The 0-100 score maps to named severity tiers (low/moderate/elevated/high/crisis) with thresholds informed by the distribution of historical scores, and a user can inspect any score and trace it back to which variables drove it up or down
  6. If multiple models are used, an ensemble/composite score is computed with documented weighting rationale
**Plans**: TBD

Plans:
- [ ] 04-01: TBD
- [ ] 04-02: TBD
- [ ] 04-03: TBD
- [ ] 04-04: TBD
- [ ] 04-05: TBD

### Phase 5: Validate
**Goal**: Determine whether the model(s) produce meaningful signal by testing against historical ground truth, quantifying uncertainty, and checking for common failure modes -- answering the question "should we trust this score?" with an honest pass/fail assessment
**Depends on**: Phase 4
**Requirements**: VAL-01, VAL-02, VAL-03, VAL-04, VAL-05, VAL-06, VAL-07, VAL-08
**Success Criteria** (what must be TRUE):
  1. Backtesting against 7 historical episodes (1968, 1970, 1992, 2001, 2008, 2011, 2020) detects at least 5 of 7 as elevated, AND the mid-1990s quiet period scores below the elevated threshold
  2. Bootstrap confidence intervals for all scores are narrow enough to distinguish crisis periods from non-crisis periods -- if the intervals overlap too much, the model cannot discriminate and that is reported as a failure
  3. Morris screening and Sobol sensitivity analysis across plausible parameter ranges show the model is not brittle -- conclusions hold under reasonable parameter variation, and the most influential parameters are identified
  4. Spurious trend detection (detrended analysis, placebo tests) confirms the score is not simply tracking GDP or another single macro trend in disguise
  5. A validation report exists with explicit pass/fail verdicts for each test, methodology documentation sufficient for reproduction, and honest disclosure of limitations -- no hedging about whether the model "works"
**Plans**: TBD

Plans:
- [ ] 05-01: TBD
- [ ] 05-02: TBD
- [ ] 05-03: TBD

## Progress

**Execution Order:**
Phases execute in numeric order: 1 -> 2 -> 3 -> 4 -> 5

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 1. Prior Work Validation | v1.0 | 3/3 | Complete | 2026-03-02 |
| 2. Literature Mining | v1.0 | 6/6 | Complete | 2026-03-04 |
| 3. Data Sourcing | v1.0 | 3/3 | Complete | 2026-03-04 |
| 4. Build | v1.1 | 0/5 | Not started | - |
| 5. Validate | v1.1 | 0/3 | Not started | - |
