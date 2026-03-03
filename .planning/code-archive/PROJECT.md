# Revolution Index

## What This Is

A public web dashboard that displays a data-driven revolution probability score for the United States. The site presents a single, clear 0-100 score via an interactive needle gauge, supported by historical trend charts and a breakdown of contributing factors. Built as a static site with mock data for v1 — designed so a real data pipeline can slot in later without changing the frontend.

## Core Value

A visitor lands on the site and immediately understands the current revolution probability score, what's driving it, and how it's been trending — no jargon, no clicks, no friction.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] Revolution gauge (needle-style, 0-100, color-coded zones)
- [ ] Historical trend chart (line chart of score over time)
- [ ] Contributing factors breakdown (visual display of what drives the score)
- [ ] Methodology page with placeholder structure (expandable sections, "coming soon" content)
- [ ] Responsive design (works on desktop and mobile)
- [ ] Mock data system (realistic JSON structure matching future pipeline output)
- [ ] Deployed and publicly accessible on Cloudflare Pages
- [ ] Clean, accessible design for general public audience

### Out of Scope

- Data research and sourcing — separate workstream, not part of this build
- Prediction model building — separate workstream
- GitHub Actions pipeline for real data — will be added after model exists
- Email/push alerts — future feature
- Public API — future feature
- Embeddable widget — future feature
- Country comparisons — future feature
- Real methodology content — depends on model decisions not yet made

## Context

This is the website phase of a larger four-phase project (research → data sourcing → model building → website). The research and modeling work happens separately. This build focuses exclusively on the public-facing dashboard.

The site architecture is static-first: data updates weekly, so there's no need for a running server. The JSON data format established here becomes the contract that the future pipeline must produce. Getting the data structure right matters even with mock data.

An existing spec sheet (`spec.md`) in the repo documents the full project vision, architecture decisions, and tech stack rationale. It covers the broader project beyond just this website build.

## Constraints

- **Hosting**: Cloudflare Pages free tier — static files only, no server-side logic
- **Budget**: Zero. All tools and services must be free tier
- **Tech stack**: Astro (static site generator), Chart.js (standard charts), D3.js or custom SVG (needle gauge), JSON flat files for data
- **Data**: Mock/placeholder data only for v1. Must define a clean JSON schema that a real pipeline can produce later
- **Audience**: General public — design for clarity and accessibility, not data scientists

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Static-first architecture | Data updates weekly, no server needed. Keeps hosting free and simple | — Pending |
| Astro for frontend | Static HTML output by default, islands for interactive charts, native Cloudflare Pages support | — Pending |
| Chart.js + D3.js split | Chart.js for standard charts (simple API), D3.js/custom SVG for the custom gauge element | — Pending |
| JSON files in repo | Tiny data volume (~52 entries/year), git provides free version history, simplest possible approach | — Pending |
| Mock data for v1 | Decouples website build from model research. Ship the dashboard, validate the UX, plug in real data later | — Pending |
| Cloudflare Pages hosting | Free CDN, automatic HTTPS, zero-config deploys from repo | — Pending |
| Placeholder methodology content | Real methodology depends on model decisions. Structure the page now, fill content later | — Pending |

---
*Last updated: 2026-03-01 after initialization*
