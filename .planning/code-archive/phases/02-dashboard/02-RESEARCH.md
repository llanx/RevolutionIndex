# Phase 2: Dashboard - Research

**Researched:** 2026-03-01
**Domain:** Astro static islands, D3.js SVG gauge, Chart.js line chart, responsive CSS layout
**Confidence:** HIGH

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| DASH-01 | Visitor sees a needle-style gauge (0–100) as visual centerpiece | D3.js arc + needle SVG pattern; data-attribute bridge for Astro |
| DASH-02 | Gauge displays color-coded zones (green/yellow/orange/red) | Multiple d3.arc() path segments with fill colors; zone thresholds from data.ts |
| DASH-03 | Each zone has a plain-language label ("Stable", "Elevated Tension", etc.) | Static text in SVG or HTML overlay; `current.zone` from JSON provides the value |
| DASH-04 | Current score displayed as prominent number alongside gauge | Static Astro template renders `{current.score}` — zero JS required |
| DASH-05 | Last-updated timestamp visible near score | Static Astro template renders formatted `{current.timestamp}` — zero JS required |
| DASH-06 | Historical trend line chart (score over time, weeks/months) | Chart.js 4 line chart; npm install + bundled Astro `<script>` |
| DASH-07 | Contributing factors breakdown showing 5–6 factors | Static HTML list/bars rendered from `current.factors` array; optional value bars in CSS |
| SITE-01 | Responsive and usable on 375px+ mobile and desktop | CSS Grid/Flexbox layout; single media query breakpoint; gauge SVG viewBox scales |
| SITE-02 | Basic accessibility: color contrast, semantic HTML, screen reader basics | WCAG AA 4.5:1 text / 3:1 UI; `role="img" aria-label` on gauge SVG; `<h1>`, `<time>` |
| SITE-05 | Minimal JavaScript — static content needs no JS, charts hydrate client-side | Astro's default bundled `<script>` for gauge + chart only; static HTML for score/timestamp/factors |
</phase_requirements>

---

## Summary

Phase 2 is a front-end rendering phase. The Astro project scaffold and all JSON data files already exist from Phase 1. The work is: replace the stub `index.astro` with a real dashboard layout, render static content (score, timestamp, zone label, factors) directly in the Astro template, and add two client-side chart islands (D3 needle gauge, Chart.js trend line).

The architecture decision from Phase 1 is already locked: D3.js for the custom needle gauge, Chart.js for the trend/factors charts. The key insight for Astro is that `<script>` tags in `.astro` files are bundled by Vite — you can `import * as d3 from 'd3'` and `import Chart from 'chart.js/auto'` directly inside a `<script>` block and Astro handles bundling automatically. Server-side data (score, history entries, factor values) must be passed to client scripts via `data-*` attributes on HTML elements, since `define:vars` prevents ES module imports.

The layout follows a natural vertical hierarchy: gauge hero (above fold), score + timestamp (above fold), trend chart (scroll), factors breakdown (scroll). This structure satisfies SITE-05 (JS only for the two chart elements), SITE-01 (single breakpoint responsive), and SITE-02 (semantic HTML with WCAG AA contrast on zone colors).

**Primary recommendation:** Use Astro `<script>` tags (bundled, not `is:inline`) importing D3 and Chart.js as npm packages. Pass data to client JS via `data-*` attributes on the canvas/SVG container elements. Render all static content (score, timestamp, zone label, factors list) in the Astro frontmatter template — zero JS required for those elements.

---

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Astro | ^5.0.0 (already installed) | Static site framework, island hydration | Already in project; output: static; bundles script tags |
| D3.js | 7.9.0 (current) | SVG arc drawing, needle rotation math | Most capable SVG data viz library; d3-shape arc API is exactly what a gauge needs |
| Chart.js | 4.x (latest) | Canvas-based line chart for trend data | Simpler API than D3 for standard charts; good Astro npm bundling story |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| d3-shape | (bundled in d3) | Arc path generation for gauge zones | Use the sub-module import `import { arc } from 'd3-shape'` for smaller bundle if desired |
| chart.js/auto | (bundled in chart.js) | Tree-shakes to only needed controllers | `import Chart from 'chart.js/auto'` — simplest for a single chart type |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| D3.js gauge | svg-gauge (zero-dep library) | svg-gauge is simpler but less control over zone colors; D3 is locked in from Phase 1 |
| D3.js gauge | Plain SVG + CSS rotate | Viable, but D3's arc generator eliminates manual path math for curved zones |
| Chart.js | D3.js line chart | D3 is more verbose; Chart.js is faster to implement for a standard time-series line |
| npm install Chart.js | Chart.js via CDN script tag | CDN works but bypasses Astro bundling/optimization; npm is cleaner for the project |

