# Revolution Indicator Metrics: Comprehensive Data Source Inventory

## Framework Overview

This document catalogs every measurable metric identified across the academic literature for predicting revolutionary instability and societal breakdown. Metrics are organized into thematic categories, each subdivided into:

- **Data Available** — Public, regularly updated datasets with established methodology
- **Data Partially Available** — Proxies exist, data is intermittent, paywalled, or requires construction from multiple sources
- **Data Unavailable / Requires Original Research** — No established public dataset; would need novel measurement, survey design, or qualitative assessment

### Key Academic Frameworks Referenced

| Framework | Author(s) | Core Contribution |
|---|---|---|
| Political Instability Task Force (PITF) | Goldstone et al. (2010) | 4-variable model with 80%+ accuracy at 2-year lead time |
| Structural-Demographic Theory (SDT) | Peter Turchin | Multiplicative PSI = MMP x EMP x SFD |
| Fragile States Index (FSI) | Fund for Peace | 12 indicators across cohesion, economic, political, social |
| Why Civil Resistance Works | Chenoweth & Stephan | 3.5% mobilization threshold, 4 success factors |
| Preference Falsification | Timur Kuran | Hidden dissent, cascade thresholds, surprise revolutions |
| Food Price / Instability Link | Lagi, Bar-Yam et al. | FAO Food Price Index > 210 threshold for deadly conflict |
| Horizontal Inequalities | Cederman, Wimmer, Min | Between-group inequality as primary civil war driver |
| Fourth-Generation Revolution Theory | Goldstone (2001, 2024) | Structure + agency + ideology + coalition dynamics |
| J-Curve Theory | James C. Davies | Trajectory reversal after improvement = peak danger |
| Regime Type & Instability | Polity Project / PITF | Anocracies 10x more unstable than democracies |

---

## 1. ECONOMIC PRESSURE INDICATORS

### 1.1 Income & Wealth Distribution

#### Data Available

| Metric | Description | Data Source(s) | Update Frequency | Geographic Coverage |
|---|---|---|---|---|
| Gini Coefficient | Measures vertical income inequality on 0-1 scale | World Bank (SI.POV.GINI); OECD Income Distribution Database; U.S. Census Bureau | Annual | Global (World Bank: 170+ countries); U.S. (Census) |
| Palma Ratio | Ratio of top 10% income share to bottom 40% income share; better captures extremes than Gini | World Bank; OECD; World Inequality Database (WID) | Annual | Global (100+ countries) |
| Top 1% / 0.1% Income & Wealth Share | Concentration of wealth at the very top; Turchin's key "wealth pump" metric | World Inequality Database (WID.world); Piketty/Saez/Zucman data; Federal Reserve Distributional Financial Accounts | Annual | 100+ countries (WID); U.S. detailed (Fed) |
| Labor Share of GDP | Proportion of national income going to workers vs. capital owners; Turchin's "relative wages" | OECD; BLS (U.S.); Penn World Table; ILO ILOSTAT | Annual | OECD countries; Global (ILO) |
| CEO-to-Median-Worker Pay Ratio | Ratio of CEO compensation to median employee pay; visceral proxy for elite extraction | AFL-CIO Executive Paywatch; Economic Policy Institute (EPI); SEC disclosures (U.S. public companies since 2018) | Annual | U.S. primarily; UK (High Pay Centre) |
| Income by Quintile / Decile | Distribution of income across population segments | U.S. Census Bureau Current Population Survey; World Bank PovcalNet; Eurostat | Annual | U.S.; Global; EU |
| Poverty Rate (Absolute & Relative) | Share of population below poverty threshold | World Bank ($2.15/day international); U.S. Census (official poverty measure & Supplemental Poverty Measure); OECD | Annual | Global |

#### Data Partially Available

| Metric | Description | Potential Source(s) | Limitations |
|---|---|---|---|
| Horizontal Inequalities (Between-Group) | Income/wealth gaps between racial, ethnic, religious, or regional groups — distinct from Gini | U.S. Census (by race); V-Dem Exclusion indices; Minorities at Risk (MAR) dataset (discontinued 2010, partially updated) | MAR discontinued; most datasets don't cross-tabulate income by ethnic group consistently across countries; requires construction from microdata |
| Wealth Mobility / Shorrocks Index | Whether current inequality is permanent or temporary | Panel Study of Income Dynamics (PSID); EU-SILC longitudinal data | Requires multi-year panel data; not available as a pre-computed index for most countries |
| Real Wage Growth by Quintile (Inflation-Adjusted) | Whether wage gains are reaching the bottom or only the top | BLS Real Earnings data; EPI State of Working America | Available for U.S.; inconsistent methodology across countries; inflation adjustment choices affect results |

#### Data Unavailable / Requires Original Research

| Metric | Description | Why It Matters | Measurement Challenge |
|---|---|---|---|
| Perceived Inequality vs. Actual Inequality Gap | The difference between how unequal people *think* society is and how unequal it *actually* is | Perceived inequality may drive behavior more than actual inequality; large gaps indicate narrative manipulation or information failure | Requires paired survey + statistical data; some academic studies exist but no ongoing tracking |
| Subjective Relative Deprivation Index | Individual-level feeling of being worse off than a reference group | Gurr's relative deprivation theory: revolution risk depends on *felt* deprivation, not objective conditions | Requires purpose-built surveys; reference group varies by individual |

---

### 1.2 Employment & Opportunity

#### Data Available

