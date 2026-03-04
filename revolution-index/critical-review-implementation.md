# Critical Review: Implementation Plan & Code
## Peer Review — As If a Colleague Presented This to Us

**Reviewer's summary:** This is a well-organized first pass that correctly identifies the right starting point (simplified models, FRED data, empirical validation). The architecture is clean, the critical review fixes are mostly applied correctly, and the data acquisition layer is solid. However, there are meaningful bugs that will produce wrong numbers, several design decisions that silently undermine the project's stated goals, and a pattern of "looks complete but isn't" that needs honest acknowledgment.

Below is a systematic critique organized by severity.

---

## CATEGORY A: BUGS THAT WILL PRODUCE WRONG NUMBERS

### A1. Turchin PSI Uses Min-Max Normalization Against an Expanding Window — This Means the Score Can Never Be the Highest It's Ever Been (Severity: HIGH)

**The problem:** `turchin_psi.py:56` computes `ref = data.loc[self.reference_start:date]`. This means the reference distribution *includes the current date*. When you then do `minmax_normalize(current_debt, ref_debt)`, the current value is always somewhere between the min and max of a range that includes itself. Today's value can never exceed the historical max of a series that includes today. The score is capped at whatever the previous high was.

**Why this matters:** SFD (debt/GDP) has been monotonically rising. Today's debt/GDP is the historical maximum. `minmax_normalize` will always return exactly 1.0 for SFD. It literally cannot produce any other value. The model thinks state fiscal distress has been permanently maxed out since the early 2000s.

Similarly for EMP — top 1% income share has been on a long uptrend. Anytime the current value is the historical max, EMP = 1.0. Anytime it's the historical min (which it can only be at the very start of the series), EMP = 0.0.

**The result:** PSI is dominated by whichever component is NOT at its historical extreme, because two of three are likely pinned at 1.0.

**Fix options:** (a) Use expanding percentile rank (already implemented in `normalization.py` as `percentile_rank_series` but not used). (b) Normalize against the full reference period up to `date - 1 month` (exclude current point). (c) Accept that min-max is the wrong normalization for trending series and use z-scores instead.

---

### A2. PLI Velocity Bonus Uses Deviation Magnitude, Not Actual Velocity (Severity: MODERATE)

**The problem:** `prospect_theory.py:184`:
```python
avg_loss_magnitude = np.mean([abs(d) for d in deviations.values() if d < 0])
velocity_bonus = min(self.max_velocity_bonus, max(0.0, avg_loss_magnitude * 100))
```

This is not velocity. Velocity is the *rate of change* of losses — are things getting worse faster? This computes the *current magnitude* of losses. A domain that fell 10% a decade ago and has been flat since gets the same "velocity bonus" as a domain that fell 10% last month.

**Why this matters:** The velocity bonus exists specifically to detect accelerating deterioration. As coded, it's just a second weighting of loss magnitude, making it redundant with the mean loss score.

**Fix:** Compute the actual 12-month change in each domain's deviation. The comment at line 182 even acknowledges this: "For single-date computation, use deviation magnitude as proxy." But single-date computation is the only mode this model runs in — `compute_historical` calls `compute` for each date. So the proxy is permanent.

---

### A3. Config ETI Weights Don't Match Financial Stress Model's Actual Weights (Severity: MODERATE)

**The problem:** `config.py:212-219` defines `eti_weights` with 6 entries summing to 1.0 — including `debt_service: 0.15` and `food_energy_cpi: 0.15`. But `financial_stress.py:46-51` defines `ETI_SERIES` with only 4 entries summing to 1.0 (UNRATE, IC4WSA, real_wage_change, CSCICP03USM665S). The model hardcodes its own weights and ignores the config entirely.

There's also a comment saying `"debt_service": 0.15, # TDSP if added later; omit for now"` — but TDSP is never defined in `FRED_SERIES` and was never downloaded. This is ghost configuration.

