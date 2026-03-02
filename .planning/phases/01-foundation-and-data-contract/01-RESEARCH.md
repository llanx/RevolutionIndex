# Phase 1: Foundation and Data Contract - Research

**Researched:** 2026-03-01
**Domain:** TypeScript JSON schema design, Astro project scaffold, mock data authoring
**Confidence:** HIGH — all stack and architecture decisions are pre-researched and locked in project-level research docs

---

## Summary

Phase 1 is a pure scaffolding and schema-definition phase. No visualization code is written here. The deliverable is a locked JSON data contract (three files in `public/data/`) with matching TypeScript interfaces in `src/lib/data.ts`, plus a passing `npm run build`. Everything downstream — the gauge, the charts, the layout — depends on the field names, nesting structure, and data types established here.

The core technical challenge is not complexity but discipline: defining the JSON schema to serve the frontend's needs (score, timestamp, zone label, factor list, historical time series) while being realistic about what a future Python data pipeline will actually produce. Fields that the frontend needs must be present; fields the pipeline cannot produce must be excluded. Mock data must be realistic enough that charts will render meaningfully (12+ weekly entries, plausible score progression, real factor names).

The stack is already decided: Astro 5.x with TypeScript strict mode, `public/data/` for JSON files, `src/lib/data.ts` for interfaces. The only decisions remaining for this phase are the exact JSON schema shapes and the realistic mock values to populate them with.

**Primary recommendation:** Define the three JSON schemas first as TypeScript interfaces, then generate the JSON files from those interfaces — not the other way around. This prevents any/unknown types from leaking in.

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| DATA-01 | JSON schema defined for current score data (score, timestamp, zone, factors) | Architecture research documents exact field structure for `current.json`; TypeScript interfaces in `src/lib/data.ts` are the schema definition mechanism |
| DATA-02 | JSON schema defined for historical score data (time series of past scores) | Architecture research documents `history.json` shape: `{ entries: [{ date, score }] }`; needs 12+ entries per DATA-04 |
| DATA-03 | Mock data files exist in the repo matching the defined schemas | Three files: `public/data/current.json`, `public/data/history.json`, `public/data/factors.json`; placed in `public/` so they are accessible both at build time and as static URLs |
| DATA-04 | Mock data includes at least 12 data points for charts to render meaningfully | History entries should span 12+ consecutive weekly dates with plausible score variation (not flat) to exercise the Chart.js line chart |
| DATA-05 | JSON schema is documented as the contract for the future data pipeline | Inline JSDoc on TypeScript interfaces + a schema comment block in each JSON file or a `public/data/README` explaining field semantics and the pipeline's obligations |
</phase_requirements>

---

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Astro | 5.18.x | Static site framework and build system | Already decided; project scaffold lives here; `npm run build` outputs `dist/` |
| TypeScript | 5.x (bundled with Astro) | Type-safe interfaces for all JSON shapes | Astro ships TS; `astro/tsconfigs/strict` preset catches schema mismatches at build time |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| @astrojs/check | latest | `astro check` command — validates TypeScript in .astro files | Run as part of `npm run build` to catch type errors across .astro frontmatter |

### No Additional Installs Needed

Phase 1 requires only the base Astro scaffold. No visualization libraries (Chart.js, D3) are installed or used in this phase. Their installation belongs in Phase 2.

**Scaffold command:**
```bash
npm create astro@latest
# Select: Empty template, TypeScript: Strict, no additional integrations
```

---

## Architecture Patterns

### Recommended Project Structure (Phase 1 scope)

```
revolutionindex/
├── public/
│   └── data/
│       ├── current.json       # Current score snapshot (DATA-01, DATA-03)
│       ├── history.json       # Time series — 12+ weekly entries (DATA-02, DATA-04)
│       └── factors.json       # Detailed per-factor data (DATA-01, DATA-03)
├── src/
│   ├── pages/
│   │   └── index.astro        # Minimal stub page — just proves build works
│   ├── layouts/
│   │   └── BaseLayout.astro   # Minimal HTML shell
│   └── lib/
│       └── data.ts            # ALL TypeScript interfaces — the schema contract (DATA-01, DATA-02, DATA-05)
├── astro.config.mjs           # output: 'static' explicitly declared
├── tsconfig.json              # extends astro/tsconfigs/strict
└── package.json
```

**Why `public/data/` not `src/data/`:** Files in `public/` are copied verbatim to `dist/` and are accessible both as build-time imports AND as static URLs (`/data/current.json`). The future pipeline writes to this location; client-side scripts can also fetch from this URL. Do not put data files in `src/` — they get bundled by Vite and lose their URL addressability.

### Pattern 1: TypeScript Interfaces as the Schema Contract

**What:** Define all JSON shapes as TypeScript interfaces in `src/lib/data.ts` BEFORE writing any JSON. Use these interfaces as the ground truth, then author JSON to match.

