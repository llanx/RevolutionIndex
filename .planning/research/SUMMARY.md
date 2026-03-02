# Project Research Summary

**Project:** Revolution Probability Tracker
**Domain:** Data-driven political instability composite index / personal research dashboard
**Researched:** 2026-03-01
**Confidence:** HIGH (stack verified via pip; architecture and pitfalls grounded in 250 pages of project-specific theory docs and existing codebase; features informed by competitor landscape analysis)

## Executive Summary

This project is a **composite index dashboard** -- the same category as the Fragile States Index or Human Development Index, but US-specific, continuously updated, and fully transparent. The standard approach for building such tools is a batch ETL pipeline (ingest free data, align frequencies, compute weighted composites) feeding a lightweight dashboard. The recommended stack is entirely Python: pandas/NumPy/SciPy for computation, DuckDB or flat Parquet files for storage, Streamlit for the dashboard, and Plotly for interactive charts. All dependencies are mature, well-documented, and free. The existing `revolution-index/` codebase provides substantial scaffolding for data ingestion, model computation, and backtesting that can be refactored into the new project.

The recommended approach is to build bottom-up through five phases: data foundation first, then model computation, then a hard validation gate (backtesting), then persistence/scheduling, and finally the dashboard. The critical insight from research is that **the dashboard must be the last thing built**, not the first. The models must prove they detect known historical crises (1968, 2008, 2020) and stay quiet during stable periods (1990s) before any dashboard work begins. The existing codebase already has most of the data pipeline and model logic, but it contains documented bugs (ETI weight divergence, normalization issues) that must be fixed during the rebuild.

The top risks are: (1) users interpreting the composite score as a calibrated probability when it is an index, (2) overfitting to only 6 historical episodes with 50+ tunable parameters, (3) spurious upward trends from secular inequality/debt increases, and (4) building a dashboard before validating that the models produce meaningful signal. Mitigation requires strict naming discipline ("Political Stress Index" not "Revolution Probability"), freezing parameters before backtesting, detrending analysis, and an explicit validation gate between model-building and dashboard phases.

## Key Findings

### Recommended Stack

The stack is standard Python data science with two opinionated additions: DuckDB for embedded analytical storage and Streamlit for zero-frontend-code dashboarding. All packages have verified versions on pip as of 2026-03-01. Use `uv` for package management (faster and better than pip/poetry).

**Core technologies:**
- **Python 3.12** -- stable runtime, full library support; avoid 3.13 until scientific packages catch up
- **pandas >=2.2 + NumPy >=2.0 + SciPy >=1.14** -- standard scientific stack for data manipulation, time series alignment, and statistical functions
- **fredapi 0.5.2** -- thin FRED API wrapper, already proven in existing codebase
- **Streamlit >=1.40** -- fastest path from Python to interactive dashboard; native Plotly support, multi-page apps, caching
- **Plotly >=6.0** -- interactive charts with native gauge support (go.Indicator), essential for the headline score display
- **DuckDB >=1.3** -- embedded analytical database, reads/writes Parquet natively, replaces file-sprawl management
- **Pydantic >=2.10** -- config validation; catches wrong FRED series IDs and parameter errors at load time
- **APScheduler 3.x** -- cross-platform weekly scheduling (stick with 3.x; 4.x is an unstable rewrite)
- **uv** -- package management; **ruff** -- linting/formatting; **pytest** -- testing

**Version risk:** SHAP 0.50 compatibility with NumPy 2.x needs testing before use. APScheduler inside Streamlit has lifecycle edge cases -- may need a separate process.

**What NOT to use:** Flask/Django (rebuilding Streamlit), PostgreSQL (overkill for 18 time series), Airflow/Prefect (absurd for weekly batch), TensorFlow/PyTorch (black boxes violate interpretability constraint), daily update cadence (false precision from stale annual data).

### Expected Features

**Must have (table stakes for v1.0):**
- T1: Single composite score (0-100) from 3-model ensemble
- T2: Historical time series chart with crisis episode shading
- T3: Component/factor breakdown showing what drives the score
- T4: Automated data pipeline with FRED fetch, LOCF alignment, freshness tracking
- T6: Backtesting results proving the model detects known crises
- T7: Score interpretation labels (low/moderate/elevated/high/crisis tiers)
- T10: Confidence intervals via bootstrap parameter perturbation
- T8: Methodology documentation