**Installation:**
```bash
npm install d3 chart.js
```

---

## Architecture Patterns

### Recommended Project Structure

```
src/
├── layouts/
│   └── BaseLayout.astro        # Add global CSS import here
├── pages/
│   └── index.astro             # Full dashboard — replaces stub
├── components/
│   ├── Gauge.astro             # SVG container + data-* attributes + bundled D3 script
│   ├── TrendChart.astro        # Canvas container + data-* attributes + bundled Chart.js script
│   └── FactorsBreakdown.astro  # Pure static HTML — no JS
└── styles/
    └── global.css              # Reset, CSS custom properties for zone colors, layout
```

### Pattern 1: Astro Data Bridge via data-* Attributes

**What:** Server-side data (computed in Astro frontmatter) is passed to client-side chart scripts via `data-*` attributes on the mount element. The script reads `element.dataset` to get values.

**When to use:** Any time you need Astro frontmatter variables (JSON data, computed values) inside a `<script>` block that also needs ES module imports. `define:vars` prevents imports — data-* attributes are the official Astro alternative.

**Example:**
```astro
---
// Astro frontmatter (runs at build time — server side)
import type { HistoryData } from '../lib/data';
import historyRaw from '../../public/data/history.json';
const history = historyRaw as unknown as HistoryData;

// Serialize data for client
const chartLabels = JSON.stringify(history.entries.map(e => e.date));
const chartValues = JSON.stringify(history.entries.map(e => e.score));
---

<!-- data-* attributes carry the serialized data to the client script -->
<canvas
  id="trend-chart"
  data-labels={chartLabels}
  data-values={chartValues}
></canvas>

<script>
  // This script is bundled by Astro/Vite — ES module imports work here
  import Chart from 'chart.js/auto';

  const canvas = document.getElementById('trend-chart') as HTMLCanvasElement;
  const labels = JSON.parse(canvas.dataset.labels!);
  const values = JSON.parse(canvas.dataset.values!);

  new Chart(canvas, {
    type: 'line',
    data: {
      labels,
      datasets: [{
        label: 'Revolution Index',
        data: values,
        borderColor: '#e85d04',
        tension: 0.3,
        fill: false,
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: { min: 0, max: 100, beginAtZero: true }
      }
    }
  });
</script>
```
Source: https://docs.astro.build/en/guides/client-side-scripts/

### Pattern 2: D3 Needle Gauge SVG Structure

**What:** The gauge is an SVG composed of (a) multiple arc segments for color zones, (b) a needle path, and (c) a center circle pin. The needle tip position is calculated via trigonometric rotation from the score value.

**When to use:** This exact pattern for the DASH-01/02/03 needle gauge.

