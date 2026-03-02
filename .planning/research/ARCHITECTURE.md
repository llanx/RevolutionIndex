# Architecture Research

**Domain:** Static data dashboard (Astro + JSON + Cloudflare Pages)
**Researched:** 2026-03-01
**Confidence:** HIGH — sourced from official Astro docs, official Cloudflare Pages docs, and verified patterns

---

## Standard Architecture

### System Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                       BUILD TIME (Astro SSG)                      │
│                                                                   │
│  ┌─────────────┐   import   ┌─────────────────────────────────┐  │
│  │ data/*.json │ ─────────> │  src/pages/index.astro           │  │
│  │             │            │  (frontmatter reads JSON,        │  │
│  │ current.json│            │   serializes to data-* attrs     │  │
│  │ history.json│            │   and passes as props)           │  │
│  │ factors.json│            └────────────┬────────────────────┘  │
│  └─────────────┘                         │                       │
│                                          │ renders                │
│                             ┌────────────▼────────────────────┐  │
│                             │  Layout Component               │  │
│                             │  (BaseLayout.astro)             │  │
│                             │  - <head>, meta, CSS            │  │
│                             │  - <slot /> for page content    │  │
│                             └────────────┬────────────────────┘  │
│                                          │                       │
│              ┌───────────────────────────┼──────────────────┐    │
│              │                           │                  │    │
│   ┌──────────▼──────────┐  ┌─────────────▼──────┐  ┌────────▼─┐ │
│   │  Static Astro        │  │  Chart Islands      │  │  Static  │ │
│   │  Components          │  │  (client:visible)   │  │  Content │ │
│   │  - ScoreDisplay      │  │  - GaugeChart       │  │  Sections│ │
│   │  - FactorList        │  │  - TrendChart       │  │          │ │
│   │  - SiteHeader        │  │  - FactorsChart     │  │          │ │
│   │  - SiteFooter        │  │                     │  │          │ │
│   └─────────────────────┘  └─────────────────────┘  └──────────┘ │
└──────────────────────────────────────────────────────────────────┘
                              │
                              │ npm run build → dist/
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│                    DEPLOY: Cloudflare Pages CDN                   │
│                                                                   │
│   dist/                                                           │
│   ├── index.html          (pre-rendered, no server needed)        │
│   ├── methodology/index.html                                      │
│   ├── _astro/             (bundled JS for islands only)           │
│   └── data/               (JSON files, copied from public/)       │
└──────────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

| Component | Responsibility | Typical Implementation |
|-----------|----------------|------------------------|
| `BaseLayout.astro` | Shared HTML shell, `<head>`, nav, footer | Astro layout with `<slot />` |
| `src/pages/index.astro` | Dashboard page, reads JSON, passes data to children | Astro page with frontmatter `import` |
| `src/pages/methodology.astro` | Static methodology page with expandable sections | Astro page, minimal JS |
| `ScoreDisplay.astro` | Renders the current score number, date, label | Pure static Astro component |
| `FactorList.astro` | Renders factor names and values as static HTML | Pure static Astro component |
| `GaugeChart` island | Interactive needle gauge SVG/D3, client-side only | Vanilla JS `<script>` or `client:visible` |
| `TrendChart` island | Interactive line chart of historical scores | `<script>` tag with Chart.js |
| `FactorsChart` island | Bar/breakdown chart of contributing factors | `<script>` tag with Chart.js |
| `SiteHeader.astro` | Site navigation and title bar | Static Astro component |
| `SiteFooter.astro` | Footer links, data freshness timestamp | Static Astro component |

---

## Recommended Project Structure

```
revolutionindex/
├── public/
│   ├── data/
│   │   ├── current.json       # Current score + factor snapshot
│   │   ├── history.json       # Time series of all past scores
│   │   └── factors.json       # Detailed factor data
│   └── favicon.svg
├── src/
│   ├── pages/
│   │   ├── index.astro        # Main dashboard page
│   │   └── methodology.astro  # Methodology/about page
│   ├── layouts/
│   │   └── BaseLayout.astro   # Shared HTML shell (head, nav, footer)
│   ├── components/
│   │   ├── charts/
│   │   │   ├── GaugeChart.astro     # Gauge island wrapper
│   │   │   ├── TrendChart.astro     # Trend line island wrapper
│   │   │   └── FactorsChart.astro   # Factors bar island wrapper
│   │   ├── ScoreDisplay.astro       # Static score hero display
│   │   ├── FactorList.astro         # Static factor list
│   │   ├── SiteHeader.astro         # Navigation header
│   │   └── SiteFooter.astro         # Footer with timestamp
│   ├── styles/
│   │   └── global.css               # Base styles, CSS variables, color zones
│   └── lib/
│       └── data.ts                  # Type definitions + data loading helpers
├── astro.config.mjs
├── tsconfig.json
└── package.json
```

### Structure Rationale

- **`public/data/`:** JSON data files placed in `public/` are copied to `dist/` untouched by Astro's build pipeline. This means they are also fetchable at runtime by JavaScript if needed, and they remain readable on the deployed CDN. Do not put them in `src/` unless you only need them at build time — `src/` imports are bundled and tree-shaken.
- **`src/components/charts/`:** Grouping all chart islands under a `charts/` subdirectory isolates the interactive/JS-heavy components from the purely static ones. Easier to audit JavaScript weight at a glance.
- **`src/lib/data.ts`:** Centralizes TypeScript interfaces for JSON shapes and any data transformation logic. Pages import from here rather than re-parsing inline. Defines the JSON contract once.
- **`src/layouts/`:** Single layout file for now. As pages grow, layouts absorb shared structure without repeating it.
- **`src/styles/`:** Global CSS (color tokens, zone colors, typography) lives here. Component-scoped styles live in the `.astro` files themselves.

---

## Architectural Patterns

### Pattern 1: Build-Time JSON Import

**What:** Import JSON files directly in frontmatter. Astro resolves them at build time — no fetch call, no API layer.

**When to use:** For data that is pre-computed and committed to the repo. The entire JSON is available as a typed object in the component script.

**Trade-offs:** Data is baked into the HTML at build time. An update requires a redeploy. Perfectly fine for weekly-updated data.

**Example:**
```astro
---
// src/pages/index.astro
import currentData from '../../public/data/current.json';
import historyData from '../../public/data/history.json';
import type { CurrentData, HistoryData } from '../lib/data';

const score = (currentData as CurrentData).score;
const history = (historyData as HistoryData).entries;
---

<ScoreDisplay score={score} />
<TrendChart data={history} />
```

Confidence: HIGH — verified in official Astro imports docs.

### Pattern 2: Data Bridging via data-* Attributes

**What:** Pass server-side data to client-side scripts using HTML `data-*` attributes on a wrapper element, then read them with `dataset` in the script.

**When to use:** When a vanilla JS script (Chart.js, D3) needs data that was loaded in Astro frontmatter. Avoids the quadratic serialization problem with deeply nested props on framework islands (verified as a real issue: GitHub #7978).

**Trade-offs:** Works cleanly for flat or shallow-nested data. For very large data sets, consider fetching the JSON directly from `/data/history.json` on the client instead of embedding in HTML.

**Example:**
```astro
---
// src/components/charts/TrendChart.astro
import historyData from '../../../public/data/history.json';
const serialized = JSON.stringify(historyData.entries);
---

<canvas id="trend-chart" data-history={serialized}></canvas>

<script>
  const canvas = document.getElementById('trend-chart') as HTMLCanvasElement;
  const history = JSON.parse(canvas.dataset.history!);
  // Initialize Chart.js with `history`
  new Chart(canvas, { type: 'line', data: { datasets: [{ data: history }] } });
</script>
```

Confidence: HIGH — official Astro client-side scripts docs.

### Pattern 3: client:visible for Below-Fold Islands

**What:** Use `client:visible` on chart components so their JavaScript only loads when the element scrolls into the viewport.

**When to use:** Any interactive component that is not immediately visible on page load. For a dashboard with a hero gauge at the top and charts below, this applies to TrendChart and FactorsChart.

**Trade-offs:** Slightly delays chart render when user scrolls. Not noticeable for charts — users see the static canvas placeholder first, then the chart hydrates. Better than `client:load` which downloads all chart JS immediately.

**Example:**
```astro
---
import TrendChart from '../components/charts/TrendChart.astro';
---

<!-- GaugeChart is hero element - load immediately -->
<GaugeChart client:load score={score} />

<!-- Charts are below fold - defer until visible -->
<TrendChart client:visible data={history} />
<FactorsChart client:visible data={factors} />
```

Confidence: HIGH — official Astro islands docs.

### Pattern 4: Vanilla JS Islands (No Framework)

**What:** Use plain `<script>` tags in `.astro` files instead of React/Vue/Svelte components for chart initialization. Astro processes and bundles these automatically.

**When to use:** When the only interactivity needed is library initialization (Chart.js, D3). Avoids shipping a full UI framework for a use case that doesn't need component reactivity.

**Trade-offs:** Less structured than a React component, but produces dramatically less JavaScript. Chart.js and D3 both work perfectly as vanilla JS. Note: `<script>` tags in Astro are deduplicated per page — use custom HTML elements (`connectedCallback`) when the same component appears multiple times and each needs its own initialization.

**Example:**
```astro
<!-- src/components/charts/GaugeChart.astro -->
<div id="gauge-container" data-score={score}></div>

<script>
  import * as d3 from 'd3';
  const container = document.getElementById('gauge-container')!;
  const score = Number(container.dataset.score);
  // D3 gauge rendering logic here
</script>
```

Confidence: MEDIUM — pattern documented in Astro client-side scripts docs and confirmed by community usage.

### Pattern 5: Static Cloudflare Pages Deploy (No Adapter)

**What:** Deploy as a fully static site (`output: 'static'` in astro.config.mjs) with no `@astrojs/cloudflare` adapter. Connect repo to Cloudflare Pages via git integration, set build command to `npm run build`, output dir to `dist`.

**When to use:** Any Astro site with no SSR or server functions. This project is fully static — adapter is not needed and adds unnecessary complexity.

**Trade-offs:** Cannot use Cloudflare Workers or D1 bindings from Astro routes. Not relevant here since there are no server routes.

**Example:**
```js
// astro.config.mjs
import { defineConfig } from 'astro/config';

export default defineConfig({
  output: 'static',  // default, can be omitted
  site: 'https://revolutionindex.com',
});
```

Confidence: HIGH — official Cloudflare Pages Astro deployment docs.

---

## Data Flow

### Build-Time Flow (JSON to HTML)

```
data/current.json         (committed to repo, weekly update)
      │
      │ import (at build time)
      ▼
src/pages/index.astro     (frontmatter reads typed JSON)
      │
      │ props / data-* attrs
      ├────────────────────────────────────────┐
      ▼                                        ▼
ScoreDisplay.astro                   TrendChart.astro
(renders static HTML with score)     (serializes history → data-* attr)
                                              │
                                      <canvas data-history="[...]">
                                              │
                                       <script> reads dataset,
                                       initializes Chart.js
```

### Runtime Flow (Page Load in Browser)

```
Browser requests page
      │
      ▼
Cloudflare CDN serves pre-built index.html
      │
      │ parse HTML
      ▼
Static content visible immediately
(score text, factor list, header, footer)
      │
      │ JS modules load (only for islands)
      ▼
GaugeChart JS loads → D3 draws needle gauge
      │
      │ user scrolls down
      ▼
TrendChart enters viewport → client:visible triggers
Chart.js initializes → reads data-history attribute → renders line chart
      │
FactorsChart enters viewport → same pattern → renders bar chart
```

### JSON Data Contract

The JSON schema defined now becomes the contract for the future data pipeline. Structure it for the frontend, not the model:

```
public/data/current.json
{
  "score": 47,
  "timestamp": "2026-03-01T00:00:00Z",
  "label": "Partial Revolution Territory",
  "factors": [
    { "id": "economic_inequality", "name": "Economic Inequality",
      "value": 0.72, "direction": "up", "weight": 0.18 }
  ]
}

public/data/history.json
{
  "entries": [
    { "date": "2026-03-01", "score": 47 },
    { "date": "2026-02-22", "score": 45 }
  ]
}

public/data/factors.json
{
  "factors": [
    { "id": "economic_inequality", "name": "Economic Inequality",
      "description": "...", "current_value": 0.72,
      "historical": [{ "date": "2026-03-01", "value": 0.72 }] }
  ]
}
```

---

## Build Order (Phase Dependencies)

The component dependencies dictate a natural build order:

```
1. Data schema + JSON files        (no dependencies — everything depends on this)
      ↓
2. BaseLayout + global styles      (no content dependencies, just structural shell)
      ↓
3. Static components               (depend on layout, independent of charts)
   (ScoreDisplay, FactorList,
    SiteHeader, SiteFooter)
      ↓
4. GaugeChart island               (depends on D3, score data schema)
      ↓
5. TrendChart island               (depends on Chart.js, history data schema)
6. FactorsChart island             (depends on Chart.js, factors data schema)
      ↓
7. Dashboard page assembly         (composes all components, depends on all above)
   (src/pages/index.astro)
      ↓
8. Methodology page                (independent of charts, just static content)
   (src/pages/methodology.astro)
      ↓
9. Cloudflare Pages deploy config  (depends on working build)
```

---

## Scaling Considerations

This is a static site served from CDN. Traditional scaling concerns (database connections, server load) do not apply. The relevant scaling axis is content/data complexity.

| Scale | Architecture Adjustments |
|-------|--------------------------|
| v1: mock data, 1 page | Current architecture — no changes needed |
| v2: real data, weekly pipeline | Add GitHub Actions workflow; JSON schema already defined |
| v3: multiple metrics pages | Add dynamic routes `src/pages/factors/[id].astro` with `getStaticPaths()` |
| v4: public API | Add Cloudflare Worker in separate service; static site unchanged |

### Scaling Priorities

1. **First bottleneck:** JSON file size. At 52 entries/year, `history.json` stays tiny indefinitely. Only becomes an issue if daily granularity is adopted (~3,650 entries after 10 years — still under 500KB).
2. **Second bottleneck:** Build time. Astro's static build is fast. Not a concern until hundreds of pages exist.

---

## Anti-Patterns

### Anti-Pattern 1: Fetching JSON at Runtime Instead of Import

**What people do:** Use `fetch('/data/current.json')` inside a `useEffect` or script to load data after page paint.

**Why it's wrong:** Causes a flash of empty content on every page load. The data is static and available at build time — there is no reason to defer it to runtime. Users see a blank gauge or empty charts before the fetch resolves.

**Do this instead:** Import JSON in Astro frontmatter at build time. The data is baked into the HTML. Zero network round-trips for data on page load.

---

### Anti-Pattern 2: Shipping a Full JS Framework for Charts

**What people do:** Install React or Vue, wrap Chart.js in a React component, use `client:load` on everything.

**Why it's wrong:** Ships the entire React runtime (~40KB gzipped) just to initialize a chart library that works fine with vanilla JS. Increases Time-to-Interactive unnecessarily.

**Do this instead:** Use `<script>` tags in `.astro` files to initialize Chart.js and D3 directly. The result is the same chart with a fraction of the JavaScript. Only add a framework if you need reactive state, form handling, or complex component composition.

---

### Anti-Pattern 3: Putting Data Files in src/ Instead of public/

**What people do:** Put `current.json` in `src/data/` and import it only in frontmatter.

**Why it's wrong:** Files in `src/` are processed by Vite and may not be directly accessible at a URL path. The future pipeline needs to write JSON to a predictable location that is also accessible as a static asset URL. `public/data/` is both importable at build time AND accessible at `/data/current.json` from the deployed site.

**Do this instead:** Put JSON data files in `public/data/`. Import them in frontmatter with a path like `../../public/data/current.json`. They will be available at `/data/current.json` on the deployed CDN, enabling future client-side fetching if needed.

---

### Anti-Pattern 4: Using @astrojs/cloudflare Adapter for a Static Site

**What people do:** Install the Cloudflare adapter following SSR tutorials, set `output: 'server'`.

**Why it's wrong:** The adapter is for server-side rendering via Cloudflare Workers. A static dashboard doesn't need it. Using it adds a Workers execution layer, complicates the build, and may introduce costs.

**Do this instead:** Deploy with `output: 'static'` (the default). Set build command to `npm run build` and output directory to `dist` in Cloudflare Pages settings. No adapter needed.

---

### Anti-Pattern 5: Prop Serialization for Deeply Nested Data

**What people do:** Pass large nested JSON as props to framework island components (e.g., `<TrendChart client:load data={largeDataset} />`).

**Why it's wrong:** Astro serializes island props into the HTML as an escaped JSON string inside the `astro-island` element. Deeply nested objects produce quadratic quote escaping (confirmed bug: withastro/astro #7978), bloating the HTML.

**Do this instead:** Use `data-*` attributes on a plain HTML element and read them with `dataset` in the client script. Or have the client script fetch the JSON file directly from `/data/history.json` — this is a clean separation since the file is already in `public/`.

---

## Integration Points

### External Services

| Service | Integration Pattern | Notes |
|---------|---------------------|-------|
| Cloudflare Pages | Git push → automatic build+deploy | Static output only; no adapter needed |
| GitHub (future) | GitHub Actions writes JSON → commit triggers Cloudflare deploy | Pipeline separate from frontend |

### Internal Boundaries

| Boundary | Communication | Notes |
|----------|---------------|-------|
| JSON data ↔ Astro pages | Direct `import` in frontmatter at build time | Type definitions in `src/lib/data.ts` |
| Astro frontmatter ↔ client scripts | `data-*` HTML attributes on wrapper elements | Avoids prop serialization issues |
| Chart islands ↔ each other | No cross-island communication needed for this project | Each chart reads its own data independently |
| Future pipeline ↔ frontend | JSON schema contract in `public/data/` | Schema is the API; pipeline must match it |

---

## Sources

- [Astro Islands Architecture — Official Docs](https://docs.astro.build/en/concepts/islands/) — HIGH confidence
- [Astro Client-Side Scripts — Official Docs](https://docs.astro.build/en/guides/client-side-scripts/) — HIGH confidence
- [Astro Imports Reference — Official Docs](https://docs.astro.build/en/guides/imports/) — HIGH confidence
- [Astro Project Structure — Official Docs](https://docs.astro.build/en/basics/project-structure/) — HIGH confidence
- [Astro Layouts — Official Docs](https://docs.astro.build/en/basics/layouts/) — HIGH confidence
- [Astro Share State Between Islands — Official Docs](https://docs.astro.build/en/recipes/sharing-state-islands/) — HIGH confidence
- [Deploy Astro to Cloudflare Pages — Official Astro Docs](https://docs.astro.build/en/guides/deploy/cloudflare/) — HIGH confidence
- [Prop Serialization Bloat Issue — withastro/astro #7978](https://github.com/withastro/astro/issues/7978) — HIGH confidence (verified issue)
- [Building Static Websites with JSON Data in Astro — dev.solita.fi](https://dev.solita.fi/2024/12/02/building-static-websites-with-astro.html) — MEDIUM confidence
- [Building a Multi-Framework Dashboard with Astro — LogRocket](https://blog.logrocket.com/building-multi-framework-dashboard-with-astro/) — MEDIUM confidence
- [Adding Interactive Charts to Astro — David Teather](https://dteather.com/blogs/astro-interactive-charts/) — MEDIUM confidence (uses data-* pattern)

---

*Architecture research for: Static data dashboard (Astro + JSON + Cloudflare Pages)*
*Researched: 2026-03-01*
