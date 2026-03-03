# Prior Work Validation Report

**Date:** 2026-03-02
**Scope:** Validation of 3 selected models and 18 data series from the Revolution Index Research project
**Supporting documents:** model assessments (3), data series audit (1), math fix checklist (1)

---

## Executive Summary

The Revolution Index Research project aims to produce a defensible, data-backed political stress score for the United States by synthesizing three independent models grounded in academic research: a structural-demographic Political Stress Indicator (Turchin PSI), a behavioral Perceived Loss Index (Prospect Theory PLI), and a Financial Stress Pathway (FSP) modeling the causal chain from financial crisis to political mobilization. The prior research produced approximately 250 pages of theory documents, model specifications, critical reviews, and a working Python codebase spanning data pipelines, model computations, normalization, backtesting, and uncertainty quantification.

This validation assessed how much of that prior work holds up under structured scrutiny. The overall verdict is **mixed: the theoretical foundations are sound, the critical review process was thorough, and several important fixes have been correctly applied -- but significant implementation issues remain that would produce misleading outputs if the models were run today.** The most critical problem is a min-max normalization bug in the PSI model that pins two of three components near 1.0, making the model's output effectively determined by whichever input is not at its historical extreme. The PLI model contains an undocumented formula transformation (sqrt compression plus a `*10` multiplier) that deviates from both the spec and the critical review. The FSP model has a config/code divergence where the configuration file and the source code define different weights for different numbers of series.

Of the 27 issues tracked across both critical reviews, 4 are fully resolved, 18 remain open for Phase 4 (model building), and 5 are deferred because they affect models not selected for the 3-model implementation. The data series audit found 15 of 18 series confirmed active, 1 discontinued (OECD Consumer Confidence, the highest-weighted ETI component in the FSP model), 1 changed (MBA mortgage delinquency methodology revision), and 1 unverified (WID top 1% income share API endpoint).

The project is ready to proceed to Phase 2 (literature mining). The theoretical frameworks are well-grounded, the data pipeline infrastructure exists, and the issues identified are implementation problems that can be fixed during Phase 4 model building. No issues were found that would fundamentally invalidate the 3-model approach. However, **this validation was conducted without running the models, downloading actual data, or verifying findings against original academic papers in depth.** The assessments are based on code review, spec analysis, and public data source verification -- not empirical testing.

---

## 1. Model Validation Summary

### 1.1 Turchin PSI -- Conceptually Sound, Implementation Needs Work

The Political Stress Indicator implements Peter Turchin's structural-demographic theory, modeling instability as the interaction of mass mobilization potential (MMP), elite mobilization potential (EMP), and state fiscal distress (SFD). The theoretical foundation is well-grounded in Turchin's published work (*Historical Dynamics*, *Secular Cycles*, *End Times*), and the multiplicative interaction structure -- where instability requires all three pressures simultaneously -- faithfully preserves the core theoretical claim.

The geometric mean fix from the critical review (spec A1) is correctly applied: the aggregation changed from `MMP x EMP x SFD` (which compresses mid-range values -- three inputs at 0.70 yield 0.343) to `(MMP x EMP x SFD)^(1/3)` (which preserves the interaction property while maintaining output in the [0,1] range). The common 1970-present reference period (config.py) addresses historical distribution length inconsistencies.

However, the implementation uses drastically simplified proxy variables compared to Turchin's multi-factor composites. Each of the three components is reduced to a single FRED series: labor share of GDP for MMP, top 1% income share for EMP, and federal debt-to-GDP for SFD. This is a defensible v1 simplification -- the spec explicitly offers these as simplified alternatives -- but it loses key theoretical channels, particularly the government trust modifier in SFD and the elite overproduction dynamic in EMP (income concentration is not the same as overproduction of frustrated elite aspirants).

**Confirmed:**
- Multiplicative interaction structure grounded in Turchin's academic work
- Geometric mean aggregation fix correctly applied (spec A1)
- Common 1970-present reference period addresses distribution length concerns (spec B2)
- Data series selections (W270RE1A156NBEA, WID sptinc992j, GFDEGDQ188S) are reasonable for a simplified v1

**Revised:**
- Aggregation changed from product to geometric mean per critical review A1
- Model scope labeled "PSI-Simple" -- 3-proxy approximation, not full Turchin PSI

