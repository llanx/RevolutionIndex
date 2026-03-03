# Model Assessment: Financial Stress Pathway (FSP)

## 1. Theoretical Basis

**What the spec claims the model measures:**
The Financial Stress Pathway models the causal chain from financial system stress through economic hardship through political grievance through mobilization (model-specifications.md, sections 3.1-3.9):

```
Financial Stress (t) -> Economic Pain (t + 3-12mo) -> Political Grievance (t + 6-18mo) -> Mobilization (t + 9-24mo)
```

The model is organized into four sequential stages:
- **Stage 1 (FSSI):** Financial System Stress Index -- composite of financial market stress indicators
- **Stage 2 (ETI):** Economic Transmission Index -- composite of household economic pain indicators
- **Stage 3 (PGFI):** Political Grievance Formation Index -- political anger and system blame
- **Stage 4 (MAI):** Mobilization Activation Index -- actual collective action

The 2008 financial crisis narrative validates this causal chain: GFC (2008) -> Tea Party/Occupy (2009-2011) -> Trump/Sanders (2016) -> January 6 (2021).

**Source academic work:**
This model does not trace to a single academic framework. It synthesizes:
- Financial crisis literature (Reinhart & Rogoff, Minsky)
- Political economy of financial crises (Funke, Schularick, & Trebesch 2016 on "Going to Extremes: Politics after Financial Crises")
- Relative deprivation theory (Gurr 1970)
- Mobilization theory (Tilly 1978)

**Faithfulness of adaptation:**
The staged causal-chain structure is the spec's most original theoretical contribution (critical review E2). While the individual stages draw on established literatures, the explicit lag modeling between stages is novel. The 2008 case study provides a plausible validation narrative, though the lag parameters are calibrated on very few data points (critical review C2).

The implementation covers only Stages 1-2, deferring Stages 3-4 because they require non-FRED data sources (polling data, protest counts, election data). This is a significant theoretical reduction: the model captures "is financial stress becoming economic pain?" but cannot answer "is economic pain becoming political mobilization?" -- which is the question that actually matters for revolution risk.

---

## 2. Component Review

### Stage 1: Financial System Stress Index (FSSI)

**Spec definition (model-specifications.md, section 3.2):**
FSSI is a z-score composite of 6 financial stress indicators:
```
FSSI = (z_OFR + z_yield + z_VIX + z_credit + z_mortgage + z_bank) / 6
```
Variables: OFR FSI, yield curve (10Y-2Y spread), VIX, credit spreads, mortgage delinquency, bank loan loss provisions. All equally weighted. Z-scores computed against 20-year rolling window.

**Code implementation (financial_stress.py:36-42):**
Uses 5 series (not 6) with unequal weights:
```python
FSSI_SERIES = {
    "STLFSI4": 0.25,      # St. Louis Fed Financial Stress Index
    "T10Y2Y": 0.20,       # Yield curve
    "VIXCLS": 0.20,       # VIX
    "BAMLH0A0HYM2": 0.20, # Credit spreads
    "DRSFRMACBS": 0.15,   # Mortgage delinquency
}
```

**Differences from spec:**
1. Uses STLFSI4 (St. Louis Fed FSI) instead of OFR FSI. These are similar but not identical composite indices.
2. Drops bank_stress (bank loan loss provisions from FDIC QBP). This data requires FDIC quarterly report scraping, not available via FRED.
3. Uses unequal weights (0.15-0.25) instead of equal weights (1/6 each). The weighting is reasonable but undocumented in the spec.
4. Weights sum to 1.0 (0.25 + 0.20 + 0.20 + 0.20 + 0.15 = 1.00), which is correct for a weighted average.

**Z-score computation (financial_stress.py:104-105):**
```python
z_series = rolling_zscore(series, self.window_years)
```
Uses `rolling_zscore` from normalization.py:70-88, which computes a rolling z-score with a 20-year (240-month) window. This correctly implements the spec's 20-year rolling standardization.

**Inversion handling (financial_stress.py:113-115):**
```python
INVERT_SERIES = {"T10Y2Y", "CSCICP03USM665S"}
if series_id in self.INVERT_SERIES:
    z_val = -z_val
```
T10Y2Y (yield curve spread) is correctly inverted: a negative spread (yield curve inversion) indicates financial stress, so the z-score is negated to make higher values = more stress. This matches config.py:98 (`invert: True` for T10Y2Y).

