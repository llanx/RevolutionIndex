# Phase 3: Data Sourcing - Research

**Researched:** 2026-03-03
**Domain:** Data sourcing for political instability composite indicator variables
**Confidence:** HIGH

## Summary

Phase 3 must map 45 concept-level variables from Phase 2's ranked catalog to concrete, freely available data sources and produce a developer-ready inventory. Research confirms this is highly feasible: the US Gov Open Data MCP provides direct access to 37 federal APIs covering the economic domain almost entirely, while a small set of well-maintained free academic datasets (V-Dem, VoteView, WID, ACLED, ANES) covers the political/institutional and social domains. The phase does NOT write code or build pipelines -- it produces a structured markdown inventory document organized by theoretical domain.

The research verified specific FRED series IDs, discovered new series (e.g., Federal Reserve DFA wealth shares on FRED, SLUEM1524ZSUSA for youth unemployment), confirmed the CSCICP03USM665S discontinuation with no direct OECD KSTEI replacement on FRED, and mapped MCP tool names to variable needs. The primary risk is survey-dependent variables (trust, affective polarization, democratic commitment) where data is periodic rather than continuous and often not available via API.

**Primary recommendation:** Work through the 45 variables systematically by domain (economic first, then political/institutional, then social/mobilization, then information/media), using MCP tools for discovery/verification of federal sources, then documenting non-MCP sources from known academic providers. Produce one markdown document organized by theoretical domain with standardized metadata per variable.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **Primary sources:** US Government Open Data MCP's 37 federal APIs (FRED, BLS, BEA, Census, Treasury, CDC, etc.) -- search these first for every variable
- **Secondary sources:** Free APIs or free downloads outside the MCP (e.g., WID.world, V-Dem, Freedom House, SIPRI) -- used when MCP APIs don't cover a variable
- **Access requirements:** Free API with registration OK; free CSV/Excel downloads OK; no paid subscriptions
- **No hard cap** on number of non-MCP sources -- cover all strong/moderate-evidence variables regardless of source count
- **Two tiers only:** Direct measure and strong proxy (literature-validated mapping). No weak/speculative proxies.
- **Strong proxy requirement:** Literature must explicitly support the variable-to-concept mapping (e.g., DW-NOMINATE scores validated as polarization measure)
- **Multiple proxies per variable:** Catalog all viable direct/strong-proxy measures per theoretical variable. Mark a recommended proxy but include alternatives. Final selection deferred to Phase 4.
- **Unmeasurable variables:** When a strong-evidence variable has no direct measure or strong proxy, document the gap, rank by theoretical importance, and flag for future work. Do not invent creative proxies.
- **Flexible start dates:** Accept whatever historical coverage each source provides. No minimum start year requirement.
- **Full metadata per source:** Document exact coverage window (start year, end year or "present"), update frequency, and any known gaps
- **Short series included:** Variables with data starting after 2000 are included if they measure strong-evidence concepts. Tag as "short series" so Phase 5 can run separate validation.
- **Frequency alignment:** Document native frequency only. Alignment decisions deferred to Phase 4.
- **Primary deliverable:** Structured markdown document -- serves as both methodology reference and Phase 4 input
- **Machine-readable config** derived from markdown in Phase 4, not produced in Phase 3
- **Organization:** By theoretical domain (economic stress, political polarization, social cohesion, etc.) -- matches Phase 2's literature review structure
- **Metadata per variable:** Variable name, theoretical concept mapped to, source name, API endpoint/download URL, series ID, native frequency, coverage window (start-end), proxy tier (direct/strong), known data gaps, API key required (y/n), rate limits, data license/terms, last verified date

### Claude's Discretion
- **Proxy approach:** User opted for two tiers only (direct + strong proxy), excluding weak proxies for rigor.
- **Gap handling:** Document and flag unmeasurable gaps rather than searching for creative alternatives.
- **Multiple proxies:** Catalog multiple proxies per variable with a recommended pick. Final selection in Phase 4.
- **Short series:** Include post-2000 series with tagging and split validation.
- **Access notes:** Include API key/rate limit/license metadata.
- **Organization:** Group by theoretical domain over data source.

