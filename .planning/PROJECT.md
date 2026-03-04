# Revolution Probability Tracker

## What This Is

A data-driven research dashboard that calculates and displays a probability score for revolution in the United States. Built bottom-up from empirical data using AI-assisted literature mining to identify predictive variables, then sourcing freely available datasets and building models to produce a single interpretable score. V1 is a personal research tool; public-facing dashboard comes later.

## Core Value

Produce a defensible, data-backed revolution probability score from freely available data — one number that synthesizes what academic research says matters into something actionable and understandable.

## Current Milestone: v1.1 Build & Validate

**Goal:** Implement data pipeline, build scoring model(s) from the 45-variable catalog, and validate against historical episodes to produce a defensible political stress score.

**Target features:**
- Data pipeline fetching from 25+ free sources with LOCF frequency alignment
- Model architecture selection informed by literature mining (45 variables, 14 Strong-rated)
- Working 0-100 political stress score with interpretable factor breakdowns
- Backtesting against 6+ historical episodes (1968-2020)
- Sensitivity analysis and uncertainty quantification
- Validation report with honest pass/fail assessment

## Requirements

### Validated

<!-- Shipped and confirmed valuable in v1.0. -->

- ✓ AI-assisted literature mining to identify variables that historically precede revolutions — v1.0 Phase 2
- ✓ Ranked variable catalog with evidence strength ratings and source papers — v1.0 Phase 2
- ✓ Data sourcing audit — which predictive variables are freely available online as regularly-updated datasets — v1.0 Phase 3
- ✓ Prior work validation — 3 models audited, math fixes documented, 18 data series verified — v1.0 Phase 1

### Active

<!-- Current scope for v1.1. Building toward these. -->

- [ ] Model(s) that compute a 0-100 revolution probability score from sourced data
- [ ] Automated data pipeline fetching from all identified free sources
- [ ] Backtesting and validation against historical crisis/quiet episodes
- [ ] Sensitivity analysis and uncertainty quantification
- [ ] Score interpretation with severity tiers and factor breakdowns

### Out of Scope

- Paywalled or commercial datasets — free data only, skip variables that aren't freely accessible
- Public-facing site — v1 is a personal research dashboard, public framing/disclaimers come later
- Email/push alerts — future feature
- Public API — future feature
- Multi-country comparison — US-only for v1
- Mobile app — web dashboard only
- Real-time updates — weekly cadence is sufficient

## Context

- **Prior research:** ~250 pages of theory docs exist in this repo (Turchin PSI, Prospect Theory PLI, Financial Stress Pathway models). These serve as loose reference — the project doesn't adopt them wholesale but may draw inspiration from variables they identified.
- **Prior code:** A `revolution-index/` Python project exists with FRED API integration, normalization, backtesting. This is prior exploratory work, not the foundation for the new project.
- **Known free data sources from prior work:** FRED API (17 economic series), WID.world (inequality data). These are candidates but not pre-committed.
- **Academic datasets to investigate:** NAVCO, PITF, UCDP, and others for labeled revolution/instability events as training data.
- **AI-assisted discovery:** Using LLMs to read and synthesize academic papers on revolution prediction to extract predictive variables — not ML-based feature discovery on raw data.

## Constraints

- **Data**: Free/open data sources only — FRED, World Bank, WID.world, similar. No paywalls.
- **Timeline**: MVP fast — get to a working score as quickly as possible, then iterate on model quality.
- **Modeling**: Python is the natural fit for data pipeline and modeling work.
- **Interpretability**: Factor breakdown feature requires the model to explain which inputs drive the score. Rules out pure black-box approaches.
- **V1 scope**: Research dashboard for personal use. No public audience concerns in v1.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Bottom-up empirical approach over adopting prior models | Prior work identified signal but this project should discover what matters independently | — Pending |
| Free data only | Removes paywall blockers; if a variable isn't freely available, skip it | — Pending |
| Literature mining via LLM (not ML feature discovery) | AI role is synthesizing papers, not crunching raw data for features | — Pending |
| V1 as research tool, not public site | Removes responsible communication concerns from v1 scope | — Pending |
| MVP-fast timeline | Get a working score quickly, iterate on quality later | — Pending |

---
*Last updated: 2026-03-03 after milestone v1.1 start*
