# Variable Catalog: Revolution and Political Instability Predictors

## Methodology

This catalog synthesizes variables discovered across 6 domain literature reviews into a unified, ranked reference for downstream phases. Variables are cataloged at the **concept level** -- "income inequality" is one entry with multiple proxy measurements, not separate entries for Gini, top 1% share, and labor share.

### Rating System (Locked Decision from 02-CONTEXT.md)

- **Strong**: Statistically significant coefficients in 2+ independent quantitative studies
- **Moderate**: Appears in 1 quantitative model OR strong qualitative consensus across 3+ studies
- **Weak**: Theoretically motivated but limited testing, or single qualitative mention
- **Contested** marker: Added where evidence conflicts exist between studies

### Measurability Filter

Only variables with at least one known measurement approach or proxy are included. Theoretically important but unmeasurable variables (e.g., "revolutionary consciousness," "elite legitimacy beliefs") are excluded entirely.

### Data Availability Tags

- `fed-data`: Known federal API source (FRED, BLS, BEA, Census, Treasury, etc.)
- `other-data`: Known non-federal source (WID, V-Dem, Pew, ACLED, etc.)
- `unknown`: No source identified yet

### Deduplication Rules

Variables appearing under different names across domains are unified into a single concept-level entry. For example:
- "Relative deprivation" (Domain 1), "perceived loss" (Domain 4), "J-curve gap" (Domain 3) -> unified as **Relative Deprivation / Expectation-Reality Gap**
- "Elite factionalism" (Domain 1), "factionalized elites" (Domain 2), "elite fragmentation" (Domain 3) -> unified as **Elite Factionalism / Fragmentation**
- "Government trust" (Domain 1), "state legitimacy" (Domain 2, 3), "institutional trust" (Domain 4, 6) -> unified as **Government Trust / State Legitimacy**

---

## Summary Table

| # | Variable | Domain(s) | Rating | Contested? | Data Availability | Key Studies |
|---|----------|-----------|--------|------------|-------------------|-------------|
| 1 | Income / Wealth Inequality | 1, 2, 3, 4 | Strong | Yes | fed-data | Muller 1985; Alesina & Perotti 1996; Piketty 2014; Cederman et al. 2013 |
| 2 | Real Wage Growth / Labor Share | 1, 3, 4 | Strong | No | fed-data | Turchin 2003; Goldstone 1991; Piketty 2014; Stiglitz 2012 |
| 3 | Political Polarization (Congressional) | 1, 2, 6 | Strong | No | other-data | McCarty et al. 2006; Mann & Ornstein 2012; Turchin 2023 |
| 4 | Affective Polarization | 2, 6 | Strong | No | other-data | Iyengar et al. 2012; McCoy & Somer 2019; Boxell et al. 2017 |
| 5 | State Fiscal Distress (Debt / Deficit) | 1, 3, 4 | Strong | Yes | fed-data | Turchin 2003; Goldstone 1991; Skocpol 1979; Brinton 1938 |
| 6 | Financial Crisis / Systemic Stress | 1, 3, 4 | Strong | No | fed-data | Funke et al. 2016; Reinhart & Rogoff 2009; Mian et al. 2014 |
| 7 | Government Trust / State Legitimacy | 1, 2, 3, 4, 6 | Strong | No | other-data | Norris 2011; Dalton 2004; Brinton 1938; Kurzman 2004 |
| 8 | Elite Overproduction | 1, 3 | Strong | No | fed-data (partial) | Turchin 2003; Goldstone 1991; Georgescu 2023 |
| 9 | Unemployment Rate | 1, 4, 5 | Strong | No | fed-data | Collier & Hoeffler 2004; Campante & Chor 2012; Fetzer 2019 |
| 10 | GDP Growth Rate | 1, 3, 4 | Strong | No | fed-data | Davies 1962; Collier & Hoeffler 2004; Acemoglu & Robinson 2006 |
| 11 | Elite Factionalism / Fragmentation | 1, 2, 3 | Strong | No | other-data | Goldstone 1991; Skocpol 1979; Walter 2022; Haggard & Kaufman 2021 |
| 12 | Protest Frequency and Participation | 1, 3, 5 | Strong | No | other-data | Chenoweth & Stephan 2011; Tarrow 1994; Clark & Regan 2016 |
| 13 | Regime Type / Institutional Quality | 1, 2, 3 | Strong | Yes | other-data | Goldstone et al. 2010; Walter 2022; V-Dem Institute 2023 |
| 14 | Relative Deprivation / Expectation-Reality Gap | 1, 3, 4 | Moderate | No | fed-data | Davies 1962; Gurr 1970; Turchin 2020 |
| 15 | Horizontal Inequality (Between-Group) | 1, 2, 4 | Moderate | No | fed-data | Cederman et al. 2013; Stewart 2008; Chetty et al. 2020 |
| 16 | Housing Affordability | 4 | Moderate | No | fed-data | Ansell 2014; Joint Center for Housing Studies 2024 |
| 17 | Inflation Rate | 3, 4 | Moderate | No | fed-data | Cavallo et al. 2017; Gatrell 2005 |
| 18 | Consumer Confidence / Sentiment | 4 | Moderate | No | fed-data | Davies 1962; Gurr 1970; Cavallo et al. 2017 |
| 19 | Intra-Elite Wealth Gap | 1, 4 | Moderate | No | other-data | Turchin 2023; Piketty & Saez 2003; Saez & Zucman 2016 |
| 20 | Middle-Class Income Share | 4 | Moderate | No | fed-data | Alesina & Perotti 1996; Stiglitz 2012 |
| 21 | Judicial Independence | 2 | Moderate | No | other-data | V-Dem Institute 2023; Ginsburg & Huq 2018; Levitsky & Ziblatt 2018 |
| 22 | Freedom of Expression / Media Independence | 2, 6 | Moderate | No | other-data | V-Dem Institute 2023; Bermeo 2016; Reporters Without Borders |
| 23 | Legislative Constraints on Executive | 2 | Moderate | No | other-data | V-Dem Institute 2023; Ginsburg & Huq 2018 |
| 24 | Electoral Integrity / Fraud Perception | 2, 3 | Moderate | No | other-data | Tucker 2007; Norris 2014; Walter 2022; Grumbach 2023 |
| 25 | Civil Society Density / Union Membership | 2, 3, 5 | Moderate | No | fed-data | McCarthy & Zald 1977; McAdam 1982; Putnam 2000 |
| 26 | Youth Unemployment / Disconnection | 3, 4 | Moderate | No | fed-data | Campante & Chor 2012; Urdal 2006; Goldstone 1991 |
| 27 | Household Debt / Leverage | 4 | Moderate | No | fed-data | Mian et al. 2014; Funke et al. 2016 |
| 28 | Media Trust / Partisan Media Trust Gap | 6 | Moderate | No | other-data | Gallup; Pew Research Center; Reuters Institute |
| 29 | Voter Access Restrictions / Partisan Gerrymandering | 2 | Moderate | No | other-data | Grumbach 2023; Stephanopoulos & McGhee 2015 |
| 30 | Democratic Commitment (Attitudinal) | 2 | Moderate | No | other-data | Mounk 2018; Foa & Mounk 2016; Norris 2011 |
| 31 | Anti-System Party Vote Share | 2, 4 | Moderate | No | fed-data | Mounk 2018; Funke et al. 2016; Norris & Inglehart 2019 |
| 32 | Executive Aggrandizement | 2 | Moderate | No | other-data | Bermeo 2016; Haggard & Kaufman 2021; Ginsburg & Huq 2018 |
| 33 | Misinformation Prevalence / Exposure | 6 | Weak | Yes | unknown | Vosoughi et al. 2018; Loomba et al. 2021 |
| 34 | Conspiratorial Thinking Prevalence | 6 | Weak | No | other-data | Uscinski & Parent 2014; PRRI surveys |
| 35 | Social Media Political Engagement | 5, 6 | Weak | Yes | unknown | Tufekci 2017; Gonzalez-Bailon et al. 2011 |
| 36 | Protest Diffusion / Contagion | 3, 5 | Weak | No | other-data | Beissinger 2002; Lynch 2012 |
| 37 | Prior Protest Experience | 5 | Weak | No | other-data | Klandermans 1997; Granovetter 1978 |
| 38 | State Capacity / Institutional Quality | 1, 2, 3 | Moderate | No | other-data | Fearon & Laitin 2003; Hanson & Sigman 2021 |
| 39 | Neighborhood / Diffusion Effects (Allied Democracies) | 1, 2 | Weak | No | other-data | Goldstone et al. 2010; Huntington 1991 |
| 40 | Cost of Living Pressure (Composite) | 3, 4 | Moderate | No | fed-data | Bellemare 2015; Lagi et al. 2011; Cavallo et al. 2017 |
| 41 | Institutional Legitimacy Denial | 6 | Weak | No | other-data | Bright Line Watch; post-2020 election surveys |
| 42 | Political Efficacy Beliefs | 5 | Weak | No | other-data | Klandermans 1997, 2004 |
| 43 | Information Fragmentation / Echo Chambers | 6 | Weak | Yes | unknown | Sunstein 2001; Bail et al. 2018 |
| 44 | Cross-Class Coalition Formation | 3, 5 | Weak | No | unknown | Wickham-Crowley 1992; Foran 2005 |
| 45 | Wealth Concentration (Top 0.1%) | 1, 4 | Strong | No | other-data | Saez & Zucman 2016; Piketty 2014 |

**Rating Distribution:** Strong: 13 (29%), Moderate: 20 (44%), Weak: 12 (27%)

**Contested Variables:** 4 of 45 (9%) -- Income Inequality, State Fiscal Distress, Regime Type, Misinformation, Social Media, Information Fragmentation

**Data Availability:** fed-data: 18 (40%), other-data: 21 (47%), unknown: 6 (13%)

---

## Detailed Entries

### 1. Income / Wealth Inequality

**Rating:** Strong -- Contested
**Domain(s):** Revolution Prediction, Democratic Backsliding, Historical Case Studies, Economic Preconditions
**Data Availability:** `fed-data`

**Definition:** The degree of unequal distribution of income and wealth across the population, measured at multiple levels (aggregate Gini, top-end concentration, wealth distribution).

**Evidence:**
| Study | Proxy Used | Finding | Type |
|-------|-----------|---------|------|
| Muller (1985) | Gini coefficient, land Gini | Higher inequality -> higher political violence cross-nationally | quant |
| Alesina & Perotti (1996) | Middle-class income share | Inequality destabilizes, especially when middle class shrinks | quant |
| Piketty (2014) | Top income/wealth shares | Long-run inequality dynamics create structural instability | quant |
| Cederman et al. (2013) | Horizontal inequality (between groups) | Group-based inequality more predictive than aggregate inequality | quant |
| Turchin (2003) | Top 1% income share as EMP proxy | Elite income concentration correlates with instability cycles | quant |
| Collier & Hoeffler (2004) | Gini | Inequality is NOT significant when growth/income level included | quant |

**Contested:** Collier & Hoeffler (2004) find that economic growth rate matters more than static inequality level. Cederman et al. (2013) argue that aggregate Gini misses the politically relevant dimension -- inequality *between groups*. The debate suggests that **dynamic inequality** (rate of change) and **horizontal inequality** (between identity groups) may be more predictive than static aggregate inequality.

