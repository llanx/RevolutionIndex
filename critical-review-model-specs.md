# Critical Review: Model Specifications
## Peer Review — As If a Colleague Presented This to Us

**Reviewer's summary:** This is ambitious, well-researched work with strong theoretical grounding and genuinely useful architectural ideas. The three-tier ensemble structure (structural / behavioral / systemic) is well-conceived, and the Financial Stress Pathway's lag structure is a real contribution. However, the specifications have serious mathematical issues, data pipeline problems, and undisclosed researcher degrees of freedom that would compromise implementation. The document needs to be honest about what is a principled formula versus what is a number someone made up.

Below is a systematic critique organized by severity.

---

## CATEGORY A: MATHEMATICAL ERRORS AND FORMULA PROBLEMS

These need to be fixed before implementation or the outputs will be misleading.

---

### A1. The PSI Multiplication Crushes Mid-Range Values (Severity: HIGH)

**The problem:**

When three percentile-normalized values (0 to 1) are multiplied, the result is dramatically compressed toward zero. This is a basic arithmetic property that the spec doesn't address.

Example: Suppose all three components are moderately elevated — each at their 70th historical percentile:

```
PSI = 0.70 × 0.70 × 0.70 = 0.343 → displays as 34.3 on 0-100 scale
```

That puts three simultaneously-elevated-to-70th-percentile conditions into the "moderate pressure" bucket (10-25 label). Three conditions at their 80th percentile:

```
PSI = 0.80 × 0.80 × 0.80 = 0.512 → displays as 51.2
```

Even with all three components at their *80th historical percentile*, you barely reach "elevated." You'd need all three at ~90th percentile (0.729 × 100 = 72.9) to hit "high pressure."

**Why this matters:** The multiplicative structure is theoretically motivated (Turchin), but the percentile normalization before multiplication means the product is always much lower than any individual component. The interpretation scale (0-10 = "low," 75-100 = "crisis") was clearly written assuming the output distributes across the full range, but the actual distribution is heavily concentrated in the 0-40 range.

**What to do:** Either:
- (a) Take the geometric mean instead of the product: `PSI = (MMP × EMP × SFD)^(1/3)`. Three 0.70s → 0.70. This preserves the multiplicative interaction (if any factor is zero, the whole thing is zero) while keeping the output in a human-readable range.
- (b) Recalibrate the interpretation scale to the actual output distribution.
- (c) Use a different transformation: `PSI = 1 - (1-MMP)(1-EMP)(1-SFD)`. This is the "probability union" form — it yields 0.973 when all three are at 0.70. Arguably better theoretical fit: "the probability that at *least one* pressure channel is active."

**Assessment: Must fix.** The current formula produces outputs that systematically understate the combination of moderate pressures, which is exactly the scenario the model should detect.

---

### A2. The PLI Scaling Is Broken — Output Clusters at 0 or 100 (Severity: HIGH)

**The problem:**

Walk through the Prospect Theory model's math with realistic numbers.

Take Domain 1 (Wages): if median income is ~5% below its 10-year peak (a moderate recession):
```
deviation = -0.05
V = -2.25 × |−0.05|^0.88 = -2.25 × 0.0631 = -0.142
loss_score = min(100, max(0, 0.142 × 500)) = min(100, 71) = 71
```

That's already 71/100 for a single domain with a *modest* 5% decline. Now if 6 out of 8 domains are in loss territory (a normal recession scenario):

```
mean_loss_score ≈ 50 (averaging some high, some low)
breadth_multiplier = 1 + 0.1 × (6-1)^1.5 = 1 + 0.1 × 11.18 = 2.12
velocity_multiplier ≈ 1.3 (moderate deterioration)
raw_PLI = 50 × 2.12 × 1.3 = 137.8
PLI = min(100, 137.8) = 100
```

The model hits the 100 ceiling during any ordinary recession. The multipliers (up to 2.81 × 2.0 = 5.62x) mean that once average loss scores exceed ~18, the model saturates at 100 with all 8 domains in loss.

Conversely, in good times when most domains are at their 10-year peak (deviation ≈ 0), every loss score is 0 and PLI = 0.

**Result:** The PLI effectively functions as a binary indicator (good times ≈ 0; any recession ≈ 100), not a graduated 0-100 scale. It has no ability to distinguish between a mild recession and a depression.