| Metric | Description | Data Source(s) | Update Frequency | Geographic Coverage |
|---|---|---|---|---|
| Youth Unemployment Rate (Ages 15-24) | Share of labor force aged 15-24 that is unemployed | ILO ILOSTAT; World Bank; BLS (U.S.); Eurostat | Monthly/Quarterly | Global (ILO: 180+ countries) |
| Youth Bulge Ratio | Share of total population aged 15-29 | UN Population Division World Population Prospects; World Bank Population Estimates | Annual (projections available decades ahead) | Global |
| NEET Rate | Youth Not in Education, Employment, or Training | OECD; ILO; Eurostat; BLS (U.S.) | Annual/Quarterly | OECD; EU; select developing countries |
| Overall Unemployment Rate | Total unemployment as % of labor force | ILO; BLS; national statistical offices | Monthly | Global |
| Long-Term Unemployment Rate | Unemployed for 27+ weeks (U.S.) or 12+ months (OECD) as share of total unemployed | BLS; OECD; Eurostat | Monthly/Quarterly | U.S.; OECD; EU |
| Labor Force Participation Rate | Share of working-age population in labor force; captures discouraged workers who stop looking | BLS; ILO; World Bank | Monthly | Global |
| Underemployment Rate (U-6) | Includes part-time for economic reasons and marginally attached workers | BLS U-6 measure (U.S.); ILO composite measures | Monthly (U.S.) | U.S. detailed; limited international comparability |

#### Data Partially Available

| Metric | Description | Potential Source(s) | Limitations |
|---|---|---|---|
| Graduate/Degree-Holder Unemployment Rate | Unemployment among those with bachelor's degree or higher — key elite overproduction proxy | BLS Current Population Survey (by education); Eurostat; national labor force surveys | Available for U.S. and EU; not consistently tracked in developing countries; definitions of "graduate" vary |
| Skill Mismatch / Overqualification Rate | Workers in jobs below their qualification level | OECD Skills for Jobs database; European Skills and Jobs Survey | Methodology varies; subjective vs. objective measures differ; limited developing country data |
| Informal Employment Share | % of workforce in informal/unregulated economy | ILO (estimates for 100+ countries) | Inherently hard to measure; methodologies inconsistent; data often several years old |

#### Data Unavailable / Requires Original Research

| Metric | Description | Why It Matters | Measurement Challenge |
|---|---|---|---|
| Aspiration-Attainment Gap | Difference between career expectations (formed during education) and actual outcomes | Frustrated expectations are more destabilizing than low expectations that are met; directly maps to elite overproduction | Requires longitudinal survey pairing educational aspirations with career outcomes years later |
| Hope Index / Future Expectation | Whether people believe their children will be better off | Forward-looking despair may matter more than current conditions | Some survey data exists (Gallup) but not standardized as an instability metric |

---

### 1.3 Cost of Living & Material Wellbeing

#### Data Available

| Metric | Description | Data Source(s) | Update Frequency | Geographic Coverage |
|---|---|---|---|---|
| Consumer Price Index (CPI) / Inflation Rate | Overall price level changes | BLS (U.S.); national statistical offices; IMF; World Bank | Monthly | Global |
| Food Price Index | International food commodity prices | FAO Food Price Index; USDA Economic Research Service; national CPI food components | Monthly | Global (FAO); National |
| Housing Affordability Ratio | Median home price or rent to median household income | FRED Housing Affordability Index; OECD Affordable Housing Database; National Association of Realtors (U.S.) | Monthly/Quarterly | U.S.; OECD |
| Rent Burden Rate | % of renters paying >30% of income on rent | U.S. Census American Community Survey; OECD; Eurostat | Annual | U.S.; OECD; EU |
| Energy Price Index | Gasoline, electricity, heating fuel costs | EIA (U.S.); IEA; Eurostat | Monthly | U.S.; Global |
| Household Debt-to-Income Ratio | Total household debt relative to disposable income | Federal Reserve (U.S.); OECD; BIS | Quarterly | U.S.; OECD; 40+ countries (BIS) |
| Infant Mortality Rate | Deaths under age 1 per 1,000 live births; PITF uses as proxy for governance quality | World Bank; WHO; UNICEF; CDC (U.S.) | Annual | Global |
| Real Median Household Income | Inflation-adjusted income at the 50th percentile | U.S. Census Bureau; OECD | Annual | U.S.; OECD |

#### Data Partially Available

| Metric | Description | Potential Source(s) | Limitations |
|---|---|---|---|
| Food Expenditure Share by Income Quintile | % of income spent on food by poorest households; captures who actually feels food price spikes | USDA Economic Research Service; BLS Consumer Expenditure Survey; FAO | Available for U.S.; inconsistent in developing countries; survey-based with lags |
| Essential Commodity Price Volatility Index | Rate of price change (not just level) for food, energy, housing combined | Constructible from CPI components, FAO, EIA data | No pre-built composite index; requires construction; weighting choices are subjective |
| Healthcare Cost Burden | Out-of-pocket medical costs as % of income | CMS (U.S.); WHO Global Health Expenditure Database | Methodologies vary widely; out-of-pocket vs. total burden definitions differ |

#### Data Unavailable / Requires Original Research

| Metric | Description | Why It Matters | Measurement Challenge |
|---|---|---|---|
| "Felt" Cost-of-Living Pressure Index | Composite subjective measure of financial stress across necessities | Objective metrics may miss regional variation and household composition effects; people revolt based on *felt* hardship | Would require regular nationwide survey with standardized methodology |
| J-Curve Reversal Detector | Identifies when a period of material improvement is followed by sharp decline | Davies' theory: this trajectory reversal is the most dangerous pattern for revolution | Requires algorithmic detection across multiple economic time series simultaneously; threshold calibration is unresolved |

---

### 1.4 Social Mobility

#### Data Available

| Metric | Description | Data Source(s) | Update Frequency | Geographic Coverage |
|---|---|---|---|---|
| Intergenerational Income Elasticity | How much parental income predicts children's income (0 = full mobility, 1 = none); the "Great Gatsby Curve" | Chetty et al. Opportunity Insights; World Bank GDIM; OECD | Periodic (major studies every few years) | U.S. (county-level); 80+ countries (World Bank) |
| Homeownership Rate by Age Cohort | Generational comparison of asset accumulation | U.S. Census Bureau; Eurostat; national housing surveys | Annual | U.S.; EU |
| College Wage Premium | Income difference between degree holders and non-degree holders | BLS; EPI; Federal Reserve | Annual | U.S. primarily; OECD |
| Income Quintile Transition Rates | Probability of moving from one income quintile to another within a generation | Panel Study of Income Dynamics (PSID); Opportunity Insights | Periodic | U.S. primarily |