**Why this order matters:** Writing JSON first and inferring types afterward produces loose types. Writing interfaces first and validating JSON against them catches mistakes immediately at build time.

**Example — `src/lib/data.ts`:**
```typescript
// Source: project architecture decision + Astro TypeScript docs
// This file IS the data contract. The future pipeline must produce JSON
// matching these interfaces exactly.

/** A single contributing factor snapshot */
export interface Factor {
  /** Stable machine identifier — pipeline must use this exact string */
  id: string;
  /** Human-readable display name */
  name: string;
  /** Normalized value 0.0–1.0 representing current factor intensity */
  value: number;
  /** Whether this factor is currently pushing the score up or down */
  direction: 'up' | 'down' | 'neutral';
  /** Relative weight of this factor in the composite score (0.0–1.0, all weights sum to 1.0) */
  weight: number;
}

/** Zone label for the revolution probability spectrum */
export type ZoneLabel =
  | 'Stable'
  | 'Elevated Tension'
  | 'Crisis Territory'
  | 'Revolution Territory';

/** current.json — the live snapshot served on the dashboard */
export interface CurrentData {
  /** Composite revolution probability score, 0–100 */
  score: number;
  /** ISO 8601 timestamp of when this score was calculated */
  timestamp: string;
  /** Human-readable zone label for the current score range */
  zone: ZoneLabel;
  /** Ordered list of contributing factors (highest weight first) */
  factors: Factor[];
}

/** A single point in the historical time series */
export interface HistoryEntry {
  /** ISO 8601 date string (date only, e.g. "2026-03-01") */
  date: string;
  /** Composite score at that date */
  score: number;
}

/** history.json — the full time series for the trend chart */
export interface HistoryData {
  entries: HistoryEntry[];
}

/** Detailed factor data including its own mini time series */
export interface FactorDetail {
  id: string;
  name: string;
  /** Explanation of what this factor measures and why it matters */
  description: string;
  /** Current normalized value 0.0–1.0 */
  current_value: number;
  /** Historical time series for this factor (parallel to HistoryData.entries) */
  historical: Array<{ date: string; value: number }>;
}

/** factors.json — detailed per-factor data for drill-down views */
export interface FactorsData {
  factors: FactorDetail[];
}
```

Confidence: HIGH — TypeScript strict mode, Astro official docs on JSON imports.

### Pattern 2: Build-Time JSON Import Validation

**What:** Import JSON data files in Astro frontmatter with explicit type assertions. TypeScript will catch any mismatch between the JSON shape and the interface.

**Example — `src/pages/index.astro` (stub for Phase 1):**
```astro
---
import type { CurrentData, HistoryData, FactorsData } from '../lib/data';
import currentRaw from '../../public/data/current.json';
import historyRaw from '../../public/data/history.json';
import factorsRaw from '../../public/data/factors.json';

// Type assertion — if JSON doesn't match interface, build fails with clear error
const current = currentRaw as CurrentData;
const history = historyRaw as HistoryData;
const factors = factorsRaw as FactorsData;

// Quick sanity assertion that will surface in build logs if data is wrong
const entryCount = history.entries.length;
---

<html>
  <body>
    <p>Score: {current.score}</p>
    <p>History entries: {entryCount}</p>
  </body>
</html>
```

Confidence: HIGH — Astro imports docs confirm JSON is importable in frontmatter.

### Pattern 3: astro.config.mjs Minimal but Explicit

```javascript
// astro.config.mjs
import { defineConfig } from 'astro/config';

export default defineConfig({
  output: 'static', // Always declare explicitly — default can change across versions
  site: 'https://revolutionindex.pages.dev', // Needed for canonical URLs and OG tags later
});
```

Confidence: HIGH — Astro configuration docs; PITFALLS.md flags skipping explicit `output: 'static'` as technical debt.

### Anti-Patterns to Avoid

- **Defining JSON first, interfaces second:** Produces `any` escape hatches and types that don't reflect intent. Write interfaces first.
- **Using `any` types anywhere in data.ts:** Defeats the entire purpose of the contract. Every field must be typed, including nested objects.
- **Putting JSON in `src/data/` instead of `public/data/`:** Files in `src/` lose their static URL. The future pipeline needs a stable write target; client JS needs a fetchable URL. Use `public/data/`.
- **Flat history array without a wrapper object:** `{ entries: [] }` is better than a bare array `[]` at the JSON root — it allows adding metadata (e.g., `last_updated`, `version`) later without a breaking schema change.
- **Skipping JSDoc on interface fields:** The pipeline author (possibly a different person in the future) needs to know exactly what `value: number` means (is it 0–1 or 0–100? Normalized or raw?). Document inline.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| TypeScript type checking in Astro files | Custom build script | `astro check` via `@astrojs/check` | Astro's checker understands .astro frontmatter context; standard `tsc` does not |
| JSON schema validation | Custom validator | TypeScript strict mode + `as TypeName` assertion | Sufficient for Phase 1; catches shape mismatches at build time without a runtime dependency |

