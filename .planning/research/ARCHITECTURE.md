# Architecture Patterns

**Domain:** Data-driven political instability index / composite score dashboard
**Researched:** 2026-03-01

## Recommended Architecture

### Overview

A **batch-oriented data pipeline** with a **layered architecture**: data ingestion at the bottom, transformation and alignment in the middle, model computation above that, score storage/persistence, and a frontend dashboard on top. This is a classic ETL-to-dashboard pattern, not a microservices system. The project is a personal research tool with weekly batch updates, so keep it simple: a Python pipeline that writes to local storage, and a lightweight web dashboard that reads from it.

The existing `revolution-index/` codebase already has solid scaffolding for layers 1-3 (ingestion, transformation, computation). The new project should learn from that code's strengths (clean separation of concerns, centralized config, base model pattern) while addressing its documented bugs (critical-review-implementation.md) and adding the missing layers (persistence, scheduling, dashboard).

```
+------------------------------------------------------------------+
|                      FRONTEND DASHBOARD                          |
|  Gauge + Trend Chart + Factor Breakdown + Model Comparison       |
+------------------------------------------------------------------+
        |  reads from                            |  reads from
        v                                        v
+---------------------------+    +---------------------------+
|   SCORE STORE (JSON/DB)   |    |  HISTORICAL STORE (Parq)  |
|   Latest composite score  |    |  Full time series for     |
|   + per-model scores      |    |  all models, components,  |
|   + component breakdowns  |    |  and raw indicators       |
|   + metadata/timestamps   |    |                           |
+---------------------------+    +---------------------------+
        ^  writes                        ^  writes
        |                                |
+------------------------------------------------------------------+
|                    MODEL COMPUTATION LAYER                        |
|  Turchin PSI | Prospect Theory PLI | Financial Stress Pathway    |
|  Ensemble combiner | Uncertainty quantification                  |
+------------------------------------------------------------------+
        ^  reads aligned data
        |
+------------------------------------------------------------------+
|                 TRANSFORMATION / ALIGNMENT LAYER                 |
|  Frequency alignment (LOCF) | Derived series | Normalization    |
|  Data quality / freshness tracking                               |
+------------------------------------------------------------------+
        ^  reads raw data
        |
+------------------------------------------------------------------+
|                    DATA INGESTION LAYER                           |
|  FRED API client | WID.world loader | (Future: World Bank, etc)  |
|  Rate limiting | Local CSV caching | Staleness detection         |
+------------------------------------------------------------------+
        ^  fetches from
        |
+------------------------------------------------------------------+
|                    EXTERNAL DATA SOURCES                          |
|  FRED API (17 series) | WID.world API/CSV (1 series)            |
+------------------------------------------------------------------+
```

### Component Boundaries

| Component | Responsibility | Communicates With | State Owned |
|-----------|---------------|-------------------|-------------|
| **FRED Client** | Fetches raw time series from FRED API. Rate-limiting. Local CSV caching with staleness detection. | FRED API (outbound HTTP), raw data cache (filesystem) | `data/raw/fred/*.csv` |
| **WID Loader** | Fetches top-1% income share from WID.world API or manual CSV. | WID API (outbound HTTP), raw data cache (filesystem) | `data/raw/wid/*.csv` |
| **Data Pipeline** | Aligns mixed-frequency data to monthly timeline via LOCF. Computes derived series (real wage change). Tracks freshness metadata. Produces unified monthly DataFrame. | Raw data cache (reads), processed data store (writes) | `data/processed/unified_monthly.parquet`, `data/processed/freshness_metadata.parquet` |
| **Normalization** | Percentile rank, min-max, z-score functions against reference distributions. Stateless utility. | Called by models | None (stateless) |
| **Turchin PSI Model** | Computes structural-demographic Political Stress Indicator from 3 components (MMP, EMP, SFD) via geometric mean. | Data pipeline output (reads) | None (stateless) |
| **Prospect Theory PLI** | Computes Perceived Loss Index across 5 life domains using prospect theory value function. | Data pipeline output (reads) | None (stateless) |
| **Financial Stress Pathway** | Computes 2-stage financial-to-economic stress transmission. Weighted z-score composites. Lag analysis. | Data pipeline output (reads) | None (stateless) |
| **Ensemble Combiner** | Weighted average of 3 model scores. Divergence alerting. | Model outputs (reads) | None (stateless) |
| **Uncertainty Engine** | Bootstrap parameter perturbation for confidence intervals. | Models (instantiates with varied params) | None (stateless) |
| **Backtester** | Evaluates models against historical episodes and quiet periods. Sensitivity, specificity, inter-model correlation. | Model outputs (reads), config (episodes) | None (stateless) |
| **Score Store** | Persists latest and historical scores. Source of truth for dashboard. | Computation layer (writes), dashboard (reads) | `data/scores/latest.json`, `data/scores/history.parquet` |
| **Scheduler** | Triggers weekly pipeline run (ingest, transform, compute, store). | All pipeline components (orchestrates) | Cron/task scheduler state |
| **Dashboard** | Web-based read-only display: gauge, trend chart, factor breakdown, data freshness. | Score store (reads) | None (read-only) |
| **Config** | Central source of truth for all series IDs, model parameters, thresholds, weights, backtesting episodes. | All components (reads) | `config.py` (or `config.yaml`) |

