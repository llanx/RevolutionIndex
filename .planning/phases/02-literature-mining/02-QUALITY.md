---
phase: 02-literature-mining
profiled: 2026-03-03T00:00:00Z
status: acceptable
overall_score: 8.1/10
files_analyzed: 10
blockers: 0
warnings: 3
tools_used:
  opengrep: false
  lizard: false
  jscpd: false
  project_linter: none
---

# Phase 2: Literature Mining Quality Report

**Phase Goal:** Produce a comprehensive, evidence-ranked catalog of variables that predict revolution/instability, along with candidate theoretical frameworks -- so model selection is driven by the full weight of academic evidence rather than three pre-chosen models.
**Profiled:** 2026-03-03
**Status:** acceptable
**Overall Score:** 8.1/10

---

## Profiling Note: Research Phase Evaluation

Phase 02 produced no executable source code. All ten deliverables are markdown knowledge artifacts: six domain literature reviews, one variable catalog, one framework assessment, one dataset inventory, and one synthesis document. Standard code-quality metrics (cyclomatic complexity, nesting depth, function length) do not apply. This profile evaluates the artifacts on four adapted dimensions:

- **Complexity** (information architecture, structural coherence, deduplication quality)
- **Performance** (efficiency of knowledge representation, usability by downstream agents)
- **Style** (internal consistency, citation hygiene, formatting discipline)
- **Idiom** (research document conventions: evidence-to-claim ratio, measurement specificity, honest limitation disclosure)

---

## File Scores

| File | Complexity | Performance | Style | Idiom | Overall | Issues |
|------|-----------|-------------|-------|-------|---------|--------|
| `literature/01-revolution-prediction.md` | 9/10 | 9/10 | 7/10 | 9/10 | 8.6/10 | 1W |
| `literature/02-democratic-backsliding.md` | 9/10 | 9/10 | 9/10 | 9/10 | 9.0/10 | 0 |
| `literature/03-historical-case-studies.md` | 8/10 | 8/10 | 7/10 | 8/10 | 7.8/10 | 1W |
| `literature/04-economic-preconditions.md` | 9/10 | 9/10 | 9/10 | 9/10 | 9.0/10 | 0 |
| `literature/05-social-movement-theory.md` | 8/10 | 9/10 | 9/10 | 8/10 | 8.5/10 | 0 |
| `literature/06-media-information.md` | 9/10 | 9/10 | 9/10 | 9/10 | 9.0/10 | 0 |
| `literature/variable-catalog.md` | 8/10 | 9/10 | 6/10 | 8/10 | 7.8/10 | 1W |
| `literature/framework-assessment.md` | 9/10 | 9/10 | 9/10 | 9/10 | 9.0/10 | 0 |
| `literature/dataset-inventory.md` | 9/10 | 9/10 | 9/10 | 9/10 | 9.0/10 | 0 |
| `literature/synthesis.md` | 9/10 | 9/10 | 8/10 | 9/10 | 8.8/10 | 1W |

---

## Issues by Severity

### Blockers

None.

---

### Warnings

#### 1. Rating distribution statistics in variable-catalog.md do not match the actual data

**File:** `literature/variable-catalog.md` line 83

**Problem:** The summary statistics line reads:

```
**Rating Distribution:** Strong: 13 (29%), Moderate: 20 (44%), Weak: 12 (27%)
```

But counting the actual summary table rows and independently verified by counting the `**Rating:**` labels in all 45 detailed entries yields: **Strong: 14, Moderate: 21, Weak: 10**. The synthesis document (`literature/synthesis.md` line 126) and the phase SUMMARY frontmatter both correctly report 14/21/10. The variable-catalog.md summary statistics line is therefore wrong by one entry in each category, with the total still summing to 45 (the 10 Weak figures, when corrected, match the synthesis).

This inconsistency means the summary line that downstream agents and humans are most likely to quote is incorrect. The error originated in the summary statistics text, not in the actual table or detailed entries.

**Suggested fix:**

```markdown
**Rating Distribution:** Strong: 14 (31%), Moderate: 21 (47%), Weak: 10 (22%)
```

**Improvement:** Eliminates the only internal quantitative inconsistency in the catalog. Downstream phases reading the summary line will get the correct distribution.

---

#### 2. Korotayev et al. (2025) citation is inconsistent across three files

**File:** `literature/01-revolution-prediction.md` line 306, `literature/03-historical-case-studies.md` line 333, `literature/synthesis.md` line 644

**Problem:** The same paper appears with three different sets of author names, journal identifications, and publication statuses:

- `01-revolution-prediction.md` (line 306): "Andrey V. Korotayev, **Stanislav A. Ustyuzhanin**, Leonid E. Grinin, and **Andrey M. Fain**" -- journal: *Comparative Sociology* 24(1): **1-42**
- `03-historical-case-studies.md` (line 333): "A. Korotayev, **V. Ustyuzhanin**, L. Grinin, & **G. Fain**" -- journal: ***Comparative Politics***, forthcoming **[UNVERIFIED]**
- `synthesis.md` (line 644): "Andrey Korotayev, **Victor Ustyuzhanin**, Leonid Grinin, and **Alina Fain**" -- journal: *Comparative Sociology* 24(1): **1-45**

