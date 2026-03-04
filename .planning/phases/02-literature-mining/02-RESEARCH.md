# Phase 2: Literature Mining - Research

**Researched:** 2026-03-03
**Domain:** Academic literature review, variable cataloging, framework assessment, dataset identification
**Confidence:** HIGH (core methodology), MEDIUM (specific variable coverage estimates), LOW (completeness of adjacent-field sources)

## Summary

Phase 2 is a pure research/documentation phase -- no code is written, no models are built, no data is downloaded. The task is to systematically mine academic literature across 6 domains (4 core + 2 adjacent), extract every variable that has been empirically linked to revolution, political instability, or democratic breakdown, catalog those variables with evidence ratings, cross-reference them against federal data APIs, identify candidate theoretical frameworks beyond the existing 3 models, locate training/validation datasets, and synthesize the findings into a gap-aware map of variables to frameworks.

The work is LLM-assisted literature review, not traditional systematic review. The LLM (Claude) reads and synthesizes papers it has in training data, supplemented by web searches for recent publications. This is explicitly the project's design (PROJECT.md: "AI-assisted literature mining to identify variables that historically precede revolutions"). The key risk is hallucination -- Claude confidently citing nonexistent papers or misattributing findings. Mitigation: require specific author-year citations, cross-reference key claims via web search, and flag any finding where the source cannot be independently verified.

The academic landscape is well-mapped. Revolution studies have gone through five generations (Korotayev et al. 2025), from early case-study work (Brinton, Skocpol) through structural-demographic theory (Turchin, Goldstone) to recent machine-learning factor-ranking approaches. The key predictive variables cluster into recognizable categories: economic distress (inequality, wages, unemployment), elite dynamics (overproduction, polarization, factionalism), state capacity (fiscal health, institutional quality), demographic pressures (youth bulge, urbanization), social mobilization potential (protest history, organization density), and information ecosystem effects (media polarization, misinformation). Most variables have known measurement approaches and many map directly to FRED, BLS, BEA, or Census data series available through the US Government Open Data MCP.

**Primary recommendation:** Structure the phase as 6 domain-specific literature reviews feeding into a unified variable catalog, framework assessment, dataset inventory, and synthesis document. Use the existing Phase 1 validation report's 7 open questions as entry points into the literature. Cross-reference each variable against the MCP's 37 federal APIs during cataloging, spending no more than 30 seconds per variable on the availability check.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **6 review domains**: 4 core (revolution prediction, democratic backsliding/state failure, historical case studies, economic preconditions) + 2 adjacent (social movement theory, media/information ecosystem studies)
- **Systematic coverage**: ~30-50 sources per domain, covering key papers + important follow-ups and critiques to capture academic consensus
- **US-first lens**: Prioritize literature studying developed democracies and the US specifically; include global studies only when variables are clearly transferable
- **Full historical range**: No time cutoff -- systematically cover from classical works (1960s+) through present, including foundational authors (Turchin, Goldstone, Skocpol, etc.)
- **Hybrid rating system** (quantitative primary + theoretical breadth secondary):
  - **Strong**: Variable has statistically significant coefficients in 2+ independent quantitative studies
  - **Moderate**: Variable appears in 1 quantitative model OR has strong qualitative consensus across 3+ studies
  - **Weak**: Theoretically motivated but limited testing, or single qualitative mention
- **Conflict handling**: Rate based on weight of evidence but flag disagreements explicitly with a 'contested' marker
- **Measurability filter**: Only catalog variables that have at least one known measurement approach or proxy
- **Proxy capture**: Each variable entry lists the specific measurement/proxy used in each citing study
- **Early availability check**: Cross-reference against US Government Open Data MCP's available data sources during cataloging
- **Classification during cataloging**: Each variable gets a tag: `fed-data` / `other-data` / `unknown`
- **Not a gate**: Data availability does NOT filter variables out -- the measurability filter handles unmeasurable variables
- **MCP as discovery tool**: Use it to spot-check whether a variable has a directly queryable federal data source
- **Scope limitation**: Quick cross-reference (~30 seconds per variable), not exhaustive data sourcing
- **Framework evaluation primary criterion: data availability** -- can the model's required inputs actually be measured for the US?
- **Independent evaluation**: Assess each framework on its own merits, not compared against existing 3 models
- **Surface all viable candidates**: No artificial cap on number of frameworks
- **Detailed assessment per framework**: Full writeup including theoretical basis, required inputs, known limitations, validation track record, and data availability assessment
- **Separate documents**: Individual files for each deliverable
- **Variable catalog format**: Hybrid -- summary table at top + detailed entries below
- **Citation style**: Author-year inline with full bibliography at end of each document

### Claude's Discretion
- Adjacent field selection (social movement theory and media/information ecosystem studies) -- already decided
- Hybrid evidence rating system -- already decided
- Separate documents format -- already decided
- Hybrid catalog format -- already decided
- Data availability cross-referencing approach -- already decided

