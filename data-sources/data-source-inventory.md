# Data Source Inventory: Revolution and Political Instability Variables

**Date:** 2026-03-04
**Phase:** 03 - Data Sourcing
**Purpose:** Map all 45 concept-level variables from Phase 2's ranked catalog to concrete, freely available data sources with verified metadata. This document serves as both a methodology reference for academic transparency and a developer-ready input for Phase 4 (Model Building).

**Source Catalog:** See `literature/variable-catalog.md` for theoretical evidence, ratings, and measurement approaches.

---

## Methodology

### Proxy Tier Definitions

This inventory uses a strict two-tier proxy system. No weak or speculative proxies are included.

| Tier | Definition | Requirement |
|------|-----------|-------------|
| **Direct** | The variable measures the theoretical concept itself (e.g., Gini coefficient for income inequality) | Standard statistical validity |
| **Strong proxy** | The variable is empirically validated in the literature as measuring the concept (e.g., DW-NOMINATE scores for congressional polarization) | Literature must explicitly support the variable-to-concept mapping in at least one peer-reviewed study |

Variables where no direct measure or strong proxy exists are documented as gaps and flagged for future work. No creative or speculative proxies are invented.

### Availability Classification Taxonomy

| Classification | Definition | Example |
|---------------|-----------|---------|
| **Available (free API)** | Data accessible via free API with no or free registration | FRED series via API, BLS API |
| **Available (manual download)** | Data freely downloadable as CSV/Excel but no API | V-Dem CSV download, VoteView data files |
| **Partially available (proxy needed)** | The theoretical concept has no direct data source; a constructible proxy exists from available data | Education-job mismatch ratio from Census + BLS |
| **Unavailable** | No direct measure or strong proxy identified | Misinformation prevalence, echo chamber metrics |

### Metadata Schema

Each variable entry records the following 14 fields:

| # | Field | Description |
|---|-------|-------------|
| 1 | **Variable name** | Matches Phase 2 catalog entry exactly |
| 2 | **Theoretical concept** | What this measures in the theoretical framework |
| 3 | **Source name** | Organization providing the data (e.g., Federal Reserve, BLS, Census Bureau) |
| 4 | **API endpoint / download URL** | Specific endpoint or URL for data access |
| 5 | **Series ID** | Unique identifier for the data series (e.g., FRED series ID) |
| 6 | **Native frequency** | How often new observations are published (daily/weekly/monthly/quarterly/annual) |
| 7 | **Coverage window** | Start year through end year or "present" |
| 8 | **Proxy tier** | Direct measure or strong proxy |
| 9 | **Known data gaps** | Any discontinuities, methodology changes, or coverage holes |
| 10 | **API key required** | Whether registration/API key is needed (yes/no) |
| 11 | **Rate limits** | API call limits if applicable |
| 12 | **Data license** | Terms of use for the data |
| 13 | **Last verified date** | Date metadata was verified (via MCP tool or web) |
| 14 | **Original source agency** | The agency that produces the data (distinct from where it is hosted) |

### Verification Approach

- **Federal data (MCP-verified):** FRED, BLS, BEA, Census, and Treasury series verified using US Government Open Data MCP tools (`fred_series_info`, `fred_search`, `bls_search_series`, `query_fiscal_data`, `search_datasets`, `census_search_variables`, `bea_gdp_national`, `hud_fair_market_rents`). MCP tools return structured metadata including observation_start, observation_end, frequency, and last_updated.
- **Non-MCP sources:** Verified via web research against official source websites. Access method, download URL, and data format confirmed.
- **Series status check:** For each FRED series, `observation_end` and `last_updated` fields confirm the series is still active. Series with `last_updated` >12 months ago and no advancing `observation_end` are flagged as potentially discontinued.

### Multiple Proxies Policy

All viable direct and strong-proxy measures are cataloged per variable. A recommended measure is marked with rationale. Final selection of the single measure to use in each model is deferred to Phase 4, where empirical backtesting results will inform the choice.

### Short Series Policy

Variables with data starting after 2000 are included if they measure strong-evidence or moderate-evidence concepts. These are tagged as "short series" so Phase 5 can run separate validation: full backtest (1970-present) on long series, recent-episodes-only validation on short series.

### Units and Deflation Note

All series document their native units. Series marked as "nominal" require deflation before use. Series marked as "real" or "index" are already adjusted. Deflation methodology is deferred to Phase 4 implementation.

---

## Domain 1: Economic Stress Variables

This domain covers 13 variables from the Phase 2 catalog that measure economic conditions contributing to political instability. The economic domain has the strongest evidence base (7 of 13 rated Strong) and best data availability (11 of 13 tagged `fed-data`), making it the most data-rich and verifiable domain.

**Variables in this domain:** #1, #2, #5, #6, #8, #9, #10, #14, #16, #17, #18, #27, #40

---

### Income / Wealth Inequality (#1)

**Catalog Rating:** Strong -- Contested
**Theoretical Concept:** The degree of unequal distribution of income and wealth across the population. Central variable in structural-demographic theory (Turchin), relative deprivation theory (Gurr), and grievance-based conflict models (Cederman). The rate of inequality change may be more predictive than the level for the US context.
**Availability Classification:** Available (free API)

#### Measures

| Measure | Source | Series/Endpoint | Frequency | Coverage | Proxy Tier | API Key? |
|---------|--------|-----------------|-----------|----------|------------|----------|
| GINI Index for the United States | Census Bureau (via FRED) | SIPOVGINIUSA | Annual | 1963-2023 | Direct | Yes (FRED) |
| Share of Total Net Worth Held by Top 1% | Federal Reserve DFA (via FRED) | WFRBST01134 | Quarterly | 1989-present | Direct | Yes (FRED) |
| Top 1% pre-tax national income share | WID.world | sptinc992j (US) | Annual | 1913-present | Direct | No |
| Income shares by quintile | Census Bureau ACS | Table B19082 | Annual | 1967-present | Direct | No (Census API) |
| Black-White median household income ratio | Census Bureau / BLS | Derived from MEHOINUSA672N + race-specific series | Annual | 1967-present | Strong proxy (horizontal inequality dimension) | Yes (FRED) |

**Recommended:** SIPOVGINIUSA (Gini) as the primary aggregate inequality measure for its long coverage (1963-present) and direct interpretability. Supplement with WFRBST01134 (top 1% wealth share) for the wealth concentration dimension and WID sptinc992j for the income concentration dimension. Use multiple measures because the literature shows aggregate Gini and top-end concentration capture different politically relevant dynamics.

**Rate Limits:** FRED API: 120 requests/minute with API key. WID.world: no documented rate limits for bulk CSV download.
**License:** FRED data is public domain (US government work). WID data is CC BY 4.0. Census data is public domain.
**Known Gaps:**
- SIPOVGINIUSA is annual with ~1-year publication lag (2023 is latest as of early 2026)
- WID sptinc992j uses the "equal-split" method (income split equally between spouses); alternative "individual" series also available
- WID API endpoint stability is uncertain -- R package (`wid-r-tool`) or bulk CSV download recommended as fallback
- Contested variable: Collier & Hoeffler (2004) find growth rate matters more than static inequality level

**Last Verified:** 2026-03-03 (SIPOVGINIUSA and WFRBST01134 via MCP `fred_series_info`; WID via web research)

---

### Real Wage Growth / Labor Share (#2)

**Catalog Rating:** Strong
**Theoretical Concept:** The trajectory of real wages for median/typical workers and the share of national income accruing to labor versus capital. Core Mass Mobilization Potential (MMP) variable in Turchin's structural-demographic theory. Declining labor share signals that economic growth is not reaching workers, creating mobilization frustration.
**Availability Classification:** Available (free API)

#### Measures

| Measure | Source | Series/Endpoint | Frequency | Coverage | Proxy Tier | API Key? |
|---------|--------|-----------------|-----------|----------|------------|----------|
| Average Hourly Earnings of All Employees, Total Private | BLS (via FRED) | CES0500000003 | Monthly | 1964-present | Direct (nominal -- requires deflation by CPIAUCSL) | Yes (FRED) |
| Real Median Household Income in the United States | Census Bureau (via FRED) | MEHOINUSA672N | Annual | 1984-present | Direct (already real/deflated) | Yes (FRED) |
| Nonfarm Business Sector: Labor Share | BLS (via FRED) | PRS85006173 | Quarterly | 1947-present | Direct | Yes (FRED) |
| Labor Share of GDP | BEA (via FRED) | W270RE1A156NBEA | Quarterly | 1947-present | Direct | Yes (FRED) |

**Recommended:** PRS85006173 (nonfarm business labor share) as the primary measure for Turchin's MMP component. It has the longest coverage (1947-present), quarterly frequency, and directly measures the labor-vs-capital split that SDT theory emphasizes. Supplement with CES0500000003 (deflated by CPIAUCSL) for the real wage trajectory dimension.

**Rate Limits:** FRED API: 120 requests/minute with API key.
**License:** Public domain (US government work). BLS and BEA data are public domain.
**Known Gaps:**
- CES0500000003 is nominal -- must be deflated by CPIAUCSL to get real wages. The deflation step is a Phase 4 implementation task.
- MEHOINUSA672N is annual with ~1-year lag (already deflated to constant dollars)
- Labor share series have a known structural break in the 2000s: declining labor share accelerated, which is the phenomenon the theory predicts but also means the series may have a structural trend that complicates z-score normalization
- W270RE1A156NBEA uses GDP-based calculation; PRS85006173 uses nonfarm business sector only (excludes agriculture, government). PRS85006173 is more commonly cited in labor economics literature.

**Last Verified:** 2026-03-03 (via MCP `fred_search` for "real wage" and "labor share"; series metadata confirmed active)

---

### State Fiscal Distress (#5)

**Catalog Rating:** Strong -- Contested
**Theoretical Concept:** The financial health of the national government, measured through debt levels, deficit spending, and debt servicing burden. Core State Fiscal Distress (SFD) variable in Turchin's PSI. Structural theorists (Skocpol, Goldstone, Brinton) identify fiscal crisis as one of the most consistently recurring preconditions across revolutionary episodes.
**Availability Classification:** Available (free API)

#### Measures

| Measure | Source | Series/Endpoint | Frequency | Coverage | Proxy Tier | API Key? |
|---------|--------|-----------------|-----------|----------|------------|----------|
| Federal Debt: Total Public Debt as Percent of GDP | BEA/Treasury (via FRED) | GFDEGDQ188S | Quarterly | 1966-present | Direct | Yes (FRED) |
| Federal Surplus or Deficit as Percent of GDP | BEA (via FRED) | FYFSGDA188S | Annual | 1929-present | Direct | Yes (FRED) |
| Federal Debt: Total Public Debt | Treasury (via FRED) | GFDEBTN | Quarterly | 1966-present | Direct | Yes (FRED) |
| Interest Expense on Public Debt | Treasury Fiscal Data API | `/v2/accounting/od/interest_expense` | Monthly | 2001-present | Direct | No |
| Total Public Debt Outstanding (daily) | Treasury Fiscal Data API | `/v2/accounting/od/debt_to_penny` | Daily | 1993-present | Direct | No |
| Monthly Treasury Statement (receipts, outlays, deficit) | Treasury Fiscal Data API | `/v1/accounting/mts/mts_table_1` | Monthly | 2001-present | Direct | No |
| Average Interest Rates on Treasury Securities | Treasury Fiscal Data API | `/v2/accounting/od/avg_interest_rates` | Monthly | 2001-present | Strong proxy (debt servicing cost) | No |

**Recommended:** GFDEGDQ188S (federal debt as % of GDP) as the primary SFD measure, matching Turchin's original PSI specification. Supplement with the Treasury Fiscal Data interest_expense endpoint for the debt servicing burden dimension, which addresses the "contested" critique (Japan example: high debt is sustainable if servicing cost is manageable).

**Rate Limits:** FRED API: 120 requests/minute. Treasury Fiscal Data API: no documented rate limits; free access without API key.
**License:** Public domain (US government work).
**Known Gaps:**
- GFDEGDQ188S is quarterly with a moderate lag
- Contested variable: Japan shows that high debt/GDP does not necessarily produce fiscal crisis when debt is domestically held and denominated in local currency. Debt trajectory and servicing cost may matter more than level.
- Treasury Fiscal Data endpoints start at 2001 for most series, limiting historical backtesting for interest expense data
- FYFSGDA188S (surplus/deficit % GDP) goes back to 1929 but is annual only

**Last Verified:** 2026-03-03 (FRED series via MCP `fred_series_info`; Treasury endpoints via MCP `search_datasets` and `query_fiscal_data`)

---

### Financial Crisis / Systemic Stress (#6)

**Catalog Rating:** Strong
**Theoretical Concept:** The occurrence and severity of systemic financial crises involving banking sector distress, credit market seizure, and broad economic disruption. The Funke et al. (2016) finding represents the single strongest empirically documented economic-to-political transmission mechanism: financial crises produce a 30% increase in far-right vote share with a 5-10 year lag.
**Availability Classification:** Available (free API)

#### Measures

