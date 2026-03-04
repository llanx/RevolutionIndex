# Dataset Inventory: Training and Validation Sources

## Purpose

This document inventories candidate datasets for training and validating political instability models. These datasets are compiled from references across all six domain literature reviews (Plans 01-03) and the framework assessment (Plan 05). For each dataset, we document coverage, access methods, US applicability, and honest assessment of how the dataset could (or could not) be used for the Revolution Index project.

The dataset inventory serves Phase 5 (Validation) by identifying what data exists for backtesting, threshold calibration, and cross-national validation. It serves Phase 4 (Model Building) by clarifying what labeled outcome data is available to evaluate model predictions against.

---

## The Zero-Event Problem

**The US has zero coded revolution events in essentially every political instability dataset.** This is the central constraint for model validation and must be honestly confronted.

In standard ML prediction tasks, a labeled dataset of positive and negative cases enables train/test splits, cross-validation, and performance metrics (precision, recall, AUC). For the Revolution Index, this approach is impossible: the US has not experienced a revolution, successful coup, civil war (since 1865), genocide, or regime change of the kind coded in major instability datasets. The REQUIREMENTS.md document explicitly excludes "ML prediction framing" for this reason.

**What the datasets CAN provide:**

1. **Cross-national threshold calibration:** Datasets like NAVCO and PITF establish what levels of structural stress, mobilization, and institutional erosion have historically preceded instability events in other countries. These thresholds can be used as reference points for interpreting US stress scores -- not as prediction targets, but as "how does the US compare to countries that actually experienced instability?"

2. **Framework validation against known episodes:** The models and frameworks can be tested against historical episodes in other countries (where we have labeled events) to check whether they correctly identify pre-crisis periods. If a model cannot detect elevated stress before the Arab Spring, the Color Revolutions, or the 2008 financial crisis, it should not be trusted for the US either.

3. **US sub-crisis event data:** While the US has no revolution events, it has extensive data on protest events (ACLED, Mass Mobilization Project), political violence incidents, polarization measures (V-Dem, DW-NOMINATE), and governance quality changes. These sub-crisis events can be used to validate whether the Revolution Index detects elevated stress during periods like 1968 (urban riots, assassinations), 1992 (LA riots), 2001 (September 11 aftermath), 2008 (financial crisis), 2020 (BLM/pandemic/election), and 2021 (January 6).

4. **Continuous governance time-series:** V-Dem and Polity provide continuous measures of democratic quality that can be used for backtesting governance-related indicators against the Revolution Index score trajectory.

**What the datasets CANNOT provide:**

- Binary classification labels for US instability onset
- Training data for supervised learning models predicting US revolution
- Ground truth for standard ML evaluation metrics (precision, recall, F1) applied to US-specific predictions
- Validation that the Revolution Index would "predict" a US revolution (there are no positive cases to predict)

---

## Dataset Summary Table

| Dataset | Coverage | Time Period | US Events | Access | Status | Potential Use |
|---------|----------|-------------|-----------|--------|--------|---------------|
| NAVCO 2.1 | 389 campaigns, global | 1945-2013 | 0 campaigns | Free, Harvard Dataverse | Complete | Threshold calibration |
| NAVCO 3.0 | 100K+ events, 21 countries | 1991-2012 | Limited | Free, Harvard Dataverse | Complete | Event-level mobilization analysis |
| Mass Mobilization Project | 162 countries, 17K+ events | 1990-2020 | ~500+ events | Free, Harvard Dataverse | Complete (not updated) | US protest trend validation |
| UCDP/PRIO | 2,500+ conflicts, global | 1946-present | 0 conflicts | Free, ucdp.uu.se | Active, annual | Cross-national threshold reference |
| ACLED | 250+ countries, 1M+ events | 2018-present (US) | 30K+ events | Free (registration), acleddata.com | Active, real-time | US protest/violence monitoring |
| V-Dem | 202 countries, 483 indicators | 1789-present | Full US coding | Free, v-dem.net | Active, annual | Democratic quality backtesting |
| PITF Worldwide Atrocities | Global atrocity events | 1995-2015 | Minimal | Limited access | Discontinued | Limited |
| OMG Dataset | 200+ countries | 1789-2019 | Included | TBD | Recently released | Historical episodes reference |
| Polity5 | 167 countries | 1800-2018 | Full US coding | Free, systemicpeace.org | Final version | Regime type backtesting |
| Reinhart-Rogoff Banking Crises | 70+ countries | 1800-2014 | ~10 US crises | Free, published data | Complete | Financial crisis identification |
| Correlates of War (COW) | Interstate and civil wars | 1816-present | US interstate wars | Free, correlatesofwar.org | Active | Military conflict reference |
| World Values Survey | 100+ countries, 7 waves | 1981-present | US included | Free, worldvaluessurvey.org | Active (Wave 7) | Attitudinal validation |
| American National Election Studies | US only | 1948-present | US only | Free, electionstudies.org | Active, biennial+ | US political attitudes |