**Example:**
```astro
---
import type { CurrentData } from '../lib/data';
import currentRaw from '../../public/data/current.json';
const current = currentRaw as unknown as CurrentData;
---

<div
  id="gauge-mount"
  data-score={current.score}
  aria-label={`Revolution Index: ${current.score} out of 100 — ${current.zone}`}
  role="img"
>
  <!-- SVG injected by D3 script -->
</div>

<script>
  import * as d3 from 'd3';

  const mount = document.getElementById('gauge-mount')!;
  const score = Number(mount.dataset.score);

  const width = 400;
  const height = 220;
  const cx = width / 2;
  const cy = height - 20; // center near bottom of semicircle
  const outerR = 180;
  const innerR = 110;

  // Zone definitions (thresholds from data.ts)
  const zones = [
    { start: 0,  end: 25,  color: '#2d6a4f', label: 'Stable' },
    { start: 25, end: 50,  color: '#f4a261', label: 'Elevated Tension' },
    { start: 50, end: 75,  color: '#e76f51', label: 'Crisis Territory' },
    { start: 75, end: 100, color: '#c1121f', label: 'Revolution Territory' },
  ];

  // Map 0–100 value to semicircle angle in radians
  // Semicircle: left = -π/2, right = +π/2
  function valueToAngle(v: number) {
    return ((v / 100) - 0.5) * Math.PI;
  }

  const arcGen = d3.arc();
  const svg = d3.select(mount).append('svg')
    .attr('viewBox', `0 0 ${width} ${height}`)
    .attr('aria-hidden', 'true'); // role/label on container

  const g = svg.append('g').attr('transform', `translate(${cx},${cy})`);

  // Draw zone arcs
  zones.forEach(z => {
    g.append('path')
      .attr('d', arcGen({
        innerRadius: innerR,
        outerRadius: outerR,
        startAngle: valueToAngle(z.start),
        endAngle: valueToAngle(z.end),
      }))
      .attr('fill', z.color);
  });

  // Draw needle
  const needleAngle = valueToAngle(score); // in radians
  const needleLength = outerR - 10;
  const tipX = needleLength * Math.sin(needleAngle);
  const tipY = -needleLength * Math.cos(needleAngle);
  const baseHalfWidth = 8;
  const leftAngle = needleAngle - Math.PI / 2;
  const rightAngle = needleAngle + Math.PI / 2;
  const lx = baseHalfWidth * Math.sin(leftAngle);
  const ly = -baseHalfWidth * Math.cos(leftAngle);
  const rx = baseHalfWidth * Math.sin(rightAngle);
  const ry = -baseHalfWidth * Math.cos(rightAngle);

  g.append('path')
    .attr('d', `M ${lx} ${ly} L ${tipX} ${tipY} L ${rx} ${ry}`)
    .attr('fill', '#1b1b1b');

  // Center pin circle
  g.append('circle').attr('r', 10).attr('fill', '#1b1b1b');
</script>
```
Source: https://d3js.org/d3-shape/arc, https://jaketrent.com/post/rotate-gauge-needle-in-d3/

### Pattern 3: Static Factor Rendering (No JS)

**What:** The contributing factors breakdown (DASH-07) is static HTML rendered in the Astro template. No JavaScript needed. CSS `width` set via inline style from factor value.

**When to use:** Satisfies SITE-05 (minimal JS). Only the two chart elements need JS.

**Example:**
```astro
---
import type { CurrentData, FactorsData } from '../lib/data';
import currentRaw from '../../public/data/current.json';
import factorsRaw from '../../public/data/factors.json';
const current = currentRaw as unknown as CurrentData;
const factors = factorsRaw as unknown as FactorsData;

// Join current factors with descriptions
const enriched = current.factors.map(f => ({
  ...f,
  description: factors.factors.find(d => d.id === f.id)?.description ?? '',
}));
---

<ul class="factors-list">
  {enriched.map(f => (
    <li class="factor-item">
      <div class="factor-header">
        <span class="factor-name">{f.name}</span>
        <span class={`factor-direction direction-${f.direction}`}>
          {f.direction === 'up' ? '↑' : f.direction === 'down' ? '↓' : '→'}
        </span>
      </div>
      <div class="factor-bar-track">
        <div
          class="factor-bar-fill"
          style={`width: ${Math.round(f.value * 100)}%`}
          aria-label={`${f.name}: ${Math.round(f.value * 100)}%`}
        ></div>
      </div>
      <p class="factor-description">{f.description}</p>
    </li>
  ))}
</ul>
```

### Pattern 4: CSS Custom Properties for Zone Colors

**What:** Zone colors defined once in `global.css` as CSS custom properties, reused across SVG fill attrs and HTML bar colors.

**Example:**
```css
/* src/styles/global.css */
:root {
  --zone-stable: #2d6a4f;
  --zone-elevated: #f4a261;
  --zone-crisis: #e76f51;
  --zone-revolution: #c1121f;
  --bg-primary: #0f0f0f;
  --text-primary: #f5f5f5;
  --text-secondary: #a0a0a0;
}
```

### Pattern 5: Responsive Layout with Single Breakpoint

**What:** Mobile-first single-column layout with a breakpoint at 768px for side-by-side sections on desktop.