| Measure | Source | Series/Endpoint | Frequency | Coverage | Proxy Tier | API Key? |
|---------|--------|-----------------|-----------|----------|------------|----------|
| St. Louis Fed Financial Stress Index | Federal Reserve Bank of St. Louis (via FRED) | STLFSI4 | Weekly | 1993-present | Direct | Yes (FRED) |
| Chicago Fed National Financial Conditions Index | Federal Reserve Bank of Chicago (via FRED) | NFCI | Weekly | 1971-present | Direct | Yes (FRED) |
| Net Percentage of Domestic Banks Tightening Standards for C&I Loans | Federal Reserve Board (via FRED) | DRTSCILM | Quarterly | 1990-present | Strong proxy (credit tightening signal) | Yes (FRED) |
| TED Spread (3-month LIBOR minus 3-month T-bill) | FRED | TEDRATE | Daily | 1986-2022 (discontinued) | Strong proxy (interbank stress) | Yes (FRED) |
| Credit Spread (Moody's BAA - AAA) | Moody's (via FRED) | BAA10Y | Daily | 1986-present | Strong proxy (credit risk premium) | Yes (FRED) |
| CBOE Volatility Index (VIX) | CBOE (via FRED) | VIXCLS | Daily | 1990-present | Strong proxy (market fear gauge) | Yes (FRED) |

**Recommended:** STLFSI4 as the primary financial stress measure. It is a composite index incorporating 18 weekly data series covering interest rates, yield spreads, and other indicators, with a zero-centered design (0 = normal conditions, positive = above-average stress). Already used in the FSP model. Supplement with NFCI for a longer historical baseline (1971 vs. 1993).

**Rate Limits:** FRED API: 120 requests/minute with API key.
**License:** Public domain (Federal Reserve data). CBOE VIX licensing permits non-commercial use.
**Known Gaps:**
- STLFSI4 replaced STLFSI3/2/1 -- older versions should NOT be used. STLFSI4 uses forward-looking SOFR instead of LIBOR (Nov 2022 change)
- TEDRATE is discontinued (LIBOR phase-out in 2023). Historical data remains available but no new observations.
- NFCI has a longer history (1971) but is less commonly used in political instability literature than STLFSI
- All financial stress indices are US-centric; they capture domestic financial conditions, not global contagion

**Last Verified:** 2026-03-03 (STLFSI4 and NFCI via MCP `fred_series_info`; both confirmed active through Feb 2026)

---

### Elite Overproduction (#8)

**Catalog Rating:** Strong
**Theoretical Concept:** The production of more individuals with elite aspirations, credentials, and expectations than the society has elite positions to offer. Core Elite Mobilization Potential (EMP) variable in Turchin's structural-demographic theory. Creates a pool of "frustrated aspirants" with the education and skills to organize opposition.
**Availability Classification:** Partially available (proxy needed)

#### Measures

| Measure | Source | Series/Endpoint | Frequency | Coverage | Proxy Tier | API Key? |
|---------|--------|-----------------|-----------|----------|------------|----------|
| Top 1% pre-tax national income share | WID.world | sptinc992j (US) | Annual | 1913-present | Strong proxy (income concentration as elite competition proxy; Turchin 2003) | No |
| Share of Total Net Worth Held by Top 1% | Federal Reserve DFA (via FRED) | WFRBST01134 | Quarterly | 1989-present | Strong proxy (wealth concentration as elite competition proxy) | Yes (FRED) |
| Advanced degree holders (master's, professional, doctorate) | Census Bureau ACS | Table B15003 (variables B15003_023E, B15003_024E, B15003_025E) | Annual | 2005-present | Direct (credential production; Georgescu 2023) | No (Census API) |
| Job openings: Professional and business services | BLS JOLTS (via FRED) | JTS540000000000000JOR | Monthly | 2000-present | Direct (elite position availability; Georgescu 2023) | Yes (FRED) |
| Total Nonfarm Job Openings Rate | BLS JOLTS | JTS000000000000000JOR | Monthly | 2000-present | Strong proxy (aggregate labor market tightness) | Yes (FRED) |

**Recommended:** Construct the Georgescu education-job mismatch proxy as the primary EMP measure: (Census advanced degree holders / BLS professional job openings rate). This is more theoretically faithful to Turchin's concept than the top 1% income share (which measures income concentration, not credential-to-position mismatch). However, the constructed proxy has a short time span (2005-present, limited by Census ACS availability) and mixed frequency (Census annual, JOLTS monthly). Retain WID sptinc992j as fallback with longer history. Final selection in Phase 4 based on empirical performance.

**Construction Recipe (Georgescu proxy):**
1. Census ACS B15003: Sum B15003_023E (master's) + B15003_024E (professional) + B15003_025E (doctorate) for total advanced degree holders
2. Normalize to population: divide by total population (B15003_001E)
3. BLS JOLTS: Use JTS540000000000000JOR (professional/business services openings rate) annualized (12-month average)
4. Ratio: (advanced degree holders per capita) / (professional openings rate)
5. Higher ratio = more elite overproduction

**Rate Limits:** FRED API: 120 requests/minute. Census API: 500 requests/day without key. WID: no documented limits for bulk download.
**License:** Public domain (Census, BLS). WID is CC BY 4.0.
**Known Gaps:**
- Census ACS only available from 2005 (1-year estimates) -- limits backtesting to ~20 years. Tag as "short series."
- JOLTS data starts December 2000 -- also a short series
- The Georgescu proxy has not been validated for US specifically (Georgescu 2023 uses OECD cross-national data)
- WID sptinc992j uses "equal-split" income method; API endpoint stability uncertain
- Top 1% income share is an imperfect proxy for elite overproduction (measures income concentration, not credential-to-position mismatch), but has much longer history (1913-present)

**Last Verified:** 2026-03-03 (WFRBST01134 via MCP `fred_series_info`; JOLTS series via MCP `bls_search_series`; Census variables via web research -- Census MCP tool returned JSON parse error during research)

---

### Unemployment Rate (#9)

**Catalog Rating:** Strong
**Theoretical Concept:** The proportion of the labor force actively seeking but unable to find employment. Unemployment directly reduces the opportunity cost of protest participation and increases economic grievances. Spikes in unemployment precede instability episodes in US history.
**Availability Classification:** Available (free API)

#### Measures

| Measure | Source | Series/Endpoint | Frequency | Coverage | Proxy Tier | API Key? |
|---------|--------|-----------------|-----------|----------|------------|----------|
| Civilian Unemployment Rate (U-3) | BLS (via FRED) | UNRATE | Monthly | 1948-present | Direct | Yes (FRED) |
| Total Unemployed plus Discouraged, Marginally Attached, and Part-Time for Economic Reasons (U-6) | BLS (via FRED) | U6RATE | Monthly | 1994-present | Direct (broader underemployment) | Yes (FRED) |
| Unemployment Rate - Black or African American (16+) | BLS (via FRED) | LNS14000006 | Monthly | 1972-present | Direct (racial disparity dimension) | Yes (FRED) |
| Youth Unemployment Rate (15-24, ILO estimate) | World Bank (via FRED) | SLUEM1524ZSUSA | Annual | 1991-present | Direct (youth-specific) | Yes (FRED) |
| Initial Claims for Unemployment Insurance | DOL (via FRED) | ICSA | Weekly | 1967-present | Strong proxy (real-time labor market distress) | Yes (FRED) |

**Recommended:** UNRATE (U-3) as the primary unemployment measure for its long history (1948-present), monthly frequency, and universal recognition. Supplement with U6RATE for the broader underemployment picture (which captures discouraged and part-time workers) and LNS14000006 for the racial disparity dimension.

**Rate Limits:** FRED API: 120 requests/minute with API key.
**License:** Public domain (US government work).
**Known Gaps:**
- UNRATE methodology has undergone revisions (1994 CPS redesign changed definitions of discouraged workers), creating minor comparability issues pre/post 1994
- U6RATE only available from 1994 due to the CPS redesign
- SLUEM1524ZSUSA is annual with 1-2 year lag (ILO estimate, not BLS direct measurement)
- Youth unemployment (15-24) captures a different phenomenon than Campante & Chor (2012) Arab Spring analysis (youth unemployment >30%); US youth unemployment has never reached those levels

**Last Verified:** 2026-03-03 (UNRATE, U6RATE, LNS14000006 via MCP `fred_series_info`; SLUEM1524ZSUSA confirmed active through 2025 observation)

---

### GDP Growth Rate (#10)

**Catalog Rating:** Strong
**Theoretical Concept:** The rate of real economic growth, particularly deviations from trend (deceleration or contraction). The J-curve theory (Davies 1962) emphasizes that growth reversal -- not absolute poverty -- produces revolutionary frustration. Top-ranked variable in Korotayev-Medvedev ML factor importance analysis.
**Availability Classification:** Available (free API)

#### Measures

| Measure | Source | Series/Endpoint | Frequency | Coverage | Proxy Tier | API Key? |
|---------|--------|-----------------|-----------|----------|------------|----------|
| Real GDP Growth (annualized quarterly rate) | BEA (via FRED) | A191RL1Q225SBEA | Quarterly | 1947-present | Direct | Yes (FRED) |
| Real GDP per Capita Growth | BEA (via FRED) | A939RX0Q048SBEA | Quarterly | 1947-present | Direct (population-adjusted) | Yes (FRED) |
| GDP (nominal level) | BEA (via FRED) | GDP | Quarterly | 1947-present | Direct (requires deflation for real comparison) | Yes (FRED) |
| BEA National GDP Data | BEA API | `bea_gdp_national` endpoint | Quarterly/Annual | 1929-present | Direct | Yes (BEA API key) |

**Recommended:** A191RL1Q225SBEA (real GDP growth, annualized quarterly rate) as the primary measure. It directly captures the growth trajectory that J-curve theory emphasizes and has excellent coverage (1947-present). For detecting growth reversals, compute rolling 4-quarter change vs. 20-quarter trend in Phase 4.

**Rate Limits:** FRED API: 120 requests/minute. BEA API: 100 requests/minute with free registration.
**License:** Public domain (US government work).
**Known Gaps:**
- GDP is subject to significant revision: advance estimate (1 month after quarter), second estimate (2 months), third estimate (3 months), plus annual comprehensive revisions
- Historical GDP data before 1947 is less reliable but available from BEA back to 1929
- Real GDP growth can be computed from levels (GDP deflated by GDP deflator) or read directly from the pre-computed growth series; the pre-computed series is recommended to avoid deflator methodology inconsistencies

**Last Verified:** 2026-03-03 (A191RL1Q225SBEA via MCP `fred_series_info`; BEA data availability confirmed via MCP `bea_gdp_national`)

---

### Relative Deprivation / Expectation-Reality Gap (#14)

**Catalog Rating:** Moderate
**Theoretical Concept:** The perceived gap between what people expect (based on prior trajectory or reference groups) and what they actually have. The psychological mechanism driving political frustration. Converges with prospect theory (Kahneman & Tversky), J-curve theory (Davies), and relative deprivation theory (Gurr).
**Availability Classification:** Partially available (proxy needed)

#### Measures

| Measure | Source | Series/Endpoint | Frequency | Coverage | Proxy Tier | API Key? |
|---------|--------|-----------------|-----------|----------|------------|----------|
| University of Michigan: Consumer Sentiment Index | U. Michigan (via FRED) | UMCSENT | Monthly | 1952-present | Strong proxy (subjective economic assessment) | Yes (FRED) |
| University of Michigan: Consumer Expectations Index | U. Michigan (via FRED) | MICH | Monthly | 1978-present | Strong proxy (forward-looking expectations) | Yes (FRED) |
| Real Median Household Income | Census Bureau (via FRED) | MEHOINUSA672N | Annual | 1984-present | Direct (actual economic reality for comparison) | Yes (FRED) |
| Real GDP per Capita | BEA (via FRED) | A939RX0Q048SBEA | Quarterly | 1947-present | Direct (actual economic performance) | Yes (FRED) |

**Recommended:** Construct the expectation-reality gap as the primary measure: (UMCSENT or MICH normalized) minus (actual GDP/employment performance normalized). Higher positive gap = expectations above reality = J-curve "dashed expectations." Higher negative gap = pessimism below reality = deprivation perception. This is a derived variable -- no single series captures the concept directly.

**Construction Recipe:**
1. Normalize UMCSENT (or MICH for expectations only) to z-scores over rolling 10-year window
2. Normalize actual economic performance indicator (MEHOINUSA672N growth rate or GDP growth) to z-scores over same window
3. Gap = sentiment z-score minus actual performance z-score
4. Positive gap = expectations above reality (J-curve vulnerability)
5. Negative gap = perceived deprivation beyond actual deterioration

**Rate Limits:** FRED API: 120 requests/minute with API key.
**License:** Public domain (FRED-hosted data). University of Michigan survey data terms apply for direct download.
**Known Gaps:**
- This is a constructed variable -- the construction recipe must be validated empirically in Phase 4
- UMCSENT methodology has remained stable since 1952, but sample sizes and response rates have changed
- MEHOINUSA672N is annual with ~1-year lag, creating frequency mismatch with monthly UMCSENT
- The "expectation-reality gap" concept is theoretically clear but no standard operationalization exists in the literature -- Phase 4 must test multiple construction approaches

**Last Verified:** 2026-03-03 (UMCSENT confirmed active through Jan 2026 via MCP `fred_series_info`)

---

### Housing Affordability (#16)

**Catalog Rating:** Moderate
**Theoretical Concept:** The cost of housing relative to household income. Identified as the US analog to food price triggers in historical revolutions: housing consumes 30-40% of US household budgets (vs. ~10% for food), making it the dominant cost-of-living pressure point for political grievance generation.
**Availability Classification:** Available (free API)

#### Measures

| Measure | Source | Series/Endpoint | Frequency | Coverage | Proxy Tier | API Key? |
|---------|--------|-----------------|-----------|----------|------------|----------|
| Housing Affordability Index (Fixed Rate) | National Association of Realtors (via FRED) | FIXHAI | Monthly | 1971-present | Direct | Yes (FRED) |
| Median Sales Price of Houses Sold | Census Bureau (via FRED) | MSPUS | Quarterly | 1963-present | Strong proxy (numerator of price-to-income ratio) | Yes (FRED) |
| 30-Year Fixed Rate Mortgage Average | Freddie Mac (via FRED) | MORTGAGE30US | Weekly | 1971-present | Strong proxy (cost of financing) | Yes (FRED) |
| S&P/Case-Shiller U.S. National Home Price Index | S&P Dow Jones Indices (via FRED) | CSUSHPISA | Monthly | 1987-present | Strong proxy (home price trajectory) | Yes (FRED) |
| HUD Fair Market Rents | HUD | `hud_fair_market_rents` MCP endpoint | Annual | Various | Strong proxy (rental affordability) | No |

**Recommended:** FIXHAI (Housing Affordability Index) as the primary measure. It directly captures affordability as a composite of home prices, mortgage rates, and median income -- the three factors that determine whether households can afford housing. A value of 100 means the median-income family has exactly enough to qualify for a median-priced home; below 100 = unaffordable. Supplement with MSPUS and MORTGAGE30US for component analysis.

**Rate Limits:** FRED API: 120 requests/minute. HUD API: no documented rate limits.
**License:** FIXHAI: National Association of Realtors proprietary but freely available on FRED. MSPUS, MORTGAGE30US: public domain. HUD data: public domain.
**Known Gaps:**
- FIXHAI is specific to home *buying* affordability; rental affordability is a separate dimension (captured by HUD FMR data and Census rent burden measures)
- The NAR methodology for FIXHAI has been stable but the index captures existing home sales only (not new construction)
- CSUSHPISA starts in 1987 (S&P/Case-Shiller methodology) -- shorter than MSPUS (1963)
- HUD Fair Market Rents are set annually based on prior-year surveys; they lag actual market conditions

**Last Verified:** 2026-03-03 (FRED series via MCP `fred_search` for "housing affordability"; HUD endpoint via MCP `hud_fair_market_rents`)

---

### Inflation Rate (#17)

**Catalog Rating:** Moderate
**Theoretical Concept:** The rate of change in the general price level. Captures cost-of-living erosion that reduces purchasing power and generates economic grievances. Politically salient due to loss aversion: people perceive price increases more intensely than equivalent income gains (prospect theory).
**Availability Classification:** Available (free API)

#### Measures

| Measure | Source | Series/Endpoint | Frequency | Coverage | Proxy Tier | API Key? |
|---------|--------|-----------------|-----------|----------|------------|----------|
| CPI for All Urban Consumers: All Items (CPI-U) | BLS (via FRED) | CPIAUCSL | Monthly | 1947-present | Direct | Yes (FRED) |
| CPI: Food at Home | BLS (via FRED) | CPIFABSL | Monthly | 1952-present | Direct (food component) | Yes (FRED) |
| CPI: Energy | BLS (via FRED) | CPIENGSL | Monthly | 1957-present | Direct (energy component) | Yes (FRED) |
| CPI: Shelter | BLS (via FRED) | CUSR0000SAH1 | Monthly | 1947-present | Direct (housing cost component) | Yes (FRED) |
| CPI: Medical Care | BLS (via FRED) | CPIMEDSL | Monthly | 1947-present | Direct (healthcare cost component) | Yes (FRED) |
| PCE Price Index | BEA (via FRED) | PCEPI | Monthly | 1959-present | Direct (alternative inflation measure) | Yes (FRED) |
| CPI Components Breakdown | BLS API | `bls_cpi_breakdown` MCP endpoint | Monthly | Various | Direct | Yes (BLS key for v2) |

**Recommended:** CPIAUCSL (CPI-U All Items) as the primary headline inflation measure, computed as year-over-year percentage change. For the cost-of-living pressure dimension (variable #40), use the individual CPI components (food, shelter, energy, medical care) separately. PCE is the Fed's preferred inflation measure but is less intuitive for the public-facing grievance analysis.

**Rate Limits:** FRED API: 120 requests/minute. BLS API v2: 500 queries/day with registration key; 25 queries/day without.
**License:** Public domain (US government work).
**Known Gaps:**
- CPI methodology has changed multiple times (hedonics, geometric weighting, owner's equivalent rent). Major revisions in 1983 (housing methodology) and 1999 (geometric means). These changes generally reduced measured inflation relative to pre-revision methodology.
- CPIAUCSL is a seasonally adjusted index level, not a rate. Must compute year-over-year or month-over-month percentage change in Phase 4.
- "Perceived inflation" (how people feel about prices) often exceeds actual CPI, especially for frequent purchases (food, gasoline). No standard series for perceived inflation exists on FRED.

**Last Verified:** 2026-03-03 (CPI series via MCP `fred_series_info` and `bls_cpi_breakdown`)

---

### Consumer Confidence / Sentiment (#18)

**Catalog Rating:** Moderate
**Theoretical Concept:** Survey-based measures of consumer attitudes about economic conditions -- both current assessment and future expectations. Captures the subjective dimension of economic experience. The gap between the expectations sub-index and actual economic performance may proxy relative deprivation.
**Availability Classification:** Available (free API) -- with important gap

#### Measures

| Measure | Source | Series/Endpoint | Frequency | Coverage | Proxy Tier | API Key? |
|---------|--------|-----------------|-----------|----------|------------|----------|
| University of Michigan: Consumer Sentiment Index | U. Michigan (via FRED) | UMCSENT | Monthly | 1952-present | Direct | Yes (FRED) |
| University of Michigan: Consumer Expectations Index | U. Michigan (via FRED) | MICH | Monthly | 1978-present | Direct (forward-looking component) | Yes (FRED) |
| OECD Consumer Confidence (Amplitude Adjusted) | OECD (via FRED) | CSCICP03USM665S | Monthly | 1960-2024 | Direct | Yes (FRED) |
| Conference Board Consumer Confidence Index | Conference Board | Not on FRED (paid subscription) | Monthly | 1967-present | Direct | N/A (paid) |

**Recommended:** UMCSENT as the primary consumer sentiment measure. It has the longest freely available history (1952-present), monthly frequency, and active data through present day.

**IMPORTANT -- CSCICP03USM665S Discontinuation:**
The OECD Consumer Confidence series (CSCICP03USM665S) used in the original FSP model codebase is **DISCONTINUED**. Last observation: January 2024. Last updated on FRED: 2025-11-17 (metadata only, no new data). The discontinuation results from OECD's restructuring of Main Economic Indicators (MEI) to the Key Short-Term Economic Indicators (KSTEI) framework. No replacement series has appeared on FRED.

**Handling Recommendation:** Drop the CSCICP03USM665S weight from the FSP model's Economic Transmission Index (ETI) and redistribute to remaining inputs. This is preferable to the alternatives:
- Using UMCSENT as replacement would violate the zero-overlap design (UMCSENT is already used in PLI)
- Conference Board CCI is not freely available on FRED (paid subscription required)
- No other free consumer confidence series on FRED captures the same OECD-standardized cross-country methodology

This loses the consumer confidence signal in the FSP model, but UMCSENT already captures consumer sentiment in the PLI model. The zero-overlap design constraint takes priority.

**Rate Limits:** FRED API: 120 requests/minute with API key.
**License:** University of Michigan survey data: publicly available via FRED. Conference Board: proprietary (paid).
**Known Gaps:**
- CSCICP03USM665S is DISCONTINUED -- see handling recommendation above
- Conference Board CCI is NOT freely available -- requires paid subscription or manual extraction from press releases
- UMCSENT methodology has remained stable but sample response rates have declined over decades
- UMCSENT and Conference Board CCI often diverge, particularly during periods of political uncertainty (they measure slightly different constructs)

**Last Verified:** 2026-03-03 (UMCSENT confirmed active through Jan 2026; CSCICP03USM665S confirmed discontinued -- both via MCP `fred_series_info`; Conference Board CCI confirmed not on FRED via MCP `fred_search`)

---

### Household Debt / Leverage (#27)

**Catalog Rating:** Moderate
**Theoretical Concept:** The level and trajectory of household indebtedness relative to income and GDP. A precursor to financial crises (Mian, Sufi & Trebbi 2014) and a measure of household financial fragility. Since financial crises have the strongest documented transmission to political instability (Funke et al. 2016), household debt serves as an upstream predictor.
**Availability Classification:** Available (free API)

#### Measures

| Measure | Source | Series/Endpoint | Frequency | Coverage | Proxy Tier | API Key? |
|---------|--------|-----------------|-----------|----------|------------|----------|
| Household Debt to GDP for the United States | BIS (via FRED) | HDTGPDUSQ163N | Quarterly | 2005-present | Direct | Yes (FRED) |
| Household Debt Service Payments as a Percent of Disposable Personal Income | Federal Reserve Board (via FRED) | TDSP | Quarterly | 1980-present | Direct (debt servicing burden) | Yes (FRED) |
| Total Consumer Credit Outstanding (Revolving) | Federal Reserve Board (via FRED) | REVOLSL | Monthly | 1968-present | Strong proxy (consumer credit growth) | Yes (FRED) |
| Mortgage Delinquency Rate | MBA (via FRED) | DRSFRMACBS | Quarterly | 1979-present | Strong proxy (debt distress signal) | Yes (FRED) |

**Recommended:** TDSP (household debt service ratio) as the primary measure. It directly captures the burden of debt on household budgets (what fraction of disposable income goes to debt payments), which is more theoretically relevant to financial fragility than the debt-to-GDP level. TDSP also has better coverage (1980-present) than HDTGPDUSQ163N (2005-present). Supplement with HDTGPDUSQ163N for the leverage dimension.

**Rate Limits:** FRED API: 120 requests/minute with API key.
**License:** Public domain (Federal Reserve data). BIS data freely available.
**Known Gaps:**
- HDTGPDUSQ163N starts only in 2005 -- tag as "short series." Limits backtesting to ~20 years.
- DRSFRMACBS had a 2023 MBA methodology revision that affects level comparability across the break point. Flagged in Phase 1 audit (01-02-PLAN). Phase 4 may need level adjustment or separate normalization windows.
- TDSP covers mortgage + consumer debt service but excludes rent payments, which are a significant household obligation for non-homeowners
- REVOLSL measures consumer credit outstanding (levels), not the flow; month-over-month growth rate is more informative than level

**Last Verified:** 2026-03-03 (HDTGPDUSQ163N confirmed active through Apr 2025 via MCP `fred_series_info`; TDSP and REVOLSL via FRED web verification)

---

### Cost of Living Pressure - Composite (#40)

**Catalog Rating:** Moderate
**Theoretical Concept:** The composite pressure of essential costs (housing, food, healthcare, energy) on household budgets. The modern equivalent of food price triggers that preceded historical revolutions (French Revolution, Arab Spring). In the US, the relevant pressures are housing (30-40% of income), healthcare, food, and energy.
**Availability Classification:** Partially available (proxy needed)

#### Measures

| Measure | Source | Series/Endpoint | Frequency | Coverage | Proxy Tier | API Key? |
|---------|--------|-----------------|-----------|----------|------------|----------|
| CPI: Food at Home | BLS (via FRED) | CPIFABSL | Monthly | 1952-present | Direct (food cost component) | Yes (FRED) |
| CPI: Shelter | BLS (via FRED) | CUSR0000SAH1 | Monthly | 1947-present | Direct (housing cost component) | Yes (FRED) |
| CPI: Energy | BLS (via FRED) | CPIENGSL | Monthly | 1957-present | Direct (energy cost component) | Yes (FRED) |
| CPI: Medical Care | BLS (via FRED) | CPIMEDSL | Monthly | 1947-present | Direct (healthcare cost component) | Yes (FRED) |
| CPI: Education and Communication | BLS (via FRED) | CPIEDUSL | Monthly | 1993-present | Direct (education cost component) | Yes (FRED) |
| CPI: Transportation | BLS (via FRED) | CPITRNSL | Monthly | 1947-present | Direct (transportation cost component) | Yes (FRED) |
| CPI Components Breakdown | BLS API | `bls_cpi_breakdown` MCP endpoint | Monthly | Various | Direct | Yes (BLS key for v2) |

**Recommended:** Construct a weighted essential cost index from CPI components. This is a derived variable that weights each essential category by its share of a typical lower/middle-income household budget.

**Construction Recipe:**
1. Obtain CPI component indices: CUSR0000SAH1 (shelter), CPIFABSL (food at home), CPIENGSL (energy), CPIMEDSL (medical care)
2. Compute year-over-year growth rate for each component
3. Weight by approximate budget share for median household: shelter 33%, food 13%, transportation 16%, healthcare 9%, energy 7%, education 6%, other 16%
4. Weighted average = essential cost pressure index
5. Compare to median household income growth (MEHOINUSA672N) for affordability dimension

**Alternative approach:** Use overall CPI (CPIAUCSL) year-over-year as a simpler single-series proxy. The composite construction adds precision but complexity; Phase 4 empirical testing should determine if the composite outperforms headline CPI.

**Rate Limits:** FRED API: 120 requests/minute. BLS API v2: 500 queries/day with registration.
**License:** Public domain (US government work).
**Known Gaps:**
- This is a constructed composite -- no single official series captures "essential cost pressure"
- Budget weights vary significantly by income quintile: lower-income households spend proportionally more on food, shelter, and energy
- CPI methodology changes (especially 1983 housing methodology change and 1999 geometric weighting) affect long-run comparability
- Education costs (tuition) have their own CPI series but tuition payment timing is irregular (semester-based, not monthly)
- The BLS "CPI for Urban Wage Earners and Clerical Workers" (CPI-W) is an alternative that weights toward lower-income consumption patterns

**Last Verified:** 2026-03-03 (CPI component series via MCP `bls_cpi_breakdown` and `fred_series_info`)

---

## Domain Summary: Economic Stress

### Coverage Assessment

| Variable | # | Rating | Availability | Primary Series | Coverage Start |
|----------|---|--------|-------------|----------------|----------------|
| Income / Wealth Inequality | 1 | Strong* | Available (free API) | SIPOVGINIUSA | 1963 |
| Real Wage Growth / Labor Share | 2 | Strong | Available (free API) | PRS85006173 | 1947 |
| State Fiscal Distress | 5 | Strong* | Available (free API) | GFDEGDQ188S | 1966 |
| Financial Crisis / Systemic Stress | 6 | Strong | Available (free API) | STLFSI4 | 1993 |
| Elite Overproduction | 8 | Strong | Partially available | Constructed (Census + BLS) | 2005 |
| Unemployment Rate | 9 | Strong | Available (free API) | UNRATE | 1948 |
| GDP Growth Rate | 10 | Strong | Available (free API) | A191RL1Q225SBEA | 1947 |
| Relative Deprivation | 14 | Moderate | Partially available | Constructed (UMCSENT - GDP) | 1952 |
| Housing Affordability | 16 | Moderate | Available (free API) | FIXHAI | 1971 |
| Inflation Rate | 17 | Moderate | Available (free API) | CPIAUCSL | 1947 |
| Consumer Confidence / Sentiment | 18 | Moderate | Available (free API) | UMCSENT | 1952 |
| Household Debt / Leverage | 27 | Moderate | Available (free API) | TDSP | 1980 |
| Cost of Living Pressure | 40 | Moderate | Partially available | Constructed (CPI components) | 1957 |

*Asterisk indicates Contested variables

### Key Statistics

- **Total variables:** 13
- **Available (free API):** 10 (77%)
- **Partially available (proxy needed):** 3 (23%) -- #8 Elite Overproduction, #14 Relative Deprivation, #40 Cost of Living Pressure
- **Unavailable:** 0
- **Strong-rated:** 7 (54%) -- #1, #2, #5, #6, #8, #9, #10
- **Moderate-rated:** 6 (46%) -- #14, #16, #17, #18, #27, #40
- **Contested:** 2 -- #1 (Income Inequality), #5 (State Fiscal Distress)
- **Short series (post-2000 start):** 2 -- #8 Elite Overproduction (2005), #27 HDTGPDUSQ163N (2005)
- **Frequency mix:** Weekly (2), Monthly (7), Quarterly (3), Annual (1)
- **Discontinued series:** 1 -- CSCICP03USM665S (handled by weight redistribution)

### Critical Gaps

1. **CSCICP03USM665S discontinuation (#18):** OECD Consumer Confidence series discontinued Jan 2024. No direct FRED replacement. Recommended: drop weight from FSP ETI and redistribute. UMCSENT cannot be used as replacement (zero-overlap constraint with PLI).

2. **Elite overproduction proxy construction (#8):** The theoretically superior Georgescu education-job mismatch proxy requires combining Census ACS (annual, 2005+) with BLS JOLTS (monthly, 2000+). The construction recipe is documented but unvalidated for US. The fallback (WID top 1% income share) has longer history but weaker theoretical alignment.

3. **DRSFRMACBS methodology break (#27):** Mortgage delinquency rate had a 2023 MBA methodology revision affecting level comparability. Phase 4 normalization must account for this break.

### Data Sources Used

| Source | Series Count | API Key Required |
|--------|-------------|-----------------|
| FRED (Federal Reserve Economic Data) | ~30 series | Yes (free registration) |
| Treasury Fiscal Data API | 4 endpoints | No |
| BLS API | CPI breakdown + JOLTS | Yes (free registration for v2) |
| BEA API | GDP endpoints | Yes (free registration) |
| Census Bureau API | ACS education variables | No (but limited without key) |
| WID.world | 1 series (sptinc992j) | No |
| HUD | Fair Market Rents | No |

---

## Domain 2: Political Polarization & Elite Dynamics

This domain covers 8 variables from the Phase 2 catalog that measure political division, elite competition, and distributional conflict between groups. The domain relies heavily on non-MCP academic sources (VoteView, WID, ANES, FEC) rather than federal APIs, making verification more web-research dependent. Political polarization -- both ideological and affective -- is among the most consistently cited predictors of democratic backsliding across 16 comparative cases (Haggard & Kaufman 2021).

**Variables in this domain:** #3, #4, #11, #15, #19, #20, #31, #45

---

### Political Polarization - Congressional (#3)

**Catalog Rating:** Strong
**Theoretical Concept:** The degree of ideological separation between political parties as measured by legislative voting behavior. Core elite-level political division indicator. DW-NOMINATE scores are the gold standard for US congressional polarization measurement (McCarty, Poole & Rosenthal 2006). Turchin (2023) includes political polarization as a key structural-demographic stress indicator.
**Availability Classification:** Available (manual download)

#### Measures

| Measure | Source | Series/Endpoint | Frequency | Coverage | Proxy Tier | API Key? |
|---------|--------|-----------------|-----------|----------|------------|----------|
| DW-NOMINATE party mean distance (House + Senate) | VoteView (UCLA) | `HSall_members.csv` from voteview.com/data | Per Congress (~biennial), weekly DB dumps | 1st-119th Congress (1789-2027) | Direct | No |
| DW-NOMINATE scores (House only) | VoteView (UCLA) | `Hall_members.csv` from voteview.com/data | Per Congress, weekly DB dumps | 1st-119th Congress (1789-2027) | Direct | No |
| DW-NOMINATE scores (Senate only) | VoteView (UCLA) | `Sall_members.csv` from voteview.com/data | Per Congress, weekly DB dumps | 1st-119th Congress (1789-2027) | Direct | No |
| Bipartisan voting frequency | Congress.gov (via MCP) | `congress_house_votes`, `congress_senate_votes` | Per vote | Recent Congresses | Strong proxy (behavioral complement to ideological distance) | No |

**Recommended:** VoteView DW-NOMINATE party mean distance as the primary measure. Compute as: |mean(Republican 1st dimension scores) - mean(Democrat 1st dimension scores)| per Congress. This is the standard operationalization in the political science literature (McCarty et al. 2006, 2016). The 1st dimension captures the liberal-conservative axis; the 2nd dimension (historically race/civil rights) is less relevant for the modern era. Use both House and Senate separately or combined (`HSall_members.csv`).

**Construction Recipe (Party Polarization from DW-NOMINATE):**
1. Download `HSall_members.csv` from https://voteview.com/data
2. Filter to a specific Congress number (e.g., congress = 118)
3. Separate by party_code (100 = Democrat, 200 = Republican)
4. Compute mean of `nominate_dim1` for each party
5. Polarization = |mean_R - mean_D|
6. Repeat for each Congress to build time series (1789-present)

**Rate Limits:** No API -- CSV download from voteview.com. Files are static downloads updated weekly.
**License:** VoteView data is freely available for academic and non-commercial use. Data produced by Keith Poole, Howard Rosenthal, and collaborators.
**Known Gaps:**
- VoteView is NOT an API -- it provides CSV file downloads only. Do not attempt REST API calls to voteview.com.
- DW-NOMINATE scores are estimated jointly across all Congresses using a bridge scaling methodology, so adding new Congresses can slightly revise historical scores
- The 2nd dimension has diminished explanatory power since the civil rights realignment (post-1970s)
- Congressional polarization measures elite behavior, not mass public polarization -- supplement with #4 (Affective Polarization) for the public dimension
- Mann & Ornstein (2012) document that polarization is asymmetric: Republican rightward shift has been larger than Democratic leftward shift

**Last Verified:** 2026-03-03 (VoteView website confirmed active, CSV files available at voteview.com/data; Congressional MCP tools confirmed available)

---

### Affective Polarization (#4)

**Catalog Rating:** Strong
**Theoretical Concept:** Growing mutual dislike and distrust between partisan groups that extends beyond policy disagreements into personal hostility. Distinct from ideological polarization (#3) -- measures how much partisans dislike each other, not how much they disagree on policy. McCoy & Somer (2019) identify pernicious polarization as the strongest predictor of democratic backsliding across 16 comparative cases.
**Availability Classification:** Available (manual download) -- periodic survey data

#### Measures

| Measure | Source | Series/Endpoint | Frequency | Coverage | Proxy Tier | API Key? |
|---------|--------|-----------------|-----------|----------|------------|----------|
| Partisan feeling thermometer difference (in-party minus out-party) | ANES Cumulative Data File | Variables VCF0218 (in-party), VCF0224 (out-party) from electionstudies.org | Biennial/quadrennial (election years) | 1948-2020 (Cumulative File) | Direct | No |
| ANES Time Series individual studies | ANES | Individual study files from electionstudies.org | Per study | 2020, 2024 (standalone studies) | Direct | No |
| Partisan antipathy surveys | Pew Research Center | Published reports with data tables | Irregular (~annual since 2014) | 2014-present (systematic tracking) | Strong proxy | No |

**Recommended:** ANES partisan feeling thermometer difference as the primary measure. Compute as: mean(in-party thermometer rating) - mean(out-party thermometer rating). The cumulative data file provides the standardized variables VCF0218 and VCF0224 across all election studies from 1948 to 2020. For post-2020 data, use individual ANES Time Series studies (2020, 2024).

**Construction Recipe (Affective Polarization from ANES):**
1. Download ANES Cumulative Data File from https://electionstudies.org/data-center/anes-time-series-cumulative-data-file/
2. Extract VCF0218 (feeling thermometer: own party) and VCF0224 (feeling thermometer: other party)
3. Compute difference: affective_polarization = mean(VCF0218) - mean(VCF0224)
4. Higher difference = greater affective polarization
5. Note: thermometers run 0-100; typical gap has grown from ~25 points (1980) to ~45+ points (2020)

**Rate Limits:** No API -- CSV download from electionstudies.org after free registration.
**License:** ANES data is freely available for research purposes. Requires citation of ANES and acknowledgment of NSF funding.
**Known Gaps:**
- Biennial/quadrennial frequency severely limits time series density -- use LOCF (Last Observation Carried Forward) for alignment with higher-frequency series per project decision
- Tag as "short series" for the systematic measurement component -- the concept has been measured since 1948 (feeling thermometers exist that far back) but the "affective polarization" interpretation is modern (Iyengar et al. 2012)
- ANES question wording and methodology have evolved across waves -- the cumulative file harmonizes variables but some waves may have different response scales or sampling frames
- ANES does not include all feeling thermometer questions in all waves -- verify VCF0218 and VCF0224 availability per wave before computing time series
- Pew partisan antipathy data provides higher frequency since 2014 but uses different methodology (not directly comparable to ANES thermometers)
- Post-2020 ANES data may require downloading individual Time Series studies separately from the cumulative file

**Last Verified:** 2026-03-03 (ANES website confirmed active, cumulative data file available; Pew trust/antipathy reports confirmed published through 2025)

---

### Elite Factionalism / Fragmentation (#11)

**Catalog Rating:** Strong
**Theoretical Concept:** The degree to which political elites are divided into competing factions unable to cooperate on governance. Central to Goldstone (1991, 2010) and the PITF model -- factionalism is a key component of the highest-risk regime category. Distinct from polarization (#3): measures division within the ruling class specifically, not just between parties.
**Availability Classification:** Partially available (proxy needed) -- constructible from VoteView data

#### Measures

| Measure | Source | Series/Endpoint | Frequency | Coverage | Proxy Tier | API Key? |
|---------|--------|-----------------|-----------|----------|------------|----------|
| Intra-party DW-NOMINATE spread (SD within each party) | VoteView (UCLA) | Derived from `HSall_members.csv` | Per Congress (~biennial) | 1st-119th Congress (1789-2027) | Strong proxy (intra-party ideological dispersion as factionalism proxy) | No |
| Primary challenge rates | FEC | `fec_search_candidates` MCP tool | Per election cycle | 1980-present (electronic filings) | Strong proxy (contested primaries signal elite competition) | No |
| House Freedom Caucus / Progressive Caucus membership and defection votes | Congress.gov (via MCP) | `congress_house_votes` | Per vote | 2015-present (Freedom Caucus founded 2015) | Strong proxy (formalized intra-party factions) | No |

**Recommended:** Construct intra-party DW-NOMINATE spread as the primary measure. This captures how ideologically dispersed each party's members are -- higher spread = more internal factions. The construction recipe uses the same VoteView data as #3 (Political Polarization) but measures within-party rather than between-party variation.

**Construction Recipe (Elite Factionalism from VoteView):**
1. Download `HSall_members.csv` from https://voteview.com/data
2. Filter to a specific Congress number
3. Separate by party_code (100 = Democrat, 200 = Republican)
4. Compute standard deviation of `nominate_dim1` within each party
5. Factionalism index = max(SD_R, SD_D) or average(SD_R, SD_D) -- Phase 4 decision
6. Higher SD = more internal fragmentation
7. Repeat for each Congress to build time series

**Rate Limits:** VoteView: no API, CSV download. FEC MCP tool: standard MCP rate limits.
**License:** VoteView: freely available for academic use. FEC: public domain (US government).
**Known Gaps:**
- This is a constructed variable -- intra-party DW-NOMINATE SD is not a pre-computed series
- DW-NOMINATE captures ideological spread but not all forms of factionalism (e.g., personal/patronage factions, generational divides)
- The PITF model uses a categorical factionalism coding (0-3 scale) based on expert judgment, not a continuous measure -- our proxy is continuous but captures a narrower concept
- FEC primary challenge data requires defining what constitutes a "primary challenge" (at least 2 candidates filing?) and is available only for federal races
- Formalized caucus data (Freedom Caucus, Progressive Caucus) provides a direct factionalism measure but only from 2015 -- tag as "short series" if used

**Last Verified:** 2026-03-03 (VoteView CSV files confirmed available; FEC MCP tool confirmed operational)

---

### Horizontal Inequality - Between-Group (#15)

**Catalog Rating:** Moderate
**Theoretical Concept:** Inequality between politically relevant identity groups (racial, ethnic, regional) rather than between individuals. Stewart (2008) and Cederman et al. (2013) show that between-group inequality is more predictive of political conflict than aggregate inequality measures like Gini.
**Availability Classification:** Available (free API)

#### Measures

| Measure | Source | Series/Endpoint | Frequency | Coverage | Proxy Tier | API Key? |
|---------|--------|-----------------|-----------|----------|------------|----------|
| Median household income by race/ethnicity | Census Bureau ACS | Tables B19013A-I (by race), via `census_search_variables` MCP | Annual | 2005-present (1-year ACS estimates) | Direct | No (Census API, limited without key) |
| Black-White median household income ratio | Census Bureau (via FRED) | Derived from race-specific income series | Annual | 1967-present (from Census historical tables) | Direct | Yes (FRED) |
| Earnings by race/ethnicity (weekly) | BLS Current Population Survey (via FRED) | LEU0252881600A (Black), LEU0252883600A (White), LEU0252885600A (Hispanic) | Quarterly | 1979-present | Direct | Yes (FRED) |
| Racial income mobility gaps | Opportunity Insights (Chetty et al.) | CSV download from opportunityinsights.org | One-time cohort data | Birth cohorts 1978-1992 | Strong proxy (intergenerational mobility dimension) | No |

**Recommended:** Census Bureau racial/ethnic median household income ratios as the primary measure. Compute Black/White and Hispanic/White income ratios from Census historical tables (available 1967-present for Black/White, 1972-present for Hispanic/White). For higher granularity post-2005, use ACS tables B19013A-I. Supplement with BLS weekly earnings by race for quarterly frequency.

**Construction Recipe (Racial Income Ratio):**
1. Obtain median household income by race: Census historical tables H-5 and H-9 from census.gov/data/tables/time-series/demo/income-poverty/historical-income-households.html
2. Compute ratio: (Black median HH income) / (White median HH income)
3. Similarly for Hispanic/White ratio
4. Track ratio over time -- declining ratio = increasing horizontal inequality
5. For post-2005 annual detail: use ACS B19013B (Black), B19013A (White non-Hispanic), B19013I (Hispanic)

**Rate Limits:** FRED API: 120 requests/minute. Census API: 500 requests/day without key, higher with key.
**License:** Public domain (US government work). Opportunity Insights data is freely available for research.
**Known Gaps:**
- Census racial categories have changed over time (multiracial category added in 2000 Census, ACS categories differ from decennial Census)
- ACS 1-year estimates available only for geographies with 65,000+ population -- limits state/local granularity
- Opportunity Insights data is cohort-based (birth year), not calendar-year time series -- useful for level assessment but not for time series modeling
- Regional inequality (e.g., Rust Belt vs. Sun Belt) is a separate dimension not captured by racial income ratios -- would require constructing from ACS geographic data

**Last Verified:** 2026-03-03 (FRED earnings series confirmed via MCP; Census ACS variable structure confirmed via web research; Census MCP tool returned JSON parse error during research phase -- fallback to direct Census API or web download)

---

### Intra-Elite Wealth Gap (#19)

**Catalog Rating:** Moderate
**Theoretical Concept:** The gap between the very top of the wealth distribution (top 0.1%) and the merely affluent (top 1-10%). Captures the frustrated aspirant dynamic central to Turchin's counter-elite formation theory. When the top 0.1% pull away from the top 1-10%, the "merely rich" become frustrated aspirants who fund counter-elite movements.
**Availability Classification:** Available (free API) + Available (manual download)

#### Measures

| Measure | Source | Series/Endpoint | Frequency | Coverage | Proxy Tier | API Key? |
|---------|--------|-----------------|-----------|----------|------------|----------|
| Top 1% net worth share | Federal Reserve DFA (via FRED) | WFRBST01134 | Quarterly | 1989-present | Direct (component) | Yes (FRED) |
| Top 0.1% net worth share | Federal Reserve DFA (via FRED) | WFRBSTP1300 | Quarterly | 1989-present | Direct (component) | Yes (FRED) |
| Bottom 50% net worth share | Federal Reserve DFA (via FRED) | WFRBSB50107 | Quarterly | 1989-present | Direct (component for reference) | Yes (FRED) |
| Top 1% pre-tax income share | WID.world | sptinc992j (US) | Annual | 1913-present | Direct (income dimension) | No |
| Top 0.1% pre-tax income share | WID.world | sptinc p99.9p100 (US) | Annual | 1913-present | Direct (income dimension) | No |
| Top 10% pre-tax income share | WID.world | sptinc p90p100 (US) | Annual | 1913-present | Direct (income dimension) | No |

**Recommended:** Construct the intra-elite concentration ratio from Fed DFA data as the primary measure: WFRBSTP1300 / (WFRBST01134 - WFRBSTP1300). This captures how much of the top 1%'s wealth is concentrated in the top 0.1% -- higher ratio = more extreme concentration at the very top. The Fed DFA data has quarterly frequency (1989-present) which is better for model building than WID annual data. For longer historical coverage, use WID income shares to construct the analogous ratio back to 1913.

**Construction Recipe (Intra-Elite Concentration Ratio):**
1. From FRED: obtain WFRBSTP1300 (top 0.1% net worth share) and WFRBST01134 (top 1% net worth share)
2. Compute "merely affluent" share: merely_affluent = WFRBST01134 - WFRBSTP1300 (this is the 99.0-99.9th percentile)
3. Intra-elite ratio = WFRBSTP1300 / merely_affluent
4. Higher ratio = more concentration within the elite (top 0.1% pulling away from top 1-10%)
5. For WID income analog: ratio = sptinc_p99.9p100 / (sptinc_p99p100 - sptinc_p99.9p100)

**Rate Limits:** FRED API: 120 requests/minute. WID.world: no documented rate limits for bulk CSV download.
**License:** FRED/DFA data: public domain (Federal Reserve). WID: CC BY 4.0.
**Known Gaps:**
- Fed DFA starts only in 1989 -- limits backtesting to ~35 years. WID income shares extend to 1913 but measure income, not wealth.
- Fed DFA and WID use different methodologies: DFA is based on the Financial Accounts + Survey of Consumer Finances; WID uses tax data + national accounts. Levels are not directly comparable.
- The "top 0.1%" threshold is arbitrary -- the theory suggests a continuous gradient of elite frustration, not a discrete cutoff
- WID API endpoint stability is uncertain -- bulk CSV download or R package (`wid-r-tool`) recommended as fallback

**Last Verified:** 2026-03-03 (WFRBST01134 and WFRBSTP1300 confirmed active via MCP `fred_series_info`; WID via web research)

---

### Middle-Class Income Share (#20)

**Catalog Rating:** Moderate
**Theoretical Concept:** The share of national income accruing to the middle three income quintiles (20th-80th percentile). A direct measure of middle-class economic health. Alesina & Perotti (1996) find middle-class income share is a stronger predictor of instability than the Gini coefficient.
**Availability Classification:** Available (free API) + Available (manual download)

#### Measures

| Measure | Source | Series/Endpoint | Frequency | Coverage | Proxy Tier | API Key? |
|---------|--------|-----------------|-----------|----------|------------|----------|
| Income shares by quintile (2nd + 3rd + 4th quintile) | Census Bureau | Table B19082 (ACS) or historical Table H-2 | Annual | 1967-present (historical tables), 2005-present (ACS) | Direct | No (Census API) |
| Median household income relative to mean | Census Bureau (via FRED) | Derived: MEHOINUSA672N / MAFAINUSA646N | Annual | 1984-present | Strong proxy (median-to-mean ratio proxies middle-class share) | Yes (FRED) |
| Pre-tax income share P50-P90 group | WID.world | sptinc p50p90 (US) | Annual | 1913-present | Direct (income share of upper-middle class) | No |
| Share of aggregate income by quintile | Census Bureau | Historical Table H-2 from census.gov | Annual | 1967-present | Direct | No |

**Recommended:** Census Bureau income shares by quintile as the primary measure. Sum the 2nd, 3rd, and 4th quintile shares from Census historical Table H-2 (available 1967-present) to compute the middle 60% income share. Supplement with WID P50-P90 income share for longer history (1913-present) and the income concentration perspective. The median-to-mean ratio from FRED provides a monthly-frequency proxy.

**Construction Recipe (Middle-Class Income Share from Census):**
1. Download Census historical Table H-2 from census.gov/data/tables/time-series/demo/income-poverty/historical-income-households.html
2. Extract shares for 2nd quintile, 3rd quintile, and 4th quintile
3. Middle-class share = sum of 2nd + 3rd + 4th quintile shares
4. Track over time -- declining share = middle-class squeeze
5. For WID alternative: download P50-P90 pre-tax income share from wid.world/data (series sptinc p50p90 for US)

**Rate Limits:** Census API: 500 requests/day without key. FRED API: 120 requests/minute. WID: no documented limits.
**License:** Public domain (Census, FRED). WID: CC BY 4.0.
**Known Gaps:**
- Census quintile shares are based on money income before taxes -- does not capture the effect of taxes and transfers, which significantly affect the middle-class income picture
- Census income definition changed in 2013 (redesigned income questions) creating a comparability break -- Census provides bridge tables
- WID uses "pre-tax national income" which includes non-cash income and employer contributions -- different concept from Census money income
- The "middle 60%" definition is one of several possible operationalizations; Alesina & Perotti (1996) use the "middle class" as the 3rd and 4th quintile only (middle 40%)

**Last Verified:** 2026-03-03 (FRED series for median/mean income confirmed active; Census historical tables confirmed available via web; WID P50-P90 series confirmed via WID data documentation)

---

### Anti-System Party Vote Share (#31)

**Catalog Rating:** Moderate
**Theoretical Concept:** The electoral support for parties or candidates that reject core democratic norms or challenge the legitimacy of the political system. Funke et al. (2016) find that financial crises produce a ~30% increase in far-right vote share with a 5-10 year lag -- the single strongest documented economic-to-political transmission mechanism.
**Availability Classification:** Available (manual download) -- with coding decision deferred

#### Measures

| Measure | Source | Series/Endpoint | Frequency | Coverage | Proxy Tier | API Key? |
|---------|--------|-----------------|-----------|----------|------------|----------|
| Third-party presidential vote share | Dave Leip's Atlas / Wikipedia / MIT Election Lab | CSV download from MIT Election Data + Science Lab (electionlab.mit.edu) | Per presidential election (quadrennial) | 1789-present | Strong proxy (third-party voting as system rejection) | No |
| FEC candidate financial data | FEC | `fec_search_candidates` MCP tool | Per election cycle | 1980-present (electronic filings) | Strong proxy (financial viability of anti-system candidates) | No |
| State-level election returns | MIT Election Data + Science Lab | CSV download from dataverse.harvard.edu | Per election | 2000-present (standardized) | Direct (when combined with coding) | No |
| Populist vote share composite | Academic coding required | Constructed from election returns + candidate classification | Per election | Requires manual coding | Direct (but requires Phase 4 coding decisions) | N/A |

**Recommended:** MIT Election Data + Science Lab election returns as the primary data source. This provides standardized US election returns at the candidate level for presidential, Senate, and House races. However, the data provides vote totals, NOT anti-system classification -- determining which candidates/parties qualify as "anti-system" requires a coding decision deferred to Phase 4.

**IMPORTANT -- Coding Decision Required (Phase 4):**
Defining "anti-system" for the US context requires explicit criteria. Options include:
- **Third-party only:** All non-D/non-R candidates (simple but misses anti-system major-party candidates)
- **Expert coding:** Classify candidates based on platform analysis (rigorous but subjective and labor-intensive)
- **Behavioral markers:** Candidates who contested election results, called for institutional change, or rejected democratic norms
- The Funke et al. (2016) operationalization uses "far-right" party family classification, which does not map cleanly onto the US two-party system

**Rate Limits:** MIT Election Lab: no API, CSV download. FEC MCP tool: standard MCP limits.
**License:** MIT Election Lab data: CC BY 4.0. FEC data: public domain (US government).
**Known Gaps:**
- FEC provides financial data (contributions, spending), NOT vote totals -- must use MIT Election Lab or state Secretary of State data for actual vote shares
- US two-party system makes "anti-system" classification fundamentally different from European multi-party systems where Funke et al. (2016) is calibrated
- Third-party vote share is a noisy proxy -- some third-party votes are protest votes, not anti-system sentiment
- No standardized dataset of US election returns with anti-system coding exists; this must be constructed
- Quadrennial frequency for presidential elections severely limits time series density; midterm House races provide biennial data but with more complex aggregation

**Last Verified:** 2026-03-03 (MIT Election Lab confirmed active; FEC MCP tool confirmed operational)

---

### Wealth Concentration - Top 0.1% (#45)

**Catalog Rating:** Strong
**Theoretical Concept:** The share of national wealth held by the top 0.1% of the distribution. Captures the emergence of an economic oligarchy distinct from general inequality. Saez & Zucman (2016) document that US top 0.1% wealth share tripled from ~7% to ~20% since 1978. Treated as separate from general inequality (#1) because extreme concentration captures qualitatively different elite capture dynamics.
**Availability Classification:** Available (free API) + Available (manual download)

#### Measures

| Measure | Source | Series/Endpoint | Frequency | Coverage | Proxy Tier | API Key? |
|---------|--------|-----------------|-----------|----------|------------|----------|
| Share of Net Worth Held by Top 0.1% | Federal Reserve DFA (via FRED) | WFRBSTP1300 | Quarterly | 1989-present | Direct | Yes (FRED) |
| Top 0.1% pre-tax income share | WID.world | sptinc p99.9p100 (US) | Annual | 1913-present | Direct (income dimension) | No |
| Top 0.1% wealth share | WID.world | shweal p99.9p100 (US) | Annual | 1913-present | Direct (wealth dimension) | No |
| Share of Net Worth Held by Top 1% | Federal Reserve DFA (via FRED) | WFRBST01134 | Quarterly | 1989-present | Strong proxy (broader top-end concentration) | Yes (FRED) |

**Recommended:** WFRBSTP1300 (Fed DFA top 0.1% net worth share) as the primary measure. It is quarterly (vs. WID annual), freely available on FRED, and directly measures wealth concentration at the 0.1% threshold. Supplement with WID shweal p99.9p100 for the longer historical perspective (1913-present) that captures the full U-shaped trajectory of US wealth concentration documented by Piketty and Saez.

**Tradeoff: Fed DFA vs. WID:**
- **Fed DFA (WFRBSTP1300):** Quarterly, 1989-present, based on Financial Accounts + Survey of Consumer Finances, FRED-accessible
- **WID (shweal p99.9p100):** Annual, 1913-present, based on tax data + national accounts capitalization, CSV/R download
- For model building, Fed DFA's quarterly frequency is preferred. For backtesting against historical episodes (Great Depression, Gilded Age), WID's century-long coverage is essential.

**Rate Limits:** FRED API: 120 requests/minute. WID: no documented rate limits for bulk download.
**License:** FRED/DFA: public domain (Federal Reserve). WID: CC BY 4.0.
**Known Gaps:**
- Fed DFA starts only in 1989 -- cannot backtest against pre-1989 wealth concentration episodes
- WID wealth estimates for the US are methodologically contested: Saez & Zucman (2016) vs. Smith, Zidar & Zwick (2023) produce meaningfully different top wealth shares depending on capitalization assumptions
- Top 0.1% is approximately 130,000 households in the US -- the threshold is stable in population terms but the composition changes
- Wealth concentration is measured at household level in DFA but at individual/tax-unit level in WID -- not directly comparable at the level

**Last Verified:** 2026-03-03 (WFRBSTP1300 confirmed active through Jul 2025 via MCP `fred_series_info`; WID wealth shares confirmed via web research)

---

## Domain Summary: Political Polarization & Elite Dynamics

### Coverage Assessment

| Variable | # | Rating | Availability | Primary Source | Coverage Start |
|----------|---|--------|-------------|----------------|----------------|
| Political Polarization (Congressional) | 3 | Strong | Available (manual download) | VoteView DW-NOMINATE | 1789 |
| Affective Polarization | 4 | Strong | Available (manual download) | ANES feeling thermometers | 1948 |
| Elite Factionalism / Fragmentation | 11 | Strong | Partially available | Constructed (VoteView intra-party SD) | 1789 |
| Horizontal Inequality (Between-Group) | 15 | Moderate | Available (free API) | Census racial income ratios | 1967 |
| Intra-Elite Wealth Gap | 19 | Moderate | Available (free API) | Fed DFA (WFRBSTP1300/WFRBST01134) | 1989 |
| Middle-Class Income Share | 20 | Moderate | Available (free API) | Census quintile shares | 1967 |
| Anti-System Party Vote Share | 31 | Moderate | Available (manual download) | MIT Election Lab + coding | 1789 |
| Wealth Concentration (Top 0.1%) | 45 | Strong | Available (free API) | WFRBSTP1300 | 1989 |

### Key Statistics

- **Total variables:** 8
- **Available (free API):** 3 (38%) -- #15, #19, #45 (with FRED DFA series)
- **Available (manual download):** 4 (50%) -- #3, #4, #20, #31 (VoteView, ANES, Census tables, MIT Election Lab)
- **Partially available (proxy needed):** 1 (13%) -- #11 Elite Factionalism (constructible from VoteView)
- **Unavailable:** 0
- **Strong-rated:** 4 (50%) -- #3, #4, #11, #45
- **Moderate-rated:** 4 (50%) -- #15, #19, #20, #31
- **Contested:** 0
- **Short series (post-2000 start):** 0 (all primary measures start before 2000; some alternatives are short)
- **Frequency mix:** Quarterly (2 via FRED), Biennial/per-Congress (3), Annual (2), Quadrennial (1)
- **MCP-verified components:** 4 -- WFRBSTP1300, WFRBST01134, WFRBSB50107 (FRED); FEC candidate search; Congressional vote tools

### Critical Gaps

1. **Anti-system party coding (#31):** Data sources provide raw election returns, but classifying candidates as "anti-system" requires an explicit coding scheme. This is a Phase 4 methodology decision -- no pre-built dataset exists.

2. **Affective polarization frequency (#4):** ANES data is biennial/quadrennial, creating sparse time series. LOCF alignment is the project standard, but this means affective polarization values are held constant for 2-4 years between measurements. Pew data supplements frequency since 2014 but uses different methodology.

3. **Elite factionalism construction (#11):** The PITF model uses a categorical 0-3 expert coding for factionalism. Our continuous DW-NOMINATE SD proxy captures a narrower concept (ideological dispersion, not all forms of factionalism). The mapping from continuous SD to the PITF categorical framework is not validated.

### Data Sources Used

| Source | Variables Served | API Key Required |
|--------|-----------------|-----------------|
| VoteView (voteview.com/data) | #3, #11 (CSV download) | No |
| ANES (electionstudies.org) | #4 (CSV download, free registration) | No |
| Federal Reserve DFA (via FRED) | #19, #45 (3 series: WFRBSTP1300, WFRBST01134, WFRBSB50107) | Yes (FRED key) |
| WID.world | #19, #45 (income/wealth shares, CSV download) | No |
| Census Bureau | #15, #20 (ACS tables, historical tables) | No (API limited without key) |
| MIT Election Data + Science Lab | #31 (CSV download) | No |
| FEC (via MCP) | #11, #31 (candidate search) | No |
| BLS / FRED | #15 (earnings by race series) | Yes (FRED key) |

---

## Domain 3: Institutional / Democratic Quality

This domain covers 8 variables from the Phase 2 catalog that measure the quality of democratic institutions, checks and balances, and governance effectiveness. This is the largest gap in the existing 3 models -- the institutional dimension is entirely uncovered in Turchin PSI, Prospect Theory PLI, and Financial Stress Pathway (per Phase 2 synthesis finding). Most variables source from V-Dem v15, making this domain heavily dependent on a single dataset. Non-V-Dem alternatives (Freedom House, Grumbach, World Bank WGI, Bright Line Watch, Electoral Integrity Project) are documented for robustness.

**Variables in this domain:** #13, #21, #22, #23, #24, #29, #32, #38

**V-Dem Common Documentation:**
All V-Dem variables share these access details:
- **Download:** https://v-dem.net/data/the-v-dem-dataset/ -> Country-Year: V-Dem Full+Others -> CSV
- **File:** V-Dem-CY-Full+Others-v15.csv
- **Version:** v15 (released March 2025)
- **US Coverage:** Full coding, 1789-present, annual
- **License:** Creative Commons Attribution 4.0 International (CC BY 4.0)
- **Update Frequency:** Annual (typically March release)
- **Measurement Method:** Expert survey (country experts code each indicator), aggregated via Bayesian item response theory models
- **API Key Required:** No -- free CSV download
- **Rate Limits:** N/A (file download, not API)
- **Known US Limitation:** Many V-Dem indices for the US are near the ceiling (maximum score) because the US has historically been coded as a full liberal democracy. This means absolute levels are less informative than within-country trends and rate-of-change. Recent V-Dem reports (2023-2025) have noted declining US scores on several indicators, but the variation is subtle compared to cross-national differences.

---

### Regime Type / Institutional Quality (#13)

**Catalog Rating:** Strong -- Contested
**Theoretical Concept:** The quality of democratic institutions and the degree to which the political system is a full democracy, partial democracy (anocracy), or autocracy. The PITF model's single strongest predictor -- Goldstone et al. (2010) find partial democracies with factionalism are 10-15x more failure-prone than full democracies or autocracies. Contested because Walter (2022) argues the US has moved toward the anocratic zone while Svolik (2019) contends established democracies have different risk dynamics.
**Availability Classification:** Available (manual download)

#### Measures

| Measure | Source | Series/Endpoint | Frequency | Coverage | Proxy Tier | API Key? |
|---------|--------|-----------------|-----------|----------|------------|----------|
| Liberal Democracy Index | V-Dem v15 | v2x_libdem | Annual | 1789-present | Direct | No |
| Polyarchy (Electoral Democracy) Index | V-Dem v15 | v2x_polyarchy | Annual | 1789-present | Direct | No |
| Regimes of the World classification | V-Dem v15 | v2x_regime (0-3 ordinal) | Annual | 1789-present | Direct (categorical) | No |
| Regimes of the World (ambiguous cases) | V-Dem v15 | v2x_regime_amb (0-9 ordinal) | Annual | 1789-present | Direct (finer-grained categorical) | No |
| Freedom in the World scores | Freedom House | freedomhouse.org (PDF/Excel) | Annual | 1972-present | Direct | No |
| Freedom in the World Aggregate/Subcategory Scores | Freedom House | freedomhouse.org/report/freedom-world | Annual | 2003-present (current methodology) | Direct | No |

**Recommended:** V-Dem v2x_libdem (Liberal Democracy Index) as the primary measure, supplemented by v2x_polyarchy for the electoral democracy dimension. V-Dem provides the longest coverage (1789-present) with the most granular measurement (continuous 0-1 scale vs. Freedom House ordinal 1-7). For the rate-of-change analysis that matters for the US context, compute year-over-year change in v2x_libdem. Freedom House provides a well-known cross-validation source but has shorter coverage and coarser measurement.

**Scale and Interpretation:**
- v2x_libdem: Continuous 0-1 (0 = least democratic, 1 = most democratic). US typically scores 0.85-0.90.
- v2x_polyarchy: Continuous 0-1. US typically scores 0.87-0.92.
- v2x_regime: 0 = closed autocracy, 1 = electoral autocracy, 2 = electoral democracy, 3 = liberal democracy. US coded as 3 (liberal democracy) throughout modern period.
- v2x_regime_amb: 0-9 scale with ambiguous cases split into separate categories.
- Freedom House: 1 (most free) to 7 (least free) for Political Rights and Civil Liberties.

**Rate Limits:** V-Dem: CSV download, no rate limits. Freedom House: report download, no rate limits.
**License:** V-Dem: CC BY 4.0. Freedom House: data available for non-commercial use with attribution.
**Known Gaps:**
- Contested variable: The US is coded as a full liberal democracy (v2x_regime = 3) throughout the V-Dem dataset. Walter (2022) argues the US has moved toward "anocracy" based on Polity scores, but V-Dem does not code the US as having crossed any categorical threshold. The variation is in continuous index values, not regime type.
- Do NOT use Polity V as a source -- it is deprecated (final version 2018, no longer updated). V-Dem is the current standard.
- Freedom House's current methodology (with disaggregated subcategory scores) dates only from 2003. Earlier scores use a different aggregation method.
- V-Dem expert surveys are retrospective for historical periods -- coding of 18th-19th century US institutions involves unavoidable historical judgment calls
- Rate of change in v2x_libdem is more analytically useful for the US than the absolute level (which has been near ceiling)

**Last Verified:** 2026-03-03 (V-Dem v15 confirmed released March 2025 via web research; Freedom House 2025 report confirmed published)

---

### Judicial Independence (#21)

**Catalog Rating:** Moderate
**Theoretical Concept:** The degree to which the judiciary operates independently of executive and legislative interference. A critical check on executive power and a pillar of democratic governance. Ginsburg & Huq (2018) identify judicial independence as one of five infrastructure domains vulnerable to democratic erosion. Levitsky & Ziblatt (2018) highlight the politicization of judicial appointments as a norm-breaking signal.
**Availability Classification:** Available (manual download)

#### Measures

| Measure | Source | Series/Endpoint | Frequency | Coverage | Proxy Tier | API Key? |
|---------|--------|-----------------|-----------|----------|------------|----------|
| High Court Independence | V-Dem v15 | v2juhcind | Annual | 1789-present | Direct | No |
| Lower Court Independence | V-Dem v15 | v2juncind | Annual | 1789-present | Direct | No |
| Judicial Constraints on Executive | V-Dem v15 | v2x_jucon | Annual | 1789-present | Direct (composite index) | No |
| Compliance with High Court Rulings | V-Dem v15 | v2jucomp | Annual | 1789-present | Direct (behavioral indicator) | No |

**Recommended:** V-Dem v2x_jucon (Judicial Constraints on Executive) as the primary measure. It is a composite index that captures both judicial independence and the judiciary's effective capacity to constrain executive action -- directly measuring the separation-of-powers function that matters for democratic quality. Supplement with v2juhcind (High Court Independence) and v2juncind (Lower Court Independence) for component-level analysis.

**Scale and Interpretation:**
- v2juhcind: Ordinal expert rating, aggregated to continuous interval via IRT. Higher = more independent.
- v2juncind: Same scale as v2juhcind but for lower courts.
- v2x_jucon: Composite index, continuous 0-1. Higher = stronger judicial constraints on executive.
- v2jucomp: Ordinal expert rating on compliance with court rulings. Higher = more compliance.

**Rate Limits:** V-Dem: CSV download, no rate limits.
**License:** V-Dem: CC BY 4.0.
**Known Gaps:**
- US judicial independence scores have been near ceiling historically -- recent variation (if any) is subtle in the V-Dem coding
- V-Dem expert surveys capture *de jure* and *de facto* independence but may lag real-time developments (e.g., inspector general firings, executive non-compliance with court orders)
- The politicization of judicial appointments (Senate confirmation battles) may not be fully captured by V-Dem's measurement of judicial independence per se
- No non-V-Dem quantitative alternative exists with comparable coverage -- Bright Line Watch expert surveys provide a supplementary signal since 2017 but are irregular

**Last Verified:** 2026-03-03 (V-Dem v15 variable list confirmed via V-Dem codebook documentation)

---

### Freedom of Expression / Media Independence (#22)

**Catalog Rating:** Moderate
**Theoretical Concept:** The degree to which media operates independently of government control and citizens can freely express political views. A critical information channel for democratic accountability. Bermeo (2016) identifies media restriction as a common tool of executive aggrandizement in contemporary democratic backsliding episodes.
**Availability Classification:** Available (manual download)

#### Measures

| Measure | Source | Series/Endpoint | Frequency | Coverage | Proxy Tier | API Key? |
|---------|--------|-----------------|-----------|----------|------------|----------|
| Freedom of Expression and Alternative Sources of Information | V-Dem v15 | v2x_freexp_altinf | Annual | 1789-present | Direct (composite index) | No |
| Government Censorship Effort (Media) | V-Dem v15 | v2mecenefm | Annual | 1789-present | Direct (specific component) | No |
| Media Bias | V-Dem v15 | v2mebias | Annual | 1789-present | Direct (media landscape indicator) | No |
| Press Freedom Index | Reporters Without Borders (RSF) | rsf.org/en/index | Annual | 2002-present | Direct | No |
| Freedom on the Net scores | Freedom House | freedomhouse.org/report/freedom-net | Annual | 2011-present | Direct (internet freedom dimension) | No |

**Recommended:** V-Dem v2x_freexp_altinf (Freedom of Expression and Alternative Sources of Information) as the primary measure for its long coverage (1789-present) and comprehensive composite construction. Supplement with Reporters Without Borders Press Freedom Index for the most widely cited international press freedom ranking (2002-present) and Freedom House Freedom on the Net for the digital dimension (2011-present).

**Scale and Interpretation:**
- v2x_freexp_altinf: Composite index, continuous 0-1. Higher = more freedom. Includes government censorship, media bias, freedom of discussion, and alternative information access.
- RSF Press Freedom Index: Continuous score (0-100 in current methodology, reversed from historical). Lower rank = more press freedom. US typically ranks 40th-50th globally (has declined from top 20 pre-2016).
- Freedom on the Net: 0-100 aggregate score. Higher = more freedom. US typically scores 75-78.

**Tradeoff: V-Dem vs. RSF vs. Freedom House:**
- **V-Dem:** Longest coverage (1789-present), broadest concept (expression + information access), academic standard
- **RSF:** Most widely cited in journalism/policy, captures media-specific threats, but short (2002-present) and methodology changed in 2022
- **Freedom House FotN:** Captures internet/digital freedom specifically, very short (2011-present)
- For this project, V-Dem as primary with RSF as robustness check is recommended.

**Rate Limits:** V-Dem: CSV download. RSF: annual report/data download from rsf.org. Freedom House: report download.
**License:** V-Dem: CC BY 4.0. RSF: data available with attribution. Freedom House: data available for non-commercial use with attribution.
**Known Gaps:**
- RSF methodology changed significantly in 2022 (new indicator framework), creating a comparability break with pre-2022 scores
- US Freedom of Expression scores in V-Dem have been near ceiling historically; recent changes are subtle
- None of these measures capture the *perception* of media bias or trust in media, which is captured by #28 (Media Trust, a different variable in the catalog)
- Freedom on the Net scores (2011-present) are too short for meaningful time series analysis -- tag as "short series" if used

**Last Verified:** 2026-03-03 (V-Dem v15 confirmed; RSF 2025 index confirmed published; Freedom House FotN 2024 report confirmed published)

---

### Legislative Constraints on Executive (#23)

**Catalog Rating:** Moderate
**Theoretical Concept:** The degree to which the legislature effectively constrains executive power through oversight, investigation, and legislative authority. A core separation-of-powers indicator. Ginsburg & Huq (2018) identify legislative constraints as one of five infrastructure domains vulnerable to constitutional retrogression.
**Availability Classification:** Available (manual download)

#### Measures

| Measure | Source | Series/Endpoint | Frequency | Coverage | Proxy Tier | API Key? |
|---------|--------|-----------------|-----------|----------|------------|----------|
| Legislative Constraints on the Executive Index | V-Dem v15 | v2xlg_legcon | Annual | 1789-present | Direct (composite index) | No |
| Executive Respects Constitution | V-Dem v15 | v2exrescon | Annual | 1789-present | Direct (executive behavior indicator) | No |
| Legislature Investigates in Practice | V-Dem v15 | v2lginvstp | Annual | 1789-present | Direct (oversight function) | No |
| Legislature Controls Resources | V-Dem v15 | v2lgfunds | Annual | 1789-present | Direct (power of the purse) | No |

**Recommended:** V-Dem v2xlg_legcon (Legislative Constraints on the Executive Index) as the primary measure. It is a composite capturing multiple dimensions of legislative power: ability to investigate, question officials, control budgets, and override vetoes. Supplement with v2exrescon (Executive Respects Constitution) for the executive behavior dimension -- does the executive actually comply with constitutional constraints?

**Scale and Interpretation:**
- v2xlg_legcon: Composite index, continuous 0-1. Higher = stronger legislative constraints on executive.
- v2exrescon: Ordinal expert rating, aggregated to interval. Higher = more executive respect for constitutional provisions.
- v2lginvstp: Ordinal expert rating on legislative investigation capacity. Higher = more effective oversight.
- v2lgfunds: Ordinal expert rating on legislative control of resources. Higher = more fiscal control.

**Rate Limits:** V-Dem: CSV download, no rate limits.
**License:** V-Dem: CC BY 4.0.
**Known Gaps:**
- US legislative constraints scores have been near ceiling historically in V-Dem coding -- the US system of divided powers has been a model case
- Rate of change is more informative than absolute level for the US context
- V-Dem's expert survey approach may not capture rapid changes in executive-legislative dynamics (e.g., government shutdowns, impoundment disputes, inspector general firings) until the following year's coding
- No quantitative non-V-Dem alternative exists with comparable coverage for this specific concept -- the closest substitute is the generic "checks and balances" literature, which is more qualitative

**Last Verified:** 2026-03-03 (V-Dem v15 variable list confirmed via V-Dem codebook documentation)

---

### Electoral Integrity / Fraud Perception (#24)

**Catalog Rating:** Moderate
**Theoretical Concept:** The degree to which elections are perceived as free, fair, and legitimate. Tucker (2007) finds that perceived electoral fraud triggered all Color Revolutions. Post-2020 US election denial represents a critical context where fraud perception diverges sharply from electoral integrity reality.
**Availability Classification:** Available (manual download)

#### Measures

| Measure | Source | Series/Endpoint | Frequency | Coverage | Proxy Tier | API Key? |
|---------|--------|-----------------|-----------|----------|------------|----------|
| Clean Elections Index | V-Dem v15 | v2xel_frefair | Annual | 1789-present | Direct (structural electoral integrity) | No |
| Election Management Body Autonomy | V-Dem v15 | v2elembaut | Annual | 1789-present | Direct (institutional independence) | No |
| Election Government Intimidation | V-Dem v15 | v2elintim | Annual | 1789-present | Direct (coercion indicator) | No |
| Perception of Electoral Integrity (PEI) | Electoral Integrity Project (Pippa Norris) | Harvard Dataverse download | Per election cycle | 2012-present (selected countries) | Direct (expert perception) | No |
| State Democracy Index | Grumbach (2023) | Harvard Dataverse / author website | Annual | 2000-2018 (published range) | Strong proxy (state-level electoral quality) | No |

**Recommended:** V-Dem v2xel_frefair (Clean Elections Index) as the primary structural measure. It captures whether elections are free from manipulation, intimidation, and fraud based on expert coding. For the perception dimension (critical in the post-2020 US context), supplement with the Electoral Integrity Project's PEI data (expert survey of election quality, available for US elections since 2012).

**Scale and Interpretation:**
- v2xel_frefair: Composite index, continuous 0-1. Higher = cleaner elections. US typically scores near maximum.
- PEI: Expert survey rating (1-100 per election). US presidential elections have scored 62-72 (moderate by global standards, reflecting structural issues like gerrymandering and campaign finance).
- Grumbach SDI: State-level democracy index capturing electoral rules, registration requirements, and gerrymandering. Higher = more democratic.

**Rate Limits:** V-Dem: CSV download. PEI/Grumbach: academic dataverse download.
**License:** V-Dem: CC BY 4.0. PEI: CC BY (Harvard Dataverse). Grumbach: academic open data.
**Known Gaps:**
- V-Dem captures structural electoral integrity but does NOT capture public perception of fraud -- a critical gap given post-2020 US politics where a significant minority believes elections were stolen despite structural integrity measures showing otherwise
- PEI is available only from 2012 and covers selected elections -- not a continuous time series
- Grumbach (2023) SDI is state-level, requiring national aggregation for composite indicator use. Published data range is 2000-2018; updates may extend coverage.
- Survey data on fraud perception (e.g., "Do you believe the 2020 election was legitimate?") exists in various polls but is not systematically compiled into a time series
- The gap between actual electoral integrity (V-Dem: high) and perceived integrity (diverging by partisanship) is itself the analytically important signal -- Phase 4 should consider modeling this gap

**Last Verified:** 2026-03-03 (V-Dem v15 confirmed; PEI project confirmed active via Harvard Dataverse; Grumbach SDI confirmed via web research)

---

### Voter Access Restrictions / Partisan Gerrymandering (#29)

**Catalog Rating:** Moderate
**Theoretical Concept:** The degree to which electoral rules restrict voter participation or distort representation through gerrymandering. A primarily state-level phenomenon in the US. Grumbach (2023) documents significant cross-state variation in democratic quality, with voter access restrictions as a key dimension of state-level democratic backsliding.
**Availability Classification:** Available (manual download) -- primarily state-level data

#### Measures

| Measure | Source | Series/Endpoint | Frequency | Coverage | Proxy Tier | API Key? |
|---------|--------|-----------------|-----------|----------|------------|----------|
| State Democracy Index (voter access components) | Grumbach (2023) | Harvard Dataverse / author website (CSV) | Annual | 2000-2018 (published range) | Direct (comprehensive state-level measure) | No |
| Efficiency gap (partisan gerrymandering measure) | Stephanopoulos & McGhee (2015) | Constructible from election returns | Per redistricting cycle (~decennial) | Computable for any election with district-level returns | Direct (quantitative gerrymandering metric) | No |
| Cost of Voting Index | Li, Pomante & Schraufnagel (2018) | Academic dataset (Harvard Dataverse) | Per election cycle | 1996-2020 (published range) | Direct (comparative voter access measure) | No |
| Voter restriction legislation tracking | Brennan Center for Justice | Published reports from brennancenter.org | Per legislative session | 2011-present (systematic tracking) | Strong proxy (legislative activity indicator) | No |

**Recommended:** Grumbach (2023) State Democracy Index as the primary measure for its comprehensive, multi-dimensional approach to state-level democratic quality. It combines voter access rules, gerrymandering, campaign finance regulations, and other dimensions into a single state-level index. For national aggregation, compute population-weighted average across states. Supplement with the Cost of Voting Index (Li et al.) for a narrower voter-access-specific measure.

**Construction Recipe (National Aggregation from State-Level Data):**
1. Download Grumbach SDI data from Harvard Dataverse
2. For each year, obtain SDI score for each state
3. Compute population-weighted national average: sum(SDI_state * population_state) / total_population
4. Alternatively, compute the standard deviation across states (captures cross-state divergence in democratic quality)
5. Both the weighted average and the dispersion are analytically interesting

**Rate Limits:** Academic dataverse: standard download, no rate limits. Brennan Center: report download.
**License:** Grumbach SDI: academic open data (Harvard Dataverse). Cost of Voting Index: academic open data. Brennan Center: reports freely available.
**Known Gaps:**
- Grumbach SDI published range is 2000-2018 -- may need to check for updates extending coverage beyond 2018
- The efficiency gap is computable only after each election with full district-level returns, making it available on a per-redistricting-cycle basis (roughly decennial, with updates after each election)
- National aggregation from state-level data requires methodological choices (population weighting, median vs. mean, etc.) that are Phase 4 decisions
- Voter restriction tracking (Brennan Center) is a count of legislative actions, not a continuous quality index -- more useful for narrative context than quantitative modeling
- State-level measures capture the most policy-relevant variation but are harder to integrate into national-level composite indicators

**Last Verified:** 2026-03-03 (Grumbach SDI confirmed via Harvard Dataverse; Cost of Voting Index confirmed via web research; Brennan Center reports confirmed available)

---

### Executive Aggrandizement (#32)

**Catalog Rating:** Moderate
**Theoretical Concept:** Actions by elected executives that concentrate power beyond institutional norms. Bermeo (2016) identifies executive aggrandizement as the most common form of 21st-century democratic backsliding, replacing the military coups and electoral fraud of earlier eras. Haggard & Kaufman (2021) find executive aggrandizement occurred in 14 of 16 backsliding cases studied.
**Availability Classification:** Available (manual download)

#### Measures

| Measure | Source | Series/Endpoint | Frequency | Coverage | Proxy Tier | API Key? |
|---------|--------|-----------------|-----------|----------|------------|----------|
| Executive Corruption Index | V-Dem v15 | v2x_execorr | Annual | 1789-present | Strong proxy (executive abuse of power) | No |
| Executive Respects Constitution | V-Dem v15 | v2exrescon | Annual | 1789-present | Direct (constitutional compliance) | No |
| Executive Attempts to Control Judiciary | V-Dem v15 | v2jupack | Annual | 1789-present | Direct (court-packing attempts) | No |
| Executive Oversight by Legislature | V-Dem v15 | v2lgotovst | Annual | 1789-present | Direct (inverse indicator -- weak oversight enables aggrandizement) | No |
| Bright Line Watch expert surveys | Bright Line Watch | brightlinewatch.org | Irregular (roughly quarterly since 2017) | 2017-present | Direct (expert assessment of democratic norm violations) | No |

**Recommended:** V-Dem v2exrescon (Executive Respects Constitution) as the primary measure for its direct relevance to the aggrandizement concept and long coverage. Supplement with v2x_execorr (Executive Corruption Index) for the abuse-of-power dimension and v2jupack (judicial packing attempts) for a specific aggrandizement mechanism. For the most current US assessment, Bright Line Watch expert surveys (2017-present) provide real-time monitoring of democratic norm violations by experts in democratic governance.

**Scale and Interpretation:**
- v2exrescon: Ordinal expert rating, aggregated to interval. Higher = more respect for constitution.
- v2x_execorr: Composite index, continuous 0-1. Higher = more executive corruption. (Note: reversed from other V-Dem indices -- higher is *worse*.)
- v2jupack: Ordinal expert rating on executive attempts to increase the number of judges or replace judges to change court composition. Higher = fewer packing attempts.
- Bright Line Watch: Expert ratings on a battery of democratic norm statements (1-4 Likert scale per item). Aggregated mean across items. Higher = healthier democratic norms.

**Rate Limits:** V-Dem: CSV download. Bright Line Watch: report/data download from brightlinewatch.org.
**License:** V-Dem: CC BY 4.0. Bright Line Watch: freely available academic data.
**Known Gaps:**
- V-Dem measures executive aggrandizement indirectly through its component indicators -- no single "executive aggrandizement" index exists in V-Dem. The concept must be operationalized from components.
- Bright Line Watch data begins only in 2017 -- tag as "short series." It was created specifically to monitor US democratic norms during the Trump administration.
- Bright Line Watch survey frequency is irregular (roughly quarterly but not fixed schedule) -- use LOCF for alignment
- The concept of "executive aggrandizement" is inherently difficult to measure quantitatively -- it involves identifying departures from norms that are themselves contested. V-Dem's expert survey approach handles this better than any available alternative, but expert disagreement is embedded in the uncertainty estimates.
- No pre-built time series of "executive aggrandizement events" exists for the US -- event coding would require Phase 4 construction work

**Last Verified:** 2026-03-03 (V-Dem v15 confirmed; Bright Line Watch confirmed active with 2025 survey waves published)

---

### State Capacity / Institutional Quality (#38)

**Catalog Rating:** Moderate
**Theoretical Concept:** The government's ability to effectively deliver public services, enforce laws, and respond to crises. Fearon & Laitin (2003) find that weak state capacity predicts conflict regardless of ethnic composition. Kaufman & Haggard (2021) find that strong institutions buffer economic shocks from producing democratic backsliding. State capacity is multidimensional: extractive (taxation), coercive (law enforcement), and administrative (service delivery).
**Availability Classification:** Available (manual download) + Available (free API) for World Bank

#### Measures

| Measure | Source | Series/Endpoint | Frequency | Coverage | Proxy Tier | API Key? |
|---------|--------|-----------------|-----------|----------|------------|----------|
| Government Effectiveness (WGI) | World Bank Worldwide Governance Indicators | `wb_indicator` MCP: GE.EST | Annual | 1996-present | Direct (administrative capacity) | No |
| Regulatory Quality (WGI) | World Bank Worldwide Governance Indicators | `wb_indicator` MCP: RQ.EST | Annual | 1996-present | Direct (regulatory capacity) | No |
| Rule of Law (WGI) | World Bank Worldwide Governance Indicators | `wb_indicator` MCP: RL.EST | Annual | 1996-present | Direct (legal institutional quality) | No |
| Control of Corruption (WGI) | World Bank Worldwide Governance Indicators | `wb_indicator` MCP: CC.EST | Annual | 1996-present | Direct (corruption control) | No |
| V-Dem Government Effectiveness components | V-Dem v15 | v2clrspct (rigorous/impartial public admin) | Annual | 1789-present | Direct | No |
| Hanson & Sigman (2021) latent state capacity | Academic dataset | Harvard Dataverse | Varies | Coverage varies by dimension | Direct (multi-dimensional) | No |

**Recommended:** World Bank WGI Government Effectiveness (GE.EST) as the primary measure, accessible via MCP `wb_indicator` tool. The WGI provides standardized scores across 6 governance dimensions, with the US scored on each annually since 1996. Government Effectiveness specifically captures "perceptions of the quality of public services, the quality of the civil service and the degree of its independence from political pressures." Supplement with V-Dem v2clrspct for longer historical coverage and the Hanson & Sigman (2021) dataset for the multi-dimensional state capacity perspective.

**Scale and Interpretation:**
- WGI indicators: Continuous score approximately -2.5 to +2.5 (standard normal distribution centered on global mean of 0). Higher = better governance. US typically scores 1.3-1.7 on Government Effectiveness.
- WGI also provides percentile rank (0-100) for easier interpretation.
- V-Dem v2clrspct: Ordinal expert rating, aggregated to interval. Higher = more rigorous/impartial administration.
- Hanson & Sigman: Latent factor scores (extractive, coercive, administrative) on standardized scales.

**Rate Limits:** World Bank MCP tool: standard MCP limits. V-Dem: CSV download. Hanson & Sigman: academic dataverse download.
**License:** World Bank WGI: CC BY 4.0. V-Dem: CC BY 4.0. Hanson & Sigman: academic open data.
**Known Gaps:**
- WGI starts only in 1996 -- limits backtesting. Data published biennially until 2002, then annually.
- WGI is based on perceptions aggregated from multiple sources (surveys, expert assessments, think tank reports) -- it measures perceived rather than objective capacity
- US state capacity has been near the top of global rankings throughout the WGI period, making within-country variation subtle
- Hanson & Sigman (2021) dataset may not extend to the most recent years -- check for updates
- The multidimensional nature of state capacity (extractive, coercive, administrative) means a single index may mask important divergences between dimensions
- V-Dem's v2clrspct is one of many possible V-Dem indicators for state capacity; others include v2cltort (torture), v2clkill (political killings), v2clsocgrp (social group equality in civil liberties)

**Last Verified:** 2026-03-03 (World Bank WGI confirmed available via MCP `wb_indicator`; V-Dem v15 confirmed; Hanson & Sigman dataset confirmed via web research)

---

## Domain Summary: Institutional / Democratic Quality

### Coverage Assessment

| Variable | # | Rating | Availability | Primary Source | Coverage Start |
|----------|---|--------|-------------|----------------|----------------|
| Regime Type / Institutional Quality | 13 | Strong* | Available (manual download) | V-Dem v2x_libdem | 1789 |
| Judicial Independence | 21 | Moderate | Available (manual download) | V-Dem v2x_jucon | 1789 |
| Freedom of Expression / Media Independence | 22 | Moderate | Available (manual download) | V-Dem v2x_freexp_altinf | 1789 |
| Legislative Constraints on Executive | 23 | Moderate | Available (manual download) | V-Dem v2xlg_legcon | 1789 |
| Electoral Integrity / Fraud Perception | 24 | Moderate | Available (manual download) | V-Dem v2xel_frefair | 1789 |
| Voter Access Restrictions / Gerrymandering | 29 | Moderate | Available (manual download) | Grumbach SDI | 2000 |
| Executive Aggrandizement | 32 | Moderate | Available (manual download) | V-Dem v2exrescon | 1789 |
| State Capacity / Institutional Quality | 38 | Moderate | Available (manual download) + (free API) | World Bank WGI GE.EST | 1996 |

*Asterisk indicates Contested variables

### Key Statistics

- **Total variables:** 8
- **Available (manual download):** 7 (88%) -- primarily V-Dem CSV download
- **Available (free API):** 1 (13%) -- #38 State Capacity via World Bank MCP tool
- **Partially available (proxy needed):** 0
- **Unavailable:** 0
- **Strong-rated:** 1 (13%) -- #13 Regime Type
- **Moderate-rated:** 7 (88%) -- #21, #22, #23, #24, #29, #32, #38
- **Contested:** 1 -- #13 (Regime Type)
- **Short series (post-2000 start):** 2 -- #29 Voter Access (Grumbach SDI, 2000), #38 State Capacity (WGI, 1996)
- **Frequency mix:** Annual (8 of 8) -- all primary sources are annual
- **V-Dem dependency:** 6 of 8 variables have V-Dem as primary source -- high single-source dependency
- **MCP-verified components:** 1 -- World Bank WGI via `wb_indicator` MCP tool

### Critical Gaps

1. **V-Dem near-ceiling limitation:** All V-Dem indices for the US are near the maximum score throughout the dataset period. Absolute levels provide minimal discriminatory power for within-country analysis. Rate-of-change and sub-indicator decomposition are necessary to extract useful signal. Phase 4 should compute year-over-year changes and analyze sub-indicator trends rather than using raw index levels.

2. **Electoral fraud perception gap (#24):** V-Dem captures structural electoral integrity (high for US) but not public perception of fraud (which diverged sharply post-2020). No systematic time series of fraud perception exists. Survey data from Pew, Gallup, and YouGov captures this post-2020 but is not compiled into a standardized series. Phase 4 may need to construct a perception-integrity gap variable.

3. **State-level aggregation (#29):** Grumbach SDI and related voter access measures are state-level. National aggregation requires methodological choices (population weighting, dispersion measures) that are Phase 4 decisions. Published range (2000-2018) may need extension.

4. **Single-source dependency:** 6 of 8 variables rely on V-Dem as the primary source. If V-Dem coding methodology changes or the dataset is not updated, this domain is disproportionately affected. Non-V-Dem alternatives are documented but are generally shorter in coverage and less comprehensive.

### Data Sources Used

| Source | Variables Served | API Key Required |
|--------|-----------------|-----------------|
| V-Dem v15 (v-dem.net) | #13, #21, #22, #23, #24, #32 (CSV download) | No |
| Freedom House (freedomhouse.org) | #13, #22 (report/data download) | No |
| Reporters Without Borders (rsf.org) | #22 (annual index download) | No |
| Electoral Integrity Project (Harvard Dataverse) | #24 (per-election data) | No |
| Grumbach State Democracy Index (Harvard Dataverse) | #24, #29 (state-level CSV) | No |
| Cost of Voting Index (Harvard Dataverse) | #29 (per-election data) | No |
| Brennan Center for Justice | #29 (published reports) | No |
| Bright Line Watch (brightlinewatch.org) | #32 (survey data download) | No |
| World Bank WGI (via MCP `wb_indicator`) | #38 (API access) | No |
| Hanson & Sigman 2021 (Harvard Dataverse) | #38 (academic dataset) | No |
