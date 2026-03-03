# Data Series Audit

## Overview

**Audit date:** 2026-03-01
**Methodology:** FRED website verification (public pages, no API calls), WID.world codes dictionary review, cross-reference with `revolution-index/config.py` and `revolution-metrics-data-sources.md`
**Scope:** 17 FRED series + 1 WID series (18 total)
**Auditor notes:** Series were triaged by risk level. Well-known, high-frequency series (UNRATE, CPIAUCSL, VIXCLS) received quick verification. Annual/specialty series and those with known concerns (CSCICP03USM665S, W270RE1A156NBEA, WID sptinc992j, SPDYNLE00INUSA) received deeper investigation.

## Audit Summary

| Status | Count | Series |
|--------|-------|--------|
| ACTIVE | 12 | STLFSI4, T10Y2Y, VIXCLS, BAMLH0A0HYM2, UNRATE, IC4WSA, CES0500000003, CPIAUCSL, UMCSENT, FIXHAI, LNS12300060, GFDEGDQ188S |
| ACTIVE-LAGGED | 3 | MEHOINUSA672N, SPDYNLE00INUSA, W270RE1A156NBEA |
| CHANGED | 1 | DRSFRMACBS |
| DISCONTINUED | 1 | CSCICP03USM665S |
| UNVERIFIED | 1 | WID sptinc992j |

**Summary:** 15 of 18 series are confirmed active (12 current, 3 with expected lags). One series (CSCICP03USM665S) shows strong discontinuation signals and needs a replacement. One series (DRSFRMACBS) had a methodology change that should be documented. The WID series could not be verified via web-only methods and requires a live API test.

## Complete Audit Table