### Deferred Ideas (OUT OF SCOPE)
None -- discussion stayed within phase scope.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| DATA-01 | For each variable in the catalog, determine if a freely available, regularly-updated online data source exists | MCP provides 37 federal APIs with search/info tools; 18/45 variables already tagged `fed-data`; V-Dem, VoteView, WID, ACLED cover most `other-data` variables; 6 `unknown` variables need investigation |
| DATA-02 | For viable data sources, document API endpoints, series IDs, update frequency, historical coverage, and access method | FRED MCP tools (`fred_series_info`, `fred_search`) return exact metadata; BLS/BEA/Census/Treasury MCP tools provide endpoint details; non-MCP sources documented via web research |
| DATA-03 | Classify each variable as: available (free API), available (manual download), partially available (proxy needed), or unavailable | Classification framework aligns with existing `fed-data`/`other-data`/`unknown` tags; MCP verification refines preliminary tags to precise availability status |
| DATA-04 | Produce a final data source inventory mapping viable variables to specific data endpoints | Structured markdown format defined in CONTEXT.md; organization by theoretical domain; standardized metadata template researched |
| DATA-05 | Identify fallback/proxy variables for critical inputs that lack ideal data sources | Multiple proxies per variable cataloged in Phase 2; CSCICP03USM665S replacement options identified; Georgescu education-job mismatch proxy constructibility assessed |
</phase_requirements>

## Standard Stack

### Core Tools (MCP-Based)

| Tool | Purpose | Key For |
|------|---------|---------|
| `fred_search` | Discover FRED series by keyword | Finding series IDs for economic variables |
| `fred_series_info` | Get metadata: title, units, frequency, date range, notes | Verifying series status, coverage window, frequency |
| `bls_search_series` | Look up BLS series by topic (employment, wages, cpi, jolts, productivity) | Labor market and price variables |
| `bls_series_data` | Fetch BLS time series observations | Verifying data availability and date range |
| `bls_cpi_breakdown` | CPI components (food, energy, shelter, etc.) | Cost of living pressure variable |
| `census_search_variables` | Search Census ACS variables by keyword | Education, income, demographics |
| `census_query` | Query Census API with specific variables and geography | Gini, education attainment, poverty |
| `query_fiscal_data` | Query Treasury Fiscal Data API (53 datasets, 181 endpoints) | Debt, interest expense, revenue |
| `search_datasets` | Search Treasury datasets by keyword | Finding fiscal endpoints |
| `bea_gdp_national` | GDP data from BEA | GDP growth rate variable |
| `bea_personal_income` | Personal income data | Income distribution |
| `hud_fair_market_rents` | HUD Fair Market Rents by area | Housing affordability context |
| `wb_indicator` | World Bank development indicators | Life expectancy, youth unemployment, Gini |
| `cdc_life_expectancy` | CDC life expectancy data | Health domain (PLI) |
| `fec_search_candidates` | FEC candidate search | Anti-system party vote share |
| `congress_house_votes` / `congress_senate_votes` | Congressional voting records | Bipartisan voting frequency |

### Supporting Tools (Non-MCP)

| Source | Access Method | Purpose | When to Use |
|--------|--------------|---------|-------------|
| V-Dem v15 | CSV download from v-dem.net | Democratic quality indices (483 indicators, US 1789-present) | Political/institutional variables |
| VoteView | CSV download from voteview.com/data | DW-NOMINATE scores, party polarization (1789-present) | Congressional polarization, elite factionalism |
| WID.world | R package or bulk CSV download from wid.world/data/ | Top income/wealth shares (US, annual) | Income inequality, wealth concentration |
| ACLED | API with free registration from acleddata.com | US protest events (2020-present, 30K+ events) | Protest frequency variable |
| ANES | CSV download from electionstudies.org | Partisan feeling thermometer, trust, attitudes (1948-present) | Affective polarization, democratic commitment |
| Pew Research Center | Published reports with data tables | Trust in government (1958-present) | Government trust variable |
| Gallup | Published reports with historical trends | Institutional confidence (1973-present) | Government trust, institutional confidence |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| WID.world API | Fed Reserve DFA (WFRBST01134 on FRED) | DFA is quarterly wealth share from 1989, covers top 1% net worth but not income; WID covers income shares back further |
| SLUEM1524ZSUSA (World Bank/FRED) for youth unemployment | BLS LNS series (LNS14000012 etc.) | BLS has monthly US data; World Bank is annual ILO estimate from 1991 |
| Pew/Gallup for government trust | ANES trust-in-government series | ANES is biennial/quadrennial; Pew/Gallup more frequent but not API-accessible |
| CSCICP03USM665S (discontinued) for consumer confidence | UMCSENT (already in PLI) or Conference Board (paid) | UMCSENT creates data overlap with PLI; Conference Board not on FRED. Drop weight and redistribute is cleanest option. |