**Flagged:**
- Min-max normalization on trending series (CRITICAL): SFD permanently pinned at 1.0 (debt/GDP is monotonically rising); EMP near 1.0 (top 1% share on long uptrend). The `percentile_rank_series` function exists in normalization.py but is not used.
- WID API reliability: Two inconsistent URLs in wid_loader.py, neither tested against live API
- SFD proxy weakness: Debt level alone does not measure fiscal distress (Japan case demonstrates high debt without crisis)
- Labor share responsiveness: W270RE1A156NBEA moves on decadal timescales; MMP may be unresponsive to within-decade shifts

See: `validation/model-assessment-turchin-psi.md` for full assessment.

### 1.2 Prospect Theory PLI -- Theoretically Strongest, Formula Needs Clarification

The Perceived Loss Index applies Kahneman and Tversky's prospect theory to measure perceived losses across five life domains (wages, housing, health, employment, security/sentiment) relative to 10-year trailing peaks. The theoretical foundation is the strongest of the three models: lambda = 2.25 and alpha = 0.88 are well-established empirical parameters from Tversky & Kahneman (1992), and the critical review specifically praised the application of prospect theory to political risk as "a legitimate theoretical contribution" (E3).

The domain reduction from 8 to 5 is well-motivated by data availability. The three dropped domains (Democracy/V-Dem, Mobility/Opportunity Insights, Trust/Pew) lack freely-available, regularly-updated FRED data. The change from multiplicative to additive aggregation for breadth and velocity bonuses correctly prevents the saturation problem identified in critical review A2 (the original formula produced binary 0-or-100 output during any recession).

The primary concern is an undocumented loss score formula. The spec defines `loss_score = -V x K`, and the critical review recommended reducing K by 5-10x. The code instead computes `sqrt(-V x K) * 10` -- adding sqrt compression and a 10x multiplier that appear in neither the spec nor the critical review. Combined with the uniform K/10 reduction, this creates a triple correction (K/10 + sqrt + additive bonuses) whose net effect on output calibration is an empirical question requiring backtesting. Additionally, the velocity bonus computes loss magnitude rather than actual rate of change, making it redundant with the mean loss score.

**Confirmed:**
- Prospect theory value function with lambda = 2.25, alpha = 0.88 (established parameters)
- 10-year trailing peak as reference point (reasonable operationalization of collective memory)
- Domain reduction from 8 to 5 (well-motivated by data availability)
- Additive aggregation prevents saturation (correct fix per critical review A2)
- K constant reduction by uniform 10x preserves relative domain weighting

**Revised:**
- Aggregation changed from multiplicative to additive per critical review A2
- K constants reduced by 10x from spec values
- Loss score formula changed from `-V x K` to `sqrt(-V x K) * 10`

**Flagged:**
- Undocumented sqrt compression and `*10` multiplier (MODERATE): Deviates from both spec and critical review
- Velocity bonus computes magnitude, not velocity (MODERATE): Redundant with mean loss score
- Potential double-correction (MODERATE): K/10 + sqrt may cause underreporting; needs backtesting against known episodes (1968, 2008, 2020)
- Domain K calibration (LOW): Relative magnitudes across domains are hand-tuned, not empirically derived

See: `validation/model-assessment-prospect-theory-pli.md` for full assessment.

### 1.3 Financial Stress Pathway -- Novel Theory, Half-Implemented

The Financial Stress Pathway models the causal chain from financial system stress through economic hardship through political grievance through mobilization. This staged causal-chain structure is the spec's most original theoretical contribution (critical review E2), and the 2008 narrative (GFC -> Tea Party/Occupy -> Trump/Sanders -> January 6) provides a plausible validation case.

The z-score normalization approach for financial and economic indicators is standard and well-understood -- significantly better than PSI's min-max approach for trending series. The FSSI (Stage 1) composite of 5 financial stress indicators uses rolling 20-year z-scores converted to a 0-100 scale via the normal CDF, producing graduated output that avoids the pinning problem seen in PSI. The cross-correlation lag analysis provides an empirical approach to measuring transmission lag that is more honest than hardcoded parameters.

However, only 2 of the 4 theoretical stages are implemented. Stages 3 (Political Grievance) and 4 (Mobilization Activation) are deferred because they require non-FRED data sources. This is a significant theoretical reduction: the model can measure "is financial stress becoming economic pain?" but not "is economic pain becoming political mobilization?" -- which is the question that matters for revolution risk. The ETI (Stage 2) has been reduced from the spec's 8 variables to 4 in code (with 6 in config, creating a divergence), and the aggregation changed from max-based (the "leading edge" of the causal chain) to a simple average, losing the early-warning insight.

