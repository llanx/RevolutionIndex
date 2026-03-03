# Pitfalls Research

**Domain:** Static data visualization dashboard (Astro + Chart.js + D3.js + Cloudflare Pages)
**Researched:** 2026-03-01
**Confidence:** MEDIUM-HIGH (verified with official docs and multiple community sources)

---

## Critical Pitfalls

### Pitfall 1: Chart.js Breaks with "window is not defined" Error

**What goes wrong:**
Chart.js accesses browser globals (`window`, `document`, `HTMLCanvasElement`) when the module is imported. Astro components execute server-side by default during the build step. Importing Chart.js into an Astro component frontmatter or a non-hydrated script tag triggers a `ReferenceError: window is not defined` at build time, which silently breaks the build or crashes the dev server.

**Why it happens:**
Astro's static build runs Node.js, not a browser. Developers familiar with standard HTML/JS projects assume `import Chart from 'chart.js/auto'` is safe anywhere. It is not — it must live in browser-only execution context. The default assumption is wrong for Astro.

**How to avoid:**
Place all Chart.js code inside a `<script>` tag in the Astro component body (not frontmatter), or use `client:only` on any framework component wrapping Chart.js. The `<script>` tag approach is simplest for a static-only project:

```astro
---
// frontmatter: NO Chart.js imports here
---
<canvas id="trend-chart"></canvas>
<script>
  import Chart from 'chart.js/auto';
  // chart init code here
</script>
```

**Warning signs:**
- Build output includes `ReferenceError: window is not defined`
- Dev server crashes on route with chart component
- Chart renders in dev but is missing in production (async loading issue)

**Phase to address:** Project setup / first chart component build — must be established before any visualization work begins.

---

### Pitfall 2: Cloudflare Pages Silently Routes Deployment to Workers Instead of Pages

**What goes wrong:**
Cloudflare is consolidating Pages and Workers into a unified platform. During project creation via the dashboard UI, static Astro sites can be silently routed to Workers instead of Pages. The deployment URL shows `*.workers.dev` instead of `*.pages.dev`. The build "succeeds" but the routing, preview deployments, and URL structure are wrong. This costs significant debugging time because nothing appears broken at first glance.

**Why it happens:**
Cloudflare's UI detects certain build artifacts or adapter configurations and defaults to Workers. The platform migration is ongoing and the UI is ambiguous. There is a "Shift to Pages" link buried in project settings but it is extremely subtle — one developer reported spending 90 minutes finding it.

**How to avoid:**
After creating the Pages project, immediately verify the deployment URL domain ends in `*.pages.dev`. If it shows `*.workers.dev`, navigate to project settings and use the "Shift to Pages" option. Do not install `@astrojs/cloudflare` adapter for a purely static site — the adapter is SSR-only and its presence can trigger Workers routing.

**Warning signs:**
- Post-deploy URL is `yourproject.workers.dev` not `yourproject.pages.dev`
- No automatic preview deployments visible for PRs
- Deployment logs reference Worker configuration instead of Pages build

**Phase to address:** Deployment setup phase — verify URL domain immediately after first deploy.

---

### Pitfall 3: Wrong Build Output Directory ("Deployment Successful" but Blank Page)