**Score conversion (financial_stress.py:130-133):**
```python
avg_z = weighted_sum / total_weight
from scipy import stats
score = float(stats.norm.cdf(avg_z) * 100)
```
Converts the weighted average z-score to a 0-100 scale using the normal CDF. z=0 -> 50, z=2 -> ~97.7, z=-2 -> ~2.3. This is a reasonable mapping. The spec says "convert to 0-100 using historical CDF" (section 3.2, Step 4); the normal CDF approximation is an acceptable simplification.

**Known issues:**

(a) **Spec-level:** None significant for FSSI. The financial stress indicators are well-established and the z-score approach is standard.

(b) **Fix-level:** N/A.

(c) **Code-level:** The `rolling_zscore` function (normalization.py:84-88) uses `min_periods=max(24, window // 4)` = max(24, 60) = 60 months = 5 years. This means the first 5 years of data produce NaN z-scores. For series starting in 1970, FSSI only produces values from 1975 onward. This is acceptable but should be documented.

### Stage 2: Economic Transmission Index (ETI)

**Spec definition (model-specifications.md, section 3.3):**
ETI is a weighted composite of 8 economic pain indicators:
```
ETI = 0.20 x unemp_delta + 0.15 x claims + 0.10 x hh_fragility + 0.15 x real_wage_delta
    + 0.15 x food_energy + 0.05 x eviction + 0.10 x consumer_conf + 0.10 x biz_failure
```
Variables: unemployment change, initial claims, household fragility, real wage change, food/energy CPI, eviction rate, consumer confidence, business bankruptcy.

**Config definition (config.py:212-219):**
6 entries:
```python
"eti_weights": {
    "UNRATE": 0.20,
    "IC4WSA": 0.15,
    "real_wage_change": 0.15,
    "CSCICP03USM665S": 0.20,
    "debt_service": 0.15,      # TDSP if added later; omit for now
    "food_energy_cpi": 0.15,   # Computed: average of food + energy CPI YoY change
}
```

**Code definition (financial_stress.py:46-51):**
4 entries:
```python
ETI_SERIES = {
    "UNRATE": 0.25,
    "IC4WSA": 0.20,
    "real_wage_change": 0.20,
    "CSCICP03USM665S": 0.35,
}
```

**Critical divergence (implementation review A3):** The config defines 6 ETI series summing to 1.0, but the code hardcodes 4 ETI series summing to 1.0. Two config entries are ghosts:
- `debt_service: 0.15` -- comments say "TDSP if added later; omit for now." TDSP is never defined in FRED_SERIES and was never downloaded.
- `food_energy_cpi: 0.15` -- comments say "Computed: average of food + energy CPI YoY change." The food/energy CPI series (CPIUFDSL, CPIENGSL) are not in FRED_SERIES (implementation review C4).

The code ignores the config entirely and uses its own hardcoded weights. The weights in the code (0.25 + 0.20 + 0.20 + 0.35 = 1.00) are different from the config weights for the same series (0.20 + 0.15 + 0.15 + 0.20 = 0.70 of the config total). Consumer confidence (CSCICP03USM665S) gets 0.35 in code vs. 0.20 in config -- a 75% increase in relative weight.

**Data reduction from spec:**
The spec defines 8 ETI variables. The config defines 6 (dropping household fragility, eviction rate, business bankruptcy -- none available from FRED). The code uses 4 (additionally dropping debt_service and food_energy_cpi). This is a significant reduction: the ETI stage captures less than half of the spec's intended economic pain signal.

**Known issues:**

(a) **Spec-level:** The spec's 8 ETI variables include data sources that don't update reliably (household fragility from Fed SHED is annual with significant lag; eviction data is patchy; business bankruptcy is quarterly from manual sources). The reduction to FRED-available series is pragmatic.

(b) **Fix-level:** N/A (no specific fix was recommended for ETI).

(c) **Code-level:**
1. Config/code weight divergence (implementation review A3): Two sources of truth with different values. If someone "fixes" the model to use config weights, 30% of weight goes to nonexistent series.
2. CSCICP03USM665S (OECD consumer confidence) may be discontinued -- data through Jan 2024 only (01-RESEARCH.md). If discontinued, the ETI loses its highest-weighted component.
3. The `real_wage_change` series is a derived series computed by the data pipeline (CES0500000003 deflated by CPIAUCSL). Its computation is not in the model code itself but in the data pipeline's `compute_derived_series` function.

### FSP Aggregation

