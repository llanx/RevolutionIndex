# Project Research Summary

**Project:** Revolution Index
**Domain:** Static public data visualization dashboard (political instability probability score)
**Researched:** 2026-03-01
**Confidence:** HIGH

## Executive Summary

Revolution Index is a single-metric public dashboard displaying a 0-100 probability score for US political instability, updated weekly. Research across comparable products (CNN Fear & Greed Index, Doomsday Clock, Fragile States Index, Our World in Data, FiveThirtyEight) confirms that expert-built public indexes succeed by leading with one prominent number, providing historical context, explaining contributing factors, and earning trust through visible methodology — even if sparse at launch. The needle gauge format is the right hero visual: cognitively faster than bar charts or raw numbers, instantly familiar from speedometers, and unused by any competing political instability index. The entire product can be built as a fully static site (no server, no database, zero hosting cost) because weekly-cadence data does not require real-time infrastructure.

The recommended stack is Astro 5 (static site generation, islands architecture) + Chart.js 4 (trend + factors charts) + D3.js 7 (custom gauge) + Tailwind CSS v4 + Cloudflare Pages. This combination is well-documented, has verified compatibility, and keeps JavaScript weight minimal through Astro's zero-JS-by-default philosophy. The critical architectural insight is that the JSON data schema must be defined first and treated as a formal contract — every visual component depends on it, and schema drift discovered at real-data integration time is the highest-cost failure mode for this project.

The primary risks are operational, not technical: the trust problem is central to this product. Users arriving at a "revolution probability" dashboard will be skeptical — alarmist or suppressive depending on their priors. Every design and copy decision must prioritize credibility: visible methodology, transparent update cadence, careful framing language, and explicit data sources. The technical build is well within established patterns; the harder challenge is responsible communication on a politically sensitive index.

---

## Key Findings

### Recommended Stack

Astro 5.18 with static output mode is the correct framework choice: zero JavaScript shipped by default, islands architecture for interactive charts, native Cloudflare Pages deployment with no adapter required, and #1 developer satisfaction in 2025 State of JS. Chart.js 4.5 handles the two standard chart types (historical trend line, contributing factors bar) with a simple declarative API. D3.js 7.9 — imported as specific submodules, not the full bundle — handles the custom needle gauge where Chart.js cannot. Tailwind CSS v4 (via the Vite plugin, not the deprecated `@astrojs/tailwind` integration) covers all styling needs without a separate design system.

**Core technologies:**
- **Astro 5.18:** Static site framework — zero-JS default, islands for charts, direct Cloudflare Pages deploy
- **Chart.js 4.5:** Historical trend + factors bar charts — declarative API, no framework dependency, ~60KB
- **D3.js 7.9 (submodules only):** Custom needle gauge — industry-standard SVG primitives, tree-shakeable
- **Tailwind CSS v4:** Utility styling — OKLCH colors, container queries, Astro ecosystem standard
- **TypeScript (strict):** Type safety — catches JSON schema mismatches before runtime

**What not to use:** React/Vue/Svelte (adds framework runtime with no benefit), `@astrojs/cloudflare` adapter (SSR-only, not needed for static sites), `d3-simple-gauge` or `d3gauge` npm packages (abandoned since 2021, D3 v5 only), Chart.js 3.x (legacy).

### Expected Features

Research benchmarked against 7 comparable public indexes. Every serious index leads with a prominent score, provides historical trend context, explains contributing factors, and includes disclaimer/methodology content — even if minimal. Missing any of these makes the product feel unfinished and untrustworthy.

**Must have (table stakes):**
- Needle gauge with score (0-100) and color-coded severity zones — the product identity
- Zone labels with plain-language meaning ("Elevated Tension") alongside the number
- Historical trend chart — without context, the score has no meaning
- Contributing factors breakdown (4-6 factors, name + weight + value)
- "Last updated" timestamp — critical trust signal for non-real-time data
- Disclaimer / framing copy — required for responsible communication on a political topic
- About / context section — for viral traffic arriving via shared links
- Methodology page (structure + placeholder content) — signals legitimacy
- Mock JSON data system — the contract that everything else depends on
- Responsive mobile layout — significant share of traffic will arrive on phones from shared links
- Cloudflare Pages deployment — must be publicly accessible to validate