**Example:**
```css
.dashboard {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem;
}

@media (min-width: 768px) {
  .dashboard-lower {
    grid-template-columns: 1fr 1fr;
  }
}

/* SVG gauge scales via viewBox — no JS needed */
.gauge-container svg {
  width: 100%;
  max-width: 500px;
  height: auto;
}
```

### Anti-Patterns to Avoid

- **Using `define:vars` with D3/Chart.js imports:** `define:vars` implies `is:inline`, which disables Astro's bundler. ES module imports inside a `define:vars` script fail with a SyntaxError. Use `data-*` attributes instead.
- **Placing D3/Chart.js in the frontmatter:** Frontmatter runs at build time (Node.js). D3's DOM manipulation and Chart.js canvas APIs require a browser. They must run in `<script>` blocks.
- **Hardcoding zone colors in the D3 script and the CSS separately:** Define colors once (CSS custom properties or a shared constant) to prevent drift between SVG zone arcs and HTML factor bars.
- **Using `is:inline` on the chart script:** `is:inline` prevents bundling, meaning `import Chart from 'chart.js/auto'` won't resolve. Only use `is:inline` for truly isolated scripts with no imports.
- **Rendering the gauge SVG at a fixed pixel size:** Use `viewBox` + `width: 100%; height: auto` so the SVG scales on mobile without a media query.
- **Not setting `aria-label` on the gauge:** The SVG communicates the score visually only. Screen readers need `role="img"` and a descriptive `aria-label` on the container.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| SVG arc paths for gauge zones | Manual path string math | `d3.arc()` generator | arc() handles start/end angles, inner/outer radius, corner radius, sweep flags automatically |
| Canvas chart rendering | Custom canvas draw loop | Chart.js `new Chart(canvas, config)` | Responsiveness, tooltip, axis labels, animation — all handled |
| Needle angle math from 0–100 score | Custom angle formula | Simple linear map: `((score/100) - 0.5) * Math.PI` | This formula is correct and verified; nothing to reinvent |
| CSS reset / base styles | Custom reset stylesheet | Plain `box-sizing: border-box` + minimal base | No framework needed; a 10-line reset is fine |
| Timestamp formatting | Custom date parser | `new Date(timestamp).toLocaleDateString('en-US', {...})` | ISO 8601 string in data.ts; browser Date API handles it |

**Key insight:** The gauge is the most complex element (D3 arcs + needle math), but D3's arc generator eliminates all the hard path math. The rest of the dashboard is straightforward static HTML + one Chart.js call.

---

## Common Pitfalls

### Pitfall 1: define:vars Blocks ES Module Imports

**What goes wrong:** Developer adds `<script define:vars={{ score }}>` to pass the score to D3, then imports D3 inside — build succeeds but the script is `is:inline` and `import` fails at runtime in the browser.

**Why it happens:** Astro's `define:vars` directive wraps the script in a function body and opts out of Vite bundling. The import statement then runs outside the module graph.

**How to avoid:** Never combine `define:vars` with `import` statements. Use `data-*` attributes on the mount element and read `element.dataset.score` inside the script.

**Warning signs:** Console error at runtime: `Cannot use import statement outside a module`; or the script silently fails because Astro bundled an empty module.

### Pitfall 2: D3 Angle Convention (0 = 12 o'clock, clockwise)

**What goes wrong:** Developer maps score 0 to `startAngle: 0` expecting left side of gauge — but D3's 0 angle is at 12 o'clock (top), and angles increase clockwise. The gauge renders rotated 90 degrees.