### Data Flow

**Weekly batch pipeline (happy path):**

```
1. SCHEDULER triggers pipeline run (cron job or manual)
       |
2. INGEST: FRED Client fetches 17 series (skips if cache < 7 days old)
   INGEST: WID Loader fetches 1 series
       |
3. TRANSFORM: Data Pipeline reads raw CSVs
   -> Aligns all series to monthly frequency (LOCF for upsampling, averaging for downsampling)
   -> Computes derived series (real_wage_change = CES0500000003 / CPIAUCSL, YoY)
   -> Tracks freshness metadata (months since last actual observation per series)
   -> Writes unified_monthly.parquet
       |
4. COMPUTE: Each model reads unified_monthly.parquet
   -> TurchinPSI.compute(data, latest_date) -> ModelOutput (score, MMP/EMP/SFD, flags)
   -> ProspectTheoryPLI.compute(data, latest_date) -> ModelOutput (score, domain losses, flags)
   -> FinancialStressPathway.compute(data, latest_date) -> ModelOutput (score, FSSI/ETI, flags)
       |
5. ENSEMBLE: Weighted average of 3 model scores
   -> Divergence check (alert if models disagree by >20 points)
   -> Uncertainty: bootstrap_all_models() for 95% CI
       |
6. STORE: Write latest composite + per-model scores to latest.json
   Append to history.parquet
       |
7. DASHBOARD: Reads latest.json and history.parquet on page load
   -> Renders gauge, trend chart, factor breakdown
```

**Data freshness cascade:** Each FRED series updates at different frequencies (daily VIX vs. annual life expectancy). The pipeline's freshness tracking tells the dashboard which components are based on recent data vs. carried-forward values. The dashboard should display freshness alongside scores, not hide it.

**Historical backfill (one-time on setup):**

```
1. INGEST: Fetch all series with start date = 1947-01-01
2. TRANSFORM: Build full unified_monthly.parquet
3. COMPUTE: compute_historical() for each model over full date range
4. VALIDATE: Run Backtester.full_report() against historical episodes
5. STORE: Write full history.parquet
```

## Patterns to Follow

### Pattern 1: Config-Driven Data Catalog

**What:** Define all external series, their frequencies, model assignments, component roles, and inversion flags in a single config file. Models discover their inputs from config, not hardcoded constants.

**When:** Always. The existing `config.py` already does this well, but the financial stress model's ETI weights diverge from config (documented bug A3 in critical-review-implementation.md). Fix this.

**Why:** Adding a new data source should require changing one file, not hunting through model code. Data catalog changes should be testable in isolation.

**Example:**
```python
# config.py — single source of truth
FRED_SERIES = {
    "UNRATE": {
        "description": "Civilian unemployment rate",
        "frequency": "monthly",
        "model": "financial_stress",
        "component": "eti",
        "invert": False,
        "weight": 0.25,  # Move weights INTO the catalog, not models
    },
}
```

### Pattern 2: Stateless Models, Stateful Pipeline

**What:** Models are pure functions: `(data, date, params) -> ModelOutput`. They hold no state between calls. All statefulness lives in the data pipeline (caching, freshness tracking) and score store (persistence).

**When:** Always. The existing `BaseModel` pattern already enforces this cleanly.

**Why:** Makes backtesting trivial (same model, different dates). Makes uncertainty quantification clean (same model, different params). Makes testing easy (mock data in, check output).

**Example:**
```python
# Good: stateless model
class TurchinPSI(BaseModel):
    def compute(self, data: pd.DataFrame, date: pd.Timestamp) -> ModelOutput:
        # Pure function of inputs
        ...

# Bad: model with internal state
class BadModel:
    def __init__(self):
        self.last_score = None  # State! Breaks backtesting.
    def compute(self, data):
        self.last_score = ...
```