**What to do:**
- The K constants are too large. They need to be reduced by roughly 5-10x, or the loss_score step needs a concavity function (e.g., sqrt or log) to compress high values before the multipliers amplify them.
- Alternatively, apply the breadth and velocity multipliers as additions rather than multiplications: `PLI = mean_loss + breadth_bonus + velocity_bonus` with defined cap values.
- Run the formulas against historical data (2008-2009, 2020, 1990s prosperity) before publishing them. This would have caught the saturation immediately.

**Assessment: Must fix.** A model that reads 0 in good times and 100 in bad times with nothing in between is a thermometer with only two readings.

---

### A3. The RVI Constellation Bonus Values Are Arbitrary (Severity: MODERATE)

**The problem:**

The constellation bonus (0, 5, 12, 22, 35) for 1-5 elevated sub-indices is presented as if it follows a logic, but the numbers are not derived from any formula or theoretical principle. Why 12 and not 10? Why 22 and not 20? Why 35 and not 30?

If the intent is a non-linear penalty, specify the generating function:
```
constellation_bonus = a × (n_elevated - 1)^b
```
...and explain the choice of a and b. If the intent is ad hoc, say so — but then acknowledge this is a tunable parameter that should be tested via sensitivity analysis.

The same critique applies to the 0.15 coefficient on `max(interaction terms)` and the threshold of 60 for "elevated." All three are ungrounded.

**What to do:** Either derive these from a principle, or explicitly label them as tunable hyperparameters and specify a sensitivity analysis protocol.

---

### A4. The PITF Coefficients Are Fiction (Severity: HIGH)

**The problem:**

The spec says:

> PITF_logit = -3.5 + 0.035 × V1 + 0.020 × V2 + 0.010 × V3 + 0.025 × V4

Then notes: "The coefficients above are illustrative adaptations — they preserve the *relative ordering* of the original model."

This is not an adaptation of the PITF model. It's a new weighted index dressed in logistic regression notation. The original PITF model's power came from *empirically estimated* coefficients on a large sample. These coefficients are made up. Running them through a logistic function to produce a "probability" gives a false sense of statistical rigor.

The problem gets worse: the input variables (V1-V4) are themselves composites of sub-variables with their own made-up weights, which are then fed through a logistic function with made-up coefficients. There are about 20 researcher degrees of freedom between the raw data and the output, none of them empirically constrained.

**What to do:**
- Option 1: Be honest. Call this "a weighted index inspired by the PITF variable selection" and drop the logistic regression framing. Present it as a composite score, not a probability.
- Option 2: Use the actual PITF coefficients. They were published in the 2010 AJPS paper. Apply them to the original variables (Polity score categories, infant mortality quartiles, neighbor conflict binary, discrimination binary) without adaptation. Accept that the output will read "low risk" for the U.S. most of the time — that's an honest result.
- Option 3: Estimate new coefficients by running the adapted variables against a cross-national sample of instability events. This is a substantial empirical project but would produce defensible coefficients.

**Assessment: Must fix before this model is presented to anyone externally.** A logistic regression with made-up coefficients is worse than a simple weighted average because it falsely implies statistical estimation.

---

## CATEGORY B: DATA PIPELINE AND TEMPORAL ALIGNMENT PROBLEMS

These are implementation-level issues that will cause problems when building the actual system.

---

### B1. Mixing Data Frequencies Without an Interpolation Strategy (Severity: HIGH)

**The problem:**

The ensemble combines:
- Daily data (VIX, OFR FSI, yield curve)
- Weekly data (initial claims)
- Monthly data (unemployment, CPI, consumer sentiment)
- Quarterly data (GDP, debt/GDP, household debt)
- Annual data (Gini, V-Dem, infant mortality, trust surveys)
- Biennial data (ANES, GSS, YRBS)
- Triennial data (Survey of Consumer Finances)
- Per-election-cycle data (anti-system vote share, candidate counts)
- Per-birth-cohort data (Opportunity Insights mobility)

The spec says the ensemble should update *monthly* and that annual data should be "interpolated." But no interpolation method is specified. Linear interpolation of the Gini coefficient between annual readings creates phantom precision — it implies the Gini changed smoothly and predictably throughout the year, which is false.

The Opportunity Insights mobility data (Domain 6 in PT-PRM) updates *by birth cohort* — the latest cohort is roughly those born in 1990. This isn't a time series that updates; it's a completed historical dataset. Using it in a monthly-updating model is conceptually incoherent.

