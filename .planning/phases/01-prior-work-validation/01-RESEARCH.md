# Phase 1: Prior Work Validation - Research

**Researched:** 2026-03-01
**Domain:** Academic model validation, data source auditing, mathematical review
**Confidence:** HIGH (all findings based on direct inspection of 250+ pages of project theory docs, existing codebase, two critical reviews, and live FRED series verification)

## Summary

Phase 1 is a pure review/documentation phase -- no new code is written, no models are built. The task is to systematically audit the existing ~250 pages of theory documents and the `revolution-index/` codebase, then produce validation reports that a new reader can use to understand the state of prior work. There are three distinct workstreams: (1) model-by-model assessment of the 3 selected models against their source material and known issues, (2) verification of all 18 data series against their actual sources, and (3) consolidation into a standalone validation report.

The prior work is in substantially better shape than a typical first-draft research project. The three-model selection (dropping RVI, PITF, CSD) was well-reasoned, the critical review identified real mathematical problems that the codebase partially addressed, and the data pipeline architecture is sound. However, the research uncovered specific issues that need documented resolution: the PSI normalization bug (min-max on trending series pins to 1.0), the PLI velocity proxy (magnitude, not actual velocity), the FSP config/code weight divergence, and at least one FRED series (CSCICP03USM665S) with potential discontinuation concerns. These are not blocking issues for validation -- they are findings that the validation report should document as "confirmed issues, deferred to model-building phase for fix."

**Primary recommendation:** Structure validation as three sequential plans: (1) model assessment documents for the 3 models, (2) data series audit for all 18 series, (3) consolidated validation report. Each plan is documentation-only and can be completed by reading existing materials and verifying against external sources.

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| VAL-01 | Review Turchin PSI model specification against academic source material and confirm or revise component definitions (MMP, EMP, SFD) | Research documents the full PSI spec (model-specifications.md sections 1.1-1.6), the critical review's A1 fix (geometric mean), the codebase's simplified 3-proxy implementation, and the implementation review's A1 bug (min-max normalization pins to 1.0 for trending series). Validation should document: what Turchin's theory actually requires vs. what the simplified version captures, which simplifications are acceptable for v1, and which bugs must be fixed before model-building. |
| VAL-02 | Review Prospect Theory PLI specification and confirm or revise domain loss functions and K constants | Research documents the full PLI spec (model-specifications.md sections 2.1-2.6), the critical review's A2 fix (K/10, additive bonuses), the codebase's 5-domain implementation (reduced from 8), the sqrt compression added beyond the critical review's suggestion, and the velocity-is-magnitude bug (implementation review A2). Validation should confirm prospect theory parameters (lambda=2.25, alpha=0.88) against Kahneman-Tversky, assess whether K/10 is sufficient or needs further calibration, and document the domain reduction rationale. |
| VAL-03 | Review Financial Stress Pathway specification and confirm or revise the 2-stage transmission model | Research documents the full 4-stage FS-PIP spec (model-specifications.md sections 3.1-3.9), the decision to implement only Stages 1-2 (FSSI + ETI), the config/code weight divergence (implementation review A3), the N=2 lag calibration concern (critical review C2), and the missing food/energy CPI series. Validation should document what Stage 1-2 captures vs. what the full 4-stage model would add, and whether the 2-stage simplification is defensible. |
| VAL-04 | Apply mathematical fixes from critical review (geometric mean for PSI, K constant correction, additive bonuses for PLI, LOCF over interpolation) | Research confirms these fixes are already partially implemented in the codebase: geometric mean (turchin_psi.py line 92), K/10 (config.py lines 189-194), additive bonuses (prospect_theory.py line 188), LOCF (data_pipeline.py line 77). However, the implementation review found additional bugs layered on top. Validation should produce a checklist: each critical review item, whether it was applied, whether the application introduced new issues, and what remains to fix. |
| VAL-05 | Audit all 18 data series (17 FRED + 1 WID) for current availability, series continuity, and definition changes | Research verified several key series against live FRED: STLFSI4 is active (updated Jan 2026, reading -0.651), FIXHAI is active (Nov 2025 reading 108.4), SPDYNLE00INUSA is active but latest data is 2023 (World Bank lag), CSCICP03USM665S shows data through Jan 2024 with potential discontinuation signal. W270RE1A156NBEA needs verification (related PRS85006173 is active through Q3 2025). MEHOINUSA672N is active (last updated Sep 2025). WID API endpoint needs live testing. The full audit requires checking each of the 17 FRED series and the WID series individually. |
| VAL-06 | Produce a validation report documenting what was confirmed, revised, or flagged for further investigation | Research defines the report structure: executive summary, per-model assessments (confirmed/revised/flagged), data series audit table, mathematical fix checklist, known bugs deferred to model-building, and open questions for literature mining. The report should be self-contained -- a reader should understand the state of prior work without reading the original 250 pages. |
</phase_requirements>