### Pattern 3: Structured Model Output

**What:** Every model returns a `ModelOutput` dataclass with: score (0-100), confidence interval, component breakdown dict, data quality metadata, and alert flags. Uniform interface regardless of model internals.

**When:** Always. The existing `ModelOutput` dataclass is well-designed.

**Why:** The ensemble combiner, backtester, uncertainty engine, and dashboard all consume model outputs. A common interface means adding a new model requires only implementing `compute()` -- everything downstream works automatically.

### Pattern 4: LOCF Alignment with Freshness Tracking

**What:** Mixed-frequency data (daily VIX, monthly unemployment, annual income share) is aligned to a common monthly timeline. High-frequency data is downsampled by averaging. Low-frequency data is upsampled via Last Observation Carried Forward (LOCF). Every value in the unified dataset tracks how many months stale it is.

**When:** For all multi-frequency data alignment. Never use linear interpolation for economic data (it implies knowledge of intermediate values that does not exist).

**Why:** Critical review B1: "step function is more honest than linear interpolation." Annual data (e.g., top 1% income share) forward-filled for 12 months should be flagged as increasingly stale, not presented as current.

### Pattern 5: Separate Latest vs. Historical Score Storage

**What:** Maintain two stores: (1) `latest.json` -- a small JSON file with the current composite score, per-model scores, component breakdowns, timestamps, and data freshness metadata. (2) `history.parquet` -- a Parquet file with the full historical time series of all scores and components.

**When:** Always. The dashboard needs both fast-loading current state (JSON, <1KB) and efficient historical data for charts (Parquet, compressed columnar).

**Why:** The dashboard should load the current score instantly (one JSON read) and load historical charts asynchronously. Parquet is the right format for time series -- it compresses well, supports column selection, and reads into pandas with zero conversion overhead.

**Example `latest.json` structure:**
```json
{
  "computed_at": "2026-03-01T08:00:00Z",
  "composite": {
    "score": 47.3,
    "ci_lower": 38.1,
    "ci_upper": 55.8,
    "label": "elevated",
    "flags": ["FINANCIAL_STRESS_NOT_YET_TRANSMITTED"]
  },
  "models": {
    "turchin_psi": {
      "score": 62.1,
      "components": {"MMP": 58.3, "EMP": 71.0, "SFD": 57.8},
      "flags": []
    },
    "prospect_theory": {
      "score": 38.2,
      "components": {"wages_loss": 22.0, "housing_loss": 45.1, "...": "..."},
      "flags": []
    },
    "financial_stress": {
      "score": 41.5,
      "components": {"FSSI": 55.2, "ETI": 27.8},
      "flags": ["FINANCIAL_STRESS_NOT_YET_TRANSMITTED"]
    }
  },
  "data_freshness": {
    "most_recent_update": "2026-02-28",
    "stalest_series": {"id": "SPDYNLE00INUSA", "months_stale": 14, "description": "Life expectancy"},
    "series_count": 18,
    "series_current": 15
  }
}
```

### Pattern 6: Dashboard Reads Files, Not Databases

**What:** For a V1 personal research dashboard, skip the database entirely. The dashboard reads `latest.json` (current score) and `history.parquet` (trend charts) directly from the filesystem. No PostgreSQL, no Redis, no ORM.

**When:** For V1 with a single user and weekly updates. Add a database when/if the project goes public (multi-user, concurrent writes, API access).

**Why:** A database adds deployment complexity, operational overhead, and migration burden for zero benefit when there is one user and one writer. A JSON file and a Parquet file are the entire "database." The pipeline writes them, the dashboard reads them. Done.

## Anti-Patterns to Avoid

### Anti-Pattern 1: Premature Microservices

**What:** Splitting the pipeline into separate services (data service, model service, API service, frontend service) with HTTP/gRPC between them.

**Why bad:** This is a single-user research tool with weekly batch updates. Microservices add network hops, deployment complexity, distributed system failure modes, and observability requirements -- all for zero benefit when everything runs on one machine. The pipeline is inherently sequential (ingest -> transform -> compute -> store) with no need for independent scaling.

**Instead:** One Python package with clear module boundaries (the existing `src/data/`, `src/models/`, `src/analysis/` structure is correct). One process runs the full pipeline. One process serves the dashboard. They share a filesystem.

### Anti-Pattern 2: Real-Time Architecture for Batch Workloads