**Measurement Approaches:**
- Gini coefficient: Census ACS (fed-data), annual
- Top 1% pre-tax income share: WID sptinc992j (other-data)
- Top 10% income share: WID (other-data)
- Wealth Gini: Federal Reserve DFA (fed-data), quarterly
- Income shares by quintile: Census (fed-data), annual
- Racial income gap: Census/BLS (fed-data)

**Theoretical Role:** Central variable in structural-demographic theory (Turchin), relative deprivation theory (Gurr), and grievance-based conflict models (Cederman). Inequality creates conditions for mass mobilization by generating perceived unfairness, reducing system legitimacy, and fueling populist resentment. In the US context, the rate of inequality change may be more predictive than the level.

---

### 2. Real Wage Growth / Labor Share

**Rating:** Strong
**Domain(s):** Revolution Prediction, Historical Case Studies, Economic Preconditions
**Data Availability:** `fed-data`

**Definition:** The trajectory of real wages for median/typical workers and the share of national income accruing to labor rather than capital. Measures whether ordinary workers are materially better or worse off over time.

**Evidence:**
| Study | Proxy Used | Finding | Type |
|-------|-----------|---------|------|
| Turchin (2003, 2023) | Labor share of GDP (W270RE1A156NBEA) | Declining labor share = mass mobilization potential (MMP) | quant |
| Goldstone (1991) | Real wage indices | Wage stagnation preceded all four early modern revolutions | qual |
| Piketty (2014) | Real wage growth vs. GDP growth | Wage-productivity gap indicates increasing capital share | quant |
| Stiglitz (2012) | Median real earnings | Stagnant wages amid rising productivity signal distributional failure | qual |

**Measurement Approaches:**
- Labor share of GDP: FRED W270RE1A156NBEA (fed-data), quarterly
- Nonfarm business labor share: FRED PRS85006173 (fed-data), quarterly
- Real median hourly earnings: BLS/FRED (fed-data), monthly
- Real median household income: Census/FRED (fed-data), annual
- Wage growth relative to GDP growth: Derived from FRED (fed-data)

**Theoretical Role:** Core Mass Mobilization Potential (MMP) variable in Turchin's structural-demographic theory. When real wages stagnate while the economy grows, the gap between elite prosperity and mass experience widens, creating the frustration that drives political mobilization. US labor share declined from ~65% (1960s) to ~57% (2014) before partial recovery.

---

### 3. Political Polarization (Congressional / Elite)

**Rating:** Strong
**Domain(s):** Revolution Prediction, Democratic Backsliding, Media/Information Ecosystem
**Data Availability:** `other-data`

**Definition:** The degree of ideological separation between political parties as measured by legislative voting behavior. Captures elite-level political division.

**Evidence:**
| Study | Proxy Used | Finding | Type |
|-------|-----------|---------|------|
| McCarty, Poole & Rosenthal (2006, 2016) | DW-NOMINATE party distance | US Congressional polarization at highest levels since Reconstruction | quant |
| Mann & Ornstein (2012) | Congressional bipartisanship measures | Polarization is asymmetric -- Republican rightward shift larger | quant |
| Turchin (2023) | Political polarization composite | Polarization is a key indicator of structural-demographic stress | qual |
| Haggard & Kaufman (2021) | Legislative polarization | Polarization preceded backsliding in all 16 cases studied | qual |

**Measurement Approaches:**
- DW-NOMINATE party distance scores: VoteView (other-data), annual, 1789-present
- Party ideological overlap: VoteView (other-data)
- Bipartisan voting frequency: Congressional Record (other-data)

**Theoretical Role:** Elite polarization signals the breakdown of cross-party cooperation that democratic governance requires. When elites cannot cooperate across party lines, governance capacity deteriorates, institutional norms erode, and each side views the other as an existential threat. DW-NOMINATE is one of the best-measured political variables in existence -- continuous objective data from the 1st Congress (1789) to present.

---

### 4. Affective Polarization

**Rating:** Strong
**Domain(s):** Democratic Backsliding, Media/Information Ecosystem
**Data Availability:** `other-data`

**Definition:** Growing mutual dislike and distrust between partisan groups that extends beyond policy disagreements into personal hostility. Distinct from ideological polarization -- measures how much partisans *dislike each other*, not how much they *disagree on policy*.

**Evidence:**
| Study | Proxy Used | Finding | Type |
|-------|-----------|---------|------|
| Iyengar, Sood & Lelkes (2012) | Partisan feeling thermometer gap (ANES) | Affective polarization doubled since 1980 | quant |
| Iyengar & Westwood (2015) | Implicit association tests | Partisan bias exceeds racial bias | quant |
| McCoy & Somer (2019) | Comparative polarization indices | Pernicious polarization is the strongest predictor of democratic backsliding across 16 cases | qual |
| Boxell, Gentzkow & Shapiro (2017, 2022) | Cross-country affective polarization | US increase is an outlier among peer democracies | quant |
| Haggard & Kaufman (2021) | Polarization measures across 16 cases | Extreme polarization preceded and enabled backsliding in all cases | qual |

**Measurement Approaches:**
- Partisan feeling thermometer gap: ANES (other-data), biennial/quadrennial, since 1968
- Pew partisan antipathy scales: Pew Research Center (other-data), periodic
- Social distance between partisans: Survey-based (other-data)

**Theoretical Role:** Affective polarization is the mechanism that converts policy disagreements into existential inter-group conflict. When partisan identity subsumes all other identities and political opponents are perceived as threats to group survival, citizens tolerate norm violations by their own side. McCoy & Somer (2019) identify pernicious polarization as the single most important precondition for democratic backsliding. The literature distinguishes this from healthy ideological polarization, which is a normal feature of democracy.

---

### 5. State Fiscal Distress (Debt / Deficit)

**Rating:** Strong -- Contested
**Domain(s):** Revolution Prediction, Historical Case Studies, Economic Preconditions
**Data Availability:** `fed-data`

**Definition:** The financial health of the national government, measured through debt levels, deficit spending, and debt servicing burden. A signal of the state's capacity to manage crises and deliver public goods.

**Evidence:**
| Study | Proxy Used | Finding | Type |
|-------|-----------|---------|------|
| Turchin (2003) | Government debt-to-GDP (GFDEGDQ188S) | State Fiscal Distress (SFD) is one of three PSI components | quant |
| Goldstone (1991) | State fiscal distress indicators | Fiscal crisis preceded all four early modern revolutions | qual |
| Skocpol (1979) | Fiscal-military strain | State fiscal crisis is a necessary precondition for revolution | qual |
| Brinton (1938) | Government financial embarrassment | Fiscal distress common across all four revolution cases | qual |
| Reinhart & Rogoff (2009) | Debt/GDP thresholds | High debt associated with lower growth and fiscal fragility | quant |

**Contested:** Japan demonstrates that very high debt levels (250%+ of GDP) do not necessarily produce fiscal crisis when debt is domestically held and denominated in local currency. Debt *level* may matter less than debt *servicing cost* or debt *trajectory*. Turchin uses debt/GDP as a simple proxy, but the relationship between debt and state capacity is more nuanced.

**Measurement Approaches:**
- Federal debt held by public as % of GDP: FRED GFDEGDQ188S (fed-data), quarterly
- Federal deficit as % of GDP: FRED/Treasury (fed-data), monthly
- Interest payments as % of revenue: Treasury Fiscal Data (fed-data)
- Primary budget balance: Treasury Fiscal Data (fed-data)

**Theoretical Role:** Core State Fiscal Distress (SFD) variable in Turchin's PSI. Structural theorists (Skocpol, Goldstone, Brinton) identify fiscal crisis as one of the most consistently recurring preconditions across revolutionary episodes. The mechanism: fiscal distress signals the state's inability to manage demands, fund public goods, and respond to crises -- creating an opening for challengers and reducing public confidence in government.

---

### 6. Financial Crisis / Systemic Stress

**Rating:** Strong
**Domain(s):** Revolution Prediction, Historical Case Studies, Economic Preconditions
**Data Availability:** `fed-data`

**Definition:** The occurrence and severity of systemic financial crises involving banking sector distress, credit market seizure, and broad economic disruption. Distinct from normal recessions -- specifically captures systemic/banking crises.

**Evidence:**
| Study | Proxy Used | Finding | Type |
|-------|-----------|---------|------|
| Funke, Schularick & Trebesch (2016) | Banking crisis indicator | Financial crises -> 30% increase in far-right vote share, 5-10 year lag | quant |
| Reinhart & Rogoff (2009) | Banking crisis chronology | Systemic crises produce deeper and longer recessions than normal downturns | quant |
| Mian, Sufi & Trebbi (2014) | Banking crisis + debt overhang | Financial crises increase political polarization and fractionalization | quant |
| De Bromhead, Eichengreen & O'Rourke (2013) | 1930s financial crisis | Interwar financial crisis -> rise of fascism and extremism | quant |

**Measurement Approaches:**
- St. Louis Fed Financial Stress Index: FRED STLFSI4 (fed-data), weekly
- Chicago Fed National Financial Conditions Index: FRED NFCI (fed-data), weekly
- Laeven & Valencia banking crisis indicator: Academic dataset (other-data)
- Credit spreads (BAA-AAA): FRED (fed-data), daily
- VIX volatility index: FRED VIXCLS (fed-data), daily

**Theoretical Role:** The Funke et al. (2016) finding represents the single strongest empirically documented economic-to-political transmission mechanism. Specifically, systemic financial crises (not normal recessions) produce a predictable political response: far-right vote gains, increased polarization, reduced governing majorities. The effect peaks 5-10 years after crisis onset. This directly supports the Financial Stress Pathway (FSP) model in the project codebase.

---

### 7. Government Trust / State Legitimacy

**Rating:** Strong
**Domain(s):** Revolution Prediction, Democratic Backsliding, Historical Case Studies, Economic Preconditions, Media/Information
**Data Availability:** `other-data`

**Definition:** The degree to which the public trusts government institutions to act competently and in the public interest. Measures the legitimacy buffer between structural stress and political instability.

**Evidence:**
| Study | Proxy Used | Finding | Type |
|-------|-----------|---------|------|
| Norris (2011) | Survey trust data (multiple countries) | Declining trust signals democratic deficit | quant |
| Dalton (2004) | Trust in government surveys | Trust erosion correlated with declining political support | quant |
| Brinton (1938) | Loss of confidence by ruling class | Loss of legitimacy preceded all four revolution cases | qual |
| Kurzman (2004) | Perceived regime vulnerability | Revolution became "thinkable" when legitimacy collapsed | qual |
| Algan et al. (2017) | Trust in economic institutions | Low institutional trust amplifies financial crisis -> political transmission | quant |

**Measurement Approaches:**
- Pew "trust in government" survey: Pew Research Center (other-data), roughly annual since 1958
- Gallup institutional confidence composite: Gallup (other-data), roughly annual since 1973
- Edelman Trust Barometer: Edelman (other-data), annual
- Trust by specific institution (Congress, presidency, courts, media): Gallup (other-data)