**What to do:**
- Specify the interpolation method for each frequency class (step function / last observation carried forward is more honest than linear interpolation for most of these)
- Acknowledge that "monthly" updates really means "monthly for the fast-moving components; whenever new data drops for the slow ones"
- Replace Domain 6 (Opportunity Insights cohort data) with a proxy that actually updates (e.g., age-specific real income ratios from CPS)
- Align each model's update frequency to its *slowest critical input*, not its fastest

---

### B2. Historical Distribution Lengths Are Wildly Inconsistent (Severity: MODERATE)

**The problem:**

Percentile normalization `P(x_t | history)` is used everywhere, but "history" means different things for different variables:
- Top 1% income share: 1913-present (113 years)
- Consumer sentiment: 1952-present (74 years)
- Gini: 1967-present (59 years)
- ACLED protest data: 2020-present (6 years)
- V-Dem LDI: 1789-present (237 years)
- Fed DFA wealth shares: 1989-present (37 years)
- Mapping Police Violence: 2013-present (13 years)

A percentile rank against a 237-year distribution means something completely different from a percentile rank against a 6-year distribution. The protest count percentile (based on 6 years of data) has enormous sampling uncertainty compared to the income share percentile (based on 113 years).

**What to do:**
- Set a minimum history length for percentile computation (e.g., 30 years). Variables with shorter histories should use z-scores against available data with explicit uncertainty flags.
- Or use a common reference window for all variables (e.g., 1970-present) and exclude variables that don't go back that far from percentile-based computations.
- Report confidence bands that reflect the length of the underlying series.

---

### B3. The Pew Trust Series Is Not a Continuous Time Series (Severity: MODERATE)

**The problem:**

The spec treats Pew's "trust in government" as a ~quarterly time series from 1958-present. In reality:
- 1958-2000: The question was asked by the ANES (biennial) and by Pew/Gallup occasionally
- The *exact wording* has changed multiple times
- Polling methodology shifted (phone → online panels → mixed mode)
- The 1958 starting value (~73%) and the 2024 value (~22%) are not measured by the same instrument

This variable appears in the Turchin PSI (SFD trust modifier), the Prospect Theory model (Domain 8), and the Expanded RVI (LSI). A methodological artifact in this one series propagates across three models.

**What to do:**
- Use the ANES cumulative file for the consistent long time series (biennial, 1958-present, consistent question wording)
- Supplement with Pew for inter-ANES years, but note the measurement inconsistency
- Consider using Gallup "confidence in Congress" instead — it's been consistently administered annually since 1973 with stable methodology
- Do NOT treat this as a quarterly series; it is at best biennial with intermittent supplements

---

### B4. No Missing Data Strategy (Severity: MODERATE)

**The problem:**

What happens when:
- The government shutdown delays BLS data releases?
- The SCF hasn't been updated in 2 years (it's triennial)?
- ANES skips a cycle or changes methodology?
- ACLED changes its U.S. coding rules (as it did in 2021)?
- Pew doesn't publish a trust number for 8 months?
- The CDC is slow to release final mortality data (as it was for 2021-2022)?

No imputation, carry-forward, or graceful degradation strategy is specified. In practice, at any given time, some fraction of the input data will be stale or missing.

**What to do:**
- Specify a "data freshness" indicator for each input: how old can the most recent observation be before the variable is flagged as stale?
- Define imputation rules: carry-forward, model-based imputation, or exclude from aggregation?
- Weight variables in part by recency: fresh data gets more weight than stale data
- Design each model to produce valid output even when some inputs are missing (graceful degradation)

---

## CATEGORY C: THEORETICAL AND CONCEPTUAL PROBLEMS

---

### C1. Massive Metric Overlap / Double-Counting (Severity: HIGH)

**The problem:**

The same underlying phenomena appear in multiple models simultaneously:

- **Government trust** appears in: Turchin PSI (SFD trust modifier), Prospect Theory (Domain 8), Expanded RVI (LSI: L1, L2, L9), and feeds into the PITF (indirectly through governance quality)
- **Income inequality / top 1% share** appears in: Turchin PSI (EMP wealth pump), Expanded RVI (EPI: E1, E2), and FS-PIP (Stage 2 modifier)
- **Unemployment / employment** appears in: Turchin PSI (MMP via relative wages), Prospect Theory (Domain 4), Expanded RVI (EPI: E3), FS-PIP (Stage 2: unemp_delta, claims)
- **Housing affordability** appears in: Prospect Theory (Domain 2), Expanded RVI (EPI: E4), FS-PIP (Stage 1: mortgage_delinq; Stage 2 implicitly)
- **Protest activity** appears in: Expanded RVI (MPI: M1), FS-PIP (Stage 4: protest_count, protest_size)
- **Consumer sentiment** appears in: Prospect Theory (Domain 7), FS-PIP (Stage 2: consumer_conf)
- **Life expectancy** appears in: Prospect Theory (Domain 3), PITF (V2: life_expect), Expanded RVI (DSI: D5 indirectly via deaths of despair)
- **Democracy scores** appear in: Prospect Theory (Domain 5), PITF (V1: polity, vdem, fh_score), Expanded RVI (LSI: L5, L6), and CSD (TS6: partisan distance)

When the ensemble combines model outputs using `0.45 × structural + 0.35 × behavioral + 0.20 × systemic`, these shared inputs get multiplied through. A decline in government trust hits the Turchin PSI, the Prospect Theory model, and the Expanded RVI simultaneously — appearing in all three with different weights and transformations, then getting combined again at the ensemble level. The effective weight of "government trust" in the final score is much higher than any single model's specification suggests.

**Why this matters:** The ensemble appears to combine "independent" models, but the models are correlated because they share inputs. This means:
1. The effective sample size for any given signal is much smaller than 6 models
2. A single data error or methodological artifact propagates everywhere
3. The ensemble's uncertainty is much larger than naively assumed

**What to do:**
- Map every raw data series to every model that uses it. Produce a "data dependency matrix" showing the overlap.
- Consider whether the ensemble truly needs 6 models or whether 3 genuinely orthogonal models would produce better signal.
- At minimum, report the correlation between model outputs. If Turchin PSI and Expanded RVI are r > 0.85, they're not providing independent information.

---

### C2. The FS-PIP Lag Structure Is Based on Three Data Points (Severity: MODERATE)

**The problem:**

The lag calibration table shows three episodes: 2008 (36 months), 2001 (disrupted), 2020 (10 months). Setting aside 2001 (which the spec itself flags as disrupted by the 9/11 rally effect), that's two usable data points with a 26-month range.

The "expected lag" of 3-12 months (Stage 1 → Stage 2) and the forward projection logic ("projected ETI peak: t + 6 months") are presented with a confidence that two data points cannot support. The 2020 case compressed all stages into ~10 months because a pandemic simultaneously delivered financial stress, economic pain, political grievance, and a mobilization trigger (George Floyd) — the stages didn't cascade sequentially. It's not really a validation of the lag model; it's a case where the model's core assumption (sequential causation) was violated.

**What to do:**
- Be honest about N=2. Present the lags as "rough empirical guidance" rather than calibrated parameters.
- Add more episodes: 1970s stagflation → 1978-80 unrest; 1990-91 recession → 1992 LA riots/Perot; dot-com bust → Iraq war protests. These are noisier but expand the sample.
- Consider whether the lag structure should be variable-dependent (financial → unemployment has a well-studied 3-6 month lag in macro literature; unemployment → political grievance is much less studied)
- The forward projection feature should report uncertainty bands, not point estimates

---

### C3. Union Density Scoring Is Incoherent (Severity: LOW)

**The problem:**

The MPI scores union density as "higher = more mobilization capacity = more risk." But union density in the U.S. has declined from ~27% (1970) to ~10% (2024). That monotonic decline means the percentile score is at its *historical minimum* today. So the model says "mobilization capacity from organized labor is at its lowest point ever."

The spec then tries to fix this with: `M5_adjusted = max(score_M5, score_M3 × 0.5)` — flooring union capacity at half the social media score. But this is an ad hoc fix that conflates two fundamentally different mobilization mechanisms (organized labor bargaining vs. social media coordination).

The deeper issue: is declining union density stabilizing (less organized pressure capacity) or destabilizing (workers have no institutional channel for grievances, so they turn to populism and street protest)? The literature supports both interpretations. The spec chooses one and patches around the other.

**What to do:**
- Either pick a direction and justify it, or create two sub-variables: "institutional mobilization capacity" (union density, nonprofit density — lower = less organized capacity) and "decentralized mobilization capacity" (social media penetration, smartphone access — higher = more flash-mob potential). These capture different things and shouldn't be forced into one variable.