## Standard Stack

This phase is documentation-only. No libraries or code are involved. The "stack" is the set of materials to be reviewed and the tools used to verify data sources.

### Core Materials to Review

| Document | Location | Size | Purpose in Validation |
|----------|----------|------|----------------------|
| model-specifications.md | repo root | ~1200 lines | Primary spec for all 6 models; Phase 1 validates Models 1-3 |
| critical-review-model-specs.md | repo root | ~425 lines | Peer review identifying math errors (A1-A4), pipeline issues (B1-B4), conceptual problems (C1-C4), missing specs (D1-D4) |
| critical-review-implementation.md | revolution-index/ | ~215 lines | Implementation review identifying code bugs (A1-A4), design issues (B1-B4), missing pieces (C1-C4) |
| revolution-metrics-data-sources.md | repo root | ~1000+ lines | Comprehensive data source inventory |
| gap-analysis-literature-review.md | repo root | ~300+ lines | Literature gaps and missing variables |
| config.py | revolution-index/ | ~297 lines | All FRED series IDs, model parameters, backtesting episodes |
| turchin_psi.py | revolution-index/src/models/ | ~119 lines | PSI implementation to verify against spec |
| prospect_theory.py | revolution-index/src/models/ | ~214 lines | PLI implementation to verify against spec |
| financial_stress.py | revolution-index/src/models/ | ~213 lines | FSP implementation to verify against spec |
| data_pipeline.py | revolution-index/src/data/ | ~253 lines | Pipeline implementation to verify LOCF, freshness |
| normalization.py | revolution-index/src/analysis/ | ~143 lines | Normalization functions to verify against spec |

### Verification Tools

| Tool | Purpose | When to Use |
|------|---------|-------------|
| FRED website | Verify series availability, check for discontinuation notices, confirm definitions | Data audit (VAL-05) |
| WID.world website | Verify sptinc992j availability and API endpoint | Data audit (VAL-05) |
| Web search | Cross-reference Turchin, Kahneman-Tversky, and financial stress literature | Model review (VAL-01, VAL-02, VAL-03) |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Manual FRED verification | fredapi Python calls | Would require FRED API key the user doesn't have yet; manual web check is sufficient for availability audit |
| Reading all 250 pages fresh | Using the two critical reviews as index | Critical reviews already synthesize the key issues; reading full specs only needed for specific sections flagged as questionable |

## Architecture Patterns

### Recommended Validation Document Structure

The validation phase produces documentation, not code. The recommended structure:

```
.planning/phases/01-prior-work-validation/
    01-RESEARCH.md          # This file
    01-01-PLAN.md           # Plan: Model assessments
    01-02-PLAN.md           # Plan: Data series audit
    01-03-PLAN.md           # Plan: Consolidated validation report
```

Output deliverables (written during plan execution):

```
validation/
    model-assessment-turchin-psi.md
    model-assessment-prospect-theory-pli.md
    model-assessment-financial-stress-pathway.md
    data-series-audit.md
    math-fix-checklist.md
    validation-report.md          # The consolidated report (VAL-06)
```