**Confirmed:**
- Causal chain theory is the most novel contribution; 2008-2021 narrative validates the general framework
- Z-score normalization is standard and produces graduated output (no pinning problem)
- FSSI composition (5 financial stress indicators) uses well-established measures
- Cross-correlation lag analysis is more honest than hardcoded lag parameters
- LOCF for frequency alignment correctly applied

**Revised:**
- Stage implementation reduced from 4 to 2 (FSSI + ETI only)
- ETI reduced from spec's 8 variables to 4 in code
- FSSI reduced from spec's 6 variables to 5 (dropped bank loan loss provisions; substituted STLFSI4 for OFR FSI)
- Aggregation changed from max-based to simple average of Stages 1-2

**Flagged:**
- Config/code ETI weight divergence (HIGH): Config lists 6 series; code hardcodes 4 with different weights. Ghost entries reference nonexistent data.
- CSCICP03USM665S potential discontinuation (HIGH): Highest-weighted ETI component (0.35 in code) appears discontinued since Jan 2024
- Stages 3-4 gap (MODERATE): Only half the causal chain is implemented
- N=2 lag calibration (MODERATE): Lag structure based on only 2 usable episodes (2008, 2020)
- Simple average aggregation (LOW): Masks early warning signals when FSSI is high but ETI is still low

See: `validation/model-assessment-financial-stress-pathway.md` for full assessment.

### 1.4 Cross-Model Observations

**Common issues across all three models:**

1. **Normalization inconsistency:** PSI uses min-max normalization (with a known pinning bug), PLI uses 10-year trailing peak comparison (sound), and FSP uses rolling 20-year z-scores (sound). The choice of normalization method has a larger impact on model output than the underlying theory. Standardizing the normalization approach -- or at minimum understanding why each model uses a different method -- should be a Phase 4 priority.

2. **Data reduction from spec:** All three models implement significantly fewer variables than their specifications define. PSI uses 3 proxies instead of multi-factor composites. PLI uses 5 of 8 domains. FSP uses 4 of 8 ETI variables and 2 of 4 stages. This is pragmatic (FRED-available data only) but means the models are testing simplified hypotheses, not the full theories.

3. **Construct-level overlap:** While the 3-model selection achieves zero overlap at the FRED series ID level, construct-level overlap remains. PSI's labor share, PLI's employment ratio, and FSP's unemployment rate all measure variants of "how the labor market treats workers." Inter-model correlation analysis in Phase 4 backtesting will quantify the actual overlap.

**Relative validation status:**

- **PLI is the most validated model:** Sound theoretical foundation, correct aggregation fixes, no normalization pinning bug, well-motivated domain selection. The undocumented formula is concerning but does not affect the theoretical framework.
- **FSP has the most novel theory but weakest implementation:** The causal chain concept is valuable, but half the chain is missing and the ETI stage has config/code divergence plus a discontinued data series.
- **PSI has the most critical bug:** The min-max normalization on trending series makes the model's current output uninterpretable. However, the fix is straightforward (switch to percentile rank, which already exists in the codebase).

**Does the 3-model selection still make sense?** Yes. The three models measure different dimensions of political stress (structural demographics, perceived losses, financial transmission), and the validation found no issues that would fundamentally invalidate any of them. The deferred models (RVI, PITF, CSD) were correctly excluded: RVI overlaps with PSI, PITF had fabricated coefficients, and CSD requires computed outputs from the other models. Phase 2 literature mining may surface alternative frameworks, but the current selection provides a reasonable starting point.

---

## 2. Mathematical Fix Status

### Summary Statistics

| Category | Total | Resolved | Open | Deferred |
|----------|-------|----------|------|----------|
| Spec-level (A1-D3) | 15 | 4 | 6 | 5 |
| Implementation-level (A1-C4) | 12 | 0 | 12 | 0 |
| **Combined Total** | **27** | **4** | **18** | **5** |

"Resolved" means the fix is applied and correct with no new issues. "Open" means the issue needs attention in Phase 4 -- either the fix was not applied, was applied with new issues, or was only partially applied. "Deferred" means the issue affects models not selected for the 3-model implementation (RVI, PITF, CSD).

### Resolved Issues (4)