### Deferred Ideas (OUT OF SCOPE)
None -- discussion stayed within phase scope
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| LIT-01 | Conduct exhaustive LLM-assisted review of revolution prediction literature across political science, economics, sociology, and conflict studies | Research identifies the 5 generations of revolution studies (Korotayev et al. 2025), key authors (Turchin, Goldstone, Skocpol, Brinton, Davies, Gurr), core variables (elite overproduction, fiscal distress, relative deprivation, demographic pressure), and the PITF quantitative forecasting tradition. The LLM-assisted methodology is well-supported by recent systematic reviews (JAMIA 2025) showing GPT-based models achieve 83% precision in data extraction from academic literature. Domain should yield 30-50 sources covering structural-demographic theory, quantitative forecasting models, and revolution typologies. |
| LIT-02 | Conduct exhaustive LLM-assisted review of democratic backsliding and state failure literature | Research identifies key frameworks: V-Dem indicators (483 indicators, liberal democracy index), Goldstone's PITF model (regime type, infant mortality, ethnic discrimination, neighborhood effects), Fragile States Index (12 indicators, 0-10 scale), Grumbach's US state-level backsliding work, and recent Kaufman/IGCC research on democratic resilience. Domain includes measurable variables: judicial independence, partisan control, polarization levels, factionalism. |
| LIT-03 | Conduct exhaustive LLM-assisted review of historical revolution case studies and precondition analysis | Research identifies Skocpol's structural approach (state crisis, elite division, peasant revolt), Goldstone's demographic-structural model (population growth -> state breakdown), Brinton's revolution anatomy, and recent case studies applying SDT to industrialized societies (Georgescu 2023, Chilean social outburst 2024). Key variables: fiscal crisis, elite fragmentation, loss of state legitimacy, military loyalty shifts. |
| LIT-04 | Produce a ranked variable catalog with evidence strength ratings, source papers, and theoretical justification | Research establishes the hybrid rating system (Strong/Moderate/Weak with contested marker), the measurability filter, proxy capture requirement, and data availability tagging. The catalog format (summary table + detailed entries) is locked. Research identifies ~40-60 candidate variables across the 6 domains that will need rating. COINr package methodology provides a reference for composite indicator variable selection best practices. |
| LIT-05 | Identify candidate models/frameworks from literature that may supplement or replace the existing 3 models | Research identifies at least 8 candidate frameworks beyond the existing 3: PITF global forecasting model, Fragile States Index, Collier-Hoeffler greed/grievance model, V-Dem Episodes of Regime Transformation, Korotayev-Medvedev ML factor ranking, Funke-Schularick-Trebesch financial crisis -> political extremism model, Chenoweth civil resistance model, and the Georgescu SDT-for-industrialized-societies operationalization. Each needs assessment against the primary criterion of data availability for the US. |
| LIT-06 | Identify candidate training/validation datasets for model evaluation | Research identifies 7+ candidate datasets: NAVCO 2.1 (389 campaigns, 1945-2013), NAVCO 3.0 (100K+ events, 21 countries, 1991-2012), Mass Mobilization Project (162 countries, 1990-2020, 10K+ events), UCDP (global conflict events, 25-death threshold), ACLED (political violence, no fatality threshold), V-Dem (483 indicators, 1900-present, 202 countries), PITF Worldwide Atrocities Dataset, and the new OMG dataset (1789-2019). Coverage, access methods, and US-applicability need documentation. |
| LIT-07 | Produce a synthesis document mapping variables to frameworks and identifying gaps | Research establishes the mapping structure: variables discovered across 6 domains mapped to theoretical frameworks, with explicit gap identification where theory suggests a variable matters but no measurement approach is obvious. The synthesis must also incorporate the Phase 1 validation report's 7 open questions as gap-awareness inputs. |
</phase_requirements>

## Standard Stack

This phase is documentation-only. No libraries or code are involved. The "stack" is the set of research tools, academic sources, and data verification methods.

### Core Research Tools

| Tool | Purpose | When to Use |
|------|---------|-------------|
| Claude's training data | Primary source for academic paper content, author-year citations, variable extraction | All 6 domain reviews (LIT-01 through LIT-03) |
| WebSearch | Verify specific claims, find recent publications (2024-2025), confirm paper existence | Cross-verification of every key finding |
| US Gov Open Data MCP | Cross-reference variables against federal data APIs (FRED, BLS, BEA, Census, etc.) | During variable cataloging (LIT-04) -- 30-second spot-checks |
| Phase 1 validation report | Context on existing 3 models, their variables, known issues, and open questions | Framework assessment (LIT-05), synthesis (LIT-07) |

### Federal Data APIs Available via MCP (37 APIs)

