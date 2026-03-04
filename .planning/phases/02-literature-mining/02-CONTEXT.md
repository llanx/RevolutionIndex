# Phase 2: Literature Mining - Context

**Gathered:** 2026-03-02
**Status:** Ready for planning

<domain>
## Phase Boundary

Produce a comprehensive, evidence-ranked catalog of variables that predict revolution/instability, along with candidate theoretical frameworks — so model selection is driven by the full weight of academic evidence rather than three pre-chosen models. This phase covers literature review, variable cataloging, framework assessment, dataset identification, and synthesis. It does NOT cover data acquisition, model implementation, or model selection.

</domain>

<decisions>
## Implementation Decisions

### Review scope & depth
- **6 review domains**: 4 core (revolution prediction, democratic backsliding/state failure, historical case studies, economic preconditions) + 2 adjacent (social movement theory, media/information ecosystem studies)
- **Systematic coverage**: ~30-50 sources per domain, covering key papers + important follow-ups and critiques to capture academic consensus
- **US-first lens**: Prioritize literature studying developed democracies and the US specifically; include global studies only when variables are clearly transferable
- **Full historical range**: No time cutoff — systematically cover from classical works (1960s+) through present, including foundational authors (Turchin, Goldstone, Skocpol, etc.)

### Variable rating criteria
- **Hybrid rating system** (quantitative primary + theoretical breadth secondary):
  - **Strong**: Variable has statistically significant coefficients in 2+ independent quantitative studies
  - **Moderate**: Variable appears in 1 quantitative model OR has strong qualitative consensus across 3+ studies
  - **Weak**: Theoretically motivated but limited testing, or single qualitative mention
- **Conflict handling**: Rate based on weight of evidence but flag disagreements explicitly with a 'contested' marker so downstream phases know to investigate
- **Measurability filter**: Only catalog variables that have at least one known measurement approach or proxy — theoretically important but unmeasurable variables are excluded
- **Proxy capture**: Each variable entry lists the specific measurement/proxy used in each citing study (e.g., 'Gini coefficient' for inequality, 'V-Dem liberal democracy index' for democratic quality)

### Data availability cross-referencing
- **Early availability check**: When cataloging each variable, cross-reference against the US Government Open Data MCP's available data sources (FRED, BLS, BEA, Census, Treasury, FEC, etc.) to note whether a known federal data source exists
- **Classification during cataloging**: Each variable entry in the catalog gets a preliminary data availability tag: `fed-data` (known federal API source via MCP), `other-data` (known non-federal source like WID, V-Dem), `unknown` (no source identified yet)
- **Not a gate**: Data availability does NOT filter variables out during Phase 2 — the measurability filter already handles unmeasurable variables. This tag is informational, giving Phase 3 a head start
- **MCP as discovery tool**: The MCP server provides 198 tools across 37 federal APIs. During variable cataloging, use it to spot-check whether a variable (e.g., "unemployment rate", "Gini coefficient", "government debt-to-GDP") has a directly queryable federal data source
- **Scope limitation**: This is a quick cross-reference, not exhaustive data sourcing. Spend no more than ~30 seconds per variable on this check. Full data sourcing remains Phase 3's job

### Framework evaluation
- **Primary criterion: data availability** — can the model's required inputs actually be measured for the US with available data? Theoretical fit is secondary
- **Independent evaluation**: Assess each candidate framework on its own merits, not compared against the existing 3 models (comparison happens in a later phase)
- **Surface all viable candidates**: No artificial cap on number of frameworks — include everything that passes the data-availability filter
- **Detailed assessment per framework**: Full writeup including theoretical basis, required inputs, known limitations, validation track record, and data availability assessment

### Output structure & format
- **Separate documents**: Individual files for each deliverable (literature review, variable catalog, framework assessments, dataset inventory, synthesis) — enables downstream phases to reference exactly what they need
- **Variable catalog format**: Hybrid — summary table at top (Variable | Domain | Rating | Contested?) for scanning, then detailed entry per variable below with full context
- **Citation style**: Author-year inline (Turchin 2013) with full bibliography at the end of each document

### Claude's Recommendation
- Adjacent field selection — social movement theory and media/information ecosystem studies added based on their production of measurable, US-applicable predictive variables (mobilization rates, polarization scores) that core domains cite but don't originate
- Hybrid evidence rating — combines quantitative rigor with theoretical breadth to avoid penalizing important variables simply because their field is young or hard to quantify
- Separate documents — recommended given the volume of systematic coverage across 6 fields; keeps individual artifacts usable by downstream agents without parsing irrelevant material
- Hybrid catalog format — summary table for human scanning, detailed entries for agent consumption; best of both approaches
- Data availability cross-referencing — added to give Phase 3 a running start; the US Gov Open Data MCP provides direct queryability against 37 federal APIs during cataloging, turning what would be a Phase 3 cold-start into an incremental check during Phase 2 variable entry

</decisions>

<specifics>
## Specific Ideas

No specific requirements — open to standard approaches

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 02-literature-mining*
*Context gathered: 2026-03-02*