**What goes wrong:**
Cloudflare Pages requires knowing where your build tool writes its output. Astro writes to `dist/`. If the Pages configuration points to a wrong directory (commonly `public/` — which is Astro's static assets input folder, not output), Cloudflare deploys an empty or wrong directory. The dashboard shows green "deployment successful" but the site is blank or serves only static assets with no HTML.

**Why it happens:**
Hugo, Gatsby, and many SSGs use `public/` as output. Developers switching from those frameworks, or following generic Cloudflare Pages tutorials, set the wrong directory. Astro's `public/` directory has the opposite meaning: it is where unprocessed static assets go *in*, not where the build goes *out*.

**How to avoid:**
Set the Cloudflare Pages build output directory to `dist` — no leading slash needed, no trailing slash. Confirm by running `npm run build` locally and verifying `dist/index.html` exists before configuring Cloudflare.

**Warning signs:**
- Cloudflare shows green build status but visiting the URL shows a blank page or 404
- The deployed site shows only images/files from `public/` with no styled HTML
- Build logs show "success" but no HTML files listed in upload step

**Phase to address:** Deployment setup phase — must be set correctly before any deployment testing.

---

### Pitfall 4: D3.js Needle Gauge Has Fixed Pixel Dimensions — Breaks on Mobile

**What goes wrong:**
D3.js gauge charts are commonly implemented with hardcoded `width` and `height` values (e.g., `width: 400, height: 300`). The SVG renders correctly on desktop but is clipped, tiny, or overflows its container on mobile. The viewBox attribute must be set correctly or the SVG will not scale with the container.

**Why it happens:**
D3 requires explicit dimensions to calculate arc radii, needle length, and center coordinates — so developers hardcode them. They test on desktop, it looks fine, and the mobile case is not caught until later. The difference between SVG `width`/`height` attributes and `viewBox` scaling behavior is non-obvious.

**How to avoid:**
Use `viewBox` and remove hardcoded `width`/`height` on the SVG element, allowing CSS to control container sizing:
```javascript
const svg = d3.select('#gauge')
  .append('svg')
  .attr('viewBox', `0 0 ${width} ${height}`)
  .attr('preserveAspectRatio', 'xMidYMid meet')
  .style('width', '100%')
  .style('height', 'auto');
```
Calculate all internal D3 coordinates relative to `width` and `height` constants, then let CSS handle the actual rendered size.

**Warning signs:**
- Gauge looks perfect on 1440px viewport, broken on 375px
- SVG has `width="400" height="300"` attributes directly on the element
- Container has `overflow: hidden` to hide clipping (a band-aid, not a fix)

**Phase to address:** Gauge component build phase — implement responsive viewBox from day one, not as a retrofit.

---

### Pitfall 5: JSON Data Schema Changes Break the Frontend

**What goes wrong:**
The v1 site uses mock JSON data. When the real data pipeline is plugged in later (Phase 4+ of the broader project), if the JSON schema has drifted from what the frontend expects, every visualization breaks simultaneously. This is the most likely source of a complete frontend regression at pipeline integration time.

**Why it happens:**
Mock data is created casually during frontend build — fields are added, renamed, or structured differently than what the pipeline will actually produce. Since the frontend and pipeline are built in separate workstreams with no enforced contract, schema drift accumulates silently.

**How to avoid:**
Define the JSON schema explicitly before writing a single line of frontend code. Treat it as a contract document, not implementation detail. Store schema definitions alongside the mock data files. Use the same field names, nesting structure, and data types as the future pipeline will produce. Consider adding a simple JSON schema validation step (e.g., `ajv`) that runs in CI against the committed data files.

Example schema contract (establish this in Phase 1):
```json
{
  "current": {
    "score": 42.7,
    "timestamp": "2026-02-23T00:00:00Z",
    "factors": [
      { "id": "economic_inequality", "label": "Economic Inequality", "weight": 0.23, "direction": "up" }
    ]
  }
}
```

**Warning signs:**
- Frontend code uses field names like `data.score` while mock JSON has `data.revolution_score`
- Mock data was created by copying from a visualization example rather than designed for this project
- No documented schema in the repo — only the JSON files themselves

**Phase to address:** Phase 1 (project setup / data structure design) — schema must be locked before frontend build begins.

---

## Technical Debt Patterns

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|----------------|-----------------|
| Hardcode gauge dimensions in pixels | Works fast in dev | Mobile layout broken, requires full SVG refactor | Never — use viewBox from start |
| Skip Chart.js `.destroy()` on chart re-renders | Simpler code | Memory leak + ghost event handlers causing hover flicker | Never — always destroy before recreating |
| Use `client:load` on all interactive components | Simple mental model | All JS hydrates immediately, defeating Astro's lazy loading | Only for above-the-fold critical elements |
| Put JSON data fetch in Astro frontmatter | Clean separation | Data is frozen at build time, stale between deploys without rebuild | Acceptable for static-first approach (this project's intent) |
| Skip `output: 'static'` explicit config in astro.config.mjs | Relies on default | Default can change across Astro versions; ambiguous when reading config | Never — always declare explicitly |
| Use inline style tags instead of CSS variables for gauge colors | Faster to write | Color zone changes require hunting through JS instead of a config object | Never — define color zones as named constants |

---

## Integration Gotchas

| Integration | Common Mistake | Correct Approach |
|-------------|----------------|------------------|
| Cloudflare Pages + Astro | Installing `@astrojs/cloudflare` adapter for a static site | Do NOT install the adapter; it is SSR-only. Static Astro deploys with zero Cloudflare-specific packages. |
| Cloudflare Pages + GitHub | Connecting repo but not setting build command and output dir explicitly | Always set: build command = `npm run build`, output dir = `dist` |
| Chart.js + Astro | Importing Chart.js in component frontmatter | Import only inside `<script>` tags in the component body, never in frontmatter |
| D3.js + Astro | Using `import * as d3 from 'd3'` in frontmatter | Same as Chart.js — D3 must execute client-side inside a `<script>` tag or `client:only` component |
| JSON files + Astro static | Fetching data files with `fetch('/data/current.json')` in frontmatter | Correct pattern for static: import JSON directly at build time using `import data from '../data/current.json'`; use fetch only for client-side updates |
| Cloudflare Pages + Auto Minify | Leaving Cloudflare's "Auto Minify" setting enabled | Disable Auto Minify in Cloudflare dashboard — it conflicts with Astro's hydration markers, causing "Hydration completed but contains mismatches" errors |

---

## Performance Traps

| Trap | Symptoms | Prevention | When It Breaks |
|------|----------|------------|----------------|
| Importing all of D3 (`import * as d3`) | Page weight increases by ~500KB for features never used | Import only needed D3 modules: `import { select, arc, pie } from 'd3'` | Any size — D3 is large, always tree-shake |
| Chart.js without tree-shaking | Bundle includes all chart types and plugins | Use `import { Chart, LineController, ... } from 'chart.js'` with explicit registration | Any size — ~200KB saved vs `chart.js/auto` |
| No loading state for client-side chart initialization | Charts render after visible DOM — users see blank space for 100-500ms | Add CSS skeleton/placeholder that hides before chart canvas is painted | Even on fast connections — noticeable flash |
| Re-fetching JSON on every component mount | Multiple network requests for same data file | Fetch once at page level, pass as props; or use module-level cache | Not a problem with one component, breaks with multiple charts |
| D3 needle animation on every page load | Expensive requestAnimationFrame on slow devices | Make animation optional; `prefers-reduced-motion` media query should skip animation | Low-end mobile devices |

---

## Security Mistakes

| Mistake | Risk | Prevention |
|---------|------|------------|
| Storing API keys or pipeline tokens in committed JSON data files | Secret exposure in public repo | Keep all secrets in GitHub Actions secrets, never in committed files; JSON data files contain only scores and timestamps |
| Setting Cloudflare Pages project to private repo access without verifying deploy key scope | Pipeline webhook may stop working | Use Cloudflare's GitHub App integration, not personal access tokens |
| No `.gitignore` for generated `dist/` directory | Committed build artifacts conflict with Cloudflare Pages build | Add `dist/` to `.gitignore`; Cloudflare Pages runs its own build |
| Trusting `data/current.json` format without validation | Frontend silently displays wrong/corrupted data if pipeline produces bad JSON | Add a JSON schema validation step in the GitHub Actions pipeline before commit |

---

## UX Pitfalls

| Pitfall | User Impact | Better Approach |
|---------|-------------|-----------------|
| Using only color to communicate gauge severity zones | Colorblind users (8% of males) cannot distinguish red/yellow/green zones | Add labels ("LOW", "ELEVATED", "CRITICAL") and pattern fills in addition to color |
| Displaying raw probability score without confidence interval | Users treat point estimate as certainty, misread small changes as significant | Show score range or "±X" uncertainty marker when methodology supports it |
| Gauge needle animates on every page visit including revisits | Repetitive animation feels gimmicky after first visit | Animate on first visit only (sessionStorage flag); on revisits jump to current position |
| Contributing factors sorted alphabetically | Users cannot quickly identify what's most important | Sort by absolute weight/contribution magnitude, highest first |
| No "last updated" timestamp visible | Users cannot tell if data is current or stale (especially if pipeline fails) | Always show `data.timestamp` formatted as "Updated: Feb 23, 2026" near the score |
| Mobile gauge too small to read needle position | Core feature fails on mobile, which is likely 50%+ of traffic | Test gauge at 375px width; minimum needle endpoint visibility must be verified on real device |
| Methodology page with all sections collapsed by default | Users who want depth don't realize content exists | Show section headings clearly visible; one section open by default with summary content |

---

## "Looks Done But Isn't" Checklist

- [ ] **Gauge:** Verify needle renders correctly at score=0, score=50, score=100 (boundary conditions) — the arc math often breaks at exact min/max
- [ ] **Gauge:** Test on 375px mobile viewport — hardcoded SVG dimensions commonly clip the gauge at mobile sizes
- [ ] **Charts:** Open browser DevTools Memory tab, navigate to page, check for growing heap on repeated gauge updates — Chart.js destroy() may be missing
- [ ] **Data loading:** Open Network tab, verify only one fetch to `current.json` fires (not one per component)
- [ ] **Cloudflare deployment:** Confirm deployment URL is `*.pages.dev` not `*.workers.dev` after first deploy
- [ ] **Build output:** Run `npm run build` locally, verify `dist/index.html` exists before pushing
- [ ] **Auto Minify:** Confirm Cloudflare Auto Minify is disabled in dashboard settings (Speed > Optimization > Auto Minify)
- [ ] **Static output mode:** Confirm `astro.config.mjs` has `output: 'static'` explicitly declared
- [ ] **JSON schema:** Document field names in a README or schema file alongside `data/` — future pipeline author must know exact contract
- [ ] **Accessibility:** Run Lighthouse accessibility audit — gauge SVG elements need `aria-label` or `role="img"` with description

---

## Recovery Strategies

| Pitfall | Recovery Cost | Recovery Steps |
|---------|---------------|----------------|
| Chart.js window error in production | LOW | Move import to `<script>` tag; no rebuild of chart logic required |
| Cloudflare deployed to Workers instead of Pages | LOW | Find "Shift to Pages" in project settings; redeploy |
| Wrong build output directory | LOW | Update output directory setting in Cloudflare Pages dashboard; retrigger deploy |
| D3 gauge not responsive (hardcoded dimensions) | MEDIUM | Refactor SVG to use viewBox + CSS width; all coordinate calculations must be re-verified relative to base dimensions |
| JSON schema drift discovered at pipeline integration | HIGH | Audit all frontend field references, update mock data schema, rebuild charts if field structure changed — can take days if schema diverged significantly |
| Chart.js memory leak discovered late | MEDIUM | Find every chart instantiation, add `.destroy()` before reinit; audit is straightforward but testing required |

---

## Pitfall-to-Phase Mapping

| Pitfall | Prevention Phase | Verification |
|---------|------------------|--------------|
| Chart.js window is not defined | Phase 1: Project scaffold | `npm run build` completes without error; charts visible in built site |
| Cloudflare silently routes to Workers | Phase: First deployment | Deployment URL ends in `.pages.dev` |
| Wrong build output directory | Phase: First deployment | `dist/` directory exists post-build; Cloudflare shows files in build log |
| D3 gauge not responsive | Phase: Gauge component build | Manual test at 375px viewport; Lighthouse mobile score |
| JSON schema contract drift | Phase 1: Data structure design | Schema document committed to repo before first chart component |
| Chart.js memory leak | Phase: Chart component build | DevTools Memory tab shows stable heap after 10 page visits |
| Cloudflare Auto Minify conflict | Phase: First deployment | Verify setting disabled; hydration mismatches absent in console |
| Hardcoded gauge color zones | Phase: Gauge component build | Colors defined as named constants in a config object, not literals in D3 code |
| No "last updated" visible | Phase: Dashboard layout | Visual design review confirms timestamp is visible without scrolling |

---

## Sources

- [Astro Official Troubleshooting Docs](https://docs.astro.build/en/guides/troubleshooting/) — window/document SSR errors (HIGH confidence)
- [Astro Deploy to Cloudflare Docs](https://docs.astro.build/en/guides/deploy/cloudflare/) — adapter requirements, static vs SSR config (HIGH confidence)
- [Cloudflare Pages Astro Guide](https://developers.cloudflare.com/pages/framework-guides/deploy-an-astro-site/) — build settings, output dir (HIGH confidence)
- [Cloudflare Pages Limits](https://developers.cloudflare.com/pages/platform/limits/) — 500 builds/month, 20-min timeout, 1 concurrent build (HIGH confidence)
- ["Deploy Astro to Cloudflare Pages Without Getting Screwed"](https://www.gmkennedy.com/blog/deploy-astro-cloudflare-pages/) — Workers silent redirect pitfall (MEDIUM confidence, single source)
- [Cloudflare Static Pages Deploy Guide](https://eastondev.com/blog/en/posts/dev/20251201-cloudflare-static-pages-deploy-guide/) — wrong output directory = blank page (MEDIUM confidence)
- [Chart.js Memory Leak GitHub Issue #462](https://github.com/chartjs/Chart.js/issues/462) — destroy() requirement (HIGH confidence, official repo)
- [D3 Responsive SVG Guide](https://brendansudol.github.io/writing/responsive-d3) — viewBox pattern (MEDIUM confidence)
- [D3 Graph Gallery - Responsive Charts](https://d3-graph-gallery.com/graph/custom_responsive.html) — viewBox + preserveAspectRatio (MEDIUM confidence)
- [FusionCharts — Common Dashboard Mistakes](https://www.fusioncharts.com/blog/the-most-common-mistakes-people-make-with-charts/) — color-only encoding, overloading (MEDIUM confidence)
- [Astro Islands Architecture Docs](https://docs.astro.build/en/concepts/islands/) — client:only behavior, props serialization (HIGH confidence)

---
*Pitfalls research for: Static data visualization dashboard — Revolution Index*
*Researched: 2026-03-01*