---

### C4. The CSD Model May Be Detecting Secular Trends, Not Tipping Points (Severity: MODERATE)

**The problem:**

Many of the CSD input time series exhibit long-term secular trends:
- Trust in government: downward trend since 1960s
- Income inequality: upward trend since 1970s
- Partisan distance: upward trend since 1970s
- Labor share: downward trend since 1970s
- Life expectancy: upward trend for decades, then COVID disruption

Rolling variance and rolling autocorrelation will *naturally* increase in a trending time series even if the system is nowhere near a tipping point. A series that moves steadily from 70% to 22% over 60 years will show high autocorrelation (because each year is close to the previous year — the trend ensures this) and potentially increasing variance (if the rate of decline fluctuates).

The spec acknowledges this in section 6.7 ("detrending before analysis may be needed") but doesn't specify how. This is not a minor caveat — it's a fundamental methodological choice that determines whether the CSD model detects genuine fragility or just measures the slope of already-known trends.

**What to do:**
- Detrend all input series before CSD analysis. Use first-differencing (simplest) or a regression-based detrend (e.g., remove linear or quadratic trend, analyze residuals).
- Run CSD on both raw and detrended series and report both. If CSD signals disappear after detrending, they were artifacts of the trend, not indicators of approaching tipping points.
- Be explicit: "CSD on raw series detects loss of resilience including from secular deterioration. CSD on detrended series detects loss of resilience *beyond* the trend."

---

## CATEGORY D: MISSING SPECIFICATIONS

Things the document should include but doesn't.

---

### D1. No Backtesting Protocol (Severity: HIGH)

The entire spec describes forward-looking formulas but never specifies how to validate them against historical episodes. A backtesting protocol should define:
- Which historical episodes constitute "true positives" (1968, 2011 Occupy, 2020 BLM/Jan 6, etc.)?
- What score level would constitute a "correct prediction"?
- What is the false positive tolerance? (A model that reads "high risk" for 30 consecutive years but only sees 3 instability events has a 90% false positive rate)
- How do you evaluate a model predicting a *structural* rare event that may not have occurred in the validation window?

Without a backtesting protocol, there's no way to know if any of these models work.

---

### D2. No Sensitivity Analysis Protocol (Severity: HIGH)

The specifications contain approximately:
- 50+ weight parameters (intra-model and inter-model)
- 20+ normalization window choices
- 10+ threshold values
- 6 model combination weights

None of these are empirically derived. A sensitivity analysis should systematically vary these parameters and report how much the output changes. If the composite RVI swings by 20 points when you change one weight by 0.05, that weight is a critical parameter that needs empirical grounding. If it barely changes, the precise value doesn't matter and the spec is overthinking it.

---

### D3. No Uncertainty Quantification (Severity: HIGH)

Every model produces a point estimate (a single number on 0-100). None produce confidence intervals. Given that:
- Every input metric has measurement error
- Many inputs are survey-based with known sampling uncertainty
- Percentile normalization is sensitive to the historical reference period
- Multiple hand-tuned parameters could be set differently

...the models should produce output with uncertainty bands. A responsible output is "PSI = 45 (95% CI: 32-58)" not just "PSI = 45." Without uncertainty bands, small movements in the score (e.g., 52 to 56) appear meaningful when they may be within measurement noise.

---

### D4. No Structural Break Handling (Severity: MODERATE)

The world changed fundamentally around 2008 (social media), 2016 (algorithmic amplification), and 2020 (pandemic restructuring). Historical distributions computed from 1950-present include a world that no longer exists. The percentile rank of a protest count in 2025 computed against a 1950-2025 distribution is meaningless if the protest measurement infrastructure didn't exist before 2017.

Specify whether to use:
- Full history (more statistical power but includes irrelevant eras)
- Post-structural-break history only (more relevant but much shorter)
- Regime-switching models that formally account for structural breaks

---

## CATEGORY E: WHAT'S ACTUALLY STRONG

Not everything is wrong. The following elements are well-designed and should survive revision.

---

### E1. The Three-Tier Architecture Is Good

Separating structural pressure (Turchin, RVI, PITF), behavioral perception (Prospect Theory, Financial Stress Pathway), and systemic fragility (CSD) is a genuinely useful conceptual framework. These capture different things and should be expected to diverge at important moments.