**Theoretical Role:** Trust in government is a mediating variable -- it modulates the transmission of structural stress into political instability. When trust is high, societies can absorb economic shocks without political crisis. When trust is low, even modest economic distress can trigger political mobilization. US trust declined from ~75% (1960s) to ~20% (2020s), removing the legitimacy buffer that historically absorbed structural pressures.

---

### 8. Elite Overproduction

**Rating:** Strong
**Domain(s):** Revolution Prediction, Historical Case Studies
**Data Availability:** `fed-data` (partial)

**Definition:** The production of more individuals with elite aspirations, credentials, and expectations than the society has elite positions to offer. Creates a pool of "frustrated aspirants" who have the education and skills to organize opposition.

**Evidence:**
| Study | Proxy Used | Finding | Type |
|-------|-----------|---------|------|
| Turchin (2003, 2023) | Ratio of elite aspirants to elite positions | Elite overproduction is a core structural-demographic variable | quant |
| Goldstone (1991) | University-educated population / official positions | Elite overproduction preceded all four early modern revolutions | qual |
| Georgescu (2023) | Education-job mismatch for OECD countries | SDT confirmed for industrialized societies using credential inflation proxy | quant |

**Measurement Approaches:**
- Advanced degree holders per professional job opening: Census/BLS (fed-data)
- Law school graduates per legal position: BLS/NCES (fed-data)
- MBA/PhD production rates vs. professional position growth: BLS/NCES (fed-data)
- Top 1% income share (imperfect proxy): WID (other-data)
- Education-job mismatch index: Derived from Census education data + BLS occupational statistics (fed-data)

**Theoretical Role:** Core Elite Mobilization Potential (EMP) variable in Turchin's structural-demographic theory. When a society produces more elites than it can absorb, the frustrated aspirants become "counter-elites" who channel mass grievances into organized opposition. In modern industrialized societies, this manifests as credential inflation -- law graduates unable to find legal employment, PhD holders in adjunct positions, MBA holders in entry-level jobs. Georgescu (2023) operationalization via education-job mismatch is more theoretically faithful than the top 1% income share proxy currently in the codebase.

---

### 9. Unemployment Rate

**Rating:** Strong
**Domain(s):** Revolution Prediction, Economic Preconditions, Social Movement Theory
**Data Availability:** `fed-data`

**Definition:** The proportion of the labor force that is actively seeking but unable to find employment. A direct measure of labor market distress.

**Evidence:**
| Study | Proxy Used | Finding | Type |
|-------|-----------|---------|------|
| Collier & Hoeffler (2004) | National unemployment rate | Low income and slow growth (correlated with high unemployment) predict conflict | quant |
| Campante & Chor (2012) | Youth unemployment | Youth unemployment > 30% preceded Arab Spring | quant |
| Fetzer (2019) | Regional unemployment + austerity | Unemployment and austerity predicted Brexit vote share | quant |
| Korotayev-Medvedev ML ranking | Unemployment rate | Ranked among top ML-identified predictive factors | quant |

**Measurement Approaches:**
- U-3 unemployment rate: BLS/FRED UNRATE (fed-data), monthly
- U-6 underemployment rate: BLS/FRED U6RATE (fed-data), monthly
- Initial jobless claims: FRED ICSA (fed-data), weekly
- Long-term unemployment share: BLS (fed-data), monthly

**Theoretical Role:** Unemployment directly reduces the opportunity cost of protest participation (unemployed people have time) and increases economic grievances. Spikes in unemployment precede instability episodes in US history (2008-2010 crisis, 2020 pandemic). Strong US time-series variation makes this a valuable predictor.

---

### 10. GDP Growth Rate

**Rating:** Strong
**Domain(s):** Revolution Prediction, Historical Case Studies, Economic Preconditions
**Data Availability:** `fed-data`

**Definition:** The rate of real economic growth, particularly deviations from trend growth (deceleration or contraction). The J-curve theory emphasizes reversal from growth as more dangerous than absolute poverty.

**Evidence:**
| Study | Proxy Used | Finding | Type |
|-------|-----------|---------|------|
| Davies (1962) | Economic growth trajectory | Growth reversal (J-curve) produces revolutionary frustration | qual |
| Collier & Hoeffler (2004) | GDP per capita growth | Low growth is the strongest predictor of civil war onset | quant |
| Acemoglu & Robinson (2006) | GDP growth and democracy transitions | Economic crises create windows for regime change | quant |
| Korotayev-Medvedev ML ranking | GDP growth rate | Top-ranked variable in ML factor importance analysis | quant |

**Measurement Approaches:**
- Real GDP growth (quarterly, annualized): FRED/BEA (fed-data)
- Real GDP per capita growth: FRED A939RX0Q048SBEA (fed-data), quarterly
- GDP growth deviation from trend: Derived from FRED (fed-data)

**Theoretical Role:** Growth deceleration or contraction creates the conditions for political instability by frustrating expectations, increasing unemployment, and reducing the state's fiscal capacity. The J-curve theory (Davies 1962) emphasizes that the reversal from growth is more politically dangerous than persistent poverty -- societies that have experienced improvement rebel when improvement stops.

---

### 11. Elite Factionalism / Fragmentation

**Rating:** Strong
**Domain(s):** Revolution Prediction, Democratic Backsliding, Historical Case Studies
**Data Availability:** `other-data`

**Definition:** The degree to which political, economic, and social elites are divided into competing factions unable to cooperate on governance. Distinct from (but related to) polarization -- measures division *within* the ruling class specifically.

**Evidence:**
| Study | Proxy Used | Finding | Type |
|-------|-----------|---------|------|
| Goldstone (1991, 2010) | PITF factionalism coding | Factionalism is a key component of the PITF's highest-risk regime category | quant |
| Skocpol (1979) | Elite cohesion in France, Russia, China | Elite division was a necessary precondition in all three cases | qual |
| Walter (2022) | Ethno-nationalist factionalism | Rising factionalism places US in higher PITF risk category | qual |
| Haggard & Kaufman (2021) | Elite polarization/factionalism | Elite division preceded backsliding in all 16 comparative cases | qual |

**Measurement Approaches:**
- DW-NOMINATE overlap scores: VoteView (other-data), annual, 1789-present
- Party unity scores: Congressional voting records (other-data)
- Bipartisan bill cosponsorship rates: Congress.gov (other-data)
- V-Dem factionalism indicators: V-Dem (other-data)

**Theoretical Role:** Elite factionalism is analytically distinct from polarization -- it measures whether the governing class can cooperate to solve problems. When elites are fractured, the state cannot respond to crises, reforms are blocked, and each faction may seek to mobilize mass supporters as political weapons. Goldstone et al. (2010) found that partial democracies *with factionalism* are 10-15x more likely to experience state failure than those without.

---

### 12. Protest Frequency and Participation

**Rating:** Strong
**Domain(s):** Revolution Prediction, Historical Case Studies, Social Movement Theory
**Data Availability:** `other-data`

**Definition:** The frequency, scale, and trajectory of protest events. Both a leading indicator of instability and a direct measure of mobilization capacity.

**Evidence:**
| Study | Proxy Used | Finding | Type |
|-------|-----------|---------|------|
| Chenoweth & Stephan (2011) | Campaign participation rate (NAVCO) | 3.5% participation threshold -- no campaign of this size has failed | quant |
| Tarrow (1994) | Protest cycle frequency | Clustering of protest events signals protest cycle onset | qual |
| Clark & Regan (2016) | Mass Mobilization Project event counts | Protest clustering is stronger predictor than isolated large events | quant |
| Lohmann (1994) | Protest size as information signal | Rising protest signals regime vulnerability, lowers subsequent thresholds | quant |

**Measurement Approaches:**
- ACLED-US protest event counts: ACLED (other-data), event-level, 2020-present
- Count Love protest tracker: Count Love (other-data), event-level, 2017-present
- Mass Mobilization Project: Academic dataset (other-data), 1990-2020
- Protest participation survey questions: Pew/ANES (other-data), periodic

**Theoretical Role:** Protest frequency and participation serve as both a leading indicator and a direct measure of political instability. Rising protest indicates that structural grievances are being translated into collective action. The social movement literature emphasizes that protest clustering (rapid succession of events) is more predictive than isolated large events. For the US, major protest waves (1960s, 2011, 2020) correspond to periods of elevated structural stress.

---

### 13. Regime Type / Institutional Quality

**Rating:** Strong -- Contested
**Domain(s):** Revolution Prediction, Democratic Backsliding, Historical Case Studies
**Data Availability:** `other-data`

**Definition:** The quality of democratic institutions and the degree to which the political system is a full democracy, partial democracy (anocracy), or autocracy. The PITF model's single strongest predictor.

**Evidence:**
| Study | Proxy Used | Finding | Type |
|-------|-----------|---------|------|
| Goldstone et al. (2010) | Polity IV/V regime type (5 categories) | Partial democracies with factionalism 10-15x more failure-prone | quant |
| Walter (2022) | Polity score + anocracy concept | Argues US has moved toward anocratic zone | qual |
| V-Dem Institute (2023) | Liberal Democracy Index | US coded as experiencing "episode of autocratization" since 2016 | quant |
| Grumbach (2023) | State Democracy Index | US democratic quality varies enormously across states | quant |

**Contested:** The application of PITF regime type variables to the US is heavily debated. Svolik (2019), Levitsky & Ziblatt (2018), and Przeworski (2019) argue US institutional depth makes it categorically different from PITF training data. V-Dem's coding of the US as "autocratizing" is contested by scholars who argue measurement artifacts conflate dramatic episodes with underlying institutional change.

**Measurement Approaches:**
- Polity V score: Center for Systemic Peace (other-data)
- V-Dem Liberal Democracy Index (v2x_libdem): V-Dem (other-data), annual, 1900-present
- V-Dem component indices (judicial independence, legislative constraints, etc.): V-Dem (other-data)
- Grumbach State Democracy Index: Academic dataset (other-data)
- Freedom House ratings: Freedom House (other-data), annual

**Theoretical Role:** The PITF model's strongest predictor -- partial democracies with ethnic factionalism have dramatically elevated instability risk. For the US, the question is whether recent institutional erosion (as measured by V-Dem and Polity declines) represents genuine movement toward the high-risk anocratic zone, or whether US institutional resilience makes this comparison inappropriate. The disaggregated approach (using V-Dem component scores and Grumbach state-level indices rather than a single national score) may be more informative.

---

### 14. Relative Deprivation / Expectation-Reality Gap

**Rating:** Moderate
**Domain(s):** Revolution Prediction, Historical Case Studies, Economic Preconditions
**Data Availability:** `fed-data`

**Definition:** The perceived gap between what people expect to have (based on prior trajectory or reference groups) and what they actually have. The psychological mechanism driving political frustration.

**Evidence:**
| Study | Proxy Used | Finding | Type |
|-------|-----------|---------|------|
| Davies (1962) | Economic trajectory reversal (J-curve) | Revolutions follow periods of rising expectations dashed by reversal | qual |
| Gurr (1970) | Perceived value discrepancy | Relative deprivation drives political violence | qual |
| Turchin (2020) | Structural indicators of mass frustration | 2010 prediction of 2020s instability confirmed | qual |
| Passarelli & Del Ponte (2020) | Prospect theory applied to political behavior | Loss aversion amplifies economic grievances | qual |

