# Revolution Probability Tracker

**Status:** detailed
**Created:** 2026-03-01
**Tech Stack:** Python, Astro, Chart.js, D3.js, GitHub Actions, Cloudflare Pages

## One-Liner
A public web dashboard that displays a data-driven probability score for revolution in the United States, built bottom-up from empirical data and AI-assisted pattern discovery.

## Problem / Motivation
There's no accessible, data-driven tool that answers the question ordinary people are increasingly asking: "How unstable is the US, really?" Public discussion about political instability is driven by gut feelings, partisan narratives, and punditry — not data. Academic research on revolution prediction exists but is locked in journals and never synthesized into something a general audience can use.

This project takes a bottom-up empirical approach: instead of starting from established academic models and fitting data to them, it starts by identifying what data actually predicts instability, determines what's available online, and then builds models from the ground up. The result is a single, clear probability score on a public dashboard that anyone can understand.

## Core Concept
The project follows a four-phase bottom-up methodology:

1. **Data Research** — Survey existing academic literature on revolution prediction and use AI-assisted discovery to identify which variables and conditions historically precede revolutions. Prior research (existing theory docs in this repo) serves as loose reference but doesn't constrain the approach.

2. **Data Sourcing** — Determine which of those identified variables can actually be found online as usable, regularly-updated datasets. The tool is only as good as the data feeding it.

3. **Model Building** — Create and evaluate models that predict revolution probability from the sourced data. Use both literature-informed approaches and AI/ML pattern discovery to find signal.

4. **Website** — Build a public-facing dashboard with charts that displays the probability score and supporting visualizations.

### Revolution Spectrum
Rather than a binary "revolution or not" output, the tool uses a continuous 0-100 scale mapped to a spectrum:
- **Low range**: Stable — no significant instability signals
- **Mid range**: Partial revolution territory — conditions consistent with major reforms, power shifts, or institutional change short of regime replacement
- **High range**: Full revolution territory — conditions consistent with a government being fully overthrown or fundamentally replaced

### Audience
General public. Anyone should be able to land on the site and immediately understand what they're seeing. Clarity and accessibility are as important as analytical rigor.

## Key Features

### Must-Have (v1)
- **Revolution Gauge** — A needle-style fuel gauge (0-100) as the visual centerpiece, with color-coded zones indicating severity levels. Immediately communicates the current score at a glance.
- **Historical Trend Chart** — Line chart showing how the score has evolved over time (weeks, months, years), giving users a sense of direction and momentum.
- **Contributing Factors Breakdown** — Visual breakdown of which data inputs are pushing the score up or down, so users understand *why* the number is what it is.
- **Layered Transparency** — Clean, accessible surface for casual visitors. Expandable sections or a dedicated methodology page for users who want to see raw data sources, model details, and how the score is calculated.
- **Weekly Updates** — Data pulled and score recalculated on a weekly cadence, balancing freshness against engineering complexity.

### Nice-to-Have (Future)
- Email/push alerts when score crosses thresholds
- Public API for researchers and developers
- Embeddable widget for other sites
- Comparison to other countries
- Historical events overlay (mark past crises on the timeline)

## Architecture
The architecture follows a **static-first** pattern. Since data only updates weekly, there's no need for a running server — the entire site is pre-computed static files served from a CDN.

### System Components
```
┌─────────────────┐     ┌──────────────────────┐     ┌─────────────────┐
│  Data Sources    │     │  GitHub Actions       │     │  Cloudflare     │
│  (APIs/datasets) │────>│  (Weekly Cron Job)    │────>│  Pages (CDN)    │
│                  │     │                       │     │                 │
│  - Census APIs   │     │  1. Fetch raw data    │     │  Static site:   │
│  - World Bank    │     │  2. Run Python pipeline│     │  - Astro HTML   │
│  - UN data       │     │  3. Execute model(s)  │     │  - Chart.js     │
│  - FRED          │     │  4. Output JSON       │     │  - D3.js gauge  │
│  - BLS           │     │  5. Commit to repo    │     │  - Data JSON    │
└─────────────────┘     │  6. Trigger deploy    │     └─────────────────┘
                        └──────────────────────┘
```

### Data Flow
1. **Weekly trigger** — GitHub Actions cron fires (e.g., Sunday 2am UTC).
2. **Data fetch** — Python script pulls latest data from source APIs (census, economic indicators, social metrics).
3. **Transform & model** — Pipeline cleans data, runs it through the prediction model(s), produces the revolution probability score and factor weights.
4. **Output** — Results written as JSON files to the repo:
   - `data/current.json` — latest score, factor breakdown, timestamp
   - `data/history.json` — time series of all past scores
   - `data/factors.json` — detailed factor data for drill-down views