1. **Spec A1 -- PSI multiplication crushes mid-range values:** Geometric mean `(MMP x EMP x SFD)^(1/3)` correctly applied.
2. **Spec B1 -- Mixing data frequencies:** LOCF implemented in data pipeline. Cleanest fix in the codebase.
3. **Spec B2 -- Inconsistent historical distribution lengths:** Common 1970-present reference period applied.
4. **Spec C2 -- FSP lag structure based on N=2:** Cross-correlation analysis provides empirical measurement rather than hardcoded lags.

### Critical Open Items (must fix in Phase 4)

1. **Impl A1 -- Min-max normalization on trending series (CRITICAL):** SFD permanently pinned at 1.0, EMP near 1.0. The `percentile_rank_series` function exists but is unused. This is the single most impactful bug in the codebase.
2. **Spec A2 / Impl A2 -- PLI undocumented formula + velocity bug:** Two separate issues. The loss score formula (`sqrt(-V * K) * 10`) must be documented with rationale or removed. The velocity bonus must be fixed to compute actual 12-month rate of change instead of magnitude.
3. **Impl A3 -- FSP config/code ETI weight divergence:** Config defines 6 series (sum 1.0), code hardcodes 4 series (sum 1.0) with different weights. Ghost entries for debt_service and food_energy_cpi reference nonexistent data.
4. **Spec D2 -- No sensitivity analysis protocol:** 50+ weights, 20+ windows, 10+ thresholds, none empirically derived. Systematic parameter variation framework needed.
5. **Spec D3 -- Uncertainty quantification incomplete:** Bootstrap only varies reference window for PSI (too narrow). K-range dominates PLI. Should be labeled "parameter sensitivity" rather than "model uncertainty."
6. **Impl B1 -- Construct-level overlap claim:** The "zero data overlap" claim is misleading at the construct level. Inter-model correlation analysis needed.
7. **Impl A4 -- WID API untested:** Two inconsistent URLs in wid_loader.py. Test live or switch to CSV-only interface.
8. **Spec D1 / Impl B3 -- Backtesting episodes not tiered:** All 6 historical episodes treated as equal true positives. 1968/2020 (mass mobilization) should not be scored the same as 1979 (pure economic stress).

### Deferred Issues (5)

Issues affecting non-selected models: Spec A3 (RVI constellation bonus), Spec A4 (PITF fabricated coefficients), Spec B3 (Pew trust series discontinuity), Spec C3 (RVI union density scoring), Spec C4 (CSD secular trend detection). These remain documented in the checklist but require no action unless the model selection changes in Phase 2.

See: `validation/math-fix-checklist.md` for the full issue-by-issue accounting.

---

## 3. Data Availability Summary

### Overall Status

| Status | Count | Impact |
|--------|-------|--------|
| ACTIVE | 12 | No issues -- series actively maintained, frequently updated |
| ACTIVE-LAGGED | 3 | Acceptable for structural indicators; lags are inherent to the data |
| CHANGED | 1 | Methodology revision may need documentation and level adjustment |
| DISCONTINUED | 1 | Replacement needed -- highest-priority data issue |
| UNVERIFIED | 1 | API endpoint needs live testing; underlying data available through multiple channels |

### Data Risks by Model

**PSI (risk: LOW-MEDIUM):** All 3 inputs available. The WID series (sptinc992j) needs API verification but the underlying top 1% income share data is accessible through WID.world, Piketty-Saez, and CBO. Labor share (W270RE1A156NBEA) is annual with ~6-9 month lag, acceptable for a structural indicator. Federal debt/GDP (GFDEGDQ188S) is active with no concerns.

**PLI (risk: LOW):** All 5 inputs confirmed available. Two have inherent lags (real median household income ~1 year, life expectancy ~2 years) that are structural and unavoidable. No action required.

**FSP (risk: MEDIUM):** Stage 1 (FSSI) is in good shape, with only a minor methodology note for DRSFRMACBS (mortgage delinquency MBA revision in 2023). Stage 2 (ETI) has the most critical data issue in the entire audit: **CSCICP03USM665S (OECD Consumer Confidence) is discontinued** since January 2024, and it carries the highest ETI weight (0.35 in code). The OECD restructured its Main Economic Indicators program into the Key Short-Term Economic Indicators (KSTEI) framework, and this specific amplitude-adjusted series was not carried forward. Replacement options include the OECD KSTEI replacement series (if published to FRED), dropping the weight and redistributing, or accepting a gap. Using UMCSENT (already in PLI) would violate the project's zero-overlap design.

