# Model Assessment: Prospect Theory Perceived Loss Index (PLI)

## 1. Theoretical Basis

**What the spec claims the model measures:**
The Perceived Loss Index (PLI) applies Kahneman and Tversky's prospect theory to measure perceived losses across multiple life domains relative to recent peaks (model-specifications.md, sections 2.1-2.6). The core behavioral insights applied:

1. **Reference point dependence:** People evaluate conditions relative to what they recently experienced, not in absolute terms. A decline from $60k to $50k is perceived as worse than always being at $50k.
2. **Loss aversion:** Losses hurt ~2.25x more than equivalent gains feel good (lambda = 2.25).
3. **Diminishing sensitivity:** The 10th unit of loss hurts less than the 1st (alpha = 0.88).
4. **Breadth compounding:** Simultaneous losses across multiple domains compound perceived crisis ("everything is falling apart").
5. **J-Curve detection:** Improvement followed by sharp reversal maximizes perceived loss (Davies hypothesis).

**Source academic work:**
- Kahneman & Tversky (1979), "Prospect Theory: An Analysis of Decision under Risk" (original formulation)
- Tversky & Kahneman (1992), "Advances in Prospect Theory: Cumulative Representation of Uncertainty" (lambda = 2.25, alpha = 0.88 parameter estimates)
- Davies (1962), "Toward a Theory of Revolution" (J-Curve theory)

**Faithfulness of adaptation:**
The value function application is theoretically sound. Using the empirically-estimated parameters (lambda = 2.25, alpha = 0.88) from Tversky & Kahneman (1992) is appropriate. The 10-year trailing peak as the reference point is a reasonable operationalization of "what people remember as normal." The critical review E3 specifically praises this as a "legitimate theoretical contribution."

The adaptation from individual decision-making (the original prospect theory context) to aggregate political risk is a novel application. There is no established academic precedent for using prospect theory parameters to score political instability, so the K constants (domain-specific scaling) are necessarily ad hoc calibrations rather than empirically derived values.

---

## 2. Component Review

### Domain Selection: 5 of 8 Domains

**Spec definition (model-specifications.md, section 2.2):**
The spec defines 8 domains: Wages, Housing, Health, Employment, Democracy, Mobility, Security/Sentiment, Trust.

**Code implementation (prospect_theory.py:36-57):**
Uses 5 domains, dropping Democracy, Mobility, and Trust:
1. Wages: MEHOINUSA672N (real median household income)
2. Housing: FIXHAI (housing affordability index)
3. Health: SPDYNLE00INUSA (life expectancy at birth)
4. Employment: LNS12300060 (prime-age employment-population ratio)
5. Security: UMCSENT (University of Michigan consumer sentiment)

**Assessment of domain reduction:** Well-reasoned. The three dropped domains lack freely-available, regularly-updated FRED data:
- Democracy (V-Dem): requires non-FRED download; annual with significant lag
- Mobility (Opportunity Insights): updates by birth cohort, not time series (critical review B1 flagged this as "conceptually incoherent" for a monthly-updating model)
- Trust (Pew): not a continuous time series; methodology changes over time (critical review B3)

The remaining 5 domains all have FRED series with regular updates. The reduction from 8 to 5 domains also changes the breadth bonus dynamics (maximum breadth is 5 instead of 8).

### Value Function Implementation

**Spec definition (model-specifications.md, section 2.3, Steps 1-4):**
```
deviation = (current - reference) / reference
If deviation < 0 (LOSS): V = -lambda x |deviation|^alpha
loss_score = min(100, max(0, -V x K))
```

**Code implementation (prospect_theory.py:96-146):**
```python
# Reference point (lines 103-111)
reference = window.max()  # for higher_is_better domains

# Deviation (lines 117-120)
deviation = (current - reference) / abs(reference)

# Value function (lines 126-131)
V = -self.lambda_ * (abs_dev ** self.alpha)
K = self.domain_K.get(domain_name, 10.0)
loss_score = min(100.0, max(0.0, np.sqrt(-V * K) * 10))
```

**Differences from spec:**
The code adds a `sqrt()` compression on the loss score (line 131) that is NOT in the original spec formula. The spec says `loss_score = -V x K`, but the code computes `sqrt(-V x K) * 10`. This is a two-part modification:

1. **sqrt compression:** Compresses high values, reducing saturation. This addresses the critical review A2 concern about saturation, but goes beyond the review's specific recommendation.
2. **`* 10` multiplier:** Undocumented in both the spec and the critical review. This rescales the sqrt output to produce values in a useful range.

**Known issues:**

(a) **Spec-level:** The original K constants (K=500 for wages, K=100 for housing, etc.) caused the model to saturate at 100 during any ordinary recession (critical review A2). The PLI effectively functioned as a binary indicator (0 in good times, 100 in bad times).

