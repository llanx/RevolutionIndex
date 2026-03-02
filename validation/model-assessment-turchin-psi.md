# Model Assessment: Turchin Structural-Demographic PSI

## 1. Theoretical Basis

**What the spec claims the model measures:**
The Political Stress Indicator (PSI) models political instability as the multiplicative interaction of three structural forces (model-specifications.md, sections 1.1-1.6):

```
PSI = MMP x EMP x SFD
```

- **MMP** (Mass Mobilization Potential): popular immiseration, measured as relative wage decline
- **EMP** (Elite Mobilization Potential): elite overproduction and intra-elite competition
- **SFD** (State Fiscal Distress): government fiscal weakness and loss of legitimacy

The multiplicative structure encodes the core theoretical claim: instability requires all three pressures simultaneously. If any one factor is zero, PSI is zero.

**Source academic work:**
Peter Turchin's structural-demographic theory (Turchin 2003, *Historical Dynamics*; Turchin 2010; Turchin & Nefedov 2009, *Secular Cycles*; Turchin 2023, *End Times*). The framework builds on Jack Goldstone's (1991) demographic-structural theory of revolution.

**Faithfulness of adaptation:**
The spec's formulation (sections 1.2-1.3) closely follows Turchin's original PSI = MMP x EMP x SFD structure. The variable definitions (relative wages, elite overproduction index, fiscal distress composite) are drawn directly from Turchin's published work. However, the implementation uses drastically simplified proxy variables (see Component Review below), which reduces the model from Turchin's multi-factor composites to single-variable proxies.

---

## 2. Component Review

### MMP (Mass Mobilization Potential)

**Spec definition (model-specifications.md, section 1.2):**
Full MMP is a composite of relative wages (median earnings / GDP per capita), amplified by urbanization rate and youth ratio:
```
MMP_t = wage_distress_t x (1 + 0.5 x urban_t) x (1 + youth_t / youth_baseline)
```
Where wage_distress measures how far wages have fallen below their 20-year trailing peak.

The spec also provides an explicit simplified alternative:
```
MMP_simple_t = 1 - N(labor_share_t)
```

**Code implementation (turchin_psi.py:34, 76):**
Uses the simplified alternative. MMP = 1.0 - minmax_normalize(labor_share, reference), where labor_share is FRED series W270RE1A156NBEA (labor share of GDP, nonfarm business sector). Lower labor share = higher mass mobilization potential.

**Simplifications:**
- Drops urbanization amplifier (constant ~83% for modern US; critical review E5 notes this is essentially a fixed multiplier)
- Drops youth bulge ratio (would require Census population-by-age data, not available from FRED)
- Drops relative wage computation (would require median earnings / GDP per capita calculation)
- Uses labor share of GDP instead of relative wages. These are related but not identical: labor share is a macro-level ratio of total compensation to GDP, while relative wages measure median worker experience relative to overall output.

**Assessment of simplification:** Defensible for a v1 approximation. The spec explicitly offers this as the simplified alternative. Labor share captures the broad trend of worker vs. capital share. However, labor share moves on decadal timescales and has limited within-decade variation, which may make the model unresponsive to shorter-term shifts (implementation review B2).

**Known issues:**

(a) **Spec-level:** The urbanization constant problem (critical review C3/E5) -- US urbanization has been ~83% for decades, making the amplifier essentially a fixed multiplier (1.415). This is a spec-level issue that the simplification correctly sidesteps by dropping urbanization entirely.

(b) **Fix-level:** No spec-level fixes are pending for MMP specifically. The geometric mean fix (A1) applies to the PSI aggregation, not to MMP computation.

(c) **Code-level:** The min-max normalization bug (implementation review A1) directly affects MMP. At `turchin_psi.py:56`, the reference period includes the current date (`ref = data.loc[self.reference_start:date]`). For labor share, which has been on a long-term decline, the current value may be near or at the historical minimum. Min-max normalization against a range that includes the current value means MMP will be pinned near 1.0 whenever labor share is at its historical low. The `percentile_rank_series` function exists in normalization.py:91-119 but is not used.

### EMP (Elite Mobilization Potential)

**Spec definition (model-specifications.md, section 1.2):**
Full EMP is a composite of elite density (degree holders per capita), elite income ratio (top 1% income / median income), elite wealth concentration (top 0.1% net worth / median), and political competition intensity (campaign spending per position).

Simplified alternative:
```
EMP_simple_t = N(top_1pct_share_t)
```

**Code implementation (turchin_psi.py:35, 79):**
Uses the simplified alternative. EMP = minmax_normalize(top_1pct_share, reference), where top_1pct_share comes from WID.world series sptinc992j (top 1% pre-tax national income share).