## Architecture Patterns

### Recommended Inventory Document Structure

```
data-source-inventory.md
├── Methodology (proxy tiers, metadata schema, verification approach)
├── Domain 1: Economic Stress Variables
│   ├── Variable 1.1: Income/Wealth Inequality
│   │   ├── Theoretical concept
│   │   ├── Direct measures (with full metadata each)
│   │   ├── Strong proxies (with full metadata each)
│   │   ├── Recommended measure + rationale
│   │   └── Data gaps / limitations
│   ├── Variable 1.2: Real Wage Growth / Labor Share
│   │   └── ...
│   └── [Domain summary: coverage, frequency mix, key gaps]
├── Domain 2: Political Polarization & Elite Dynamics
│   └── ...
├── Domain 3: Institutional / Democratic Quality
│   └── ...
├── Domain 4: Social Mobilization & Trust
│   └── ...
├── Domain 5: Information / Media Ecosystem
│   └── ...
├── Availability Summary Matrix (all 45 variables x availability classification)
├── Gap Analysis (unmeasurable variables ranked by importance)
└── Source Registry (all unique data sources with access details)
```

### Pattern 1: Variable Entry Template

Each variable in the inventory should follow this standardized template:

```markdown
### [Variable Name] (#[catalog number])

**Catalog Rating:** [Strong/Moderate/Weak] [Contested?]
**Theoretical Concept:** [What this measures in the theoretical framework]
**Availability Classification:** [Available (free API) / Available (manual download) / Partially available (proxy needed) / Unavailable]

#### Measures

| Measure | Source | Series/Endpoint | Frequency | Coverage | Proxy Tier | API Key? |
|---------|--------|-----------------|-----------|----------|------------|----------|
| [name] | [source] | [ID] | [freq] | [start]-[end] | [direct/strong] | [y/n] |

**Recommended:** [Which measure and why]
**Rate Limits:** [If applicable]
**License:** [Terms of use]
**Known Gaps:** [Any discontinuities, methodology changes, or coverage holes]
**Last Verified:** [Date verified via MCP or web]
```

### Pattern 2: MCP Verification Workflow

For each variable with `fed-data` tag:
1. Use `fred_search` with relevant keywords to find candidate series
2. Use `fred_series_info` on each candidate to get exact metadata (date range, frequency, status)
3. Record series ID, observation_start, observation_end, frequency, last_updated
4. Check `last_updated` to confirm series is still active (not stale >12 months)
5. Note any methodology changes from the `notes` field

For Treasury data:
1. Use `search_datasets` to find relevant endpoints
2. Use `get_endpoint_fields` to understand available fields
3. Use `query_fiscal_data` with a test filter to verify data structure