**Key insight:** For this phase, TypeScript IS the schema validation tool. No runtime JSON schema library (ajv, zod) is needed in Phase 1 — the build failing is the validation.

---

## Common Pitfalls

### Pitfall 1: Schema Drift Between Mock Data and Future Pipeline

**What goes wrong:** Mock data field names diverge from what the Python pipeline will produce. When the real pipeline is plugged in, every chart breaks simultaneously.

**Why it happens:** Mock data is authored casually. Fields get renamed for convenience, nesting changes, units differ (0–1 vs 0–100).

**How to avoid:** Document field semantics in JSDoc on the TypeScript interfaces. Use the interfaces as the authority. The JSON files are instances; the interfaces are the law. Add a comment block at the top of each JSON file referencing `src/lib/data.ts` as the schema source.

**Warning signs:** `value` field ranges are inconsistent (some factors use 0–1, others use percentages); `id` fields are not stable machine-readable strings; `timestamp` lacks timezone info.

### Pitfall 2: Insufficient Mock History Causes Flat/Empty Chart

**What goes wrong:** 12 entries minimum is required (DATA-04), but if all entries have nearly identical scores (e.g., all 45–47), the trend chart will render but appear meaningless.

**Why it happens:** Mock data is generated mechanically rather than thoughtfully.

**How to avoid:** Make mock history data tell a story — a gradual rise over 2024, a plateau, a spike in late 2025, settling to current. This exercises the chart's range and makes the visualization meaningful for Phase 2 development.

**Warning signs:** All 12+ history entries have scores within a 5-point band; no variation in `direction` fields across factors.

### Pitfall 3: `npm run build` Succeeds But `dist/` is Missing Data Files

**What goes wrong:** JSON files placed in `src/` are processed by Vite and may not appear at the expected URL in `dist/`. Or they are not copied at all.

**Why it happens:** Developers expect all files to flow through to output. Only `public/` files are guaranteed to copy verbatim.

**How to avoid:** After `npm run build`, verify `dist/data/current.json` exists before calling Phase 1 complete. The success criterion requires a valid `dist/` directory.

**Warning signs:** `dist/` exists with `index.html` but no `data/` subdirectory.

### Pitfall 4: TypeScript `resolveJsonModule` Not Enabled

**What goes wrong:** `import currentRaw from '../../public/data/current.json'` produces a TypeScript error about module resolution.

**Why it happens:** `resolveJsonModule` must be true in tsconfig. Astro's strict preset should include it, but worth verifying.

**How to avoid:** Use `extends: "astro/tsconfigs/strict"` in `tsconfig.json`. Verify `resolveJsonModule` is inherited. If not, add it explicitly.

```json
{
  "extends": "astro/tsconfigs/strict",
  "compilerOptions": {
    "resolveJsonModule": true
  }
}
```

Confidence: HIGH — Astro TypeScript docs confirm strict preset includes this.

---

## Code Examples

### current.json — Realistic Mock

```json
{
  "_schema": "src/lib/data.ts#CurrentData",
  "_note": "Pipeline must produce JSON matching this exact structure",
  "score": 47,
  "timestamp": "2026-03-01T00:00:00Z",
  "zone": "Elevated Tension",
  "factors": [
    {
      "id": "economic_inequality",
      "name": "Economic Inequality",
      "value": 0.72,
      "direction": "up",
      "weight": 0.22
    },
    {
      "id": "institutional_trust",
      "name": "Institutional Trust",
      "value": 0.31,
      "direction": "down",
      "weight": 0.18
    },
    {
      "id": "political_polarization",
      "name": "Political Polarization",
      "value": 0.78,
      "direction": "up",
      "weight": 0.20
    },
    {
      "id": "unemployment_stress",
      "name": "Unemployment & Economic Stress",
      "value": 0.44,
      "direction": "neutral",
      "weight": 0.15
    },
    {
      "id": "protest_intensity",
      "name": "Protest Activity",
      "value": 0.58,
      "direction": "up",
      "weight": 0.25
    }
  ]
}
```

### history.json — 14-Entry Mock (exceeds 12-week minimum)

```json
{
  "_schema": "src/lib/data.ts#HistoryData",
  "entries": [
    { "date": "2025-11-30", "score": 38 },
    { "date": "2025-12-07", "score": 36 },
    { "date": "2025-12-14", "score": 39 },
    { "date": "2025-12-21", "score": 41 },
    { "date": "2025-12-28", "score": 40 },
    { "date": "2026-01-04", "score": 43 },
    { "date": "2026-01-11", "score": 42 },
    { "date": "2026-01-18", "score": 44 },
    { "date": "2026-01-25", "score": 46 },
    { "date": "2026-02-01", "score": 45 },
    { "date": "2026-02-08", "score": 47 },
    { "date": "2026-02-15", "score": 46 },
    { "date": "2026-02-22", "score": 48 },
    { "date": "2026-03-01", "score": 47 }
  ]
}
```