| API Category | Key APIs | Variable Types Covered |
|--------------|----------|----------------------|
| Economic | FRED (840K+ series), BEA (GDP, personal income), BLS (employment, wages, CPI, PPI, JOLTS) | Income, wages, unemployment, inflation, GDP, productivity |
| Financial | Treasury Fiscal Data (53 datasets, 181 endpoints), FDIC (bank data) | Government debt, fiscal health, banking stability |
| Demographic | Census (ACS, Decennial, PEP), CDC (mortality, life expectancy, health) | Population, age structure, health outcomes, mortality |
| Social/Governance | FBI (crime data), FEC (campaign finance), SEC (corporate filings) | Crime rates, political finance, corporate concentration |
| Housing/Welfare | HUD (fair market rents, income limits), CMS (healthcare), CFPB (consumer complaints) | Housing affordability, healthcare access, consumer financial stress |
| Environmental/Energy | EPA (air quality), EIA (energy data), NOAA (climate), NREL (renewable energy) | Energy prices, environmental stress |
| Education | NAEP (education achievement), College Scorecard | Educational attainment, mobility |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| LLM-assisted review | Traditional systematic review with database searches | Traditional is more rigorous but impractical at this scale without a research team; LLM approach covers more ground faster with known hallucination risk |
| Author-year citation style | Numbered references | Author-year is more readable and easier to verify; numbered references save space but lose context |
| Separate document per deliverable | Single monolithic document | Separate files enable downstream phases to reference exactly what they need without parsing irrelevant material; locked decision |
| Manual FRED website checks for data availability | MCP API spot-checks | MCP is faster and can be done inline during cataloging; FRED website provides more context (discontinuation notices, methodology notes) but takes longer |

## Architecture Patterns

### Recommended Output Structure

```
.planning/phases/02-literature-mining/
    02-CONTEXT.md                    # User decisions (exists)
    02-RESEARCH.md                   # This file
    02-01-PLAN.md through 02-NN-PLAN.md  # Execution plans

literature/
    01-revolution-prediction.md      # Domain 1: Revolution prediction literature
    02-democratic-backsliding.md     # Domain 2: Democratic backsliding & state failure
    03-historical-case-studies.md    # Domain 3: Historical revolution case studies
    04-economic-preconditions.md     # Domain 4: Economic preconditions
    05-social-movement-theory.md     # Domain 5: Social movement theory (adjacent)
    06-media-information.md          # Domain 6: Media/information ecosystem (adjacent)
    variable-catalog.md              # Ranked variable catalog (LIT-04)
    framework-assessment.md          # Candidate frameworks beyond existing 3 (LIT-05)
    dataset-inventory.md             # Training/validation datasets (LIT-06)
    synthesis.md                     # Variable-to-framework mapping + gaps (LIT-07)
```

### Pattern 1: Domain Literature Review Document

**What:** A structured review of academic literature within one of the 6 domains.
**When to use:** For each of the 6 domain reviews (part of LIT-01, LIT-02, LIT-03).

**Structure:**
```markdown
# Literature Review: [Domain Name]

## Scope
[What this domain covers, boundaries with other domains]

## Foundational Works
[Classical/seminal papers that defined the field, pre-2000]

## Core Empirical Studies
[Quantitative studies with testable variables and results]

## Recent Developments (2020-2025)
[Latest research, methodological advances, new variables]

## Variables Discovered
| Variable | Measurement/Proxy | Studies | Direction | Notes |
[Table of every variable found in this domain with citations]

## Key Debates and Contested Findings
[Where scholars disagree, contradictory evidence]

## US Applicability Assessment
[Which findings transfer to the US context, which don't, and why]

## Bibliography
[Full author-year references for all cited works]
```

### Pattern 2: Variable Catalog Entry

**What:** A standardized entry for each variable in the ranked catalog.
**When to use:** For LIT-04.

**Structure:**
```markdown
### [Variable Name]

**Rating:** Strong / Moderate / Weak [+ Contested if applicable]
**Domain(s):** [Which of the 6 domains this variable appears in]
**Data Availability:** `fed-data` / `other-data` / `unknown`

**Definition:** [What this variable measures]

**Evidence:**
| Study | Proxy Used | Finding | Type |
|-------|-----------|---------|------|
| Author (Year) | [specific measurement] | [direction/magnitude] | quant/qual |

**Measurement Approaches:**
- [Proxy 1]: [description, source]
- [Proxy 2]: [description, source]

**Federal Data Sources (if fed-data):**
- [API]: [series/endpoint], [frequency], [coverage]

**Theoretical Role:** [How this variable fits into causal theories of instability]
```

### Pattern 3: Framework Assessment Entry

**What:** A standardized assessment of a candidate theoretical framework.
**When to use:** For LIT-05.

**Structure:**
```markdown
### [Framework Name] ([Author(s)], [Year])

**Theoretical Basis:** [Core theory in 2-3 sentences]
**Required Inputs:** [List of variables the framework needs]
**Known Limitations:** [Documented weaknesses, criticisms]
**Validation Track Record:** [Where has it been tested? Results?]
**Data Availability for US:** [Can the required inputs be measured with available data?]
**Assessment:** [Overall viability for this project]
```

### Anti-Patterns to Avoid

