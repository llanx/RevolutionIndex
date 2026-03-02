# Phase 3: Content and Launch - Research

**Researched:** 2026-03-01
**Domain:** Astro content pages, Open Graph meta tags, Cloudflare Pages deployment
**Confidence:** HIGH (deployment, OG meta), MEDIUM (disclaimer/content framing)

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| CONT-01 | Methodology page exists with expandable sections and placeholder structure | Native HTML `<details>`/`<summary>` in a new `src/pages/methodology.astro` page; no library required |
| CONT-02 | Methodology page sections cover: data sources, model approach, score calculation, limitations | Static Astro page with four `<details>` blocks; content marked "coming soon" inline |
| CONT-03 | Disclaimer text is visible on the dashboard explaining what the score is and isn't | Static text block added to `src/pages/index.astro` inside `BaseLayout`; no interactivity needed |
| CONT-04 | About section explains the project's purpose and approach | Static text section in `src/pages/index.astro` or a dedicated `src/pages/about.astro` page |
| SITE-03 | Open Graph meta tags set so shared links display site name, description, and preview image | Extend `BaseLayout.astro` to accept `description` and `ogImage` props; add `<meta property="og:*">` tags; static PNG image at `public/og.png` |
| SITE-04 | Site is deployed and publicly accessible on Cloudflare Pages | Connect GitHub repo to Cloudflare Pages dashboard (Git integration); build command `npm run build`, output directory `dist` |
</phase_requirements>

---

## Summary

Phase 3 has two distinct work streams: (1) content additions to the Astro site and (2) deploying the site publicly on Cloudflare Pages. The content work is straightforward static Astro — a new methodology page using native HTML `<details>`/`<summary>` for expandable sections, a disclaimer block on the dashboard, and an About section. None of this requires new libraries or complex patterns.

The deployment work is also well-understood. The project already has `site: 'https://revolutionindex.pages.dev'` set in `astro.config.mjs`, which is the exact value Astro needs to generate absolute URLs for Open Graph. Deploying to Cloudflare Pages requires connecting the GitHub repository through the Cloudflare dashboard with build command `npm run build` and output directory `dist`. The free tier is unlimited bandwidth for static assets, with a 500-build/month cap and 20,000-file limit — both non-issues for this project.

Open Graph support requires extending `BaseLayout.astro` with OG meta tags and providing a static `public/og.png` image (1200x630px, under 5MB). The simplest approach is a manually created static PNG rather than Satori-based generation, since this site has one shared OG image, not per-page dynamic images. The `Astro.site` variable (already configured) enables absolute URL generation.

**Primary recommendation:** Use native `<details>`/`<summary>` for the methodology accordion, extend `BaseLayout.astro` with OG meta tags accepting props, create one static OG PNG in `public/`, and deploy via Cloudflare Pages Git integration from the Cloudflare dashboard.

---

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Astro | ^5.0.0 (already installed) | Static page generation | Already in project; methodology page is just a new `.astro` file |
| HTML `<details>`/`<summary>` | Native browser | Expandable accordion sections | Zero-JS, keyboard-accessible, no library needed; supported in all modern browsers |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| Wrangler CLI | latest | Manual CLI deploys to Cloudflare Pages | If you want to deploy from the command line without the dashboard |
| sharp + satori | latest | Generate OG images programmatically | Only needed for per-page dynamic OG images; NOT needed for this project's single static OG image |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Native `<details>`/`<summary>` | JavaScript accordion component | JS accordion adds interactivity (animations, exclusive open) but breaks SITE-05 (minimal JS) and adds complexity for no user benefit on a simple methodology page |
| Static hand-made PNG for OG | Satori + sharp build-time generation | Satori is powerful for per-page images but requires `npm install satori sharp`, embedding fonts (~400KB+), and an API route endpoint. For a single global OG image, a static PNG is 10x simpler |
| Cloudflare Pages Git integration | Wrangler CLI direct upload | Git integration is fully automated (every push deploys); CLI is useful if you want manual control. Git integration is recommended for this project |
| Custom disclaimer copy | Boilerplate legal disclaimer | This site is data/analysis content, not a political campaign, so FEC-style disclaimers are NOT required. A plain "not a prediction" disclaimer is appropriate and sufficient |

**Installation:** No new packages required for core Phase 3 work. OG image approach uses a static PNG file.

---

## Architecture Patterns

### Recommended Project Structure