### Pattern 1: Model Assessment Document

**What:** A structured assessment for each of the 3 models that documents what the spec claims, what the critical review found, what the code actually does, and what the validation concludes.

**When to use:** For VAL-01, VAL-02, VAL-03.

**Structure:**
```markdown
# Model Assessment: [Model Name]

## 1. Theoretical Basis
- What the spec claims the model measures
- Source academic work and how faithfully it's adapted

## 2. Component Review
For each component (e.g., MMP, EMP, SFD for PSI):
- Spec definition vs. code implementation
- Simplifications made and whether they're defensible
- Known issues from critical reviews

## 3. Mathematical Fix Status
- Which critical review fixes were applied
- Whether the application is correct
- Any new issues introduced by the fix

## 4. Verdict
- CONFIRMED: Elements that hold up
- REVISED: Elements changed from spec with rationale
- FLAGGED: Elements that are questionable and need attention in model-building
```

### Pattern 2: Data Series Audit Row

**What:** A standardized row format for auditing each of the 18 data series.

**When to use:** For VAL-05.

**Structure per series:**
```markdown
| Series ID | Description | Model | Status | Latest Data | Frequency | Notes |
```

Status categories:
- ACTIVE: Series is current, regularly updated, no definition changes
- ACTIVE-LAGGED: Series is current but latest data is significantly behind (e.g., annual series with 1-2 year lag)
- CHANGED: Series is active but definition/methodology changed
- DISCONTINUED: Series no longer updated; replacement identified or needed
- UNVERIFIED: Could not confirm status (flag for follow-up)

### Pattern 3: Mathematical Fix Checklist

**What:** A row-by-row accounting of each fix recommended by the critical review.

**When to use:** For VAL-04.

**Structure:**
```markdown
| Review ID | Issue | Recommended Fix | Applied? | Correct? | New Issues? | Status |
```

### Anti-Patterns to Avoid

- **Re-implementing models during validation:** Phase 1 reviews what exists. Code changes happen in Phase 4 (Model Building). Validation documents what needs to change, it does not make the changes.
- **Treating the validation report as a literature review:** The validation report assesses the state of existing prior work. Literature mining is Phase 2. Do not scope-creep into new academic sources.
- **Verifying data by downloading it:** The user does not have a FRED API key yet. Data audit means checking the FRED website for series availability, not running the pipeline.
- **Rewriting the 250 pages:** The validation report should be a concise 15-25 page document, not a restatement of the original research. It should be structured so a reader knows what was confirmed, what was revised, and what was flagged -- without reading everything else.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Checking FRED series availability | Python API calls | FRED website manual check | No API key available yet; website shows discontinuation notices, definition changes, and latest values |
| Academic source verification | Full literature review | Targeted verification of specific claims | Full literature mining is Phase 2; validation only verifies claims already made in the existing docs |
| Model correctness testing | Running the models | Code review against spec | Cannot run models without data; code review identifies bugs without execution |

**Key insight:** This phase is entirely about reading, reviewing, and documenting. Every temptation to "just quickly fix this" or "let me run this to check" should be redirected to a "FLAGGED for Phase 4" note in the validation report.

## Common Pitfalls

### Pitfall 1: Scope Creep into Literature Mining
**What goes wrong:** While reviewing Turchin PSI, the reviewer discovers that Turchin published new work in 2024 and wants to incorporate it. Or while reviewing the gap analysis, the reviewer wants to find additional missing variables.
**Why it happens:** The prior work is intellectually stimulating and there's always more to read.
**How to avoid:** Phase 1 validates the existing prior work as-is. New literature is Phase 2. If new sources are discovered during validation, add them to an "open questions for Phase 2" section, do not pursue them.
**Warning signs:** Finding yourself doing web searches for new academic papers rather than verifying claims in the existing documents.