- **Fabricating citations:** The most dangerous anti-pattern. Never cite a paper unless you can provide author, year, and a plausible journal/venue. Flag uncertain citations with "[VERIFY]". Better to cite fewer papers accurately than many papers unreliably.
- **Treating all variables as equally important:** The rating system exists for a reason. A variable that appears in one theoretical paper is fundamentally different from one with statistically significant coefficients in 5 independent studies.
- **Ignoring the US-first lens:** Global conflict studies (Collier-Hoeffler, PITF) focus on developing countries. Variables like "natural resource dependence" or "infant mortality rate" may be powerful global predictors but irrelevant or non-discriminating for the US. Every variable must be assessed for US applicability.
- **Scope creep into data sourcing:** Phase 2 tags variables with `fed-data`/`other-data`/`unknown`. It does NOT build data pipelines, download data, or verify API endpoints. That is Phase 3.
- **Treating the literature review as a textbook:** The goal is variable extraction and framework assessment, not comprehensive intellectual history. Summarize theories only enough to justify why specific variables matter.
- **Conflating revolution with protest:** The literature distinguishes between protest (common, mostly harmless), sustained campaigns (NAVCO-scale mobilization), democratic backsliding (institutional erosion), and revolution (regime change). Variables predict different things on this spectrum. Be precise about what each variable predicts.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Citation verification | Manual web searches for every paper | Targeted verification of key/surprising claims only | 200+ papers across 6 domains; verify the 20% that matter most |
| Data availability checking | FRED website manual lookups | US Gov Open Data MCP `fred_search` and `fred_series_info` | MCP provides programmatic access; 30-second spot-checks during cataloging |
| Variable deduplication | Manual cross-referencing | Domain-aware naming convention + synthesis document | Same concept appears under different names across domains (e.g., "relative deprivation" vs. "perceived loss" vs. "economic grievance") |
| Evidence rating | Pure judgment calls | Hybrid rating system with explicit criteria | The locked rating system (Strong/Moderate/Weak) provides reproducible ratings |
| Framework comparison | Side-by-side matrix | Independent assessment per framework | Locked decision: evaluate each on its own merits, not relative to each other |

**Key insight:** This phase produces knowledge artifacts, not code. The temptation will be to "quickly check" a data source or "prototype" a model. Resist. The deliverables are documents that enable downstream phases to make informed decisions.

## Common Pitfalls

### Pitfall 1: Hallucinated Citations
**What goes wrong:** Claude generates plausible-sounding but nonexistent paper citations (e.g., "Smith & Jones 2019, Journal of Political Risk, found that..."). The paper does not exist.
**Why it happens:** LLMs generate text that pattern-matches academic citation style. Training data includes millions of citations, and the model can recombine them into novel, false citations.
**How to avoid:** For every Strong-rated variable, verify at least one key citation via WebSearch. Flag any citation that cannot be independently confirmed with "[UNVERIFIED]". Prefer well-known, frequently-cited works (Turchin 2003, Goldstone 2010, Chenoweth & Stephan 2011) over obscure papers.
**Warning signs:** Very specific page numbers, unusually recent dates for classic findings, journals with generic names, authors who don't appear in web searches.

### Pitfall 2: Western Democracy Blindness
**What goes wrong:** Including variables from global conflict studies (civil war onset, ethnic fractionalization, natural resource dependence) that are statistically powerful for developing countries but irrelevant or non-discriminating for the US.
**Why it happens:** Most quantitative political instability research focuses on cross-national samples dominated by developing countries. The US is an extreme outlier on most of these variables.
**How to avoid:** Apply the US-first lens rigorously. For each variable, ask: "Does this variable vary meaningfully within the US over time? If it's been essentially constant (e.g., ethnic fractionalization has been stable), it cannot predict instability timing."
**Warning signs:** Variables where the US sits at the floor or ceiling of the global distribution, variables that only predict onset in countries below some GDP threshold.

### Pitfall 3: Variable Proliferation Without Discrimination
**What goes wrong:** The catalog balloons to 100+ variables, most rated "Moderate" or "Weak," making it useless for downstream model selection.
**Why it happens:** Every paper mentions dozens of control variables and theoretical constructs. It's easy to catalog everything without discriminating.
**How to avoid:** The measurability filter is the first gate -- if there's no known measurement approach, exclude. The rating system is the second gate -- be honest about what's Strong vs. Weak. Aim for 40-60 cataloged variables, not 100+.
**Warning signs:** More than 70 variables in the catalog, more than 50% rated "Weak," variables that are really sub-indicators of the same concept.

### Pitfall 4: Confusing Frameworks with Variables
**What goes wrong:** Cataloging "Structural-Demographic Theory" as a variable instead of a framework, or treating "PITF Model" as a single variable instead of a model that uses specific variables.
**Why it happens:** The boundary between "framework" and "variable" blurs in interdisciplinary review.
**How to avoid:** Frameworks go in LIT-05 (framework-assessment.md). Variables go in LIT-04 (variable-catalog.md). A framework is a theory about how variables interact to produce outcomes. A variable is a measurable quantity. "Elite overproduction" is a variable. "Structural-demographic theory" is a framework that says elite overproduction + mass immiseration + fiscal distress = instability.
**Warning signs:** Catalog entries that describe relationships between concepts rather than measurable quantities.