(b) **Fix-level:** The critical review recommended reducing K by 5-10x and/or using additive bonuses instead of multiplicative. The codebase applies both: K/10 in config.py AND sqrt compression AND additive bonuses. The concern (from 01-RESEARCH.md) is that this triple correction may overcorrect, causing the model to *underreport* losses. This is an empirical question that requires backtesting in Phase 4.

(c) **Code-level:** The `sqrt(-V * K) * 10` formula is undocumented. A developer reading the spec would expect `-V * K`, and a developer reading the critical review would expect `-V * K/10` or similar. The actual formula applies sqrt compression AND a 10x multiplier that appear nowhere in either document.

### K Constants

**Spec values (model-specifications.md, section 2.3, Step 4):**
| Domain | Original K |
|--------|-----------|
| Wages | 500 |
| Housing | 100 |
| Health | 1500 |
| Employment | 35 |
| Security | 10 |

**Config values (config.py:188-194):**
| Domain | Implemented K | Reduction Factor |
|--------|--------------|-----------------|
| Wages | 50.0 | 10x |
| Housing | 10.0 | 10x |
| Health | 150.0 | 10x |
| Employment | 3.5 | 10x |
| Security | 1.0 | 10x |

All K constants are reduced by exactly 10x, consistent with the critical review A2 recommendation. The reduction is uniform across all domains, which preserves the relative weighting between domains.

### Breadth Bonus

**Spec definition (model-specifications.md, section 2.3, Step 5):**
Multiplicative breadth multiplier: `breadth_multiplier = 1 + 0.1 x (n_losses - 1)^1.5`
Applied as: `raw_PLI = mean_loss x breadth_multiplier x velocity_multiplier`

**Code implementation (prospect_theory.py:176-179):**
Additive breadth bonus: `breadth_bonus = min(max_breadth_bonus, max(0, (n_losses - 1) * (max_breadth_bonus / (len(DOMAINS) - 1))))`
Applied as: `pli = mean_loss + breadth_bonus + velocity_bonus` (line 188)

**Difference:** Changed from multiplicative to additive, per critical review A2 recommendation. The additive approach prevents the runaway amplification that caused saturation in the original formula. The maximum breadth bonus is 20.0 (config.py:195), applied linearly based on number of domains in loss.

### Velocity Bonus

**Spec definition (model-specifications.md, section 2.3, Step 6):**
Velocity is the *rate of change* of losses -- the 12-month change in deviation:
```
velocity_d,t = -(deviation_d,t - deviation_d,t-12) / 12
```
Applied as a multiplicative factor: `velocity_multiplier = 1 + min(1.0, mean_velocity x 20)`

**Code implementation (prospect_theory.py:182-185):**
```python
avg_loss_magnitude = np.mean([abs(d) for d in deviations.values() if d < 0])
velocity_bonus = min(self.max_velocity_bonus, max(0.0, avg_loss_magnitude * 100))
```

**Critical issue (implementation review A2):** This computes the *magnitude* of current losses, not their *velocity* (rate of change). A domain that fell 10% a decade ago and has been flat since gets the same "velocity bonus" as one that fell 10% last month. The code comment at line 182-183 acknowledges this: "For single-date computation, use deviation magnitude as proxy." But single-date computation is the only mode -- `compute_historical` calls `compute` for each date, so the proxy is permanent.

The velocity bonus changed from multiplicative to additive (per critical review A2), which is correct. But the underlying metric is wrong -- it measures loss magnitude redundantly rather than acceleration.

### PLI Aggregation

**Spec definition:** `raw_PLI = mean_loss x breadth_multiplier x velocity_multiplier` (multiplicative)
**Code implementation (line 188):** `pli = mean_loss + breadth_bonus + velocity_bonus` (additive)

The change to additive aggregation (critical review A2 fix) is correctly applied.

---

## 3. Mathematical Fix Status

### Critical Review A2: PLI Scaling Broken -- Output Clusters at 0 or 100

- **Issue:** Original K constants too large; multiplicative breadth/velocity amplifiers cause saturation at 100 during any recession.
- **Recommended fix:** Reduce K by 5-10x; change multipliers to additive bonuses.
- **Applied in code:** YES (partially, with additions)
  - K constants divided by 10: config.py:188-194
  - Breadth bonus changed to additive: prospect_theory.py:176-179
  - Velocity bonus changed to additive: prospect_theory.py:188
  - Additional sqrt compression added: prospect_theory.py:131 (beyond critical review scope)
  - Additional `* 10` multiplier added: prospect_theory.py:131 (undocumented)
- **Application correct:** PARTIAL -- the K/10 and additive changes are correct per the review. The sqrt compression and `* 10` multiplier are undocumented additions that may or may not be appropriate. Whether the combined effect (K/10 + sqrt + additive) properly calibrates the output range is an empirical question requiring backtesting.
- **New issues introduced:**
  1. sqrt + K/10 may double-correct, causing underreporting (01-RESEARCH.md)
  2. The `* 10` multiplier at line 131 is undocumented
  3. The velocity bonus measures magnitude, not velocity (separate bug, implementation review A2)