**Measurement Approaches:**
- Consumer sentiment (UMCSENT) vs. actual GDP/employment: FRED (fed-data), monthly
- Consumer expectations vs. current conditions gap: FRED (fed-data), monthly
- Perceived vs. actual inflation gap: BLS/survey data (fed-data + other-data)
- Subjective economic well-being surveys: Pew/Gallup (other-data)

**Theoretical Role:** Relative deprivation is the psychological mechanism linking economic conditions to political behavior. People do not rebel based on absolute conditions but based on the gap between expectations and reality. The J-curve (Davies), relative deprivation (Gurr), and prospect theory (Kahneman & Tversky, applied by Passarelli & Del Ponte) all converge on this insight. Measurable through the gap between consumer sentiment/expectations and actual economic indicators.

---

### 15. Horizontal Inequality (Between-Group)

**Rating:** Moderate
**Domain(s):** Revolution Prediction, Democratic Backsliding, Economic Preconditions
**Data Availability:** `fed-data`

**Definition:** Inequality between politically relevant identity groups (racial, ethnic, regional) rather than between individuals. The politically salient dimension of inequality.

**Evidence:**
| Study | Proxy Used | Finding | Type |
|-------|-----------|---------|------|
| Cederman, Gleditsch & Buhaug (2013) | GeoEPR group-level inequality | Groups much richer or poorer than average are more conflict-prone | quant |
| Stewart (2008) | Horizontal inequality measures | Between-group inequality more predictive than aggregate inequality | quant |
| Chetty et al. (2020) | Racial income/mobility gaps | Persistent racial gaps in intergenerational mobility | quant |

**Measurement Approaches:**
- Black-White median household income ratio: Census/BLS (fed-data), annual
- Racial wealth gap: Federal Reserve SCF (fed-data), triennial
- Hispanic-White earnings gap: BLS (fed-data), annual
- Geographic (urban-rural, state-level) income inequality: BEA (fed-data), annual

**Theoretical Role:** Cederman et al. (2013) demonstrated that aggregate inequality measures (Gini) miss the politically relevant dimension: inequality between identity-based groups. In the US, persistent racial income and wealth gaps represent horizontal inequalities that map onto politically mobilized identity groups. This variable captures dynamics that aggregate inequality measures miss.

---

### 16. Housing Affordability

**Rating:** Moderate
**Domain(s):** Economic Preconditions
**Data Availability:** `fed-data`

**Definition:** The cost of housing relative to household income. Identified as the US analog to food price triggers in historical revolutions, since housing consumes a much larger share of US household budgets (~30-40%) than food (~10%).

**Evidence:**
| Study | Proxy Used | Finding | Type |
|-------|-----------|---------|------|
| Ansell (2014) | Home price indices, affordability ratios | Housing wealth and prices affect political attitudes | quant |
| Joint Center for Housing Studies (2024) | Rent burden measures | Record-high cost-burdened renter share | quant |
| Bellemare (2015) | Food prices (analog) | Cost-of-living shocks trigger political mobilization | quant |

**Measurement Approaches:**
- Housing Affordability Index: FRED FIXHAI (fed-data), monthly
- Median home price / median income ratio: FRED MSPUS + Census (fed-data)
- Rent burden (gross rent as % of renter income): Census ACS / HUD (fed-data), annual
- Case-Shiller Home Price Index: FRED (fed-data), monthly

**Theoretical Role:** Historical revolutions were often triggered by food price spikes (French Revolution, Arab Spring). In the US, food is only ~10% of household spending, so food prices are unlikely triggers. Housing, at ~30-40% of household spending, is the analogous pressure point. Record-low housing affordability in 2023-2024 represents a cost-of-living shock concentrated on younger and lower-income households -- the demographics most available for political mobilization.

---

### 17. Inflation Rate

**Rating:** Moderate
**Domain(s):** Historical Case Studies, Economic Preconditions
**Data Availability:** `fed-data`

**Definition:** The rate of change in the general price level. Captures the cost-of-living erosion that reduces purchasing power and generates economic grievances.

**Evidence:**
| Study | Proxy Used | Finding | Type |
|-------|-----------|---------|------|
| Cavallo et al. (2017) | Inflation expectations, perceived inflation | Perceived inflation exceeds actual and drives political attitudes | quant |
| Gatrell (2005) | Wartime inflation in Russia | Inflation + supply disruption triggered mass protest in 1917 | qual |
| Rudé (1959) | Bread prices in Paris | Food price inflation was proximate trigger of French Revolution | qual |

**Measurement Approaches:**
- CPI-U year-over-year: BLS/FRED CPIAUCSL (fed-data), monthly
- Core CPI (excluding food and energy): BLS/FRED (fed-data), monthly
- PCE deflator: BEA/FRED (fed-data), monthly
- CPI food component: BLS/FRED (fed-data), monthly
- CPI shelter component: BLS/FRED (fed-data), monthly

**Theoretical Role:** Inflation is politically salient because of loss aversion -- people perceive price increases more intensely than price decreases or income gains (prospect theory). The 2021-2023 inflation surge in the US demonstrated that even moderate inflation (peaking at 9.1% in June 2022) generates significant political grievance. However, the US has never experienced hyperinflation, making this a contributing variable rather than a primary driver.

---

### 18. Consumer Confidence / Sentiment

**Rating:** Moderate
**Domain(s):** Economic Preconditions
**Data Availability:** `fed-data`

**Definition:** Survey-based measures of consumer attitudes about economic conditions -- both current assessment and future expectations. Captures the subjective dimension of economic experience.

**Evidence:**
| Study | Proxy Used | Finding | Type |
|-------|-----------|---------|------|
| Davies (1962) | Economic expectations vs. reality | Gap between expectations and reality drives revolutionary frustration | qual |
| Gurr (1970) | Perceived value capabilities | Subjective perception of deprivation matters more than objective level | qual |
| Cavallo et al. (2017) | Consumer confidence indices | Perception diverges from economic reality; perception drives behavior | quant |

**Measurement Approaches:**
- University of Michigan Consumer Sentiment Index: FRED UMCSENT (fed-data), monthly
- Conference Board Consumer Confidence Index: Conference Board (other-data), monthly
- Consumer Expectations sub-index: FRED MICH (fed-data), monthly

**Theoretical Role:** Consumer sentiment captures the subjective experience of economic conditions that drives political behavior. The gap between the expectations sub-index and actual economic performance may be particularly informative -- a proxy for relative deprivation. Note: the OECD Consumer Confidence series (CSCICP03USM665S) used in the original codebase is DISCONTINUED (flagged in Phase 1 audit). UMCSENT is the recommended replacement.

---

### 19. Intra-Elite Wealth Gap

**Rating:** Moderate
**Domain(s):** Revolution Prediction, Economic Preconditions
**Data Availability:** `other-data`

**Definition:** The gap between the very top of the wealth distribution (top 0.1%) and the merely affluent (top 1-10%). Captures the frustrated aspirant dynamic that drives counter-elite formation.

**Evidence:**
| Study | Proxy Used | Finding | Type |
|-------|-----------|---------|------|
| Turchin (2023) | Top 0.1% vs. top 1-10% income/wealth gap | Intra-elite competition drives counter-elite formation | qual |
| Piketty & Saez (2003) | Top income shares at different thresholds | Divergence between top 0.1% and top 1% accelerated since 1980 | quant |
| Saez & Zucman (2016) | Wealth shares at different percentiles | Top 0.1% wealth share tripled since 1978 | quant |

**Measurement Approaches:**
- Top 0.1% vs. next 0.9% income share: WID (other-data)
- Top 0.1% vs. next 9.9% wealth share: WID (other-data), Federal Reserve DFA (fed-data)
- Ratio of top 0.1% to "merely affluent" income: Piketty-Saez data (other-data)

**Theoretical Role:** Distinct from overall inequality. Turchin emphasizes that elite overproduction creates frustrated aspirants -- people who have elite education and expectations but cannot achieve elite positions. The intra-elite wealth gap measures how much the very top has pulled away from the merely affluent, creating resentment within the professional and educated classes. This is the mechanism that produces "counter-elites" who lead opposition movements.

---

### 20. Middle-Class Income Share

**Rating:** Moderate
**Domain(s):** Economic Preconditions
**Data Availability:** `fed-data`

**Definition:** The share of national income accruing to the middle three income quintiles (20th-80th percentile). A direct measure of middle-class economic health.

**Evidence:**
| Study | Proxy Used | Finding | Type |
|-------|-----------|---------|------|
| Alesina & Perotti (1996) | Middle-class income share | Stronger predictor of instability than Gini coefficient | quant |
| Stiglitz (2012) | Middle-class economic indicators | Hollowing middle class signals distributional failure | qual |
| Piketty (2014) | Income distribution over time | Middle-class share squeezed as top and bottom diverge | quant |

**Measurement Approaches:**
- Income share of 20th-80th percentile: Census income distribution data (fed-data), annual
- Median household income relative to GDP per capita: FRED/Census (fed-data), annual
- Middle-class size (% of households within 2/3 to 2x median income): Census (fed-data)

**Theoretical Role:** Alesina & Perotti (1996) found that middle-class income share was a stronger predictor of political instability than the Gini coefficient. A shrinking middle class signals that economic gains are concentrating at the top while the majority experiences stagnation or decline. The US middle class has experienced well-documented hollowing since the 1970s.

---

### 21. Judicial Independence

**Rating:** Moderate
**Domain(s):** Democratic Backsliding
**Data Availability:** `other-data`

**Definition:** The degree to which the judiciary operates independently of executive and legislative interference. A critical check on executive power and a pillar of democratic governance.

**Evidence:**
| Study | Proxy Used | Finding | Type |
|-------|-----------|---------|------|
| V-Dem Institute (2023) | v2juhcind (high court independence) | US judicial independence has declined in V-Dem coding | quant |
| Ginsburg & Huq (2018) | Constitutional retrogression indicators | Judicial independence is one of five infrastructure domains vulnerable to erosion | qual |
| Levitsky & Ziblatt (2018) | Norm erosion around judicial appointments | Court-packing and appointment politicization signals norm breakdown | qual |

**Measurement Approaches:**
- V-Dem high court independence (v2juhcind): V-Dem (other-data), annual
- V-Dem government attacks on judiciary (v2jupoatck): V-Dem (other-data), annual
- World Justice Project Rule of Law Index: WJP (other-data), annual
- Supreme Court approval rating: Gallup (other-data), periodic

**Theoretical Role:** Judicial independence is a key democratic guardrail. When courts can check executive overreach, the mechanisms of democratic erosion (executive aggrandizement, strategic harassment) are constrained. Declining judicial independence -- whether through court packing, appointment politicization, or delegitimization campaigns -- removes a critical buffer.

---

### 22. Freedom of Expression / Media Independence

**Rating:** Moderate
**Domain(s):** Democratic Backsliding, Media/Information Ecosystem
**Data Availability:** `other-data`

**Definition:** The degree to which media operates independently of government control and citizens can freely express political views. A critical information channel for democratic accountability.