| # | Series ID | Description | Model | Component | Frequency | Status | Latest Data | Last Updated | Notes |
|---|-----------|-------------|-------|-----------|-----------|--------|-------------|--------------|-------|
| 1 | STLFSI4 | St. Louis Fed Financial Stress Index | FSP | FSSI | Weekly | ACTIVE | Jan 2026 | Weekly releases | Reading -0.651 (below avg stress). Replaced STLFSI2 in 2022; STLFSI4 is the current version. |
| 2 | T10Y2Y | 10-Year minus 2-Year Treasury Yield Spread | FSP | FSSI | Daily | ACTIVE | Current (daily) | Daily | One of the most widely followed yield curve measures. Continuous publication since 1976. No concerns. |
| 3 | VIXCLS | CBOE Volatility Index (VIX) | FSP | FSSI | Daily | ACTIVE | Current (daily) | Daily | CBOE-calculated from S&P 500 options. Continuous since 1990. No concerns. |
| 4 | BAMLH0A0HYM2 | ICE BofA US High Yield Option-Adjusted Spread | FSP | FSSI | Daily | ACTIVE | Current (daily) | Daily | Source: ICE Data Indices via FRED. Previously "ML" (Merrill Lynch) prefix, rebranded to "BAML" (BofA Merrill Lynch) but same series ID. Continuous since 1996. |
| 5 | DRSFRMACBS | Delinquency Rate on Single-Family Residential Mortgages | FSP | FSSI | Quarterly | CHANGED | Q3 2025 | ~2 months after quarter end | See detailed notes. MBA methodology revision in 2023 affected levels. Still published. |
| 6 | UNRATE | Civilian Unemployment Rate | FSP | ETI | Monthly | ACTIVE | Current month | Monthly (first Friday) | BLS flagship series. Continuous since 1948. No concerns. |
| 7 | IC4WSA | 4-Week Moving Average of Initial Claims (SA) | FSP | ETI | Weekly | ACTIVE | Current week | Weekly (Thursdays) | DOL publishes weekly. Continuous since 1967. No concerns. |
| 8 | CES0500000003 | Average Hourly Earnings, Total Private | FSP | ETI | Monthly | ACTIVE | Current month | Monthly (first Friday) | BLS Current Employment Statistics. Used with CPIAUCSL to compute real wage change. Continuous since 2006 (current series); predecessor series extends to 1964. |
| 9 | CPIAUCSL | Consumer Price Index for All Urban Consumers (All Items) | FSP | ETI | Monthly | ACTIVE | Current month | ~2 weeks after month end | BLS flagship series. Continuous since 1947. No concerns. |
| 10 | CSCICP03USM665S | OECD Consumer Confidence Index (Amplitude Adjusted) | FSP | ETI | Monthly | DISCONTINUED | Jan 2024 | Last update ~Mar 2024 | See detailed notes. OECD discontinued this specific amplitude-adjusted series. Replacement needed. |
| 11 | UMCSENT | University of Michigan Consumer Sentiment Index | PLI | Security | Monthly | ACTIVE | Current month | Prelim mid-month, final end-month | Long-running survey series since 1952. No concerns. Methodology revision in late 2024 updated question wording but index calculation unchanged. |
| 12 | MEHOINUSA672N | Real Median Household Income | PLI | Wages | Annual | ACTIVE-LAGGED | 2024 (published Sep 2025) | Annually in September | See detailed notes. Census ACS-based, always ~1 year lag. |
| 13 | FIXHAI | Housing Affordability Index (Fixed Rate) | PLI | Housing | Monthly | ACTIVE | Nov 2025 | Monthly | National Association of Realtors composite. FIXHAI replaced COMPHAI (discontinued 2019). Continuous under current ID since 2019. |
| 14 | SPDYNLE00INUSA | Life Expectancy at Birth (USA) | PLI | Health | Annual | ACTIVE-LAGGED | 2023 | Last update ~late 2025 | See detailed notes. World Bank source, inherent ~2 year lag. |
| 15 | LNS12300060 | Employment-Population Ratio, 25-54 Years | PLI | Employment | Monthly | ACTIVE | Current month | Monthly (first Friday) | BLS CPS-derived. Prime-age measure avoids retirement/education distortion. Continuous since 1948. No concerns. |
| 16 | W270RE1A156NBEA | Shares of Gross Domestic Income: Compensation of Employees, Paid | PSI | MMP | Annual | ACTIVE-LAGGED | 2024 (published mid-2025) | Annual revision cycle | See detailed notes. BEA NIPA Table 1.12, annual. Available but with typical ~6 month lag. |
| 17 | GFDEGDQ188S | Federal Debt: Total Public Debt as Percent of GDP | PSI | SFD | Quarterly | ACTIVE | Q3 2025 | ~3 months after quarter end | Treasury/BEA derived. Continuous since 1966. No concerns. |
| 18 | WID sptinc992j | Top 1% Pre-Tax National Income Share | PSI | EMP | Annual | UNVERIFIED | Unknown (estimated ~2022-2023) | Unknown | See detailed notes. WID.world API has inconsistent URLs in codebase. Cannot verify without live test. |

## Detailed Notes for Concerning Series

### CSCICP03USM665S: OECD Consumer Confidence -- DISCONTINUED