```
src/
├── layouts/
│   └── BaseLayout.astro      # Extend with OG meta tag props
├── pages/
│   ├── index.astro           # Add disclaimer block + About section
│   └── methodology.astro     # NEW: methodology page with <details> sections
public/
├── data/                     # Existing JSON data files
└── og.png                    # NEW: 1200x630 static OG preview image
```

### Pattern 1: Extending BaseLayout.astro with OG Meta Tags

**What:** Accept `description` and `ogImage` props in `BaseLayout.astro`, add `<meta property="og:*">` tags to `<head>`. Pages that need non-default values pass them as props; others use defaults.

**When to use:** All pages — the layout is shared.

**Example:**
```astro
---
// src/layouts/BaseLayout.astro
import '../styles/global.css';

export interface Props {
  title: string;
  description?: string;
  ogImage?: string;
}

const {
  title,
  description = 'A data-driven dashboard tracking the US revolution probability score.',
  ogImage = '/og.png',
} = Astro.props;

// Astro.site is 'https://revolutionindex.pages.dev' (already set in astro.config.mjs)
const canonicalURL = new URL(Astro.url.pathname, Astro.site);
const ogImageURL = new URL(ogImage, Astro.site);
---
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title}</title>
    <meta name="description" content={description} />

    <!-- Open Graph -->
    <meta property="og:type" content="website" />
    <meta property="og:url" content={canonicalURL} />
    <meta property="og:site_name" content="Revolution Index" />
    <meta property="og:title" content={title} />
    <meta property="og:description" content={description} />
    <meta property="og:image" content={ogImageURL} />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />

    <!-- Twitter/X Card -->
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content={title} />
    <meta name="twitter:description" content={description} />
    <meta name="twitter:image" content={ogImageURL} />
  </head>
  <body>
    <slot />
  </body>
</html>
```

### Pattern 2: Methodology Page with Native HTML Accordion

**What:** A new `src/pages/methodology.astro` using `<details>`/`<summary>` for four expandable sections. Each section has a heading and placeholder "coming soon" body.

**When to use:** Any content page requiring expandable sections with zero JavaScript.

**Example:**
```astro
---
// src/pages/methodology.astro
import BaseLayout from '../layouts/BaseLayout.astro';
---

<BaseLayout
  title="Methodology — Revolution Index"
  description="How the Revolution Index score is calculated: data sources, model approach, and limitations."
>
  <main class="methodology">
    <h1>Methodology</h1>
    <p class="intro">How the Revolution Index score is constructed.</p>

    <div class="accordion">
      <details>
        <summary>Data Sources</summary>
        <div class="accordion-body">
          <p><em>Coming soon.</em> The data sources used to calculate the score will be documented here.</p>
        </div>
      </details>

      <details>
        <summary>Model Approach</summary>
        <div class="accordion-body">
          <p><em>Coming soon.</em> The modeling methodology will be explained here.</p>
        </div>
      </details>

      <details>
        <summary>Score Calculation</summary>
        <div class="accordion-body">
          <p><em>Coming soon.</em> How individual factor scores are weighted and combined will be documented here.</p>
        </div>
      </details>

      <details>
        <summary>Limitations</summary>
        <div class="accordion-body">
          <p><em>Coming soon.</em> Known limitations of the model and score will be listed here.</p>
        </div>
      </details>
    </div>
  </main>
</BaseLayout>
```

### Pattern 3: Disclaimer Block on Dashboard

**What:** A static text block added to `src/pages/index.astro` below the dashboard content. Explains what the score is and is not (not a prediction, not political advocacy, based on mock data for v1).

**When to use:** Once, on the dashboard page. No interactivity required.

**Example:**
```astro
<!-- Add inside <main class="dashboard"> in index.astro, below .dashboard-lower -->
<section class="disclaimer" aria-label="Score disclaimer">
  <p>
    <strong>Note:</strong> The Revolution Index score is a data-driven indicator derived from
    publicly available social, economic, and political signals. It is <em>not</em> a prediction
    of future events, a political endorsement, or a statement of advocacy. The score displayed
    is currently based on demonstration data and does not reflect real-time research.
  </p>
</section>
```

### Pattern 4: Cloudflare Pages Deployment via Git Integration

**What:** Connect the GitHub repo to Cloudflare Pages in the dashboard. Cloudflare builds and deploys on every push to `master`.

