# Requirements: Revolution Index

**Defined:** 2026-03-01
**Core Value:** A visitor lands on the site and immediately understands the current revolution probability score, what's driving it, and how it's been trending

## v1 Requirements

Requirements for initial release. Each maps to roadmap phases.

### Dashboard

- [ ] **DASH-01**: Visitor sees a needle-style gauge (0-100) as the visual centerpiece of the page
- [ ] **DASH-02**: Gauge displays color-coded zones indicating severity levels (e.g., green/yellow/orange/red)
- [ ] **DASH-03**: Each zone has a plain-language label (e.g., "Stable", "Elevated Tension", "Crisis Territory")
- [x] **DASH-04**: Current score is displayed as a prominent number alongside the gauge
- [x] **DASH-05**: Last-updated timestamp is visible near the score
- [ ] **DASH-06**: Visitor sees a historical trend line chart showing score over time (weeks/months)
- [x] **DASH-07**: Visitor sees a contributing factors breakdown showing 5-6 factors pushing the score up or down

### Data Contract

- [x] **DATA-01**: JSON schema is defined for current score data (score, timestamp, zone, factors)
- [x] **DATA-02**: JSON schema is defined for historical score data (time series of past scores)
- [x] **DATA-03**: Mock data files exist in the repo matching the defined schemas
- [x] **DATA-04**: Mock data includes enough data points for charts to render meaningfully (minimum 12 weeks)
- [x] **DATA-05**: JSON schema is documented as the contract for the future data pipeline

### Content

- [ ] **CONT-01**: Methodology page exists with expandable sections and placeholder structure
- [ ] **CONT-02**: Methodology page sections cover: data sources, model approach, score calculation, limitations
- [ ] **CONT-03**: Disclaimer text is visible on the dashboard explaining what the score is and isn't
- [ ] **CONT-04**: About section explains the project's purpose and approach

### Site Infrastructure

- [x] **SITE-01**: Site is responsive and usable on mobile devices (375px+) and desktop
- [x] **SITE-02**: Design meets basic accessibility standards (sufficient color contrast, semantic HTML, screen reader basics)
- [ ] **SITE-03**: Open Graph meta tags are set so shared links display site name, description, and preview image
- [ ] **SITE-04**: Site is deployed and publicly accessible on Cloudflare Pages
- [x] **SITE-05**: Site loads with minimal JavaScript (static HTML by default, JS only for interactive charts)

## v2 Requirements

Deferred to future release. Tracked but not in current roadmap.

### Alerts & Distribution

- **ALRT-01**: User can sign up for email alerts when score crosses thresholds
- **ALRT-02**: Dynamic Open Graph social card showing the live score value

### API & Embedding

- **API-01**: Public REST API for researchers and developers to access score data
- **API-02**: Embeddable widget for other sites to display the current score

### Extended Features

- **EXT-01**: Comparison view against other countries' stability scores
- **EXT-02**: Historical events overlay marking past crises on the timeline chart
- **EXT-03**: Real data pipeline via GitHub Actions replacing mock data

## Out of Scope

| Feature | Reason |
|---------|--------|
| Data research and sourcing | Separate workstream, not part of website build |
| Prediction model building | Separate workstream |
| GitHub Actions data pipeline | Added after model exists; website uses mock data for v1 |
| User accounts / authentication | No user-specific features in v1; adds backend complexity |
| Comment sections | Moderation nightmare for politically charged content |
| Real-time updates | Breaks static architecture; data updates weekly |
| Country comparisons (v1) | Multiplies research scope; deferred to v2 |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| DATA-01 | Phase 1 | Complete (01-01) |
| DATA-02 | Phase 1 | Complete (01-01) |
| DATA-03 | Phase 1 | Complete (01-01) |
| DATA-04 | Phase 1 | Complete (01-01) |
| DATA-05 | Phase 1 | Complete (01-01) |
| DASH-01 | Phase 2 | Pending |
| DASH-02 | Phase 2 | Pending |
| DASH-03 | Phase 2 | Pending |
| DASH-04 | Phase 2 | Complete (02-01) |
| DASH-05 | Phase 2 | Complete (02-01) |
| DASH-06 | Phase 2 | Pending |
| DASH-07 | Phase 2 | Complete (02-01) |
| SITE-01 | Phase 2 | Complete (02-01) |
| SITE-02 | Phase 2 | Complete (02-01) |
| SITE-05 | Phase 2 | Complete (02-01) |
| CONT-01 | Phase 3 | Pending |
| CONT-02 | Phase 3 | Pending |
| CONT-03 | Phase 3 | Pending |
| CONT-04 | Phase 3 | Pending |
| SITE-03 | Phase 3 | Pending |
| SITE-04 | Phase 3 | Pending |

**Coverage:**
- v1 requirements: 21 total
- Mapped to phases: 21
- Unmapped: 0

---
*Requirements defined: 2026-03-01*
*Last updated: 2026-03-01 after 02-01 execution — DASH-04, DASH-05, DASH-07, SITE-01, SITE-02, SITE-05 complete*