### E2. The Financial Stress Pathway's Causal Chain Is the Most Novel Contribution

Modeling the *temporal sequence* from financial shock → economic pain → political grievance → mobilization is the strongest original idea in the document. The 2008-2021 case study makes it backtestable. Even with only N=2-3 calibration episodes, the staged model provides something no other framework offers: a forward-looking projection based on where in the causal chain the system currently sits.

### E3. The Prospect Theory Application Is Theoretically Sound

Applying loss aversion asymmetry, reference point dependence, and diminishing sensitivity to political instability is a legitimate theoretical contribution. The J-Curve detection logic is clever. The scaling and multipliers need fixing, but the underlying framework is solid.

### E4. The Divergence Alerts Are a Smart Meta-Feature

The idea that "when structural models and behavioral models disagree, the disagreement itself is informative" is genuinely useful. A structural-behavioral divergence flag ("structural pressure high but not yet perceived") could provide early warning. A behavioral-structural divergence ("public distress exceeds structural conditions") could indicate information-environment-driven instability.

### E5. The Simplified Alternatives Are Potentially Better Than the Complex Versions

The "Alternative MMP (simplified): use labor share of GDP alone" option may actually outperform the complex MMP formula, because it has fewer researcher degrees of freedom and avoids the urbanization constant-multiplier problem. The document should consider whether the simple versions are the *primary* specification, not the fallback.

### E6. The Honest Calibration Limitations Appendix Is Rare and Valuable

Most frameworks in this space don't acknowledge that they're operating without calibration data for their target context. The appendix that says "no wealthy democracy has crossed a political tipping point in the modern data era, so there is no calibration case" is refreshingly honest and should be preserved prominently.

---

## SUMMARY: PRIORITY FIXES

| Priority | Issue | Fix |
|---|---|---|
| **MUST FIX** | PSI multiplication crushes mid-range | Switch to geometric mean or probability union form |
| **MUST FIX** | PLI saturates at 100 in any recession | Reduce K constants by 5-10x; test against historical episodes |
| **MUST FIX** | PITF coefficients are fiction | Drop logistic framing or use actual published coefficients |
| **MUST FIX** | No backtesting protocol | Define historical true positives, false positive tolerance, evaluation metrics |
| **MUST FIX** | No sensitivity analysis protocol | Specify systematic parameter variation and output stability testing |
| **MUST FIX** | No uncertainty quantification | Add confidence intervals to all model outputs |
| **SHOULD FIX** | Massive metric overlap across models | Build data dependency matrix; measure inter-model correlation |
| **SHOULD FIX** | Inconsistent historical distribution lengths | Set minimum history; use common reference period |
| **SHOULD FIX** | No interpolation / missing data strategy | Specify LOCF, imputation, and data freshness rules |
| **SHOULD FIX** | CSD detecting trends not tipping points | Detrend input series; report both raw and detrended CSD |
| **SHOULD FIX** | Constellation bonus values are arbitrary | Derive from formula or label as tunable hyperparameters |
| **SHOULD FIX** | FS-PIP lag calibrated on N=2 | Add more episodes; report as guidance not parameters |
| **NICE TO FIX** | Union density scoring is incoherent | Split into institutional vs. decentralized mobilization |
| **NICE TO FIX** | Pew trust is not a continuous series | Use ANES cumulative for consistency; supplement with Pew |
| **NICE TO FIX** | Urbanization in MMP is a constant | Remove or replace with a variable that actually varies |

---

## OVERALL ASSESSMENT

**Grade: B- (Strong framework, weak execution)**

The architecture, data source identification, and theoretical grounding are genuinely strong — better than most work in this space. The three-tier ensemble design, the Financial Stress Pathway, and the Prospect Theory application are real contributions.

But the mathematical formulas haven't been tested against actual data, and it shows. The PSI compression, PLI saturation, PITF fake coefficients, and absent validation protocols would be caught immediately by running the formulas against even one historical episode. The spec reads like it was designed conceptually rather than computationally — the formulas *describe* the right ideas but don't *produce* the right numbers.

**Recommended next step:** Before refining any model further, implement the simplest version of each (using the "Alternative/Simplified" options) against historical U.S. data from 1970-present. Plot the outputs. See what they look like. Identify which models produce meaningful variation versus which flatline or saturate. *Then* iterate on the specifications with empirical feedback. The theoretical work is done; it's time to get into the data.