**Why this matters:** Whoever reads the config thinks the model uses 6 inputs. The model actually uses 4. The weights in the config (summing to 1.0 across 6 variables) and the weights in the model (summing to 1.0 across 4 variables) describe different systems. If someone later "fixes" the model to use the config weights, 30% of the weight will be assigned to series that don't exist.

**Fix:** Remove phantom entries from config, or make the model actually read from config. Pick one source of truth.

---

### A4. WID API URL Is Likely Wrong / Untested (Severity: MODERATE)

**The problem:** `wid_loader.py:82` hits `https://api.wid.world/api/country-series/sptinc_p99p100_992j_t/US`. WID.world's public API has changed multiple times, and this URL format is not from their current documentation. There's a reasonable chance this returns a 404 or unexpected format.

The top of the file declares two different URLs (`WID_API_URL` on line 29 using a different indicator code `piinc_p99p100_992_t` vs. the one actually called on line 82 using `sptinc_p99p100_992j_t`). Neither is used consistently.

**Why this matters:** If the API call fails, the fallback is good (manual CSV download instructions). But it's dishonest to present this as a working automated pipeline when the primary data source for an entire model component hasn't been tested.

**Fix:** Actually test the API call. If it doesn't work, remove the dead code and make `load_from_csv` the primary interface.

---

## CATEGORY B: DESIGN DECISIONS THAT UNDERMINE STATED GOALS

### B1. The "Zero Data Overlap" Claim Is Misleading (Severity: HIGH, Conceptual)

**The problem:** The plan proudly states "zero overlapping FRED series" between the three models. This is true at the series-ID level but misleading at the *construct* level.

- PSI uses `W270RE1A156NBEA` (labor share of GDP) as MMP.
- PLI uses `LNS12300060` (prime-age employment ratio) for employment losses.
- FSP uses `UNRATE` (unemployment rate) for ETI.

These are three different FRED series measuring variants of the same underlying construct: *how the labor market is treating workers*. When unemployment rises, labor share tends to shift, and employment-population ratio drops. They are not independent signals — they are three views of the same signal.

Similarly, PLI's `UMCSENT` (consumer sentiment) and FSP's `CSCICP03USM665S` (consumer confidence) measure nearly identical constructs with different survey methodologies. Their pairwise correlation is historically above 0.85.

**Why this matters:** The whole reason for selecting three models was to get "genuinely independent signals" that address critical review C1 (metric overlap). But the independence is only at the surface level. You've renamed the overlap problem rather than solved it.

**What to do:** Don't claim independence — measure it. The inter-model correlation analysis in the backtester will reveal this empirically. If PSI and FSP track each other closely, that's an honest finding. But don't market it as solved before the data says so.

---

### B2. PSI With Three Simplified Proxies May Not Measure What Turchin Measures (Severity: MODERATE, Theoretical)

**The problem:** The simplified PSI uses:
- MMP = inverted labor share
- EMP = top 1% income share
- SFD = debt/GDP

Turchin's actual PSI theory requires:
- MMP = *relative wage* decline (wages falling relative to GDP per capita) amplified by *urbanization* and *youth bulge*
- EMP = elite *overproduction* (too many elites for too few positions) + intra-elite *competition* for status
- SFD = *fiscal distress* (deficit trajectory, not debt level) + inability to fund security apparatus

The simplified version strips out every amplifier and interaction term. The labor share of GDP is a structural macro variable that moves on decadal timescales — it has almost no meaningful variation within a 5-year window. Top 1% income share is a wealth concentration measure, not an elite overproduction measure. And debt level is not the same as fiscal distress — Japan has debt/GDP over 250% without fiscal crisis because it can borrow cheaply.

**Why this matters:** The model-specifications.md explicitly provides these simplified alternatives and flags them as "if constructing the full composite is too complex for an initial implementation." That's fine for a first pass. But the code and plan present them as "the Turchin PSI model" without caveat. If the backtesting shows PSI flatlines, it may be because the proxies are wrong, not because Turchin's theory is wrong.