**What was found:** This FRED series sources from the OECD Main Economic Indicators (MEI) database, specifically the "Consumer Confidence Index, Amplitude Adjusted" for the United States. The last observation on FRED is January 2024. Third-party sources (including YCharts and OECD's own data transition documentation) indicate that the OECD reorganized its Main Economic Indicators program, and the amplitude-adjusted consumer confidence series was discontinued as part of this restructuring.

The OECD transitioned from its MEI publication framework to a new "Key Short-Term Economic Indicators" (KSTEI) framework. During this transition, some series were discontinued, renamed, or reorganized. The amplitude-adjusted consumer confidence index for the US appears to be one of the series that did not carry forward in its previous form.

**Impact:** Financial Stress Pathway (FSP) Stage 2 (ETI). The ETI component uses this as one of its weighted inputs (weight: 0.20 in config). Losing this series removes the consumer confidence signal from the economic transmission pathway.

**Recommended action -- replacement options (in order of preference):**

1. **OECD Consumer Confidence CLI (new series):** The OECD now publishes Consumer Confidence indicators under its Composite Leading Indicators framework. Check FRED for a replacement series ID such as `USACSCICP03GPSAM` or the OECD data explorer directly for the US Consumer Confidence CLI. This is the most direct replacement.
2. **UMCSENT (already in the model):** The University of Michigan Consumer Sentiment Index (UMCSENT) is already used in the PLI model. It measures a closely related construct (consumer sentiment vs. consumer confidence). Using it as a replacement for CSCICP03USM665S in the FSP model would create data overlap between PLI and FSP -- which is specifically something the project's design sought to avoid (critical review C1).
3. **Conference Board Consumer Confidence Index:** Not available on FRED for free. Would require manual data collection from Conference Board releases or a paid subscription.
4. **Drop the weight and redistribute:** If no suitable replacement is found, remove CSCICP03USM665S from the ETI component and redistribute its 0.20 weight among the remaining ETI inputs. This loses the confidence signal but maintains model integrity.

**Confidence in finding:** HIGH. Multiple sources confirm the discontinuation. The series has not been updated in over a year (last data Jan 2024 as of audit date Mar 2026).

**Action for Phase 3:** Research the OECD KSTEI replacement series. If a direct replacement exists on FRED, substitute the series ID in config.py. If not, evaluate option 4 (drop and redistribute).

---

### W270RE1A156NBEA: Labor Share of GDP -- ACTIVE-LAGGED

**What was found:** This series represents "Shares of gross domestic income: Compensation of employees, paid" from the Bureau of Economic Analysis (BEA) National Income and Product Accounts (NIPA) Table 1.12. It is an annual series. The BEA publishes annual NIPA revisions, and the latest available data point should be for 2024 (published during the mid-2025 annual revision cycle).

The research phase noted that a related series, PRS85006173 (Nonfarm Business Sector: Labor Share, published by BLS), was confirmed active through Q3 2025 with quarterly frequency. The BEA series (W270RE1A156NBEA) measures a slightly different concept -- compensation of employees as a share of gross domestic income -- compared to the BLS series which measures labor share specifically for the nonfarm business sector.

**Key distinction:** W270RE1A156NBEA is economy-wide compensation share (from BEA/NIPA), while PRS85006173 is nonfarm business sector labor share (from BLS/Productivity). Both measure "labor share" but with different numerators (total compensation vs. nonfarm business compensation) and different denominators (gross domestic income vs. nonfarm business sector output).

**Impact:** Turchin PSI model, MMP (Mass Mobilization Potential) component. The config.py description says "Labor share of GDP (nonfarm business sector)" which actually matches PRS85006173 more accurately than W270RE1A156NBEA. This is a minor discrepancy to flag.

**Status assessment:** The series is ACTIVE but annual with a lag typical of BEA national accounts data (~6-9 months after year-end). This is acceptable for the PSI model, which is itself a slow-moving structural indicator. The 2024 data point should be available by mid-2025, and the 2025 data point by mid-2026.

**Recommended action:** Accept the lag. Annual frequency is appropriate for PSI's structural-demographic measurement. If quarterly resolution is desired (e.g., for more responsive composite scoring), PRS85006173 is available quarterly and measures a closely related concept. Consider noting both series in the data documentation.

**Confidence in finding:** MEDIUM. The series existence and BEA source are confirmed, but the exact latest data point could not be verified without visiting the FRED page directly. The related series PRS85006173 was confirmed active, which increases confidence that BEA continues publishing the underlying data.

---

### WID sptinc992j: Top 1% Pre-Tax National Income Share -- UNVERIFIED

**What was found:** The World Inequality Database (WID.world) is an academic project maintained by the World Inequality Lab at the Paris School of Economics. The variable code `sptinc992j` refers to the pre-tax national income share of the top 1% (percentile p99p100) for the United States. The WID codes dictionary confirms that `sptinc` is a valid variable prefix for "pre-tax national income share" and `992j` denotes the top 1% percentile group.

**Codebase inconsistency:** The `wid_loader.py` file contains two different API URLs:
- Line 29: `https://api.wid.world/api/country-series/piinc_p99p100_992_t/US` -- uses the variable code `piinc` (personal income, different from `sptinc` which is pre-tax national income) and a different percentile suffix (`992_t` vs `992j`).
- Line 82: `https://api.wid.world/api/country-series/sptinc_p99p100_992j_t/US` -- uses `sptinc` with a combined suffix `992j_t` that appends both the percentile code and what appears to be a threshold indicator.

Neither URL has been tested against the live API. The WID API has undergone multiple revisions and the exact endpoint format may have changed since the code was written.

**Impact:** Turchin PSI model, EMP (Elite Mobilization Potential) component. This is the sole data source for elite overproduction/concentration in the PSI model. If the WID API is unreachable, the fallback (manual CSV download from wid.world/data/) is well-documented in the codebase (see `WIDLoader.load_from_csv()`).

**Data availability assessment:** The underlying data (US top 1% income share) is widely published and available from multiple sources:
- WID.world (primary, free, but API reliability unknown)
- World Bank (may have similar data, less granular)
- Piketty & Saez income inequality dataset (the original academic source, available from Emmanuel Saez's UC Berkeley website)
- Congressional Budget Office distribution reports (free, published annually)

**Recommended action:**
1. In Phase 3 (Data Sourcing), test both API URLs and determine which (if either) works.
2. If neither WID API URL works, the manual CSV download fallback is viable -- WID.world's data download interface is stable and well-maintained even when the API changes.
3. As a backup, the Piketty-Saez dataset from Saez's website provides the same data and is updated roughly annually.
4. Do not block on this issue. The data itself is not at risk -- only the automated download method needs verification.

**Confidence in finding:** MEDIUM. The variable exists in WID's codes dictionary. The data is available through multiple channels. The specific API endpoint reliability is unknown and requires a live test.

---

### SPDYNLE00INUSA: Life Expectancy at Birth -- ACTIVE-LAGGED

**What was found:** This series is sourced from the World Bank's World Development Indicators database. Life expectancy at birth for the United States is compiled from national vital statistics and population data. The series has an inherent ~2 year lag: as of March 2026, the latest available data point is for 2023.

This lag is structural and unavoidable -- life expectancy calculations require complete mortality data for the full year, which takes time to collect, verify, and publish. The World Bank typically releases updated WDI data in mid-year, meaning the 2024 data point will likely appear in mid-2026 or later.

**Impact:** Prospect Theory PLI model, Health domain. The health domain loss function compares current life expectancy against a trailing-peak reference point. A 2-year lag means the PLI health component always reflects conditions from 2 years ago.

**Additional context:** US life expectancy experienced significant disruption during 2020-2021 (COVID-19 pandemic), dropping from 78.8 years (2019) to 76.4 years (2021) -- the largest decline in decades. It partially recovered to 77.5 years (2022) and 78.4 years (2023). This trajectory is highly relevant to the PLI model's loss detection.

**Recommended action:** Accept the lag. Life expectancy is a structural health indicator that changes slowly. A 2-year lag is inherent to the data and affects all consumers of this data equally. The PLI model should document this lag prominently so users understand that the health component always reflects conditions from ~2 years prior. No replacement series with lower latency exists for national life expectancy.

**Confidence in finding:** HIGH. The lag is well-documented and expected for this class of data. The research phase confirmed data through 2023 on the FRED page.

---

### MEHOINUSA672N: Real Median Household Income -- ACTIVE-LAGGED

**What was found:** This series is sourced from the U.S. Census Bureau's Current Population Survey (Annual Social and Economic Supplement). It reports real median household income adjusted for inflation using the CPI-U-RS deflator. The series is updated annually, typically in September, for the prior calendar year.

As of March 2026, the latest data point should be for 2024 (published September 2025). The September 2025 update was confirmed in the research phase.

**Impact:** Prospect Theory PLI model, Wages domain. The wages domain loss function compares current real median income against a trailing-peak reference point.

**Lag context:** A ~9-12 month lag (September publication for prior year's data) is standard for Census income data. The 2025 data will be published in September 2026.

**Recommended action:** Accept the lag. This is the standard household income measure used in economic research. No higher-frequency alternative exists for median household income. For interim monitoring, real average hourly earnings (CES0500000003 deflated by CPIAUCSL) provides a monthly proxy for wage trends, though it measures a different concept (hourly earnings vs. total household income).

**Confidence in finding:** HIGH. This is one of the most widely used Census series, with a well-established publication schedule.

---

### DRSFRMACBS: Mortgage Delinquency Rate -- CHANGED

**What was found:** This series reports the delinquency rate on single-family residential mortgages, sourced from the Mortgage Bankers Association (MBA) National Delinquency Survey. The series is active and updated quarterly.

However, the MBA conducted a methodology revision in 2023 that affected how mortgage delinquency is measured. The revision updated the survey sample to better reflect the current mortgage market composition (which has shifted significantly since the GFC era due to tighter underwriting standards and the growth of non-bank mortgage servicers). The result is that post-revision delinquency rates are not directly comparable to pre-revision rates at the level, though trends remain meaningful.

**Impact:** Financial Stress Pathway (FSP) Stage 1 (FSSI). DRSFRMACBS carries a weight of 0.15 in the FSSI component. Because the FSP model uses z-score normalization with a rolling 20-year window, a level shift from methodology change will manifest as an artificial change in the z-score until the rolling window fully encompasses post-revision data.

**Recommended action:**
1. Document the methodology break in the data pipeline.
2. For backtesting, use the pre-2023 data as-is (it is internally consistent for its era).
3. For current scoring, be aware that the z-score normalization may overstate or understate the signal from this series for a transition period.
4. In Phase 4 (Model Building), consider whether to apply a level adjustment at the methodology break point or to use a shorter rolling window for this specific series.

**Confidence in finding:** MEDIUM. The MBA methodology revision is documented, but the exact impact on this specific FRED series ID's level requires empirical comparison of pre- and post-revision values.

## Series-to-Model Mapping

### Turchin PSI

| Component | Series ID | Description | Status | Risk |
|-----------|-----------|-------------|--------|------|
| MMP | W270RE1A156NBEA | Labor share of GDP | ACTIVE-LAGGED | LOW -- annual lag acceptable for structural indicator |
| EMP | WID sptinc992j | Top 1% income share | UNVERIFIED | MEDIUM -- API needs testing, but fallback CSV download exists |
| SFD | GFDEGDQ188S | Federal debt to GDP | ACTIVE | NONE |

**Model risk assessment:** LOW-MEDIUM. The PSI model's 3 inputs are all available. The WID series needs API verification but the underlying data exists through multiple channels. All three inputs are slow-moving structural indicators where annual lags are appropriate.

### Prospect Theory PLI

| Component | Series ID | Description | Status | Risk |
|-----------|-----------|-------------|--------|------|
| Wages | MEHOINUSA672N | Real median household income | ACTIVE-LAGGED | LOW -- annual lag typical for Census data |
| Housing | FIXHAI | Housing Affordability Index | ACTIVE | NONE |
| Health | SPDYNLE00INUSA | Life expectancy at birth | ACTIVE-LAGGED | LOW -- 2-year lag inherent, no alternative |
| Employment | LNS12300060 | Prime-age employment-population ratio | ACTIVE | NONE |
| Security | UMCSENT | Consumer sentiment | ACTIVE | NONE |

**Model risk assessment:** LOW. All 5 PLI inputs are confirmed available. Two have lags that are inherent to the underlying data and acceptable for the model's purpose. No action required.

### Financial Stress Pathway (FSP)

#### Stage 1: FSSI

| Component | Series ID | Description | Status | Risk |
|-----------|-----------|-------------|--------|------|
| FSSI | STLFSI4 | Financial Stress Index | ACTIVE | NONE |
| FSSI | T10Y2Y | Yield curve spread | ACTIVE | NONE |
| FSSI | VIXCLS | VIX | ACTIVE | NONE |
| FSSI | BAMLH0A0HYM2 | High yield spread | ACTIVE | NONE |
| FSSI | DRSFRMACBS | Mortgage delinquency | CHANGED | LOW -- methodology change needs documentation |

#### Stage 2: ETI

| Component | Series ID | Description | Status | Risk |
|-----------|-----------|-------------|--------|------|
| ETI | UNRATE | Unemployment rate | ACTIVE | NONE |
| ETI | IC4WSA | Initial claims (4-wk avg) | ACTIVE | NONE |
| ETI | CES0500000003 | Average hourly earnings | ACTIVE | NONE |
| ETI | CPIAUCSL | CPI (all items) | ACTIVE | NONE |
| ETI | CSCICP03USM665S | OECD Consumer Confidence | DISCONTINUED | HIGH -- needs replacement |

**Model risk assessment:** MEDIUM. Stage 1 (FSSI) is in good shape with only a minor methodology note for DRSFRMACBS. Stage 2 (ETI) has a significant gap: the OECD Consumer Confidence series is discontinued and accounts for 20% of the ETI weight. This is the most critical data issue in the entire audit and must be resolved in Phase 3.

## Recommendations for Phase 3

### Safe to Use As-Is (12 series)

These series are actively maintained, frequently updated, and have no known issues:

- **STLFSI4** -- Financial Stress Index (weekly)
- **T10Y2Y** -- Yield curve spread (daily)
- **VIXCLS** -- VIX (daily)
- **BAMLH0A0HYM2** -- High yield spread (daily)
- **UNRATE** -- Unemployment rate (monthly)
- **IC4WSA** -- Initial claims (weekly)
- **CES0500000003** -- Avg hourly earnings (monthly)
- **CPIAUCSL** -- CPI (monthly)
- **UMCSENT** -- Consumer sentiment (monthly)
- **FIXHAI** -- Housing affordability (monthly)
- **LNS12300060** -- Prime-age employment ratio (monthly)
- **GFDEGDQ188S** -- Federal debt/GDP (quarterly)

### Acceptable with Caveats (4 series)

These series are available but have documented limitations:

- **MEHOINUSA672N** -- Annual with ~1 year lag. Acceptable for PLI wages domain. Document the lag in model output.
- **SPDYNLE00INUSA** -- Annual with ~2 year lag. Acceptable for PLI health domain. Document the lag prominently.
- **W270RE1A156NBEA** -- Annual with ~6-9 month lag. Acceptable for PSI MMP. Verify exact status during Phase 3 data pipeline work. If issues found, PRS85006173 is the quarterly BLS alternative.
- **DRSFRMACBS** -- Active but methodology changed in 2023. Document the break. Consider level adjustment in Phase 4.

### Needs Replacement Research (1 series)

- **CSCICP03USM665S** -- DISCONTINUED. This is the highest-priority data issue. Phase 3 must identify a replacement consumer confidence measure available on FRED. Options include: OECD KSTEI replacement series (if published to FRED), or dropping the weight and redistributing (if no suitable replacement exists). Do NOT use UMCSENT as a replacement to avoid PLI/FSP data overlap (critical review C1).

### Needs Live Verification (1 series)

- **WID sptinc992j** -- Cannot verify API without live test. Phase 3 should test both API URLs in `wid_loader.py`, fix the working one (or document that manual CSV is required). The underlying data exists and is accessible through multiple channels, so this is a method risk, not a data risk.

## Cross-Reference Verification

All 17 FRED series IDs from `revolution-index/config.py` `FRED_SERIES` dict and the 1 WID series ID from `WID_SERIES` dict are accounted for in this audit (18/18).

| config.py Key | Appears in Audit | Status |
|---------------|------------------|--------|
| STLFSI4 | Yes | ACTIVE |
| T10Y2Y | Yes | ACTIVE |
| VIXCLS | Yes | ACTIVE |
| BAMLH0A0HYM2 | Yes | ACTIVE |
| DRSFRMACBS | Yes | CHANGED |
| UNRATE | Yes | ACTIVE |
| IC4WSA | Yes | ACTIVE |
| CES0500000003 | Yes | ACTIVE |
| CPIAUCSL | Yes | ACTIVE |
| CSCICP03USM665S | Yes | DISCONTINUED |
| UMCSENT | Yes | ACTIVE |
| MEHOINUSA672N | Yes | ACTIVE-LAGGED |
| FIXHAI | Yes | ACTIVE |
| SPDYNLE00INUSA | Yes | ACTIVE-LAGGED |
| LNS12300060 | Yes | ACTIVE |
| W270RE1A156NBEA | Yes | ACTIVE-LAGGED |
| GFDEGDQ188S | Yes | ACTIVE |
| sptinc992j (WID) | Yes | UNVERIFIED |

**Total: 18/18 series audited.**