**Spec definition (model-specifications.md, section 3.7):**
```
FSPIP = max(FSSI, ETI, PGFI, MAI) x transmission_modifier
```
The max-based aggregation reflects the "leading edge" of the causal chain.

**Code implementation (financial_stress.py:143):**
```python
combined = (fssi + eti) / 2.0
```

**Difference:** The code uses a simple average of Stages 1-2 instead of the spec's max-based aggregation. This is defensible given that only 2 of 4 stages are implemented -- taking the max of 2 values is less meaningful than the max of 4 (where the leading stage can be identified). However, the simple average loses the causal-chain insight: during a financial crisis (FSSI high, ETI still low), the average would be moderate, while the max would correctly flag the leading indicator.

**Alternative consideration:** Even with 2 stages, a max-based approach might be preferable:
- `max(FSSI, ETI)` during financial stress onset: FSSI high -> composite reflects the financial warning
- `(FSSI + ETI) / 2` during financial stress onset: FSSI high but ETI low -> composite shows moderate, masking the warning

### Lag Analysis

**Spec definition (model-specifications.md, section 3.8):**
Lag calibration based on 3 historical episodes: 2008 (36 months total lag), 2001 (disrupted), 2020 (10 months, compressed).

**Code implementation (financial_stress.py:167-212):**
```python
def compute_lag_analysis(self, data, start, end, max_lag_months=24):
```
Computes cross-correlation between FSSI and ETI at various lags (0-24 months). This is a sound empirical approach to measuring the transmission lag.

**Known issues:**

(a) **Spec-level (critical review C2):** The lag structure is based on N=2 usable data points (2008 and 2020; 2001 is flagged as disrupted). The "expected lag of 3-12 months" is presented with confidence that two data points cannot support. The 2020 case compressed all stages into ~10 months due to simultaneous triggers, making it a poor validation of the sequential causation model.

(b) **Fix-level:** The critical review recommended treating lags as "rough empirical guidance" rather than calibrated parameters, and adding more historical episodes (1970s stagflation, 1990-91 recession). The code's cross-correlation approach is appropriate but the N=2 calibration concern remains.

(c) **Code-level:** The `compute_lag_analysis` method uses `compute_historical` internally, which is O(n^2) (implementation review C3). For 660 months of history, this could be very slow.

---

## 3. Mathematical Fix Status

### Critical Review C2: FS-PIP Lag Structure Based on Three Data Points

- **Issue:** Lag calibration uses N=2-3 episodes. The "expected lag" of 3-12 months is overly precise for the evidence base.
- **Recommended fix:** Be honest about N=2. Present lags as rough guidance, not calibrated parameters. Add more episodes.
- **Applied in code:** PARTIAL -- the cross-correlation analysis (financial_stress.py:167-212) provides empirical measurement rather than hardcoded lags. However, the config (FSP_PARAMS) still uses `max_lag_months: 24` as if the lag structure is well-characterized.
- **New issues introduced:** NONE.
- **Status:** APPLIED-CORRECT (the empirical correlation approach is more honest than hardcoded lags)

### Implementation Review A3: Config/Code ETI Weight Divergence

- **Issue:** Config lists 6 ETI series with weights summing to 1.0; code hardcodes 4 series with different weights summing to 1.0. Ghost entries `debt_service` and `food_energy_cpi` in config reference nonexistent data.
- **Recommended fix:** Remove phantom entries from config, or make the model read from config. Single source of truth.
- **Applied in code:** NO -- the divergence remains.
- **Status:** NOT-APPLIED (deferred to Phase 4)

### Implementation Review C4: Food/Energy CPI Planned But Not Implemented

- **Issue:** Config's ETI weights include `food_energy_cpi: 0.15`. The data pipeline's `compute_derived_series` docstring mentions it. But the actual code only computes `real_wage_change`. The food/energy CPI series (CPIUFDSL, CPIENGSL) are not in FRED_SERIES.
- **Applied in code:** NO -- food/energy CPI is not implemented.
- **Status:** NOT-APPLIED (documented ghost configuration)

### Critical Review B1: Mixing Data Frequencies

- **Issue:** FSP combines daily (VIX, yield curve, credit spreads), weekly (STLFSI4, IC4WSA), monthly (UNRATE, CES0500000003, CPIAUCSL, CSCICP03USM665S), and quarterly (DRSFRMACBS) data.
- **Relevant fix:** LOCF is implemented in the data pipeline for frequency alignment.
- **Applied in code:** YES -- the data pipeline handles frequency alignment via LOCF. The rolling z-score computation in normalization.py uses monthly frequency.
- **Status:** APPLIED-CORRECT

