# Framework Assessment: Candidate Theoretical Frameworks

## Purpose

This document provides detailed assessments of candidate theoretical frameworks beyond the three models currently implemented in the Revolution Index codebase (Turchin PSI, Prospect Theory PLI, Financial Stress Pathway). Each framework is evaluated independently on its own merits, with data availability for the US as the primary assessment criterion (locked decision from 02-CONTEXT.md). The question for each framework is: **"Could we build this?"** -- not "Should we build this?" Model selection is Phase 4's job.

These assessments expand the model selection space available to Phase 4 by documenting what the academic literature offers beyond the pre-chosen three models. Together with the dataset inventory (dataset-inventory.md) and the synthesis document (Plan 06), they provide the evidence base for informed model architecture decisions.

**Phase 1 Open Question #6 addressed:** Should Phase 2 explore frameworks beyond these 3 models? **Answer: Yes.** Eight candidate frameworks are assessed below, each with full documentation of theoretical basis, required inputs, validation track record, and -- most importantly -- data availability for the US. Several offer strong complementary or alternative approaches to the existing three models.

**Phase 1 Open Question #7 (partial):** Sensitivity analysis methodologies used by these frameworks are noted where applicable. Key methods identified: COINr variance-based global sensitivity analysis (FSI methodology), bootstrap resampling (PITF), Bayesian measurement models (V-Dem), Monte Carlo simulation (Collier-Hoeffler). The synthesis document (Plan 06) will provide a consolidated sensitivity analysis recommendation.

---

## Assessment Methodology

Each framework is assessed using Pattern 3 from 02-RESEARCH.md:

1. **Theoretical Basis:** Core theory in 2-3 sentences
2. **Required Inputs:** Specific variables the framework needs
3. **Known Limitations:** Documented weaknesses, criticisms from the literature
4. **Validation Track Record:** Where has it been tested? What were the results?
5. **Data Availability for US:** Can the required inputs be measured with available data? (PRIMARY criterion)
6. **Assessment:** Overall viability for this project

Frameworks are assessed independently -- no comparisons against the existing 3 models. Comparison is deferred to Phase 4 model selection.

---

## Candidate Frameworks

### 1. PITF Global Instability Forecasting Model (Goldstone et al., 2010)

**Theoretical Basis:** The Political Instability Task Force model, funded by the CIA since 1994, found that a parsimonious 4-variable model outperforms complex alternatives for predicting state failure. The model is grounded in the finding that regime type -- specifically partial democracies (anocracies) with factionalism -- is the dominant predictor of instability, interacting with development level, ethnic discrimination, and regional conflict contagion. The theoretical logic is that institutional incoherence (mixed democratic-autocratic features) combined with identity-based political competition creates structural vulnerability to breakdown (Goldstone et al. 2010).

**Required Inputs:**
- Regime type classification (5 categories: full autocracy, partial autocracy without factionalism, partial autocracy with factionalism, partial democracy without factionalism, partial democracy with factionalism, full democracy)
- Infant mortality rate (proxy for state capacity and development level)
- Ethnic discrimination indicator (state-led discrimination against ethnic minorities)
- Neighborhood conflict indicator (armed conflict in neighboring states)

**Known Limitations:**
- **Developed democracy blindness:** The model was trained on global state failure events dominated by developing countries. The US consistently falls in the "full democracy, low infant mortality" cell, which the model codes as minimal risk. The model has little to say about instability pathways in consolidated democracies (Ulfelder 2012).
- **Categorical coding reduces sensitivity:** Regime type is coded in 5 broad categories. Significant within-category variation (e.g., democratic erosion within the "full democracy" category) is invisible to the model.
- **Infant mortality as proxy:** While infant mortality is an excellent proxy for state capacity in cross-national comparisons, it does not discriminate within the US context -- the US has consistently low infant mortality by global standards, even as other state capacity indicators have deteriorated (Goldstone et al. 2010).
- **Definition of "instability":** The PITF codes state failure events (ethnic wars, revolutionary wars, adverse regime change, genocides/politicides) -- events categorically different from the democratic erosion, political violence, and institutional stress most likely in the US context.
- **Threshold vs. continuous:** The model produces binary onset predictions (instability onset in 2-year window: yes/no), not a continuous risk score.

**Validation Track Record:**
- Out-of-sample accuracy exceeding 80% for 1955-2003 period with 2-year prediction window (Goldstone et al. 2010)
- Sample: 162 countries, thousands of country-years, approximately 200 instability onset cases
- The most rigorously validated political instability model in the literature
- Bootstrap and cross-validation methods used for uncertainty quantification
- Replicated and extended by multiple independent research teams (Ward, Greenhill, Bakke 2010; Hegre et al. 2013)

**Data Availability for US:**
- **Regime type:** Polity5 scores available (1800-present), freely downloadable from the Center for Systemic Peace. V-Dem also provides continuous democracy measures. The US is coded as a full democracy (Polity score 10/10 through most of its history, with some recent debate). `other-data`
- **Infant mortality:** CDC data available via federal APIs, FRED series available. `fed-data`. However, infant mortality does not vary meaningfully within the US context for instability prediction purposes.
- **Ethnic discrimination:** Minorities at Risk (MAR) dataset coded through 2006, now discontinued. V-Dem provides alternative indicators. `other-data`
- **Neighborhood conflict:** UCDP/PRIO Armed Conflict Dataset, freely available. US neighbors (Canada, Mexico) have had limited armed conflict events. `other-data`