**Should have (v1.x differentiators):**
- D1: Multi-model divergence alerts (when models disagree by >20 points)
- D2: Rate-of-change and trajectory analysis (first/second derivatives, J-curve detection)
- D3: Full model transparency page (every formula visible)
- D9: Honest limitations disclosure ("what this cannot predict")
- D10: Inter-model correlation monitoring (independence health check)
- T5: Data freshness indicators surfaced in UI
- T9: Automated data quality report

**Defer to v2+:**
- D4: Interactive sensitivity analysis (parameter sliders)
- D7: "What changed since last update" diff view (requires snapshot storage)
- D5: Cross-correlation lag analysis visualization
- Multi-country expansion, public API, push notifications

**Anti-features (do NOT build):**
- Real-time/daily updates (false precision), news sentiment integration (noise), ML prediction framing (no labeled outcomes), multi-country comparison in v1 (scope explosion), scenario modeling (garbage in/garbage out without calibrated parameters)

### Architecture Approach

The architecture is a classic **batch ETL-to-dashboard pipeline** with five layers: data ingestion (FRED/WID clients with caching), transformation (LOCF frequency alignment, derived series, freshness tracking), model computation (3 stateless models returning structured ModelOutput), score persistence (latest.json + history.parquet), and a read-only dashboard. The critical architectural boundary is that the **dashboard depends ONLY on the score store** -- it never imports model code or triggers data fetches. The pipeline writes files; the dashboard reads files. No database, no API layer, no microservices for v1.

**Major components:**
1. **Config** -- single source of truth for all series IDs, model parameters, weights, thresholds, backtesting episodes
2. **FRED Client + WID Loader** -- data ingestion with rate limiting, caching, staleness detection
3. **Data Pipeline** -- frequency alignment via LOCF, derived series computation, freshness metadata, output as unified monthly Parquet
4. **Three Stateless Models** -- Turchin PSI (structural-demographic), Prospect Theory PLI (behavioral-economic), Financial Stress Pathway (financial-to-economic transmission); each returns ModelOutput dataclass
5. **Ensemble Combiner** -- weighted average with divergence alerting
6. **Uncertainty Engine** -- bootstrap parameter perturbation for confidence intervals
7. **Backtester** -- episode detection, quiet-period evaluation, distribution quality checks
8. **Score Store** -- latest.json (fast dashboard load) + history.parquet (trend charts)
9. **Scheduler** -- weekly pipeline trigger (APScheduler or OS task scheduler)
10. **Dashboard** -- Streamlit read-only display: gauge, trends, factor breakdown, freshness

**Key patterns:** Config-driven data catalog (one file change to add a series), stateless models (pure functions for easy backtesting), structured ModelOutput interface (uniform contract for all downstream consumers), LOCF with freshness tracking (honest about data currency), dashboard-reads-files-not-databases (no operational overhead for v1).

### Critical Pitfalls

1. **Index vs. Probability Confusion (CRITICAL)** -- The 0-100 scale will be misread as a calibrated probability. Prevention: name it "Political Stress Index," always show confidence intervals, use integer scores (no false decimal precision), include persistent "what this means" context.

2. **Overfitting to 6 Episodes (CRITICAL)** -- 50+ parameters and only 6 historical events means any parameter fit is a tautology. Prevention: freeze ALL parameters before running backtests (justify theoretically, not empirically), use sensitivity analysis as the primary validation tool, report parameter sensitivity honestly.

3. **Spurious Upward Trends (CRITICAL)** -- Inequality, debt, and distrust all trend upward over 50 years, mechanically inflating the score. Prevention: compute a detrended variant, run placebo tests on stable periods (1990s must score low), use expanding-window percentile normalization.

4. **Dashboard Before Validation (CRITICAL)** -- Building UI before proving the models work wastes effort. Prevention: explicit validation gate -- models must detect 4+ of 6 crises and score low during quiet periods before any dashboard code is written.

5. **Data Source Fragility (HIGH)** -- FRED series get discontinued (STLFSI already became STLFSI4). Prevention: data dependency matrix, graceful degradation when series unavailable, fallback series identified, freshness metadata surfaced prominently.

## Implications for Roadmap

Based on the combined research, the natural phase structure follows the architecture's dependency chain (bottom-up) with a hard validation gate between model-building and dashboard-building.

### Phase 1: Project Setup and Data Foundation
**Rationale:** Everything depends on having aligned, quality-checked data. Cannot validate models without data. The existing codebase has scaffolding but needs bug fixes and a clean rebuild with the recommended stack.
**Delivers:** Working data pipeline that fetches 17 FRED series + 1 WID series, aligns to monthly via LOCF, computes derived series, tracks freshness, and outputs unified_monthly.parquet.
**Addresses:** T4 (automated pipeline), T5 (freshness tracking), T9 (data quality report)
**Avoids:** P6 (data source fragility) by building in graceful degradation and fallback series from day one. P9 (mixed-frequency false precision) by implementing freshness metadata per series.
**Stack:** Python 3.12, uv, pandas, NumPy, fredapi, pyarrow, DuckDB, Pydantic, python-dotenv, ruff, pytest