### Phase 3 Action Items

- **Replace CSCICP03USM665S:** Research OECD KSTEI replacement. If a direct replacement exists on FRED, substitute the series ID. If not, drop and redistribute ETI weight.
- **Verify WID API:** Test both URLs in wid_loader.py. If neither works, document that manual CSV download is required.
- **Confirm W270RE1A156NBEA:** Verify exact latest data point during Phase 3 data pipeline work.
- **Document DRSFRMACBS break:** Note the 2023 methodology revision and consider level adjustment in Phase 4.

See: `validation/data-series-audit.md` for full audit details.

---

## 4. Known Bugs Deferred to Phase 4

| # | Bug | Model | Severity | What Needs to Change |
|---|-----|-------|----------|---------------------|
| 1 | Min-max normalization pins trending series to 1.0 (impl A1) | PSI | CRITICAL | Switch to `percentile_rank_series` (exists in normalization.py:91-119) or z-scores |
| 2 | Undocumented `sqrt(-V*K)*10` formula (spec A2) | PLI | MODERATE | Document rationale for sqrt compression and `*10` multiplier, or revert to spec formula |
| 3 | Velocity bonus computes magnitude, not velocity (impl A2) | PLI | MODERATE | Compute actual 12-month change in each domain's deviation instead of average magnitude |
| 4 | Config/code ETI weight divergence (impl A3) | FSP | MODERATE | Remove ghost entries (debt_service, food_energy_cpi) from config or implement them; single source of truth |
| 5 | Food/energy CPI planned but not implemented (impl C4) | FSP | LOW | Either add CPIUFDSL/CPIENGSL to FRED_SERIES and implement, or remove from config |
| 6 | Config `invert` field defined but never used (impl C2) | All | LOW | Either use the config invert field or remove it |
| 7 | Backtesting treats all episodes as equal severity (impl B3) | All | MODERATE | Assign expected severity tiers to historical episodes |
| 8 | Bootstrap uncertainty too narrow (impl B4) | PSI, PLI | MODERATE | Broaden perturbation beyond reference window for PSI; document as parameter sensitivity |
| 9 | No unit or integration tests (impl C1) | All | MODERATE | tests/ directory contains only empty `__init__.py` |
| 10 | `compute_historical` is O(n^2) (impl C3) | FSP | LOW | Vectorize the rolling z-score computation |
| 11 | PSI model not labeled "PSI-Simple" (impl B2) | PSI | LOW | Add labeling to clarify this is a 3-proxy approximation |
| 12 | WID API URLs inconsistent (impl A4) | PSI | MODERATE | Test both URLs; fix or document CSV-only fallback |

---

## 5. Open Questions for Phase 2 Literature Mining

These questions emerged during the validation process and should inform the scope of literature mining:

1. **Has Turchin published updated PSI operationalizations since *End Times* (2023)?** The simplified 3-proxy approach in the codebase may not reflect Turchin's latest thinking on which variables best capture MMP, EMP, and SFD. Recent publications or working papers may offer better proxy selections or composite formulas.

2. **Are there other applications of prospect theory to aggregate political risk?** The PLI's application of Kahneman-Tversky parameters to political instability is described as novel. Has anyone else attempted this? Are there empirical studies validating loss aversion at the population level for political outcomes?

3. **What is the empirical evidence for financial stress -> political mobilization transmission?** The FSP's causal chain is the most novel theoretical claim. Funke, Schularick & Trebesch (2016) is cited for "Going to Extremes," but what does the broader literature say about lag structures, transmission mechanisms, and the conditions under which financial crises do vs. do not produce political instability?

4. **What alternative data sources exist for the discontinued/unavailable series?** CSCICP03USM665S needs replacement. Are there other consumer confidence or economic sentiment measures available on FRED that would be appropriate for the FSP's ETI stage? What about non-FRED sources that could fill the Stages 3-4 gap (political grievance, mobilization)?

5. **How do other researchers handle the normalization problem for trending macroeconomic series?** The min-max pinning bug in PSI is a common issue in composite indicator construction. What normalization methods are used in comparable political risk indices (e.g., Fragile States Index, Political Instability Task Force models)?