#### Data Partially Available

| Metric | Description | Potential Source(s) | Limitations |
|---|---|---|---|
| Wealth Mobility (Not Just Income) | Intergenerational transmission of wealth (property, inheritance, financial assets) | Survey of Consumer Finances (Fed); academic studies (Pfeffer, Killewald) | Much harder to measure than income mobility; wealth is hidden and underreported; limited longitudinal data |
| Geographic Mobility as Proxy | Ability to move to opportunity (declining in U.S. since 1980s) | Census migration data; IRS Statistics of Income migration data | Available but interpretation as mobility metric is indirect |

---

## 2. ELITE DYNAMICS INDICATORS

### 2.1 Elite Overproduction

#### Data Available

| Metric | Description | Data Source(s) | Update Frequency | Geographic Coverage |
|---|---|---|---|---|
| Bachelor's Degree Attainment Rate | % of population with bachelor's degree or higher | U.S. Census; OECD Education at a Glance; UNESCO | Annual | U.S.; OECD; Global |
| Graduate/Professional Degree Production | Annual number of JDs, MBAs, PhDs, MDs produced | NCES Integrated Postsecondary Education Data System (IPEDS); ABA (law); AAMC (medicine) | Annual | U.S. primarily |
| Lawyers Per Capita | Number of licensed attorneys per 100,000 population | American Bar Association; national bar associations | Annual | U.S.; many countries |
| Student Loan Debt Total & Per Borrower | Aggregate and individual educational debt burden | Federal Reserve; Department of Education; NY Fed Consumer Credit Panel | Quarterly | U.S. |
| Millionaire/Decamillionaire Household Count | Number of households with $1M+ / $10M+ net worth; Turchin tracked this as elite expansion metric | Federal Reserve Survey of Consumer Finances; Credit Suisse Global Wealth Report; Capgemini World Wealth Report | Annual/Triennial | U.S.; Global |

#### Data Partially Available

| Metric | Description | Potential Source(s) | Limitations |
|---|---|---|---|
| Elite Aspirant-to-Position Ratio | Number of qualified candidates per available elite position (executive roles, political seats, prestigious jobs) | Constructible from BLS Occupational Outlook + IPEDS degree production + political candidate filing data | No pre-built index; "elite position" definition is subjective; requires combining multiple datasets |
| Political Candidate-to-Seat Ratio | Number of candidates filing for office per available seat | FEC (federal); state election commissions | Available for U.S. but fragmented across jurisdictions; no single compiled dataset |
| Campaign Spending Growth | Total and per-race spending growth as proxy for elite competition intensity | OpenSecrets/FEC (U.S.) | U.S. only; spending doesn't always map to competition |

#### Data Unavailable / Requires Original Research

| Metric | Description | Why It Matters | Measurement Challenge |
|---|---|---|---|
| Counter-Elite Formation Index | Rate at which frustrated elite aspirants create alternative power structures (new media outlets, political organizations, parallel institutions) | Turchin identifies counter-elite mobilization as the bridge between structural pressure and actual instability | Would require tracking organizational formation rates, alternative media growth, elite defections to opposition; no established methodology |
| Elite Consensus Index | Degree to which elites agree on basic rules of the game vs. treating politics as zero-sum | Elite consensus breakdown is the final stage before instability in Turchin's model | Would require elite surveys or content analysis of elite discourse; extremely difficult to operationalize |
| Intra-Elite Conflict Intensity | Distinct from mass polarization: measures whether ruling elites are using state power against each other | Factionalism (PITF term) is the #1 risk multiplier; 30x greater instability odds | Partially measurable via impeachment proceedings, investigations of political opponents, judicial weaponization — but no standardized index |

---

### 2.2 Elite Wealth Dynamics

#### Data Available

| Metric | Description | Data Source(s) | Update Frequency | Geographic Coverage |
|---|---|---|---|---|
| Billionaire Count & Wealth Growth | Number of billionaires and total billionaire wealth | Forbes Billionaires List; Bloomberg Billionaires Index; Oxfam annual reports | Annual/Real-time | Global |
| Top 0.1% Income Growth vs. Median Income Growth | Whether elite income is pulling away from the middle | World Inequality Database; Piketty/Saez data; CBO Distribution of Household Income | Annual | U.S.; 100+ countries (WID) |
| Capital Gains as % of Top Income | Share of elite income coming from capital vs. labor | IRS Statistics of Income; CBO | Annual | U.S. |

---

## 3. LEGITIMACY & INSTITUTIONAL TRUST INDICATORS

#### Data Available

| Metric | Description | Data Source(s) | Update Frequency | Geographic Coverage |
|---|---|---|---|---|
| Trust in Federal Government | % who trust government to do the right thing "always" or "most of the time" | Pew Research Center; Gallup; American National Election Studies (ANES) | Ongoing (monthly/quarterly) | U.S. (long time series since 1958) |
| Trust in Institutions (Composite) | Trust in Congress, courts, media, police, military, corporations, etc. | Gallup Confidence in Institutions; Edelman Trust Barometer | Annual | U.S. (Gallup); Global (Edelman: 28 countries) |
| Confidence in Elections | % who believe votes are counted accurately, elections are fair | Gallup; Pew; MIT Election Data + Science Lab | Periodic (around elections) | U.S. primarily; some international (IDEA) |
| Polity Score / Regime Type | -10 (autocracy) to +10 (democracy); anocracy zone (-5 to +5) is the danger zone | Polity5 (Center for Systemic Peace) | Annual | Global (167 countries) |
| V-Dem Liberal Democracy Index | Continuous democracy score incorporating multiple dimensions | Varieties of Democracy (V-Dem) Institute | Annual | Global (202 countries, 1789-present) |
| Freedom House Score | Political rights and civil liberties ratings | Freedom House Freedom in the World | Annual | Global (210 countries/territories) |
| Corruption Perceptions Index (CPI) | Perceived levels of public sector corruption | Transparency International | Annual | Global (180 countries) |
| Judicial Independence Score | Independence of judiciary from political interference | V-Dem; World Justice Project Rule of Law Index | Annual | Global |
| Democratic Backsliding Indicators | Direction and speed of movement on democracy indices | V-Dem annual democracy report; IDEA Global State of Democracy | Annual | Global |