**Evidence:**
| Study | Proxy Used | Finding | Type |
|-------|-----------|---------|------|
| V-Dem Institute (2023) | v2x_freexp_altinf | Freedom of expression component has declined in US V-Dem coding | quant |
| Bermeo (2016) | Media restriction as backsliding mechanism | Media restriction is a common tool of executive aggrandizement | qual |
| Reporters Without Borders | Press Freedom Index | US press freedom ranking has declined | quant |

**Measurement Approaches:**
- V-Dem freedom of expression (v2x_freexp_altinf): V-Dem (other-data), annual
- V-Dem government censorship of media (v2mecenefm): V-Dem (other-data), annual
- Reporters Without Borders Press Freedom Index: RSF (other-data), annual
- Local news deserts data: UNC School of Media and Journalism (other-data)

**Theoretical Role:** A free and independent press enables democratic accountability by informing citizens about government actions and enabling public deliberation. When media independence declines -- through government pressure, ownership concentration, or economic collapse of local news -- the information environment degrades, making it harder for citizens to hold leaders accountable and easier for misinformation to fill the void.

---

### 23. Legislative Constraints on Executive

**Rating:** Moderate
**Domain(s):** Democratic Backsliding
**Data Availability:** `other-data`

**Definition:** The degree to which the legislature effectively constrains executive power through oversight, investigation, and legislative authority. A core separation-of-powers indicator.

**Evidence:**
| Study | Proxy Used | Finding | Type |
|-------|-----------|---------|------|
| V-Dem Institute (2023) | v2xlg_legcon | Legislative constraints component in US V-Dem coding | quant |
| Ginsburg & Huq (2018) | Checks and balances index | One of five infrastructure domains vulnerable to retrogression | qual |

**Measurement Approaches:**
- V-Dem legislative constraints on executive (v2xlg_legcon): V-Dem (other-data), annual
- Congressional oversight hearing frequency: Congressional Research Service (other-data)
- Executive order frequency: Federal Register (fed-data)
- Government shutdown frequency: Derived from Treasury/FRED (fed-data)

**Theoretical Role:** Legislative constraints are a key check on executive aggrandizement -- the dominant mechanism of modern democratic backsliding (Bermeo 2016). When legislatures cannot or will not constrain executive overreach, the separation-of-powers framework weakens. US variation occurs with unified vs. divided government and with shifting norms around congressional oversight.

---

### 24. Electoral Integrity / Fraud Perception

**Rating:** Moderate
**Domain(s):** Democratic Backsliding, Historical Case Studies
**Data Availability:** `other-data`

**Definition:** The degree to which elections are perceived as free, fair, and legitimate. Includes both actual electoral integrity and public perception of it.

**Evidence:**
| Study | Proxy Used | Finding | Type |
|-------|-----------|---------|------|
| Tucker (2007) | Perceived electoral fraud | Electoral fraud perception triggered all Color Revolutions | qual |
| Norris (2014) | Perception of Electoral Integrity (PEI) index | Electoral integrity varies across democracies and over time | quant |
| Walter (2022) | Election legitimacy perception | Election denial increases extra-institutional mobilization risk | qual |
| Grumbach (2023) | State-level electoral integrity indicators | Significant US state-level variation | quant |

**Measurement Approaches:**
- Perception of Electoral Integrity (PEI) index: Electoral Integrity Project (other-data)
- Public confidence in elections surveys: Gallup/Pew (other-data)
- State-level election law databases: NCSL (other-data)
- Election challenge filings: Court records (other-data)

**Theoretical Role:** When citizens believe elections are stolen or rigged, they may turn to extra-institutional means of contesting power. The Color Revolutions were all triggered by manifestly fraudulent elections. In the US, persistent election denial (roughly 30% of Americans questioning the 2020 election legitimacy as of 2023) represents a qualitative shift in the information environment around elections.

---

### 25. Civil Society Density / Union Membership

**Rating:** Moderate
**Domain(s):** Democratic Backsliding, Historical Case Studies, Social Movement Theory
**Data Availability:** `fed-data`

**Definition:** The density of civil society organizations, with union membership as the primary measurable proxy. Captures organizational infrastructure for collective action.

**Evidence:**
| Study | Proxy Used | Finding | Type |
|-------|-----------|---------|------|
| McCarthy & Zald (1977) | Organizational resources | Resource availability determines whether mobilization occurs | qual |
| McAdam (1982) | Indigenous organizational strength | Pre-existing organizations enabled civil rights mobilization | qual |
| Putnam (2000) | Civic association membership | Declining "social capital" weakens democratic resilience | quant |
| Kaufman & Haggard (2021) | Civil society density | Active civil society buffers against democratic erosion | qual |
| Pinckney (2020) | Labor union participation in campaigns | Union involvement significantly increases campaign success probability | quant |

**Measurement Approaches:**
- Union membership as % of labor force: BLS (fed-data), annual, 1973-present
- IRS nonprofit registrations per capita: IRS (fed-data)
- Professional association membership: Surveys (other-data)
- Religious congregation participation: Surveys (other-data)

**Theoretical Role:** Civil society organizations serve dual roles: they buffer against democratic erosion (by constraining would-be authoritarians) and they facilitate mobilization (by providing organizational infrastructure for collective action). US union density declined from ~35% (1954) to ~10% (2024), representing a significant decline in organized mobilization capacity. The relationship is complex -- both very high and very low organizational density may be associated with instability.

---

### 26. Youth Unemployment / Disconnection

**Rating:** Moderate
**Domain(s):** Historical Case Studies, Economic Preconditions
**Data Availability:** `fed-data`

**Definition:** Unemployment and economic disconnection among young adults (ages 16-24). Young people have lower opportunity costs for political mobilization and are disproportionately affected by credential inflation.

**Evidence:**
| Study | Proxy Used | Finding | Type |
|-------|-----------|---------|------|
| Campante & Chor (2012) | Youth unemployment rate | Youth unemployment > 30% preceded Arab Spring uprisings | quant |
| Urdal (2006) | Youth bulge + unemployment interaction | Youth demographic pressure amplified by unemployment | quant |
| Goldstone (1991) | Young population competition for positions | Youth overproduction drives mobilization potential | qual |

**Measurement Approaches:**
- Youth (16-24) unemployment rate: BLS/FRED (fed-data), monthly
- NEET rate (not in education, employment, or training): BLS/OECD (fed-data / other-data)
- Student debt burden: Federal Reserve / Education Department (fed-data)

**Theoretical Role:** Young people are disproportionately available for mobilization (lower economic and family commitments) and disproportionately affected by credential inflation and labor market barriers. While the US does not have a demographic youth bulge (aging population), youth disconnection from economic opportunity creates similar dynamics. The NEET rate captures a broader set of disengaged youth than the unemployment rate alone.

---

### 27. Household Debt / Leverage

**Rating:** Moderate
**Domain(s):** Economic Preconditions
**Data Availability:** `fed-data`

**Definition:** The level and trajectory of household indebtedness relative to income and GDP. A precursor to financial crises and a measure of household financial fragility.

**Evidence:**
| Study | Proxy Used | Finding | Type |
|-------|-----------|---------|------|
| Mian, Sufi & Trebbi (2014) | Household debt-to-GDP | Rapid household leverage growth precedes financial crises | quant |
| Funke et al. (2016) | Banking crisis indicator (often debt-driven) | Financial crises -> political extremism | quant |

**Measurement Approaches:**
- Household debt-to-GDP: FRED HDTGPDUSQ163N (fed-data), quarterly
- Household debt service ratio: FRED TDSP (fed-data), quarterly
- Consumer credit growth rate: FRED (fed-data), monthly
- Mortgage delinquency rates: FRED (fed-data), quarterly

**Theoretical Role:** Household leverage is a leading indicator of financial crisis -- rapid debt growth creates fragility that can produce systemic crises when triggered by economic shocks. Since financial crises have the strongest documented transmission to political instability (Funke et al. 2016), household debt serves as an upstream predictor.

---

### 28. Media Trust / Partisan Media Trust Gap

**Rating:** Moderate
**Domain(s):** Media/Information Ecosystem
**Data Availability:** `other-data`

**Definition:** Public trust in media institutions, particularly the gap in trust between partisan groups. Captures the information environment fracture where partisans inhabit different media ecosystems.

**Evidence:**
| Study | Proxy Used | Finding | Type |
|-------|-----------|---------|------|
| Gallup | Trust in mass media survey | Trust declined from 72% (1976) to 32% (2023) | quant |
| Pew Research Center | Partisan media trust gap | Republican trust in national news media fell from 52% (2002) to 11% (2022) | quant |
| Reuters Institute | Digital News Report | US has among lowest media trust of developed democracies | quant |

**Measurement Approaches:**
- Gallup trust in media: Gallup (other-data), roughly annual since 1972
- Pew partisan media trust gap: Pew Research Center (other-data), periodic
- Reuters Institute Digital News Report: Reuters (other-data), annual

**Theoretical Role:** When media trust collapses and the trust gap between partisans widens, the shared information baseline for democratic deliberation erodes. Each partisan group increasingly inhabits a different informational reality, making compromise and cooperation harder. The partisan trust gap may be more politically meaningful than overall trust levels -- it captures the fracture that produces parallel information ecosystems.

---

### 29. Voter Access Restrictions / Partisan Gerrymandering

**Rating:** Moderate
**Domain(s):** Democratic Backsliding
**Data Availability:** `other-data`

**Definition:** The degree to which electoral rules restrict voter participation or distort representation through gerrymandering. Measures electoral fairness at the state level.

**Evidence:**
| Study | Proxy Used | Finding | Type |
|-------|-----------|---------|------|
| Grumbach (2023) | State Democracy Index components | Voter access and gerrymandering are key backsliding indicators | quant |
| Stephanopoulos & McGhee (2015) | Efficiency gap | Quantitative measure of partisan gerrymandering | quant |
| Haggard & Kaufman (2021) | Electoral manipulation measures | Electoral manipulation is a form of executive aggrandizement | qual |

**Measurement Approaches:**
- Grumbach State Democracy Index: Academic dataset (other-data)
- Efficiency gap by state/district: Redistricting data (other-data)
- Voter ID law stringency: NCSL state election law database (other-data)
- Polling place closures: State/county records (other-data)

**Theoretical Role:** Electoral fairness is a foundational requirement for democratic legitimacy. When citizens perceive that elections are rigged through gerrymandering or voter suppression, they may turn to extra-institutional means of contesting power. Grumbach's (2023) finding that state-level variation in the US is enormous -- with some states comparable to European democracies and others to hybrid regimes -- highlights this as a key US-specific variable.

---

### 30. Democratic Commitment (Attitudinal)

**Rating:** Moderate
**Domain(s):** Democratic Backsliding
**Data Availability:** `other-data`

**Definition:** The degree to which citizens believe democracy is essential and reject authoritarian alternatives. Measures the attitudinal foundation of democratic governance.

**Evidence:**
| Study | Proxy Used | Finding | Type |
|-------|-----------|---------|------|
| Mounk (2018) | World Values Survey "importance of democracy" | Declining percentages rate democracy as essential, especially younger cohorts | quant |
| Foa & Mounk (2016) | Support for authoritarian alternatives | Growing openness to military rule, rule by strong leader | quant |
| Norris (2011) | Democratic commitment surveys | "Critical citizens" vs. disengaged citizens | quant |

