# Feature Research

**Domain:** Public data index / single-metric dashboard (revolution probability tracker)
**Researched:** 2026-03-01
**Confidence:** MEDIUM-HIGH (based on analysis of CNN Fear & Greed Index, Doomsday Clock, Fragile States Index, FiveThirtyEight, Our World in Data, Transparency International CPI, Alternative.me Crypto F&G)

---

## Feature Landscape

### Table Stakes (Users Expect These)

Features users assume exist on any serious public index site. Missing these makes the product feel unfinished or untrustworthy.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Single prominent score display | Every comparable index (Fear & Greed: 0-100, Doomsday Clock: seconds-to-midnight, CPI: 0-100) leads with one number. Users arrive expecting to immediately see "the number." | LOW | Needle gauge is the right call per spec — familiar from speedometers, instantly scannable |
| Color-coded severity zones | Fear & Greed uses red/amber/green, Doomsday uses clock-face position, FSI uses heat maps. Users parse meaning through color before reading labels. | LOW | Zones (stable / elevated / critical) must be defined — currently deferred per spec, use placeholder zones for v1 |
| Historical trend chart | Every index provides time-series context. Without it, a single number has no meaning — users cannot tell if 63 is rising, falling, or stable. | MEDIUM | Line chart is the standard; show at minimum 6-12 months of mock history |
| "Last updated" timestamp | Users on any data site check when the data was last refreshed. Absent timestamp → distrust. Becomes more important when data is NOT real-time. | LOW | Show date of last update prominently near the score; weekly cadence means this matters |
| Contributing factors / components breakdown | Fear & Greed breaks into 7 weighted sub-indicators. FSI uses 12 indicators across 4 categories. FiveThirtyEight explains signal sources. Users who care at all want to know WHY. | MEDIUM | Bar chart or factor list showing top drivers; spec calls this out explicitly |
| Methodology page (even if sparse) | CPI, Doomsday Clock, and FiveThirtyEight all have dedicated methodology content. Without it, the score is a black box with no credibility. | LOW | Structure + placeholder content is fine for v1; spec explicitly plans this |
| Responsive mobile layout | All modern public dashboards are mobile-accessible. A significant share of viral traffic will arrive on phones (shared link → mobile browser). | MEDIUM | Gauge must work on small screens; collapse layout to single column |
| Disclaimer / framing copy | Every sensitive probability index includes context-setting language: "This is a model, not a prediction." CNN: "does not constitute investment advice." FiveThirtyEight uses weather-forecast framing. | LOW | Spec flags "responsible communication" as an open question — must address in v1 with brief framing copy |
| About / context section | Users arriving from a shared link have no background. They need a brief answer to "what is this?" before they can trust the score. | LOW | One paragraph on the homepage is sufficient; expands into a full About page later |

---

### Differentiators (Competitive Advantage)