### Critical Review C1: Metric Overlap

- **Issue:** FSP's UNRATE (unemployment) and CSCICP03USM665S (consumer confidence) overlap with PLI's LNS12300060 (employment ratio) and UMCSENT (consumer sentiment) at the construct level.
- **Applied in code:** N/A -- this is a design constraint, not a bug. The 3-model selection achieves zero overlap at the FRED series ID level but construct-level overlap remains (implementation review B1).
- **Status:** OPEN (acknowledged; inter-model correlation will be measured in Phase 4)

---

## 4. Verdict

### CONFIRMED
- **Causal chain theory:** The staged model (financial stress -> economic pain -> political grievance -> mobilization) is the spec's most novel theoretical contribution (critical review E2). The 2008-2021 narrative validates the general framework.
- **Z-score normalization:** Rolling 20-year z-scores for financial and economic indicators are a standard, well-understood approach. Better than min-max for trending series.
- **FSSI composition:** The 5 financial stress indicators (STLFSI4, T10Y2Y, VIXCLS, BAMLH0A0HYM2, DRSFRMACBS) are well-established financial stress measures. The z-score + CDF approach produces graduated output (unlike PSI's min-max pinning problem).
- **Cross-correlation lag analysis:** The empirical approach to measuring transmission lag (financial_stress.py:167-212) is more honest than hardcoded lag parameters.
- **LOCF for frequency alignment:** Correctly applied for mixing daily/weekly/monthly/quarterly data.

### REVISED
- **Stage implementation scope:** Reduced from 4 stages to 2 (FSSI + ETI only). Stages 3-4 (political grievance, mobilization) deferred because they require non-FRED data sources (polling, protest counts, election results). This is a pragmatic constraint but a significant theoretical reduction.
- **ETI composition:** Reduced from spec's 8 variables to 4 FRED-available series. Ghost entries in config (debt_service, food_energy_cpi) document intended but unimplemented components.
- **FSSI composition:** Reduced from spec's 6 variables to 5 (dropped bank loan loss provisions; substituted STLFSI4 for OFR FSI). Weights changed from equal to unequal.
- **Aggregation method:** Changed from `max(FSSI, ETI, PGFI, MAI)` to `(FSSI + ETI) / 2.0`. Defensible given only 2 stages are implemented, but loses causal-chain leading-indicator insight.

### FLAGGED
- **Config/code ETI weight divergence (HIGH):** Implementation review A3. Config and code define different weights for different numbers of series. This is a maintenance hazard and a source of confusion. Must be resolved in Phase 4: either remove ghost entries from config or make the model read from config.
- **CSCICP03USM665S potential discontinuation (HIGH):** This series has the highest weight in the code's ETI (0.35). If discontinued (data ends Jan 2024), the ETI stage loses its most important component. A replacement must be identified during the data audit (Plan 01-02).
- **Stages 3-4 gap (MODERATE):** The model's theoretical contribution is the full causal chain, but only half is implemented. Without Stages 3-4, the model cannot answer "is economic pain becoming political mobilization?" Phase 2 literature mining should identify data sources for PGFI and MAI.
- **N=2 lag calibration (MODERATE):** Critical review C2. The lag structure is rough guidance, not calibrated parameters. The cross-correlation analysis improves this, but the underlying sample (2008, 2020) is very small.
- **Simple average aggregation (LOW):** `(FSSI + ETI) / 2.0` may mask early warning signals when FSSI is high but ETI is still low (financial stress not yet transmitted). Consider max-based approach even for 2 stages.
- **O(n^2) compute_historical performance (LOW):** Implementation review C3. The lag analysis calls compute_historical, which recomputes rolling z-scores for every date in a Python loop. May be slow for 660+ months of history. Not a correctness issue.

### Summary Statement
FSP correctly implements z-score-based financial stress and economic pain composites (Stages 1-2) with sound normalization and lag analysis infrastructure. However, the ETI stage has a critical config/code weight divergence (6 config series vs. 4 code series), and the CSCICP03USM665S series (highest ETI weight at 0.35) may be discontinued. The model's main theoretical contribution -- the full 4-stage causal chain -- is only half-implemented, and the simple average aggregation loses the causal-chain leading-indicator insight. Phase 4 must resolve the config/code divergence, verify or replace CSCICP03USM665S, and consider implementing Stages 3-4 with non-FRED data.
