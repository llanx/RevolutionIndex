# Stack Research

**Domain:** Data-driven political instability prediction dashboard
**Researched:** 2026-03-01
**Confidence:** HIGH (versions verified via pip index; library choices based on strong ecosystem knowledge + project constraints)

## Recommended Stack

### Core Technologies

| Technology | Version | Purpose | Why Recommended |
|------------|---------|---------|-----------------|
| Python | 3.12 | Runtime | Already installed on machine. 3.12 is the stable production target with widespread library support. Avoid 3.13 for now -- some scientific packages lag on new minor versions. |
| pandas | >=2.2,<3.1 | Data manipulation, time series alignment | Industry standard for tabular data. The project's prior code already uses pandas. Version 2.x has Arrow backend for performance. Pin below 3.1 since 3.0 has breaking changes from 2.x -- test before upgrading. |
| NumPy | >=2.0,<3.0 | Numerical computation | Foundation for all scientific Python. 2.x is current stable line (2.4.2 latest). |
| SciPy | >=1.14,<2.0 | Statistical functions (percentile normalization, z-scores, bootstrap) | Provides stats.percentileofscore, stats.zscore, and bootstrap resampling that the models need. |
| Plotly | >=6.0,<7.0 | Interactive charts (gauges, time series, bar charts) | Native Streamlit integration via st.plotly_chart. Plotly 6.x (latest 6.5.2) is current stable. Has built-in gauge (go.Indicator), time series (go.Scatter), and waterfall charts out of the box. |
| Streamlit | >=1.40,<2.0 | Dashboard framework | Fastest path from Python to interactive dashboard. No frontend code needed. Native Plotly support. Multi-page apps, session state, caching, auto-refresh. Ideal for a personal research tool. |
| fredapi | >=0.5.2 | FRED API client | Thin wrapper around FRED REST API. Stable (0.5.2 is latest, rarely changes). Already used in prior code. |
| DuckDB | >=1.3,<2.0 | Local analytical storage | Replaces SQLite/Parquet-file sprawl with a single embedded analytical database. Reads/writes Parquet natively. SQL interface for querying time series. Zero-server, zero-config. |

### Data Pipeline Libraries

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| pyarrow | >=20.0,<24.0 | Parquet I/O, Arrow backend for pandas | Always -- DuckDB and pandas both benefit from Arrow. Latest is 23.0.1. |
| requests | >=2.31 | HTTP client for WID.world and any non-FRED API | For data sources without a dedicated Python client. |
| pydantic | >=2.10,<3.0 | Config validation, data contracts | Validate FRED series configs, model parameters, API responses. Catches config errors at load time instead of runtime. |
| python-dotenv | >=1.0 | Environment variable management | Load FRED_API_KEY from .env file. Simple and proven. |
| wbgapi | >=1.0.14 | World Bank data API | If World Bank indicators are added later. Clean Python interface for WDI. |

### Modeling Libraries

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| scikit-learn | >=1.6,<2.0 | Normalization, preprocessing, potential ensemble methods | QuantileTransformer for percentile normalization, StandardScaler for z-scores, and if any ML-based scoring is added later. Latest is 1.8.0. |
| statsmodels | >=0.14 | Statistical tests, time series analysis | For structural break detection (Chow test), autocorrelation analysis, and backtesting statistical significance. |
| SHAP | >=0.46,<1.0 | Model explainability | Generate factor contribution breakdowns -- "what drove the score this week?" Even works with custom scoring functions via KernelExplainer. Latest is 0.50.0. |

### Development Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| uv | Package management and virtual environments | 10-100x faster than pip. Replaces pip + venv + pip-tools. Use `uv init`, `uv add`, `uv sync`. Latest 0.10.7. |
| ruff | Linting and formatting | Replaces flake8 + black + isort in one tool. ~100x faster than alternatives. Latest 0.15.4. |
| pytest | >=9.0 | Testing | Standard Python test runner. Use with pytest-cov for coverage. |
| pre-commit | Git hooks | Run ruff and pytest before commits. Catches issues early. |
| Jupyter | Exploration notebooks | For data exploration and model prototyping. Keep out of production code path. |

### Scheduling

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| APScheduler | >=3.10,<4.0 | Weekly data refresh scheduling | Run within the Streamlit app or as a standalone cron-like process. 3.x is stable (3.11.2 latest). Note: APScheduler 4.x exists as alpha but is a complete rewrite -- avoid it, stick with 3.x. |