#### Data Partially Available

| Metric | Description | Potential Source(s) | Limitations |
|---|---|---|---|
| Factionalism Index | Whether political competition has become zero-sum with factions using state power against each other | Polity5 factionalism coding (FRACT variable); V-Dem polarization measures | Polity5 codes this but coarsely; difficult to measure in real-time; subjective assessments |
| State-Led Discrimination | Active government discrimination against minority groups; one of PITF's four core variables | Minorities at Risk (MAR) dataset; V-Dem exclusion indicators; CIRI Human Rights Dataset | MAR discontinued in 2010; CIRI ended 2011; V-Dem covers some dimensions but less granular |
| Legislative Responsiveness | Whether legislature acts on issues the public cares about (proxy for accommodation capacity) | Congressional Research Service; GovTrack bill tracking; Stimson's policy mood data | No standardized "responsiveness" index; requires matching public priorities to legislative output |
| Protest Policing Severity | How aggressively police respond to protests | U.S. Protest Event Dataset; Armed Conflict Location & Event Data (ACLED); various NGO trackers | Data collection is reactive and inconsistent; coding depends on media coverage |

#### Data Unavailable / Requires Original Research

| Metric | Description | Why It Matters | Measurement Challenge |
|---|---|---|---|
| Legitimacy Deficit Score | Gap between what citizens expect from government and what they perceive it delivers | Legitimacy deficit, not just low trust, drives instability — expectations matter as much as performance | Would require paired expectations/performance surveys; no established cross-national methodology |
| Institutional Reform Capacity | Speed and willingness of institutions to adapt to public demands | States that make timely concessions prevent cascades (UK Reform Acts, New Deal); this is perhaps the most important stability factor for wealthy democracies | Inherently qualitative; could proxy via time-to-legislation on salient issues, but no established metric |
| Constitutional Crisis Probability | Likelihood of constitutional order being challenged or breaking down | The distinction between "normal politics" and "constitutional crisis" is the threshold that separates instability from revolution | No predictive model exists; historical base rate in the U.S. is extremely low |

---

## 4. SUBJECTIVE WELLBEING & SOCIAL COHESION INDICATORS

#### Data Available