### Pitfall 5: Ignoring Phase 1 Open Questions
**What goes wrong:** The literature review proceeds without addressing the 7 specific open questions from the validation report, leaving Phase 4 with the same gaps.
**Why it happens:** The open questions are in a separate document and easy to forget when deep in literature review.
**How to avoid:** Use the 7 open questions as explicit entry points into the literature. Each question should have a corresponding finding in the relevant domain review or synthesis document.
**Warning signs:** The synthesis document (LIT-07) doesn't reference the validation report's open questions.

### Pitfall 6: Data Availability Cross-Referencing Becomes Data Sourcing
**What goes wrong:** The 30-second spot-check balloons into full data pipeline design, API endpoint documentation, and series verification -- which is Phase 3 work.
**Why it happens:** The MCP makes it easy to query federal APIs, and once you start exploring, it's tempting to go deep.
**How to avoid:** Strict 30-second time box per variable. The check is: "Does FRED/BLS/BEA/Census have something that could measure this?" Tag it `fed-data` and move on. Don't retrieve actual data, don't document series IDs, don't verify update frequencies. That's Phase 3.
**Warning signs:** Variable catalog entries with FRED series IDs, API endpoints, or data frequency details.

## Code Examples

Not applicable -- this phase produces documentation, not code. The only "code" involved is MCP tool calls for data availability spot-checks.

### MCP Spot-Check Pattern

For a variable like "unemployment rate," the spot-check looks like:
1. Call `mcp__us-gov-open-data__fred_search` with query "unemployment rate"
2. If results come back, tag as `fed-data`
3. Move on -- no further investigation

For a variable like "elite overproduction," the spot-check looks like:
1. Call `mcp__us-gov-open-data__fred_search` with query "advanced degree holders" or "graduate degrees"
2. If no results, try `mcp__us-gov-open-data__census_search_variables` with keyword "education"
3. If still unclear, tag as `unknown`
4. Move on

## State of the Art

### Revolution Studies: Five Generations

The academic study of revolutions has evolved through five generations (Korotayev, Ustyuzhanin, Grinin, Fain 2025):

| Generation | Era | Approach | Key Authors | Variables Emphasized |
|-----------|-----|----------|-------------|---------------------|
| 1st | 1920s-1940s | Natural history of revolutions | Brinton, Edwards, Pettee | Stages/phases of revolution (descriptive) |
| 2nd | 1950s-1960s | Behavioral/psychological | Davies, Gurr | Relative deprivation, J-curve, frustration-aggression |
| 3rd | 1970s-1990s | Structural | Skocpol, Goldstone, Wickham-Crowley | State crisis, elite division, fiscal distress, demographic pressure |
| 4th | 2000s-2010s | Mixed methods, cliodynamics | Turchin, Chenoweth, Beissinger | Structural-demographic cycles, nonviolent resistance, diffusion |
| 5th | 2020s | Computational, ML-assisted | Korotayev, Medvedev, Zhdanov | Factor ranking via ML, multi-variable prediction models |

### Key Quantitative Models and Their Variables

| Model | Authors | Key Variables | Validation | US Applicable? |
|-------|---------|---------------|------------|----------------|
| PITF Global Forecasting | Goldstone et al. 2010 | Regime type (5 categories), infant mortality, ethnic discrimination, neighborhood conflict | 80%+ accuracy, 1955-2003, 2-year lead | Partially -- regime type is key; infant mortality non-discriminating for US |
| Structural-Demographic PSI | Turchin 2003, 2010, 2023 | MMP (relative wages, urbanization, youth bulge), EMP (elite numbers, elite income), SFD (debt/GDP, deficit, trust) | Retrospective for US 1780-2020; Georgescu 2023 tested for industrialized societies | Yes -- designed for US; simplified proxies already in codebase |
| Collier-Hoeffler | Collier & Hoeffler 2004 | Primary commodities, per capita income, economic growth, diaspora, ethnic fractionalization | Cross-national, developing countries | Limited -- "greed" variables (resource dependence) not relevant for US |
| Funke-Schularick-Trebesch | Funke et al. 2016 | Systemic financial crisis onset, vote share changes, government majority, polarization | 20 advanced economies, 800+ elections, 1870-2014 | Yes -- includes advanced democracies; financial crisis -> political extremism pathway |
| Fragile States Index | Fund for Peace | 12 indicators across cohesion, economic, political, social, cross-cutting | Annual, 178 countries since 2006 | Limited -- US consistently near bottom (most stable); useful methodology reference |
| V-Dem ERT | V-Dem Institute | 483 indicators, liberal democracy index, episodes of autocratization/democratization | 202 countries, 1900-present | Yes -- includes detailed US coding; recent episodes identified |
| Chenoweth Civil Resistance | Chenoweth & Stephan 2011 | Participation size/diversity, security force loyalty shifts, nonviolent discipline | 323 campaigns, 1900-2006 | Partially -- framework useful, but coded at campaign level not country-year |