---

## Detailed Entries

### 1. NAVCO 2.1 (Nonviolent and Violent Campaigns and Outcomes)

**Full Name and Citation:** Nonviolent and Violent Campaigns and Outcomes (NAVCO) Data Project, version 2.1. Chenoweth, E. and Lewis, O.A. (2013). "Unpacking Nonviolent Campaigns: Introducing the NAVCO 2.0 Dataset." *Journal of Peace Research* 50(3): 415-423. Updated through NAVCO 2.1 by Chenoweth and Shay.

**Coverage:**
- 389 maximalist campaigns (regime change, territorial independence, anti-occupation)
- Global coverage, 1945-2013
- Annual-level observations for each campaign
- Coded variables include: campaign start/end year, peak participation size, violent/nonviolent classification, outcome (success, partial success, failure), security force defections, international sanctions, regime repression level

**Key Variables:**
- Campaign outcome (6-point scale from full success to full failure)
- Peak membership/participation (estimated participants at peak mobilization)
- Violent/nonviolent primary method
- Security force defections (binary: did significant military/police units defect?)
- Campaign diversity (did participation span multiple demographic groups?)
- External state support (did foreign states provide material support?)

**Access Method:**
- URL: https://dataverse.harvard.edu/dataverse/navco
- Download: Direct CSV/Stata download from Harvard Dataverse
- License: CC-BY, free for academic and non-commercial use
- No API; batch download only

**Update Status:**
- Last updated: 2013 (NAVCO 2.1 extends through 2013 campaigns)
- Update frequency: Sporadic (major version updates every 3-5 years)
- Status: Complete dataset for 1945-2013 period; not actively updated for new campaigns

**US Coverage:**
- **Zero US campaigns coded** in NAVCO. The dataset codes maximalist campaigns -- the US has not had a campaign seeking regime change, territorial secession, or ending foreign occupation since 1945.
- The US Civil Rights Movement, Vietnam War protests, and BLM are NOT coded as NAVCO campaigns because they did not seek regime change (they sought policy change within the existing regime).

**Applicability Assessment:**
- **Cannot be used for:** Direct US validation (no US positive cases)
- **Can be used for:** (a) Establishing what participation thresholds have historically preceded successful regime challenges (the 3.5% rule); (b) Cross-national calibration -- what structural conditions were present in countries that did experience maximalist campaigns? (c) Testing whether the Revolution Index framework correctly identifies pre-campaign elevated stress in countries that have NAVCO-coded campaigns.

---

### 2. NAVCO 3.0 (Event-Level Nonviolent and Violent Campaign Data)

**Full Name and Citation:** NAVCO 3.0 Dataset. Chenoweth, E. and Pinckney, J. (2021) [UNVERIFIED specific publication details]. Event-level data for campaigns coded in NAVCO 2.1.

**Coverage:**
- Over 100,000 events within 21 countries
- 1991-2012
- Event-level coding: date, location, participation size, tactic type (demonstration, strike, boycott, riot, etc.), repression response

**Key Variables:**
- Event type (demonstration, strike, riot, sit-in, boycott, blockade, etc.)
- Estimated participation per event
- Repression response (none, arrests, beatings, shootings, etc.)
- Event outcome (concession, repression, no response)
- Organizational affiliation

**Access Method:**
- URL: https://dataverse.harvard.edu/dataverse/navco
- Download: CSV/Stata from Harvard Dataverse
- License: CC-BY
- No API

**Update Status:**
- Last updated: ~2021
- Status: Complete for the 21 countries and 1991-2012 period
- Not actively updated

**US Coverage:**
- **Limited US coverage** -- NAVCO 3.0 codes events within campaigns that are already in the NAVCO 2.1 dataset. Since the US has no NAVCO 2.1 campaigns, US events are coded only if they occurred within the context of a campaign in one of the 21 covered countries.
- Effectively zero US-specific events.

**Applicability Assessment:**
- **Cannot be used for:** US-specific analysis
- **Can be used for:** Understanding event-level mobilization dynamics within campaigns (how campaigns escalate, how repression affects participation, how events cluster temporally) -- these patterns may inform how to interpret US protest event data from ACLED.

---

### 3. Mass Mobilization Project (MMP)

**Full Name and Citation:** Clark, D. and Regan, P. (2016). "Mass Mobilization Protest Data." Harvard Dataverse. Developed at Binghamton University.

**Coverage:**
- 162 countries, 1990-2020
- Over 17,000 protest events
- Coding threshold: protests involving 50+ participants with political demands directed at the government