**What:** Using WebSockets, streaming data, event-driven architecture, or message queues for a system that updates weekly.

**Why bad:** The underlying data sources (FRED, WID.world) update on daily-to-annual schedules. The most frequent is daily (VIX, yield curve). Weekly batch runs capture all updates with days to spare. Real-time infrastructure adds complexity for a cadence that a cron job handles perfectly.

**Instead:** A cron job (or `schedule` library, or OS task scheduler) triggers the pipeline once per week. The dashboard reloads data on page load. If a user wants to see the latest score, they refresh the page.

### Anti-Pattern 3: Shared Mutable DataFrame State

**What:** Passing a single mutable DataFrame through the pipeline where each model modifies it in place (adding columns, mutating values).

**Why bad:** Makes the computation order-dependent. Model B's results change if Model A ran first and added columns. Debugging becomes impossible when you cannot tell which component modified a value.

**Instead:** The existing pattern is correct: the Data Pipeline produces an immutable unified DataFrame. Each model receives it read-only and returns a ModelOutput. The ensemble combiner reads ModelOutputs. No component modifies the unified data.

### Anti-Pattern 4: Database-Per-Model Score Storage

**What:** Each model writing its own output files in its own format to its own location.

**Why bad:** The dashboard and ensemble combiner need to read all model outputs together. If each model has its own storage format, the dashboard becomes a multi-format parser. Versioning and rollback become model-specific.

**Instead:** One score store module handles all persistence. Models return `ModelOutput` objects. The store module serializes them consistently.

### Anti-Pattern 5: Coupling Dashboard Framework to Data Computation

**What:** Running model computations inside dashboard request handlers (e.g., computing the score on page load).

**Why bad:** Model computation can take minutes (especially with bootstrap uncertainty). The dashboard would be unresponsive during computation. The user's browser refresh triggers expensive API calls to FRED.

**Instead:** Strict separation: the batch pipeline runs independently (scheduled or manual). It writes results to the score store. The dashboard only reads from the score store. The dashboard never imports model code.

## Component Interaction Matrix

Shows which components depend on which others. Read as "row depends on column."

|                     | Config | FRED Client | WID Loader | Data Pipeline | Normalization | Models | Ensemble | Uncertainty | Backtester | Score Store | Dashboard |
|---------------------|--------|-------------|------------|---------------|---------------|--------|----------|-------------|------------|-------------|-----------|
| **Config**          | --     |             |            |               |               |        |          |             |            |             |           |
| **FRED Client**     | YES    | --          |            |               |               |        |          |             |            |             |           |
| **WID Loader**      | YES    |             | --         |               |               |        |          |             |            |             |           |
| **Data Pipeline**   | YES    |             |            | --            |               |        |          |             |            |             |           |
| **Normalization**   |        |             |            |               | --            |        |          |             |            |             |           |
| **Models**          | YES    |             |            |               | YES           | --     |          |             |            |             |           |
| **Ensemble**        | YES    |             |            |               |               | YES    | --       |             |            |             |           |
| **Uncertainty**     | YES    |             |            |               |               | YES    |          | --          |            |             |           |
| **Backtester**      | YES    |             |            |               |               | YES    |          |             | --         |             |           |
| **Score Store**     |        |             |            |               |               |        | YES      | YES         |            | --          |           |
| **Dashboard**       |        |             |            |               |               |        |          |             |            | YES         | --        |

Key insight: **The dashboard depends ONLY on the score store.** It has zero transitive dependency on data ingestion, transformation, or model computation. This is the critical boundary that keeps the system simple.

## Suggested Build Order

Based on the dependency matrix above, the natural build order is bottom-up:

### Phase 1: Data Foundation (no dependencies except external APIs)
1. **Config** -- series catalog, model params, thresholds
2. **FRED Client** -- API integration with caching
3. **WID Loader** -- API integration with caching
4. **Data Pipeline** -- frequency alignment, LOCF, derived series, quality report

*Rationale:* Everything downstream depends on having aligned data. Cannot validate models without data. The existing codebase has most of this done but needs bug fixes from critical-review-implementation.md.

### Phase 2: Model Computation (depends on Phase 1)
5. **Normalization utilities** -- percentile rank, z-score, min-max
6. **Base Model interface** -- ModelOutput dataclass, BaseModel ABC
7. **Three models** -- Turchin PSI, Prospect Theory PLI, Financial Stress Pathway
8. **Ensemble combiner** -- weighted average, divergence detection