### Anti-Patterns to Avoid
- **Assuming FRED series ID stability:** Series can be discontinued (CSCICP03USM665S) or superseded (STLFSI -> STLFSI2 -> STLFSI3 -> STLFSI4). Always verify current status.
- **Confusing "on FRED" with "from FRED":** Many FRED series are sourced from other agencies (BLS, BEA, World Bank, OECD). The original source matters for understanding methodology changes and lag structure.
- **Treating all FRED series as equivalent:** Some are daily (VIX), some annual with 2-year lag (life expectancy). Metadata matters.
- **Mixing up nominal and real series:** Always check units. MEHOINUSA672N is already deflated; CES0500000003 is nominal and must be deflated by CPIAUCSL.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| FRED series discovery | Manual FRED website browsing | `fred_search` MCP tool | Returns series metadata including status, date range, popularity |
| FRED series verification | Manual page checks | `fred_series_info` MCP tool | Returns structured metadata with observation_start/end, last_updated |
| BLS series lookup | Decoding BLS series ID format | `bls_search_series` MCP tool | Curated series by topic, no need to understand BLS ID encoding |
| Treasury fiscal endpoint discovery | Manual API docs browsing | `search_datasets` MCP tool | Searches across 53 datasets (181 endpoints) |
| Census variable discovery | Reading Census API docs | `census_search_variables` MCP tool | Keyword search across ACS variable catalog |
| Data availability determination | Guessing from Phase 2 tags | MCP verification + web checks | Phase 2 tags were preliminary; Phase 3 verifies empirically |

**Key insight:** The MCP tools make verification fast and reliable. A single `fred_series_info` call returns the exact same metadata a human would get from visiting the FRED website, but structured and machine-readable. The research phase should lean heavily on MCP tools rather than manual browsing.

## Common Pitfalls

### Pitfall 1: Discontinued Series Without Replacement
**What goes wrong:** A FRED series stops updating (like CSCICP03USM665S, last observation Jan 2024) but no replacement series appears under a new ID.
**Why it happens:** Source agencies restructure data programs (OECD MEI -> KSTEI transition). FRED mirrors the source; when the source stops, FRED stops.
**How to avoid:** For every series, check `observation_end` and `last_updated` from `fred_series_info`. If `last_updated` is >12 months ago and `observation_end` is not "present," investigate.
**Warning signs:** Series notes mentioning "DISCONTINUED," observation_end dates that stopped advancing, source program restructuring announcements.
**Verified example:** CSCICP03USM665S confirmed discontinued -- observation_end: 2024-01-01, last_updated: 2025-11-17. No OECD KSTEI replacement found on FRED.

### Pitfall 2: Methodology Breaks in Continuing Series
**What goes wrong:** A series continues publishing but the methodology changes mid-stream, creating a level shift that contaminates z-score normalization.
**Why it happens:** Source agencies update methodologies to improve accuracy, but historical data is not revised.
**How to avoid:** Read the `notes` field from `fred_series_info` carefully. Document known breaks. Flag for Phase 4 normalization treatment.
**Warning signs:** Notes mentioning "revised methodology," "updated sample," or "new calculation method."
**Verified example:** DRSFRMACBS (mortgage delinquency) -- 2023 MBA methodology revision affects level comparability.

### Pitfall 3: Survey Data Masquerading as Time Series
**What goes wrong:** Variables like "trust in government" or "affective polarization" appear to have long time series but are actually periodic survey snapshots with irregular spacing and changing methodologies.
**Why it happens:** Survey organizations (Pew, Gallup, ANES) don't run the same questions at fixed intervals. Question wording changes. Sampling methodology evolves.
**How to avoid:** Document native frequency honestly. Note survey-specific limitations. Do not interpolate between survey waves -- use LOCF as specified in project decisions.
**Warning signs:** Irregular data point spacing, question wording changes in documentation, switching between phone/online methodology.

### Pitfall 4: Data Overlap Between Models
**What goes wrong:** Using the same series in multiple models (e.g., UMCSENT in both PLI and FSP) violates the zero-overlap design principle, inflating apparent model agreement.
**Why it happens:** When replacing discontinued series, the closest substitute may already be used elsewhere.
**How to avoid:** Maintain a cross-reference of which series maps to which model. Before adding a replacement, check if it's already assigned. The project explicitly chose zero-overlap (Critical Review C1).
**Warning signs:** Same FRED series ID appearing under multiple models in config.py.

