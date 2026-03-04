# Revolution Vulnerability Index: Model Specifications
## Phase 1 & Phase 2 — Data Sources, Formulas, and Computational Logic

### Document Purpose

This document provides implementation-ready specifications for six models organized into two phases:

- **Phase 1 (Core Ensemble):** Turchin PSI, Prospect Theory PRM, Financial Stress Pathway
- **Phase 2 (Broadening):** Expanded RVI, PITF, CSD Tipping Point

Each model specification includes: variable definitions, exact data sources with identifiers, mathematical formulas, normalization procedures, aggregation logic, output interpretation, and known limitations.

### Notation Conventions

- `x_t` = value of metric x at time t
- `x̄` = mean of x over reference period
- `σ(x)` = standard deviation of x over reference period
- `Δx_t` = x_t - x_{t-1} (first difference)
- `Δ²x_t` = Δx_t - Δx_{t-1} (second difference / acceleration)
- `P(x)` = percentile rank of x within its historical distribution
- `N(x)` = min-max normalization of x to [0, 1]
- `Z(x)` = z-score standardization: (x - x̄) / σ(x)

---

---

# PHASE 1: CORE ENSEMBLE

---

## MODEL 1: TURCHIN STRUCTURAL-DEMOGRAPHIC PSI

### 1.1 Theoretical Foundation

Peter Turchin's Political Stress Indicator (PSI or Ψ) models instability as the **multiplicative** interaction of three forces:

```
PSI = MMP × EMP × SFD
```

Where:
- **MMP** = Mass Mobilization Potential (popular immiseration)
- **EMP** = Elite Mobilization Potential (elite overproduction and competition)
- **SFD** = State Fiscal Distress (government fiscal weakness)

The multiplicative structure is the core theoretical claim: if any one factor is zero (no popular grievance, or no elite conflict, or no state weakness), overall instability pressure is zero regardless of the others. Instability requires all three simultaneously.

### 1.2 Variable Definitions and Data Sources

#### MMP — Mass Mobilization Potential

MMP captures the degree to which the general population is economically distressed relative to overall economic output. The central concept is **relative wages** (w): wages scaled by GDP per capita, capturing whether workers are receiving their share of economic growth.

| Variable | Definition | Primary Source | Series ID / Access | Frequency | History |
|---|---|---|---|---|---|
| `w` — Relative Wage | (Median real weekly earnings) / (Real GDP per capita) | BLS Current Population Survey + BEA NIPA | BLS: LEU0252881500 (median usual weekly earnings); BEA: Table 7.1 (real GDP per capita) | Quarterly (BLS quarterly median; BEA quarterly GDP) | BLS median earnings: 1979-present; BEA GDP: 1947-present |
| `w_alt` — Labor Share of GDP | Compensation of employees / GDP | BLS Productivity & Costs (Major Sector); BEA NIPA Table 1.12 | BLS: PRS85006173 (labor share, nonfarm business); FRED: W270RE1A156NBEA | Quarterly | 1947-present |
| `urban` — Urbanization Rate | % of population living in urban areas | Census Bureau (decennial); World Bank WDI | World Bank: SP.URB.TOTL.IN.ZS | Annual (Census intercensal estimates) | 1790-present (Census); 1960-present (World Bank) |
| `youth` — Youth Ratio | Population aged 15-29 / Total population | Census Bureau Population Estimates; UN World Population Prospects | Census: Annual Estimates of Resident Population by Age; UN WPP medium variant | Annual | 1900-present (Census) |
| `CPI_food` — Real Food Cost Burden | Food CPI / Overall CPI × (food expenditure share of bottom quintile) | BLS CPI (Food at Home: CUUR0000SAF11); BLS Consumer Expenditure Survey | FRED: CPIUFDSL (food CPI); CEX Table 1101 (expenditure by quintile) | Monthly (CPI); Annual (CEX) | 1947-present (CPI) |

**MMP Computation:**

Step 1 — Compute relative wage:
```
w_t = (median_real_weekly_earnings_t × 52) / real_GDP_per_capita_t
```

Step 2 — Compute wage distress. MMP rises as w falls below its historical peak. Use the 20-year trailing peak as the reference (w₀):
```
w₀ = max(w_{t-80}, w_{t-79}, ..., w_t)    [20 years of quarterly data = 80 quarters]
```

Step 3 — Wage distress ratio:
```
wage_distress_t = max(0, (w₀ - w_t) / w₀)
```
This yields 0 when wages are at their peak, and positive values proportional to the decline from peak.

Step 4 — MMP composite. Weight by urbanization and youth share (both as amplifiers of mobilization capacity):
```
MMP_t = wage_distress_t × (1 + 0.5 × urban_t) × (1 + youth_t / youth_baseline)
```
Where `youth_baseline` = 0.20 (a 20% youth share is the neutral reference point; higher ratios amplify MMP).

Step 5 — Normalize to [0, 1] using the historical distribution (1950-present):
```
MMP_norm_t = P(MMP_t | MMP_1950, ..., MMP_t)
```

**Alternative MMP (simplified):** If constructing the full composite is too complex for an initial implementation, use labor share of GDP alone as the primary proxy:
```
MMP_simple_t = 1 - N(labor_share_t)
```
Where N() is min-max normalization over the 1947-present range. As labor share declines toward its historical minimum, MMP approaches 1.

---

#### EMP — Elite Mobilization Potential

EMP captures the degree to which there are more elite aspirants than the society can absorb into elite positions, and the intensity of competition among existing elites.

| Variable | Definition | Primary Source | Series ID / Access | Frequency | History |
|---|---|---|---|---|---|
| `e_num` — Elite Density | Number of adults with bachelor's degree or higher per 100,000 population | Census Bureau CPS (Table A-1, Educational Attainment) | Census: Historical Table A-1; FRED: CEPHE (% with bachelor's+) | Annual | 1940-present (decennial); 1964-present (annual CPS) |
| `e_income` — Relative Elite Income | Mean income of top 1% / Median household income | World Inequality Database (WID.world); Census CPS HINC-06 | WID: sptinc992j (top 1% pre-tax income share); Census: Table HINC-06 | Annual | 1913-present (WID); 1967-present (Census) |
| `e_wealth` — Elite Wealth Concentration | Net worth of top 0.1% households / Median household net worth | Federal Reserve DFA (Distributional Financial Accounts) | Fed DFA: Table 1 (wealth shares by percentile group) | Quarterly | 1989-present |
| `lawyers` — Lawyers Per Capita | Licensed attorneys per 100,000 population | American Bar Association (ABA) National Lawyer Counts | ABA annual lawyer demographics reports | Annual | 1878-present (ABA) |
| `e_competition` — Political Competition Intensity | Total campaign spending (inflation-adjusted) per federal elected position | FEC / OpenSecrets | OpenSecrets.org bulk data; FEC individual contributions database | Per election cycle | 1990-present (FEC electronic); 1976-present (manual) |

**EMP Computation:**