### Normalization State of the Art

The Phase 1 validation report flagged the normalization problem for trending macroeconomic series (PSI min-max pinning). Here is how established indices handle this:

| Index | Normalization Method | Trending Series Handling |
|-------|---------------------|------------------------|
| Fragile States Index | 0-10 expert-scaled, quantitative data normalized | Trends measured as rate-of-change against own history |
| V-Dem | Bayesian item response theory (IRT) | Designed for ordinal expert ratings, handles time-series via measurement model |
| PITF | Categorical coding (regime type in 5 bins) | Avoids continuous normalization entirely for key predictor |
| FRED-based indices (STLFSI) | Rolling z-scores | Standard in financial stress indices; handles trends via rolling window |
| COINr composite indicators | Multiple methods: z-score, min-max, rank, percentile, distance to frontier | Recommends rank/percentile for skewed or trending series; supports global sensitivity analysis |

**Recommendation for the project:** Rolling z-scores (as already used by FSP) or percentile ranks (as exists in normalization.py but unused by PSI) are standard approaches for trending macroeconomic series. Min-max on raw values is known to be problematic. This is consistent with Phase 1 findings.

### LLM-Assisted Literature Review: State of the Art

A 2025 systematic review in the Journal of the American Medical Informatics Association examined LLM use in literature reviews:

| Capability | LLM Performance | Best Practices |
|------------|----------------|----------------|
| Literature searching | 41% of studies used LLMs for this | Supplement with traditional database searches |
| Study selection/screening | 38% of studies | Clear inclusion/exclusion criteria essential |
| Data extraction | 30% of studies; 83% precision, 86% recall for GPT-based models | Lower accuracy for numeric data; human oversight required |
| Overall | GPT-based models dominant (89% of studies) | Clear protocols, refined criteria, human oversight for quality |

**Implication for this project:** LLM-assisted review is a legitimate and increasingly common methodology. The key risk is hallucination, not capability. Mitigation through targeted verification of key claims is standard practice.

## Open Questions

1. **How many variables will survive the measurability filter?**
   - What we know: Initial estimates suggest 40-60 variables across 6 domains will have known measurement approaches. Variables like "revolutionary consciousness" or "elite legitimacy beliefs" are theoretically important but unmeasurable without surveys.
   - What's unclear: The exact count won't be known until the review is complete.
   - Recommendation: Proceed with the review; the measurability filter is a during-cataloging decision, not a pre-screening gate.

2. **Will the 30-50 sources per domain target be achievable with LLM-assisted review?**
   - What we know: For core domains (revolution prediction, economic preconditions), Claude's training data likely contains sufficient material. For adjacent domains (media/information ecosystem), coverage may be thinner, especially for post-2024 work.
   - What's unclear: Whether the effective source count will hit 30 per domain or fall short in adjacent fields.
   - Recommendation: Set 30 as a minimum target for core domains and 20 as a realistic floor for adjacent domains. Supplement with WebSearch for recent publications.

3. **How to handle the "US applicability" assessment consistently?**
   - What we know: The US is a massive outlier in most cross-national instability datasets. Variables that predict civil war onset globally (infant mortality, ethnic fractionalization) may be irrelevant for the US.
   - What's unclear: Where to draw the line between "not applicable" and "applicable but with different dynamics."
   - Recommendation: Use a three-tier assessment: (a) directly applicable (variable varies meaningfully over US history), (b) applicable with adaptation (concept transfers but measurement needs US-specific proxy), (c) not applicable (US is at floor/ceiling, no variation). Only categories (a) and (b) enter the catalog.

4. **Will candidate datasets (NAVCO, PITF, etc.) actually be usable for US-focused model validation?**
   - What we know: Most political instability datasets code events globally. The US typically has few or zero coded instability events, making traditional training/validation impossible for a US-specific model.
   - What's unclear: Whether these datasets can be used indirectly (e.g., using cross-national patterns to calibrate thresholds that are then applied to US data).
   - Recommendation: Document each dataset's US coverage honestly. The zero-event-for-US problem is a known constraint (REQUIREMENTS.md explicitly excludes "ML prediction framing" for this reason). Datasets may be more useful for framework validation than direct model training.