## Installation

```bash
# Initialize project with uv
uv init revolution-tracker
cd revolution-tracker

# Core data pipeline
uv add pandas numpy scipy pyarrow duckdb fredapi requests python-dotenv pydantic

# Modeling
uv add scikit-learn statsmodels

# Dashboard
uv add streamlit plotly

# Scheduling
uv add apscheduler

# Explainability (optional, add when building factor breakdown)
uv add shap

# World Bank (optional, add when expanding data sources)
uv add wbgapi

# Dev dependencies
uv add --dev pytest pytest-cov ruff pre-commit jupyter
```

## Alternatives Considered

| Recommended | Alternative | When to Use Alternative |
|-------------|-------------|-------------------------|
| Streamlit | Dash (4.0.0) | When you need fine-grained control over layout, CSS, multi-user auth, or enterprise deployment. Dash requires writing callbacks (more code) but gives more control. Overkill for a personal research tool. |
| Streamlit | Panel (HoloViz) | When deeply embedded in the HoloViz ecosystem (HoloViews, Bokeh). Panel is powerful but smaller community and less intuitive API than Streamlit. |
| Streamlit | Gradio | When building ML model demos. Not designed for data dashboards. |
| DuckDB | SQLite | When you need broad ORM support or are doing OLTP workloads. SQLite is row-oriented and slow for analytical queries over time series. |
| DuckDB | Raw Parquet files | For the simplest possible setup. But you lose SQL querying, and file management becomes painful as you add more data sources. DuckDB reads Parquet natively so you get both. |
| Plotly | Matplotlib/Seaborn | For static publication-quality figures in papers/notebooks. Not interactive, poor fit for dashboards. |
| Plotly | Altair/Vega-Lite | When you want a declarative grammar-of-graphics API. Good for exploration but gauge charts require workarounds. Plotly has native gauge support. |
| Plotly | ECharts (via streamlit-echarts) | When you need specific chart types Plotly lacks. But adds a third-party Streamlit component dependency. |
| uv | pip + venv | When you must use only stdlib tools. But uv is strictly better in every dimension (speed, lockfile, resolution). |
| uv | Poetry | Poetry is mature but slower than uv and has historically had dependency resolution issues. uv has won the Python packaging race. |
| ruff | flake8 + black + isort | When your organization mandates specific tool configs. Otherwise ruff does all three, faster, in one binary. |
| APScheduler | cron (system) | When running on Linux with root access and wanting OS-level scheduling. Platform-dependent and harder to manage from Python. APScheduler is cross-platform and embeddable. |
| APScheduler | Celery | When you need distributed task queues. Massive overkill for a weekly data refresh on a single machine. |
| Pydantic | dataclasses | When you want stdlib-only and don't need validation. But config validation is critical for this project -- wrong FRED series IDs or parameter ranges should fail loudly. |

## What NOT to Use

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| Flask/Django for dashboard | You would be rebuilding what Streamlit gives you for free. Months of frontend work for a personal tool. | Streamlit |
| React/Next.js frontend | Same problem -- enormous frontend effort for a research dashboard that one person uses. | Streamlit |
| PostgreSQL/MySQL | Server-based databases require setup, maintenance, backups. Total overkill for ~20 time series with weekly updates. | DuckDB (embedded, zero-config) |
| MongoDB | Document store is wrong model for time series data. No analytical query performance. | DuckDB |
| Apache Airflow | Enterprise workflow orchestrator. Requires its own database, web server, scheduler daemon. Absurd for a weekly FRED pull. | APScheduler or a simple Python script on cron/Task Scheduler |
| Prefect/Dagster | Same as Airflow -- powerful but massive overhead for what amounts to "fetch 18 series once a week." | APScheduler |
| TensorFlow/PyTorch | Deep learning frameworks. The project explicitly requires interpretable models. Neural nets are black boxes and overkill for index computation. | scikit-learn + custom scoring functions |
| XGBoost/LightGBM | Gradient boosting is powerful but harder to interpret than the explicit formula-based models this project uses. SHAP can explain them but adds complexity. | Stick with formula-based models (Turchin PSI, Prospect Theory). Use scikit-learn if any ML is needed. |
| Plotly Dash (for charting) | Confusingly, Dash is both a framework AND uses Plotly for charting. You can use Plotly charts inside Streamlit without Dash. Don't conflate the two. | Plotly (the charting library) inside Streamlit |
| Bokeh | Lower-level charting library. More code for equivalent results. Gauge charts require manual construction. | Plotly |
| pip (for package management) | Slow resolution, no lockfile by default, no built-in virtual env management. | uv |
| conda | Heavy, slow, sometimes conflicts with pip packages. Not needed when all dependencies are pip-installable. | uv |