Step 1 — Elite overproduction index. Measure how far elite density has risen above its historical norm:
```
elite_overproduction_t = e_num_t / e_num_1970
```
Using 1970 as the baseline (when ~11% of adults had a bachelor's degree, roughly matching available elite positions). Current values (~37-40%) yield an overproduction ratio of ~3.5x.

Step 2 — Elite income ratio (measures the "wealth pump" — how aggressively elites are extracting relative to the median):
```
wealth_pump_t = e_income_t / e_income_1970
```
Top 1% income share was ~10% in 1970; it is ~20% now, yielding a ratio of ~2.0.

Step 3 — EMP composite:
```
EMP_t = (elite_overproduction_t × wealth_pump_t) / (elite_overproduction_1970 × wealth_pump_1970)
```
This normalizes so that 1970 = 1.0 (the "baseline" level of elite competition). Values >1.0 indicate elevated elite pressure.

Step 4 — Normalize:
```
EMP_norm_t = P(EMP_t | EMP_1950, ..., EMP_t)
```

**Alternative EMP (simplified):** Use top 1% income share alone:
```
EMP_simple_t = N(top_1pct_share_t)
```
Min-max normalized over 1913-present range (Piketty-Saez data). The 1928 peak (~23.9%) and the 1976 trough (~8.9%) define the range.

---

#### SFD — State Fiscal Distress

SFD captures the government's fiscal weakness — its inability to fund operations, respond to crises, or buy social peace through spending.

| Variable | Definition | Primary Source | Series ID / Access | Frequency | History |
|---|---|---|---|---|---|
| `debt_gdp` — Federal Debt to GDP | Federal debt held by public / GDP | CBO Budget and Economic Outlook; FRED | FRED: GFDEGDQ188S (quarterly); CBO historical tables | Quarterly | 1966-present (FRED); 1790-present (Treasury historical) |
| `deficit_gdp` — Federal Deficit to GDP | Annual budget deficit / GDP | CBO Monthly Budget Review; FRED | FRED: FYFSGDA188S (annual); CBO monthly budget reports | Monthly/Annual | 1901-present |
| `interest_revenue` — Debt Service Burden | Net interest payments / Total federal revenue | CBO Budget Outlook; Treasury Monthly Statement | CBO Table 1-1; Treasury MTS | Monthly/Annual | 1962-present |
| `trust_gov` — Government Trust (inverse) | 1 - (% trusting government to do right thing "always/most of the time") | Pew Research Center; ANES | Pew: "Public Trust in Government" series; ANES cumulative file | Varies (Pew: ~3-4x/year; ANES: biennial) | 1958-present |

**SFD Computation:**

Step 1 — Fiscal distress composite. Combine debt level, deficit flow, and debt service burden:
```
fiscal_distress_t = 0.4 × N(debt_gdp_t) + 0.3 × N(deficit_gdp_t) + 0.3 × N(interest_revenue_t)
```
Weights reflect that the debt *stock* is the structural condition, while deficit *flow* and interest burden are the dynamic pressures. N() is min-max normalization over 1950-present.

Step 2 — Incorporate government trust as a modifier. Low trust reduces the state's capacity to raise revenue, implement reforms, or rally support during crises:
```
trust_deficit_t = 1 - (trust_gov_t / trust_gov_1960)
```
Using 1960 trust levels (~73%) as the baseline. Current levels (~22%) yield trust_deficit ≈ 0.70.

Step 3 — SFD composite:
```
SFD_t = fiscal_distress_t × (1 + 0.5 × trust_deficit_t)
```
Trust deficit amplifies fiscal distress (a state that is both broke and distrusted is in worse shape than one that is merely broke).

Step 4 — Normalize:
```
SFD_norm_t = P(SFD_t | SFD_1950, ..., SFD_t)
```

**Alternative SFD (simplified):**
```
SFD_simple_t = N(debt_gdp_t)
```

---

### 1.3 Master PSI Formula

```
PSI_t = MMP_norm_t × EMP_norm_t × SFD_norm_t
```

Output range: [0, 1], where 0 = no instability pressure and 1 = maximum historical pressure.

**Rescale to 0-100 for dashboard display:**
```
PSI_display_t = PSI_t × 100
```

### 1.4 Interpretation Scale

| PSI Range | Interpretation | Historical Analog |
|---|---|---|
| 0-10 | Low pressure | U.S. 1950s-1960s ("Era of Good Feelings 2.0") |
| 10-25 | Moderate pressure | U.S. 1990s |
| 25-50 | Elevated pressure | U.S. 1840s-1850s (pre-Civil War buildup) |
| 50-75 | High pressure | U.S. 1920s-1930s; U.S. 1850s-1860s |
| 75-100 | Crisis-level pressure | Secular cycle crisis phase; pre-revolutionary conditions |

**Critical note:** PSI measures *structural pressure*, not *probability of revolution*. A PSI of 80 means "structural conditions are as severe as the worst historical episodes" — it does not mean "revolution is 80% likely." Trigger events, state response, and contingency determine whether pressure becomes action.

### 1.5 Temporal Dynamics Enhancement

In addition to the point-in-time PSI, compute:

```
ΔPSI_t = PSI_t - PSI_{t-4}           [1-year change, quarterly data]
Δ²PSI_t = ΔPSI_t - ΔPSI_{t-4}        [acceleration]
PSI_5yr_avg_t = mean(PSI_{t-20}, ..., PSI_t)   [5-year moving average]
```

Flag conditions:
- **Rapid deterioration:** ΔPSI_t > 2 × σ(ΔPSI) over the historical series
- **Accelerating deterioration:** Δ²PSI_t > 0 for 4+ consecutive quarters
- **Sustained elevation:** PSI_5yr_avg_t > 50

### 1.6 Data Pipeline Summary

```
┌─────────────────────┐
│   BLS (wages, CPI,  │──→ Quarterly ──→ MMP Computation
│   labor share)      │
├─────────────────────┤
│   BEA (GDP per cap) │──→ Quarterly ──→ MMP Computation
├─────────────────────┤
│   Census (education,│──→ Annual ────→ EMP Computation
│   population)       │
├─────────────────────┤
│   WID / Fed DFA     │──→ Annual ────→ EMP Computation
│   (wealth shares)   │
├─────────────────────┤
│   CBO / FRED (debt, │──→ Quarterly ──→ SFD Computation
│   deficit, interest)│
├─────────────────────┤
│   Pew/ANES (trust)  │──→ Interpolated → SFD Computation
│                     │    to quarterly
└─────────────────────┘
         │
         ▼
    PSI = MMP × EMP × SFD
         │
         ▼
    Normalize, flag, display
```

---

---

## MODEL 2: PROSPECT THEORY POLITICAL RISK MODEL (PT-PRM)

### 2.1 Theoretical Foundation

Based on Kahneman & Tversky's prospect theory, this model captures a core behavioral insight: **people evaluate conditions relative to a reference point, not in absolute terms**, and **losses hurt ~2.25x more than equivalent gains feel good**. Applied to political instability:

- A country where wages declined from $60k to $50k is more unstable than one where wages were always $50k
- The J-Curve (Davies) is a special case: improvement followed by decline maximizes perceived loss
- When losses occur across *multiple domains simultaneously*, the aggregate perceived loss exceeds any single domain's contribution

This model transforms absolute indicator values into **perceived loss scores** using the prospect theory value function.

### 2.2 Domain Definitions and Data Sources

The model tracks 8 domains. Each domain has a primary metric and reference point:

| # | Domain | Primary Metric | Source | Series ID | Frequency | History |
|---|---|---|---|---|---|---|
| 1 | **Wages** | Real median household income (2023 dollars) | Census CPS ASEC | FRED: MEHOINUSA672N | Annual | 1984-present |
| 2 | **Housing** | Housing Affordability Index (higher = more affordable) | NAR / FRED | FRED: FIXHAI | Monthly | 1971-present |
| 3 | **Health** | Life expectancy at birth | CDC NVSS / NCHS | CDC WONDER; FRED: SPDYNLE00INUSA | Annual | 1900-present |
| 4 | **Employment** | Prime-age (25-54) employment-to-population ratio | BLS CPS | FRED: LNS12300060 | Monthly | 1948-present |
| 5 | **Democracy** | V-Dem Liberal Democracy Index (0-1) | V-Dem Institute | V-Dem: v2x_libdem | Annual | 1789-present |
| 6 | **Mobility** | Intergenerational mobility (absolute, by birth cohort) | Opportunity Insights (Chetty et al.) | opportunityinsights.org datasets | By birth cohort (5-year intervals) | Birth cohorts 1940-1990 |
| 7 | **Security** | Consumer Sentiment Index (expectations component) | U. Michigan Survey of Consumers | FRED: UMCSENT | Monthly | 1952-present |
| 8 | **Trust** | % trusting government "always/most of time" | Pew Research Center | Pew public trust time series | ~Quarterly | 1958-present |

### 2.3 Computation Logic

#### Step 1 — Reference Point Calculation

For each domain `d`, compute the **10-year trailing peak** as the population's reference point:

```
ref_d,t = max(x_{d,t-120}, x_{d,t-119}, ..., x_{d,t})    [for monthly data; 120 months = 10 years]
ref_d,t = max(x_{d,t-10}, x_{d,t-9}, ..., x_{d,t})        [for annual data]
```

Why 10 years: This approximates the horizon of collective memory — most adults vividly remember conditions within the last decade and use them as their expectation baseline.

#### Step 2 — Loss/Gain Calculation

For each domain, compute the deviation from reference:

```
deviation_d,t = (x_{d,t} - ref_d,t) / ref_d,t
```

This is a proportional deviation. Negative values = loss territory; positive values = gain territory (only possible if x is currently at its 10-year peak, making deviation = 0, or if the metric has been monotonically improving).

#### Step 3 — Prospect Theory Value Function

Apply the asymmetric value function:

```
If deviation_d,t < 0 (LOSS):
    V_d,t = -λ × |deviation_d,t|^α

If deviation_d,t >= 0 (GAIN):
    V_d,t = deviation_d,t^α
```

Parameters (from Kahneman & Tversky empirical estimates):
- `λ = 2.25` (loss aversion coefficient — losses hurt 2.25x as much as equivalent gains)
- `α = 0.88` (diminishing sensitivity — the 10th unit of loss hurts less than the 1st)

The output `V_d,t` is negative when the domain is in loss territory and positive when at or above reference.

#### Step 4 — Loss Magnitude Score (per domain)

Convert V to a 0-100 "loss pressure" score:

```
loss_score_d,t = min(100, max(0, -V_d,t × K_d))
```

Where `K_d` is a domain-specific scaling constant calibrated so that the worst historical loss in that domain maps to ~90-95 on the scale:

| Domain | Worst Historical Loss | K_d (calibration constant) |
|---|---|---|
| Wages | 2011 trough: median income ~8% below 1999 peak | K = 500 |
| Housing | 2006 peak to 2012 trough: affordability index dropped ~50% | K = 100 |
| Health | 2019-2021: life expectancy dropped ~2.5 years (3.2%) | K = 1500 |
| Employment | 2020 April: prime-age EPOP dropped from 80.5% to 69.6% (13.5%) | K = 35 |
| Democracy | V-Dem 2015-2024: LDI dropped from ~0.85 to ~0.72 (15%) | K = 30 |
| Mobility | Cohort 1940: 90% earned more than parents; Cohort 1980: ~50% | K = 12 |
| Security | Consumer sentiment dropped from 101 (2000) to 50 (2022) — 50% | K = 10 |
| Trust | 73% (1958) to 22% (2024) — 70% decline from peak | K = 7 |

#### Step 5 — Loss Breadth Score

Count how many domains are simultaneously in loss territory (deviation < 0):

```
n_losses_t = count(d where deviation_d,t < 0)
```

Breadth multiplier (non-linear — simultaneous losses across many domains compound perceived crisis):

```
breadth_multiplier_t = 1 + 0.1 × (n_losses_t - 1)^1.5
```

| Domains in Loss | Breadth Multiplier |
|---|---|
| 1 | 1.00 |
| 2 | 1.10 |
| 3 | 1.28 |
| 4 | 1.52 |
| 5 | 1.80 |
| 6 | 2.11 |
| 7 | 2.45 |
| 8 | 2.81 |

Rationale: When losses are concentrated in 1-2 domains, people can rationalize ("the economy is bad but at least democracy is strong"). When 6-8 domains are simultaneously declining, the system-level perception shifts to "everything is falling apart."

#### Step 6 — Loss Velocity Score

Measure how fast conditions are deteriorating (rate of change of the loss):

```
velocity_d,t = -(deviation_d,t - deviation_d,t-12) / 12    [monthly, annualized]
```

Positive velocity = conditions worsening; negative = conditions improving.

Aggregate velocity:
```
mean_velocity_t = mean(velocity_d,t for all d where velocity_d,t > 0)
```

Velocity multiplier:
```
velocity_multiplier_t = 1 + min(1.0, mean_velocity_t × 20)
```

This ranges from 1.0 (no acceleration of losses) to 2.0 (rapid deterioration across multiple domains).

#### Step 7 — Composite Perceived Loss Index (PLI)

```
raw_PLI_t = (mean(loss_score_d,t for all d)) × breadth_multiplier_t × velocity_multiplier_t
```

Normalize to 0-100:
```
PLI_t = min(100, raw_PLI_t)
```

### 2.4 Interpretation Scale

| PLI Range | Interpretation | Pattern |
|---|---|---|
| 0-15 | Low perceived loss | Most domains at or near 10-year peaks |
| 15-35 | Moderate perceived loss | 1-2 domains below peak; stable or improving |
| 35-55 | Elevated perceived loss | 3-4 domains below peak; some deteriorating |
| 55-75 | High perceived loss | 5+ domains below peak; deterioration accelerating |
| 75-100 | Crisis-level perceived loss | Broad, rapid, simultaneous deterioration across most domains |

### 2.5 J-Curve Detection (Special Flag)

The J-Curve pattern (Davies) is the single most dangerous trajectory: a period of improvement creates rising expectations, then a sharp reversal devastates perceived wellbeing.

For each domain, detect J-curve conditions:
```
j_curve_d,t = TRUE if:
    1. ref_d,t was set within the last 3 years (improvement was recent)
    AND
    2. deviation_d,t < -0.05 (current value is >5% below that recent peak)
    AND
    3. velocity_d,t > 0.01 (deterioration is ongoing, not bottomed out)
```

J-curve domain count:
```
j_curve_count_t = count(d where j_curve_d,t = TRUE)
```

**J-Curve Alert:** Trigger when `j_curve_count_t >= 3` (three or more domains simultaneously exhibiting the dangerous improvement-then-reversal pattern).

### 2.6 Data Pipeline Summary

```
┌─────────────────────┐
│  Census (income)     │──→ Annual ────────→ Domain 1: Wages
│  FRED (housing)      │──→ Monthly ───────→ Domain 2: Housing
│  CDC (life expect.)  │──→ Annual ────────→ Domain 3: Health
│  BLS (employment)    │──→ Monthly ───────→ Domain 4: Employment
│  V-Dem (democracy)   │──→ Annual ────────→ Domain 5: Democracy
│  Opp. Insights       │──→ By cohort ────→ Domain 6: Mobility
│  U. Michigan (sent.) │──→ Monthly ───────→ Domain 7: Security
│  Pew (trust)         │──→ ~Quarterly ───→ Domain 8: Trust
└─────────────────────┘
         │
         ▼
    For each domain:
    1. Compute 10-year trailing peak (reference point)
    2. Compute deviation from reference
    3. Apply prospect theory value function (λ=2.25, α=0.88)
    4. Convert to loss score (0-100)
         │
         ▼
    Aggregate:
    × Breadth multiplier (how many domains in loss)
    × Velocity multiplier (how fast are losses worsening)
         │
         ▼
    PLI (0-100) + J-Curve flags
```

---

---

## MODEL 3: FINANCIAL STRESS PATHWAY MODEL (FS-PIP)

### 3.1 Theoretical Foundation

This model maps the **causal chain** from financial system stress through economic hardship through political grievance through mobilization. Rather than treating financial and political indicators as contemporaneous inputs to a single score, it models the **temporal sequence** with defined lag structures:

```
Financial Stress (t) → Economic Pain (t + 3-12 months) → Political Grievance (t + 6-18 months) → Mobilization (t + 9-24 months)
```

The 2008 financial crisis → Tea Party/Occupy (2009-2011) → Trump/Sanders (2016) → January 6 (2021) validates this causal chain operating over ~13 years.

### 3.2 Stage 1: Financial System Stress Index (FSSI)

| Variable | Definition | Source | Series ID | Frequency |
|---|---|---|---|---|
| `OFR_FSI` | OFR Financial Stress Index (composite) | Office of Financial Research | FRED: STLFSI4 (St. Louis Fed alternative); OFR website | Daily |
| `yield_curve` | 10Y-2Y Treasury spread (inverted = stress) | FRED | FRED: T10Y2Y | Daily |
| `VIX` | CBOE Volatility Index | CBOE | FRED: VIXCLS | Daily |
| `credit_spread` | ICE BofA US High Yield Option-Adjusted Spread | ICE / FRED | FRED: BAMLH0A0HYM2 | Daily |
| `mortgage_delinq` | Mortgage delinquency rate (90+ days) | FRED / MBA | FRED: DRSFRMACBS (residential, all) | Quarterly |
| `bank_stress` | Bank loan loss provisions / total loans | FDIC Quarterly Banking Profile | FDIC QBP Tables | Quarterly |

**FSSI Computation:**

Step 1 — Standardize each variable to z-scores using a 20-year rolling window:
```
z_i,t = (x_i,t - mean(x_i, t-5040..t)) / std(x_i, t-5040..t)    [5040 trading days ≈ 20 years for daily data]
```
For quarterly data, use 80-quarter (20-year) rolling window.

Step 2 — Invert yield curve (positive spread = low stress, negative = high stress):
```
z_yield_curve = -z_yield_curve    [so that inversion shows as positive stress]
```

Step 3 — Composite with equal weights:
```
FSSI_t = (z_OFR + z_yield + z_VIX + z_credit + z_mortgage + z_bank) / 6
```

Step 4 — Convert to 0-100 scale using historical CDF:
```
FSSI_100_t = P(FSSI_t | FSSI history) × 100
```

**Threshold flags:**
- `FSSI > 70`: Significant financial stress (roughly: 2008-level or above)
- `FSSI > 85`: Severe financial stress (comparable to GFC peak or March 2020)

### 3.3 Stage 2: Economic Transmission Index (ETI)

This stage captures how financial stress translates into household economic pain. **Expected lag: 3-12 months after Stage 1.**

| Variable | Definition | Source | Series ID | Frequency |
|---|---|---|---|---|
| `unemp_delta` | 12-month change in unemployment rate | BLS CPS | FRED: UNRATE | Monthly |
| `claims` | Initial unemployment claims (4-week moving average) | DOL ETA | FRED: IC4WSA | Weekly |
| `hh_fragility` | % of households that cannot cover $400 emergency expense | Federal Reserve SHED survey | Fed SHED annual report | Annual |
| `real_wage_delta` | 12-month change in real average hourly earnings | BLS CES | FRED: CES0500000003 (nominal); deflate by CPIAUCSL | Monthly |
| `food_energy_CPI` | 12-month % change in food + energy CPI | BLS | FRED: CPIUFDSL (food); CPIENGSL (energy) | Monthly |
| `eviction_rate` | Eviction filing rate (per renter household) | Princeton Eviction Lab | evictionlab.org data downloads | Weekly (select cities); annual (national) |
| `consumer_conf` | Consumer Confidence Index (Conference Board) | Conference Board | FRED: CSCICP03USM665S | Monthly |
| `biz_failure` | Business bankruptcy filings | U.S. Courts / American Bankruptcy Institute | ABI quarterly filing statistics | Quarterly |

**ETI Computation:**

Step 1 — Normalize each variable. For variables where higher = worse stress:
```
n_i,t = P(x_i,t | 20-year rolling history)
```
For consumer_conf (higher = less stress):
```
n_conf,t = 1 - P(consumer_conf_t | 20-year rolling history)
```

Step 2 — Weighted composite:
```
ETI_t = 0.20 × n_unemp_delta + 0.15 × n_claims + 0.10 × n_hh_fragility
      + 0.15 × n_real_wage_delta + 0.15 × n_food_energy + 0.05 × n_eviction
      + 0.10 × n_consumer_conf + 0.10 × n_biz_failure
```

Weights rationale: Unemployment change and initial claims are the most responsive and visible indicators of economic pain. Food/energy prices have disproportionate impact on lower-income households. Consumer confidence captures the subjective dimension.

Step 3 — Scale to 0-100:
```
ETI_100_t = ETI_t × 100
```

### 3.4 Stage 3: Political Grievance Formation Index (PGFI)

This stage captures how economic hardship converts to political anger and system blame. **Expected lag: 3-6 months after Stage 2.**

| Variable | Definition | Source | Series ID | Frequency |
|---|---|---|---|---|
| `wrong_direction` | % saying country is on "wrong track" | RealClearPolitics average; Gallup | RCP average; Gallup: "Satisfaction with Direction" | ~Weekly (RCP aggregate); Monthly (Gallup) |
| `pres_disapproval` | Presidential disapproval rate | Gallup; FiveThirtyEight aggregate | Gallup presidential approval; 538 approval tracker | ~Daily (538); Monthly (Gallup) |
| `congress_disapproval` | Congressional disapproval rate | Gallup | Gallup: "Do you approve or disapprove of Congress?" | Monthly |
| `system_blame` | % who say "the system is rigged" or equivalent | Pew; Gallup; academic surveys | Pew political values surveys; ANES | Periodic (1-2x/year) |
| `anti_system_support` | Combined vote share of "outsider" / anti-establishment candidates in primaries | FEC; state election data | OpenSecrets; Dave Leip's Election Atlas; state SOS results | Per election cycle |
| `extremist_search` | Google Trends index for extremist-related search terms | Google Trends | trends.google.com (custom queries) | Daily/Weekly |

**PGFI Computation:**

Step 1 — Normalize each variable to 0-1 range using rolling 20-year percentiles.

Step 2 — Weighted composite:
```
PGFI_t = 0.25 × n_wrong_direction + 0.20 × n_pres_disapproval + 0.15 × n_congress_disapproval
       + 0.20 × n_system_blame + 0.15 × n_anti_system + 0.05 × n_extremist_search
```

Step 3 — Scale to 0-100.

### 3.5 Stage 4: Mobilization Activation Index (MAI)

This stage captures whether political grievance has translated into actual collective action. **Expected lag: 1-6 months after Stage 3.**

| Variable | Definition | Source | Series ID | Frequency |
|---|---|---|---|---|
| `protest_count` | Number of protest events per month | ACLED (US data, 2020+); Count Love (2017-2023) | ACLED data export (filter: US, event type: protests) | Weekly/Monthly |
| `protest_size` | Estimated total participants in protests per month | ACLED (size estimates where available) | ACLED data export | Monthly |
| `strike_workers` | Workers involved in work stoppages | BLS Work Stoppage Data | BLS: Major Work Stoppages | Monthly |
| `political_violence` | Political violence events (attacks, threats, armed demonstrations) | ACLED; START Global Terrorism Database | ACLED (filter: US, event type: violence against civilians, strategic developments) | Monthly |
| `far_vote_share` | Combined far-left + far-right vote share in most recent election | FEC; state election data | Requires manual classification of candidates | Per election cycle |
| `militia_activity` | Armed militia sightings / activities | ACLED; SPLC Hatewatch | ACLED armed group subcategory; SPLC tracking | Monthly |

**MAI Computation:**

Step 1 — Normalize each variable using rolling 5-year percentiles (shorter window because mobilization data is more recent and volatile):
```
n_i,t = P(x_i,t | x_i, t-60..t)    [5 years of monthly data]
```

Step 2 — Weighted composite:
```
MAI_t = 0.25 × n_protest_count + 0.20 × n_protest_size + 0.15 × n_strike_workers
      + 0.20 × n_political_violence + 0.10 × n_far_vote + 0.10 × n_militia
```

Step 3 — Scale to 0-100.

### 3.6 Transmission Modifiers

**Amplifiers** (increase transmission efficiency from one stage to the next):

| Amplifier | Metric | Source | Effect |
|---|---|---|---|
| Pre-existing inequality | Gini coefficient | Census | If Gini > 0.45: multiply transmission by 1.2 |
| Weak safety net | Social spending as % of GDP | OECD SOCX | If below OECD median: multiply by 1.15 |
| Elite division | DW-NOMINATE partisan distance | Poole/Rosenthal | If distance > 80th percentile historical: multiply by 1.15 |
| Upcoming election | Months to next presidential election | Calendar | If < 12 months: multiply by 1.2 |

**Dampeners** (reduce transmission efficiency):

| Dampener | Metric | Source | Effect |
|---|---|---|---|
| Strong fiscal response | Fiscal stimulus as % of GDP within 6 months of Stage 1 peak | CBO; BEA | If > 3% GDP: multiply by 0.7 |
| Bipartisan crisis response | Whether major relief legislation passed with bipartisan votes | Congressional Record | If yes: multiply by 0.8 |
| Central bank credibility | 5-year inflation expectations anchored near target | FRED: T5YIFR | If < 2.5%: multiply by 0.85 |

### 3.7 Master FS-PIP Computation

The model produces both a **current-state assessment** and a **forward-looking projection**:

**Current state:** Which stage is currently active?
```
active_stage_t =
    Stage 1 if FSSI > 60 AND ETI < 50
    Stage 2 if ETI > 50 AND PGFI < 50
    Stage 3 if PGFI > 50 AND MAI < 50
    Stage 4 if MAI > 50
    Dormant if FSSI < 40 AND ETI < 40
```

**Forward projection:** Based on empirical lag structure, forecast downstream stages:
```
If FSSI_t > 60 (Stage 1 active):
    Projected ETI peak: t + 6 months (range: t+3 to t+12)
    Projected PGFI peak: t + 12 months (range: t+6 to t+18)
    Projected MAI peak: t + 18 months (range: t+9 to t+24)
```

**Composite FS-PIP Score:**
```
FSPIP_t = max(FSSI_t, ETI_t, PGFI_t, MAI_t) × transmission_modifier
```

The max-based aggregation ensures the score reflects whichever stage is currently most elevated — the "leading edge" of the causal chain.

### 3.8 Lag Calibration

Based on U.S. historical episodes:

| Episode | Stage 1 Peak | Stage 2 Peak | Stage 3 Peak | Stage 4 Peak | Total Lag |
|---|---|---|---|---|---|
| 2008 Financial Crisis | Sep 2008 | Oct 2009 (~13mo) | Nov 2010 (~26mo) | Sep 2011 / Occupy (~36mo) | ~36 months |
| 2001 Dot-Com / 9/11 | Sep 2001 | Jun 2003 (~21mo) | 2004-2006 (diffuse) | Tea Party 2009 (~96mo) | Extended; interrupted by 9/11 rally effect |
| 2020 COVID Shock | Mar 2020 | Apr 2020 (~1mo) | Summer 2020 (~3mo) | Jan 2021 (~10mo) | ~10 months (compressed by simultaneous trigger) |

Average Stage 1 → Stage 4 lag: **10-36 months**, depending on shock speed and severity.

### 3.9 Data Pipeline Summary

```
STAGE 1 (Financial)              STAGE 2 (Economic)
┌──────────────────┐             ┌──────────────────┐
│ OFR FSI (daily)  │             │ BLS unemp (mo)   │
│ Yield curve (d)  │──3-12 mo──→│ Claims (weekly)   │
│ VIX (daily)      │    lag      │ CPI food/energy   │
│ Credit spread(d) │             │ Consumer conf     │
│ Mortgage delinq  │             │ Eviction rate     │
│ Bank stress      │             │ Biz bankruptcy    │
└────────┬─────────┘             └────────┬─────────┘
         │                                │
    FSSI (0-100)                     ETI (0-100)
                                          │
                    3-6 mo lag            │
                           ┌──────────────┘
                           ▼
                  STAGE 3 (Political)           STAGE 4 (Mobilization)
                  ┌──────────────────┐          ┌──────────────────┐
                  │ Wrong direction  │          │ Protest count    │
                  │ Pres disapproval │──1-6mo──→│ Protest size     │
                  │ System blame     │   lag    │ Strike activity  │
                  │ Anti-system vote │          │ Political violence│
                  │ Extremist search │          │ Far vote share   │
                  └────────┬─────────┘          └────────┬─────────┘
                           │                             │
                      PGFI (0-100)                  MAI (0-100)
                           │                             │
                           └──────────┬──────────────────┘
                                      ▼
                              FS-PIP Composite
                              + Active Stage ID
                              + Forward Projection
                              × Transmission Modifiers
```

---

---

# PHASE 2: BROADENING

---

## MODEL 4: EXPANDED REVOLUTION VULNERABILITY INDEX (RVI)

### 4.1 Theoretical Foundation

The Expanded RVI is the broadest model in the ensemble — a comprehensive dashboard covering economic, legitimacy, mobilization, demographic, and state capacity dimensions. It draws from Gurr (relative deprivation), Skocpol (state breakdown), Tilly (mobilization), Goldstone (demographics + elite competition), and Davies (J-curve).

**Critical architectural change from prior version:** The original RVI used a simple additive average: `RVI = (EPI + LSI + MPI + DSI + SFI) / 5`. Based on the literature review critique (see gap-analysis-literature-review.md §11), this specification adopts a **hybrid additive-multiplicative structure** with interaction terms.

### 4.2 Sub-Index 1: Economic Pressure Index (EPI)

| # | Metric | Definition | Source | Series ID | Freq |
|---|---|---|---|---|---|
| E1 | Gini Coefficient | Income inequality | Census CPS ASEC Table H-4 | FRED: GINIALLRF | Annual |
| E2 | Palma Ratio | Top 10% share / Bottom 40% share | Constructible from Census CPS income tables or WID | WID: sdiinc992j (decile shares) | Annual |
| E3 | Youth Unemployment | Unemployment rate ages 16-24 | BLS CPS | FRED: LNU04000012 (16-19); LNU04000036 (20-24) | Monthly |
| E4 | Housing Affordability | Median home price / Median household income | Census; NAR; FRED | FRED: MSPUS (median sale price) / MEHOINUSA672N | Quarterly / Annual |
| E5 | Real Wage Growth | 12-month % change in real average hourly earnings (production workers) | BLS CES | FRED: CES0500000003 / CPIAUCSL | Monthly |
| E6 | Food + Energy Price Spike | 12-month % change in food + energy CPI components | BLS | FRED: CPIUFDSL, CPIENGSL | Monthly |
| E7 | Household Debt Burden | Household debt service payments as % of disposable income | Fed | FRED: TDSP | Quarterly |
| E8 | Poverty Rate | Official poverty rate + Supplemental Poverty Measure | Census CPS ASEC | Census: POV-01; SPM research tables | Annual |
| E9 | Healthcare Cost Burden | Out-of-pocket health spending as % of income (bottom quintile) | BLS CEX; CMS | CEX Table 3001 (by income quintile) | Annual |

**EPI Computation:**

Step 1 — Normalize each metric to 0-100 risk score using historical percentile method:
```
For metrics where higher = more risk (E1, E2, E3, E4, E6, E7, E8, E9):
    score_i = P(x_i,t | 1970..t) × 100

For metrics where higher = less risk (E5 — real wage growth):
    score_i = (1 - P(x_i,t | 1970..t)) × 100
```

Step 2 — Apply threshold bonus (from prior work, §Step C):
```
If score_i >= 95: score_i = min(100, score_i + 5)
```

Step 3 — Weighted aggregation:
```
EPI = 0.15×E1 + 0.10×E2 + 0.15×E3 + 0.15×E4 + 0.10×E5 + 0.10×E6 + 0.10×E7 + 0.10×E8 + 0.05×E9
```

Weights rationale: Gini, youth unemployment, and housing affordability are the most empirically linked to unrest in the literature. Healthcare is U.S.-specific and less directly tied to mobilization.

---

### 4.3 Sub-Index 2: Legitimacy Stress Index (LSI)

| # | Metric | Definition | Source | Series ID | Freq |
|---|---|---|---|---|---|
| L1 | Trust in Federal Government | % "always/most of the time" | Pew Research Center | Pew public trust series | ~Quarterly |
| L2 | Trust in Congress | % with "great deal/quite a lot" of confidence | Gallup Confidence in Institutions | Gallup annual institutions poll | Annual |
| L3 | Confidence in Elections | % who believe votes are counted accurately | Gallup; MIT MEDSL | Gallup: "Confidence in elections" | Periodic |
| L4 | Affective Polarization | Feeling thermometer gap (own party vs. other party) | ANES; Pew Political Typology | ANES cumulative file: ft_dem, ft_rep | Biennial (ANES) |
| L5 | Polity Score Trajectory | Polity5 score and 5-year rate of change | Center for Systemic Peace | Polity5 dataset: polity2 variable | Annual |
| L6 | V-Dem Liberal Democracy Index | Continuous democracy score and trajectory | V-Dem Institute | v2x_libdem | Annual |
| L7 | Corruption Perception | CPI score for U.S. | Transparency International | TI CPI annual | Annual |
| L8 | Legislative Gridlock | % of salient issues on which Congress fails to act | Brookings / Binder Gridlock Score; GovTrack | Binder legislative gridlock series | Per Congress (2-year) |
| L9 | Judicial Legitimacy | Gallup confidence in Supreme Court | Gallup Confidence in Institutions | Gallup annual institutions poll | Annual |

**LSI Computation:**

Step 1 — Normalize. All legitimacy metrics are "higher = more legitimate = less risk," so invert:
```
For L1, L2, L3, L9 (trust/confidence metrics):
    score_i = (1 - P(x_i,t | 1970..t)) × 100

For L4 (polarization — higher = more risk):
    score_i = P(x_i,t | 1970..t) × 100

For L5, L6 (democracy scores — higher = more democratic = less risk):
    score_i = (1 - P(x_i,t | full history)) × 100

For L7 (CPI — higher = less corrupt = less risk):
    score_i = (1 - P(x_i,t | 1995..t)) × 100

For L8 (gridlock — higher = more gridlocked = more risk):
    score_i = P(x_i,t | 1947..t) × 100
```

Step 2 — Weighted aggregation:
```
LSI = 0.15×L1 + 0.10×L2 + 0.15×L3 + 0.15×L4 + 0.10×L5 + 0.10×L6 + 0.05×L7 + 0.10×L8 + 0.10×L9
```

---

### 4.4 Sub-Index 3: Mobilization Potential Index (MPI)

| # | Metric | Definition | Source | Series ID | Freq |
|---|---|---|---|---|---|
| M1 | Protest Event Count | Monthly count of protest events in U.S. | ACLED (2020+) | ACLED US export, event_type="Protests" | Weekly |
| M2 | Strike Activity | Workers involved in major work stoppages (annual) | BLS | BLS Work Stoppage Data | Annual |
| M3 | Social Media Penetration | % of U.S. adults on social media | Pew Internet surveys | Pew "Social Media Fact Sheet" | Annual |
| M4 | Armed Militia Groups | Active hate/antigovernment groups count | SPLC | SPLC Hate Map annual count | Annual |
| M5 | Union Density | Union membership as % of workforce | BLS | FRED: LUU0204899600A (union members / employed) | Annual |
| M6 | Voter Turnout Volatility | Standard deviation of turnout across last 3 election cycles | Census; U.S. Elections Project | electproject.org | Per election cycle |
| M7 | Internet Penetration | % of households with broadband internet | Census ACS; FCC | Census ACS: S2801; FCC Broadband Data | Annual |

**MPI Computation:**

Step 1 — Normalize (all metrics: higher = more mobilization capacity = more risk, except M5 which is ambiguous):
```
For M1, M2, M3, M4, M6, M7:
    score_i = P(x_i,t | available history) × 100

For M5 (union density — higher unions = more organized mobilization capacity):
    score_i = P(x_i,t | 1970..t) × 100
```

Note: Union density has declined from ~27% (1970) to ~10% (2024). Low union density means less *organized* collective action capacity but not necessarily less mobilization — decentralized digital mobilization has partially substituted. Score both:
```
M5_adjusted = max(score_M5, score_M3 × 0.5)    [floor M5 at half the social media score]
```

Step 2 — Weighted aggregation:
```
MPI = 0.25×M1 + 0.20×M2 + 0.15×M3 + 0.15×M4 + 0.10×M5_adj + 0.05×M6 + 0.10×M7
```

---

### 4.5 Sub-Index 4: Demographic Structural Index (DSI)

| # | Metric | Definition | Source | Series ID | Freq |
|---|---|---|---|---|---|
| D1 | Graduate Unemployment | Unemployment rate for bachelor's+ ages 25-34 | BLS CPS (by education) | BLS: Unpublished tables from CPS, Education/age cross-tabs | Monthly |
| D2 | Student Debt per Borrower | Average federal student loan balance | Dept of Education; NY Fed | FRED: SLOAS (total outstanding); Dept of Ed annual report | Quarterly |
| D3 | Intergenerational Wealth Gap | Ratio of median net worth (age 65+) to median net worth (age < 35) | Fed Survey of Consumer Finances | SCF summary tables by age of head | Triennial |
| D4 | Homeownership Gap (Generational) | Homeownership rate (age <35) / Homeownership rate (age 55+) | Census CPS Housing Vacancy Survey | Census: Table 7 (homeownership by age) | Quarterly |
| D5 | Deaths of Despair Rate | Drug overdose + suicide + alcohol-related deaths per 100k | CDC WONDER; NCHS | CDC WONDER: Multiple Cause of Death query | Annual |
| D6 | Youth Mental Health | % of high school students reporting persistent sadness/hopelessness | CDC YRBS (Youth Risk Behavior Survey) | CDC YRBS data | Biennial |
| D7 | Social Trust | % saying "most people can be trusted" | General Social Survey | GSS: TRUST variable | Biennial |
| D8 | Loneliness/Social Isolation | % of adults reporting loneliness | Cigna / Surgeon General data; Gallup | Cigna Loneliness Index; Gallup Social Series | Annual |

**DSI Computation:**

Step 1 — Normalize:
```
For D1, D2, D5, D6, D8 (higher = worse):
    score_i = P(x_i,t | available history) × 100

For D3 (wealth gap ratio — higher ratio = greater generational gap = worse):
    score_i = P(x_i,t | 1989..t) × 100    [SCF triennial since 1989]

For D4 (homeownership ratio — lower = worse for young):
    score_i = (1 - P(x_i,t | available history)) × 100

For D7 (social trust — higher = more trust = less risk):
    score_i = (1 - P(x_i,t | 1972..t)) × 100    [GSS since 1972]
```

Step 2 — Weighted aggregation:
```
DSI = 0.15×D1 + 0.15×D2 + 0.15×D3 + 0.10×D4 + 0.15×D5 + 0.10×D6 + 0.10×D7 + 0.10×D8
```

---

### 4.6 Sub-Index 5: State Fragility Index (SFI)

| # | Metric | Definition | Source | Series ID | Freq |
|---|---|---|---|---|---|
| S1 | Federal Debt to GDP | Federal debt held by public / GDP | CBO; FRED | FRED: GFDEGDQ188S | Quarterly |
| S2 | Debt Service Burden | Net interest / Federal revenue | CBO Budget Outlook | CBO: Table 1-1 | Annual |
| S3 | Government Effectiveness | World Bank WGI Government Effectiveness score, U.S. | World Bank WGI | WGI: GE.EST (U.S.) | Annual |
| S4 | Trust in Military | % with "great deal/quite a lot" of confidence | Gallup Confidence in Institutions | Gallup annual | Annual |
| S5 | Trust in Police | % with "great deal/quite a lot" of confidence | Gallup Confidence in Institutions | Gallup annual | Annual |
| S6 | Police Use-of-Force Deaths | Fatal police encounters per capita | Mapping Police Violence | mappingpoliceviolence.us data downloads | Annual |
| S7 | FEMA Disaster Response Rating | Post-disaster public satisfaction surveys | FEMA; Gallup post-disaster polls | FEMA after-action reports; Gallup | Per event |
| S8 | Rule of Law Index | World Justice Project overall score, U.S. | World Justice Project | WJP Rule of Law Index: U.S. profile | Annual |

**SFI Computation:**

Step 1 — Normalize:
```
For S1, S2, S6 (higher = weaker state):
    score_i = P(x_i,t | available history) × 100

For S3, S4, S5, S7, S8 (higher = stronger state = less risk):
    score_i = (1 - P(x_i,t | available history)) × 100
```

Step 2 — Weighted aggregation:
```
SFI = 0.20×S1 + 0.15×S2 + 0.10×S3 + 0.10×S4 + 0.15×S5 + 0.10×S6 + 0.05×S7 + 0.15×S8
```

---

### 4.7 RVI Master Aggregation

**Hybrid additive-multiplicative formula:**

Step 1 — Compute additive component (baseline):
```
RVI_additive = 0.25×EPI + 0.25×LSI + 0.20×MPI + 0.15×DSI + 0.15×SFI
```

Weights rationale: Economic pressure and legitimacy stress are the two strongest empirical predictors across multiple frameworks. Mobilization potential is the mechanism. Demographics and state capacity are structural conditions.

Step 2 — Compute interaction terms. These flag dangerous *combinations* (inspired by Turchin's multiplicative logic):
```
interaction_economic_legitimacy = (EPI/100) × (LSI/100) × 100
interaction_mobilization_weakness = (MPI/100) × (SFI/100) × 100
interaction_elite_youth = (DSI/100) × (EPI/100) × 100
```

Step 3 — Danger constellation bonus. When multiple sub-indices simultaneously exceed threshold (60):
```
n_elevated = count(sub-index > 60 for EPI, LSI, MPI, DSI, SFI)

constellation_bonus =
    0     if n_elevated <= 1
    5     if n_elevated == 2
    12    if n_elevated == 3
    22    if n_elevated == 4
    35    if n_elevated == 5
```

Step 4 — Final RVI:
```
RVI_raw = RVI_additive + 0.15 × max(interaction terms) + constellation_bonus
RVI = min(100, RVI_raw)
```

### 4.8 Interpretation Scale

| RVI Range | Risk Level | Description |
|---|---|---|
| 0-25 | Low | Structural conditions well within historical norms; strong institutions |
| 25-45 | Moderate | Some indicators elevated; system under pressure but absorbing it |
| 45-65 | Elevated | Multiple indicators elevated; structural conditions comparable to historical pre-unrest periods |
| 65-80 | High | Broad-based structural stress; comparable to worst U.S. historical episodes (1850s, 1930s, late 1960s) |
| 80-100 | Crisis | Structural conditions beyond any modern U.S. precedent; system fragility extreme |

---

---

## MODEL 5: PITF GLOBAL INSTABILITY MODEL (U.S. ADAPTATION)

### 5.1 Theoretical Foundation

The Political Instability Task Force model (Goldstone et al., 2010, *American Journal of Political Science*) achieved 80%+ accuracy in predicting instability onset using just four variables. This specification adapts the model for ongoing U.S. monitoring while preserving the original variable structure.

**Original PITF logistic regression:**
```
log(p / (1-p)) = β₀ + β₁(regime_type) + β₂(infant_mortality) + β₃(neighbor_conflict) + β₄(discrimination)
```

### 5.2 Variable Definitions — U.S. Adaptation

#### Variable 1: Regime Type (Primary Predictor)

| Sub-Variable | Definition | Source | Series ID | Freq |
|---|---|---|---|---|
| `polity` | Polity5 combined polity score (-10 to +10) | Center for Systemic Peace | Polity5: p5v2018.sav (polity2 variable) | Annual |
| `vdem_ldi` | V-Dem Liberal Democracy Index (0-1) | V-Dem Institute | v2x_libdem | Annual |
| `fh_score` | Freedom House combined score (0-100) | Freedom House | Freedom in the World: U.S. score | Annual |
| `eiu_type` | EIU Democracy Index classification | Economist Intelligence Unit | EIU Democracy Index annual | Annual |
| `factionalism` | Polity5 Factionalism coding (PARREG variable) | Polity5 | Polity5: parreg variable (5 = factionalized) | Annual |

**Regime Type Risk Computation:**

The PITF's critical finding: partial democracies (anocracies, Polity -5 to +5) are ~10x more unstable than full democracies; partial democracies *with factionalism* have 30x greater odds of instability.

Step 1 — Classify regime type:
```
If polity >= 6: regime_class = "full_democracy" (low risk)
If polity >= 1 AND polity <= 5: regime_class = "partial_democracy" (moderate risk)
If polity >= -5 AND polity <= 0: regime_class = "partial_autocracy" (high risk)
If polity <= -6: regime_class = "full_autocracy" (moderate risk)
```

Step 2 — Assign base risk score:
```
regime_score =
    10  if full_democracy
    55  if partial_democracy without factionalism
    75  if partial_democracy with factionalism (parreg = 5)
    85  if partial_autocracy with factionalism
    40  if full_autocracy
```

Step 3 — Trajectory adjustment. Apply the V-Dem and Freedom House trend to detect *movement toward* anocracy:
```
vdem_5yr_change = vdem_ldi_t - vdem_ldi_{t-5}
fh_5yr_change = fh_score_t - fh_score_{t-5}

If vdem_5yr_change < -0.05 OR fh_5yr_change < -5:
    regime_score = regime_score + 15    [democratic backsliding bonus]

If vdem_5yr_change < -0.10 OR fh_5yr_change < -10:
    regime_score = regime_score + 25    [severe backsliding bonus]
```

Step 4 — Walter cumulative compounding. If the country has been in anocracy range (polity <= 5) AND factionalism is present, accumulate risk:
```
years_in_anocracy_with_factionalism = count of consecutive years where polity <= 5 AND parreg = 5
cumulative_risk = 1 - (1 - 0.04)^years_in_anocracy_with_factionalism
```
4% annual civil war risk, compounding.

Step 5 — Cap and normalize:
```
V1_regime = min(100, regime_score + cumulative_risk × 100)
```

---

#### Variable 2: State Development / Governance Quality

The PITF uses infant mortality as a proxy for overall governance quality (not because infant mortality *causes* instability but because it is the best single predictor of state capacity and development).

| Sub-Variable | Definition | Source | Series ID | Freq |
|---|---|---|---|---|
| `infant_mort` | Infant mortality rate (deaths under 1 per 1,000 live births) | CDC NVSS; World Bank | FRED: SPDYNIMRTINUSA (World Bank); CDC WONDER | Annual |
| `gov_effectiveness` | World Bank Government Effectiveness estimate, U.S. | World Bank WGI | GE.EST | Annual |
| `life_expect` | Life expectancy at birth | CDC NVSS | CDC WONDER; FRED: SPDYNLE00INUSA | Annual |

**Governance Quality Score:**

Step 1 — The U.S. ranks well globally on infant mortality and governance but has been *declining relative to peers* — this trajectory matters more than absolute level for a wealthy democracy:
```
infant_mort_peer_ratio = US_infant_mortality / OECD_median_infant_mortality
```
A ratio of 1.0 = at peer level; higher = worse than peers. U.S. currently ~1.5x (5.4 vs. ~3.6 OECD median).

Step 2 — Track trajectory:
```
life_expect_change_5yr = life_expectancy_t - life_expectancy_{t-5}
```
The U.S. saw unprecedented declines (2019-2021: ~2.5 years lost).

Step 3 — Composite:
```
V2_governance = 0.40 × P(infant_mort_peer_ratio | 1960..t) × 100
              + 0.30 × (1 - P(gov_effectiveness | 1996..t)) × 100
              + 0.30 × (1 - P(life_expect_change_5yr | 1960..t)) × 100
```

---

#### Variable 3: Regional Conflict / External Pressure

The PITF uses "armed conflict in 4+ bordering states" as a binary predictor. For the U.S. (with only 2 land borders — Canada and Mexico — and maritime boundaries), this variable requires substantial adaptation.

| Sub-Variable | Definition | Source | Series ID | Freq |
|---|---|---|---|---|
| `mex_conflict` | Mexico organized violence fatalities (annual) | ACLED; IISS Armed Conflict Survey; Justice in Mexico project | ACLED: Mexico data export | Annual |
| `intl_conflict_exposure` | U.S. military personnel deployed in active conflict zones | DOD Personnel, Workforce Reports | DOD DMDC reports | Semi-annual |
| `sanctions_received` | Trade sanctions or restrictions targeting U.S. (count) | WTO; government reports | WTO Dispute Settlement database | Annual |
| `foreign_interference` | Documented foreign interference in U.S. elections / politics | DNI Threat Assessments; academic databases | DNI Annual Threat Assessment | Annual |

**External Pressure Score:**

For the U.S., the PITF "neighboring conflict" variable is near-irrelevant in its original form. Adapt to capture the broader concept of external destabilizing pressures:

```
V3_external = 0.30 × N(mex_conflict_t) × 100
            + 0.25 × N(intl_conflict_exposure_t) × 100
            + 0.20 × N(sanctions_received_t) × 100
            + 0.25 × N(foreign_interference_t) × 100
```

**Note:** This variable will likely be consistently low for the U.S., which is correct — the U.S. is largely buffered from external destabilization. The value of including it is that *if* external pressure increases (e.g., severe trade war, significant foreign interference campaign), the model captures it.

---

#### Variable 4: State-Led Discrimination

The PITF uses state-led political discrimination against minorities. For the U.S., this captures systematic disparities in state treatment by race, ethnicity, or political identity.

| Sub-Variable | Definition | Source | Series ID | Freq |
|---|---|---|---|---|
| `racial_incarceration` | Black-white incarceration rate ratio | BJS Prisoners in [year]; Sentencing Project | BJS: NCJ series; Sentencing Project race data | Annual |
| `voter_restriction` | Restrictive voting laws enacted (annual count) | Brennan Center for Justice | Brennan Center voting law trackers | Annual |
| `civil_rights_complaints` | Federal civil rights complaints filed | DOJ Civil Rights Division annual reports | DOJ CRD annual reports | Annual |
| `police_disparity` | Ratio of police fatal encounter rate (Black / White) | Mapping Police Violence | mappingpoliceviolence.us | Annual |
| `immigration_enforcement` | Immigration detention population | ICE ERO annual report; TRAC Syracuse | ICE ERO reports; TRAC data | Annual |

**State Discrimination Score:**
```
V4_discrimination = 0.25 × P(racial_incarceration_t | 1980..t) × 100
                  + 0.25 × P(voter_restriction_t | 2000..t) × 100
                  + 0.15 × P(civil_rights_complaints_t | 1990..t) × 100
                  + 0.20 × P(police_disparity_t | 2013..t) × 100
                  + 0.15 × P(immigration_enforcement_t | 2000..t) × 100
```

---

### 5.3 PITF Master Formula

**Adapted logistic model:**
```
PITF_logit = -3.5 + 0.035 × V1_regime + 0.020 × V2_governance + 0.010 × V3_external + 0.025 × V4_discrimination
```

Convert to probability:
```
PITF_probability = 1 / (1 + exp(-PITF_logit))
```

Scale to 0-100:
```
PITF_score = PITF_probability × 100
```

**Coefficient notes:** The original PITF coefficients were estimated on a global sample of instability events (1955-2003) using logistic regression. The coefficients above are illustrative adaptations — they preserve the *relative ordering* of the original model (regime type > discrimination > governance > neighbors) while adjusting the intercept and slopes to produce meaningful variation in the U.S. range. Proper calibration would require backtesting against comparable wealthy-democracy episodes.

### 5.4 Known Limitations for U.S. Application

1. The U.S. typically sits in the PITF's "low risk" zone (full democracy, low infant mortality, no neighboring conflict), which means the model has limited discrimination power in normal times
2. The model becomes highly relevant *if and when* the U.S. enters the anocracy zone — it functions as a "democratic backsliding alarm"
3. The V3 (external) variable contributes minimal signal for the U.S.
4. Coefficient calibration against U.S. historical episodes is not possible with standard statistical methods (N too small)

---

---

## MODEL 6: CRITICAL SLOWING DOWN (CSD) TIPPING POINT MODEL

### 6.1 Theoretical Foundation

Critical Slowing Down theory, drawn from complex systems science, posits that as a system approaches a tipping point (critical transition), it exhibits characteristic statistical signatures in its time series:

1. **Rising variance** — the system fluctuates more wildly
2. **Rising autocorrelation** — the system takes longer to recover from perturbations
3. **Flickering** — the system oscillates between two states before transitioning
4. **Skewness shift** — the distribution of system states becomes asymmetric

These are generic properties of dynamical systems approaching bifurcation points. They have been validated in ecology, climate science, financial markets, and (emerging) political systems.

### 6.2 Input Time Series

The CSD model does not define its own variables — it operates on time series from other models and indicators. The following are the primary input series, selected for length, frequency, and relevance:

| # | Series | Source | FRED / Access | Frequency | Start |
|---|---|---|---|---|---|
| TS1 | Consumer Sentiment Index | U. Michigan | FRED: UMCSENT | Monthly | 1952 |
| TS2 | Trust in Government | Pew / ANES | Pew public trust; ANES cumulative | ~Quarterly | 1958 |
| TS3 | Real Median Household Income | Census | FRED: MEHOINUSA672N | Annual | 1984 |
| TS4 | Labor Share of GDP | BLS / BEA | FRED: W270RE1A156NBEA | Quarterly | 1947 |
| TS5 | Gini Coefficient | Census | FRED: GINIALLRF | Annual | 1967 |
| TS6 | Partisan Distance (Congress) | DW-NOMINATE | Poole/Rosenthal voteview.com | Per Congress | 1879 |
| TS7 | Presidential Approval | Gallup | Gallup historical; FRED: USAGFCEAQDSMEI | Monthly | 1945 |
| TS8 | OFR Financial Stress Index | OFR | FRED: STLFSI4 (St. Louis Fed alt) | Weekly | 2000 |
| TS9 | Life Expectancy | CDC | CDC WONDER; FRED: SPDYNLE00INUSA | Annual | 1900 |
| TS10 | Top 1% Income Share | WID / Piketty-Saez | WID.world: sptinc992j | Annual | 1913 |

### 6.3 CSD Indicators — Computation

For each input time series, compute four CSD indicators using a **rolling window** approach.

#### Window Size Selection

```
window_size = max(20, length(series) / 5)
```

For monthly series: use 120-month (10-year) rolling windows.
For annual series: use 20-year rolling windows.
For very long series (TS6, TS10): use 30-year rolling windows.

#### Indicator 1: Rolling Variance

```
var_t = variance(x_{t-window+1}, ..., x_t)
```

Standardize the variance series to detect *trend* in variance:
```
var_trend_t = Mann-Kendall trend test statistic for var_{t-window+1}, ..., var_t
```

A significantly positive trend (p < 0.05) indicates rising variance — a CSD warning signal.

#### Indicator 2: Lag-1 Autocorrelation (AR1)

```
ar1_t = correlation(x_{t-window+1..t-1}, x_{t-window+2..t})
```

Rising AR1 indicates the system is becoming "sluggish" — taking longer to return from perturbations.

```
ar1_trend_t = Mann-Kendall trend test for ar1_{t-window+1}, ..., ar1_t
```

Significantly positive trend (p < 0.05) = CSD warning.

#### Indicator 3: Flickering (Bimodality)

Compute Hartigan's dip test for unimodality on the rolling window:

```
dip_t = HartiganDipTest(x_{t-window+1}, ..., x_t)
```

If dip test rejects unimodality (p < 0.05), the series is exhibiting bimodal behavior — flickering between two states.

#### Indicator 4: Skewness

```
skew_t = skewness(x_{t-window+1}, ..., x_t)
```

Increasing absolute skewness indicates the system's distribution is becoming asymmetric, potentially tilting toward a new state.

### 6.4 CSD Composite Score

Step 1 — For each time series, compute a CSD signal strength (0-1):
```
csd_signal_i,t = 0.35 × N(var_trend_i,t)      [variance trend, normalized]
              + 0.35 × N(ar1_trend_i,t)        [autocorrelation trend, normalized]
              + 0.15 × (1 if dip_test significant else 0)    [flickering binary]
              + 0.15 × N(|skew_i,t|)            [absolute skewness, normalized]
```

Step 2 — Aggregate across all time series:
```
CSD_composite_t = mean(csd_signal_i,t for i = 1..10)
```

Step 3 — Scale to 0-100:
```
CSD_score_t = CSD_composite_t × 100
```

### 6.5 CSD Alert Levels

| CSD Score | Alert Level | Interpretation |
|---|---|---|
| 0-20 | Green | No CSD signals detected; system appears resilient |
| 20-40 | Yellow | Emerging CSD signals in some series; monitor closely |
| 40-60 | Orange | Clear CSD signals across multiple series; system resilience declining |
| 60-80 | Red | Strong CSD signals; system approaching potential tipping point |
| 80-100 | Critical | CSD signals at or near maximum across most series; tipping point may be imminent |

### 6.6 Cross-Series Coherence

An additional signal: when CSD indicators *across different series* begin rising simultaneously, it suggests system-level fragility (not just domain-specific stress).

```
coherence_t = pairwise_correlation_mean(csd_signal_1,t, ..., csd_signal_10,t)
```

Rising coherence (i.e., CSD signals appearing together across unrelated domains — wages, trust, health, inequality — simultaneously) is a higher-order warning that the system is coupling together in a fragility-amplifying way.

**Coherence flag:**
```
If coherence_t > 0.6 AND CSD_score_t > 40: FLAG = "System-level fragility detected"
```

### 6.7 Limitations and Calibration Challenges

1. **No calibrated threshold**: CSD can detect "the system is becoming less resilient" but cannot say "the tipping point is at CSD = X." No wealthy democracy has crossed a political tipping point in the modern data era, so there is no calibration case.

2. **False positives**: CSD signals can appear in systems that are simply becoming more volatile without approaching a tipping point. The 2020 COVID shock produced massive CSD signals that partially reversed.

3. **Window size sensitivity**: Results depend on window size choice. Sensitivity analysis across multiple window sizes (5, 10, 15, 20 years for monthly data) is essential.

4. **Non-stationarity**: Long-term structural trends (declining trust, rising inequality) will produce apparent CSD signals even if the system is not near a tipping point but is simply in a secular trend. Detrending before analysis may be needed, but detrending itself involves subjective choices.

**Recommendation:** Report CSD scores with explicit uncertainty bands derived from sensitivity analysis across window sizes and detrending choices. Present CSD as a "directional fragility indicator" rather than a calibrated predictor.

### 6.8 Data Pipeline Summary

```
10 Input Time Series (monthly/annual)
         │
         ▼
    For each series, rolling window:
    ┌────────────────────────┐
    │ 1. Rolling variance    │
    │ 2. Lag-1 autocorrelat. │
    │ 3. Hartigan dip test   │
    │ 4. Rolling skewness    │
    └────────┬───────────────┘
             │
             ▼
    CSD signal per series (0-1)
             │
             ▼
    Mean across all series → CSD composite (0-100)
             │
             ▼
    Cross-series coherence check
             │
             ▼
    Alert level + coherence flag
```

---

---

# ENSEMBLE INTEGRATION

## How the Six Models Combine

### Ensemble Architecture

The six models are not averaged — they serve distinct roles:

```
┌─────────────────────────────────────────────────────┐
│                  ENSEMBLE OUTPUT                      │
│                                                       │
│  Composite Risk Score (0-100)                        │
│  + Active Risk Factors (narrative)                   │
│  + Forward Projections (FS-PIP lag structure)        │
│  + Fragility Assessment (CSD)                        │
│  + Alert Flags (J-curve, constellation, backsliding) │
└───────────────────────┬─────────────────────────────┘
                        │
         ┌──────────────┼──────────────┐
         ▼              ▼              ▼
   STRUCTURAL      BEHAVIORAL      SYSTEMIC
   PRESSURE        PERCEPTION      FRAGILITY
         │              │              │
    ┌────┴────┐    ┌────┴────┐    ┌────┴────┐
    │Turchin  │    │Prospect │    │  CSD    │
    │PSI      │    │Theory   │    │Tipping  │
    │         │    │PRM      │    │Point    │
    │Expanded │    │         │    │         │
    │RVI      │    │Financial│    │         │
    │         │    │Stress   │    │         │
    │PITF     │    │Pathway  │    │         │
    └─────────┘    └─────────┘    └─────────┘
```

### Composite Score Computation

```
structural_avg = 0.40 × PSI_display + 0.40 × RVI + 0.20 × PITF_score
behavioral_avg = 0.50 × PLI + 0.50 × FSPIP_score
systemic = CSD_score

composite = 0.45 × structural_avg + 0.35 × behavioral_avg + 0.20 × systemic
```

Weights rationale:
- **Structural (45%)**: Largest weight because structural conditions are the most empirically validated predictors and the most stable signals
- **Behavioral (35%)**: Perception and causal-chain dynamics capture how structural conditions translate to actual political behavior
- **Systemic (20%)**: CSD is directional and uncalibrated — it gets meaningful weight as a fragility check but not primary influence

### Divergence Alerts

When models disagree significantly, that divergence itself is informative:

```
If |structural_avg - behavioral_avg| > 25:
    FLAG: "Structural-Behavioral Divergence"
    If structural > behavioral: "Structural pressure high but not yet perceived by public"
    If behavioral > structural: "Public distress exceeds structural conditions — narrative/information-driven"

If CSD_score > 60 AND composite < 40:
    FLAG: "Hidden Fragility — system resilience declining despite moderate overall scores"

If FSPIP active_stage >= 2 AND PSI < 30:
    FLAG: "Acute economic shock hitting a structurally stable system — monitor for rapid cascade"
```

### Update Cadence

| Component | Fastest-Updating Input | Recommended Update Frequency |
|---|---|---|
| Turchin PSI | Wages (quarterly), debt (quarterly) | Quarterly |
| Prospect Theory PRM | Consumer sentiment (monthly), employment (monthly) | Monthly |
| Financial Stress Pathway | OFR FSI (daily), VIX (daily) | Stage 1: Weekly; Stages 2-4: Monthly |
| Expanded RVI | Mixed (monthly to annual) | Monthly (interpolating annual data) |
| PITF | Polity, V-Dem, infant mortality (annual) | Annually (with backsliding detection monthly via V-Dem updates) |
| CSD | Varies by input series | Quarterly (rolling window statistics are stable over short periods) |
| **Ensemble Composite** | — | **Monthly** (with weekly financial stress monitoring) |

---

# APPENDIX A: DATA ACCESS REFERENCE

## Free / Open Access Sources

| Source | URL | Registration Required | API Available |
|---|---|---|---|
| FRED (Federal Reserve Economic Data) | https://fred.stlouisfed.org | No | Yes (free API key) |
| BLS Public Data API | https://api.bls.gov/publicAPI/v2/ | API key recommended | Yes (free) |
| Census Bureau Data API | https://api.census.gov/data.html | API key recommended | Yes (free) |
| World Inequality Database | https://wid.world | No | Yes (bulk download) |
| V-Dem Institute | https://www.v-dem.net/data/ | Registration required | Bulk download (free) |
| ACLED | https://acleddata.com | Registration required | Yes (free for researchers) |
| FRED / OFR Financial Stress | https://fred.stlouisfed.org/series/STLFSI4 | No | Yes (via FRED API) |
| CDC WONDER | https://wonder.cdc.gov | No | Query-based (no batch API) |
| Opportunity Insights | https://opportunityinsights.org/data/ | No | Bulk download |
| DW-NOMINATE / Voteview | https://voteview.com/data | No | Bulk download |
| Polity5 | https://www.systemicpeace.org/inscrdata.html | No | Bulk download |
| Freedom House | https://freedomhouse.org/report/freedom-world | No | Bulk download |
| Mapping Police Violence | https://mappingpoliceviolence.us | No | Bulk download |
| OpenSecrets | https://www.opensecrets.org/open-data | Registration for bulk | Yes (API + bulk) |
| Pew Research Center | https://www.pewresearch.org/datasets/ | Registration required | Dataset downloads |
| General Social Survey | https://gssdataexplorer.norc.org | Registration required | Query-based |
| World Bank WGI | https://info.worldbank.org/governance/wgi/ | No | Bulk download |
| World Justice Project | https://worldjusticeproject.org/rule-of-law-index/ | No | Reports + data |
| UN Population Division | https://population.un.org/wpp/ | No | Bulk download |
| IMF WEO | https://www.imf.org/en/Publications/WEO | No | Bulk download |
| Eviction Lab | https://evictionlab.org/map/ | No | Query + download |
| Transparency International CPI | https://www.transparency.org/en/cpi | No | Bulk download |
| Google Trends | https://trends.google.com | Google account | Pytrends (unofficial) |
| SPLC Hate Map | https://www.splcenter.org/hate-map | No | Manual or scrape |

## Paid / Restricted Sources

| Source | Content | Access |
|---|---|---|
| Economist Intelligence Unit Democracy Index | Full methodology and country scores | Subscription ($) |
| Gallup full microdata | Confidence in Institutions, Presidential Approval, full time series | Gallup Analytics subscription |
| ANES full cumulative file | Complete survey data 1948-present | Free registration at electionstudies.org |
| Conference Board Consumer Confidence | Full historical series | Subscription (available via FRED with lag) |
| Brennan Center voting law data | Restrictive/expansive voting law tracking | Free reports; bulk data by request |

---

# APPENDIX B: KNOWN CALIBRATION CHALLENGES

1. **No training data for wealthy democracy revolution.** All models are calibrated against contexts fundamentally different from the modern U.S. Thresholds and coefficients should be treated as informed estimates, not empirical calibrations.

2. **The N-of-1 problem.** The U.S. is a single case. Backtesting against historical U.S. episodes (1968, 1992, 2011, 2020) provides only 4-5 data points — far too few for statistical validation.

3. **Structural breaks.** The information environment (social media, 24-hour news) fundamentally changed after ~2008. Models calibrated on pre-2008 dynamics may not capture digitally-mediated mobilization and grievance formation.

4. **Turchin's multiplicative structure** was derived from pre-industrial and early-modern societies. The specific functional form may not hold for a post-industrial service economy.

5. **PITF coefficients** were estimated on a global sample dominated by developing-country instability events. The adapted coefficients in this specification are illustrative and require formal estimation against comparable cases.

6. **CSD thresholds** are uncalibrated for political systems. The statistical signals are theoretically grounded but the "how high is dangerous?" question has no empirical answer for this domain.

**Recommended mitigation:** Treat all model outputs as *relative* indicators (rising/falling, better/worse than historical baseline) rather than *absolute* probabilities. The ensemble's value is in detecting directional trends and dangerous combinations, not in producing precise risk percentages.