5. **How to handle the 7 open questions from Phase 1?**
   - What we know: The validation report raises 7 specific questions (Turchin's latest PSI operationalization, prospect theory in political risk, financial stress -> mobilization evidence, alternative data sources, normalization methods, frameworks beyond the 3 models, sensitivity analysis methods).
   - What's unclear: Whether all 7 will be answerable from the literature alone, or whether some require empirical investigation in later phases.
   - Recommendation: Address each question explicitly in the relevant domain review or synthesis document. Some (normalization methods, frameworks beyond the 3) can be definitively answered. Others (Turchin's latest operationalization, prospect theory validation) may require flagging for Phase 4 empirical testing.

6. **What is the right granularity for variable catalog entries?**
   - What we know: "Income inequality" could be one variable or ten (Gini coefficient, top 1% share, top 10% share, Palma ratio, labor share of GDP, wealth Gini, etc.).
   - What's unclear: Whether to catalog at the concept level (income inequality) or the measurement level (Gini coefficient, top 1% share).
   - Recommendation: Catalog at the concept level with measurement/proxy sub-entries. "Income inequality" is one catalog entry with multiple proxy rows (Gini, top 1%, labor share, etc.). This avoids proliferation while preserving measurement detail.

## Addressing Phase 1 Open Questions

The validation report (Section 5) raised 7 questions for Phase 2. Here is how the literature review should address each:

| # | Question | Relevant Domain(s) | Expected Answer Source |
|---|----------|-------------------|----------------------|
| 1 | Updated Turchin PSI operationalizations since *End Times* (2023)? | Revolution prediction | Georgescu (2023) PLoS ONE tested SDT for industrialized societies; Turchin's blog and Cliodynamics journal for latest working papers |
| 2 | Other applications of prospect theory to aggregate political risk? | Economic preconditions | Passarelli & Del Ponte (Oxford Research Encyclopedia 2020) survey prospect theory in political behavior; Vis (2011) on policy-making under prospect theory |
| 3 | Evidence for financial stress -> political mobilization transmission? | Economic preconditions, Historical case studies | Funke, Schularick & Trebesch (2016) provide the strongest evidence: 20 countries, 800+ elections, 1870-2014. Also Mian, Sufi & Trebbi (2014) on financial crises and political polarization |
| 4 | Alternative data sources for discontinued/unavailable series? | Cross-cutting (data availability tags) | MCP cross-referencing during cataloging; OECD KSTEI replacement for CSCICP03USM665S flagged for Phase 3 |
| 5 | Normalization methods for trending macroeconomic series? | Cross-cutting (methodology) | COINr documentation, FSI methodology, financial stress index literature all converge on z-scores or percentile ranks for trending series |
| 6 | Frameworks beyond the existing 3 models? | All 6 domains feed into LIT-05 | At least 8 candidate frameworks identified in this research (see State of the Art section) |
| 7 | Sensitivity analysis methods for composite indicators? | Cross-cutting (methodology) | COINr package provides variance-based global sensitivity analysis; Saltelli (2004) is the standard reference; two-stage approach (Morris screening + Sobol indices) recommended for 50+ parameter models |

## MCP Federal API Coverage Map

For the data availability cross-referencing task, here is a mapping of common instability-related variable categories to available MCP APIs:

| Variable Category | MCP API(s) | Example Variables | Expected Tag |
|-------------------|-----------|-------------------|-------------|
| Labor market | FRED, BLS | Unemployment rate, wages, labor force participation, JOLTS | `fed-data` |
| Income/inequality | FRED, Census ACS, BEA | Median household income, Gini, income by quintile | `fed-data` (partial) |
| Fiscal/government | FRED, Treasury Fiscal Data | Debt/GDP, deficit, interest payments, tax revenue | `fed-data` |
| Financial stress | FRED | STLFSI, VIX, yield curve, credit spreads, delinquency | `fed-data` |
| Housing | FRED, HUD, Census | Housing affordability, homeownership, rent burden | `fed-data` |
| Health/mortality | CDC, FRED | Life expectancy, mortality rates, health insurance | `fed-data` |
| Crime/safety | FBI | Violent crime rate, property crime | `fed-data` |
| Education | NAEP, Census, College Scorecard | Educational attainment, test scores, degree holders | `fed-data` |
| Demographic | Census | Age structure, urbanization, population growth | `fed-data` |
| Political finance | FEC | Campaign contributions, spending, donor concentration | `fed-data` |
| Elite dynamics | WID, FRED (partial) | Top 1% share, wealth concentration | `other-data` (WID) |
| Political polarization | V-Dem, Pew | Polarization scores, partisan antipathy | `other-data` |
| Government trust | Gallup, Pew | Trust in government, institutional confidence | `other-data` |
| Social mobilization | ACLED, MM Project | Protest frequency, participation, demands | `other-data` |
| Media/information | Pew, academic datasets | Media polarization, misinformation exposure | `other-data` / `unknown` |
| Regime type | V-Dem, Polity | Democracy indices, institutional quality | `other-data` |

## Sources

### Primary (HIGH confidence)
- Phase 1 validation report (`validation/validation-report.md`) -- direct inspection, all 7 open questions documented
- Phase 1 research (`01-RESEARCH.md`) -- direct inspection, model details and data series documented
- CONTEXT.md -- direct inspection, all locked decisions and discretion areas documented
- REQUIREMENTS.md -- direct inspection, LIT-01 through LIT-07 requirements documented

### Secondary (MEDIUM confidence)
- [Korotayev et al. 2025 -- Fifth Generation of Revolution Studies](https://journals.sagepub.com/doi/abs/10.1177/08969205241300595) -- systematic review of revolution causes, forms, and waves
- [Goldstone et al. 2010 -- PITF Global Forecasting Model](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-5907.2009.00426.x) -- regime type, infant mortality, ethnic discrimination, neighborhood effects; 80%+ accuracy
- [Georgescu 2023 -- SDT Revisited for Industrialized Societies](https://pmc.ncbi.nlm.nih.gov/articles/PMC10621949/) -- empirical test of Turchin's predictions for industrialized societies
- [Turchin 2020 -- SDT Retrospective Assessment](https://pmc.ncbi.nlm.nih.gov/articles/PMC7430736/) -- validation of 2010 forecast for 2010-2020 decade
- [Funke, Schularick & Trebesch 2016 -- Going to Extremes](https://www.sciencedirect.com/science/article/abs/pii/S0014292116300587) -- financial crises -> far-right vote share increase; 20 countries, 1870-2014
- [Chenoweth & Stephan 2011 -- Why Civil Resistance Works](https://www.ericachenoweth.com/research/wcrw) -- 323 campaigns, 160 variables, nonviolent campaigns 2x more effective
- [Collier & Hoeffler 2004 -- Greed and Grievance](https://academic.oup.com/oep/article-abstract/56/4/563/2361902) -- economic opportunity > grievance as conflict predictor
- [NAVCO Data Project](https://dataverse.harvard.edu/dataverse/navco) -- 389 campaigns (NAVCO 2.1), 1945-2013
- [Mass Mobilization Project](https://massmobilization.github.io/about.html) -- 162 countries, 1990-2020, 10K+ events
- [V-Dem Dataset](https://v-dem.net/data/the-v-dem-dataset/) -- 483 indicators, 202 countries, 1900-present
- [UCDP](https://ucdp.uu.se/downloads/) -- global conflict events, systematic data
- [Fragile States Index Methodology](https://fragilestatesindex.org/methodology/) -- 12 indicators, 0-10 scale, normalization methodology
- [COINr R Package -- Composite Indicator Development](https://bluefoxr.github.io/COINr/) -- normalization, aggregation, global sensitivity analysis for composite indicators
- [COINr Sensitivity Analysis](https://bluefoxr.github.io/COINrDoc/sensitivity-analysis.html) -- variance-based (global) sensitivity analysis for composite indicators
- [Passarelli & Del Ponte -- Prospect Theory and Political Behavior](https://oxfordre.com/politics/display/10.1093/acrefore/9780190228637.001.0001/acrefore-9780190228637-e-947) -- loss aversion in voting, status quo bias
- [JAMIA 2025 -- LLM-Assisted Systematic Review](https://academic.oup.com/jamia/article/32/6/1071/8126534) -- GPT performance in literature reviews: 83% precision, 86% recall
- [Our World in Data -- Political Polarization Score](https://ourworldindata.org/grapher/political-polarization-score) -- expert-estimated polarization across countries
- [Grumbach -- Laboratories of Democratic Backsliding](https://ideas.repec.org/a/cup/apsrev/v117y2023i3p967-984_13.html) -- US state-level backsliding, partisan control as predictor

### Tertiary (LOW confidence)
- Turchin *End Times* (2023) -- referenced for updated PSI narrative but book content not directly verified; need to check if new operationalizations are included vs. just a popular science treatment
- Korotayev & Medvedev ML factor ranking work -- referenced from HSE news article, not from the original paper; specific variables and rankings need verification
- Media polarization measurement approaches -- multiple fragmentary sources; no single authoritative reference for US-specific quantitative measurement
- OMG Dataset (Dahl et al. 2025) -- recently announced (1789-2019 coverage), access and documentation not yet verified
- Chilean SDT application (PLoS ONE 2024) -- cited in search results but content not directly verified

## Metadata

**Confidence breakdown:**
- Literature domain mapping: HIGH -- the 5 generations of revolution studies are well-documented; key authors and frameworks are canonical
- Variable identification: MEDIUM -- initial variable landscape is clear but completeness depends on depth of each domain review during execution
- Framework assessment candidates: HIGH -- at least 8 frameworks identified with published validation studies
- Dataset identification: HIGH -- NAVCO, UCDP, V-Dem, ACLED, Mass Mobilization Project are all well-documented and accessible
- Data availability cross-referencing approach: HIGH -- MCP provides 37 federal APIs; the spot-check methodology is simple and well-scoped
- Normalization and methodology: HIGH -- COINr, FSI, and financial stress index literature converge on z-scores/percentile ranks
- LLM-assisted review methodology risks: MEDIUM -- hallucination risk is real but mitigatable with targeted verification

**Research date:** 2026-03-03
**Valid until:** 2026-04-03 (30 days) -- academic literature moves slowly; the main expiration risk is new 2025-2026 publications in adjacent fields