### Pitfall 5: Confusing Coverage Window with Update Frequency
**What goes wrong:** A series covers 1947-present (long history) but updates annually with a 2-year lag, meaning the "present" is actually 2023-2024.
**Why it happens:** Annual series from Census, World Bank, or BEA have structural publication lags. "Present" means "most recent available," not "today."
**How to avoid:** Record both the coverage window AND the effective latency. `observation_end` from `fred_series_info` shows the latest data point, not today's date.
**Warning signs:** Annual frequency + observation_end 1-2 years behind current date = expected lag, not a problem. But observation_end >3 years behind = investigate.

### Pitfall 6: MCP Tool Errors and Fallbacks
**What goes wrong:** MCP tools occasionally return errors (Census API returned invalid JSON during research), requiring fallback verification methods.
**Why it happens:** Upstream government APIs have intermittent availability issues, rate limits, or format changes.
**How to avoid:** When an MCP tool fails, try again or use WebFetch against the official API documentation page. Document the fallback method used.
**Warning signs:** JSON parse errors, timeout errors, empty result sets for queries that should return data.

## Verified Data Source Findings

### FRED Series -- Verified Active via MCP

The following series were verified active (observation data current through 2025-2026) via `fred_series_info`:

| Series ID | Title | Frequency | Coverage | Status |
|-----------|-------|-----------|----------|--------|
| STLFSI4 | St. Louis Fed Financial Stress Index | Weekly | 1993-present | ACTIVE (Feb 2026) |
| UMCSENT | U. Michigan Consumer Sentiment | Monthly | 1952-present | ACTIVE (Jan 2026) |
| NFCI | Chicago Fed National Financial Conditions Index | Weekly | 1971-present | ACTIVE (Feb 2026) |
| HDTGPDUSQ163N | Household Debt to GDP (US) | Quarterly | 2005-present | ACTIVE (Apr 2025) |
| SIPOVGINIUSA | GINI Index (US) | Annual | 1963-present | ACTIVE (2023 obs) |
| SLUEM1524ZSUSA | Youth Unemployment Rate (US, 15-24) | Annual | 1991-present | ACTIVE (2025 obs) |
| WFRBST01134 | Share of Net Worth Held by Top 1% | Quarterly | 1989-present | ACTIVE (Jul 2025) |
| WFRBSTP1300 | Share of Net Worth Held by Top 0.1% | Quarterly | 1989-present | ACTIVE (Jul 2025) |

### FRED Series -- Confirmed Discontinued

| Series ID | Title | Last Observation | Replacement |
|-----------|-------|------------------|-------------|
| CSCICP03USM665S | OECD Consumer Confidence (Amplitude Adjusted) | Jan 2024 | No direct FRED replacement found. Options: drop weight, use UMCSENT (creates overlap), or Conference Board (not free on FRED) |

### Key Non-MCP Sources -- Verified via Web Research

| Source | Current Version | Access | Format | US Coverage | Update Frequency | Cost |
|--------|----------------|--------|--------|-------------|------------------|------|
| V-Dem | v15 (March 2025) | CSV/Stata download from v-dem.net | CSV, Stata, R, SPSS | Full US coding, 1789-present | Annual (March) | Free |
| VoteView | Continuously updated | CSV download from voteview.com/data | CSV, JSON | 1st-119th Congress (1789-2027) | Weekly database dumps | Free |
| WID.world | Current | R package (`wid-r-tool`) or bulk CSV from wid.world/data | CSV, R | US income/wealth shares, annual | Varies by country/variable | Free |
| ACLED | Current | API with free registration (acleddata.com) | CSV, API (JSON) | US events since 2020 (30K+) | Real-time (weekly updates) | Free (registration required) |
| ANES | Cumulative file + individual studies | CSV download from electionstudies.org | CSV, Stata, SPSS | US only, 1948-present | Biennial/quadrennial | Free |
| BLS Union Membership | 2025 release (Feb 2026) | Annual news release PDF/tables from bls.gov | PDF tables, extractable | National + state, 1983-present | Annual (January) | Free |
| Pew Trust Survey | 2025 update (Dec 2025) | Published reports with data tables | Report/chart data | Trust in government, 1958-present | Irregular (roughly annual) | Free |

### Treasury Fiscal Data -- Verified Endpoints via MCP