## Stack Patterns by Variant

**If the dashboard stays personal (v1):**
- Use Streamlit Cloud free tier or `streamlit run` locally
- DuckDB file stored in project directory
- APScheduler running inside the Streamlit app process
- No authentication needed

**If the dashboard goes public later (v2+):**
- Deploy Streamlit on a VPS (or Streamlit Cloud with auth)
- Add `streamlit-authenticator` for basic auth
- Move scheduling to a separate process or system cron
- Consider switching to Dash if Streamlit layout limitations become painful
- DuckDB still fine -- it handles concurrent reads well

**If modeling grows beyond formula-based indices:**
- Add scikit-learn pipelines for any ML-based scoring
- Use SHAP for all model explanations to maintain interpretability requirement
- Keep formula-based models as baselines

## Version Compatibility

| Package A | Compatible With | Notes |
|-----------|-----------------|-------|
| pandas 3.0.x | NumPy >=2.0 | pandas 3.0 requires NumPy 2.x. If pinning pandas 2.2.x, NumPy 1.26 also works. |
| Plotly 6.x | Streamlit >=1.40 | Plotly 6 is a major version bump from 5.x. Streamlit 1.40+ has full support via st.plotly_chart. |
| DuckDB 1.x | pyarrow >=14.0 | DuckDB reads Arrow tables natively. No version conflicts observed. |
| scikit-learn 1.8 | NumPy >=2.0, SciPy >=1.9 | Standard scientific stack, well-tested together. |
| SHAP 0.50 | NumPy >=1.20, scikit-learn >=1.0 | SHAP has historically been slow to support newest NumPy. Verify SHAP 0.50 works with NumPy 2.4 before pinning. LOW confidence on this specific compatibility. |
| Streamlit 1.54 | Python 3.9-3.12 | Verified: 3.12 is supported. 3.13 support is likely but unverified. |
| APScheduler 3.11 | Python 3.8+ | Stable, no known conflicts. |

## Confidence Assessment

| Component | Confidence | Verification Method |
|-----------|------------|---------------------|
| Streamlit as dashboard framework | HIGH | Verified version (1.54.0) via pip. Well-established for Python data apps. Dominant in the single-user research tool space. |
| Plotly for visualizations | HIGH | Verified version (6.5.2) via pip. go.Indicator gauge chart is documented and widely used. |
| pandas + NumPy + SciPy core | HIGH | Verified versions via pip. Industry standard, no controversy. |
| DuckDB for storage | HIGH | Verified version (1.4.4) via pip. Proven for analytical workloads. Embedded, zero-config. |
| fredapi for FRED | HIGH | Verified version (0.5.2) via pip. Already used in prior code. Thin stable wrapper. |
| uv for packaging | HIGH | Verified version (0.10.7) via pip. Has become the de facto Python package manager. |
| SHAP for explainability | MEDIUM | Verified version (0.50.0) via pip. NumPy 2.x compatibility needs testing. KernelExplainer for custom functions is documented but can be slow. |
| APScheduler for scheduling | MEDIUM | Verified version (3.11.2). Solid library but scheduling inside Streamlit apps has edge cases (process lifecycle). May need to run as separate process. |
| Pydantic for config | HIGH | Verified version (2.12.5). Standard for data validation in Python. |

## Sources

- pip index versions (all packages) -- verified 2026-03-01 on local machine
- Prior project code: `revolution-index/requirements.txt`, `revolution-index/config.py` -- established fredapi, pandas, numpy, scipy, plotly as working choices
- Project constraints from `.planning/PROJECT.md` -- Python, free data, interpretable models, personal research tool, MVP-fast

---
*Stack research for: Revolution Probability Tracker*
*Researched: 2026-03-01*