Features that set this product apart from generic political index sites. Should connect directly to the core value proposition: "one clear number, immediately understandable, with enough context to trust it."

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Needle gauge as hero element | Gauge charts are cognitively efficient — users process them faster than bar charts or numbers alone because they mirror familiar real-world instruments (speedometers, fuel gauges). No major political instability index uses a needle gauge as its primary visual. | MEDIUM | D3.js or custom SVG per spec. Must animate on load. Color zones (red/amber/green) do the heavy cognitive lifting. |
| Zone labels with plain-language meaning | "63 — Elevated Tension" beats "63." The Doomsday Clock labels like "85 seconds to midnight" carry narrative weight. FiveThirtyEight named their states: "Lean Democrat," "Tossup." Translating a number into a named state reduces cognitive load for casual visitors. | LOW | Four zones max: Stable / Elevated / High / Critical (or similar). Avoid academic language. |
| Factor breakdown with direction arrows | Showing not just which factors contribute, but whether they are worsening or improving (e.g., "Inequality: ↑ rising") gives users a forward-looking signal that static scores do not. No comparable index does this well. | MEDIUM | Requires the mock data structure to include per-factor trend direction (up/down/flat). Adds to the JSON schema design. |
| Clean, accessible non-expert writing | Most political stability indexes (FSI, World Bank, V-Dem) are built for researchers and policy analysts. The language is academic. Writing for a general audience — short sentences, plain terms, no jargon — is a genuine differentiator. | LOW | Editorial/copy decision, not a build decision. But it shapes the methodology page and all UI labels. |
| Shareable social card (Open Graph) | When users share the page, the social preview should show the current score and gauge image. Fear & Greed sites that do this (Alternative.me) get significantly more organic sharing. This is passive distribution. | MEDIUM | Requires a static OG image that reflects the current score, OR a generated/pre-built image updated weekly. Static approach: rebuild the OG image as part of the weekly data pipeline. |
| Structured JSON data schema (public-facing) | FiveThirtyEight and Our World in Data both make their underlying data accessible (CSV downloads, public API). Designing the JSON contract openly — even without a formal API — signals legitimacy and enables third-party use. | LOW | Already in spec as a requirement for the pipeline contract. Framing it as a feature for the methodology page costs nothing extra. |
| Historical events overlay (future) | Marking significant US political events on the historical chart (Jan 6, COVID, elections) would help users correlate score movements with real-world context. No political instability index does this for a general audience. | HIGH | Defer to v2. Requires editorial curation and a data structure for event annotations. |

---

### Anti-Features (Commonly Requested, Often Problematic)

Features that seem like obvious additions but create outsized problems for this specific product.

| Feature | Why Requested | Why Problematic | Alternative |
|---------|---------------|-----------------|-------------|
| Real-time score updates | Users assume live dashboards are better. Fear & Greed (hourly), Crypto F&G (daily) set this expectation. | The revolution probability model updates on weekly economic/political data — there is nothing meaningful to update in real-time. Real-time refresh would imply false precision, create infrastructure complexity, and require a server. Breaks the static architecture entirely. | Make the weekly cadence a feature, not a limitation: "Updated every Sunday. The factors driving revolution don't change hour-to-hour." Frame the weekly refresh as methodologically appropriate. |
| User accounts / personalization | Any dashboard that gains traction gets feature requests for "save my view," "set my alerts," bookmarks. | Accounts require a backend, authentication, session management, and ongoing security maintenance. Contradicts the zero-cost, zero-server constraint. Diverts build time from core features. | Defer all account features permanently until there is clear demand AND budget. Use URL state (like Our World in Data does for chart configs) for any shareable custom views. |
| Comment section / user discussion | Index sites attract strong political opinions. Users will want to "respond" to the score. | Moderation overhead is enormous for politically charged content. The revolution topic will attract bad-faith actors, conspiracy theories, and harassment. Risk of the comments becoming the story. | Link to an external discussion platform (Reddit, a Discord server) where the community can self-moderate. Do not host discussion. |
| Country comparison mode | Natural extension: "What's France's score? What's Brazil's?" This is what FSI and V-Dem do. | Requires data, models, and methodology for every country added. Multiplies the research and modeling work by the number of countries. The value proposition of this site is depth on ONE country, not breadth across many. | Explicitly label this as a US-focused index. Add a footnote: "Global comparison is a future consideration." Resist pressure to add countries until the US model is validated. |
| Prediction / forecast feature | Users may want "where will the score be in 6 months?" | Forecasting political instability carries even greater epistemic uncertainty than the current score. Would require an entirely different modeling approach. Risk of being wrong in a high-stakes, politically charged way. | Focus exclusively on current conditions. Describe the score as "current conditions assessment," not "prediction." |
| Email/push alerts at launch | "Notify me when the score changes" is a natural request. Alternative.me and Amsflow both offer this. | Requires an email service provider, list management, opt-in compliance (CAN-SPAM, GDPR), and ongoing deliverability maintenance. High operational overhead for a v1 with mock data. Alerts on mock data are meaningless. | List email alerts as a planned v2 feature. Collect interest (email address opt-in on the site) without building the actual alert system. |
| Embeddable widget | Other sites may want to embed the gauge. Alternative.me and Bitcoin Magazine Pro both offer embed codes. | Widget hosting requires CORS configuration, versioning, and a reliability commitment. Breaking embeds on third-party sites creates support burden. | Offer static image embeds (just a `<img>` tag pointing to the weekly-updated OG image). No JavaScript widget required. Much lower complexity and maintenance burden. |