**Steps:**
1. Push all code to GitHub (already done — project is a git repo)
2. Log in to `dash.cloudflare.com`
3. Navigate to **Workers & Pages** > **Create** > **Pages** > **Connect to Git**
4. Authorize GitHub, select the `RevolutionIndex` repository
5. Configure build settings:
   - Framework preset: **Astro**
   - Build command: `npm run build`
   - Build output directory: `dist`
   - Node version: 20+ (set via environment variable `NODE_VERSION=20` if needed)
6. Click **Save and Deploy**
7. Site available at `revolutionindex.pages.dev` (matches `astro.config.mjs` `site` value)

### Anti-Patterns to Avoid

- **Using a JavaScript-based accordion:** `<details>`/`<summary>` is native, keyboard-accessible, and requires no JS. Adding a JS accordion library to a page that SITE-05 requires be minimal-JS is wrong.
- **Using a relative path for `og:image`:** Social crawlers require absolute URLs. Always use `new URL(ogImage, Astro.site)`. `Astro.site` is already configured as `https://revolutionindex.pages.dev`.
- **Dynamic OG image generation for a single global image:** Satori + sharp adds significant complexity (font embedding, API route, build step). For one shared OG image, a static PNG in `public/` is correct.
- **Putting the OG image in `src/` instead of `public/`:** Astro copies `public/` verbatim to `dist/`. Images that must be URL-accessible at a known path (like `/og.png`) belong in `public/`.
- **Omitting `og:site_name`:** Required for WhatsApp previews. Easy to miss.
- **Forgetting `twitter:card` meta tag:** Without `twitter:card: summary_large_image`, X/Twitter falls back to a small thumbnail even if `og:image` is set.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Expandable sections | Custom JS toggle with click handlers, aria-expanded state, etc. | Native `<details>`/`<summary>` | Browser handles keyboard, ARIA, and animation natively. Zero JS. |
| OG image (single global) | React component rendered to canvas, PNG export pipeline | Static PNG file in `public/` | Satori/sharp is appropriate for per-page dynamic images; for one static image it's pure overhead |
| Absolute URL construction | String concatenation (`'https://site.com' + path`) | `new URL(path, Astro.site)` | Handles trailing slashes, encoding, and keeps the domain in one place |

**Key insight:** For static content pages on a static site generator, the right answer is almost always "write the HTML." Astro pages are just HTML with a front matter block. The methodology page and disclaimer do not need components, state, or libraries.

---

## Common Pitfalls

### Pitfall 1: OG Image URL Is Relative

**What goes wrong:** Social media crawlers (Facebook, X, Slack, Discord) receive a relative path like `/og.png` instead of `https://revolutionindex.pages.dev/og.png` and fail to load the preview image. The OG card shows with no image.

**Why it happens:** Astro renders `Astro.url.pathname` for the current request path, and developers mistakenly use that instead of constructing absolute URLs.

**How to avoid:** Always use `new URL(imagePath, Astro.site)` to construct OG image URLs. The `site` value in `astro.config.mjs` is already `https://revolutionindex.pages.dev`.

**Warning signs:** OG debugger tools (Facebook Sharing Debugger, opengraph.xyz) show "Could not fetch image" or no image in the preview card.

### Pitfall 2: Cloudflare Pages Build Fails Due to Node Version

**What goes wrong:** Cloudflare Pages defaults to an older Node version (e.g., Node 16) which may not satisfy Astro 5's requirements.

**Why it happens:** Cloudflare Pages has a default Node version that doesn't update automatically.

**How to avoid:** Set the environment variable `NODE_VERSION=20` (or `22`) in the Cloudflare Pages project settings under **Settings > Environment Variables**.

**Warning signs:** Build log shows Node version errors, `npm install` failures mentioning peer dependency issues, or Astro version compatibility warnings.

### Pitfall 3: `Astro.site` Is `undefined` During Local Dev

**What goes wrong:** `new URL(ogImage, Astro.site)` throws a runtime error locally because `Astro.site` returns `undefined` when the site config is set but the dev server doesn't inject it.

**Why it happens:** `Astro.site` is populated from `astro.config.mjs` `site` field, but during `astro dev`, if the URL construction is not guarded, it can produce unexpected results.

**How to avoid:** Provide a fallback: `const ogImageURL = new URL(ogImage, Astro.site ?? 'http://localhost:4321')`. Alternatively, test OG tags against the built output (use `npm run build && npm run preview`).

**Warning signs:** `TypeError: Failed to construct 'URL': Invalid URL` in the dev server console.

### Pitfall 4: `<details>` Default Open State Unexpected