**Key Variables:**
- Protest event date and country
- Number of participants (estimated)
- Protester demands (coded: labor/wages, land/farm, police brutality, political process, price increases, removal of politician, social restrictions, tax policy)
- State response (ignore, crowd dispersal, arrests, beatings, killings, shootings)
- Protest violence (by protesters: yes/no)

**Access Method:**
- URL: https://massmobilization.github.io/
- Download: CSV from Harvard Dataverse (https://dataverse.harvard.edu/dataverse/MMdata)
- License: Free for academic use
- No API

**Update Status:**
- Last updated: 2020
- Status: **No longer actively maintained** -- the project appears to have concluded
- Coverage through 2020 captures the BLM protests and early COVID-era mobilization

**US Coverage:**
- **Approximately 500+ US events coded** (1990-2020), making this one of the most comprehensive US protest event datasets for this period
- Events include labor strikes, political protests, anti-war demonstrations, BLM events, Occupy Wall Street, Tea Party rallies, Women's March, and other politically directed protests
- Participation estimates available for most events
- State response coded (though US state response is overwhelmingly "ignore" or "crowd dispersal" with limited violence)

**Applicability Assessment:**
- **Directly useful for:** (a) Validating whether the Revolution Index shows elevated scores during periods of high protest frequency (e.g., 2020 BLM peak); (b) Establishing baseline US protest frequency to contextualize any future increases; (c) Tracking the relationship between protest frequency/demands and structural stress indicators
- **Limitation:** Dataset ends in 2020 and is not being updated. For ongoing monitoring, ACLED provides the continuation.
- **The zero-event constraint applies:** The Mass Mobilization Project codes protest events, not revolution events. US protest events are common and do not constitute instability by themselves.

---

### 4. UCDP/PRIO Armed Conflict Dataset

**Full Name and Citation:** Uppsala Conflict Data Program / Peace Research Institute Oslo. Gleditsch, N.P. et al. (2002). "Armed Conflict 1946-2001: A New Dataset." *Journal of Peace Research* 39(5): 615-637. Updated annually.

**Coverage:**
- All armed conflicts globally, 1946-present
- Inclusion threshold: 25+ battle-related deaths in a calendar year
- 2,500+ conflict episodes coded
- Three types: state-based conflict (government vs. organized opposition), non-state conflict (organized groups, neither is government), one-sided violence (organized group vs. civilians)

**Key Variables:**
- Conflict type (interstate, intrastate, intrastate with foreign involvement, extrasystemic)
- Intensity level (minor: 25-999 deaths/year; war: 1,000+ deaths/year)
- Conflict parties (government, rebel group, identity)
- Battle-related deaths (best estimate, low estimate, high estimate)
- Conflict onset, duration, termination type

**Access Method:**
- URL: https://ucdp.uu.se/downloads/
- Download: CSV, Excel, and API access
- API: https://ucdpapi.pcr.uu.se/ (RESTful, free)
- License: Free for academic and non-commercial use
- Well-documented codebook

**Update Status:**
- Last updated: Annually (most recent version typically covers through previous calendar year)
- Status: **Actively maintained** by Uppsala University, Sweden
- Regular annual updates with 1-year lag

**US Coverage:**
- **Zero US intrastate conflicts coded** meeting the 25-death threshold since 1946
- US interstate conflicts coded: Korean War, Vietnam War, Gulf War, Afghanistan, Iraq
- US one-sided violence and non-state conflict: not coded at levels meeting UCDP thresholds
- The January 6 Capitol attack (2021) did not meet the 25-death threshold and is not coded as an armed conflict

**Applicability Assessment:**
- **Cannot be used for:** Direct US instability validation (no US intrastate conflict events)
- **Can be used for:** (a) Cross-national threshold reference -- what levels of political stress preceded armed conflict onset in other countries? (b) Neighborhood conflict variable construction for the PITF model (conflicts in US neighbors, primarily Mexico's drug war); (c) Establishing that the US is an extreme outlier on armed conflict measures, which contextualizes why standard conflict prediction models are poorly suited for the US case
- **Honest assessment:** UCDP's 25-death threshold is too high to capture the forms of political instability most relevant for the US (institutional erosion, political violence below armed conflict thresholds, democratic backsliding).

---

### 5. ACLED (Armed Conflict Location & Event Data Project)

**Full Name and Citation:** Armed Conflict Location & Event Data Project (ACLED). Raleigh, C. et al. (2010). "Introducing ACLED: An Armed Conflict Location and Event Dataset." *Journal of Peace Research* 47(5): 651-660.

**Coverage:**
- Over 250 countries and territories
- Over 1 million events globally
- US coverage from 2020 to present
- No fatality threshold -- codes all politically relevant events including peaceful protests
- Event types: battles, explosions/remote violence, violence against civilians, protests, riots, strategic developments

**Key Variables:**
- Event date, location (lat/long), country, admin regions
- Event type and sub-event type (peaceful protest, violent demonstration, mob violence, etc.)
- Actors involved (named groups, generic categories)
- Fatalities (reported deaths)
- Notes (detailed event description)
- Source citations (media reports used for coding)

**Access Method:**
- URL: https://acleddata.com/
- Download: CSV via ACLED's data export tool (free registration required)
- API: Available for registered users
- License: Free for academic and non-commercial use; registration required
- Updated weekly (near-real-time)

**Update Status:**
- Status: **Actively maintained** with weekly updates
- US coverage began in 2020 and continues to present
- Global coverage varies by region (Africa from 1997, Middle East from 2016, US from 2020)
- Full-time coding team with regional specialists

**US Coverage:**
- **30,000+ US events coded since 2020**, making ACLED the most comprehensive current source of US political event data
- Events include: BLM protests (2020), counter-protests, January 6 Capitol breach (2021), abortion-related protests (2022), labor actions, election-related demonstrations
- Each event has participation estimates (where available), fatality counts, and actor identification
- Sub-event coding distinguishes peaceful protests from violent demonstrations, mob violence, and attacks

**Applicability Assessment:**
- **Directly useful for:** (a) Continuous monitoring of US protest frequency, violence levels, and political event dynamics (aligns with the Revolution Index's monitoring purpose); (b) Validating mobilization-related model components against actual protest activity; (c) Constructing mobilization variables (protest frequency, violent event ratio, geographic spread of contention); (d) Tracking escalation patterns -- are US political events becoming more frequent, more violent, or more geographically concentrated?
- **Limitation:** US coverage only begins in 2020, preventing historical backtesting before that date. For pre-2020 US protest data, the Mass Mobilization Project provides coverage (1990-2020).
- **Strength:** Weekly updates enable the closest-to-real-time political event monitoring available.

---

### 6. V-Dem (Varieties of Democracy)

**Full Name and Citation:** Coppedge, M. et al. (2023). "V-Dem Dataset v13." Varieties of Democracy (V-Dem) Project, University of Gothenburg.

**Coverage:**
- 202 countries
- 483 indicators (lower-level) + 82 indices (higher-level aggregations)
- 1900 to present (some indicators back to 1789 for long-established states)
- 30,000+ country-year observations

**Key Variables:**
- **Electoral democracy index** (v2x_polyarchy): freedom of expression, association, suffrage, clean elections
- **Liberal democracy index** (v2x_libdem): judicial independence, legislative constraints, civil liberties
- **Egalitarian democracy index** (v2x_egaldem): resource equality, access equality
- **Participatory democracy index** (v2x_partipdem): civil society, direct democracy
- **Deliberative democracy index** (v2x_delibdem): reasoned justification, common good
- **Political polarization** (v2cacamps): expert-coded partisan polarization
- **Government censorship** (v2mecenefm): media censorship effort
- **Judicial independence** (v2juhcind): high court independence
- **Civil society participation** (v2x_cspart): civil society organizational density

**Access Method:**
- URL: https://v-dem.net/data/the-v-dem-dataset/
- Download: CSV, R, Stata formats; direct download after registration (free)
- API: R package (vdemdata), Python access via CSV
- License: Free for all uses with citation
- Comprehensive codebook (500+ pages)

**Update Status:**
- Status: **Actively maintained** by University of Gothenburg with major funding
- Updated annually (typically March-April release for previous year's data)
- Version history maintained; current is v13 (through 2022 data, with v14 covering 2023)
- 1-2 year lag between events and data availability

**US Coverage:**
- **Comprehensive US coding from 1789 to present** -- one of the longest continuous time-series of democratic quality measurement available for any country
- All 483 indicators are coded for the US
- Recent notable findings: US Liberal Democracy Index declined from ~0.89 (2015) to ~0.72 (2022), placing the US in the "autocratizing" category in some V-Dem analyses
- US coding includes uncertainty intervals from the Bayesian IRT measurement model
- Expert coders for the US include US-based political scientists

**Applicability Assessment:**
- **Directly useful for:** (a) Backtesting the relationship between democratic quality changes and Revolution Index stress scores across 200+ years of US history; (b) Providing institutional health indicators (judicial independence, legislative constraints, press freedom) as direct model inputs; (c) Identifying autocratization episodes that should correlate with elevated stress scores; (d) Cross-national comparison -- where does the US sit relative to countries that have experienced democratic breakdown?
- **Strongest dataset for the project** in terms of US coverage, time depth, and indicator breadth
- **Limitation:** Annual frequency with 1-2 year lag limits real-time monitoring utility. Expert coding introduces subjectivity, though Bayesian aggregation mitigates this.

---

### 7. PITF Worldwide Atrocities Dataset

**Full Name and Citation:** Political Instability Task Force Worldwide Atrocities Dataset. PITF, Center for Systemic Peace.

**Coverage:**
- Global atrocity events (mass killings of 5+ civilians by state or non-state actors)
- 1995-2015

**Key Variables:**
- Event date and location
- Perpetrator type (state forces, rebel groups, militia, etc.)
- Number of deaths (estimated)
- Event type (massacre, extrajudicial killing, etc.)

**Access Method:**
- URL: Previously hosted at systemicpeace.org; access has been intermittent
- Download: CSV (when available)
- License: Public domain (US government-funded)
- **Access reliability concerns:** The PITF has undergone institutional changes. The dataset's current hosting and maintenance status is uncertain.

**Update Status:**
- Last updated: 2015
- Status: **Effectively discontinued** -- no updates since 2015
- The broader PITF project continues under different organizational structures, but this specific atrocity dataset has not been maintained

**US Coverage:**
- **Minimal US events** -- the US has very few events meeting the 5+ civilian death threshold from political violence
- Events that might qualify (mass shootings) are generally not coded as political atrocities unless they have clear political motivation

**Applicability Assessment:**
- **Limited utility for the project:** The dataset is discontinued, has minimal US coverage, and focuses on extreme violence events that are not the primary instability pathway for the US.
- **Marginal use:** Could provide cross-national reference for the severity spectrum -- establishing that US political violence is orders of magnitude below atrocity thresholds.

---

### 8. OMG Dataset (Dahl et al., 2025)

**Full Name and Citation:** OMG (Outcomes of Mass Groups) Dataset. Dahl, M. et al. (2025). Coverage of mass political movements and their outcomes. [UNVERIFIED -- recently announced dataset; full documentation not yet independently confirmed.]

**Coverage:**
- 200+ countries
- 1789-2019 (claimed)
- Mass political movements, including revolutionary movements, reform movements, and repressive campaigns

**Key Variables:**
- Movement type and goals
- Movement outcomes (success, partial success, failure)
- Regime response
- Time period and country
- [Full variable list not independently verified]

**Access Method:**
- URL: Not independently confirmed as of early 2026
- Access method: Expected to be published via academic data repositories
- License: Expected free academic access
- **Verification needed:** This dataset has been referenced in recent publications but the full public release and documentation have not been independently confirmed.

**Update Status:**
- Status: **Recently released** (2025)
- As a newly released dataset, it has not been widely used or validated by the research community

**US Coverage:**
- **Expected to include US** given the 1789-2019 coverage period and broad country scope
- Specific US event count and coding not independently verified

**Applicability Assessment:**
- **Potentially useful but unverified:** If the dataset provides coded political movement outcomes from 1789 to 2019, it could offer the longest historical coverage of US political movements of any dataset in this inventory. This would be valuable for backtesting whether the Revolution Index framework correctly identifies periods of elevated political mobilization in US history.
- **Caution:** The dataset's recency means it has not been peer-reviewed or independently validated. Its coding methodology, reliability, and US-specific coverage need verification before reliance.

---

### 9. Polity5 (Polity Project)

**Full Name and Citation:** Marshall, M.G. and Gurr, T.R. (2020). Polity5: Political Regime Characteristics and Transitions, 1800-2018. Center for Systemic Peace.

**Coverage:**
- 167 countries
- 1800-2018
- Coded regime characteristics for all independent states with population > 500,000

**Key Variables:**
- **Polity score** (-10 to +10): composite of institutionalized democracy and autocracy indicators
- **Democracy score** (0-10): competitiveness of political participation, openness of executive recruitment, constraints on chief executive
- **Autocracy score** (0-10): regulation of participation, competitiveness of executive recruitment, constraints on chief executive
- **Regime durability** (years since last regime change)
- **Regime type** (democracy, anocracy, autocracy based on Polity score thresholds)
- Special codes for interruption (-66), interregnum (-77), and transition periods (-88)

**Access Method:**
- URL: https://www.systemicpeace.org/polityproject.html
- Download: Excel/CSV, free download
- License: Free for academic use
- Well-documented codebook with coding rules for each component

**Update Status:**
- Last updated: 2018 data (Polity5 is the final version)
- Status: **Final version -- no further updates planned.** The Polity project has concluded. The Center for Systemic Peace has indicated that Polity5 is the terminal version.
- Polity has been partially superseded by V-Dem for many research purposes, though Polity's simplicity (a single -10 to +10 score) remains useful

**US Coverage:**
- **Full US coding from 1800 to 2018**
- US coded as Polity score +10 (full democracy) for most of its history post-Civil War
- The US Polity score has remained at +10 without interruption since 1871
- This constancy is itself informative: by Polity's measure, no democratic erosion has occurred in the US. Critics argue this reflects Polity's measurement limitations rather than actual US democratic stability (V-Dem has detected more variation)

**Applicability Assessment:**
- **Limited direct utility:** The US has a constant Polity score of +10 for 150+ years, meaning Polity provides zero variation for modeling US instability dynamics. The score would need to change to -5 or below (anocracy range) to trigger PITF-type instability predictions.
- **Cross-national reference value:** Polity's simplicity makes it useful for one specific purpose -- comparing the US to the PITF model's instability thresholds. The US is firmly in the "full democracy" category that the PITF model identifies as lowest risk.
- **Historical value:** Polity's long time series (1800-present) provides the best available measure of the Civil War and Reconstruction era regime transitions, if backtesting against the 19th century is attempted.

---

### 10. Reinhart-Rogoff Banking Crises Database

**Full Name and Citation:** Reinhart, C.M. and Rogoff, K.S. (2009). *This Time Is Different: Eight Centuries of Financial Folly*. Princeton University Press. Database updated in Laeven, L. and Valencia, F. (2013). "Systemic Banking Crises Database." *IMF Economic Review* 61(2): 225-270.

**Coverage:**
- 70+ countries, 1800-2014 (Reinhart-Rogoff); 1970-2017 (Laeven-Valencia)
- Codes systemic banking crises, currency crises, sovereign debt crises, and domestic debt crises
- Approximately 150 systemic banking crisis episodes in the modern sample

**Key Variables:**
- Crisis onset year (binary coding: crisis/no crisis)
- Crisis type (banking, currency, sovereign debt, domestic debt, inflation)
- Crisis duration
- Fiscal costs (% of GDP)
- Output loss (cumulative GDP decline)
- Debt increase (government debt change during crisis)

**Access Method:**
- Reinhart-Rogoff: Published data tables in the book appendix and on Carmen Reinhart's website (previously at Harvard, now at World Bank)
- Laeven-Valencia: IMF Working Paper, data tables in appendix, downloadable from IMF website
- License: Public/academic use (published data)

**Update Status:**
- Reinhart-Rogoff: Through 2014 (not actively updated as a standalone dataset)
- Laeven-Valencia: Updated periodically by the IMF; last update covers through 2017
- Status: Foundational reference datasets; updates are periodic rather than continuous

**US Coverage:**
- **~10 US banking/financial crisis episodes coded**, including:
  - Panic of 1907
  - Great Depression (1929-1933)
  - Savings and Loan Crisis (1988)
  - Global Financial Crisis (2007-2009)
- US crises are well-documented with extensive data on fiscal costs, output losses, and recovery periods

**Applicability Assessment:**
- **Directly useful for:** (a) Identifying financial crisis onset dates for the FST model's transmission mechanism (financial crisis -> political extremism); (b) Calibrating the Financial Stress Pathway model's "systemic crisis" threshold -- what level of financial stress constitutes a "systemic crisis" as defined by Reinhart-Rogoff? (c) Backtesting whether the Revolution Index shows elevated stress scores in post-crisis periods (particularly post-2008)
- **The FST model's key finding** (30% far-right vote increase after systemic financial crises) can be tested against the Reinhart-Rogoff US crisis dates combined with US election data.

---

### 11. Correlates of War (COW) Project

**Full Name and Citation:** Correlates of War Project. Sarkees, M.R. and Wayman, F.W. (2010). *Resort to War: A Data Guide to Inter-state, Extra-state, Intra-state, and Non-state Wars, 1816-2007*. CQ Press.

**Coverage:**
- Interstate wars, intrastate (civil) wars, extra-state wars, non-state wars
- 1816-present
- Inclusion threshold: 1,000 battle deaths
- Additional datasets: National Material Capabilities, Diplomatic Exchange, Trade, Alliances, IGO Membership

**Key Variables:**
- War type, participants, dates, battle deaths
- National Material Capabilities (CINC score): military expenditure, military personnel, energy consumption, iron/steel production, urban population, total population
- State system membership
- Territorial contiguity (for neighborhood effects)

**Access Method:**
- URL: https://correlatesofwar.org/
- Download: CSV/Stata, free download from project website
- License: Free for academic use with citation
- Well-documented codebooks for each dataset

**Update Status:**
- Status: **Actively maintained** by various affiliated researchers
- War dataset updates are periodic (latest versions extend through recent years)
- National Material Capabilities dataset updated periodically (latest through 2016)
- Some component datasets have more recent updates than others

**US Coverage:**
- **US interstate wars coded:** War of 1812, Mexican-American War, Spanish-American War, World Wars I and II, Korean War, Vietnam War, Gulf War, Afghanistan, Iraq
- **Zero US civil wars coded since 1865** (the Civil War is the last US intrastate war meeting the 1,000 battle deaths threshold)
- **National Material Capabilities:** Full US CINC scores available, showing the US as the globally dominant state for most of the 20th and 21st centuries

**Applicability Assessment:**
- **Limited direct utility for instability prediction:** The US has no post-1865 civil wars, and interstate wars are initiated by state policy, not caused by domestic instability.
- **Some indirect value:** (a) National Material Capabilities data provides long-run state capacity indicators; (b) The dataset confirms that the US is a military-dominant state where domestic instability pathways differ fundamentally from countries experiencing armed conflict; (c) Interstate war periods may correlate with domestic political stress (Vietnam era, War on Terror) and could serve as backtesting reference points.

---

### 12. World Values Survey (WVS)

**Full Name and Citation:** Inglehart, R.F. et al. World Values Survey: All Rounds -- Country-Pooled Datafile. JD Systems Institute & WVSA Secretariat.

**Coverage:**
- Over 100 countries, 7 waves (1981-2022)
- Approximately 400,000 respondents across all waves
- Representative national surveys on values, beliefs, and attitudes

**Key Variables (selected for instability relevance):**
- Confidence in government, parliament, political parties, courts, military, police, press
- Satisfaction with democracy and political system
- Justifiability of political violence, revolution, protest
- Economic perceptions and financial satisfaction
- Social trust (generalized and institutional)
- Political interest and participation
- Left-right self-placement
- National pride and identity strength

**Access Method:**
- URL: https://www.worldvaluessurvey.org/
- Download: Free registration, then CSV/SPSS/Stata download
- API: No API; batch download only
- License: Free for academic use

**Update Status:**
- Status: **Actively maintained** by the World Values Survey Association
- Wave 7 (2017-2022) is the most recent completed wave
- Wave 8 (2024-2028) is in progress
- Each wave takes 3-5 years to complete

**US Coverage:**
- **US included in most waves** (Waves 1-7), though not every wave
- US sample sizes typically 1,000-2,000 respondents per wave
- Data available for ~7 time points spanning 1981-2022
- Key US findings: declining institutional trust, increasing political polarization, changing values on social issues

**Applicability Assessment:**
- **Useful for attitudinal validation:** (a) WVS measures of institutional confidence, democratic satisfaction, and political violence justifiability provide direct measures of the attitudinal conditions that precede instability; (b) Cross-national comparison: do US attitudes look more like stable democracies or like countries that subsequently experienced instability?
- **Severe limitation:** Survey-based, with only ~7 US data points over 40 years. Far too infrequent for time-series modeling or real-time monitoring. Best used as periodic validation checkpoints rather than model inputs.
- **The "revolution justifiability" question** is directly relevant: what percentage of Americans believe revolution can be justified? Trend data over 40 years provides unique attitudinal context.

---

### 13. American National Election Studies (ANES)

**Full Name and Citation:** American National Election Studies. ANES, University of Michigan and Stanford University.

**Coverage:**
- US only
- 1948-present
- Pre-election and post-election surveys around presidential and midterm elections
- Cumulative datafile includes 50,000+ respondents across all years

**Key Variables (selected for instability relevance):**
- Partisan feeling thermometers (warmth toward own party, opposing party) -- the foundation of affective polarization measurement
- Trust in government ("How much of the time do you trust the government in Washington to do what is right?")
- External political efficacy (does government care what people think?)
- Political engagement and participation
- Perceptions of economic conditions (national and personal)
- Racial resentment scales
- Evaluations of democratic norms and institutions

**Access Method:**
- URL: https://electionstudies.org/
- Download: Free registration, then direct download (SPSS, Stata, CSV)
- License: Free for academic and non-commercial use
- Comprehensive codebooks and user guides

**Update Status:**
- Status: **Actively maintained** with biennial/quadrennial releases
- Time Series study runs every presidential election year; additional pilot studies and special modules
- 2024 study likely to be released in 2025-2026

**US Coverage:**
- **Exclusively US** -- the deepest time-series of US political attitudes available
- Continuous coverage from 1948 to present (biennial or quadrennial)
- Trust in government series: iconic measure showing decline from ~75% (1958-1964) to ~20% (2010s-2020s)
- Partisan feeling thermometer gap: tracked since 1968, showing dramatic widening (from ~25 points to ~45+ points)

**Applicability Assessment:**
- **Directly useful for:** (a) Backtesting attitudinal components of political stress against the Revolution Index timeline -- does declining trust correlate with rising stress scores? (b) The partisan feeling thermometer gap is the primary measure of affective polarization, one of the most consistently cited predictors of democratic backsliding; (c) The trust-in-government time series (1958-present) provides the longest continuous measure of institutional legitimacy for the US.
- **Limitation:** Survey frequency is biennial at best (presidential election years only for full Time Series), making it unsuitable for monthly or quarterly monitoring. Best used for calibration and validation at the 2-4 year timescale.
- **Complementarity:** ANES provides the attitudinal validation that structural/economic measures (FRED series) cannot -- it measures whether people feel the conditions that structural variables indicate.

---

## Summary Assessment

### Datasets Ranked by Utility for the Revolution Index Project

| Rank | Dataset | Primary Utility | US Coverage Quality |
|------|---------|----------------|---------------------|
| 1 | V-Dem | Democratic quality backtesting, institutional health indicators | Excellent (1789-present, 483 indicators) |
| 2 | ACLED | Real-time protest/violence monitoring, mobilization variables | Good (2020-present, 30K+ events) |
| 3 | ANES | Attitudinal validation, affective polarization, trust trends | Excellent (1948-present, US-only) |
| 4 | Mass Mobilization Project | Historical US protest trends (1990-2020) | Good (~500+ events) |
| 5 | Reinhart-Rogoff Banking Crises | Financial crisis identification for FSP calibration | Good (~10 US crises) |
| 6 | World Values Survey | Cross-national attitudinal comparison, revolution attitudes | Fair (7 waves, small samples) |
| 7 | NAVCO 2.1 | Cross-national threshold calibration | None (0 US campaigns) |
| 8 | Polity5 | Long-run regime type reference | Limited (constant +10 for 150 years) |
| 9 | Correlates of War | State capacity reference, war-era stress validation | Fair (interstate wars only) |
| 10 | UCDP/PRIO | Cross-national conflict thresholds | None (0 US conflicts) |
| 11 | OMG Dataset | Historical movements reference (if verified) | Unknown (unverified) |
| 12 | NAVCO 3.0 | Event-level mobilization dynamics | None (no US campaigns) |
| 13 | PITF Atrocities | Limited reference | Minimal (discontinued) |

### Validation Strategy Implications

Given the zero-event constraint, the Revolution Index validation strategy should rely on:

1. **Sub-crisis backtesting:** Use V-Dem (democratic quality changes), ACLED/Mass Mobilization (protest events), and ANES (attitudinal shifts) to validate that the model detects elevated stress during known periods of US political tension (1968, 1992, 2001, 2008, 2020-2021).

2. **Cross-national threshold calibration:** Use NAVCO, UCDP, and PITF to establish what stress levels preceded instability in other countries, then assess where the US falls relative to those thresholds.

3. **Financial crisis validation:** Use Reinhart-Rogoff banking crisis dates combined with the FST model's findings to test whether the Revolution Index correctly identifies post-crisis political stress periods.

4. **Attitudinal corroboration:** Use WVS and ANES to check whether structural stress scores correlate with measured changes in public attitudes about institutional trust, democratic satisfaction, and political violence acceptability.

This multi-source validation approach acknowledges the zero-event constraint honestly while providing rigorous assessment of whether the model produces meaningful signal.

---

## Bibliography

Chenoweth, E. and Lewis, O.A. (2013). Unpacking Nonviolent Campaigns: Introducing the NAVCO 2.0 Dataset. *Journal of Peace Research* 50(3): 415-423.

Chenoweth, E. and Stephan, M.J. (2011). *Why Civil Resistance Works: The Strategic Logic of Nonviolent Conflict*. Columbia University Press.

Clark, D. and Regan, P. (2016). Mass Mobilization Protest Data. Harvard Dataverse.

Coppedge, M. et al. (2023). V-Dem Dataset v13. Varieties of Democracy Project, University of Gothenburg.

Gleditsch, N.P. et al. (2002). Armed Conflict 1946-2001: A New Dataset. *Journal of Peace Research* 39(5): 615-637.

Laeven, L. and Valencia, F. (2013). Systemic Banking Crises Database. *IMF Economic Review* 61(2): 225-270.

Marshall, M.G. and Gurr, T.R. (2020). Polity5: Political Regime Characteristics and Transitions, 1800-2018. Center for Systemic Peace.

Raleigh, C. et al. (2010). Introducing ACLED: An Armed Conflict Location and Event Dataset. *Journal of Peace Research* 47(5): 651-660.

Reinhart, C.M. and Rogoff, K.S. (2009). *This Time Is Different: Eight Centuries of Financial Folly*. Princeton University Press.

Sarkees, M.R. and Wayman, F.W. (2010). *Resort to War: A Data Guide to Inter-state, Extra-state, Intra-state, and Non-state Wars, 1816-2007*. CQ Press.