| Metric | Description | Data Source(s) | Update Frequency | Geographic Coverage |
|---|---|---|---|---|
| Life Satisfaction (Cantril Ladder) | 0-10 self-reported life evaluation | World Happiness Report / Gallup World Poll | Annual | Global (150+ countries) |
| Social Trust ("Most People Can Be Trusted") | Interpersonal trust level | World Values Survey; General Social Survey (U.S.); European Social Survey | Every 5 years (WVS); Biennial (GSS) | Global (WVS: 100+ countries) |
| Affective Polarization | Dislike/distrust of opposing political party members | ANES; Pew Political Typology; academic surveys (Iyengar, Boxell et al.) | Periodic | U.S. primarily; growing international data |
| Deaths of Despair | Drug overdose + suicide + alcohol-related mortality | CDC WONDER; Case & Deaton datasets; OECD Health Statistics | Annual | U.S. detailed; OECD |
| Homicide Rate | Intentional homicides per 100,000 population | UNODC; FBI Uniform Crime Reports (U.S.); WHO | Annual | Global (UNODC); U.S. (FBI) |
| Social Isolation / Loneliness | Self-reported loneliness, lack of social connections | U.S. Surgeon General advisory data; Cigna Loneliness Survey; OECD Better Life Index | Periodic | U.S.; OECD |
| Union Membership Density | % of workforce that belongs to a union | BLS (U.S.); OECD; ILO | Annual | U.S.; OECD; Global |
| Religious Participation Rate | Church/mosque/temple attendance and membership | Gallup; Pew Religious Landscape Study; General Social Survey | Periodic | U.S.; Global |
| Civic Organization Membership | Participation in voluntary associations (Putnam's social capital) | General Social Survey; World Values Survey; OECD | Every 2-5 years | U.S.; Global |

#### Data Partially Available

| Metric | Description | Potential Source(s) | Limitations |
|---|---|---|---|
| Ideological Distance Between Parties | How far apart the two major parties are on policy positions | DW-NOMINATE scores (Poole/Rosenthal); Manifesto Project | U.S. well-covered; other countries via Manifesto Project but methodology differs; measures elite polarization, not mass |
| Racial/Ethnic Trust Differentials | Trust gaps between racial or ethnic groups | General Social Survey (some questions); academic studies | Limited time series; sensitive survey topic with social desirability bias |
| Social Media Sentiment / Anger Index | Aggregate emotional tone of political discourse online | Academic projects (various); commercial sentiment APIs | No standardized methodology; platform API access increasingly restricted; bias toward active users |

#### Data Unavailable / Requires Original Research

| Metric | Description | Why It Matters | Measurement Challenge |
|---|---|---|---|
| Cross-Cutting Cleavage Index | Whether identity cleavages (race, class, religion, region, party) align or crosscut | Civil war onset is 12x less probable in societies where cleavages crosscut; aligned cleavages create explosive fault lines | Requires mapping multiple identity dimensions simultaneously; some academic work exists but no ongoing index |
| Collective Identity Fragmentation Score | Whether a society shares a common identity narrative or has fractured into incompatible narratives | Goldstone's 4th-gen theory: revolution requires identity construction; fragmentation can both enable and prevent revolution | Deeply qualitative; could proxy via content analysis of national narratives in media/education |
| Anomie Index | Durkheim's concept of normlessness — breakdown of social norms and shared values | Anomie predates and enables revolutionary mobilization; it measures the "social fabric" deterioration | Classic sociological concept but no established ongoing measurement; would require custom survey instrument |

---

## 5. MOBILIZATION POTENTIAL INDICATORS

#### Data Available

| Metric | Description | Data Source(s) | Update Frequency | Geographic Coverage |
|---|---|---|---|---|
| Protest Event Count & Size | Number and estimated attendance of protest events | ACLED (Armed Conflict Location & Event Data); GDELT; Count Love (U.S.); Mass Mobilization Data | Ongoing/Daily | Global (ACLED); U.S. (Count Love) |
| Social Media Penetration | % of population on major social platforms | DataReportal; Pew Internet surveys; platform filings | Annual | Global |
| Internet Penetration Rate | % of population with internet access | ITU; World Bank; Pew | Annual | Global |
| Smartphone Penetration | % with smartphone access (mobilization tool) | GSMA; Pew; Statista | Annual | Global |
| Strike Activity | Number of work stoppages, workers involved, days idle | BLS Work Stoppage Data (U.S.); ILO; Eurostat | Annual | U.S.; OECD; EU |

#### Data Partially Available

| Metric | Description | Potential Source(s) | Limitations |
|---|---|---|---|
| Protest Diversity Index | Whether protests draw from cross-class, cross-racial, cross-geographic coalitions | Constructible from ACLED / protest datasets with demographic coding | Most protest datasets code location and size but not demographic composition of participants |
| Protest Sustainability / Duration | Average duration of protest campaigns and repeat participation rates | Chenoweth NAVCO dataset (for major campaigns); ACLED (for events) | NAVCO covers major campaigns (300+) but not routine protests; no dataset tracks individual repeat participation |
| Encrypted Communications Adoption | Use of Signal, Telegram, VPNs as organizing tools | App download statistics; academic surveys | Proxy measures only; actual organizing use is invisible by design |
| Peak Mobilization as % of Population | Largest single protest event relative to total population; Chenoweth's 3.5% threshold | Constructible from protest event data + population data | Crowd size estimation is notoriously unreliable; counts vary by 10x between sources |
| Militia / Armed Group Membership | Number of organized armed groups and estimated membership | SPLC; ADL; academic trackers (ACLED) | Inherently covert; estimates vary wildly; definitional challenges (what counts as a "militia"?) |

#### Data Unavailable / Requires Original Research

| Metric | Description | Why It Matters | Measurement Challenge |
|---|---|---|---|
| Preference Falsification Gap | Difference between privately held opinions and publicly expressed opinions; Kuran's key variable | Massive gaps = high cascade potential; this is why revolutions are "surprising" — hidden dissent suddenly reveals itself | Requires comparing anonymous surveys with public opinion data; some experimental methods exist (list experiments, endorsement experiments) but no ongoing tracking |
| Movement Strategic Capacity | Quality of movement leadership, tactical innovation, planning sophistication | Chenoweth: movements that strategize responses to violence and build communication infrastructure are far more successful | Inherently qualitative; no quantitative index exists; would require expert assessment panels |
| Defection Promotion Activity | Whether movements are actively trying to pull security forces or elites to their side | Chenoweth: regime change is 46x more likely when activists promote security force defections | Observable in retrospect but very hard to detect in real-time; coded in NAVCO but only for major campaigns |
| Revolutionary Organization Density | Number and capacity of organizations explicitly seeking regime change | Distinct from protest movements; revolutionary organizations have different structures and goals | Underground organizations are invisible by design; what's visible (rhetoric, propaganda) may not indicate capacity |

---

## 6. STATE CAPACITY & SECURITY FORCE INDICATORS

#### Data Available

| Metric | Description | Data Source(s) | Update Frequency | Geographic Coverage |
|---|---|---|---|---|
| Government Debt-to-GDP Ratio | Total government debt relative to economic output; Turchin's State Fiscal Distress proxy | IMF World Economic Outlook; Federal Reserve FRED; World Bank | Quarterly/Annual | Global |
| Budget Deficit/Surplus as % of GDP | Annual fiscal balance | CBO (U.S.); IMF; OECD | Annual | Global |
| Tax Revenue as % of GDP | State's ability to extract resources; proxy for fiscal capacity | OECD Revenue Statistics; IMF Government Finance Statistics | Annual | Global |
| Government Effectiveness Index | Quality of public services, civil service, policy formulation | World Bank Worldwide Governance Indicators (WGI) | Annual | Global (200+ countries) |
| Rule of Law Index | Confidence in and adherence to rules of society | World Bank WGI; World Justice Project | Annual | Global |
| Military Spending (% of GDP and Total) | Defense expenditure level | SIPRI Military Expenditure Database; World Bank | Annual | Global |
| Police-to-Population Ratio | Number of law enforcement officers per capita | FBI UCR (U.S.); UNODC | Annual | U.S.; select countries |
| Trust in Military | Public confidence in armed forces | Gallup; Pew; World Values Survey | Annual/Periodic | U.S.; Global |
| Trust in Police | Public confidence in law enforcement | Gallup; Pew; Eurobarometer | Annual/Periodic | U.S.; EU |

#### Data Partially Available

| Metric | Description | Potential Source(s) | Limitations |
|---|---|---|---|
| Internal Security vs. External Defense Spending Ratio | Share of security budget devoted to internal control; proxy for regime anxiety | SIPRI; national budget documents; Jane's Defence | Requires disaggregating military vs. internal security budgets, which many countries obscure |
| Crisis Response Effectiveness | Government's track record in responding to natural disasters, pandemics, etc. | FEMA after-action reports; academic assessments; EM-DAT disaster database | No standardized effectiveness metric; assessments are post-hoc and subjective |
| State Capacity Index (Composite) | Ability to collect taxes, deliver services, enforce laws, maintain order | Hanson & Sigman State Capacity Dataset; V-Dem state capacity indicators | Academic datasets with significant lag; definitions of "state capacity" vary across frameworks |
| Parallel Security Force Structures | Existence of competing security services (national guard, federal police, state police, private military) | National organizational charts; academic analyses | Describes U.S. structure well (highly fragmented) but no standardized cross-national index |

#### Data Unavailable / Requires Original Research

| Metric | Description | Why It Matters | Measurement Challenge |
|---|---|---|---|
| Security Force Internal Cohesion | Whether military/police are internally unified or faction-ridden | Nepstad/Bellin: military behavior during crisis is THE decisive variable for whether pressure becomes regime change | Deeply internal to organizations; requires insider surveys, leaked documents, or expert assessment; highly sensitive topic |
| Officer Corps Political Alignment | Political leanings and factional loyalties of military/police leadership | If security forces are politically divided, they may split rather than act as unified regime defender or unified defector | Extremely sensitive; survey data rare; self-reporting unreliable; academic studies use proxy measures with significant error |
| Security Force Ethnic/Racial Composition vs. Population | Whether security forces mirror or diverge from population demographics | "Ethnic stacking" (overrepresenting regime-loyal groups) increases regime defense but makes security forces targets of resentment | Some data available for U.S. military (DoD demographics); police demographics fragmented across 18,000+ agencies |
| Repression Backfire Probability | Likelihood that state repression will increase rather than decrease mobilization | Backfire occurred in ~50% of cases with broader civil resistance; but predicting which 50% is the challenge | Dependent on movement preparedness, media coverage, moral shock intensity — all difficult to quantify ex ante |
| Accommodation vs. Repression Tendency | Whether regime's default response to dissent is reform/co-optation or force | Accommodation-oriented regimes can absorb much higher pressure levels; repression-oriented regimes are more brittle | Requires historical behavioral coding; partially available via V-Dem responses to dissent variables |

---

## 7. EXTERNAL & GEOPOLITICAL INDICATORS

#### Data Available

| Metric | Description | Data Source(s) | Update Frequency | Geographic Coverage |
|---|---|---|---|---|
| Armed Conflict in Neighboring Countries | Presence and intensity of armed conflict in adjacent states; PITF top-4 predictor | Uppsala Conflict Data Program (UCDP); ACLED; PITF datasets | Annual/Ongoing | Global |
| International Sanctions | Active sanctions regimes targeting a country | UN Security Council; OFAC (U.S.); EU sanctions lists | Ongoing | Global |
| Trade Dependency Concentration | % of trade with any single partner or bloc | UN COMTRADE; World Bank WITS; WTO | Annual | Global |
| Foreign Direct Investment Flows | FDI inflows/outflows as indicator of external economic engagement | UNCTAD; World Bank; IMF Balance of Payments | Annual | Global |
| Refugee/IDP Populations | Refugees produced and hosted; internally displaced persons | UNHCR; IDMC | Annual | Global |
| Bilateral Trade Volume (Contagion Proxy) | Protest contagion spreads most between high-trade-volume partners | UN COMTRADE; World Bank | Annual | Global |

#### Data Partially Available

| Metric | Description | Potential Source(s) | Limitations |
|---|---|---|---|
| Foreign Election Interference Incidents | Documented cases of external interference in domestic elections | Academic databases (Levin's PEIG dataset; various); government intelligence reports | Covert by nature; detection is incomplete; attribution is contested; data lags events by years |
| Diaspora Political Activism | Political mobilization of expatriate/exile communities | No systematic dataset; academic case studies; social media monitoring | Fragmented; no standardized measurement; activity is dispersed across platforms and countries |
| International Demonstration Effect | Whether protests abroad are inspiring domestic mobilization | ACLED; GDELT; academic contagion studies | Requires causal inference methodology to distinguish genuine contagion from coincidence; complex time-series analysis |
| Geopolitical Alignment Stability | Whether a country's alliance/patron relationships are stable or shifting | Expert assessments; SIPRI; Correlates of War alliance data | Largely qualitative; alliance "stability" is subjective; rapid shifts may not appear in annual data |

#### Data Unavailable / Requires Original Research

| Metric | Description | Why It Matters | Measurement Challenge |
|---|---|---|---|
| Covert Regime Change Operations Index | Ongoing covert operations by foreign powers to destabilize government | Between 1946-2000, the U.S. intervened in 81 foreign elections, USSR/Russia in 36; most were covert | By definition unobservable in real-time; only known retrospectively; attribution is contested even after declassification |
| Diaspora Funding Flows to Opposition | Financial transfers from exile communities to domestic opposition movements | Exile funding can sustain movements beyond what domestic conditions alone would support | Flows often use informal channels (hawala, crypto); formal banking data misses most of this |
| Foreign Information Warfare Intensity | Scale of foreign-sponsored disinformation and influence operations targeting a country | Can amplify domestic grievances and create artificial mobilization or paralysis | Detection is technically challenging; attribution is contested; platform cooperation varies |

---

## 8. INFORMATION ENVIRONMENT INDICATORS

#### Data Available

| Metric | Description | Data Source(s) | Update Frequency | Geographic Coverage |
|---|---|---|---|---|
| Press Freedom Index | Media freedom and independence from government/commercial pressure | Reporters Without Borders (RSF) World Press Freedom Index | Annual | Global (180 countries) |
| Internet Freedom Score | Online censorship, surveillance, user rights violations | Freedom House Freedom on the Net | Annual | 70 countries |
| Digital Literacy Rate | Population's ability to critically evaluate online information | OECD PIAAC; Eurostat Digital Skills indicators; national digital literacy surveys | Periodic | OECD; EU; select countries |
| Media Trust (by Political Affiliation) | Divergence in media trust between political groups | Gallup; Pew; Edelman Trust Barometer | Annual | U.S.; Global (Edelman) |
| Social Media Platform Concentration | Market share of dominant social platforms | DataReportal; Statista; platform financial filings | Annual | Global |

#### Data Partially Available

| Metric | Description | Potential Source(s) | Limitations |
|---|---|---|---|
| Disinformation Prevalence / Velocity | Volume and spread speed of false information | Academic studies (Vosoughi et al. MIT); EU DisinfoLab; platform transparency reports | No standardized ongoing measurement; platform data access increasingly restricted; "disinformation" definition contested |
| Algorithmic Amplification of Outrage | Degree to which recommendation algorithms promote divisive content | Platform internal research (occasionally leaked); academic audit studies | Platforms control the data; external measurement is incomplete; methodologies still developing |
| Media Ecosystem Fragmentation | Degree to which different political groups consume entirely different information | Pew media consumption studies; academic media diet research; CrowdTangle (discontinued) | Measurement fragmented; key data source (CrowdTangle) shut down; relies on self-reported media consumption |
| State Narrative Control | Government's ability to shape dominant public narratives | V-Dem media censorship indicators; RSF; academic analyses | Partially captured by press freedom scores; "narrative control" in democracies is more subtle than outright censorship |

#### Data Unavailable / Requires Original Research

| Metric | Description | Why It Matters | Measurement Challenge |
|---|---|---|---|
| Preference Falsification Visibility Index | Whether the information environment allows or suppresses revelation of true preferences | Kuran: revolution timing depends on whether hidden dissent can suddenly become visible; information architecture determines cascade potential | Would require mapping the relationship between information environment characteristics and preference revelation dynamics; no methodology exists |
| Revolutionary Narrative Penetration | How widely a coherent "the system must be replaced" narrative has spread | Goldstone 4th-gen: no revolution without a compelling alternative vision; narrative precedes action | Content analysis at scale is possible (NLP) but defining "revolutionary narrative" vs. "reform narrative" is deeply subjective |
| Radicalization Pipeline Throughput | Rate at which people move from moderate to extreme positions via online pathways | Understanding radicalization velocity helps predict mobilization potential | Requires longitudinal tracking of individual belief trajectories; raises serious privacy and ethics concerns |

---

## 9. DEMOGRAPHIC & ENVIRONMENTAL PRESSURE INDICATORS

#### Data Available

| Metric | Description | Data Source(s) | Update Frequency | Geographic Coverage |
|---|---|---|---|---|
| Population Growth Rate | Annual population change rate | UN Population Division; World Bank; national census bureaus | Annual | Global |
| Urbanization Rate | % of population in urban areas and rate of change | UN World Urbanization Prospects; World Bank | Annual | Global |
| Age Dependency Ratio | Ratio of dependents (0-14, 65+) to working-age population | World Bank; UN Population Division | Annual | Global |
| Net Migration Rate | Immigration minus emigration per 1,000 population | UN; World Bank; national statistics | Annual | Global |
| Water Stress Index | Ratio of water withdrawals to available supply | WRI Aqueduct; FAO AQUASTAT | Annual | Global |
| Natural Disaster Frequency & Impact | Number and severity of climate/geological events | EM-DAT International Disaster Database; NOAA | Ongoing | Global |
| CO2 Emissions / Climate Vulnerability | Exposure to climate change impacts | ND-GAIN Country Index; World Bank Climate Change Portal | Annual | Global |
| Agricultural Productivity Index | Crop yields, agricultural GDP, food self-sufficiency | FAO; USDA; World Bank | Annual | Global |

#### Data Partially Available

| Metric | Description | Potential Source(s) | Limitations |
|---|---|---|---|
| Climate-Driven Internal Migration | Population displacement due to climate events | IDMC; academic studies; FEMA data | Attribution of migration to climate specifically is methodologically challenging; data is fragmented |
| Regional Resource Competition | Competition over water, land, energy between subnational regions | WRI Aqueduct; USGS; state-level resource assessments | Available in pieces but no integrated conflict-risk framing; requires combining datasets |
| Energy Transition Winner/Loser Geography | Which regions gain or lose from fossil fuel to renewable shift | EIA; DOE; academic studies | Projections exist but actual impact data is emerging in real-time; heavily politicized |

#### Data Unavailable / Requires Original Research

| Metric | Description | Why It Matters | Measurement Challenge |
|---|---|---|---|
| Climate Grievance Index | Degree to which populations attribute hardship to government climate policy (or inaction) | Climate as a *political* mobilization trigger depends on whether people connect climate impacts to government failure | Would require surveys linking climate experience to political attribution; some academic work emerging |
| Resource Scarcity Conflict Probability | Likelihood that resource competition escalates to violent conflict | Climate-conflict nexus research suggests this pathway but quantification is highly context-dependent | Causal chain is long (climate -> resource stress -> livelihood impact -> grievance -> conflict); many intervening variables |

---

## 10. TRIGGER SENSITIVITY & CATALYTIC INDICATORS

These metrics don't predict when triggers occur but measure how sensitive the system is to shocks.

#### Data Available

| Metric | Description | Data Source(s) | Update Frequency | Geographic Coverage |
|---|---|---|---|---|
| Electoral Contestation Calendar | Upcoming elections, referendum dates, political transitions | IDEA Election Calendar; national election commissions | Ongoing | Global |
| Commodity Price Volatility (Leading Indicator) | Rate of change in food, energy, essential goods prices | FAO; EIA; commodity futures markets | Daily/Monthly | Global |
| Police Use-of-Force Incidents | Frequency of police killings and excessive force events | Mapping Police Violence (U.S.); Fatal Encounters database; ACLED | Ongoing | U.S. detailed; Global (ACLED) |
| Major Corruption Scandal Frequency | High-profile corruption revelations | Transparency International; media tracking; ICIJ investigations | Ongoing | Global |
| Political Assassination / Violence Events | Targeted political violence incidents | ACLED; Global Terrorism Database (GTD); PITF | Ongoing | Global |

#### Data Partially Available

| Metric | Description | Potential Source(s) | Limitations |
|---|---|---|---|
| "Near-Miss" Event Count | Incidents that almost cascaded into larger unrest but were contained | Constructible from ACLED event data with escalation/de-escalation coding | "Near-miss" is subjective; requires counterfactual judgment about what *could have* escalated; no standardized coding |
| Judicial/Constitutional Crisis Indicators | Constitutional confrontations between branches of government, legitimacy disputes over elections | Legal scholarship; V-Dem judiciary indicators; media tracking | No standardized real-time index; events are unique and context-dependent |
| Pre-Election Violence Indicators | Intimidation, threats, and violence in the period before elections | ACLED election violence tracker; IFES | Available for some countries/elections but not consistently global |

#### Data Unavailable / Requires Original Research

| Metric | Description | Why It Matters | Measurement Challenge |
|---|---|---|---|
| Trigger Sensitivity / Cascade Potential | How close the system is to a tipping point where a small event produces a large cascade | This is the core of Kuran's model: structurally similar societies can have vastly different trigger sensitivities | Would require estimating the distribution of individual "thresholds" for joining collective action; some experimental methods exist but no ongoing measurement |
| Moral Shock Probability | Likelihood of an event occurring that generates widespread outrage | "Moral shocks" (televised brutality, dramatic injustice) are key catalysts; their occurrence is somewhat predictable based on background rates | Background rates (police encounters, corruption investigations) can be estimated but the *shock* depends on media amplification and public receptiveness |
| Preference Revelation Cascade Threshold | The tipping point at which hidden dissent begins revealing itself in a self-reinforcing cascade | Kuran's key theoretical contribution: the cascade threshold determines whether structural pressure becomes actual revolution | Theoretically measurable via anonymous survey techniques but never operationalized as an ongoing index |

---

## 11. TEMPORAL DYNAMICS (Meta-Metrics Applied to All Categories)

These are not standalone metrics but analytical operations applied to the metrics above.

#### Data Available (Constructible from Existing Time Series)

| Meta-Metric | Description | How to Compute | Why It Matters |
|---|---|---|---|
| Rate of Change (1-year, 5-year) | First derivative: how fast is each metric changing? | Simple year-over-year or 5-year moving average change | Velocity of deterioration matters more than absolute level (Gurr's relative deprivation) |
| Acceleration (Second Derivative) | Is the rate of change itself increasing? | Change in rate-of-change over time | Accelerating deterioration is a warning signal |
| J-Curve Detection | Identifying trajectory reversals: improvement followed by sharp decline | Algorithmic detection of trend reversals in key time series | Davies' J-Curve: peak revolution risk comes after hopes are raised then dashed |
| Turchin Secular Cycle Phase | Where in the expansion-stagflation-crisis-depression cycle the society currently sits | Pattern matching against Turchin's historical cycle models; requires multiple indicator trends | Same absolute levels have different implications depending on cycle phase |
| Danger Constellation Flags | When multiple sub-indices simultaneously exceed critical thresholds | Define threshold for each category; flag when 3+ categories exceed simultaneously | Turchin's multiplicative model: interaction between factors matters more than sum |
| Volatility / Standard Deviation | How much each metric is fluctuating (stability of conditions) | Rolling standard deviation of time series | High volatility itself is destabilizing even if the average is moderate |

#### Data Unavailable / Requires Original Research

| Meta-Metric | Description | Why It Matters | Measurement Challenge |
|---|---|---|---|
| Calibrated Threshold Values for Wealthy Democracies | At what levels do these metrics become "dangerous" specifically for countries like the U.S.? | Thresholds derived from developing-country revolutions may not apply to wealthy federal democracies | N-of-1 problem: there are essentially no historical cases of wealthy established democracies experiencing revolution; calibration data does not exist |
| Interaction Effect Coefficients | How much does the combination of two factors amplify risk beyond what each contributes alone? | Turchin's PSI is multiplicative, but the specific interaction terms for modern democracies are unknown | Would require large-N cross-national dataset with interaction terms; rare-event problem makes statistical estimation unreliable |

---

## SUMMARY: DATA AVAILABILITY SCORECARD

| Category | Data Available | Partially Available | Unavailable |
|---|---|---|---|
| 1. Economic Pressure | 19 metrics | 7 metrics | 4 metrics |
| 2. Elite Dynamics | 8 metrics | 3 metrics | 3 metrics |
| 3. Legitimacy & Trust | 9 metrics | 4 metrics | 3 metrics |
| 4. Wellbeing & Cohesion | 9 metrics | 3 metrics | 3 metrics |
| 5. Mobilization Potential | 5 metrics | 5 metrics | 4 metrics |
| 6. State Capacity & Security | 9 metrics | 4 metrics | 5 metrics |
| 7. External & Geopolitical | 6 metrics | 4 metrics | 3 metrics |
| 8. Information Environment | 5 metrics | 4 metrics | 3 metrics |
| 9. Demographic & Environmental | 8 metrics | 3 metrics | 2 metrics |
| 10. Trigger Sensitivity | 5 metrics | 3 metrics | 3 metrics |
| 11. Temporal Dynamics | 6 meta-metrics | — | 2 meta-metrics |
| **TOTAL** | **89 metrics** | **40 metrics** | **35 metrics** |

### Key Takeaways

1. **~89 metrics have established, publicly available data sources** — these can be incorporated immediately into any framework
2. **~40 metrics have partial data** — proxies exist or data requires construction from multiple sources
3. **~35 metrics have no established data source** — these represent genuine frontiers requiring original research, novel survey instruments, or qualitative expert assessment
4. **The hardest-to-measure metrics are often the most theoretically important** — preference falsification, intra-elite conflict, trigger sensitivity, security force internal cohesion, and revolutionary narrative penetration are all identified by the literature as critical variables but remain largely unquantifiable
5. **Temporal dynamics can be computed from existing data** — adding rate-of-change and J-curve detection to available metrics is a high-value, low-cost improvement