**Why it happens:** D3 arc angles differ from standard math convention (0 = 3 o'clock, counterclockwise). D3's 0 = top, positive = clockwise.

**How to avoid:** For a horizontal semicircle (left = 0, right = 100), use `startAngle = -Math.PI/2` (left) to `endAngle = Math.PI/2` (right). Score value maps: `angle = ((score/100) - 0.5) * Math.PI`.

**Warning signs:** Gauge zones appear rotated; needle points wrong direction.

### Pitfall 3: SVG Coordinate Origin for Needle

**What goes wrong:** Needle renders at wrong position because D3 arc generator centers at (0,0) but the SVG `<g>` transform hasn't moved the group to the gauge center.

**Why it happens:** D3 generates arc paths centered at (0,0). Without `translate(cx, cy)` on the containing `<g>`, arcs and needle appear at top-left of SVG.

**How to avoid:** Apply `g.attr('transform', 'translate(cx, cy)')` to the group before drawing arcs and needle. Set `cy` near the bottom of the SVG (e.g., `height - 20`) so the semicircle fits.

**Warning signs:** Arc paths render partially or completely off-screen; SVG has empty white space.

### Pitfall 4: Chart.js Canvas Sizing

**What goes wrong:** Chart.js renders at wrong size or canvas is 0x0 on mobile because the canvas element has no explicit dimensions and the container has no width.

**Why it happens:** Chart.js respects `responsive: true` (default) but needs the canvas container to have a defined CSS width.

**How to avoid:** Wrap `<canvas>` in a `<div>` with explicit `width: 100%`. Set `options.maintainAspectRatio: false` if you need custom height; otherwise let Chart.js default 2:1 aspect ratio apply.

**Warning signs:** Chart renders as a thin sliver or is invisible on mobile.

### Pitfall 5: Zone Color Contrast Failing WCAG AA (SITE-02)

**What goes wrong:** Zone colors chosen to look attractive fail the 4.5:1 contrast ratio against white/black text labels printed over them.

**Why it happens:** Saturated mid-range colors (yellow, orange) often have poor contrast with both black and white text.

**How to avoid:** Test each zone color against the label text color with WebAIM contrast checker. WCAG AA requires 4.5:1 for normal text, 3:1 for large text (18px+ or 14px+ bold). Avoid placing text directly on zone arc fills — keep labels in the HTML below the SVG where contrast is controlled.

**Warning signs:** axe DevTools or Lighthouse accessibility audit flags contrast errors.

---

## Code Examples

Verified patterns from official sources:

### Chart.js Line Chart — Full Config
```javascript
// Source: https://www.chartjs.org/docs/latest/charts/line.html
import Chart from 'chart.js/auto';

new Chart(canvas, {
  type: 'line',
  data: {
    labels: ['2025-11-30', '2025-12-07', /* ... */],
    datasets: [{
      label: 'Revolution Index Score',
      data: [38, 36, /* ... */],
      borderColor: '#e85d04',
      backgroundColor: 'rgba(232, 93, 4, 0.1)',
      tension: 0.3,
      fill: true,
      pointRadius: 3,
    }]
  },
  options: {
    responsive: true,
    plugins: {
      legend: { display: false },
      tooltip: { mode: 'index' }
    },
    scales: {
      x: {
        ticks: { maxTicksLimit: 6 }  // prevent crowded x-axis on mobile
      },
      y: {
        min: 0,
        max: 100,
        ticks: { stepSize: 25 }
      }
    }
  }
});
```

### D3 Arc Generator — Semicircle Zone
```javascript
// Source: https://d3js.org/d3-shape/arc
import { arc } from 'd3-shape'; // or: import * as d3 from 'd3'; d3.arc()

const arcGen = arc();

// One zone arc (0–25 = Stable zone)
const pathData = arcGen({
  innerRadius: 110,
  outerRadius: 180,
  startAngle: -Math.PI / 2,      // D3 convention: 0 is top, so left = -π/2
  endAngle: -Math.PI / 2 + (25 / 100) * Math.PI,  // 25% of semicircle
});
// pathData is an SVG path string for a path[d] attribute
```

### Astro: Import CSS in Layout
```astro
---
// src/layouts/BaseLayout.astro
import '../styles/global.css';  // bundled and injected into <head>
export interface Props { title: string; }
const { title } = Astro.props;
---
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title}</title>
  </head>
  <body>
    <slot />
  </body>
</html>
```
Source: https://docs.astro.build/en/guides/styling/

### Timestamp Formatting (Static, No JS)
```astro
---
// In Astro frontmatter — runs at build time
const dateDisplay = new Date(current.timestamp).toLocaleDateString('en-US', {
  year: 'numeric',
  month: 'long',
  day: 'numeric',
});
---
<time datetime={current.timestamp}>{dateDisplay}</time>
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Chart.js CDN `<script>` tag | `npm install chart.js` + Astro bundling | Chart.js 4+ / Astro 2+ | Tree-shaking, version locking, no CDN dependency |
| D3 framework components (react-d3) | Vanilla D3 in Astro `<script>` tag | Astro 2+ | No framework overhead; works with static Astro output |
| `define:vars` for passing data to scripts | `data-*` attributes + `element.dataset` | Astro 2+ (documented pattern) | Avoids `is:inline` trap; allows ES module imports alongside server data |
| Fixed SVG width/height | `viewBox` + CSS `width:100%; height:auto` | CSS standard, widely adopted | SVG scales responsively without JavaScript |

**Deprecated/outdated:**
- `<script is:inline>` with import statements: does not work; `is:inline` disables bundling
- Chart.js v2/v3 API: `Chart.defaults.global.*` is replaced by `Chart.defaults.*` in v4; migration guide at https://www.chartjs.org/docs/latest/migration/v4-migration.html

---

## Open Questions

1. **Gauge animation on load**
   - What we know: D3 can animate arc `endAngle` from 0 to final value using `selection.transition().duration()`; needle can animate using the same pattern
   - What's unclear: Whether the project wants entry animation or static render; not specified in requirements
   - Recommendation: Implement static first (satisfies all requirements); animation can be added as one line change per element. Flag for planner to make a call.

2. **Exact zone color palette**
   - What we know: Zones are green/yellow/orange/red; thresholds are 0-25/26-50/51-75/76-100 from data.ts; colors must pass WCAG AA contrast against the page background
   - What's unclear: Specific hex values — dark tones are safer for contrast on dark backgrounds, saturated tones on light backgrounds
   - Recommendation: Choose a page background first (dark or light theme), then select zone colors against that background. Suggest dark theme (`#0f0f0f` bg) with muted zone colors: stable `#40916c`, elevated `#f4a261`, crisis `#e76f51`, revolution `#c1121f`. Verify contrast of any text placed near/over these zones.

3. **Factors breakdown visual format**
   - What we know: Requirements say "5-6 factors pushing score up or down"; mock data has `value` (0-1), `direction` ('up'/'down'/'neutral'), `weight`, `name`, `description`
   - What's unclear: Whether factors should show weight bars, value bars, or both; whether direction arrows are sufficient without a bar
   - Recommendation: A horizontal bar showing `value` (intensity) with a direction arrow and name label. Weight can be shown as a secondary label. Pure CSS + static HTML — no JS needed.

---

## Sources

### Primary (HIGH confidence)
- https://docs.astro.build/en/guides/client-side-scripts/ — `<script>` bundling, data-* pattern, `define:vars` limitations
- https://docs.astro.build/en/guides/styling/ — CSS scoping, `is:global`, layout CSS import
- https://docs.astro.build/en/reference/directives-reference/ — `client:*` directives, `is:inline`, `define:vars`
- https://d3js.org/getting-started — D3 7.9.0 version, npm install, ESM import
- https://d3js.org/d3-shape/arc — arc() API: innerRadius, outerRadius, startAngle, endAngle
- https://www.chartjs.org/docs/latest/charts/line.html — line chart config, dataset properties
- https://www.chartjs.org/docs/latest/getting-started/installation.html — `npm install chart.js`

### Secondary (MEDIUM confidence)
- https://jaketrent.com/post/rotate-gauge-needle-in-d3/ — Needle rotation math (trigonometric approach, verified consistent with D3 arc convention)
- https://webaim.org/articles/contrast/ — WCAG AA contrast ratios 4.5:1 (text) / 3:1 (UI components)
- https://github.com/withastro/astro/issues/12343 — Confirms `define:vars` + import incompatibility (community-verified)

### Tertiary (LOW confidence)
- Medium article on Chart.js + Astro patterns — general approach consistent with docs but not officially from Astro team

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — D3 7.9.0 and Chart.js 4.x confirmed from official sites; Astro already installed at ^5.0.0
- Architecture (data-* pattern): HIGH — Confirmed from official Astro docs; define:vars limitation confirmed via GitHub issue
- D3 gauge pattern: MEDIUM — Core arc API is HIGH from official docs; needle trigonometry is MEDIUM (verified from community source consistent with math)
- Pitfalls: MEDIUM — Most derived from official docs + known Astro gotcha; zone contrast is spec (WCAG AA)
- Chart.js config: HIGH — Confirmed from official Chart.js docs

**Research date:** 2026-03-01
**Valid until:** 2026-04-01 (D3 and Chart.js are stable; Astro 5.x stable API unlikely to change in this window)