**Should have (competitive differentiators):**
- Needle gauge animation on load — static gauges feel broken; animation is the difference between "impressive" and "toy"
- Factor direction arrows (worsening/improving trend per factor) — no comparable index does this well
- Open Graph social card with current score — passive organic distribution on shares
- Weekly cadence framed as rigor ("structural conditions change slowly") — reframes a constraint as a methodology feature

**Defer to v2+:**
- Email/push alerts — requires real data pipeline and email infrastructure
- Public API — the JSON files in the repo are already a de-facto data source; formal API adds versioning burden
- Embeddable widget — use static OG image as substitute; no CORS/versioning complexity
- Country comparison — fundamentally changes product scope; contradicts US-focused depth

**Anti-features (never build):**
- Real-time updates — implies false precision, requires server, breaks static architecture
- User accounts — contradicts zero-cost/zero-server constraint
- Comment section — moderation overhead for politically charged content is unacceptable; link to external communities instead

### Architecture Approach

The architecture is a pure static site: JSON data files committed to `public/data/` are imported in Astro frontmatter at build time, passed to components as props or serialized into `data-*` attributes for client-side chart libraries. The gauge and charts are Astro "islands" that hydrate in the browser — gauge with `client:load` (above fold, must be immediate), trend and factors charts with `client:visible` (below fold, defer until scroll). No framework runtime (React/Vue/Svelte) is needed — Chart.js and D3 are vanilla JS libraries that initialize via plain `<script>` blocks in Astro components.

**Major components:**
1. `BaseLayout.astro` — shared HTML shell, `<head>`, nav, footer, global CSS
2. `src/lib/data.ts` — TypeScript interfaces for all JSON shapes; the schema contract in code
3. `public/data/` (current.json, history.json, factors.json) — the data layer and pipeline contract point
4. `GaugeChart.astro` — D3.js needle gauge island, `client:load`, viewBox-based responsive SVG
5. `TrendChart.astro` + `FactorsChart.astro` — Chart.js line/bar islands, `client:visible`
6. `ScoreDisplay.astro`, `FactorList.astro` — pure static components, no JavaScript
7. `src/pages/index.astro` — dashboard page, reads all JSON, composes components
8. `src/pages/methodology.astro` — static content page, minimal JS

**Build order dictated by dependencies:** JSON schema first → layout/styles → static components → gauge island → chart islands → page assembly → methodology page → deployment config.

### Critical Pitfalls

1. **Chart.js "window is not defined" at build time** — Import Chart.js only inside `<script>` tags in the component body, never in Astro frontmatter. Frontmatter executes in Node.js; browser globals don't exist there. Prevention phase: project scaffold, before any visualization work.

2. **JSON schema contract drift** — Mock data created casually during frontend build diverges from what the real pipeline will produce. Discovered at pipeline integration time, this causes simultaneous failure of every visualization. Fix: define and document the full JSON schema before writing a single component. Treat it as a contract document. Prevention phase: Phase 1, before frontend build begins.

3. **D3 gauge with hardcoded pixel dimensions breaks on mobile** — SVG elements need `viewBox` + `preserveAspectRatio` with `width: 100%; height: auto` CSS, not hardcoded `width`/`height` attributes. Retrofitting responsive behavior after the fact requires refactoring all coordinate calculations. Prevention phase: gauge component build, implement viewBox from day one.