**Measurement Approaches:**
- World Values Survey democratic essentialness question: WVS (other-data), waves every ~5 years
- ANES questions on democratic norms: ANES (other-data), biennial
- Pew governance preferences: Pew (other-data), periodic
- Support for authoritarian alternatives: WVS/ANES (other-data)

**Theoretical Role:** When a significant share of the public is open to authoritarian alternatives, elected leaders face no electoral punishment for norm-breaking behavior. Democratic deconsolidation (Mounk's concept) describes the attitudinal decay that enables institutional erosion. Generational differences are significant -- younger cohorts show lower democratic commitment in survey data.

---

### 31. Anti-System Party Vote Share

**Rating:** Moderate
**Domain(s):** Democratic Backsliding, Economic Preconditions
**Data Availability:** `fed-data`

**Definition:** The electoral support for parties or candidates that reject core democratic norms or challenge the legitimacy of the political system. A behavioral measure of democratic dissatisfaction.

**Evidence:**
| Study | Proxy Used | Finding | Type |
|-------|-----------|---------|------|
| Mounk (2018) | Anti-system party vote share | Rising support for anti-establishment parties signals democratic stress | quant |
| Funke et al. (2016) | Far-right vote share post-financial crisis | Financial crises produce ~30% increase in far-right voting | quant |
| Norris & Inglehart (2019) | Populist party support | Cultural backlash drives authoritarian populist voting | quant |

**Measurement Approaches:**
- Third-party and anti-establishment candidate vote shares: FEC election data (fed-data)
- Primary election results for anti-establishment candidates: FEC (fed-data)
- Congressional Freedom Caucus / Progressive Caucus size: Congressional records (other-data)

**Theoretical Role:** Anti-system voting is a behavioral indicator of political dissatisfaction that goes beyond survey attitudes. When significant portions of the electorate support candidates who reject democratic norms or the political establishment, it signals that structural grievances have translated into political action. In the US two-party system, this manifests within parties (anti-establishment primary candidates) rather than through third parties.

---

### 32. Executive Aggrandizement

**Rating:** Moderate
**Domain(s):** Democratic Backsliding
**Data Availability:** `other-data`

**Definition:** Actions by elected executives that concentrate power beyond institutional norms -- court packing, inspector general firings, executive order overreach, weakening oversight mechanisms.

**Evidence:**
| Study | Proxy Used | Finding | Type |
|-------|-----------|---------|------|
| Bermeo (2016) | Executive aggrandizement events | The dominant form of 21st-century democratic backsliding | qual |
| Haggard & Kaufman (2021) | Executive power concentration measures | Executive aggrandizement occurred in 14 of 16 backsliding cases | qual |
| Ginsburg & Huq (2018) | Constitutional retrogression indicators | Incremental, formally legal power concentration | qual |

**Measurement Approaches:**
- V-Dem executive respect for constitution (v2exrescon): V-Dem (other-data), annual
- Executive order frequency: Federal Register (fed-data)
- Inspector general firings/vacancies: Government records (other-data)
- Signing statement frequency: Academic datasets (other-data)

**Theoretical Role:** Bermeo (2016) established that modern democratic backsliding occurs primarily through executive aggrandizement -- elected leaders gradually dismantling institutional checks through formally legal means. This is the dominant mechanism in 21st-century cases (Hungary, Poland, Turkey, Venezuela). It is incremental and operates within legal bounds, making it harder to detect and resist than outright coups.

---

### 33. Misinformation Prevalence / Exposure

**Rating:** Weak -- Contested
**Domain(s):** Media/Information Ecosystem
**Data Availability:** `unknown`

**Definition:** The prevalence and spread of false or misleading information in the political information ecosystem. Theoretically important but with contested impact and severe measurement challenges.

**Evidence:**
| Study | Proxy Used | Finding | Type |
|-------|-----------|---------|------|
| Vosoughi, Roy & Aral (2018) | Twitter false news sharing rates | False news spreads 6x faster than true news | quant |
| Loomba et al. (2021) | Misinformation exposure + vaccination intent | Exposure to misinformation reduced vaccination intent by 8.8 percentage points | quant |
| Guess et al. (2019) | Facebook fake news exposure | 1% of users accounted for 80% of fake news exposure | quant |

**Contested:** Guess et al. (2019) found that misinformation consumption is highly concentrated among a small minority. Nyhan (2020) argues that individual-level persuasion effects are modest. The counter-argument (Benkler et al. 2018) is that the system-level effect -- creating an "epistemic crisis" where shared facts collapse -- matters more than individual persuasion.

**Measurement Approaches:**
- Self-reported misinformation exposure: Pew surveys (other-data)
- False news sharing rates: Platform data (increasingly restricted) (unknown)
- Specific conspiracy belief prevalence: PRRI/Pew surveys (other-data)

**Theoretical Role:** Misinformation's political importance may lie not in individual persuasion but in undermining the shared factual basis for democratic deliberation. When significant population segments inhabit different factual realities, democratic processes break down. However, measurement at population scale remains extremely difficult, and the causal relationship between misinformation exposure and political behavior is contested.

---

### 34. Conspiratorial Thinking Prevalence

**Rating:** Weak
**Domain(s):** Media/Information Ecosystem
**Data Availability:** `other-data`

**Definition:** The prevalence of conspiracy beliefs (election denial, deep state beliefs, QAnon-adjacent thinking) that delegitimize democratic institutions.

**Evidence:**
| Study | Proxy Used | Finding | Type |
|-------|-----------|---------|------|
| Uscinski & Parent (2014) | Survey measures of conspiracy belief | Conspiracy thinking has deep historical roots in US politics | qual |
| PRRI surveys (2017-present) | QAnon, election denial tracking | ~30% of Americans question 2020 election legitimacy | quant |

**Measurement Approaches:**
- PRRI American Values Survey conspiracy items: PRRI (other-data), annual since ~2017
- Pew conspiracy belief tracking: Pew (other-data), periodic
- Election denial survey measures: Multiple survey organizations (other-data)

**Theoretical Role:** Conspiratorial thinking signals that a portion of the population has rejected the legitimacy of democratic institutions. This population is more likely to support extra-institutional political action. However, measurement is relatively new (systematic tracking since ~2017) and historical time-series depth is insufficient for backtesting.

---

### 35. Social Media Political Engagement

**Rating:** Weak -- Contested
**Domain(s):** Social Movement Theory, Media/Information Ecosystem
**Data Availability:** `unknown`

**Definition:** The volume and intensity of political content on social media platforms. Captures digital mobilization capacity and the information environment that shapes political behavior.

**Evidence:**
| Study | Proxy Used | Finding | Type |
|-------|-----------|---------|------|
| Tufekci (2017) | Social media protest coordination | Digital tools enable rapid mobilization but may weaken organizational depth | qual |
| Gonzalez-Bailon et al. (2011) | Twitter protest recruitment dynamics | Broadcast messages from central nodes drive recruitment | quant |
| Steinert-Threlkeld et al. (2015) | Geolocated tweets | Social media coordination signals predicted next-day protest size | quant |

**Contested:** The causal relationship between social media engagement and political outcomes is debated. Boxell et al. (2017) found that polarization increased most among demographics using social media least (over-65). The "slacktivism" critique (Gladwell 2010) argues that online engagement substitutes for rather than complements real-world action.

**Measurement Approaches:**
- Political content volume on platforms: Platform APIs (increasingly restricted) (unknown)
- FEC political ad spending on social media: FEC (fed-data, partial)
- Protest-related hashtag frequency: Platform data (unknown)

**Theoretical Role:** Social media is a transmission mechanism that can accelerate mobilization and amplify grievances. However, it is increasingly unmeasurable due to platform API restrictions since 2023, and the causal direction (does social media cause mobilization or reflect it?) remains debated. For the Revolution Index, this is best understood as an amplifier of underlying structural conditions rather than an independent predictor.

---

### 36. Protest Diffusion / Contagion

**Rating:** Weak
**Domain(s):** Historical Case Studies, Social Movement Theory
**Data Availability:** `other-data`

**Definition:** The spatial and temporal clustering of protest events -- the tendency for protests to spread from one location/issue to another in cascade dynamics.

**Evidence:**
| Study | Proxy Used | Finding | Type |
|-------|-----------|---------|------|
| Beissinger (2002) | Protest diffusion across Soviet republics | Spatial and temporal diffusion with decay function | quant |
| Lynch (2012) | Arab Spring cross-country spread | Social media and geographic proximity accelerated diffusion | qual |

**Measurement Approaches:**
- Temporal clustering analysis of ACLED event data: ACLED (other-data)
- Spatial autocorrelation of protest events: Derived from event data (other-data)
- Protest acceleration rate (events per week): Derived from ACLED (other-data)

**Theoretical Role:** Protest clustering is a stronger predictor of political instability than isolated large events (Clark & Regan 2016). When protests spread rapidly across locations and issues, it signals that cascading dynamics have engaged -- each successful protest lowers the threshold for subsequent action (Lohmann 1994). This is more of a contextual amplifier than a stable time-series predictor.

---

### 37. Prior Protest Experience

**Rating:** Weak
**Domain(s):** Social Movement Theory
**Data Availability:** `other-data`

**Definition:** The proportion of the population with recent protest participation history. Individuals who have protested before have lower thresholds for future action.

**Evidence:**
| Study | Proxy Used | Finding | Type |
|-------|-----------|---------|------|
| Klandermans (1997) | Survey-based protest participation history | Prior participation lowers future mobilization thresholds | qual |
| Granovetter (1978) | Threshold model of collective behavior | Threshold heterogeneity determines cascade potential | quant |

**Measurement Approaches:**
- Self-reported protest participation: ANES/Pew surveys (other-data), periodic
- BLM 2020 participation estimates: Academic research (other-data)

**Theoretical Role:** The population's "protest experience base" determines how easily structural grievances translate into collective action. BLM 2020 created a large cohort of first-time protesters (estimated 15-26 million participants), potentially lowering future mobilization thresholds. However, this is measurable only through periodic surveys and is not a continuous time-series variable.

---

### 38. State Capacity / Institutional Quality

**Rating:** Moderate
**Domain(s):** Revolution Prediction, Democratic Backsliding, Historical Case Studies
**Data Availability:** `other-data`

**Definition:** The government's ability to effectively deliver public services, enforce laws, and respond to crises. A measure of institutional strength that moderates the relationship between structural stress and instability.

**Evidence:**
| Study | Proxy Used | Finding | Type |
|-------|-----------|---------|------|
| Fearon & Laitin (2003) | State capacity proxies | Weak state capacity predicts conflict regardless of ethnic composition | quant |
| Hanson & Sigman (2021) | Latent state capacity dimensions | State capacity is multidimensional (extractive, coercive, administrative) | quant |
| Kaufman & Haggard (2021) | Institutional resilience measures | Strong institutions buffer economic shocks from producing backsliding | qual |

**Measurement Approaches:**
- World Governance Indicators: World Bank (other-data), annual
- V-Dem state capacity measures: V-Dem (other-data), annual
- Government shutdown frequency: Derived from Treasury/news records (fed-data)
- Agency staffing levels: OPM FedScope data (fed-data)
- GAO High-Risk List: GAO (other-data)

**Theoretical Role:** State capacity is a moderating variable -- it determines whether structural pressures translate into instability or are absorbed by effective institutional responses. Countries with strong institutions can weather economic crises without democratic erosion; countries with weak institutions cannot (Kaufman & Haggard 2021). In the US, standard international measures (WGI) show minimal variation, but granular measures (government shutdowns, agency staffing, congressional productivity) may capture meaningful changes.

---

### 39. Neighborhood / Diffusion Effects (Allied Democracies)

**Rating:** Weak
**Domain(s):** Revolution Prediction, Democratic Backsliding
**Data Availability:** `other-data`

**Definition:** The democratic quality and stability of allied/peer democracies. For the US, geographic neighbors are irrelevant; what matters is whether allied democracies (NATO, Five Eyes, G7) are experiencing backsliding.

**Evidence:**
| Study | Proxy Used | Finding | Type |
|-------|-----------|---------|------|
| Goldstone et al. (2010) | Neighborhood conflict (PITF) | Armed conflict in neighboring states increases instability risk | quant |
| Huntington (1991) | Regional democratic waves | Democratization and de-democratization occur in regional waves | qual |

**Measurement Approaches:**
- Average V-Dem score for NATO/Five Eyes/G7 democracies: V-Dem (other-data)
- Democratic backsliding events in allied states: V-Dem/Freedom House (other-data)
- Global protest wave indices: ACLED/Mass Mobilization Project (other-data)

**Theoretical Role:** Instability diffuses across borders through demonstration effects, shared media environments, and economic linkages. For the US, "neighborhood" means allied democracies rather than geographic neighbors. Brexit, European populist surges, and democratic erosion in EU member states may function as ideological diffusion channels that normalize anti-democratic behavior.

---

### 40. Cost of Living Pressure (Composite)

**Rating:** Moderate
**Domain(s):** Historical Case Studies, Economic Preconditions
**Data Availability:** `fed-data`

**Definition:** The composite pressure of essential costs (housing, food, healthcare, education, energy) on household budgets, particularly for lower-income and middle-income households.

**Evidence:**
| Study | Proxy Used | Finding | Type |
|-------|-----------|---------|------|
| Bellemare (2015) | Food price index | Food price spikes trigger political mobilization | quant |
| Lagi et al. (2011) | FAO food price index | Food price spikes preceded Arab Spring protests | quant |
| Cavallo et al. (2017) | Perceived vs. actual inflation | Perceived inflation exceeds actual and drives political attitudes | quant |

**Measurement Approaches:**
- CPI components (food, shelter, medical care, education, energy): BLS/FRED (fed-data), monthly
- Essential cost burden (essential spending / median income): Derived from BLS/Census (fed-data)
- Food-at-home CPI: FRED (fed-data), monthly
- Healthcare cost growth: CMS/FRED (fed-data)

**Theoretical Role:** Cost-of-living pressure is the modern equivalent of the food price triggers that preceded historical revolutions. In the US, the relevant pressures are housing (30-40% of income), healthcare, education, and food. A composite measure capturing the aggregate burden of essential costs on typical households may be more informative than any single CPI component.

---

### 41. Institutional Legitimacy Denial

**Rating:** Weak
**Domain(s):** Media/Information Ecosystem
**Data Availability:** `other-data`

**Definition:** The proportion of the population that rejects the legitimacy of core democratic institutions -- elections, courts, government authority. Distinct from low trust (which implies frustration) -- denial implies rejection.

**Evidence:**
| Study | Proxy Used | Finding | Type |
|-------|-----------|---------|------|
| Bright Line Watch | Expert and public democratic norm assessments | Tracking of democratic norm support and violation | quant |
| Post-2020 election surveys | Election denial rates | ~30% of Americans questioned 2020 election legitimacy | quant |

**Measurement Approaches:**
- Bright Line Watch surveys: BWL (other-data), periodic
- Election denial survey measures: Pew/PRRI (other-data), periodic
- Proportion rejecting court authority: Surveys (other-data)

**Theoretical Role:** Institutional legitimacy denial represents a qualitative shift from dissatisfaction to rejection. Citizens who deny institutional legitimacy are more likely to support extra-institutional action (as demonstrated on January 6, 2021). This is a relatively new variable in the literature with limited historical depth, but its theoretical importance is high for the contemporary US context.

---

### 42. Political Efficacy Beliefs

**Rating:** Weak
**Domain(s):** Social Movement Theory
**Data Availability:** `other-data`

**Definition:** The belief that collective political action can influence outcomes. A psychological determinant of whether grievances translate into mobilization.

**Evidence:**
| Study | Proxy Used | Finding | Type |
|-------|-----------|---------|------|
| Klandermans (1997, 2004) | Survey-measured efficacy beliefs | Higher efficacy -> more mobilization willingness | qual |

**Measurement Approaches:**
- ANES external political efficacy questions: ANES (other-data), biennial
- Pew political engagement surveys: Pew (other-data), periodic

**Theoretical Role:** Political efficacy moderates the relationship between grievances and action. When people believe action is futile, even severe structural stress produces apathy rather than mobilization. When efficacy is high, modest grievances can produce significant collective action. Survey-based and not continuous time-series.

---

### 43. Information Fragmentation / Echo Chambers

**Rating:** Weak -- Contested
**Domain(s):** Media/Information Ecosystem
**Data Availability:** `unknown`

**Definition:** The degree to which the information environment is fragmented into ideologically homogeneous segments, reducing shared-reality baseline.

**Evidence:**
| Study | Proxy Used | Finding | Type |
|-------|-----------|---------|------|
| Sunstein (2001, 2017) | Ideological segregation of media consumption | Echo chambers reduce exposure to opposing views | qual |
| Bail et al. (2018) | Cross-cutting exposure experiment | Exposure to opposing views did not reduce polarization | quant |
| Flaxman et al. (2016) | Online news consumption patterns | Some ideological segregation but less than often assumed | quant |

**Contested:** The "filter bubble" thesis is largely rejected by empirical evidence (Gentzkow & Shapiro 2011; Boxell et al. 2017). Most people's online news consumption is more diverse than their offline consumption. However, the platform design effects on affective polarization (amplifying outrage and in-group/out-group dynamics) may be the real mechanism rather than information filtering.

**Measurement Approaches:**
- Audience overlap between news sources: Nielsen (other-data)
- Ideological segregation of news consumption: Academic datasets (unknown)
- Cross-cutting exposure measures: Survey/platform data (unknown)

**Theoretical Role:** Information fragmentation theoretically reduces the shared factual basis for democratic deliberation. However, empirical evidence for the "filter bubble" mechanism is weak, and measurement approaches are fragmented and non-standardized. This variable is included for completeness but rated Weak due to both measurement challenges and contested evidence.

---

### 44. Cross-Class Coalition Formation

**Rating:** Weak
**Domain(s):** Historical Case Studies, Social Movement Theory
**Data Availability:** `unknown`

**Definition:** The formation of political alliances that span social classes -- working class, middle class, and disaffected elites -- in opposition to the status quo. A key determinant of whether protest becomes revolution.

**Evidence:**
| Study | Proxy Used | Finding | Type |
|-------|-----------|---------|------|
| Wickham-Crowley (1992) | Cross-class guerrilla-bourgeois alliances | Cross-class coalitions were necessary for successful Latin American revolutions | qual |
| Foran (2005) | Five-factor model including cross-class alliance | Cross-class coalition is one of five necessary revolution conditions | qual |

**Measurement Approaches:**
- Protest participation diversity by demographic: ACLED/survey data (unknown)
- Partisan realignment patterns: FEC/election data (fed-data, partial)
- Cross-income protest participation: Survey data (other-data)

**Theoretical Role:** Historical case studies show that revolutions succeed when they unite multiple social classes. In the US context, the formation of cross-class political coalitions (e.g., Tea Party uniting wealthy donors and working-class voters; BLM uniting Black communities, suburban whites, and progressive professionals) signals the kind of broad opposition that can produce political change. Difficult to measure as a continuous variable.

---

### 45. Wealth Concentration (Top 0.1%)

**Rating:** Strong
**Domain(s):** Revolution Prediction, Economic Preconditions
**Data Availability:** `other-data`

**Definition:** The share of national wealth held by the top 0.1% of the distribution -- the extreme concentration that captures the emergence of an economic oligarchy.

**Evidence:**
| Study | Proxy Used | Finding | Type |
|-------|-----------|---------|------|
| Saez & Zucman (2016, 2020) | Top 0.1% wealth share | US top 0.1% wealth share tripled since 1978 (from ~7% to ~20%) | quant |
| Piketty (2014) | r > g dynamics | Capital return exceeding growth rate drives concentration | quant |
| Turchin (2023) | Wealth concentration as elite power proxy | Extreme concentration signals elite capture of institutions | qual |

**Measurement Approaches:**
- Top 0.1% wealth share: WID (other-data)
- Federal Reserve Distributional Financial Accounts: Federal Reserve DFA (fed-data)
- Forbes 400 / billionaire wealth as % of GDP: Forbes/FRED (other-data)

**Theoretical Role:** Extreme wealth concentration at the very top (0.1%) captures a qualitatively different phenomenon than broader inequality. When a tiny fraction of the population commands disproportionate economic and political power, it signals elite capture of institutions and the emergence of an oligarchic dynamic that structural-demographic theory identifies as a precursor to instability.

---

## Cross-Reference Notes

### Variables Excluded by Measurability Filter

The following theoretically important variables were excluded because no known measurement approach exists:

- **Revolutionary consciousness** (Foran 2005): Qualitative concept with no established quantitative measure
- **Frame resonance** (Snow & Benford 1986): Movement messaging effectiveness; no standardized measure
- **Preference falsification gap** (Kuran 1991): By definition, concealed preferences cannot be directly measured
- **Spiral of silence strength** (Noelle-Neumann 1974): Theoretical construct without established quantitative operationalization
- **AI-generated content prevalence**: Too new; no measurement methodology exists

### Variables Excluded as Not Applicable to US

The following variables are strong global predictors but do not vary meaningfully in the US:

- **Youth bulge / demographic pressure**: US youth share declining (~13% age 15-24); aging population
- **Urbanization rate**: US already ~83% urban with minimal rate of change
- **Military / security force loyalty**: US has stable civilian control; no history of military intervention
- **Natural resource dependence**: US has a diversified economy; not resource-dependent
- **Infant mortality (PITF proxy)**: US consistently in low-mortality group globally
- **Ethnic fractionalization (static)**: Essentially constant over forecasting-relevant timescales
- **Rough terrain / new statehood** (Fearon & Laitin controls): Irrelevant for established states

### Framework Variables (Not Cataloged Here)

The following are frameworks, not variables, and will be assessed in Plan 05:

- Structural-Demographic Theory (Turchin): Framework using MMP, EMP, SFD variables
- PITF Global Forecasting Model (Goldstone): Framework using regime type, infant mortality, discrimination, neighborhood
- Fragile States Index: Framework using 12 composite indicators
- V-Dem Episodes of Regime Transformation: Framework using 483 democracy indicators

---

## Bibliography

Abrahamian, E. 1982. *Iran Between Two Revolutions*. Princeton University Press.

Acemoglu, Daron, and James A. Robinson. 2006. *Economic Origins of Dictatorship and Democracy*. Cambridge University Press.

Alesina, Alberto, and Roberto Perotti. 1996. "Income Distribution, Political Instability, and Investment." *European Economic Review* 40(6): 1203-1228.

Algan, Yann, Sergei Guriev, Elias Papaioannou, and Evgenia Passari. 2017. "The European Trust Crisis and the Rise of Populism." *Brookings Papers on Economic Activity* 2017(2): 309-400.

Ansell, Ben. 2014. "The Political Economy of Ownership: Housing Markets and the Welfare State." *American Political Science Review* 108(2): 383-402.

Bail, Christopher A., et al. 2018. "Exposure to Opposing Views on Social Media Can Increase Political Polarization." *Proceedings of the National Academy of Sciences* 115(37): 9216-9221.

Beissinger, Mark R. 2002. *Nationalist Mobilization and the Collapse of the Soviet State*. Cambridge University Press.

Bellemare, Marc F. 2015. "Rising Food Prices, Food Price Volatility, and Social Unrest." *American Journal of Agricultural Economics* 97(1): 1-21.

Benkler, Yochai, Robert Faris, and Hal Roberts. 2018. *Network Propaganda*. Oxford University Press.

Bermeo, Nancy. 2016. "On Democratic Backsliding." *Journal of Democracy* 27(1): 5-19.

Boxell, Levi, Matthew Gentzkow, and Jesse M. Shapiro. 2017. "Greater Internet Use Is Not Associated with Faster Growth in Political Polarization." *Proceedings of the National Academy of Sciences* 114(40): 10612-10617.

Boxell, Levi, Matthew Gentzkow, and Jesse M. Shapiro. 2022. "Cross-Country Trends in Affective Polarization." *Review of Economics and Statistics* 106(2): 557-565.

Brinton, Crane. 1938. *The Anatomy of Revolution*. Vintage Books.

Campante, Filipe R., and Davin Chor. 2012. "Why Was the Arab World Poised for Revolution?" *Journal of Economic Perspectives* 26(2): 167-188.

Cavallo, Alberto, Guillermo Cruces, and Ricardo Perez-Truglia. 2017. "Inflation Expectations, Learning, and Supermarket Prices." *American Economic Journal: Macroeconomics* 9(3): 1-35.

Cederman, Lars-Erik, Kristian S. Gleditsch, and Halvard Buhaug. 2013. *Inequality, Grievances, and Civil War*. Cambridge University Press.

Chenoweth, Erica, and Maria J. Stephan. 2011. *Why Civil Resistance Works*. Columbia University Press.

Chetty, Raj, et al. 2020. "Race and Economic Opportunity in the United States." *Quarterly Journal of Economics* 135(2): 711-783.

Clark, David, and Patrick Regan. 2016. Mass Mobilization Protest Data. Harvard Dataverse.

Collier, Paul, and Anke Hoeffler. 2004. "Greed and Grievance in Civil War." *Oxford Economic Papers* 56(4): 563-595.

Dalton, Russell J. 2004. *Democratic Challenges, Democratic Choices*. Oxford University Press.

Davies, James C. 1962. "Toward a Theory of Revolution." *American Sociological Review* 27(1): 5-19.

De Bromhead, Alan, Barry Eichengreen, and Kevin H. O'Rourke. 2013. "Political Extremism in the 1920s and 1930s." *Economic Journal* 123(571): F371-F406.

Fearon, James D., and David D. Laitin. 2003. "Ethnicity, Insurgency, and Civil War." *American Political Science Review* 97(1): 75-90.

Fetzer, Thiemo. 2019. "Did Austerity Cause Brexit?" *American Economic Review* 109(11): 3849-3886.

Foa, Roberto Stefan, and Yascha Mounk. 2016. "The Danger of Deconsolidation." *Journal of Democracy* 27(3): 5-17.

Foran, John. 2005. *Taking Power*. Cambridge University Press.

Funke, Manuel, Moritz Schularick, and Christoph Trebesch. 2016. "Going to Extremes." *European Economic Review* 88: 227-260.

Gatrell, Peter. 2005. *Russia's First World War*. Pearson.

Gentzkow, Matthew, and Jesse M. Shapiro. 2010. "What Drives Media Slant?" *Econometrica* 78(1): 35-71.

Georgescu, Petru A. 2023. "Structural-Demographic Theory Revisited." *PLoS ONE* 18(11): e0294030.

Ginsburg, Tom, and Aziz Z. Huq. 2018. *How to Save a Constitutional Democracy*. University of Chicago Press.

Goldstone, Jack A. 1991. *Revolution and Rebellion in the Early Modern World*. University of California Press.

Goldstone, Jack A., et al. 2010. "A Global Model for Forecasting Political Instability." *American Journal of Political Science* 54(1): 190-208.

Gonzalez-Bailon, Sandra, et al. 2011. "The Dynamics of Protest Recruitment through an Online Network." *Scientific Reports* 1: 197.

Granovetter, Mark. 1978. "Threshold Models of Collective Behavior." *American Journal of Sociology* 83(6): 1420-1443.

Grumbach, Jacob M. 2023. "Laboratories of Democratic Backsliding." *American Political Science Review* 117(3): 967-984.

Gurr, Ted Robert. 1970. *Why Men Rebel*. Princeton University Press.

Haggard, Stephan, and Robert Kaufman. 2021. *Backsliding*. Cambridge University Press.

Hanson, Jonathan K., and Rachel Sigman. 2021. "Leviathan's Latent Dimensions." *Journal of Politics* 83(4): 1495-1510.

Huntington, Samuel P. 1991. *The Third Wave*. University of Oklahoma Press.

Iyengar, Shanto, Gaurav Sood, and Yphtach Lelkes. 2012. "Affect, Not Ideology." *Public Opinion Quarterly* 76(3): 405-431.

Iyengar, Shanto, and Sean J. Westwood. 2015. "Fear and Loathing across Party Lines." *American Journal of Political Science* 59(3): 690-707.

Kaufman, Robert, and Stephan Haggard. 2021. Democratic Resilience Workshop Report. IGCC, UC San Diego.

Klandermans, Bert. 1997. *The Social Psychology of Protest*. Blackwell.

Kurzman, Charles. 2004. *The Unthinkable Revolution in Iran*. Harvard University Press.

Lagi, Marco, Karla Z. Bertrand, and Yaneer Bar-Yam. 2011. "The Food Crises and Political Instability in North Africa and the Middle East." *arXiv* 1108.2455.

Levitsky, Steven, and Daniel Ziblatt. 2018. *How Democracies Die*. Crown Publishing.

Lohmann, Susanne. 1994. "The Dynamics of Informational Cascades." *World Politics* 47(1): 42-101.

Loomba, Sahil, et al. 2021. "Measuring the Impact of COVID-19 Vaccine Misinformation." *Nature Human Behaviour* 5: 337-348.

Lynch, Marc. 2012. *The Arab Uprising*. PublicAffairs.

Mann, Thomas E., and Norman J. Ornstein. 2012. *It's Even Worse Than It Looks*. Basic Books.

McAdam, Doug. 1982. *Political Process and the Development of Black Insurgency*. University of Chicago Press.

McCarty, Nolan, Keith T. Poole, and Howard Rosenthal. 2006. *Polarized America*. MIT Press.

McCoy, Jennifer, and Murat Somer. 2019. "Toward a Theory of Pernicious Polarization." *Annals of the American Academy of Political and Social Science* 681(1): 234-271.

McCarthy, John D., and Mayer N. Zald. 1977. "Resource Mobilization and Social Movements." *American Journal of Sociology* 82(6): 1212-1241.

Mian, Atif, Amir Sufi, and Francesco Trebbi. 2014. "Resolving Debt Overhang." *American Economic Journal: Macroeconomics* 6(2): 1-28.

Mounk, Yascha. 2018. *The People vs. Democracy*. Harvard University Press.

Muller, Edward N. 1985. "Income Inequality, Regime Repressiveness, and Political Violence." *American Sociological Review* 50(1): 47-61.

Norris, Pippa. 2011. *Democratic Deficit*. Cambridge University Press.

Norris, Pippa. 2014. *Why Electoral Integrity Matters*. Cambridge University Press.

Norris, Pippa, and Ronald Inglehart. 2019. *Cultural Backlash*. Cambridge University Press.

Passarelli, Francesco, and Giacomo Del Ponte. 2020. "Prospect Theory and Political Behavior." *Oxford Research Encyclopedia of Politics*.

Piketty, Thomas. 2014. *Capital in the Twenty-First Century*. Harvard University Press.

Piketty, Thomas, and Emmanuel Saez. 2003. "Income Inequality in the United States." *Quarterly Journal of Economics* 118(1): 1-41.

Putnam, Robert D. 2000. *Bowling Alone*. Simon & Schuster.

Reinhart, Carmen M., and Kenneth S. Rogoff. 2009. *This Time Is Different*. Princeton University Press.

Saez, Emmanuel, and Gabriel Zucman. 2016. "Wealth Inequality in the United States since 1913." *Quarterly Journal of Economics* 131(2): 519-578.

Skocpol, Theda. 1979. *States and Social Revolutions*. Cambridge University Press.

Stephanopoulos, Nicholas O., and Eric M. McGhee. 2015. "Partisan Gerrymandering and the Efficiency Gap." *University of Chicago Law Review* 82(2): 831-900.

Stewart, Frances. 2008. *Horizontal Inequalities and Conflict*. Palgrave Macmillan.

Stiglitz, Joseph E. 2012. *The Price of Inequality*. W.W. Norton.

Sunstein, Cass R. 2001. *Republic.com*. Princeton University Press.

Tarrow, Sidney. 1994. *Power in Movement*. Cambridge University Press.

Tucker, Joshua A. 2007. "Enough! Electoral Fraud, Collective Action Problems, and Post-Communist Colored Revolutions." *Perspectives on Politics* 5(2): 535-551.

Tufekci, Zeynep. 2017. *Twitter and Tear Gas*. Yale University Press.

Turchin, Peter. 2003. *Historical Dynamics*. Princeton University Press.

Turchin, Peter. 2020. "Dynamics of Political Instability in the United States." *Cliodynamica*.

Turchin, Peter. 2023. *End Times*. Penguin.

Urdal, Henrik. 2006. "A Clash of Generations?" *International Studies Quarterly* 50(3): 607-629.

Uscinski, Joseph E., and Joseph M. Parent. 2014. *American Conspiracy Theories*. Oxford University Press.

V-Dem Institute. 2023. *Democracy Report 2023*. University of Gothenburg.

Vosoughi, Soroush, Deb Roy, and Sinan Aral. 2018. "The Spread of True and False News Online." *Science* 359(6380): 1146-1151.

Walter, Barbara F. 2022. *How Civil Wars Start*. Crown Publishing.

Wickham-Crowley, Timothy P. 1992. *Guerrillas and Revolution in Latin America*. Princeton University Press.