The second and third co-authors' first names differ across all three files (Stanislav vs. Victor vs. V.; Andrey M. vs. G. vs. Alina). The journal differs in Domain 3 review (*Comparative Politics* vs. *Comparative Sociology*). The page range differs between Domain 1 and Synthesis (1-42 vs. 1-45). Domain 3 marks it as forthcoming while Domains 1 and Synthesis treat it as published.

This is the single most-cited source for 5th-generation revolution studies. Citation errors here undermine the document's utility for anyone verifying the source.

**Suggested fix:** Standardize on the Domain 1 version which has the most complete bibliographic data, and mark clearly that specific author names should be verified:

```markdown
Korotayev, Andrey V., Stanislav A. Ustyuzhanin, Leonid E. Grinin, and Andrey M. Fain.
2025. "Five Generations of Revolution Studies: A Systematic Review."
*Comparative Sociology* 24(1): 1-42.
[Author names and page range require verification against published version]
```

Update `03-historical-case-studies.md` and `synthesis.md` to use this standardized entry.

**Improvement:** Consistent, verifiable citation for the source that anchors the entire 5th-generation framing of the phase. Eliminates three-way factual conflict.

---

#### 3. Turchin 2020 bibliography entry in revolution-prediction.md conflates two separate publications

**File:** `literature/01-revolution-prediction.md` line 338

**Problem:** The bibliography entry reads:

```
Turchin, Peter. 2020. "Dynamics of Political Instability in the United States, 1780-2010."
*Journal of Peace Research* 49(4): 577-591.
[Note: Original publication was 2012; the 2020 retrospective assessment appeared in *Cliodynamica*.]
```

This conflates two genuinely distinct works into a single entry:
1. The 2012 *Journal of Peace Research* article ("Dynamics of Political Instability in the United States, 1780-2010" -- a quantitative empirical study)
2. A 2020 *Cliodynamica* blog post/retrospective assessment (a different, lighter-format publication)

The body text at line 112-114 correctly discusses the 2020 *Cliodynamica* piece as a "retrospective assessment." But the bibliography entry is formatted as if it refers to the 2012 JPR article with a clarifying note about the 2020 piece -- which will confuse anyone trying to cite or verify either source. The inline citation `(Turchin 2020)` in the variables table at line 161 would also retrieve the wrong entry.

**Suggested fix:** Split into two separate bibliography entries:

```markdown
Turchin, Peter. 2012. "Dynamics of Political Instability in the United States, 1780-2010."
*Journal of Peace Research* 49(4): 577-591.

Turchin, Peter. 2020. "A Retrospective on 'Ages of Discord.'" *Cliodynamica* (blog),
peterturchin.com, 2020. [URL unavailable; confirm exact post date]
```

Update any inline citations in the body to use `(Turchin 2012)` or `(Turchin 2020)` consistently per which source is actually being referenced.

**Improvement:** Eliminates ambiguity between a peer-reviewed quantitative study and a blog retrospective. Both are valid sources; they should not be merged into one entry.

---

### Info

- `literature/variable-catalog.md:8` -- Variable #8 "Elite Overproduction" uses an undeclared data availability tag `fed-data (partial)` that does not exist in the defined tag system (`fed-data` / `other-data` / `unknown`). The informal "(partial)" qualifier is meaningful but creates a parsing inconsistency. Consider using `fed-data` with a note in the measurement approaches section, or define a formal `fed-data-partial` tag in the Methodology section.

