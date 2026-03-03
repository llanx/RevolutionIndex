# Feature Research

**Domain:** Political instability prediction / revolution probability dashboard
**Researched:** 2026-03-01
**Confidence:** MEDIUM (domain knowledge strong; web verification of competitor features unavailable due to tool restrictions)

## Competitor Landscape Overview

Before categorizing features, here is what exists in this space and what each tool focuses on. This draws on training data knowledge of these platforms (verified against the project's own literature review documents which reference these tools directly).

| Tool | Focus | Model Type | Update Cadence | Access |
|------|-------|------------|----------------|--------|
| **ACLED** | Event-level conflict tracking (protests, battles, violence) | Event coding, not prediction | Daily | Free/academic tier |
| **Fragile States Index (FSI)** | Country-level fragility ranking (178 countries, 12 indicators) | Composite index from mixed methods | Annual | Free dashboard |
| **Global Peace Index (GPI)** | Country-level peacefulness ranking (23 indicators) | Weighted composite | Annual | Free dashboard |
| **PITF** | Instability onset prediction (4 variables, logistic regression) | Statistical model, empirically estimated | Classified (US government) | Not public |
| **CoupCast (OEF Research)** | Coup probability by country | Machine learning ensemble | Monthly | Free dashboard |
| **PRS Group ICRG** | Political risk ratings for investors | Expert assessment + quantitative | Monthly | Paywalled ($$$) |
| **EIU Democracy Index** | Democracy health scoring | Expert assessment | Annual | Paywalled |
| **V-Dem** | Democracy measurement (500+ indicators) | Expert coding | Annual | Free data, no dashboard |

**Key insight for this project:** Most tools in this space are (a) cross-national comparisons, (b) event trackers, or (c) composite indices published annually. Almost none produce a continuously-updated **probability score for a single country** from freely available data with full model transparency. That is the gap this project fills.

---

## Feature Landscape

### Table Stakes (Users Expect These)

These are features that any data-driven instability monitoring tool must have to be taken seriously, even as a personal research dashboard.

| # | Feature | Why Expected | Complexity | Notes |
|---|---------|--------------|------------|-------|
| T1 | **Single composite score (0-100)** | The core value proposition. FSI, GPI, CoupCast all produce one number. Users need a headline figure to anchor interpretation. | MEDIUM | Already designed: ensemble of 3 models with equal weights. Need to validate that output distributes meaningfully across the range (critical review A1/A2 fix). |
| T2 | **Historical time series chart** | Every serious index shows trends over time. A number without context is meaningless. Users must see "is it going up or down?" | LOW | Already built: `plots.py` has multi-panel time series with episode shading. Extend to composite view. |
| T3 | **Component/factor breakdown** | FSI shows 12 sub-indicators. CoupCast shows contributing factors. Users need to know *why* the score is what it is, not just *what* it is. PROJECT.md lists interpretability as a constraint. | MEDIUM | Each model already exposes components (MMP/EMP/SFD, domain losses, FSSI/ETI). Need a unified "top contributors" view across models. |
| T4 | **Automated data pipeline with scheduled refresh** | FRED/WID data must be fetched, aligned, and processed without manual intervention. A tool that requires hand-cranking is a toy. | MEDIUM | Already built: `fred_client.py` with caching, `data_pipeline.py` with LOCF alignment. Need scheduling (cron/task scheduler) and staleness alerts. |
| T5 | **Data freshness indicators** | When data is stale (annual series carried forward 11 months), the user must know. FSI publishes methodology notes on data currency. Without this, false precision. | LOW | Already built: `data_pipeline.py` tracks `months_stale` per series. Need to surface in dashboard UI. |
| T6 | **Backtesting against known episodes** | Any predictive model must show it would have flagged known crises (1968, 2008, 2020) and stayed quiet during calm periods. Without this, no credibility. | MEDIUM | Already built: `backtesting.py` with episode detection, quiet period evaluation, distribution quality checks. Need to present results clearly. |
| T7 | **Score interpretation guide** | What does "45" mean? FSI has "Alert/Warning/Stable" tiers. GPI has "Very High/High/Medium/Low" peace levels. Users need a semantic label, not just a number. | LOW | Already designed: `SCORE_THRESHOLDS` in config (low/moderate/elevated/high/crisis). Need prominent display with color coding. |
| T8 | **Data source documentation** | Academic credibility requires listing every data source, series ID, frequency, and transformation. FSI publishes full methodology. This project's audience (the user) is research-oriented. | LOW | Partially exists in `config.py`. Needs a human-readable "methodology" page in the dashboard. |
| T9 | **Error handling and missing data reporting** | When a FRED series goes unavailable or changes definition, the system must degrade gracefully and report what's missing rather than silently produce garbage. | MEDIUM | Partially built in pipeline. Needs explicit "data quality report" surface in dashboard. |
| T10 | **Confidence intervals / uncertainty bands** | A point estimate without uncertainty is irresponsible, especially for something as consequential as instability prediction. CoupCast shows probability ranges. | MEDIUM | Already built: `uncertainty.py` with bootstrap parameter perturbation. Need to render CI bands on all charts. |

### Differentiators (Competitive Advantage)

Features that set this project apart from existing tools. Not expected by users of a personal research dashboard, but valuable for credibility and insight.

| # | Feature | Value Proposition | Complexity | Notes |
|---|---------|-------------------|------------|-------|
| D1 | **Multi-model ensemble with divergence alerts** | No public tool combines structural-demographic (Turchin), behavioral-economic (prospect theory), and financial stress models into one view. The divergence between models is itself informative: if financial stress screams but structural indicators are quiet, that's a recession, not a revolution. | HIGH | Architecture exists (3 models, equal weights). The differentiation is showing model disagreement as a feature, not a bug. `ENSEMBLE_PARAMS["divergence_alert_threshold"]` already defined at 20 points. |
| D2 | **Rate-of-change and trajectory analysis** | Gap analysis identifies this as a critical missing piece in most frameworks: Davies' J-curve (improvement followed by sharp decline), velocity of change, and acceleration. FSI and GPI only show levels, not derivatives. | MEDIUM | Not yet built. Requires computing first and second derivatives of each component, plus a J-curve detection algorithm (peak-then-decline pattern). |
| D3 | **Full model transparency / open methodology** | PITF is classified. PRS is paywalled. FSI methodology is published but scores are opaque. This project's entire model is open-source Python with every formula visible. Academic users value this immensely. | LOW | Already inherent in the codebase. Formalize with a methodology doc and "view the math" links in dashboard. |
| D4 | **Sensitivity analysis dashboard** | Show users "if you change the normalization window from 1965 to 1975, the PSI moves from X to Y." Exposes researcher degrees of freedom honestly rather than hiding them behind a single number. Critical review D2 identified uncalibrated parameters as a major issue. | HIGH | `uncertainty.py` does bootstrap perturbation. Needs interactive UI: sliders for key parameters, real-time score recomputation. |
| D5 | **Cross-correlation lag analysis (financial stress to social stress)** | The financial stress pathway model hypothesizes 3-12 month lag between financial market stress and real-economy pain. Visualizing this lag structure is novel and useful for timing. | MEDIUM | `plots.py` has `plot_lag_analysis`. Need to run empirically and present findings. |
| D6 | **Annotated historical overlay** | Overlay known events (assassinations, recessions, protests, elections) on the time series to build intuition about what drives score changes. ACLED does this for individual events but no composite risk tool does it well. | MEDIUM | Partially built: `HISTORICAL_EPISODES` in config provides crisis periods. Need event-level annotations (not just period shading). |
| D7 | **"What's changed since last update" diff view** | When the weekly refresh runs, show what moved and why: which data series updated, which components shifted, what drove the score change. No competitor does this. | MEDIUM | Requires storing snapshots and computing deltas between refreshes. Not yet built. |
| D8 | **Literature-grounded variable selection** | Each variable in the model can be traced back to specific academic papers and findings. The project's 250 pages of theory docs provide this grounding. No other public tool makes the academic justification this explicit at the variable level. | LOW | Documentation exists in theory docs. Needs to be surfaced as in-app references per variable. |
| D9 | **Honest "what this can't predict" disclosures** | The gap analysis identifies trigger events, preference falsification, and security force behavior as fundamentally unpredictable from structural data. Stating these limits builds credibility rather than undermining it. | LOW | Content exists in gap analysis. Needs a permanent "limitations" section in the dashboard, not buried in docs. |
| D10 | **Inter-model correlation monitoring** | Track whether the three models are providing independent information or have become correlated over time (critical review C1). If correlation exceeds 0.85, flag that the ensemble is effectively a single model. | LOW | `backtesting.py` has `compute_inter_model_correlation`. Surface in dashboard as ongoing health check. |

### Anti-Features (Commonly Requested, Often Problematic)

Features that seem valuable but would hurt the project if built, especially in v1.

| # | Feature | Why Requested | Why Problematic | Alternative |
|---|---------|---------------|-----------------|-------------|
| A1 | **Multi-country comparison** | "Compare US to other countries" seems natural. FSI and GPI do this. | Data sources are US-specific (FRED, BLS). Cross-national models require completely different data pipelines and the academic literature warns that models calibrated for developing countries misfire on wealthy democracies (gap analysis section 13). Scope explosion for minimal v1 value. | Acknowledge US-only scope. Future v2 could add UK/France with separate pipelines. |
| A2 | **Real-time / daily updates** | "Why weekly? Markets move daily." | Most input data is monthly or quarterly (unemployment, income, sentiment). Daily financial data (VIX, yield curve) creates false precision when combined with annual series carried forward via LOCF. The pipeline already tracks staleness -- daily updates would just show the same stale annual data with a fresh timestamp. | Weekly pipeline runs are honest. Show data freshness prominently so users understand what actually updated. |
| A3 | **Push notifications / email alerts** | "Alert me when the score crosses a threshold." | For a personal research tool, alerts create anxiety without actionability. The model has wide confidence intervals and the score moves slowly (structural data changes gradually). A "crisis alert" based on a 2-point score change is noise. | Show trend direction and velocity on the dashboard. Let the user check when they want to, rather than being pushed. Revisit for v2 public tool. |
| A4 | **Natural language news integration** | "Ingest news headlines to detect triggers." | Trigger events are unpredictable by definition (Kuran's preference falsification model). NLP sentiment on news is noisy, biased toward sensationalism, and creates a feedback loop where media hysteria inflates the score. The project's value is in *structural* indicators, not news sentiment. | Keep the model purely data-driven from economic/demographic sources. Mention "trigger sensitivity" conceptually in interpretation, but don't feed news into the score. |
| A5 | **Machine learning "prediction" framing** | "Use ML to predict revolution probability." | The US has zero revolution events in the training data. ML needs labeled outcomes. Cross-national training data is inapplicable (gap analysis section 13: wealthy democracy problem). Calling it "ML prediction" implies statistical validity that doesn't exist. The critical review (section A4) already flagged that logistic regression with made-up coefficients is worse than an honest weighted index. | Frame as "composite stress indicator" or "structural pressure index," not "prediction." Use interpretable models (weighted composites, not black boxes). Reserve ML for cross-correlation and lag estimation where data is sufficient. |
| A6 | **Crowdsourced expert assessments** | "Let political scientists rate components." | Creates dependency on external contributors, introduces subjectivity, and the Delphi method is known to produce consensus bias. For a personal research tool, this is massive overhead with unclear benefit. | Use published expert-coded datasets (V-Dem, Polity) as inputs where needed. Don't build a survey platform. |
| A7 | **Scenario modeling / "what-if" simulations** | "What if unemployment hits 15%? What if the debt doubles?" | Without empirically calibrated relationships between variables and outcomes, scenarios are just "garbage in, garbage out" with extra steps. The model's parameters are not empirically estimated (critical review D2). Scenarios would convey false precision. | The sensitivity analysis (D4) honestly shows "if parameters vary within plausible ranges, the score varies by X." This is the honest version of scenario modeling. |
| A8 | **Public API for third-party consumption** | "Let others build on top of this data." | v1 is a personal research tool. API design, rate limiting, versioning, documentation, and maintenance overhead are enormous. Premature optimization for a tool with one user. | Export to CSV/JSON for personal use. API is a v2+ feature if the project goes public. |

---

## Feature Dependencies

```
Data Pipeline (T4)
    |-- feeds --> All Models (T1)
    |-- feeds --> Data Freshness (T5)
    |-- feeds --> Data Quality Report (T9)
    |-- feeds --> Lag Analysis (D5)

All Models (T1)
    |-- feeds --> Composite Score (T1)
    |-- feeds --> Component Breakdown (T3)
    |-- feeds --> Historical Time Series (T2)
    |-- feeds --> Uncertainty/CI (T10)
    |-- feeds --> Backtesting (T6)
    |-- feeds --> Inter-Model Correlation (D10)

Composite Score (T1)
    |-- feeds --> Score Interpretation (T7)
    |-- feeds --> Divergence Alerts (D1)

Historical Time Series (T2)
    |-- enhances --> Annotated Overlay (D6)
    |-- enhances --> Rate-of-Change Analysis (D2)

Uncertainty/CI (T10)
    |-- enhances --> Sensitivity Analysis (D4)

Data Pipeline (T4) + Snapshot Storage
    |-- feeds --> "What Changed" Diff View (D7)

Score Interpretation (T7)
    |-- enhances --> Limitations Disclosure (D9)

Documentation (T8)
    |-- enhances --> Literature-Grounded Variables (D8)
    |-- enhances --> Model Transparency (D3)
```

### Dependency Notes

- **Everything depends on T4 (Data Pipeline):** No features work without reliable, aligned data. This is the foundation.
- **T1 (Composite Score) requires all 3 models working:** Each model must produce a 0-100 score before ensemble aggregation. Models can be brought online incrementally (financial stress first -- highest-frequency data, fastest to validate).
- **D7 (Diff View) requires snapshot infrastructure:** Must store previous pipeline run results to compute deltas. This is a new persistence requirement not in the current codebase.
- **D4 (Sensitivity Analysis) extends T10 (Uncertainty):** Same bootstrap machinery, but interactive rather than batch-computed. Requires a UI framework that supports parameter sliders.
- **D2 (Rate-of-Change) can be built independently:** It's a transformation on existing time series data, not a new data source or model. Good candidate for early implementation.

---

## MVP Definition

### Launch With (v1.0) -- Get a Working Score

The absolute minimum to validate the concept: can we produce a defensible, interpretable number from free data?

- [ ] **T4: Automated data pipeline** -- FRED API fetch, LOCF alignment, freshness tracking (mostly built)
- [ ] **T1: Composite score from 3-model ensemble** -- Financial Stress + Turchin PSI + Prospect Theory PLI (models built, need integration)
- [ ] **T2: Historical time series chart** -- Multi-panel view with crisis episode shading (built in matplotlib)
- [ ] **T3: Component breakdown** -- Which sub-components are driving the score (model internals exposed)
- [ ] **T7: Score interpretation labels** -- Color-coded severity tiers (config exists)
- [ ] **T6: Backtesting results** -- Prove the model detects known crises and stays quiet during calm (framework built)
- [ ] **T10: Confidence intervals** -- Bootstrap CI on all scores (framework built)
- [ ] **T8: Methodology documentation** -- What data, what math, what assumptions (partially exists in theory docs)

**v1.0 is a Jupyter notebook or static HTML report, not a live dashboard.** The user can run a script, pull fresh data, and generate charts. This validates the core value proposition before investing in dashboard infrastructure.

### Add After Validation (v1.x) -- Make It Usable

Once the core score is producing sensible output and backtests are passing:

- [ ] **T5: Data freshness indicators in UI** -- Surface staleness visually (data exists, needs rendering)
- [ ] **T9: Data quality report** -- Automated health check on pipeline runs
- [ ] **D1: Divergence alerts** -- Highlight when models disagree by >20 points
- [ ] **D2: Rate-of-change analysis** -- First/second derivatives, J-curve detection
- [ ] **D6: Annotated historical overlay** -- Event markers on time series
- [ ] **D10: Inter-model correlation monitoring** -- Ongoing independence check
- [ ] **D3: Model transparency page** -- Formulas, references, assumptions in one place
- [ ] **D9: Limitations disclosure** -- Permanent "what this can't tell you" section
- [ ] **Scheduling** -- Weekly cron job for data refresh, output generation

### Future Consideration (v2+) -- If the Project Goes Public

Features to defer until the core tool is validated and there's reason to share it:

- [ ] **D4: Interactive sensitivity analysis** -- Requires web UI with parameter sliders
- [ ] **D5: Lag analysis visualization** -- Useful for research but not core to the score
- [ ] **D7: "What changed" diff view** -- Requires snapshot storage infrastructure
- [ ] **D8: Literature-grounded variable references** -- In-app academic citations per variable
- [ ] **Web dashboard** -- Move from Jupyter/static to a live web app (Streamlit/Dash/Panel)
- [ ] **Public-facing framing** -- Responsible communication, disclaimers, media guidance
- [ ] **Multi-country expansion** -- Separate data pipelines per country
- [ ] **Public API** -- For third-party consumption

---

## Feature Prioritization Matrix

| Feature | User Value | Implementation Cost | Priority | Phase |
|---------|------------|---------------------|----------|-------|
| T4: Data pipeline | HIGH | LOW (mostly built) | **P1** | v1.0 |
| T1: Composite score | HIGH | MEDIUM | **P1** | v1.0 |
| T2: Historical charts | HIGH | LOW (mostly built) | **P1** | v1.0 |
| T3: Factor breakdown | HIGH | MEDIUM | **P1** | v1.0 |
| T7: Interpretation labels | HIGH | LOW | **P1** | v1.0 |
| T6: Backtesting | HIGH | LOW (mostly built) | **P1** | v1.0 |
| T10: Confidence intervals | HIGH | LOW (mostly built) | **P1** | v1.0 |
| T8: Methodology docs | MEDIUM | LOW | **P1** | v1.0 |
| T5: Freshness indicators | MEDIUM | LOW | **P2** | v1.x |
| T9: Data quality report | MEDIUM | LOW | **P2** | v1.x |
| D1: Divergence alerts | MEDIUM | LOW | **P2** | v1.x |
| D2: Rate-of-change | HIGH | MEDIUM | **P2** | v1.x |
| D3: Model transparency | MEDIUM | LOW | **P2** | v1.x |
| D6: Annotated overlay | MEDIUM | MEDIUM | **P2** | v1.x |
| D9: Limitations section | MEDIUM | LOW | **P2** | v1.x |
| D10: Correlation monitoring | LOW | LOW | **P2** | v1.x |
| D4: Sensitivity analysis | MEDIUM | HIGH | **P3** | v2+ |
| D5: Lag analysis viz | LOW | MEDIUM | **P3** | v2+ |
| D7: Diff view | MEDIUM | HIGH | **P3** | v2+ |
| D8: Literature references | LOW | MEDIUM | **P3** | v2+ |

**Priority key:**
- P1: Must have for launch -- produces the core score and proves it works
- P2: Should have -- makes the tool usable and credible for ongoing monitoring
- P3: Nice to have -- polish and public-readiness features

---

## Competitor Feature Analysis

| Feature | ACLED | FSI | CoupCast | This Project |
|---------|-------|-----|----------|--------------|
| Single composite score | No (event counts) | Yes (0-120) | Yes (probability %) | Yes (0-100 with interpretation tiers) |
| Country scope | Global | 178 countries | Global | US-only (by design) |
| Update frequency | Daily (events) | Annual | Monthly | Weekly |
| Factor breakdown | Event type categories | 12 indicators | Feature importance | 3 models x 2-5 components each |
| Confidence intervals | No | No | No (point estimate) | Yes (bootstrap CI) |
| Historical backtesting | N/A (event data) | Retrospective rankings | Claimed but not public | Explicit with episode/quiet period evaluation |
| Model transparency | Event coding methodology public | Methodology published, but weighting opaque | "Machine learning" -- black box | Fully open source, every formula visible |
| Rate-of-change analysis | Trend charts for event counts | Year-over-year rank change | No | Planned (D2): first/second derivatives, J-curve detection |
| Data sources | Own field research + media | Mixed methods (quantitative + qualitative + expert) | 70+ features from public data | 17 FRED series + 1 WID series (free, verifiable) |
| Free data? | Event data free for academic use | Scores free, methodology docs free | Dashboard free | Entirely free data, open source code |
| Trigger event detection | Yes (core function) | No (structural only) | No | No (deliberate anti-feature: A4) |
| Sensitivity analysis | N/A | No | No | Planned (D4): parameter perturbation with interactive UI |

---

## Sources

- **Project internal:** `model-specifications.md`, `critical-review-model-specs.md`, `revolution-metrics-data-sources.md`, `gap-analysis-literature-review.md` -- these 250+ pages of prior research provide the academic grounding (HIGH confidence)
- **Existing codebase:** `revolution-index/` Python project with FRED client, data pipeline, 3 models, backtesting, uncertainty, visualization (HIGH confidence -- directly inspected)
- **Competitor knowledge:** ACLED, FSI, GPI, CoupCast, PITF, PRS ICRG, V-Dem, EIU -- based on training data knowledge of these platforms (MEDIUM confidence -- could not verify current feature sets via web due to tool restrictions)
- **Academic frameworks:** Turchin SDT, Goldstone PITF, Chenoweth/Stephan civil resistance, Kuran preference falsification, Davies J-curve -- referenced in project's own literature review (HIGH confidence for theoretical grounding)

**Confidence note:** The competitor analysis section is based on training data knowledge (cutoff ~mid-2025). Specific dashboard features of ACLED, FSI, and CoupCast may have changed since then. The feature categorizations (table stakes vs. differentiators) are HIGH confidence because they are grounded in what this specific project needs, not just what competitors offer.

---
*Feature research for: Political instability prediction / revolution probability dashboard*
*Researched: 2026-03-01*
