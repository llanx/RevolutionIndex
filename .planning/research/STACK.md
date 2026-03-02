# Stack Research

**Domain:** Static data visualization dashboard (public-facing, political instability score)
**Researched:** 2026-03-01
**Confidence:** HIGH — core choices verified via official docs and multiple current sources

## Recommended Stack

### Core Technologies

| Technology | Version | Purpose | Why Recommended |
|------------|---------|---------|-----------------|
| Astro | 5.18.x | Static site framework | Zero-JS by default, islands architecture for interactive charts, native Cloudflare Pages support, #1 in 2025 State of JS for interest/satisfaction. Static mode outputs plain HTML — ideal for a weekly-updated dashboard. |
| Chart.js | 4.5.1 | Historical trend line chart + contributing factors bar chart | Simple declarative API for standard chart types, responsive out of the box, small bundle (~60KB), no framework dependency. Use for the two "standard" chart types in this project. |
| D3.js | 7.9.0 | Custom needle gauge element | D3's arc, scale, and transform primitives are the industry-standard tool for custom SVG visualization. The gauge is the signature visual; it needs custom rendering that Chart.js cannot provide. Use only d3-scale, d3-shape, and d3-transition modules — not the full bundle. |
| Tailwind CSS | 4.x (via @tailwindcss/vite) | Utility-first styling | Dominant CSS approach in the Astro ecosystem for 2025/2026. v4 ships a Vite plugin that integrates cleanly into Astro 5.2+. CSS-first configuration, OKLCH color system, container queries. Handles responsive layout and design token consistency without a separate design system. |
| TypeScript | 5.x (bundled with Astro) | Type safety | Astro ships with TypeScript support. Use `astro/tsconfigs/strict` preset. Catches JSON schema mismatches between mock data and future pipeline output — important given the data contract requirement. |

### Supporting Libraries

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| @astrojs/check | latest | Astro-aware TypeScript type checking in CI | Use for `astro check` in CI pipeline to catch type errors in .astro files |
| Inter (via Astro Fonts API) | variable font | UI typography | Inter is purpose-built for screen readability, has well-crafted number forms essential for data displays, works well at small sizes for factor labels. Use via Astro's experimental Fonts API (stable enough for production since 5.7.0+) for automatic self-hosting and preload optimization. |
| prettier + prettier-plugin-astro | latest | Code formatting | Astro's official formatter plugin. Handles .astro file syntax that standard Prettier doesn't understand. |

### Development Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| `astro` CLI | Dev server, build, type checking | `npx astro dev`, `npx astro build`, `npx astro check` |
| Wrangler CLI (wrangler) | Cloudflare Pages deployment | `npx wrangler pages deploy ./dist` — optional if using git-connected auto-deploy |
| Node.js 18.17.1+ | Runtime requirement | Astro 5.x requires Node ≥ 18.17.1. Use Node 20 LTS for stability. |

## Installation

```bash
# Scaffold new Astro project (select "Empty" template, TypeScript: strict)
npm create astro@latest

# Add Tailwind CSS v4 (Astro 5.2+ supports `astro add`)
npx astro add tailwind

# Visualization libraries
npm install chart.js d3

# Development / tooling
npm install -D prettier prettier-plugin-astro @astrojs/check
```

**Note on D3:** Install the full `d3` package for convenience during development, but only import the specific submodules you use (`d3-arc`, `d3-scale`, `d3-path`, `d3-transition`). Tree-shaking via Vite will exclude unused D3 modules from the final bundle.

**Note on Cloudflare deployment:** No `@astrojs/cloudflare` adapter is needed for a purely static site. The adapter is only required for SSR/on-demand rendering. Static build output goes to `dist/` and is deployed directly via Cloudflare Pages dashboard or Wrangler CLI.

## Alternatives Considered

| Recommended | Alternative | When to Use Alternative |
|-------------|-------------|-------------------------|
| Astro (static) | Next.js / Nuxt | If you need server-side rendering, ISR, or a React/Vue component ecosystem. Not needed here — weekly static updates don't justify a running server. |
| Tailwind CSS v4 | Vanilla CSS / CSS Modules | If the project had a strong existing design system or strong designer preference. Tailwind is the clear standard in the Astro ecosystem for new projects in 2025/2026. |
| D3.js (submodules) for gauge | d3-simple-gauge (library) | d3-simple-gauge is abandoned — last release August 2021, only supports D3 v5, not v6/v7. Build the gauge as a custom SVG component using D3 primitives directly (arc generator + transform for needle rotation). ~50 lines of code; more control than any library. |
| D3.js for gauge | Chart.js with custom plugin | Chart.js does not natively support gauge/speedometer charts. Building a custom plugin for it is more complex than writing the gauge in D3 directly. |
| Inter (self-hosted via Astro Fonts API) | Google Fonts CDN | Google Fonts CDN adds DNS lookup overhead and sends user IP to Google. Astro's experimental Fonts API self-hosts and auto-generates preload links. The "experimental" label is misleading — it has been in production use since Astro 5.7.0 (mid-2025) and is actively refined. |
| Chart.js for trend + factors | D3.js for all charts | D3 for standard charts requires far more boilerplate. Chart.js handles line and bar charts with one config object. Split responsibility: Chart.js for standard charts, D3 for custom gauge. |
| Chart.js for trend + factors | Recharts / Victory | Both require React or another UI framework as a dependency. This project does not need a UI framework. Chart.js works standalone in vanilla JS Astro islands. |