- `literature/variable-catalog.md:85` -- The "Contested Variables" note lists six names separated by commas ("Income Inequality, State Fiscal Distress, Regime Type, Misinformation, Social Media, Information Fragmentation") but only 4 variables carry the Contested marker in the table. The list reads as if six variables are contested rather than four (with three of the six names being sub-parts of variable #33/#35/#43). Adding a clarifying parenthetical would prevent misreading: "4 of 45 (9%) -- Income Inequality, State Fiscal Distress, Regime Type, and the Misinformation/Social Media/Information Fragmentation cluster (variables 33, 35, 43)."

- `literature/01-revolution-prediction.md:118` -- The Korotayev-Medvedev ML discussion includes an explicit `[UNVERIFIED]` flag, which is appropriate. However, the flag sits in the body text rather than in the bibliography entry, where it would be more actionable for downstream verification. Consider migrating verification notes to bibliography entries.

- `literature/03-historical-case-studies.md` -- The NAVCO dataset referenced in the Case Studies domain review is cited as providing evidence for the Chilean Social Outburst (2019) case, but Chile 2019 is beyond NAVCO 2.1's coverage end date (2013). The dataset inventory (Plan 05) correctly documents NAVCO's 2013 cutoff. Cross-checking the case study's source claims against the dataset inventory is recommended before Phase 3 uses these dataset references.

- `literature/synthesis.md:7` -- The executive summary states "14 Strong, 21 Moderate, 10 Weak" -- this is correct and matches the detailed entries. It directly contradicts the variable-catalog.md summary line (Warning #1). Once Warning #1 is fixed, these will be in agreement.

---

## Dimension Summaries

### Complexity

The phase's information architecture is excellent. The decision to catalog at the concept level (rather than treating each proxy measurement as a separate variable) produces a 45-entry catalog that is genuinely scannable and usable by downstream phases, compared to what would have been 95+ raw entries. The deduplication logic is documented, principled, and consistently applied. The synthesis document's variable-to-framework matrix is a particularly high-value artifact -- it directly answers "what is and is not covered by the existing models" in a single table. The only structural weakness is the Tier 13/21/10 vs. 14/21/10 inconsistency noted in Warning #1.

### Performance

All ten documents are immediately usable by downstream phases without preprocessing. The summary tables at the top of each document allow quick scanning; the detailed entries provide depth on demand. The three-tier US applicability classification (directly applicable / applicable with adaptation / not applicable) is a particularly efficient convention -- it prevents Phase 3 from rediscovering the same limitations. The data availability tags (fed-data / other-data / unknown) give Phase 3 a genuine head start on sourcing. The framework assessment's "Could we build this?" framing is an efficient filter that prevents Phase 4 from pursuing theoretically appealing but data-unavailable approaches.

### Style

Most documents are internally consistent and well-formatted. The six domain reviews follow a uniform structure (Scope, Foundational Works, Core Empirical Studies, Recent Developments, Variables Discovered, Key Debates, US Applicability, Bibliography) that makes the collection navigable as a set. The two style issues are localized: the Korotayev citation inconsistency (Warning #2) and the conflated Turchin bibliography entry (Warning #3) in `01-revolution-prediction.md`. The `03-historical-case-studies.md` bibliography uses a citation style (Author, Year. Title. *Journal*. forthcoming.) that differs slightly from the author-year inline convention used in the other five domain reviews, though this is minor.

### Idiom

Research document quality is high. All 45 variables in the catalog include: a rating with explicit criteria, a domain tag, a data availability tag, a definition, an evidence table with study/proxy/finding/type columns, specific measurement approaches with source identification, and a theoretical role section. The distinction between what the evidence supports and what is contested is well-maintained throughout. Particularly strong: the explicit "UNVERIFIED" flags on sources that could not be confirmed, the honest measurement challenge documentation in `06-media-information.md`, and the zero-event problem section in `dataset-inventory.md` which documents a genuine methodological constraint rather than papering over it. These are idiom-correct research document practices.

---

## Cross-File Architecture

The ten files function as a coherent knowledge graph with clear dependency direction: domain reviews (01-06) feed variable catalog (variable-catalog.md), framework assessment (framework-assessment.md), and dataset inventory (dataset-inventory.md), which all feed synthesis (synthesis.md). This is the intended architecture per 02-CONTEXT.md.

| Issue | Type | Files | Severity |
|-------|------|-------|----------|
| Rating statistics mismatch | internal-inconsistency | `variable-catalog.md` (line 83) vs. `synthesis.md` (line 126) | Warning |
| Korotayev citation conflict | citation-inconsistency | `01-revolution-prediction.md`, `03-historical-case-studies.md`, `synthesis.md` | Warning |
| Turchin 2020 conflated entry | citation-issue | `01-revolution-prediction.md` (line 338) | Warning |

No circular dependencies. No orphaned documents. The variable-catalog.md at 1,432 lines is the largest single artifact but its structure (summary table + detailed entries) is appropriate for its role as the project's core reference document. The cross-referencing between domain reviews and the catalog (via concept-level deduplication decisions documented in the catalog) is well-executed.

---

## Rewrite Priority

1. **`literature/variable-catalog.md:83`** -- Fix rating distribution statistics (13/20/12 -> 14/21/10) to match actual data in table and detailed entries. (Warning #1)

2. **`literature/01-revolution-prediction.md:338`, `literature/03-historical-case-studies.md:333`, `literature/synthesis.md:644`** -- Standardize Korotayev et al. (2025) citation and add verification note on author names. (Warning #2)

3. **`literature/01-revolution-prediction.md:338`** -- Split conflated Turchin bibliography entry into Turchin 2012 (JPR) and Turchin 2020 (Cliodynamica). Update inline citations accordingly. (Warning #3)

---

## Overall Assessment

Phase 02 produced ten high-quality knowledge artifacts covering approximately 200 sources across six academic domains. The deliverables are well-structured, internally coherent, and ready for downstream use by Phases 3-5. The three warnings are all citation/metadata issues that do not affect the substantive research conclusions or the variable ratings -- the knowledge itself is sound. None rise to blocker level. The variable catalog, framework assessment, and synthesis document in particular are exceptional outputs that will serve as durable references throughout the project lifecycle.

---
*Profiled: 2026-03-03*
*Profiler: Claude (gsd-profiler)*