| Endpoint | Description | Key Fields | Relevance |
|----------|-------------|------------|-----------|
| `/v2/accounting/od/interest_expense` | Monthly interest expense on public debt | record_date, expense_amt | Debt servicing burden (SFD proxy) |
| `/v2/accounting/od/debt_to_penny` | Total public debt outstanding (daily) | record_date, tot_pub_debt_out_amt | State fiscal distress |
| `/v1/accounting/mts/mts_table_1` | Monthly Treasury Statement: receipts, outlays, deficit | record_date, receipts, outlays | Deficit/surplus tracking |
| `/v2/accounting/od/avg_interest_rates` | Average interest rates on Treasury securities | record_date, avg_interest_rate | Cost of debt service |

### BLS Series -- Verified via MCP

| Topic | Series Available | Relevant To |
|-------|-----------------|-------------|
| JOLTS | JTS000000000000000JOR (openings), JTS000000000000000HIR (hires), JTS000000000000000QUR (quits), JTS000000000000000LDR (layoffs) | Elite overproduction (education-job mismatch ratio), labor market tightness |
| Employment by industry | 13 CES series across all major sectors | Structural employment shifts |
| CPI breakdown | Food, shelter, energy, medical, transportation components | Cost of living pressure composite |

### Variable-to-Source Mapping Summary

**By availability (preliminary, to be finalized in execution):**

| Classification | Count | Examples |
|---------------|-------|---------|
| Available (free API via MCP) | ~20 | All FRED series, BLS, BEA, Census, Treasury |
| Available (free API, non-MCP) | ~3 | ACLED (API), World Bank via MCP |
| Available (manual download) | ~12 | V-Dem, VoteView, WID, ANES, BLS union tables |
| Partially available (proxy needed) | ~6 | Elite overproduction (constructible), affective polarization (periodic surveys) |
| Unavailable | ~4 | Misinformation prevalence, social media engagement, echo chambers, cross-class coalition |

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Manual FRED website browsing for series | MCP `fred_search` + `fred_series_info` | Project adoption of MCP | Verification in seconds vs. minutes per series |
| OECD MEI consumer confidence (CSCICP03USM665S) | OECD KSTEI framework (no FRED replacement found) | 2024 OECD restructuring | Need alternative consumer confidence source |
| STLFSI2/3 for financial stress | STLFSI4 (uses forward-looking SOFR) | Nov 2022 | Already using correct version in config.py |
| Polity IV/V for regime type | V-Dem v15 (March 2025) | V-Dem replaced Polity as standard | V-Dem has 483 indicators vs Polity's single composite |
| BLS LUU series for union data | Annual BLS news release (union2.htm) | Ongoing | No API series; requires table extraction from annual release |
| Fed Survey of Consumer Finances (triennial) for wealth | Fed DFA on FRED (quarterly, 1989-present) | DFA launched ~2019 | Much higher frequency for wealth concentration tracking |

**Deprecated/outdated:**
- STLFSI, STLFSI2, STLFSI3: All superseded by STLFSI4
- CSCICP03USM665S: OECD discontinued; no FRED replacement
- CSCICP02USM661S: Older OECD confidence series, discontinued 2013
- Polity5: Final version (2018), no longer updated; V-Dem is the current standard

## Open Questions

1. **WID.world API endpoint format**
   - What we know: The R package (`wid-r-tool`) provides programmatic access. Two inconsistent URLs exist in the codebase. Bulk CSV download is available as fallback.
   - What's unclear: Whether a Python-accessible REST API exists with stable endpoints, or if R package/CSV download are the only viable methods.
   - Recommendation: Test both codebase URLs during Phase 3 execution. If neither works, use bulk CSV download and document as manual-download source. The R package could be invoked from Python via subprocess if needed.

2. **Conference Board Consumer Confidence as CSCICP03USM665S replacement**
   - What we know: Conference Board CCI is the most commonly used alternative to UMCSENT. It is NOT on FRED. It requires either paid subscription or manual extraction from press releases.
   - What's unclear: Whether free academic access exists, or whether recent data can be scraped from published press releases.
   - Recommendation: The cleanest solution for Phase 4 is to drop the CSCICP03USM665S weight from FSP ETI and redistribute to remaining inputs, rather than introducing a paid or fragile data source. This loses the consumer confidence signal in FSP but UMCSENT already captures it in PLI.