6. **Should Phase 2 explore frameworks beyond these 3 models?** The current selection was made primarily based on the original spec. Are there established political instability frameworks in the literature that were not considered? For example, Goldstone's state failure models, Collier-Hoeffler models of civil conflict, or more recent machine learning approaches to political risk scoring?

7. **What does the sensitivity analysis literature recommend for composite indicators with this many parameters?** The project has 50+ weights, 20+ windows, and 10+ thresholds. Are there established methods (e.g., Sobol indices, Morris screening) that are appropriate for this scale of parameter space?

---

## 6. Readiness Assessment

### What is ready for Phase 2 (Literature Mining):

- Three model frameworks are identified with clear theoretical lineages (Turchin structural-demographic theory, Kahneman-Tversky prospect theory, financial crisis transmission literature)
- Each model has a structured assessment documenting what was confirmed, revised, and flagged
- A complete inventory of 27 critical review issues exists with resolution status
- 18 data series are audited with availability status and model mapping
- Open questions for literature mining are specific and actionable
- The codebase exists with data pipelines, model computations, and infrastructure (normalization, backtesting, uncertainty) -- even if buggy, this provides a concrete implementation to compare against the literature

### What needs resolution before Phase 4 (Model Building):

- Min-max normalization bug in PSI (the single most impactful issue)
- PLI formula clarification (document or remove undocumented sqrt transformation)
- FSP config/code weight divergence (single source of truth)
- CSCICP03USM665S replacement (highest-priority data issue)
- WID API verification (method risk, not data risk)
- Sensitivity analysis framework (50+ parameters, no systematic testing)
- Backtesting episode tiering (not all episodes are equal-severity true positives)

### Honest limitations of this validation:

This validation has important limitations that readers should understand:

1. **No models were run.** All assessments are based on code reading, spec analysis, and logical reasoning. The actual output behavior of the models has not been tested. The normalization bug is identified from code inspection, not from observing it produce wrong outputs.

2. **No data was downloaded.** The data series audit verified availability through FRED website pages and public documentation, not by actually calling the FRED API or WID API. Series that appear active may have undiscovered issues that only surface during actual data retrieval.

3. **No verification against original academic papers.** The assessments compare the code against the spec and the critical reviews, but do not independently verify that the spec faithfully represents Turchin's published PSI formulation, Kahneman-Tversky's prospect theory parameters, or the financial crisis literature's transmission mechanisms. Phase 2 literature mining should close this gap.

4. **No empirical backtesting.** The assessments identify issues with the backtesting framework (episode tiering, sensitivity analysis) but do not actually backtest the models against historical episodes. Whether the models would have flagged 1968, 2008, or 2020 remains unknown.

5. **Single-reviewer assessment.** This validation was conducted by a single automated agent reviewing code and documents. There was no peer review, no domain expert consultation, and no adversarial testing.

---

## Appendix: Document Map

| Document | Location | What It Contains | When to Read It |
|----------|----------|------------------|-----------------|
| model-specifications.md | repo root | Full 6-model specs (~1200 lines) with mathematical formulations, data requirements, and implementation guidance | Only if you need original spec details beyond what the model assessments cover |
| critical-review-model-specs.md | repo root | 15 spec-level issues (A1-D3) with severity ratings and recommended fixes | If you need the full issue context, not just the checklist summary |
| critical-review-implementation.md | revolution-index/ | 12 code-level issues (A1-C4) with file:line citations | If you need implementation bug details beyond what model assessments describe |
| gap-analysis-literature-review.md | repo root | Literature review gaps and research directions | If you need background on what academic literature was consulted |
| revolution-metrics-data-sources.md | repo root | Detailed data source documentation for all 18+ series | If you need original data source research beyond the audit |
| validation/model-assessment-turchin-psi.md | validation/ | Full PSI assessment: component review, fix status, verdict | For detailed PSI findings including code-level citations |
| validation/model-assessment-prospect-theory-pli.md | validation/ | Full PLI assessment: component review, fix status, verdict | For detailed PLI findings including undocumented formula analysis |
| validation/model-assessment-financial-stress-pathway.md | validation/ | Full FSP assessment: component review, fix status, verdict | For detailed FSP findings including config/code divergence |
| validation/math-fix-checklist.md | validation/ | All 27 issues tracked: ID, severity, model, status, cross-references | For fix-by-fix status accounting |
| validation/data-series-audit.md | validation/ | 18 series verified: status, frequency, latest data, detailed notes for 6 concerning series | For series-specific availability details and replacement recommendations |