**What to do:** Label it clearly: "PSI-Simple (3-proxy approximation)." Document that a flat or unresponsive PSI is not evidence against Turchin — it's evidence that labor share, top-1% share, and debt/GDP are insufficient proxies. Phase 2 should implement the fuller formulas.

---

### B3. The Backtesting Treats All Six Episodes as Equal True Positives — They Aren't (Severity: MODERATE)

**The problem:** The backtester evaluates whether models "detect" 1968, 1979, 1992, 2001, 2008, and 2020 using the same threshold (45). But these episodes are qualitatively different:

- **1968 and 2020** had genuine mass mobilization (millions in streets, political violence, legitimacy crisis). These are the closest to actual "revolutionary conditions."
- **2008** was a massive economic crisis with modest political mobilization (Tea Party and Occupy were relatively small movements).
- **1992** and **2001** were significant but more contained — single events (LA riots, 9/11) rather than systemic crises.
- **1979-82** was a pure economic stress episode with minimal political mobilization (no mass protests, no legitimacy crisis).

Using the same detection threshold for all six treats a stagflation recession as equivalent to a near-insurrection. If the model scores 1979 the same as 2020, it has no ability to distinguish economic pain from revolutionary potential.

**What to do:** Assign expected severity tiers. Episodes that involved mass political mobilization should score higher than pure economic stress episodes. Something like: 1968 and 2020 → expected score 60-80, 2008 → expected 50-70, 1979 and 1992 → expected 30-50, 2001 → expected 30-45. Then evaluate whether the model *rank-orders them correctly*, not just whether they all cross 45.

---

### B4. The Bootstrap Uncertainty Is Too Narrow — Only Perturbs Reference Window, Not the Thing That Matters (Severity: MODERATE)

**The problem:** `uncertainty.py:30-41` bootstraps PSI uncertainty by varying the reference start date from 1965 to 1975. This is a 10-year range applied to data series that span 50+ years. The min and max of a 50-year series don't change much whether you start in 1965 or 1975. The resulting CI will be extremely narrow — maybe +/- 2-3 points.

What actually drives uncertainty in PSI is: (a) the choice of normalization method (min-max vs. percentile vs. z-score), (b) the choice of proxy (labor share vs. relative wage; debt level vs. deficit; income share vs. elite count), and (c) the aggregation method (geometric mean vs. probability union). None of these are varied.

For PLI, varying lambda from 2.0 to 2.5 and K by a factor of 0.5-2.0 is better, but the K range dominates. A 4x range in K will produce a wide CI. The lambda perturbation is cosmetic by comparison.

**Why this matters:** The critical review demanded uncertainty quantification (D3). If the CIs are trivially narrow for PSI, it gives false confidence. If they're driven entirely by K-range for PLI, they're just measuring "I don't know what K should be."

**What to do:** Be honest about what the bootstrap measures: *parameter sensitivity*, not *model uncertainty*. True model uncertainty includes structural choices (which proxies, which formula) that can't be bootstrapped. Report the narrow CIs alongside a caveat like: "Confidence interval reflects parameter sensitivity only. Structural model uncertainty is much larger."

---

## CATEGORY C: THINGS THAT ARE MISSING OR INCOMPLETE

### C1. No Tests (Severity: MODERATE)

The `tests/` directory exists but contains only an empty `__init__.py`. The plan lists notebooks 02-05 as future deliverables but they don't exist either. The notebook that does exist (`01_data_exploration.ipynb`) hasn't been run, so we don't actually know if the pipeline works end-to-end.

The verification test that *was* run (`python -c "import ..."`) only checks that modules import and basic arithmetic works. It doesn't verify that the data pipeline produces correct LOCF alignment, that min-max normalization handles edge cases, or that models produce outputs in the expected range.

**Fix:** At minimum, add a test that constructs synthetic data (known values), runs each model, and asserts the output is in the expected range.

---

### C2. The `invert` Field in Config Is Defined But Never Used (Severity: LOW)