**What goes wrong:** If `<details open>` is accidentally added, sections appear expanded by default, changing the intended "collapsed on load" UX of the methodology page.

**Why it happens:** Copy-paste error or misunderstanding of the `open` attribute.

**How to avoid:** Omit the `open` attribute from all `<details>` elements on the methodology page. CONT-01 specifies expandable sections — they should start collapsed.

### Pitfall 5: Methodology Page Not in Site Navigation

**What goes wrong:** The methodology page exists at `/methodology` but no link to it exists on the site, making it unreachable for users who don't know the URL.

**Why it happens:** Building a page without wiring it into navigation.

**How to avoid:** Add a nav link to `/methodology` in `BaseLayout.astro` or `index.astro`. Also add the URL to the About section text as a reference.

### Pitfall 6: Responsible Framing of "Revolution Probability"

**What goes wrong:** Disclaimer and About copy uses language that comes across as alarmist, political, or as an actual prediction, inviting misuse or reputational risk.

**Why it happens:** The project domain (revolution probability) is politically sensitive. STATE.md flags this explicitly: "Responsible communication copy (disclaimer, framing language) requires editorial judgment."

**How to avoid:** Disclaimer must clearly state: (1) this is a data indicator, not a prediction; (2) it is not political advocacy; (3) v1 uses demonstration data. Review copy for tone before launch. Prefer neutral, analytical language ("indicator," "signal," "historical patterns") over emotive language ("danger," "crisis imminent").

---

## Code Examples

Verified patterns from official sources and project codebase:

### Astro.site-Based Absolute URL for OG Image

```astro
---
// In BaseLayout.astro — Astro.site is 'https://revolutionindex.pages.dev'
// Source: https://docs.astro.build/en/reference/configuration-reference/ (site option)
const ogImageURL = new URL(ogImage ?? '/og.png', Astro.site ?? 'http://localhost:4321');
---
<meta property="og:image" content={ogImageURL} />
```

### Native HTML Expandable Section (Zero JS)

```html
<!-- Source: https://developer.mozilla.org/en-US/blog/html-details-exclusive-accordions/ -->
<details>
  <summary>Section Title</summary>
  <div class="accordion-body">
    <p>Section content here.</p>
  </div>
</details>
```

### Exclusive Accordion (Only One Open at a Time)

```html
<!-- The `name` attribute makes only one open at a time — supported in modern browsers -->
<!-- Source: MDN - HTML details exclusive accordions -->
<details name="methodology">
  <summary>Data Sources</summary>
  <p>Content...</p>
</details>
<details name="methodology">
  <summary>Model Approach</summary>
  <p>Content...</p>
</details>
```

Note: The `name` attribute for exclusive accordions is a newer feature. Browser support is good in Chromium 120+ and Firefox 130+, but Safari support should be verified. Without `name`, standard `<details>` works universally — multiple can be open simultaneously, which is acceptable for a methodology page.

### Full OG Meta Tag Block

```astro
<!-- Essential OG tags — order does not matter -->
<meta property="og:type" content="website" />
<meta property="og:url" content={canonicalURL} />
<meta property="og:site_name" content="Revolution Index" />
<meta property="og:title" content={title} />
<meta property="og:description" content={description} />
<meta property="og:image" content={ogImageURL} />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />

<!-- Twitter/X — "summary_large_image" shows the full image, not a thumbnail -->
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content={title} />
<meta name="twitter:description" content={description} />
<meta name="twitter:image" content={ogImageURL} />
```

### Cloudflare Pages Build Settings (reference)

