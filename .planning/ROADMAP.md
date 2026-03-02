# Roadmap: Revolution Index

## Overview

Three phases from empty repo to publicly deployed dashboard. Phase 1 defines the data contract that everything else depends on. Phase 2 builds the full interactive dashboard — gauge, charts, layout, and responsive design — against that contract. Phase 3 adds supporting content and ships to Cloudflare Pages. Because v1 uses mock data, the critical risk is schema drift: the JSON shape defined in Phase 1 becomes a binding contract for Phase 2 and, eventually, the real data pipeline.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [x] **Phase 1: Foundation and Data Contract** - Scaffold the Astro project and define the JSON schema that all visualizations depend on
- [ ] **Phase 2: Dashboard** - Build the complete interactive dashboard with gauge, charts, layout, and responsive design
- [ ] **Phase 3: Content and Launch** - Add methodology page and supporting content, then deploy publicly on Cloudflare Pages

## Phase Details

### Phase 1: Foundation and Data Contract
**Goal**: The JSON data schema is locked and the project can be built against it
**Depends on**: Nothing (first phase)
**Requirements**: DATA-01, DATA-02, DATA-03, DATA-04, DATA-05
**Success Criteria** (what must be TRUE):
  1. Three JSON files exist in `public/data/` (current.json, history.json, factors.json) with realistic mock data
  2. TypeScript interfaces in `src/lib/data.ts` match every field in the JSON files — no `any` types
  3. Mock history data contains at least 12 weekly entries so charts will render meaningfully
  4. Schema is documented (inline or README) as the contract a future pipeline must produce
  5. `npm run build` succeeds and outputs a valid `dist/` directory
**Plans**: 1 (01-01-PLAN.md completed 2026-03-01)

### Phase 2: Dashboard
**Goal**: A visitor can land on the site and immediately understand the current score, what's driving it, and how it's been trending
**Depends on**: Phase 1
**Requirements**: DASH-01, DASH-02, DASH-03, DASH-04, DASH-05, DASH-06, DASH-07, SITE-01, SITE-02, SITE-05
**Success Criteria** (what must be TRUE):
  1. Visitor sees a needle gauge with color-coded severity zones and a plain-language zone label (e.g., "Elevated Tension") as the page centerpiece
  2. Current score number and last-updated timestamp are visible without scrolling
  3. Scrolling down reveals a historical trend line chart and a contributing factors breakdown showing 5-6 factors
  4. Page is usable and visually coherent on a 375px mobile screen and a 1440px desktop screen
  5. Page ships minimal JavaScript — charts hydrate client-side; static content requires no JS
**Plans**: TBD

### Phase 3: Content and Launch
**Goal**: The site is publicly accessible with supporting content that establishes credibility and enables social sharing
**Depends on**: Phase 2
**Requirements**: CONT-01, CONT-02, CONT-03, CONT-04, SITE-03, SITE-04
**Success Criteria** (what must be TRUE):
  1. A methodology page exists with expandable sections covering data sources, model approach, score calculation, and limitations — content marked "coming soon" where not yet defined
  2. Dashboard includes visible disclaimer text explaining what the score is and is not
  3. An About section explains the project's purpose and approach
  4. Sharing the site URL on social platforms shows a populated Open Graph card (site name, description, preview image)
  5. Site is live at a `*.pages.dev` URL and loads correctly in a fresh browser with no console errors
**Plans**: TBD

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Foundation and Data Contract | 1/1 | Complete | 2026-03-01 |
| 2. Dashboard | 0/TBD | Not started | - |
| 3. Content and Launch | 0/TBD | Not started | - |