Every FRED series entry in `config.py` has an `invert` field, thoughtfully documenting which series need to be flipped. But no model code reads this field. The Turchin PSI hardcodes the inversion: `mmp = 1.0 - minmax_normalize(...)`. The Financial Stress Pathway has its own hardcoded `INVERT_SERIES` set. The pipeline ignores it.

This is a minor consistency issue but it's exactly the kind of "looks configured but isn't" pattern that causes confusion later.

---

### C3. `compute_historical` Will Be Extremely Slow (Severity: LOW-MODERATE)

`base_model.py:44-68` computes models one date at a time in a Python loop. For 660 months of history (1970-2025), the Financial Stress model calls `rolling_zscore` on every series for every date — recomputing the entire rolling window each time. This is O(n²) when it could be O(n) by computing the rolling z-score once and indexing into it.

For a research notebook this may be tolerable (minutes, not hours), but it's worth flagging.

---

### C4. Food and Energy CPI Were Planned But Not Implemented (Severity: LOW)

The config's `eti_weights` includes `"food_energy_cpi": 0.15`. The data pipeline's `compute_derived_series` docstring says it computes `food_energy_cpi_yoy`. But the actual code only computes `real_wage_change`. The food/energy CPI series (`CPIUFDSL`, `CPIENGSL`) are not in `FRED_SERIES` and won't be downloaded.

---

## CATEGORY D: STRENGTHS — What the Colleague Got Right

### D1. Data Acquisition Layer Is Solid

The FRED client with caching, rate limiting, stale-cache fallback, and catalog summary is genuinely well-built. This is the part of the codebase that will actually work on first run (given an API key).

### D2. Correct Decision to Start with 3 Models

The project had 6 models with known flaws. Picking 3 and deferring the others (especially PITF with its admitted fictional coefficients) is the right call. The critical review explicitly recommended this.

### D3. Freshness Tracking Is a Good Idea

Tracking months-since-last-observation alongside LOCF values is genuinely useful metadata that most pipeline implementations skip. It enables downstream models to degrade gracefully.

### D4. The Backtesting Framework Design Is Sound

Episode-based evaluation with detection thresholds, distribution analysis, and inter-model correlation — this is the right framework. The implementation issues are fixable; the architecture is correct.

### D5. Critical Review Fixes Are Mostly Applied

Geometric mean for PSI (A1), reduced K constants for PLI (A2), LOCF instead of linear interpolation (B1), common reference period (B2) — these are all implemented. The project took its own medicine.

---

## PRIORITY FIX TABLE

| # | Issue | Severity | Fix Effort |
|---|-------|----------|------------|
| A1 | Min-max on trending series pins to 1.0 | HIGH | Switch to expanding percentile rank or z-score |
| A2 | Velocity bonus is magnitude, not velocity | MODERATE | Compute actual 12-month change in deviations |
| A3 | Config weights don't match model weights | MODERATE | Single source of truth for FSP weights |
| B1 | "Zero overlap" claim is construct-level false | HIGH (conceptual) | Drop the claim; let correlation analysis speak |
| B3 | All episodes treated as equal severity | MODERATE | Add expected severity tiers to backtesting |
| A4 | WID API URL untested | MODERATE | Test or switch to CSV-only |
| C1 | No tests | MODERATE | Add synthetic-data unit tests |
| B4 | Bootstrap too narrow for PSI | MODERATE | Document as parameter sensitivity, not full uncertainty |

---

## OVERALL ASSESSMENT

**Grade: B (Good architecture, implementation bugs, some self-deception)**

The architecture and plan are sound. The decision to start with data-first empirical validation is exactly right. But the code was written quickly without being run against real data, and it shows — there are bugs that will produce wrong numbers (A1 is the most consequential), design decisions that are more fragile than they appear (the "independence" claim), and a pattern of documenting intentions in config that aren't reflected in code.

The honest next step is: fix A1, run the notebook with real data, and look at the output before building anything else. The models may produce something interesting or they may flatline — either outcome is valuable information. But fix the normalization bug first, or you'll be debugging model behavior when the actual issue is a capped min-max score.