### factors.json — Detailed Factor Data

```json
{
  "_schema": "src/lib/data.ts#FactorsData",
  "factors": [
    {
      "id": "economic_inequality",
      "name": "Economic Inequality",
      "description": "Measures the concentration of wealth and income disparities. Elevated inequality correlates with historical preconditions for mass unrest.",
      "current_value": 0.72,
      "historical": [
        { "date": "2026-02-01", "value": 0.70 },
        { "date": "2026-02-15", "value": 0.71 },
        { "date": "2026-03-01", "value": 0.72 }
      ]
    },
    {
      "id": "protest_intensity",
      "name": "Protest Activity",
      "description": "Tracks frequency, size, and geographic spread of organized public demonstrations. A leading indicator of mass mobilization capacity.",
      "current_value": 0.58,
      "historical": [
        { "date": "2026-02-01", "value": 0.49 },
        { "date": "2026-02-15", "value": 0.53 },
        { "date": "2026-03-01", "value": 0.58 }
      ]
    }
  ]
}
```

---

## State of the Art

| Old Approach | Current Approach | Impact |
|--------------|------------------|--------|
| JSON schema in a separate `schema.json` file | TypeScript interfaces in `src/lib/data.ts` as the contract | No separate tooling; build fails on mismatch; interfaces serve as documentation |
| `src/data/` for JSON data files | `public/data/` for JSON data files | Files are both importable at build time AND accessible at static URL — dual access needed for pipeline integration |

---

## Open Questions

1. **Zone boundary thresholds for score-to-label mapping**
   - What we know: Four zones planned ("Stable", "Elevated Tension", "Crisis Territory", "Revolution Territory"); spec notes boundaries depend on empirical data
   - What's unclear: The exact score ranges for each zone (e.g., 0–25 = Stable, 26–50 = Elevated, etc.)
   - Recommendation: For Phase 1 mock data, use placeholder boundaries (0–25, 26–50, 51–75, 76–100) hardcoded in `data.ts`. Document that these are provisional and will be calibrated when the model is built. The `ZoneLabel` union type is the contract; boundary values are implementation detail.

2. **Factor count — exactly 5 or flexible?**
   - What we know: DASH-07 says "5-6 factors"; spec says "contributing factors breakdown"
   - What's unclear: Whether the interface should enforce a fixed count or allow any number
   - Recommendation: Interface allows any `Factor[]` array. Mock data uses exactly 5 factors. Document that the Phase 2 UI is designed for 5–6 and the pipeline should respect that practical constraint.

3. **`factors.json` historical entry count**
   - What we know: `history.json` needs 12+ entries; `factors.json` has per-factor history
   - What's unclear: Whether per-factor history needs 12+ entries too, or just 2–3 for sparklines
   - Recommendation: 3 entries per factor is sufficient for Phase 1. Phase 2 will determine if the factors chart needs deeper history.

---

## Sources

### Primary (HIGH confidence)
- `.planning/research/ARCHITECTURE.md` — JSON file placement (`public/data/`), build-time import patterns, data bridging patterns, anti-patterns
- `.planning/research/STACK.md` — Astro 5.18.x, TypeScript strict preset, `astro/tsconfigs/strict`, `resolveJsonModule`
- `.planning/research/PITFALLS.md` — Schema drift pitfall (Pitfall 5), JSON-in-src anti-pattern (Anti-Pattern 3)
- `.planning/REQUIREMENTS.md` — DATA-01 through DATA-05 exact definitions
- `.planning/ROADMAP.md` — Phase 1 success criteria (5 criteria, verbatim)
- `spec.md` — Data flow design, field names for `current.json`, `history.json`, `factors.json`

### Secondary (MEDIUM confidence)
- Architecture research: build-time import path `import data from '../../public/data/current.json'` — confirmed pattern from Astro docs

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — Astro scaffold, TypeScript interfaces, `public/data/` location all verified in prior research
- Architecture: HIGH — file structure and import patterns are directly from ARCHITECTURE.md which cites official Astro docs
- Pitfalls: HIGH — schema drift, data location, and `resolveJsonModule` all sourced from PITFALLS.md and verified sources
- Mock data design: MEDIUM — field names and values are design decisions, not researched facts; plausible but pipeline author may adjust

**Research date:** 2026-03-01
**Valid until:** 2026-04-01 (stable domain — Astro TypeScript JSON import behavior is not fast-moving)