---

## Feature Dependencies

```
[Score display (gauge)]
    └──requires──> [Current score data (current.json)]
                       └──requires──> [Mock data system (JSON schema)]

[Historical trend chart]
    └──requires──> [Historical score data (history.json)]
                       └──requires──> [Mock data system (JSON schema)]

[Contributing factors breakdown]
    └──requires──> [Factor weights data (factors.json)]
                       └──requires──> [Mock data system (JSON schema)]

[Methodology page]
    └──requires──> [JSON schema defined] (to describe data sources accurately)

[Shareable social card (OG image)]
    └──requires──> [Score display finalized] (score + zone label must be stable)
    └──requires──> [Color zone definitions] (zones must be locked to generate image)

[Color zone definitions]
    └──requires──> [Score range decisions] (deferred in spec — placeholder zones needed for v1)

[Historical events overlay]
    └──requires──> [Historical trend chart]
    └──requires──> [Event annotation data structure]
    └──requires──> [Editorial curation of event list]

[Email alerts]
    └──requires──> [Real data pipeline] (alerts on mock data are meaningless)
    └──requires──> [Email service integration]

[Zone labels with plain-language meaning] ──enhances──> [Score display (gauge)]
[Factor direction arrows] ──enhances──> [Contributing factors breakdown]
[Open Graph social card] ──enhances──> [Score display (gauge)] (shareability)

[Real-time updates] ──conflicts──> [Static architecture] (requires server)
[User accounts] ──conflicts──> [Zero-cost, zero-server constraint]
[Comment section] ──conflicts──> [Responsible communication goals]
```

### Dependency Notes

- **Score display requires mock data system:** The gauge, chart, and factors breakdown all depend on a well-designed JSON schema. This must be designed first — getting the schema right is the highest-leverage early decision.
- **Social card requires score display + zones:** Cannot generate a meaningful social card until the visual design and zone boundaries are finalized. Low priority for v1; can launch without it.
- **Zone definitions are currently deferred:** The spec intentionally defers color zone thresholds to the modeling phase. For v1 with mock data, use four labeled placeholder zones with even distribution (0-25 / 26-50 / 51-75 / 76-100) and note they are preliminary.
- **Methodology page requires JSON schema:** The methodology page should document the data sources and structure. This can only be written after the schema is defined.

---

## MVP Definition

### Launch With (v1)

Minimum viable product to validate the UX concept and prove the dashboard communicates clearly.

- [ ] **Revolution gauge (needle, 0-100, color zones)** — The product's identity. Without it there is no "Revolution Index."
- [ ] **Current score display with zone label** — Plain-language zone name (e.g., "Elevated") alongside the number.
- [ ] **Historical trend chart** — Line chart with 12 months of mock history. Without trend context, the score is meaningless.
- [ ] **Contributing factors breakdown** — 4-6 factors with name, weight, and value. Users need to understand why.
- [ ] **"Last updated" timestamp** — Trust signal. Must be visible near the gauge.
- [ ] **Disclaimer / framing copy** — Brief, plain-language statement about what the score is and is not. Required for responsible communication on a politically sensitive topic.
- [ ] **About / context section** — One paragraph explaining what this site is for viral traffic arriving from a share.
- [ ] **Methodology page (structure only)** — Page exists with expandable sections, "coming soon" content, and description of the JSON schema. Signals seriousness.
- [ ] **Mock data system (JSON schema)** — Defines the data contract. Required by all other features.
- [ ] **Responsive design** — Mobile layout required for shared-link traffic.
- [ ] **Deployment on Cloudflare Pages** — Must be publicly accessible to validate.