### Phase 2: Model Computation
**Rationale:** Models are the intellectual core but depend on Phase 1 data. Build each model individually and unit-test against known historical values before combining into ensemble.
**Delivers:** Three working models (Turchin PSI, Prospect Theory PLI, Financial Stress Pathway) producing ModelOutput objects, plus ensemble combiner with divergence detection.
**Addresses:** T1 (composite score), T3 (factor breakdown), T7 (interpretation labels)
**Avoids:** P1 (index vs. probability) by establishing correct naming/framing from the start. P7 (uncalibrated parameters) by documenting theoretical justification for every parameter. P8 (ensemble interpretation failure) by always exposing per-model scores alongside composite.
**Stack:** SciPy, scikit-learn (QuantileTransformer), config-driven model parameters via Pydantic

### Phase 3: Validation Gate (HARD GATE -- must pass before proceeding)
**Rationale:** This is the most important phase. If models fail backtesting, all subsequent work is wasted. This phase answers: "do these models actually detect historical crises?" The 6-episode / 50-parameter overfitting risk (P2) makes this non-negotiable.
**Delivers:** Backtesting report (sensitivity/specificity across 6 episodes + 2 quiet periods), uncertainty quantification (bootstrap CI), inter-model correlation check, detrended analysis, sensitivity analysis across plausible parameter ranges. Output is a Jupyter notebook or static HTML report with clear pass/fail criteria.
**Addresses:** T6 (backtesting), T10 (confidence intervals), D10 (inter-model correlation)
**Avoids:** P2 (overfitting) by freezing parameters before backtesting. P3 (spurious trends) by requiring low scores during 1990s stability. P4 (dashboard before validation) by making this an explicit gate.
**Pass criteria:** Detect 4+ of 6 crises, score below "elevated" during 1990s quiet period, inter-model correlation below 0.85, score distribution uses meaningful range (not clustered at extremes).

### Phase 4: Persistence, Scheduling, and Pipeline Orchestration
**Rationale:** Only after models are validated does it make sense to persist scores and automate updates. This is the "glue" phase that turns validated models into an operational pipeline.
**Delivers:** Score store (latest.json + history.parquet), pipeline orchestrator (single entry point for full ingest-transform-compute-store flow), weekly scheduler, historical backfill of full time series.
**Addresses:** T4 (scheduled refresh), enables all dashboard work
**Avoids:** P6 (data fragility) with monitoring and staleness alerts in the orchestrator.
**Stack:** DuckDB or Parquet files, APScheduler, JSON for latest scores

### Phase 5: Dashboard
**Rationale:** Dashboard is last because it depends on everything else and is the least risky (standard web dev). The hard problems are all in Phases 1-3. Dashboard is read-only consumption of pre-computed data.
**Delivers:** Interactive Streamlit dashboard with: headline gauge (composite score + CI), historical trend chart with episode shading, per-model score comparison, factor breakdown, data freshness indicators, methodology page, limitations disclosure.
**Addresses:** T2 (time series chart), T3 (factor breakdown in UI), T5 (freshness in UI), T7 (interpretation labels in UI), T8 (methodology page), D1 (divergence alerts), D3 (model transparency), D9 (limitations)
**Avoids:** P1 (probability confusion) with correct labeling. P10 (irresponsible communication) with persistent context. P9 (false precision) by showing freshness per component.
**Stack:** Streamlit, Plotly (go.Indicator gauge, go.Scatter trends), reads from score store only

### Phase 6: Enhancement and Polish (v1.x)
**Rationale:** After the core dashboard works, add differentiating features that improve insight quality.
**Delivers:** Rate-of-change analysis (D2), annotated historical overlay (D6), enhanced sensitivity analysis, "what changed" diff view (D7).
**Addresses:** D2, D6, D7, D4 (interactive sensitivity)
**Stack:** Additional Plotly chart types, snapshot storage for diff views

### Phase Ordering Rationale

- **Data before models:** Models are pure functions of data. No data, no models.
- **Models before validation:** Cannot validate what does not exist.
- **Validation before dashboard:** The FEATURES.md research explicitly recommends v1.0 as a "Jupyter notebook or static HTML report, not a live dashboard." The PITFALLS.md research identifies dashboard-before-validation as a critical pitfall. Both research streams independently converge on this ordering.
- **Dashboard last:** It has zero transitive dependencies on data ingestion or model code (reads files only). It is also the most well-understood work (standard Streamlit patterns). All risk is in Phases 1-3.
- **Enhancement after core:** Differentiators (D2, D4, D7) add value but are not needed to validate the core proposition.