```
Framework preset:          Astro
Build command:             npm run build
Build output directory:    dist
Node version (env var):    NODE_VERSION=20
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Custom JS accordion with click handlers | Native `<details>`/`<summary>` | ~2020 (baseline browser support) | Zero JS, native keyboard/ARIA support |
| Cloudflare Pages as separate product | Cloudflare Pages merged into Workers & Pages dashboard | 2024 | Navigation changed; find Pages under "Workers & Pages" in Cloudflare dashboard |
| Per-platform OG tags (fb:, twitter: prefixes) | Unified `og:*` with `twitter:card` supplement | ~2022 | Most platforms now read `og:*` first; Twitter-specific tags only needed for card type override |
| Wrangler Pages vs Workers distinction | Wrangler supports `--assets` for static sites | Sept 2025 | Can deploy static assets without a Worker config file using interactive prompts |

**Deprecated/outdated:**
- `twitter:image:src`: Use `twitter:image` instead (the `:src` suffix was an older alias).
- `fb:app_id`: No longer required for basic OG sharing; only needed for Facebook-specific analytics features.
- Cloudflare Pages standalone product: Now integrated into the Workers & Pages section of the Cloudflare dashboard.

---

## Open Questions

1. **OG image creation method**
   - What we know: A static 1200x630 PNG at `public/og.png` is the simplest correct approach. The project already has a design aesthetic established in Phase 2.
   - What's unclear: Does the planner want a pre-made PNG committed to the repo, or should a task generate one programmatically? If the latter, Satori + sharp adds ~30min of setup.
   - Recommendation: Plan a task that creates a static PNG manually (e.g., using Figma, screenshot tool, or a simple HTML-to-PNG approach). This is editorial work, not engineering. Flag it as a manual step.

2. **About section placement**
   - What we know: CONT-04 requires "an About section." It could be a section on the dashboard page (`index.astro`) or a separate `about.astro` page.
   - What's unclear: Requirements don't specify whether this is a page (`/about`) or a section on the dashboard.
   - Recommendation: Default to a section near the bottom of `index.astro` for simplicity. A separate `/about` page is also valid — choose based on content length. If the About copy is 2-3 sentences, inline it. If it needs more space, make it a page.

3. **Navigation between pages**
   - What we know: After Phase 3, there will be at least two pages: `/` (dashboard) and `/methodology`. A nav link is needed.
   - What's unclear: Should `BaseLayout.astro` include a site-wide nav bar, or should links be inline text within pages?
   - Recommendation: Add a minimal `<nav>` to `BaseLayout.astro` with links to Dashboard (`/`) and Methodology (`/methodology`). This is simpler than per-page inline linking and keeps it DRY.

4. **Disclaimer copy — editorial judgment flagged**
   - What we know: STATE.md explicitly flags: "Responsible communication copy requires editorial judgment — flag for content review before launch."
   - What's unclear: The exact disclaimer language is not drafted. The content must avoid implying the score is a real-time prediction or political statement.
   - Recommendation: Draft placeholder disclaimer text during implementation, clearly marked `<!-- TODO: review before launch -->`. The plan should note this requires editorial review.

---

## Validation Architecture

> `workflow.nyquist_validation` is not present in `.planning/config.json` — skipping this section.

---

## Sources

### Primary (HIGH confidence)
- Astro official docs: https://docs.astro.build/en/guides/deploy/cloudflare/ — Cloudflare deployment options, wrangler config
- Cloudflare Pages docs: https://developers.cloudflare.com/pages/framework-guides/deploy-an-astro-site/ — exact build settings
- Cloudflare Pages limits: https://developers.cloudflare.com/pages/platform/limits/ — free tier file/build limits
- Astro configuration reference: https://docs.astro.build/en/reference/configuration-reference/ — `site` option and `Astro.site`
- MDN HTML details/summary: https://developer.mozilla.org/en-US/blog/html-details-exclusive-accordions/ — exclusive accordion with `name` attribute
- Project codebase (`astro.config.mjs`): `site: 'https://revolutionindex.pages.dev'` already configured

### Secondary (MEDIUM confidence)
- Open Graph image dimensions (1200x630): Cross-referenced across multiple sources including share-preview.com and krumzi.com — consistent across the ecosystem
- Astro SEO meta tag patterns: https://eastondev.com/blog/en/posts/dev/20251202-astro-seo-complete-guide/ — verified against Astro.site docs
- Twitter card `summary_large_image`: X Developer Community documentation — twitter:card required for large image format

### Tertiary (LOW confidence)
- `<details name="...">` exclusive accordion browser support: MDN blog post confirms spec exists; Safari support for `name` attribute was added later than Chromium/Firefox. Flag for cross-browser testing.
- Cloudflare Pages Node version default: Multiple community sources suggest older default; verified behavior may vary by account/region. Set `NODE_VERSION=20` proactively.

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — Astro, HTML details/summary, Cloudflare Pages are all mature and well-documented
- Architecture: HIGH — OG meta pattern from official Astro docs; Cloudflare Pages deploy steps from official docs
- Pitfalls: HIGH for OG URL absoluteness and Node version; MEDIUM for disclaimer framing (editorial, not technical)
- `<details name>` exclusive accordion support: LOW — spec is new, browser support table should be verified

**Research date:** 2026-03-01
**Valid until:** 2026-06-01 (stable technology — Astro 5 and Cloudflare Pages deployment patterns change slowly; OG spec is very stable)