### Add After Validation (v1.x)

Features to add once the dashboard is live and receiving real traffic.

- [ ] **Open Graph social card (OG image with current score)** — Trigger: once the design is stable and we want to encourage sharing. Low build cost once the static site is running.
- [ ] **Factor direction arrows (worsening/improving)** — Trigger: when the mock data is replaced with real data and trend tracking is possible.
- [ ] **Historical events overlay** — Trigger: once real data shows score movements that benefit from event context.
- [ ] **Email interest capture** — Trigger: before building actual alerts, add a simple "notify me when this launches alerts" opt-in. Zero backend required — use a free form service (Formspree, etc.).

### Future Consideration (v2+)

Features to defer until product-market fit is established and real data is running.

- [ ] **Email/push alerts** — Defer: requires real data pipeline, email infrastructure, and user base to justify.
- [ ] **Public API** — Defer: the JSON files in the repo ARE a de-facto public data source. A formal versioned API requires documentation, versioning commitments, and support.
- [ ] **Embeddable widget** — Defer: use static image embed (OG image URL) as the v1 substitute.
- [ ] **Country comparison mode** — Defer: fundamentally changes the product scope and multiplies research/modeling work.

---

## Feature Prioritization Matrix

| Feature | User Value | Implementation Cost | Priority |
|---------|------------|---------------------|----------|
| Revolution gauge (needle + zones) | HIGH | MEDIUM | P1 |
| Current score + zone label | HIGH | LOW | P1 |
| Historical trend chart | HIGH | MEDIUM | P1 |
| Contributing factors breakdown | HIGH | MEDIUM | P1 |
| Mock data JSON schema | HIGH | MEDIUM | P1 |
| Last updated timestamp | HIGH | LOW | P1 |
| Disclaimer / framing copy | HIGH | LOW | P1 |
| About / context section | MEDIUM | LOW | P1 |
| Methodology page (placeholder) | MEDIUM | LOW | P1 |
| Responsive design | HIGH | MEDIUM | P1 |
| Cloudflare Pages deployment | HIGH | LOW | P1 |
| Open Graph social card | MEDIUM | MEDIUM | P2 |
| Factor direction arrows | MEDIUM | LOW | P2 |
| Email interest capture | LOW | LOW | P2 |
| Historical events overlay | MEDIUM | HIGH | P3 |
| Email/push alerts | MEDIUM | HIGH | P3 |
| Public API (formal) | LOW | HIGH | P3 |
| Embeddable widget | LOW | MEDIUM | P3 |
| Country comparison | LOW | HIGH | P3 |

**Priority key:**
- P1: Must have for launch
- P2: Should have, add when possible
- P3: Nice to have, future consideration

---

## Competitor Feature Analysis

| Feature | CNN Fear & Greed | Doomsday Clock | Fragile States Index | Our World in Data | Revolution Index (plan) |
|---------|-----------------|----------------|----------------------|-------------------|-------------------------|
| Primary display | Gauge (0-100) | Clock face / countdown | Score table + map | Line chart | Needle gauge (0-100) — differentiated by real-time feel |
| Color zones | Yes (red/amber/green) | Implicit (proximity to midnight) | Heat map (red gradient) | No | Yes — explicit labeled zones |
| Historical chart | Yes | Yes (timeline of all settings) | Yes (annual reports 2017-2024) | Yes (core feature) | Yes |
| Factor breakdown | Yes (7 sub-indicators) | Yes (thematic statements) | Yes (12 indicators, 4 categories) | Varies by chart | Yes (4-6 factors) |
| Methodology page | Minimal inline | Deep (full statements + FAQs) | Yes (separate section) | Yes (Sources & Processing on every chart) | Yes (placeholder for v1, real content later) |
| Data download | No (walled in CNN) | No | Yes (Excel) | Yes (CSV) | JSON in repo (de-facto download) |
| Embed / widget | No | No | No | Yes (iframe embed code) | Static OG image (v1.x) |
| Public API | No | No | No | Yes (owidapi R package) | Deferred (JSON files are accessible) |
| Social sharing | Yes | Yes | No | Yes (config-aware previews) | Yes via OG meta tags |
| Disclaimer | Yes ("not investment advice") | Yes (extensive framing) | Yes (academic caveats) | Yes (data caveats inline) | Yes — required for responsible communication |
| Update frequency | Hourly | Annual | Annual | Varies (dataset-dependent) | Weekly |
| Mobile responsive | Yes | Yes | Yes | Yes | Yes |
| About / context | Minimal | Deep (full org background) | Yes | Yes | Brief (v1), expandable later |