3. **Georgescu education-job mismatch proxy constructibility**
   - What we know: Census ACS has education attainment variables (B15003_022E bachelor's, B15003_023E master's, B15003_025E doctorate). BLS JOLTS has job openings by occupation. The ratio of advanced degree holders to professional positions could proxy elite overproduction.
   - What's unclear: Whether Census + JOLTS data at the occupational detail level needed can produce a meaningful annual time series. Frequency mismatch (Census annual, JOLTS monthly but aggregate) may limit precision.
   - Recommendation: Document as "constructible from Census + BLS" with a specific construction recipe. Flag as needing Phase 4 empirical validation. The existing top 1% income share from WID remains the fallback.

4. **BLS union membership as API-accessible time series**
   - What we know: BLS publishes union membership data annually (February, via news release union2.htm). The data is available as tables in PDF/HTML format, not as a FRED or BLS API series.
   - What's unclear: Whether BLS API series IDs exist for union membership rate (LUU prefix), or if data must be extracted from annual release tables.
   - Recommendation: Classify as "available (manual download)" with annual update frequency. The series is short (1983-present for the current CPS methodology) but adequate for the project's flexible date requirement.

5. **Pew/Gallup trust data granularity and API access**
   - What we know: Pew has published "Public Trust in Government: 1958-2025" (Dec 2025). Gallup tracks institutional confidence since 1973. Neither offers a free data API.
   - What's unclear: Exact data point spacing (roughly annual but irregular), whether historical data points can be extracted from published charts/tables in machine-readable form.
   - Recommendation: Classify as "available (manual download)" with irregular frequency. Compile a time series from published Pew/Gallup reports as a one-time data extraction task. Note that ANES trust questions provide a more standardized alternative but with lower frequency (biennial/quadrennial).

## Sources

### Primary (HIGH confidence)
- US Gov Open Data MCP -- tested `fred_search`, `fred_series_info`, `bls_search_series`, `search_datasets` tools directly; returned structured metadata confirming series status
- FRED API via MCP -- verified specific series (STLFSI4, UMCSENT, NFCI, HDTGPDUSQ163N, SIPOVGINIUSA, SLUEM1524ZSUSA, WFRBST01134, WFRBSTP1300, CSCICP03USM665S)
- US Gov Open Data MCP reference document (`govdata://reference`) -- complete listing of 37 APIs with endpoints, key requirements, and documentation links
- V-Dem website (v-dem.net) -- confirmed v15, March 2025, CSV download, free
- VoteView website (voteview.com/data) -- confirmed CSV downloads, 1st-119th Congress, weekly DB dumps

### Secondary (MEDIUM confidence)
- WID.world -- confirmed R package access and bulk download; API specifics less clear
- ACLED -- confirmed free registration, API access, US coverage since 2020; registration process status verified via web search
- ANES -- confirmed free CSV downloads from electionstudies.org; API access not found
- BLS union membership -- confirmed annual release (Feb 2026 for 2025 data); API series access unclear
- Pew Research Center -- confirmed trust time series publication (Dec 2025); data download method unclear

### Tertiary (LOW confidence)
- Conference Board CCI FRED availability -- searched but not found on FRED; likely requires paid access
- Census API variable search -- MCP tool returned JSON parse error during testing; Census API appears intermittently available

## Metadata

**Confidence breakdown:**
- Standard stack (MCP tools for federal data): HIGH -- tools tested and working, metadata verified
- Non-MCP academic sources (V-Dem, VoteView, ANES): HIGH -- well-established free academic datasets
- WID API specifics: MEDIUM -- R package confirmed, REST API unclear
- Survey data sources (Pew, Gallup): MEDIUM -- data exists but access method needs per-source investigation
- Constructed proxies (education-job mismatch): LOW -- theoretically sound but requires empirical construction validation

**Research date:** 2026-03-03
**Valid until:** 2026-04-03 (30 days -- stable sources, unlikely to change)