5. **Deploy** — Commit triggers Cloudflare Pages rebuild, which builds the Astro site and deploys to CDN.
6. **Serve** — Users hit the Cloudflare Pages URL. Astro site loads JSON data and renders gauge and charts client-side.

### Key Design Decisions
- **Static over dynamic**: Weekly updates mean no live server is needed. Pre-computed JSON eliminates backend complexity and keeps hosting free.
- **JSON in repo**: Data volume is tiny (~52 entries/year). Git provides free version history and audit trail. Migration to object storage is trivial if ever needed.
- **Pipeline in CI**: GitHub Actions runs the Python analysis in the cloud. No local infrastructure to maintain. 2,000 free minutes/month covers the weekly job easily.
- **CDN-served frontend**: Cloudflare Pages provides global CDN, automatic HTTPS, and zero-config deploys from the repo.
- **Model interpretability**: Still an open question (see Open Questions), but the architecture supports both interpretable models (factor weights in JSON) and black-box models with post-hoc explanation layers.

## Tech Stack Notes

### Data Pipeline & Analysis: Python
Best ecosystem for the job: `pandas` for data manipulation, `requests` for API calls, `scikit-learn` and custom models for prediction. Huge library support for Census, World Bank, and UN data APIs. Aligns with the AI/ML modeling requirements from the research phase.

### Frontend Framework: Astro
Static-first architecture — outputs plain HTML by default, which is ideal for a site that's mostly static content with a few interactive elements. Astro's "islands" architecture lets interactive components (gauge, charts) hydrate independently without shipping a full JS framework to the browser. Native Cloudflare Pages deployment support. Component-based structure keeps code organized as the site grows (methodology page, about page, data explorer).

### Data Visualization: Chart.js + D3.js
**Chart.js** for standard visualizations: historical trend line chart, contributing factors bar/breakdown chart. Simple API, responsive out of the box, good defaults. **D3.js** (or custom SVG) for the **needle gauge** — the signature visual element that needs custom rendering beyond what charting libraries offer.

### CI/CD: GitHub Actions
Weekly cron schedule triggers the data pipeline. 2,000 free minutes/month on the free tier — a weekly Python job uses a tiny fraction. Handles the full workflow: fetch data, run model, write JSON, commit, trigger deploy.

### Hosting: Cloudflare Pages
Free tier covers this use case entirely (static site + CDN). Automatic deploys on repo push. Global CDN, automatic HTTPS, custom domain support. No server to manage, no uptime to monitor.

### Data Storage: JSON files in the repo
One score per week means a few kilobytes per year. Git history provides a complete audit trail for free. Frontend fetches JSON as static assets — no API layer needed. Simple to inspect, debug, and validate.

## Open Questions

### Critical (could kill the project)
- **Data availability**: The bottom-up approach depends on finding usable, regularly-updated datasets for the variables that matter. If the predictive variables identified in the research phase turn out to be unmeasurable or locked behind paywalls, the project stalls. Mitigation: the data sourcing phase exists specifically to confront this early before any modeling or building starts.

### Important (shape the design)
- **What counts as a training dataset?** AI-assisted discovery needs labeled examples of revolutions with preceding conditions. Which existing conflict/instability dataset to use (NAVCO, PITF, UCDP, custom compilation) is an open research question.
- **Revolution definition calibration**: The 0-100 spectrum is defined conceptually (stable → partial → full revolution), but where exactly to draw the zone boundaries requires empirical grounding from the data.
- **Model interpretability vs. accuracy**: The factor breakdown feature requires an interpretable model, but the best-performing model might be a black box. May need an ensemble approach or may need to sacrifice some accuracy for explainability.
- **Validation**: How do you validate a revolution prediction model for a country that hasn't had one? Cross-country validation, historical backtesting, and out-of-sample testing are all imperfect.
- **Responsible communication**: Showing "revolution probability" to a general public audience carries risks — could be misinterpreted, cause panic, or be weaponized by bad actors. Need to think about framing, disclaimers, and how to communicate uncertainty.

### Deferred (decide later)
- Gauge color zones and threshold labels — depends on where empirical data places the zone boundaries on the 0-100 spectrum

### Resolved (previously deferred)
- ~~Frontend framework and charting library~~ → Astro + Chart.js + D3.js for the gauge
- ~~Hosting platform and cost model~~ → Cloudflare Pages (free tier)
- ~~Data storage approach~~ → JSON files committed to the repo
- ~~Update pipeline architecture~~ → Static site with pre-computed JSON via GitHub Actions cron

## References & Inspiration
- Prior research in this repo (Revolution Index Research) as loose reference
- No specific existing tool identified as a direct model — this aims to fill a gap rather than replicate something