**Simplifications:**
- Drops elite density (degree holders per capita)
- Drops political competition intensity (campaign spending)
- Drops wealth concentration (top 0.1% net worth)
- Uses top 1% income share alone as the EMP proxy

**Assessment of simplification:** Partially defensible. Top 1% income share is a widely-used inequality metric with data back to 1913 (Piketty-Saez). However, it measures wealth concentration, not elite *overproduction* -- the key Turchin insight. A society could have high income concentration with few elite aspirants (stable oligarchy) or moderate concentration with many frustrated credential-holders competing for few positions (elite overproduction). The proxy captures one dimension of EMP but misses the overproduction dynamic.

**Known issues:**

(a) **Spec-level:** None specific to the simplified EMP.

(b) **Fix-level:** N/A.

(c) **Code-level:** Same min-max normalization bug as MMP (implementation review A1). Top 1% income share has been on a long-term uptrend since ~1976. When current value is at or near historical maximum, EMP is pinned at or near 1.0. Additionally, the WID API endpoint reliability is questionable (implementation review A4) -- two different URLs exist in wid_loader.py (lines 29 and 82) with inconsistent indicator codes (`piinc_p99p100_992_t` vs. `sptinc_p99p100_992j_t`). Neither has been tested against the live API.

### SFD (State Fiscal Distress)

**Spec definition (model-specifications.md, section 1.2):**
Full SFD is a composite of debt/GDP, deficit/GDP, and interest/revenue burden, amplified by a government trust modifier:
```
SFD_t = fiscal_distress_t x (1 + 0.5 x trust_deficit_t)
```
Where fiscal_distress = 0.4 x N(debt_gdp) + 0.3 x N(deficit_gdp) + 0.3 x N(interest_revenue).

Simplified alternative:
```
SFD_simple_t = N(debt_gdp_t)
```

**Code implementation (turchin_psi.py:36, 82):**
Uses the simplified alternative. SFD = minmax_normalize(debt_gdp, reference), where debt_gdp is FRED series GFDEGDQ188S (federal debt held by public as % of GDP).

**Simplifications:**
- Drops deficit flow (annual budget deficit / GDP)
- Drops interest/revenue burden (net interest payments / total federal revenue)
- Drops government trust modifier (Pew/ANES trust data)
- Uses debt level alone

**Assessment of simplification:** Weakest of the three simplifications. As the implementation review B2 notes, debt *level* is not the same as fiscal *distress*. Japan has debt/GDP over 250% without fiscal crisis because it can borrow cheaply. The trust modifier is arguably the most important part of Turchin's SFD -- a broke state that is also distrusted has far less room to maneuver. Dropping it loses a key theoretical channel.

**Known issues:**

(a) **Spec-level:** The Pew trust series used in the full SFD is not a continuous time series (critical review B3) -- it combines different survey instruments with different methodologies over time. This is a spec-level problem that the simplification sidesteps by dropping trust entirely.

(b) **Fix-level:** N/A.

(c) **Code-level:** Same min-max normalization bug as MMP and EMP (implementation review A1). Federal debt/GDP has been on a strong uptrend, especially post-2008. The current value is the historical maximum, so SFD is permanently pinned at 1.0. This is the most severe manifestation of the bug: SFD literally cannot produce any value other than 1.0 for recent dates.

### PSI Aggregation

**Spec definition (model-specifications.md, section 1.3):**
Original: `PSI = MMP x EMP x SFD` (multiplicative).

**Critical review fix (A1):**
Switch to geometric mean: `PSI = (MMP x EMP x SFD)^(1/3)`. This preserves the multiplicative interaction (any zero factor zeroes the result) while keeping output in a readable range.

**Code implementation (turchin_psi.py:87-92):**
```python
components_arr = np.array([mmp, emp, sfd])
if np.any(components_arr == 0):
    psi_raw = 0.0
else:
    psi_raw = np.power(np.prod(components_arr), 1.0 / 3.0)
```
The geometric mean fix is correctly applied. The zero-check at line 89 prevents domain errors with np.power when components are zero. The result is scaled to 0-100 at line 94.

---

## 3. Mathematical Fix Status

### Critical Review A1: PSI Multiplication Crushes Mid-Range Values

- **Issue:** Three percentile-normalized values (0 to 1) multiplied together compress the result toward zero. Three values at 0.70 yield 0.343, not 0.70.
- **Recommended fix:** Geometric mean `(MMP x EMP x SFD)^(1/3)`.
- **Applied in code:** YES -- turchin_psi.py:92 `np.power(np.prod(components_arr), 1.0 / 3.0)`
- **Application correct:** YES -- the geometric mean is mathematically correct. The zero-check at line 89 is a good defensive measure.
- **New issues introduced:** NONE from the geometric mean fix itself.
- **Status:** APPLIED-CORRECT