**Assessment:** The PITF model's core insight -- that regime type is the single strongest predictor of instability -- is important and well-validated. However, the model is poorly suited for the Revolution Index project as currently specified. The US falls squarely in the "low risk" cell on all four variables, meaning the model would produce a near-zero risk assessment regardless of domestic political stress. The model could contribute specific elements: (a) the factionalism concept could be operationalized as a continuous variable (partisan factionalization) rather than a binary coding, and (b) the regime type dimension could be reconceptualized using V-Dem's continuous measures to detect within-democracy variation. The full model framework, however, would require significant adaptation for the US context.

---

### 2. Fragile States Index (Fund for Peace, 2005-present)

**Theoretical Basis:** The Fragile States Index (FSI, formerly Failed States Index) is built on the premise that state fragility is a multidimensional condition measurable across 12 indicators spanning four dimensions: cohesion, economic, political, and social. The theoretical foundation draws on state capacity literature, development economics, and conflict studies. The FSI treats fragility as a spectrum (not binary), where any country can move toward or away from fragility along multiple dimensions simultaneously. The methodology combines quantitative data with qualitative expert assessment, using a triangulation approach (Fund for Peace 2023).

**Required Inputs:**
- **Cohesion:** Security apparatus (state monopoly on force), factionalized elites (elite fragmentation), group grievance (inter-group tensions)
- **Economic:** Economic decline (GDP, income, inflation), uneven development (Gini, urban-rural gap), human flight/brain drain (emigration)
- **Political:** State legitimacy (public confidence), public services (service delivery capacity), human rights and rule of law (civil liberties, judicial independence, press freedom)
- **Social:** Demographic pressures (population, food, disease), refugees and IDPs
- **Cross-cutting:** External intervention (foreign military, economic, political)

**Known Limitations:**
- **Methodological opacity:** The exact weighting and aggregation methods have been criticized as insufficiently transparent. The Fund for Peace uses a proprietary content analysis tool (Conflict Assessment System Tool, CAST) whose internal mechanics are not fully documented (Ferreira 2017).
- **Expert judgment dependence:** Qualitative inputs introduce subjective variation. Intercoder reliability is not publicly reported.
- **Low sensitivity for stable countries:** The US consistently scores in the "Sustainable" range (35-45 out of 120). The index is designed to differentiate fragile from stable states, not to detect variation within stable states.
- **Annual frequency:** Published once per year, which is too slow for monitoring within-year political stress dynamics.
- **Unclear causal model:** The FSI aggregates indicators that are both causes and consequences of fragility (e.g., "refugees" is both an indicator and a result of state failure), raising endogeneity concerns.