## What NOT to Use

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| React / Vue / Svelte as Astro integration | Adds framework runtime to the bundle with no benefit for this project. Chart.js and D3 are both vanilla JS libraries that work in plain `<script>` tags inside Astro components. Astro client islands work without a UI framework. | Vanilla JS `<script>` blocks in Astro components with `is:inline` or `type="module"` |
| `@astrojs/cloudflare` adapter | Only needed for SSR. Static sites deploy without it. Adding the adapter unnecessarily opts you into on-demand rendering complexity. | Remove from config; deploy `dist/` directly |
| `@astrojs/tailwind` (legacy integration) | Deprecated for Tailwind v4. The old integration used Tailwind 3. | `@tailwindcss/vite` Vite plugin (added via `npx astro add tailwind`) |
| d3-simple-gauge or d3gauge npm packages | Both are abandoned (2021 or older), only support D3 v4/v5, unmaintained. | Custom SVG gauge component using D3 v7 primitives directly |
| google-fonts CDN `<link>` tag | Adds external DNS dependency, GDPR concerns, and render-blocking risk. | Astro experimental Fonts API (self-hosted, preloaded) |
| Chart.js 3.x | Legacy major version. Chart.js 4.x has breaking API changes and is the current supported version. | chart.js@^4.5.1 |

## Stack Patterns by Variant

**For the needle gauge component:**
- Implement as an Astro `.astro` component with an inline `<svg>` element and a `<script>` block
- Use `client:load` directive if the gauge needs to animate on page load
- D3 arc generator creates the color band arcs; a `<line>` or `<path>` element rotated via CSS transform handles the needle
- Pass the score value via an Astro component prop at build time (static data) or via a `data-*` attribute readable by the client script

**For Chart.js charts (trend + factors):**
- Create a `<canvas>` element in the Astro component
- Initialize Chart.js in a `<script>` block using `import Chart from 'chart.js/auto'`
- Embed JSON data in the page via a `<script type="application/json" id="chart-data">` element to bridge build-time data to client-side scripts without a framework
- Use `client:visible` if charts are below the fold to defer hydration

**For JSON data import (mock data):**
- Place `current.json`, `history.json`, and `factors.json` in `src/data/` (or `public/data/`)
- Import directly in Astro frontmatter: `import currentData from '../data/current.json'`
- Data is inlined at build time — no runtime fetch needed. For charts that need runtime access to the data, pass as a `data-*` prop or inline as a script element.

## Version Compatibility

| Package A | Compatible With | Notes |
|-----------|-----------------|-------|
| astro@5.18.x | Node.js 18.17.1+ | Must use Node 20 LTS for stable long-term development |
| astro@5.18.x | @tailwindcss/vite@^4.0 | `npx astro add tailwind` handles this automatically from Astro 5.2+ |
| chart.js@^4.5.1 | No framework required | Works in vanilla JS; no react-chartjs-2 needed |
| d3@^7.9.0 | No framework required | Tree-shakeable; import only needed submodules |
| tailwindcss@^4.x | astro@^5.2.0 | v4 requires Astro 5.2+ for the `astro add` command; manual setup works on earlier versions |

## Sources

- https://astro.build/blog/whats-new-february-2026/ — Confirmed Astro 5.18 as current stable (MEDIUM confidence, from blog post)
- https://docs.astro.build/en/guides/deploy/cloudflare/ — Confirmed no adapter required for static sites (HIGH confidence, official docs)
- https://docs.astro.build/en/reference/experimental-flags/fonts/ — Fonts API status: experimental since 5.7.0, actively maintained (HIGH confidence, official docs)
- https://docs.astro.build/en/guides/typescript/ — TypeScript config `strict` preset (HIGH confidence, official docs)
- https://docs.astro.build/en/guides/imports/ — JSON import support at build time (HIGH confidence, official docs)
- https://github.com/chartjs/Chart.js/releases — Chart.js 4.5.1 current version (MEDIUM confidence, search result from GitHub)
- https://github.com/antoinebeland/d3-simple-gauge — Abandoned: last release 2021, D3 v5 only (HIGH confidence, GitHub inspection)
- https://tailwindcss.com/docs/installation/framework-guides/astro — Tailwind v4 with Astro via Vite plugin (HIGH confidence, official docs)
- https://d3js.org/ — D3 7.9.0 current version (MEDIUM confidence, multiple sources agree)
- https://dev.to/absurdityindex/building-a-congressional-satire-site-with-astro-5-tailwind-css-v4-and-cloudflare-pages-3hoe — Real-world Astro 5 + Tailwind v4 + Cloudflare Pages project (LOW confidence, community article, corroborates other sources)

---
*Stack research for: Revolution Index — static data visualization dashboard*
*Researched: 2026-03-01*