- **Status:** APPLIED-BUGGY (core fix applied but with undocumented modifications and a velocity bug)

### Implementation Review A2: Velocity Bonus Is Magnitude, Not Velocity

- **Issue:** Code computes average deviation magnitude, not rate of change. The velocity bonus is redundant with loss magnitude.
- **Recommended fix:** Compute actual 12-month change in each domain's deviation.
- **Applied in code:** NO -- the code still uses magnitude as a proxy (prospect_theory.py:184)
- **Status:** NOT-APPLIED (deferred to Phase 4)

### Critical Review B1: Mixing Data Frequencies Without Interpolation Strategy

- **Issue:** PLI domains mix monthly (housing, employment, sentiment), annual (wages, health), and other frequencies.
- **Relevant fix:** LOCF (Last Observation Carried Forward) is implemented in the data pipeline.
- **Applied in code:** YES -- the data pipeline uses LOCF for frequency alignment.
- **Status:** APPLIED-CORRECT

### Critical Review B2: Inconsistent Historical Distribution Lengths

- **Issue:** Different domains have different history lengths (sentiment: 1952+, housing: 1971+, health: 1960+).
- **Relevant fix:** 10-year trailing window for reference point.
- **Applied in code:** YES -- prospect_theory.py:103-104 uses `ref_window_years` (default 10 from config.py:187) for the trailing peak reference point. This sidesteps the inconsistent-history problem because the reference is always the trailing 10-year peak, not the full-history percentile.
- **Status:** APPLIED-CORRECT (for PLI specifically; the trailing window approach is appropriate here)

---

## 4. Verdict

### CONFIRMED
- **Prospect theory value function:** Lambda = 2.25 and alpha = 0.88 are well-established empirical parameters from Tversky & Kahneman (1992). Their application to perceived political losses is a legitimate theoretical contribution (critical review E3).
- **10-year trailing peak as reference point:** Reasonable operationalization of collective memory and expectation baselines.
- **Domain reduction from 8 to 5:** Well-motivated by data availability. Dropped domains (Democracy, Mobility, Trust) lacked freely-available, regularly-updated data sources. Mobility was particularly incoherent as a time series input (critical review B1).
- **Additive aggregation:** Changing from multiplicative to additive bonuses for breadth and velocity correctly prevents runaway amplification and saturation.
- **K constant reduction:** 10x uniform reduction preserves relative domain weighting while addressing the saturation problem.

### REVISED
- **PLI aggregation method:** Changed from multiplicative (`mean x breadth_mult x velocity_mult`) to additive (`mean + breadth_bonus + velocity_bonus`) per critical review A2. Rationale: multiplicative amplifiers caused saturation at 100 during any recession, making the model a binary indicator rather than a graduated scale.
- **K constants reduced by 10x:** Original values (e.g., wages K=500) caused immediate saturation; reduced values (wages K=50) aim for graduated output. Combined with sqrt compression, the net effect on output range needs empirical validation.
- **Loss score formula:** Changed from spec's `-V x K` to code's `sqrt(-V x K) * 10`. This adds sqrt compression (dampens high values) and a 10x multiplier (rescales to useful range). This revision goes beyond the critical review's recommendation.

### FLAGGED
- **Undocumented sqrt compression and `* 10` multiplier (MODERATE):** The loss score formula at prospect_theory.py:131 (`np.sqrt(-V * K) * 10`) includes two transformations not documented in the spec or the critical review. The `* 10` multiplier is entirely undocumented. These need to be either documented with rationale or removed.
- **Velocity bonus is magnitude, not velocity (MODERATE):** Implementation review A2. The velocity bonus computes average loss magnitude, not rate of change. This makes it redundant with the mean loss score. Fix required in Phase 4: compute actual 12-month change in deviations.
- **Potential double-correction (MODERATE):** K/10 + sqrt may cause the model to underreport losses. The original problem was saturation at 100; the triple fix (K/10 + sqrt + additive) may push the model toward the opposite extreme. Needs empirical backtesting against known episodes (1968, 2008, 2020) to verify the output range is meaningful.
- **Domain K calibration (LOW):** Even at K/10, the relative magnitudes across domains (wages K=50 vs. security K=1) are not empirically derived. They are hand-tuned guesses about how a 5% decline in income should compare to a 5% decline in consumer sentiment. Sensitivity analysis in Phase 4 should test whether the domain ordering matters.

### Summary Statement
PLI correctly implements prospect theory value function parameters and the additive aggregation fix, but contains an undocumented loss score transformation (sqrt + `* 10` multiplier) that deviates from both the spec and the critical review. The velocity bonus computes loss magnitude rather than actual velocity, making it redundant. Phase 4 must resolve the undocumented formula, fix the velocity computation, and empirically validate that the combined corrections (K/10 + sqrt + additive) produce graduated output across known historical episodes.