---

## Domain-Specific Notes

### The Trust Problem Is Central to This Product

Unlike a stock market index, "revolution probability" carries political weight. Users will arrive skeptical — either "this is alarmist" or "this is government-suppressing truth." The product must earn credibility through:
1. Visible methodology (even placeholder)
2. Explicit data sources (even mock)
3. Careful framing language (not a prediction, not advocacy)
4. Transparent update cadence

Every design decision that increases trust is more valuable here than on a finance index.

### Gauge Is the Right Primary Visual — But Needs Animation

Cognitive research on gauge charts confirms users process them faster than bars or numbers because of speedometer familiarity. The needle MUST animate on page load (smooth sweep to current position) — static gauges feel broken. This is the difference between "impressive" and "toy." MEDIUM complexity because D3.js animation requires care, but well-trodden territory.

### Zone Labels Are as Important as the Number

FiveThirtyEight's insight that "67% chance" means different things to different people led them to add named states. Same applies here. A user who sees "63" and then "Elevated Tension" understands the score. A user who only sees "63" may not. Plain-language zone labels are LOW complexity and HIGH value.

### The Score Update Cadence Is a Feature, Not a Bug

Weekly updates seem like a limitation compared to hourly Fear & Greed. Frame it as rigor: "Unlike sentiment indexes that change by the hour, the structural conditions that drive revolution probability change slowly. We update weekly to capture meaningful signal, not noise." This reframes a constraint as a methodology choice.

---

## Sources

- [CNN Fear & Greed Index](https://www.cnn.com/markets/fear-and-greed) — primary UX reference for single-metric public index
- [Doomsday Clock — Bulletin of the Atomic Scientists](https://thebulletin.org/doomsday-clock/) — reference for responsible communication and methodology transparency on a sensitive index
- [Alternative.me Crypto Fear & Greed Index](https://alternative.me/crypto/fear-and-greed-index/) — reference for embed/API features, component weighting display
- [Fragile States Index — Fund for Peace](https://fragilestatesindex.org/) — reference for factor breakdown design and political stability dashboard patterns
- [FiveThirtyEight Methodology](https://fivethirtyeight.com/methodology/) — reference for probability communication design and named state labels
- [Our World in Data — Stability of Democratic Institutions Index](https://ourworldindata.org/grapher/stability-democratic-institutions-index-bti) — reference for embed, download, and citation features on public data charts
- [Corruption Perceptions Index — Transparency International](https://www.transparency.org/en/cpi/2025) — reference for methodology transparency and Creative Commons licensing on sensitive indices
- [DesignRush Dashboard Design Principles 2026](https://www.designrush.com/agency/ui-ux-design/dashboard/trends/dashboard-design-principles) — dashboard UX best practices
- [Gauge Chart Best Practices — Cluster Design](https://clusterdesign.io/gauge-charts-best-practices-and-examples/) — gauge chart UX research
- [Gauge Chart UI Element — UIkits](https://www.uinkits.com/components/gauge-chart-ui-element) — cognitive load analysis for gauge displays

---
*Feature research for: public data index / revolution probability dashboard*
*Researched: 2026-03-01*
