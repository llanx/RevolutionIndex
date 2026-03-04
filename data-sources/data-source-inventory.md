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