### Research Flags

Phases likely needing deeper research during planning:
- **Phase 2 (Model Computation):** The mathematical fixes from critical-review-model-specs.md (geometric mean for PSI, K constant division for PLI, additive bonuses) need careful implementation. The existing code has documented bugs. Research into the specific normalization approach (expanding-window percentile rank vs. z-score) will be needed.
- **Phase 3 (Validation Gate):** Defining pass/fail criteria for backtesting with only 6 episodes is inherently subjective. Research into how other composite indices (FSI, HDI) validate their models could inform this.
- **Phase 5 (Dashboard):** Streamlit multi-page app patterns and Plotly gauge chart configuration may need phase-specific research, but these are well-documented.

Phases with standard patterns (skip research-phase):
- **Phase 1 (Data Foundation):** FRED API integration and pandas time-series alignment are well-documented. The existing codebase provides a working reference.
- **Phase 4 (Persistence/Scheduling):** Writing JSON and Parquet files, running APScheduler -- all standard patterns with extensive documentation.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | All package versions verified via pip on local machine. Prior codebase validates core library choices (fredapi, pandas, plotly). Only concern: SHAP + NumPy 2.x compatibility untested. |
| Features | MEDIUM-HIGH | Table stakes and differentiators grounded in project's 250-page theory docs and existing code. Competitor analysis based on training data (mid-2025 cutoff), not live verification. Feature prioritization is sound regardless. |
| Architecture | HIGH | Batch ETL-to-dashboard is a well-established pattern. Component boundaries derived from direct inspection of existing codebase. Layered architecture matches project's sequential data flow perfectly. |
| Pitfalls | HIGH | All critical pitfalls grounded in project-specific documents (critical-review-model-specs.md, gap-analysis-literature-review.md). These are not generic warnings -- they are documented issues with this specific project's prior approach. |

**Overall confidence:** HIGH

### Gaps to Address

- **WID.world API reliability:** No SLA, API format may change. Need a manual CSV fallback path. Test during Phase 1 data pipeline build.
- **SHAP + NumPy 2.x compatibility:** SHAP 0.50 may not work with NumPy 2.4. Test before committing to SHAP for factor explanations. Fallback: manual contribution decomposition (models already expose component scores).
- **Backtesting pass/fail criteria:** With only 6 US episodes, what constitutes a "passing" backtest is subjective. The suggested 4/6 detection + quiet period check is reasonable but needs discussion during Phase 3 planning.
- **APScheduler in Streamlit process lifecycle:** Running the scheduler inside the Streamlit app has edge cases. May need a separate scheduling process. Resolve during Phase 4.
- **pandas 2.x vs 3.0 decision:** pandas 3.0 has breaking changes. Pin to 2.2.x for stability or test 3.0 compatibility early. Decide during Phase 1 setup.
- **PROJECT.md scope tension:** PROJECT.md describes a "bottom-up empirical approach" and says prior models are "loose reference," while the research assumes building the three specific models (Turchin PSI, PLI, Financial Stress). This tension should be resolved during requirements -- either commit to the three models or define the literature-mining discovery process that might produce different ones.

## Sources

### Primary (HIGH confidence)
- Project theory documents: `model-specifications.md`, `critical-review-model-specs.md`, `gap-analysis-literature-review.md`, `revolution-metrics-data-sources.md` -- 250+ pages of domain-specific research
- Existing codebase: `revolution-index/` -- directly inspected Python code (config, data pipeline, 3 models, backtesting, uncertainty, visualization)
- pip package index -- all library versions verified locally on 2026-03-01

### Secondary (MEDIUM confidence)
- Competitor platforms (ACLED, FSI, CoupCast, PRS ICRG, V-Dem) -- training data knowledge, not live-verified
- Architectural patterns for ETL pipelines and composite index systems -- established patterns from training data
- Dashboard framework capabilities (Streamlit, Plotly) -- training data, verify specific features during implementation

### Tertiary (LOW confidence)
- SHAP 0.50 + NumPy 2.x compatibility -- untested, needs verification
- APScheduler behavior inside Streamlit process -- known edge cases, needs testing
- pandas 3.0 migration impact -- breaking changes documented but not tested against this project

---
*Research completed: 2026-03-01*
*Ready for roadmap: yes*