### Implementation Review A1: Min-Max Normalization on Trending Series

- **Issue:** Reference period includes current date (turchin_psi.py:56). Trending series pin to 1.0 when current value is the historical extreme. SFD (debt/GDP, monotonically rising) is permanently 1.0. EMP (top 1% share, uptrending) is near 1.0.
- **Recommended fix:** Switch to expanding percentile rank (normalization.py:91-119, `percentile_rank_series`), or normalize against reference period excluding current point.
- **Applied in code:** NO -- the model still uses `minmax_normalize`.
- **Status:** NOT-APPLIED (deferred to Phase 4)

### Critical Review B2: Inconsistent Historical Distribution Lengths

- **Issue:** Different data series have different history lengths, making percentile comparisons inconsistent.
- **Recommended fix:** Common reference period for all variables.
- **Applied in code:** PARTIAL -- config.py:22 sets `REFERENCE_START = "1970-01-01"` as common reference. But within the PSI model, `ref = data.loc[self.reference_start:date]` uses an expanding window from 1970 to current date, which still produces inconsistencies when comparing a series available from 1947 vs. one from 1989.
- **Status:** APPLIED-CORRECT (the 1970 common start is appropriate; the expanding window is a separate issue from A1 above)

### Critical Review C1: Metric Overlap / Double-Counting

- **Issue:** Same underlying phenomena appear in multiple models.
- **Relevant to PSI:** The 3-model selection reduces overlap from 6-model version. However, construct-level overlap remains (implementation review B1): PSI's labor share, PLI's employment ratio, and FSP's unemployment rate all measure variants of "how the labor market treats workers."
- **Status:** OPEN (acknowledged as a design constraint, not a bug; inter-model correlation analysis in Phase 4 backtesting will quantify the actual overlap)

---

## 4. Verdict

### CONFIRMED
- **Multiplicative interaction structure:** The theoretical claim that instability requires all three pressures simultaneously is well-grounded in Turchin's academic work and is correctly preserved by the geometric mean formulation.
- **Geometric mean fix:** The critical review A1 fix is correctly applied. Three components at 0.70 now yield 0.70, not 0.343.
- **Reference period standardization:** The common 1970-present reference start (config.py:22) addresses the distribution length inconsistency concern (B2).
- **Prospect theory parameters:** Lambda = 2.25 and alpha = 0.88 are standard Kahneman-Tversky values.
- **Data series selection:** W270RE1A156NBEA, WID sptinc992j, and GFDEGDQ188S are reasonable proxy choices for a simplified v1.

### REVISED
- **Aggregation method:** Changed from multiplicative product to geometric mean per critical review A1. Rationale: product compresses mid-range values toward zero, making the interpretation scale misleading. The geometric mean preserves the interaction property while maintaining output in the [0, 1] range.
- **Model scope labeled "PSI-Simple":** This is a 3-proxy approximation, not the full Turchin PSI. Loses urbanization amplifier, youth bulge, elite density, wealth concentration, deficit flow, interest burden, and trust modifier. Should be labeled accordingly (per implementation review B2).

### FLAGGED
- **Min-max normalization on trending series (CRITICAL):** Implementation review A1. SFD is permanently pinned at 1.0 (debt/GDP is monotonically rising). EMP is near 1.0 (top 1% share is on a long uptrend). The PSI output is effectively determined by whichever component is NOT at its historical extreme. Fix required before Phase 4 model-building: switch to `percentile_rank_series` (already exists in normalization.py) or use z-scores.
- **WID API reliability:** Implementation review A4. Two inconsistent URLs in wid_loader.py. The EMP component depends on WID data; if the API fails, fallback is manual CSV download. Needs live testing.
- **SFD proxy weakness:** Debt level alone is not fiscal distress. Japan case demonstrates debt/GDP can be very high without distress. The trust modifier (dropped from full spec) arguably matters more for instability prediction than the debt level itself.
- **Labor share responsiveness:** W270RE1A156NBEA moves on decadal timescales. MMP may be unresponsive to within-decade shifts in worker immiseration. A flat PSI may reflect proxy choice, not absence of structural pressure.

### Summary Statement
PSI-Simple implements the geometric mean fix correctly but suffers from a critical normalization bug (min-max on trending series) that pins two of three components near 1.0. The 3-proxy simplification is defensible for v1 but loses key theoretical channels, especially the trust modifier in SFD and the elite overproduction dynamic in EMP. Phase 4 must fix the normalization bug before PSI outputs are interpretable.