**Validation Track Record:**
- Published annually since 2005 for 178 countries
- The FSI has successfully tracked deterioration in states that subsequently experienced instability (Syria's scores rose steadily before the 2011 civil war; Yemen, South Sudan, and Libya showed deterioration before crises)
- No formal out-of-sample predictive accuracy assessment has been published (in contrast to the PITF model)
- Widely cited in policy and journalism, less in academic political science
- Criticized by academic researchers for conflating description with prediction (Eizenstat, Porter, Weinstein 2005)

**Data Availability for US:**
- **FSI scores themselves:** Freely available at fragilestatesindex.org (2005-present, annual). `other-data`
- **To replicate/adapt the methodology with US-specific data:**
  - Security apparatus: FBI crime data (`fed-data`), but this is a poor proxy for state monopoly on force
  - Factionalized elites: No direct federal data source; could proxy via DW-NOMINATE polarization or partisan conflict measures. `other-data`
  - Economic decline: FRED (GDP, income, CPI). `fed-data`
  - Uneven development: Census income distribution, Gini. `fed-data`
  - State legitimacy: Gallup/Pew trust surveys. `other-data`
  - Public services: Various federal agency data. `fed-data`
  - Human rights/rule of law: V-Dem, Freedom House. `other-data`
  - Demographic pressures: Census, CDC. `fed-data`

**Assessment:** The FSI's 12-indicator framework provides a useful conceptual template for structuring a multidimensional political stress assessment. The specific indicators map well onto available US data sources. However, the FSI itself is not designed to detect variation within stable democracies -- it would not flag meaningful US political stress increases because the US sits at the stable end of the global distribution. The project could adapt the FSI's dimensional structure (cohesion, economic, political, social) while developing US-specific scoring that uses the full range of variation within US historical experience rather than the global distribution. The FSI's normalization methodology (0-10 expert-scaled) is also instructive as a contrast to the project's current min-max approach.

---

### 3. Collier-Hoeffler Greed/Grievance Model (Collier and Hoeffler, 2004)

**Theoretical Basis:** The Collier-Hoeffler model tests whether civil conflict is better predicted by "greed" (economic opportunity for rebellion) or "grievance" (inequality, repression, ethnic tensions). Using cross-national data on civil war onset (1960-1999), they found that greed variables -- particularly primary commodity dependence, low per capita income, and slow economic growth -- dominate grievance variables. The theoretical implication is that civil conflict is more about economic viability of rebellion than about the intensity of popular discontent. A rebel organization needs to be economically viable (able to recruit, fund, and sustain armed opposition) for conflict to occur (Collier and Hoeffler 2004).

**Required Inputs:**
- Primary commodity exports as share of GDP
- Per capita income (in constant USD)
- Economic growth rate
- Male secondary school enrollment (proxy for opportunity cost of rebellion)
- Diaspora population size
- Ethnic fractionalization (Herfindahl index)
- Ethnic dominance (one group > 45-90%)
- Population size and density
- Geographic dispersion of population
- Prior conflict history (peace duration)
- Mountainous terrain percentage

**Known Limitations:**
- **Developed country blindness:** The model was designed for civil war onset in developing countries, particularly resource-dependent economies. The "greed" mechanism (looting natural resources to finance rebellion) is irrelevant for wealthy democracies (Ross 2004).
- **Primary commodity dependence:** The model's strongest predictor -- primary commodity exports/GDP -- is non-discriminating for the US and other advanced economies.
- **Civil war vs. political instability:** The model predicts large-scale civil war onset (1,000+ battle deaths), not democratic erosion, institutional stress, or sub-war political violence. The US has not experienced civil war since 1865.
- **Endogeneity:** Low income may cause conflict, but conflict also causes low income. Collier and Hoeffler use lagged values, but the causal direction remains debated (Fearon 2005).
- **Ethnic fractionalization:** The US has essentially constant ethnic fractionalization at the national level, making this variable non-informative for temporal prediction.

**Validation Track Record:**
- Cross-national sample covering 79 civil wars in 161 countries (1960-1999)
- Logistic regression with temporal controls
- The "greed" finding has been widely replicated (Fearon and Laitin 2003 find similar primacy of income over grievance, though with different interpretive framing)
- Significant academic debate about the interpretation of results -- Cederman, Gleditsch, and Buhaug (2013) argue that the null result for grievance reflects measurement problems, not genuine absence of grievance effects
- No formal out-of-sample testing protocol published

**Data Availability for US:**
- **GDP per capita:** FRED. `fed-data`
- **GDP growth:** FRED/BEA. `fed-data`
- **Primary commodity exports:** Limited US relevance; could construct from BEA trade data but theoretically non-discriminating. `fed-data`
- **School enrollment:** NAEP, Census, College Scorecard. `fed-data`
- **Ethnic fractionalization:** Census racial composition data, but essentially constant at national level. `fed-data`
- **Prior conflict:** UCDP/ACLED. `other-data`

**Assessment:** The Collier-Hoeffler framework is poorly suited for the Revolution Index project. Its core predictive mechanism (natural resource financing of rebellion) does not operate in the US context. The grievance variables it tests (ethnic fractionalization, income inequality) are better measured and theorized in other frameworks (PITF for ethnic dynamics, Alesina-Perotti for middle-class position). The one transferable insight is the primacy of growth deceleration over static inequality -- the model confirms the J-curve tradition's emphasis on change rather than level. This insight is already captured by the prospect theory PLI model. The framework is documented here for completeness but is not recommended for adaptation.

---

### 4. V-Dem Episodes of Regime Transformation (V-Dem Institute, 2013-present)

**Theoretical Basis:** The Varieties of Democracy (V-Dem) project operationalizes democracy as a multidimensional concept with five distinct principles: electoral, liberal, participatory, deliberative, and egalitarian. Rather than collapsing democracy into a single score, V-Dem maintains over 483 indicators coded by country-expert teams, enabling high-resolution measurement of democratic quality over time and across dimensions. The Episodes of Regime Transformation (ERT) framework identifies discrete episodes of autocratization (democratic decline) and democratization, treating regime change as a process rather than an event. The theoretical basis integrates Dahl's polyarchy concept, Linz's democratic breakdown theory, and contemporary democratic erosion research (Coppedge et al. 2023).

**Required Inputs:**
- Electoral democracy indicators (freedom of expression, freedom of association, suffrage, clean elections, elected officials)
- Liberal democracy indicators (judicial independence, legislative constraints, civil liberties)
- Participatory democracy indicators (civil society participation, direct democracy mechanisms)
- Deliberative democracy indicators (reasoned justification, common good orientation)
- Egalitarian democracy indicators (equal distribution of resources, equal access)
- Each indicator coded by 5+ country experts on ordinal scales, aggregated via Bayesian Item Response Theory (IRT)

**Known Limitations:**
- **Expert coding subjectivity:** Despite Bayesian aggregation, expert assessments of concepts like "freedom of expression" inevitably involve subjective judgment. Intercoder agreement varies by indicator (Coppedge et al. 2023).
- **Annual resolution:** V-Dem is coded at the country-year level, unable to detect within-year dynamics.
- **Developed democracy sensitivity:** Small absolute changes in V-Dem scores for countries near the top of the distribution may be within measurement error. The US Liberal Democracy Index declined from approximately 0.89 to approximately 0.72 (2015-2022), which is significant in V-Dem's framework but represents variation in a range where the Bayesian measurement model has relatively less precision.
- **Lag in publication:** V-Dem data typically lags 1-2 years behind the current date, limiting real-time monitoring utility.
- **Expert selection:** V-Dem experts are disproportionately Western academics, which may introduce systematic bias in coding of non-Western countries (but is arguably advantageous for coding the US and peer democracies).

**Validation Track Record:**
- 202 countries coded from 1900 to present (latest release covers through 2023)
- V-Dem has correctly identified autocratization episodes in Hungary, Poland, Turkey, India, and Brazil before these were widely recognized in policy discourse
- ERT methodology has been used in 300+ published academic studies (V-Dem Institute 2023)
- Cross-validated against Polity and Freedom House measures, showing strong convergent validity but greater sensitivity to within-regime variation
- Bayesian IRT measurement model provides uncertainty estimates for all indicators
- No formal predictive accuracy assessment for regime change events (V-Dem is primarily descriptive/diagnostic, not predictive)

**Data Availability for US:**
- **V-Dem dataset:** Freely downloadable from v-dem.net. Comprehensive US coding from 1789 to present. `other-data`
- **Key US-relevant indices available:**
  - Liberal Democracy Index (v2x_libdem): continuous, annual, 1789-present
  - Electoral Democracy Index (v2x_polyarchy): continuous, annual
  - Political polarization (v2cacamps): ordinal expert coding
  - Civil society participation (v2x_cspart): continuous
  - Judicial independence (v2juhcind): continuous
  - Freedom of expression (v2x_freexp_altinf): continuous
  - Executive respect for constitution (v2exrescon): ordinal
- **All indicators freely available** with uncertainty intervals from the Bayesian measurement model

**Assessment:** V-Dem provides the most comprehensive measurement framework for democratic quality available. For the Revolution Index project, V-Dem's value is threefold: (a) it provides long-run time-series of US democratic quality across multiple dimensions, enabling backtesting of the relationship between democratic erosion and other stress indicators; (b) the ERT framework offers a validated methodology for detecting autocratization episodes; and (c) specific V-Dem indicators (judicial independence, legislative constraints, polarization) could serve as direct inputs to a political stress model measuring institutional health. The main adaptation needed is handling the annual frequency limitation -- V-Dem indicators cannot be updated more frequently than annually, which limits their utility for real-time monitoring. This framework is strongly recommended for incorporation in some form.

---

### 5. Korotayev-Medvedev ML Factor Ranking (Korotayev and Medvedev, ~2021-2025)

**Theoretical Basis:** The fifth generation of revolution studies, as characterized by Korotayev, Ustyuzhanin, Grinin, and Fain (2025), uses machine learning methods to empirically rank the relative importance of instability predictors across large cross-national datasets. Rather than beginning with a theoretical framework and testing its predictions, this approach uses gradient boosting, random forests, or similar ML methods to discover which variables have the highest predictive power for instability events in a data-driven manner. The theoretical contribution is the empirical ranking itself: which variables actually predict instability best when the data is allowed to speak without strong theoretical priors (Korotayev et al. 2025)?

**Required Inputs:**
- The ML approach is flexible on inputs -- it ingests a large feature set and ranks them
- Variables tested include: GDP per capita, GDP growth rate, urbanization rate, youth bulge (15-24 as % of population), infant mortality, regime type, ethnic fractionalization, education levels, unemployment, income inequality, and dozens of others
- The method requires a training dataset of instability events with country-year observations

**Known Limitations:**
- **Publication accessibility:** The specific Korotayev-Medvedev ML factor ranking work is primarily available through HSE University (Moscow) publications and working papers. The original papers with full methodological details and ranked variable lists have limited English-language availability. Key findings are referenced in the 2025 review article but the full technical specifications are not independently verified [UNVERIFIED].
- **Training data composition:** ML factor rankings are dependent on the training sample. A model trained primarily on developing-country instability events will rank variables like infant mortality and GDP per capita highly because they discriminate between stable and unstable country-years globally -- but these same variables do not discriminate within the US.
- **Black box criticism:** ML factor importance rankings (e.g., Shapley values, permutation importance) tell you which variables predict outcomes but not why. This makes it difficult to construct a theoretically interpretable stress index.
- **Overfitting risk:** With many variables and relatively few instability events in any dataset, ML approaches risk fitting noise, especially for rare events.
- **US applicability:** Factor rankings derived from cross-national data may not transfer to within-country temporal prediction for a single developed democracy.

**Validation Track Record:**
- Korotayev et al. (2025) report that ML-based approaches improve on traditional models for cross-national instability prediction, though specific accuracy metrics for the Korotayev-Medvedev model are not available in English-language publications
- The general approach (ML for conflict prediction) has been validated in other contexts: Hegre et al. (2019) used gradient boosting for ViEWS conflict forecasting; Muchlinski et al. (2016) used random forests for civil war prediction, though Hegre and Sambanis (2006) showed that simple logistic regression often performs comparably
- The ML approach has NOT been validated for within-country temporal prediction for developed democracies

**Data Availability for US:**
- The ML approach does not specify fixed inputs -- it can use whatever variables are available
- Cross-national datasets (V-Dem, World Bank, FRED for US) provide the feature set
- The challenge is not input availability but the training data: there are no US revolution/instability events to train on
- If using cross-national training, the same global datasets (V-Dem, WDI, PITF) provide both inputs and labels. `other-data`

**Assessment:** The ML factor ranking approach is interesting as a validation tool rather than a primary model architecture for the Revolution Index project. The project's fundamental constraint -- zero labeled revolution events for the US -- makes supervised ML inherently problematic. However, the factor importance rankings from cross-national ML models provide a useful cross-check: if the project's chosen variables align with what ML identifies as important globally, that increases confidence. If not, it raises a productive question about whether the project has missed key predictors. The Korotayev-Medvedev rankings, once fully accessible, could inform variable weighting in Phase 4. The framework is not recommended as a standalone model but as a supplementary evidence source for variable selection.

---

### 6. Funke-Schularick-Trebesch Financial Crisis Model (Funke, Schularick, and Trebesch, 2016)

**Theoretical Basis:** The Funke-Schularick-Trebesch (FST) model establishes the empirical transmission mechanism from systemic financial crises to political extremism in advanced democracies. The core finding is that financial crises produce a persistent rightward shift in voting behavior: far-right vote shares increase by approximately 30% relative to pre-crisis levels in the five years following a systemic financial crisis. The mechanism operates through economic hardship (unemployment, income loss), which generates voter backlash that is channeled disproportionately toward far-right rather than far-left parties. Importantly, normal recessions do NOT produce comparable effects -- the transmission is specific to systemic financial crises (banking crises, credit crunches, asset price collapses) (Funke, Schularick, and Trebesch 2016).

**Required Inputs:**
- Systemic financial crisis indicator (binary: onset/no onset in a given year)
- Election results (vote shares by party family: far-right, far-left, center-right, center-left)
- Government majority size (seat share of governing coalition)
- Parliamentary fractionalization index
- Economic controls: GDP growth, unemployment rate, inflation
- Time since last financial crisis

**Known Limitations:**
- **Financial crisis definition:** The model depends on identifying "systemic financial crises" -- a classification that is clear for major events (2008 GFC) but debatable for borderline cases. The Reinhart-Rogoff (2009) and Laeven-Valencia (2013) crisis databases are the standard references, but coding decisions are non-trivial.
- **20-country advanced economy sample:** The training sample is limited to 20 OECD-type economies (1870-2014). The US is included, but the sample provides limited statistical power for US-specific dynamics.
- **Election-level analysis:** The model operates at the election level, not the continuous country-year level. Between elections, the model has no mechanism for tracking political stress.
- **Lag structure specificity:** The 5-10 year lag between financial crisis and peak political effect is average across the sample. Individual country experiences vary, and the model does not predict lag duration for any specific case.
- **Far-right focus:** The model primarily predicts far-right vote gains. The relationship between financial crises and left-populism, centrist erosion, or democratic backsliding is less clearly specified.
- **Pre-2014 data:** The model was estimated on data through 2014 and does not incorporate the 2016-2024 populist wave that may or may not represent a post-2008 financial crisis political response.

**Validation Track Record:**
- 20 advanced economies, 800+ elections, 1870-2014
- Robust across multiple specifications, time periods, and country subsamples
- The most rigorous empirical study of the financial crisis -> political extremism transmission in the literature
- Replicated and extended by Mian, Sufi, and Trebbi (2014) for financial crises and political polarization
- De Bromhead, Eichengreen, and O'Rourke (2013) found similar patterns for the 1930s specifically
- The 2008 GFC -> 2016 populist wave in multiple countries provides post-publication quasi-validation

**Data Availability for US:**
- **Financial crisis indicator:** Reinhart-Rogoff banking crisis database (freely available), Laeven-Valencia database (IMF). `other-data`
- **Election results:** MIT Election Data + Science Lab, Dave Leip's Atlas, FEC. `fed-data` (FEC) and `other-data`
- **GDP growth:** FRED. `fed-data`
- **Unemployment:** FRED/BLS. `fed-data`
- **Government majority:** Congressional seat shares (publicly available). `other-data`
- **Parliamentary fractionalization:** Computable from election results. `other-data`

**Assessment:** The FST model is directly relevant to the Revolution Index project -- its core finding (financial crises cause persistent political radicalization in advanced democracies, including the US) is exactly the kind of empirical relationship the project aims to capture. The existing Financial Stress Pathway (FSP) model is already inspired by this literature. However, the FST model operates at the election level and cannot provide continuous monitoring. Its primary value for the project is: (a) validating that the FSP model's causal chain is empirically grounded; (b) providing the lag structure (5-10 years) for calibrating when financial stress should produce political stress; and (c) establishing that the relationship is specific to systemic financial crises, not ordinary recessions. This framework strongly supports the existing FSP model's theoretical foundation and may inform its calibration.

---

### 7. Chenoweth Civil Resistance Model (Chenoweth and Stephan, 2011)

**Theoretical Basis:** Based on the most comprehensive dataset of major resistance campaigns (NAVCO), Chenoweth and Stephan found that nonviolent campaigns succeed at twice the rate of violent campaigns (53% vs. 26%) and that campaign participation size is the single strongest predictor of success. The theoretical mechanism is that large, diverse nonviolent campaigns undermine regime pillars of support by: (a) reducing the willingness of security forces to use repression (loyalty shifts), (b) broadening the base of resistance across demographic groups, and (c) increasing the costs of maintaining the status quo for fence-sitting elites. The framework identifies measurable threshold effects -- campaigns mobilizing at least 3.5% of the population have always succeeded, establishing a quantitative benchmark for "critical mass" (Chenoweth and Stephan 2011).

**Required Inputs:**
- Campaign participation rate (% of population actively participating)
- Campaign diversity (cross-demographic breadth of participation)
- Security force loyalty/defection indicators
- Nonviolent discipline maintenance
- Campaign duration and escalation trajectory
- Regime response type (repression, accommodation, combination)

**Known Limitations:**
- **Campaign-level, not country-year:** The unit of analysis is the maximalist campaign (demanding regime change, territorial independence, or ending occupation), not the country-year. This makes the framework unsuitable for continuous monitoring of political stress.
- **Maximalist campaigns only:** NAVCO codes campaigns seeking regime change or equivalent, not routine protest, policy advocacy, or reform movements. The US has had no coded maximalist campaigns in the NAVCO dataset.
- **3.5% threshold debate:** The 3.5% finding is based on campaign success, not campaign emergence. The threshold tells us that campaigns above 3.5% succeed -- it does not tell us when campaigns will emerge or reach that threshold. Ketchley and El-Rayyes (2021) have challenged whether the 3.5% threshold holds for the post-2010 period.
- **Nonviolent focus:** The model's strongest findings apply to nonviolent campaigns. The relationship between violent campaigns and political outcomes is less systematic.
- **Coding difficulty:** Participation rates for historical campaigns are approximate, particularly for pre-survey eras. NAVCO participation estimates rely on media reports, government sources, and secondary analyses.

**Validation Track Record:**
- 323 major campaigns (NAVCO 1.0), 1900-2006; expanded to 389 in NAVCO 1.1 (through 2013)
- 160 covariates tested; participation size is the dominant predictor
- Replicated across time periods, regions, and campaign types
- Extended by Chenoweth (2020) with updated data and analysis of declining success rates for post-2010 campaigns
- NAVCO dataset has generated 50+ published studies building on the original findings
- The framework has been critiqued but not overturned; the core finding (nonviolent > violent, participation size matters) is robust

**Data Availability for US:**
- **Protest participation:** ACLED US data (2020-present) provides event-level protest data with participation estimates. Mass Mobilization Project (1990-2020) provides global protest data including US events. `other-data`
- **Security force loyalty:** No systematic quantitative measure for the US. Qualitative assessments of military/police political neutrality exist but are not time-series data. `unknown`
- **Campaign diversity:** Could be constructed from protest demographic data, but no existing time-series. `unknown`
- **Nonviolent discipline:** Could be coded from ACLED event data (peaceful vs. violent protest), but not pre-existing as a time-series. `other-data`

**Assessment:** The Chenoweth civil resistance model provides theoretically important insights but is not directly operationalizable as a continuous monitoring framework. Its campaign-level unit of analysis does not match the Revolution Index's country-year/country-month monitoring approach. However, two elements are valuable: (a) the 3.5% participation threshold provides a benchmark for assessing whether US protest activity approaches historically consequential levels (current US protest participation is far below this threshold); and (b) the security force loyalty concept identifies a critical variable -- military/police political neutrality -- that other frameworks overlook. The framework is best used as a reference for calibrating mobilization-related variables rather than as a standalone model.

---

### 8. Georgescu SDT for Industrialized Societies (Georgescu, 2023)

**Theoretical Basis:** Georgescu (2023) provides the most directly relevant empirical test of Turchin's structural-demographic theory (SDT) for industrialized societies. Published in PLoS ONE, the study extends SDT beyond its original agricultural-empire context to modern developed economies. Georgescu operationalizes structural-demographic variables with country-specific proxies for 10 industrialized nations and tests whether SDT dynamics (elite overproduction, mass immiseration, state fiscal distress) correlate with instability indicators (political violence, protest, government crises) in the 20th and 21st centuries. The key theoretical contribution is demonstrating that SDT mechanisms operate in modern economies, but with different proxies: education-job mismatch replaces land-based elite competition, cost-of-living pressure replaces subsistence crisis, and government debt replaces tribute extraction failure (Georgescu 2023).

**Required Inputs:**
- **Elite overproduction proxy:** Education-job mismatch -- ratio of advanced degree holders to professional/managerial job openings (a departure from Turchin's income-based proxy)
- **Mass immiseration proxy:** Cost-of-living adjusted wage stagnation -- real wages relative to housing, healthcare, and education costs
- **State fiscal distress proxy:** Government debt trajectory and deficit patterns
- **Instability indicators (dependent variable):** Political violence events, mass protest frequency, government crisis episodes
- Country-specific calibration for each proxy

**Known Limitations:**
- **Single study:** This is one empirical test with a small sample (10 countries). It has not been independently replicated.
- **Correlation, not prediction:** The study tests whether SDT correlates with instability indicators in industrialized societies -- it does not build a predictive model or test out-of-sample forecasting accuracy.
- **Proxy operationalization choices:** The education-job mismatch proxy for elite overproduction is theoretically motivated but debatable. Turchin himself uses income concentration as the primary proxy. Georgescu's choice may be better for the "frustrated aspirant" mechanism but less directly measurable with standard data sources.
- **Dependent variable measurement:** "Instability" in industrialized societies is coded as protest/political violence events, not regime change or state failure. This is appropriate for the US context but makes comparisons with traditional SDT applications difficult.
- **Time coverage:** The study covers primarily 1960-2020, missing the longer historical cycles that Turchin emphasizes (200-300 year secular cycles).

**Validation Track Record:**
- 10 industrialized countries analyzed (including the US)
- Published in PLoS ONE (2023), a peer-reviewed journal
- Found statistically significant correlations between SDT variables and instability indicators across the sample
- Education-job mismatch showed stronger correlation with instability than traditional income inequality measures in several countries
- Has not been independently replicated as of early 2026
- Turchin's blog has referenced the study but has not published a formal response or endorsement

**Data Availability for US:**
- **Education-job mismatch:** Census (educational attainment), BLS (occupational employment statistics, job openings by occupation via JOLTS). Constructing the ratio requires combining Census education data with BLS job opening data -- feasible but not a pre-existing series. `fed-data` (constructible)
- **Cost-of-living adjusted wages:** FRED (real wages), BLS CPI components (housing, healthcare, education). The existing PSI MMP proxy (labor share of GDP) is related but not identical. `fed-data`
- **Government debt trajectory:** FRED (GFDEGDQ188S). Already used in the existing PSI model. `fed-data`
- **Instability indicators:** ACLED (US events), protest event data. `other-data`

**Assessment:** The Georgescu framework is the most directly relevant candidate for the Revolution Index project. It tests the same theoretical family as the existing PSI model (structural-demographic theory) but with operationalizations specifically designed for industrialized societies. The education-job mismatch proxy for elite overproduction is theoretically appealing (it captures the "frustrated aspirant" mechanism more directly than income concentration) and constructible from federal data. This framework is strongly recommended for Phase 4 evaluation as either a replacement for or supplement to the existing PSI operationalization. The key question for Phase 4 is whether the education-job mismatch proxy provides better signal than the current top 1% income share proxy.

---

### 9. Grumbach US State-Level Democracy Index (Grumbach, 2023)

**Theoretical Basis:** Grumbach's framework treats democratic backsliding as a subnational phenomenon in federal systems. Published in the American Political Science Review, Grumbach argues that national-level democracy measures miss the most important variation in US democratic quality, which occurs across states. Using a latent variable model combining multiple indicators (voter registration barriers, gerrymandering severity, campaign finance transparency, civil liberties protections), Grumbach constructs state-level democracy indices and finds significant and growing variation: some US states have become substantially less democratic since 2000 while others have become more democratic. The theoretical basis draws on comparative federalism research and the "laboratories of backsliding" concept -- that democratic erosion in federal systems begins at the subnational level before affecting national institutions (Grumbach 2023).

**Required Inputs:**
- Voter registration restrictions (same-day registration, ID requirements, purge frequency)
- Redistricting methodology (independent commission vs. partisan legislature)
- Campaign finance transparency laws
- Early voting and mail voting access
- Civil liberties protections (state-level LGBTQ+ protections, criminal justice indicators)
- State legislature professionalism and capacity
- Partisan control of state government (trifecta status)

**Known Limitations:**
- **State-level, not national:** The framework produces 50 state-level scores, not a single national score. Aggregating to a national-level indicator requires weighting assumptions (population-weighted? electoral-college-weighted?).
- **US-specific:** Unlike the other frameworks assessed here, Grumbach's model is built for the US and only the US. It cannot be validated against other country experiences.
- **Institutional focus:** The framework measures institutional quality (laws, procedures, barriers) rather than behavioral outcomes (protest, political violence, trust). A state can have strong democratic institutions while its citizens are politically alienated, or vice versa.
- **Controversial coding decisions:** Some variables (e.g., voter ID requirements) are politically contested, and coding them as democratic erosion reflects specific normative commitments that not all scholars share.
- **Limited time depth:** State-level data availability constrains the time series to approximately 2000-present, preventing backtesting against earlier periods.

**Validation Track Record:**
- Published in the American Political Science Review (2023), the discipline's most prestigious journal
- Data covers all 50 states from 2000-2018 (with ongoing updates)
- Found that partisan control (especially Republican trifectas) is the strongest predictor of democratic erosion at the state level
- The finding has been supported by related work from Hacker and Pierson (2020), Grumbach and Hill (2022), and Hertel-Fernandez (2019)
- No formal predictive accuracy assessment (the framework is descriptive/diagnostic)

**Data Availability for US:**
- **Grumbach's state democracy index:** Data available from the author's website and replication repository (Harvard Dataverse). `other-data`
- **To construct/update:**
  - Voter registration data: State election offices, NCSL, `other-data`
  - Redistricting data: Brennan Center for Justice, state redistricting commissions. `other-data`
  - Campaign finance: FEC (federal), state campaign finance agencies. `fed-data` (partial)
  - Partisan control: NCSL, Ballotpedia. `other-data`
- **Aggregation to national score:** Would require combining state scores with population or electoral weighting from Census data. `fed-data` (Census)

**Assessment:** Grumbach's framework offers a unique contribution by capturing the subnational dimension of democratic erosion that all other frameworks miss. The insight that democratic backsliding in the US is primarily happening at the state level is empirically well-supported and theoretically important. For the Revolution Index project, this framework could provide: (a) a state-level democratic health dimension that captures institutional erosion invisible to national-level measures, and (b) a population-weighted national aggregation that tracks whether the average American lives in a more or less democratic state over time. The main challenge is data construction -- the state-level democracy index requires assembling multiple data sources across 50 states, which is more labor-intensive than pulling a single FRED series. This framework is recommended for consideration in Phase 4, particularly as a component of a broader institutional health dimension.

---

## Cross-Cutting Findings

### Sensitivity Analysis Methods Identified (Phase 1 Open Question #7)

The following sensitivity analysis methods were identified across the assessed frameworks:

| Method | Framework(s) | Applicability |
|--------|-------------|---------------|
| Bootstrap resampling | PITF | Well-suited for binary prediction models with defined events |
| Bayesian IRT measurement model | V-Dem | Provides uncertainty intervals for all indicators; captures measurement error |
| Monte Carlo simulation | Collier-Hoeffler | Standard for parametric models with coefficient uncertainty |
| COINr variance-based sensitivity analysis | FSI methodology reference | Designed specifically for composite indicators; Sobol indices for parameter importance ranking |
| Permutation importance / Shapley values | Korotayev-Medvedev ML | ML-specific; identifies which features drive predictions |
| Cross-validation (k-fold, leave-one-out) | PITF, Collier-Hoeffler | Standard for out-of-sample predictive accuracy |

**Recommendation for Phase 4:** The COINr approach (Morris screening for initial parameter reduction, followed by Sobol indices for full global sensitivity analysis) is most appropriate for the Revolution Index project, which is a composite indicator with 50+ parameters. This is documented in the synthesis (Plan 06) for full discussion.

### Data Availability Summary

| Framework | US Data Available | Real-Time Capable | Continuous Score | Recommended |
|-----------|-------------------|-------------------|------------------|-------------|
| PITF | Partial (regime type, mortality; not discrimination, neighborhood) | No (annual, lagged) | No (binary) | Elements only |
| FSI | Yes (most indicators constructible) | No (annual) | Yes (0-120) | Methodology reference |
| Collier-Hoeffler | Partial (economic yes, conflict-specific no) | No | No (binary) | Not recommended |
| V-Dem ERT | Yes (comprehensive US coding) | No (annual, lagged) | Yes (0-1 indices) | Strongly recommended |
| Korotayev-Medvedev ML | Yes (flexible inputs) | Potentially | Yes | Validation tool only |
| Funke-Schularick-Trebesch | Yes (economic data; elections episodic) | No (election-level) | No | Supports existing FSP |
| Chenoweth Civil Resistance | Partial (protest data yes; loyalty/diversity no) | Partial (ACLED events) | No (campaign-level) | Threshold reference |
| Georgescu SDT | Yes (all proxies constructible from fed data) | Yes (fed data series) | Yes (constructible) | Strongly recommended |
| Grumbach State Democracy | Yes (constructible but labor-intensive) | Partial (annual updates) | Yes (state-level) | Recommended |

---

## Bibliography

Alesina, A. and Perotti, R. (1996). Income Distribution, Political Instability, and Investment. *European Economic Review* 40(6): 1203-1228.

Cederman, L., Gleditsch, K.S., and Buhaug, H. (2013). *Inequality, Grievances, and Civil War*. Cambridge University Press.

Chenoweth, E. (2020). The Future of Nonviolent Resistance. *Journal of Democracy* 31(3): 69-84.

Chenoweth, E. and Stephan, M.J. (2011). *Why Civil Resistance Works: The Strategic Logic of Nonviolent Conflict*. Columbia University Press.

Collier, P. and Hoeffler, A. (2004). Greed and Grievance in Civil War. *Oxford Economic Papers* 56(4): 563-595.

Coppedge, M. et al. (2023). V-Dem Codebook v13. Varieties of Democracy (V-Dem) Project.

De Bromhead, A., Eichengreen, B., and O'Rourke, K. (2013). Political Extremism in the 1920s and 1930s: Do German Lessons Generalize? *Journal of Economic History* 73(2): 371-400.

Eizenstat, S., Porter, J.E., and Weinstein, J. (2005). Rebuilding Weak States. *Foreign Affairs* 84(1): 134-146.

Esty, D.C. et al. (1995). State Failure Task Force Report. Science Applications International Corporation.

Fearon, J.D. (2005). Primary Commodity Exports and Civil War. *Journal of Conflict Resolution* 49(4): 483-507.

Fearon, J.D. and Laitin, D.D. (2003). Ethnicity, Insurgency, and Civil War. *American Political Science Review* 97(1): 75-90.

Ferreira, I.A. (2017). Measuring State Fragility: A Review of the Social Science Literature. *Third World Quarterly* 38(5): 1123-1141.

Fund for Peace (2023). Fragile States Index Methodology. fragilestatesindex.org.

Funke, M., Schularick, M., and Trebesch, C. (2016). Going to Extremes: Politics After Financial Crises, 1870-2014. *European Economic Review* 88: 227-260.

Georgescu, S. (2023). Structural-Demographic Theory Revisited: Evidence from Industrialized Societies. *PLoS ONE* 18(11): e0293672.

Goldstone, J.A. (1991). *Revolution and Rebellion in the Early Modern World*. University of California Press.

Goldstone, J.A. et al. (2010). A Global Model for Forecasting Political Instability. *American Journal of Political Science* 54(1): 190-208.

Grumbach, J.M. (2023). Laboratories of Democratic Backsliding. *American Political Science Review* 117(3): 967-984.

Grumbach, J.M. and Hill, C.C. (2022). Rock the Registration: Same Day Registration Increases Turnout of Young Voters. *Journal of Politics* 84(1): 405-417.

Hacker, J.S. and Pierson, P. (2020). *Let Them Eat Tweets: How the Right Rules in an Age of Extreme Inequality*. Liveright.

Hegre, H. et al. (2013). Predicting Armed Conflict, 2010-2050. *International Studies Quarterly* 57(2): 250-270.

Hegre, H. et al. (2019). ViEWS: A Political Violence Early-Warning System. *Journal of Peace Research* 56(2): 155-174.

Hertel-Fernandez, A. (2019). *State Capture: How Conservative Activists, Big Businesses, and Wealthy Donors Reshaped the American States*. Oxford University Press.

Ketchley, N. and El-Rayyes, T. (2021). Unpacking the 3.5% Rule. *International Interactions* 47(4): 668-689.

Korotayev, A., Ustyuzhanin, V., Grinin, L., and Fain, A. (2025). Five Generations of Revolution Studies. *Comparative Sociology* 24(1): 1-45.

Laeven, L. and Valencia, F. (2013). Systemic Banking Crises Database. *IMF Economic Review* 61(2): 225-270.

Luhrmann, A. and Lindberg, S.I. (2019). A Third Wave of Autocratization Is Here. *Democratization* 26(7): 1095-1113.

Mian, A., Sufi, A., and Trebbi, F. (2014). Resolving Debt Overhang: Political Constraints in the Aftermath of Financial Crises. *American Economic Journal: Macroeconomics* 6(2): 1-28.

Muchlinski, D. et al. (2016). Comparing Random Forest with Logistic Regression for Predicting Class-Imbalanced Civil War Onset Data. *Political Analysis* 24(1): 87-103.

Reinhart, C.M. and Rogoff, K.S. (2009). *This Time Is Different: Eight Centuries of Financial Folly*. Princeton University Press.

Ross, M.L. (2004). What Do We Know About Natural Resources and Civil War? *Journal of Peace Research* 41(3): 337-356.

Turchin, P. (2003). *Historical Dynamics: Why States Rise and Fall*. Princeton University Press.

Turchin, P. (2010). Political Instability May Be a Contributor in the Coming Decade. *Nature* 463: 608.

Turchin, P. (2023). *End Times: Elites, Counter-Elites, and the Path of Political Disintegration*. Penguin Press.

Ulfelder, J. (2012). Forecasting State Instability. PITF Global Forecasting Model Update.

V-Dem Institute (2023). Autocratization Changing Nature? Democracy Report 2023. University of Gothenburg.

Ward, M.D., Greenhill, B.D., and Bakke, K.M. (2010). The Perils of Policy by P-Value. *Journal of Peace Research* 47(4): 363-375.