4. **Cloudflare Pages silently routes deployment to Workers** — After first deploy, verify the URL ends in `.pages.dev` not `.workers.dev`. If wrong, use "Shift to Pages" in project settings. Do not install `@astrojs/cloudflare` adapter — its presence can trigger Workers routing. Additionally, disable Cloudflare Auto Minify (it conflicts with Astro's hydration markers). Prevention phase: first deployment.

5. **Wrong build output directory = "deployment successful" blank page** — Astro writes to `dist/`, not `public/`. Set Cloudflare Pages output directory to `dist` explicitly. Run `npm run build` locally and verify `dist/index.html` exists before any deployment configuration. Prevention phase: deployment setup.

---

## Implications for Roadmap

Based on component dependencies, pitfall prevention phases, and feature groupings, the natural phase structure is:

### Phase 1: Foundation and Data Contract

**Rationale:** Everything in this project depends on the JSON schema. The gauge, charts, and methodology page all consume it. Defining the schema last creates schema drift — the highest-cost failure mode identified in research. Project scaffolding, TypeScript setup, and data schema definition must come before any visual work.

**Delivers:** Working Astro project scaffold, TypeScript configured, `public/data/` directory with designed JSON schema for all three files (`current.json`, `history.json`, `factors.json`), mock data populated, `src/lib/data.ts` with typed interfaces, basic `BaseLayout.astro` shell, global CSS with color zone definitions as named constants.

**Addresses features:** Mock data system (P1 dependency for all other features)

**Avoids pitfalls:** JSON schema contract drift (Pitfall 5), hardcoded gauge color zones, missing static output config declaration

**Research flag:** Standard patterns — skip research-phase. Astro scaffold and TypeScript config are well-documented. JSON schema design requires product judgment, not research.

---

### Phase 2: Static Layout and Non-Interactive Components

**Rationale:** Building the static structural components before adding JavaScript islands establishes the layout, typography, and spacing without JavaScript complexity. `ScoreDisplay`, `FactorList`, `SiteHeader`, `SiteFooter`, and the dashboard page skeleton can all be built and visually validated before any D3 or Chart.js work begins. Responsive layout is easier to establish without interactive elements interfering.

**Delivers:** Dashboard page with responsive layout (desktop + mobile), static score display with zone label and timestamp, static factor list, site header/footer, global typography (Inter via Astro Fonts API), Tailwind CSS v4 color system and responsive breakpoints.

**Addresses features:** Current score display + zone label (P1), "Last updated" timestamp (P1), About/context section (P1), disclaimer/framing copy (P1), responsive design (P1)

**Avoids pitfalls:** Easier to establish mobile layout before adding chart islands that complicate the flow

**Research flag:** Standard patterns — skip research-phase. Tailwind v4 + Astro component patterns are well-documented with official sources.

---

### Phase 3: Gauge Chart (Hero Visual)

**Rationale:** The gauge is the product's identity and the most technically complex visualization. It uses D3.js custom SVG rather than a charting library, requires needle animation, must be responsive via viewBox, and needs accessible aria attributes. Building it in isolation (before the other charts) allows focused iteration on the most important and riskiest component. The `client:load` hydration strategy means this is also the component that impacts initial page load performance most directly.

**Delivers:** D3.js needle gauge island with responsive viewBox, color zone arcs (stable/elevated/high/critical), animated needle sweep on load, `prefers-reduced-motion` support, aria-label for accessibility, `client:load` hydration, verified at 375px and 1440px viewports.

**Addresses features:** Revolution gauge with needle + zones (P1), zone labels (differentiator), gauge animation (differentiator)

**Avoids pitfalls:** D3 fixed pixel dimensions (Pitfall 4 — implement viewBox from day one), Chart.js window error pattern (same pattern applies to D3 — client-side only), color zones as named constants not literals

**Research flag:** May benefit from brief research-phase. D3 v7 arc generator + needle rotation patterns are documented but the responsive viewBox + Astro island combination has subtleties. A focused research pass on Astro `<script>` + D3 patterns would reduce trial-and-error.

---

### Phase 4: Chart.js Visualizations

**Rationale:** Historical trend line chart and contributing factors bar chart both use Chart.js and follow the same Astro island pattern. Building them together after the gauge is complete leverages the patterns established in Phase 3 (data-* attribute bridging, client:visible, client-side import only). Two charts in one phase is efficient because they share the same library and hydration approach.

**Delivers:** Historical trend line chart (12 months of mock history), contributing factors bar chart (sorted by weight, highest first), both using `client:visible` for below-fold lazy hydration, data bridged via `data-*` attributes from frontmatter, Chart.js `.destroy()` lifecycle handling to prevent memory leaks.

**Addresses features:** Historical trend chart (P1), contributing factors breakdown (P1), factor direction arrows (P2 — add direction indicators to bar chart)

**Avoids pitfalls:** Chart.js window error (Pitfall 1 — import only in `<script>` tags), Chart.js memory leak (Chart.js `.destroy()` before reinit), re-fetching JSON on every component mount (use data-* pattern established in architecture research), `client:load` overuse (use `client:visible` for below-fold charts)

**Research flag:** Standard patterns — skip research-phase. Chart.js 4 + Astro `<script>` tag pattern is well-documented with multiple verified sources. Data bridging via `data-*` attributes is confirmed in official Astro docs.

---

### Phase 5: Methodology Page and Content

**Rationale:** The methodology page is static content with minimal JavaScript. It can only be written after the JSON schema is defined (Phase 1), since the methodology page describes the data structure and sources. Doing content work after all visualizations are complete ensures the page accurately reflects the implemented system rather than aspirational descriptions.

**Delivers:** Methodology page with section structure (data sources, factor definitions, update process, JSON schema documentation), disclaimer/responsible communication copy (if not placed on homepage in Phase 2), expandable sections with at least one open by default, placeholder content flagged as "coming soon."

**Addresses features:** Methodology page (P1), responsible communication framing, JSON schema documentation (signals legitimacy, enables future pipeline authors)

**Avoids pitfalls:** Methodology page with all sections collapsed by default (UX pitfall — one section open, content visible)

**Research flag:** Standard patterns — skip research-phase. Static Astro page with expandable sections is straightforward. Content decisions are editorial, not technical.

---

### Phase 6: Deployment and Launch Verification

**Rationale:** Deployment is its own phase because Cloudflare Pages has specific pitfalls that must be verified systematically after first deploy. This is not just "push to main" — it requires active verification of deployment URL, output directory, Auto Minify settings, and hydration correctness. The "Looks Done But Isn't" checklist from PITFALLS.md must be run in full.

**Delivers:** Cloudflare Pages project connected to git repo, build command and output directory configured (`npm run build`, `dist`), deployment URL verified as `*.pages.dev`, Cloudflare Auto Minify disabled, Open Graph meta tags for social sharing, custom domain configuration (if applicable), full "looks done but isn't" verification checklist completed.

**Addresses features:** Cloudflare Pages deployment (P1), Open Graph social card meta tags (P2 — basic OG tags are low cost at this stage)

**Avoids pitfalls:** Cloudflare silently routes to Workers (Pitfall 2 — verify `.pages.dev` URL immediately), wrong build output directory (Pitfall 3 — set `dist` explicitly), Cloudflare Auto Minify hydration conflicts, missing `dist/` in `.gitignore`

**Research flag:** Standard patterns — skip research-phase. Cloudflare Pages + static Astro deployment is documented with official sources. The pitfalls are known and the verification steps are explicit.

---

### Phase Ordering Rationale

- **Schema before visuals:** The JSON schema is the foundation. Every component touches it. Building any visual before the schema is defined risks schema drift — the one pitfall with HIGH recovery cost.
- **Static before interactive:** Establishing layout and static components before adding JavaScript islands simplifies responsive layout work and separates concerns cleanly.
- **Gauge before charts:** The gauge is higher risk (custom D3, no library abstraction) and more central to product identity. Validating it early surfaces problems before they compound.
- **Charts together:** Chart.js trend and factors charts share the same library, hydration pattern, and data bridging approach. Building them sequentially within one phase is efficient.
- **Content after structure:** The methodology page content accurately describes the implemented system; writing it last avoids describing things that change during build.
- **Deployment as its own phase:** Deployment verification has distinct failure modes that deserve focused attention, not an afterthought appended to a feature phase.

### Research Flags

Phases likely needing deeper research during planning:
- **Phase 3 (Gauge Chart):** The specific combination of D3 v7 arc generator + responsive viewBox + Astro vanilla JS `<script>` island has subtleties. Research into D3 v7 needle animation patterns and Astro client-side script scoping would reduce trial-and-error. Recommend `/gsd:research-phase` before gauge implementation.

Phases with standard patterns (skip research-phase):
- **Phase 1 (Foundation):** Astro scaffold, TypeScript strict config, JSON schema design — all well-documented with official sources. JSON schema design is a product judgment call, not a research problem.
- **Phase 2 (Static Layout):** Tailwind v4 + Astro component patterns have official documentation and confirmed compatibility.
- **Phase 4 (Chart.js):** Chart.js 4 + Astro `<script>` + data-* attribute pattern is confirmed in official Astro docs and multiple community sources.
- **Phase 5 (Methodology Page):** Static content page with minimal JS — standard Astro patterns.
- **Phase 6 (Deployment):** Cloudflare Pages + static Astro is thoroughly documented; the pitfalls are known and the checklist is explicit.

---

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | Core choices (Astro, Chart.js, D3, Tailwind v4, Cloudflare Pages) verified against official docs and confirmed version compatibility. One medium-confidence item: Astro 5.18 as current stable confirmed from blog post, not release notes. |
| Features | HIGH | Benchmarked against 7 comparable public indexes with direct inspection. Feature prioritization reflects clear patterns across multiple products. Zone threshold values deferred in spec — placeholder 0-25/26-50/51-75/76-100 distribution is appropriate for v1. |
| Architecture | HIGH | All major patterns verified against official Astro docs. Prop serialization bloat issue confirmed via GitHub issue #7978. Build-time JSON import, data-* bridging, client:visible patterns are from official documentation. |
| Pitfalls | MEDIUM-HIGH | Critical pitfalls 1-4 verified from official sources and confirmed GitHub issues. Cloudflare Workers silent routing pitfall sourced from single community article — credible but single source. Auto Minify conflict verified in Cloudflare docs. |

**Overall confidence:** HIGH

### Gaps to Address

- **Color zone thresholds:** The spec intentionally defers score range decisions (what score is "Stable" vs "Elevated" vs "Critical"). This is a modeling/product decision, not a research gap. For v1, use placeholder even distribution (0-25/26-50/51-75/76-100) and flag as preliminary. Zone thresholds become meaningful when the real scoring model is calibrated.

- **Gauge animation specifics:** D3 v7 needle animation timing, easing, and `prefers-reduced-motion` implementation are not fully detailed in research. The Phase 3 research flag addresses this — a focused research pass during gauge planning is recommended.

- **OG image generation strategy:** Research notes that the Open Graph social card should reflect the current score and ideally be regenerated with each weekly data update. The exact mechanism (pre-built static image updated by pipeline, or Cloudflare Image Resizing service) is not resolved. Low priority for v1 launch — basic OG meta tags without a score-reflective image are acceptable initially.

- **Responsible communication copy:** Research confirms the need for framing language but does not prescribe specific wording. The exact disclaimer and methodology framing copy requires editorial judgment — flag for content review before launch.

---

## Sources

### Primary (HIGH confidence)
- https://docs.astro.build/en/guides/deploy/cloudflare/ — Static deploy config, no adapter required
- https://docs.astro.build/en/concepts/islands/ — Islands architecture, client directives
- https://docs.astro.build/en/guides/client-side-scripts/ — data-* attribute pattern, script scoping
- https://docs.astro.build/en/guides/imports/ — Build-time JSON import
- https://docs.astro.build/en/guides/typescript/ — TypeScript strict preset
- https://docs.astro.build/en/reference/experimental-flags/fonts/ — Astro Fonts API status
- https://tailwindcss.com/docs/installation/framework-guides/astro — Tailwind v4 + Astro via Vite plugin
- https://developers.cloudflare.com/pages/framework-guides/deploy-an-astro-site/ — Build settings, output dir
- https://github.com/withastro/astro/issues/7978 — Prop serialization bloat (confirmed bug)
- https://github.com/chartjs/Chart.js/issues/462 — Chart.js destroy() memory leak requirement
- https://github.com/antoinebeland/d3-simple-gauge — Confirmed abandoned (2021, D3 v5 only)

### Secondary (MEDIUM confidence)
- https://astro.build/blog/whats-new-february-2026/ — Astro 5.18 as current stable
- https://github.com/chartjs/Chart.js/releases — Chart.js 4.5.1 current version
- https://d3js.org/ — D3 7.9.0 current version
- https://www.gmkennedy.com/blog/deploy-astro-cloudflare-pages/ — Workers silent redirect pitfall
- https://eastondev.com/blog/en/posts/dev/20251201-cloudflare-static-pages-deploy-guide/ — Wrong output directory = blank page
- https://brendansudol.github.io/writing/responsive-d3 — D3 viewBox responsive pattern
- https://dteather.com/blogs/astro-interactive-charts/ — data-* attribute pattern for Chart.js in Astro

### Tertiary (LOW confidence)
- https://dev.to/absurdityindex/building-a-congressional-satire-site-with-astro-5-tailwind-css-v4-and-cloudflare-pages-3hoe — Astro 5 + Tailwind v4 + Cloudflare Pages real-world project (corroborates stack choices)

### Feature Research References
- https://www.cnn.com/markets/fear-and-greed — Primary UX reference for single-metric public index
- https://thebulletin.org/doomsday-clock/ — Responsible communication and methodology transparency
- https://alternative.me/crypto/fear-and-greed-index/ — Embed/API features, component weighting display
- https://fragilestatesindex.org/ — Factor breakdown design, political stability dashboard patterns
- https://fivethirtyeight.com/methodology/ — Probability communication design, named state labels
- https://ourworldindata.org/grapher/stability-democratic-institutions-index-bti — Embed, download, citation features
- https://www.transparency.org/en/cpi/2025 — Methodology transparency on sensitive indices

---
*Research completed: 2026-03-01*
*Ready for roadmap: yes*