### Pitfall 2: Trying to Fix Code During Validation
**What goes wrong:** The normalization bug (implementation review A1) is easy to fix -- just switch to `percentile_rank_series`. The temptation is to fix it now.
**Why it happens:** Known bugs create discomfort. The fix seems trivial.
**How to avoid:** Document the bug, document the fix, flag it for Phase 4. Validation produces a punch list, not patches.
**Warning signs:** Opening code files in edit mode rather than read mode.

### Pitfall 3: Perfectionism on the Validation Report
**What goes wrong:** The validation report tries to be comprehensive about every detail in the 250 pages, becoming 100+ pages itself.
**Why it happens:** The prior work is detailed and there's pressure to be thorough.
**How to avoid:** The validation report has a specific audience: someone who needs to understand the state of prior work to plan Phase 2-5. Focus on decisions (confirmed/revised/flagged), not on exhaustive restatement. Use references to the source documents for details.
**Warning signs:** The report exceeds 30 pages or spends more than 2 paragraphs on any single issue.

### Pitfall 4: Failing to Distinguish Spec Issues from Code Issues
**What goes wrong:** Conflating "the spec's formula is wrong" (critical review A1: PSI multiplication) with "the code's implementation of the fix is also wrong" (implementation review A1: min-max normalization). These are different layers of problems.
**Why it happens:** Both reviews exist and both flag issues. It's easy to blur which problems are in the theory vs. which are in the code.
**How to avoid:** The model assessment should explicitly separate: (a) spec-level issues (theory/formula problems), (b) fix-level issues (was the critical review's fix correctly specified?), (c) code-level issues (was the fix correctly implemented?). Use a three-column structure.
**Warning signs:** A finding that says "PSI is broken" without specifying whether the spec, the fix, or the code is the problem.

### Pitfall 5: Treating All 18 Series as Equal Audit Effort
**What goes wrong:** Spending the same time verifying CPIAUCSL (one of the most stable series in FRED) as verifying CSCICP03USM665S (which has discontinuation signals).
**Why it happens:** The requirement says "audit all 18."
**How to avoid:** Triage. High-frequency, well-known series (UNRATE, CPIAUCSL, VIXCLS) need a quick "still active, no changes" check. Annual/specialty series (SPDYNLE00INUSA, CSCICP03USM665S) and the WID series need deeper investigation. Concentrate effort where risk is highest.
**Warning signs:** Equal-length audit entries for UNRATE and for the WID API.

## Code Examples

Not applicable -- this phase produces documentation, not code. See "Architecture Patterns" above for document templates.

## State of the Art

### What the Critical Reviews Already Established

The two critical reviews (of the spec and of the implementation) are the closest thing to "prior art" for this validation phase. They provide a systematic issues list that forms the backbone of the validation.

| Review | Scope | Key Findings Count | Must-Fix Count |
|--------|-------|--------------------|----------------|
| critical-review-model-specs.md | 6 model specs | 15 issues (A1-A4, B1-B4, C1-C4, D1-D3) | 6 "must fix" |
| critical-review-implementation.md | 3-model codebase | 12 issues (A1-A4, B1-B4, C1-C4) | 3 HIGH severity |

### Overlap Between Reviews

Several issues appear in both reviews (the spec problem AND its implementation):

| Spec Issue | Implementation Issue | Nature |
|------------|---------------------|--------|
| A1: PSI multiplication crushes mid-range | Implemented as geometric mean, BUT A1: min-max pins trending series to 1.0 | Fix applied, new bug introduced |
| A2: PLI K constants too large | K reduced by 10x, BUT A2: velocity bonus is magnitude not velocity | Fix applied, separate bug present |
| B1: No interpolation strategy | LOCF implemented correctly | Fix applied correctly |
| B2: Inconsistent historical distributions | Common 1970-present reference, BUT expanding window still includes current value | Fix partially applied |
| C1: Massive metric overlap | 3-model selection reduces overlap, BUT B1: construct-level overlap remains | Partially addressed, honestly documented |

### Issues Unique to Each Review

**Spec-only issues (not yet relevant to code because they affect deferred models):**
- A3: RVI constellation bonus arbitrary (RVI deferred)
- A4: PITF coefficients fictional (PITF deferred)
- C3: Union density scoring incoherent (RVI deferred)
- C4: CSD detecting trends not tipping points (CSD deferred)

**Implementation-only issues:**
- A3: Config ETI weights don't match model weights (6 config vs. 4 code)
- A4: WID API URL untested/inconsistent
- B2: PSI simplified proxies may not measure what Turchin measures
- B3: Backtesting treats all episodes as equal severity
- B4: Bootstrap uncertainty too narrow (only perturbs reference window)
- C1: No tests
- C2: Config `invert` field defined but never read
- C3: `compute_historical` is O(n^2)
- C4: Food/energy CPI planned but not implemented

## Detailed Findings for Each Model

### Turchin PSI (VAL-01)

**Theoretical basis:** Turchin's structural-demographic theory. PSI = MMP x EMP x SFD. Multiplicative interaction means all three pressures must be present simultaneously. This is well-established academic work (Turchin 2003, 2010, 2023).

**Simplified implementation uses:**
- MMP = inverted labor share of GDP (W270RE1A156NBEA) -- spec offers this as "Alternative MMP"
- EMP = top 1% income share (WID sptinc992j) -- spec offers this as "Alternative EMP"
- SFD = federal debt/GDP (GFDEGDQ188S) -- spec offers this as "Alternative SFD"

**What the simplification loses (from implementation review B2):**
- MMP: loses urbanization amplifier and youth bulge ratio
- EMP: loses elite density (degree holders per capita), political competition intensity, wealth concentration ratio
- SFD: loses deficit flow, interest/revenue burden, and government trust modifier

**Known issues to document:**
1. Geometric mean fix (critical review A1) -- correctly applied in code (line 92 of turchin_psi.py)
2. Min-max normalization bug (implementation review A1) -- reference includes current date, trending series pin to 1.0. The `percentile_rank_series` function exists in normalization.py but is not used by PSI.
3. The implementation review correctly notes this is "PSI-Simple" and should be labeled as such

**Confidence:** HIGH -- the issues are well-documented across both reviews and the code is readable.

### Prospect Theory PLI (VAL-02)

**Theoretical basis:** Kahneman & Tversky prospect theory. Loss aversion (lambda=2.25), diminishing sensitivity (alpha=0.88), reference-point dependence. These parameters are from the original 1992 paper and are well-established.

**Implementation reduces from 8 domains to 5:**
- Kept: Wages, Housing, Health, Employment, Security/Sentiment
- Dropped: Democracy (V-Dem), Mobility (Opportunity Insights), Trust (Pew)
- Rationale: dropped domains lack freely-available, regularly-updated data from FRED

**Fixes applied:**
1. K constants divided by 10 (critical review A2) -- applied in config.py
2. Breadth/velocity changed from multiplicative to additive bonuses (A2) -- applied in prospect_theory.py line 188
3. Additional sqrt compression on loss scores (line 131) -- this goes beyond the critical review's recommendation

**Known issues to document:**
1. Velocity bonus (implementation review A2) -- computes deviation magnitude, not actual rate of change. The code comment at line 182-183 acknowledges this as a "proxy."
2. The sqrt compression + K/10 may overcorrect (original saturated at 100; the double fix may now underreport). This needs empirical testing in Phase 4.
3. Loss score formula at line 131: `min(100, max(0, sqrt(-V * K) * 10))` -- the `* 10` multiplier is undocumented in either the spec or the critical review. This is an implementation-level addition that should be documented.

**Confidence:** HIGH -- prospect theory parameters are well-established; implementation issues are clearly identified.

### Financial Stress Pathway (VAL-03)

**Theoretical basis:** Causal chain model: Financial Stress -> Economic Pain -> Political Grievance -> Mobilization. The 2008 GFC -> Occupy/Tea Party -> Trump/Sanders narrative is the primary validation case.

**Implementation covers Stages 1-2 only (FSSI + ETI):**
- Stage 1 (FSSI): 5 financial stress indicators with z-score normalization
- Stage 2 (ETI): 4 economic pain indicators (code) vs. 6 (config)
- Stages 3-4 (Political Grievance, Mobilization): deferred -- require non-FRED data

**Known issues to document:**
1. Config/code weight divergence (implementation review A3): config lists 6 ETI series summing to 1.0, code uses 4 series summing to 1.0. Two config entries are ghosts (`debt_service`, `food_energy_cpi`).
2. N=2 lag calibration (critical review C2): the lag structure is "rough empirical guidance" based on 2008 and 2020, not calibrated parameters.
3. The combined score (`(FSSI + ETI) / 2.0`) is a simple average that loses the causal-chain insight. The spec's max-based aggregation (`max(FSSI, ETI, PGFI, MAI)`) is more theoretically motivated but requires all 4 stages.
4. The model is the most novel theoretical contribution in the project (critical review E2) but also the most data-constrained.

**Confidence:** HIGH for Stage 1 (financial stress indicators are standard); MEDIUM for Stage 2 (config/code divergence needs resolution); LOW for the deferred Stages 3-4 assessment.

## Data Series Preliminary Findings (VAL-05)

Based on web verification conducted during research:

### Verified Active

| Series ID | Description | Model | Status | Latest Data | Notes |
|-----------|-------------|-------|--------|-------------|-------|
| STLFSI4 | St. Louis Fed Financial Stress Index | FSP-FSSI | ACTIVE | Jan 2026 | Weekly updates, reading -0.651 |
| FIXHAI | Housing Affordability Index (Fixed) | PLI | ACTIVE | Nov 2025 | Monthly; note COMPHAI was discontinued in 2019, FIXHAI is the replacement |
| MEHOINUSA672N | Real median household income | PLI | ACTIVE-LAGGED | Sep 2025 update (2024 data) | Annual, ~1 year lag typical |
| SPDYNLE00INUSA | Life expectancy at birth | PLI | ACTIVE-LAGGED | 2023 | World Bank source, ~2 year lag typical |
| W270RE1A156NBEA | Labor share of GDP | PSI | NEEDS VERIFICATION | Unknown | Related series PRS85006173 active through Q3 2025; need to confirm this specific series ID |

### Potentially Concerning

| Series ID | Description | Model | Status | Concern |
|-----------|-------------|-------|--------|---------|
| CSCICP03USM665S | OECD Consumer Confidence (amplitude adjusted) | FSP-ETI | POSSIBLE DISCONTINUATION | Data through Jan 2024 only; YCharts shows OECD indicator as discontinued. Need to verify and identify replacement. |
| WID sptinc992j | Top 1% income share | PSI | UNVERIFIED | WID API endpoint in code may be wrong (two different URLs in wid_loader.py). Need live test. |

### Not Yet Checked (require full audit)

The following series need verification during plan execution:
- GFDEGDQ188S (debt/GDP)
- T10Y2Y (yield curve spread)
- VIXCLS (VIX)
- BAMLH0A0HYM2 (high yield spread)
- DRSFRMACBS (mortgage delinquency)
- UNRATE (unemployment)
- IC4WSA (initial claims)
- CES0500000003 (average hourly earnings)
- CPIAUCSL (CPI)
- UMCSENT (consumer sentiment)
- LNS12300060 (prime-age employment ratio)

Most of these are major, well-known series unlikely to have availability issues, but the audit should confirm and document.

## Open Questions

1. **W270RE1A156NBEA vs. PRS85006173**
   - What we know: The config uses W270RE1A156NBEA ("Labor share of GDP, nonfarm business sector"). The model-specifications.md mentions PRS85006173 as an alternative. Web search found PRS85006173 active through Q3 2025 but did not confirm W270RE1A156NBEA specifically.
   - What's unclear: Whether W270RE1A156NBEA is still actively updated or has been superseded.
   - Recommendation: Check FRED directly during data audit. If discontinued, PRS85006173 is the natural replacement.

2. **CSCICP03USM665S Discontinuation**
   - What we know: Data appears to end at Jan 2024. One source shows it as discontinued.
   - What's unclear: Whether this is a permanent discontinuation or a temporary lag in OECD data publication.
   - Recommendation: Verify during data audit. If discontinued, identify replacement (possibly OECD's newer CLI series or Conference Board direct data).

3. **WID API Reliability**
   - What we know: The codebase has two different API URLs (lines 29 and 82 of wid_loader.py). The implementation review flagged this as untested.
   - What's unclear: Whether either URL works. WID.world API has changed multiple times.
   - Recommendation: Document as "UNVERIFIED -- requires live test." The fallback (manual CSV download) is well-documented in the code.

4. **How deep should model assessment go into source academic work?**
   - What we know: The spec cites Turchin, Kahneman-Tversky, and the 2008 financial crisis literature.
   - What's unclear: Whether validation should trace claims back to the original papers or treat the spec + critical review as sufficient.
   - Recommendation: Treat the spec + critical review as the primary sources. Only check original academic work for specific disputed claims. Full literature review is Phase 2.

5. **What counts as "confirmed" for the validation report?**
   - What we know: The success criteria say "documented assessment stating what is confirmed, what is revised, and what is flagged as questionable."
   - What's unclear: The standard of evidence for "confirmed." Does the spec's claim need to be verified against external sources, or is it sufficient that the critical review did not dispute it?
   - Recommendation: Use a three-tier system. CONFIRMED = critical review did not dispute AND code implements correctly. REVISED = critical review flagged an issue AND a fix was applied. FLAGGED = issue identified but not yet resolved (deferred to later phases).

## Sources

### Primary (HIGH confidence)
- `model-specifications.md` -- 1200+ lines of model specs (direct inspection)
- `critical-review-model-specs.md` -- 425 lines of academic critique (direct inspection)
- `critical-review-implementation.md` -- 215 lines of code review (direct inspection)
- `revolution-index/` codebase -- all Python files directly read and analyzed
- `revolution-metrics-data-sources.md` -- 1000+ lines of data inventory (direct inspection)
- `gap-analysis-literature-review.md` -- 300+ lines of gap analysis (direct inspection)
- `config.py` -- all 17 FRED series IDs and 1 WID series ID (direct inspection)

### Secondary (MEDIUM confidence)
- [FRED STLFSI4](https://fred.stlouisfed.org/series/STLFSI4) -- verified active, Jan 2026 data
- [FRED FIXHAI](https://fred.stlouisfed.org/series/FIXHAI) -- verified active, Nov 2025 data
- [FRED MEHOINUSA672N](https://fred.stlouisfed.org/series/MEHOINUSA672N) -- verified active, updated Sep 2025
- [FRED SPDYNLE00INUSA](https://fred.stlouisfed.org/series/SPDYNLE00INUSA) -- verified active, data through 2023
- [FRED CSCICP03USM665S](https://fred.stlouisfed.org/series/CSCICP03USM665S) -- data through Jan 2024, possible discontinuation
- [WID.world codes dictionary](https://wid.world/codes-dictionary/) -- sptinc992j variable confirmed in dictionary

### Tertiary (LOW confidence)
- W270RE1A156NBEA availability -- not directly verified against FRED website, inferred from related series
- WID API endpoint reliability -- neither URL in the codebase has been tested
- CSCICP03USM665S discontinuation status -- conflicting signals between FRED page and third-party sources

## Metadata

**Confidence breakdown:**
- Model assessments: HIGH -- both critical reviews provide comprehensive issue inventories; code is readable and well-commented
- Data series audit: MEDIUM -- several series verified but 11 of 18 still need individual checks; one series has concerning signals
- Mathematical fix checklist: HIGH -- fixes are explicitly documented in critical review and traceable in code
- Validation report structure: HIGH -- success criteria are clear and the output format is well-defined

**Research date:** 2026-03-01
**Valid until:** No expiration -- this is a review of existing static materials. FRED series status should be re-verified if more than 30 days pass before the data audit is executed.