*Rationale:* Models are the intellectual core but worthless without data. Build and validate each model individually against historical episodes before combining.

### Phase 3: Validation (depends on Phases 1-2)
9. **Backtesting framework** -- episode detection, quiet period assessment, distribution checks
10. **Uncertainty quantification** -- bootstrap parameter perturbation
11. **Historical backfill** -- compute full time series for all models

*Rationale:* Must validate models produce meaningful signal before building a dashboard. This phase answers "do these models actually detect historical crises?" If not, iterate on models before proceeding.

### Phase 4: Persistence and Scheduling (depends on Phases 1-3)
12. **Score Store** -- write latest.json and history.parquet
13. **Pipeline orchestrator** -- single entry point that runs ingest -> transform -> compute -> store
14. **Scheduler** -- weekly cron job or task scheduler

*Rationale:* Only after models are validated does it make sense to persist scores and schedule updates. The orchestrator is the "glue" script that ties all components together.

### Phase 5: Dashboard (depends on Phase 4)
15. **Dashboard backend** -- serve latest.json and history.parquet as API endpoints
16. **Dashboard frontend** -- gauge, trend chart, factor breakdown, data freshness display

*Rationale:* Dashboard is the last thing built because it depends on everything else. It is also the least risky -- standard web development with well-understood patterns. The hard problems are all in Phases 1-3.

### Critical Path

```
Config -> FRED Client -> Data Pipeline -> Models -> Backtesting -> Score Store -> Dashboard
                   \                         |
                    WID Loader -------->-----+
```

The longest dependency chain runs through data ingestion and model validation. Dashboard work cannot begin until the score store exists and has data in it. However, dashboard **design** (wireframes, component selection) can happen in parallel with Phases 1-3.

## Technology Decisions with Architectural Implications

| Decision | Choice | Architectural Impact |
|----------|--------|---------------------|
| Data storage format | Parquet for time series, JSON for latest score | No database needed. Dashboard reads files directly. |
| Dashboard framework | To be decided -- but must support reading Parquet and rendering charts | If Python: Streamlit or Panel (read Parquet natively). If JS: need an API layer. |
| Scheduler | OS-level cron (Linux) or Task Scheduler (Windows) | No orchestration framework needed. Pipeline is one Python script. |
| Model interface | ABC with `compute(data, date) -> ModelOutput` | New models slot in by implementing one method. Ensemble/backtesting work automatically. |
| Normalization reference period | Expanding window from 1970 to current date | All models share the same historical baseline. Scores are comparable across models. |

## Scalability Considerations

| Concern | V1 (1 user) | Future (public dashboard) | Notes |
|---------|-------------|---------------------------|-------|
| Data volume | ~18 series x 600 months = ~11K data points | Same (data doesn't grow with users) | Parquet handles this trivially |
| Computation time | ~10 sec for full historical backfill, <1 sec for single date | Same (computation is user-independent) | Bootstrap uncertainty is the bottleneck (~30 sec for 500 samples x 3 models) |
| Concurrent reads | 1 | Many | V1: file reads. Future: add a read-only API layer or CDN for static JSON |
| Score storage | ~1 MB total | Same | Even 50 years of monthly scores at 18 columns is tiny |
| Dashboard serving | `python -m http.server` or Streamlit | Proper web server (nginx + gunicorn, or static site on CDN) | The score data is pre-computed; serving is cheap |
| API access | Not needed | Add FastAPI or similar thin layer over score store | The pipeline and API are separate processes; API is read-only |

The system fundamentally does not have scaling problems. The data is small (18 time series), the computation is fast (<1 minute even with uncertainty), and the output is tiny (<1MB). The only scaling concern is concurrent dashboard reads, which is trivially solved by serving pre-computed static files.

## Sources

- Existing codebase: `revolution-index/` (config.py, src/data/, src/models/, src/analysis/, src/visualization/) -- HIGH confidence, direct inspection
- Prior theory documents: model-specifications.md, critical-review-model-specs.md, critical-review-implementation.md -- HIGH confidence, project-specific
- Data source inventory: revolution-metrics-data-sources.md -- HIGH confidence, project-specific
- Architectural patterns: training data knowledge of ETL pipeline architecture, composite index systems (e.g., Fragile States Index, Human Development Index), batch data processing patterns -- MEDIUM confidence (training data, not verified against current sources due to web access restrictions)
- Dashboard architecture: training data knowledge of Streamlit, Panel, Plotly Dash for Python data dashboards -- MEDIUM confidence (training data, verify specific library capabilities during implementation phase)
