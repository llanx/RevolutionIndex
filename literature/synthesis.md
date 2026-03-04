# Literature Mining Synthesis

## Executive Summary

Phase 2 of the Revolution Index project conducted an exhaustive LLM-assisted literature review across six academic domains -- revolution prediction, democratic backsliding/state failure, historical case studies, economic preconditions, social movement theory, and media/information ecosystem studies -- to discover the full landscape of variables, frameworks, and data sources relevant to predicting political instability in the United States. The review synthesized approximately 200 sources spanning five generations of revolution studies (Korotayev et al. 2025), from classical structural analysis (Brinton 1938; Skocpol 1979) through structural-demographic theory (Turchin 2003; Goldstone 1991) to modern machine-learning factor ranking (Korotayev-Medvedev).

The review produced **45 concept-level variables** with hybrid evidence ratings (14 Strong, 21 Moderate, 10 Weak), **9 candidate frameworks** beyond the existing 3 models (PSI, PLI, FSP), and an inventory of **13 training/validation datasets**. Of the 45 cataloged variables, 18 (40%) have known federal data sources accessible through FRED, BLS, BEA, Census, or Treasury APIs; 21 (47%) have known non-federal sources (V-Dem, WID, ACLED, Pew, Gallup); and 6 (13%) have no identified data source. The evidence base converges on a core finding: political instability in developed democracies is driven by the interaction of economic distress (particularly financial crises and wage stagnation), elite dynamics (polarization, overproduction, factionalism), and institutional erosion (declining trust, weakening democratic guardrails) -- not by any single variable in isolation.

The most significant findings for the Revolution Index project are: (1) the Funke-Schularick-Trebesch financial crisis model provides the strongest empirically documented economic-to-political transmission mechanism, validating the existing FSP model's theoretical foundation; (2) Georgescu's (2023) structural-demographic theory operationalization for industrialized societies offers a more theoretically faithful proxy for elite overproduction (education-job mismatch) than the current top 1% income share; (3) V-Dem provides the most comprehensive measurement framework for democratic quality, with 483 indicators and continuous US coding from 1789 to present; and (4) the zero-event problem (the US has never experienced a revolution) requires a multi-source validation strategy that uses sub-crisis backtesting, cross-national thresholds, and attitudinal corroboration rather than standard supervised learning metrics.

---

## Variable-Framework Map

The following matrix shows which cataloged variables are used or referenced by each major framework. Frameworks include both the existing 3 models in the codebase (PSI, PLI, FSP) and the 9 candidate frameworks assessed in the framework assessment document. A checkmark indicates the framework explicitly uses or references the variable; a dash indicates it does not.

**Legend:**
- PSI = Turchin Political Stress Indicator (existing)
- PLI = Prospect Theory Perceived Loss Index (existing)
- FSP = Financial Stress Pathway (existing)
- PITF = Political Instability Task Force (Goldstone et al. 2010)
- FSI = Fragile States Index (Fund for Peace)
- CH = Collier-Hoeffler Greed/Grievance (2004)
- VDem = V-Dem Episodes of Regime Transformation
- KM = Korotayev-Medvedev ML Factor Ranking
- FST = Funke-Schularick-Trebesch Financial Crisis (2016)
- Chen = Chenoweth Civil Resistance (2011)
- Geo = Georgescu SDT for Industrialized Societies (2023)
- Grum = Grumbach State Democracy Index (2023)

### Strong-Rated Variables (14)

| # | Variable | PSI | PLI | FSP | PITF | FSI | CH | VDem | KM | FST | Chen | Geo | Grum |
|---|----------|-----|-----|-----|------|-----|----|------|----|----|------|-----|------|
| 1 | Income/Wealth Inequality | x | - | - | - | x | x | - | x | - | - | - | - |
| 2 | Real Wage Growth / Labor Share | x | x | - | - | - | - | - | x | - | - | x | - |
| 3 | Political Polarization (Congressional) | x | - | - | x | x | - | x | - | - | - | - | - |
| 4 | Affective Polarization | - | - | - | - | x | - | x | - | - | - | - | - |
| 5 | State Fiscal Distress | x | - | - | - | x | - | - | x | - | - | x | - |
| 6 | Financial Crisis / Systemic Stress | - | - | x | - | x | - | - | x | x | - | - | - |
| 7 | Government Trust / State Legitimacy | - | - | - | - | x | - | x | - | - | - | - | - |
| 8 | Elite Overproduction | x | - | - | - | - | - | - | - | - | - | x | - |
| 9 | Unemployment Rate | - | x | x | - | x | x | - | x | x | - | - | - |
| 10 | GDP Growth Rate | - | - | x | - | x | x | - | x | x | - | - | - |
| 11 | Elite Factionalism / Fragmentation | - | - | - | x | x | - | x | - | - | - | - | - |
| 12 | Protest Frequency and Participation | - | - | - | - | - | - | - | x | - | x | x | - |
| 13 | Regime Type / Institutional Quality | - | - | - | x | x | - | x | x | - | - | - | x |
| 14 | Wealth Concentration (Top 0.1%) | x | - | - | - | - | - | - | - | - | - | - | - |

### Moderate-Rated Variables (21)

| # | Variable | PSI | PLI | FSP | PITF | FSI | CH | VDem | KM | FST | Chen | Geo | Grum |
|---|----------|-----|-----|-----|------|-----|----|------|----|----|------|-----|------|
| 15 | Relative Deprivation / Expectation-Reality Gap | - | x | - | - | - | - | - | - | - | - | x | - |
| 16 | Horizontal Inequality (Between-Group) | - | - | - | x | x | x | - | - | - | - | - | - |
| 17 | Housing Affordability | - | x | - | - | - | - | - | - | - | - | x | - |
| 18 | Inflation Rate | - | - | x | - | x | - | - | x | x | - | - | - |
| 19 | Consumer Confidence / Sentiment | - | x | x | - | - | - | - | - | - | - | - | - |
| 20 | Intra-Elite Wealth Gap | x | - | - | - | - | - | - | - | - | - | - | - |
| 21 | Middle-Class Income Share | - | - | - | - | x | - | - | - | - | - | - | - |
| 22 | Judicial Independence | - | - | - | - | - | - | x | - | - | - | - | x |
| 23 | Freedom of Expression / Media Independence | - | - | - | - | x | - | x | - | - | - | - | - |
| 24 | Legislative Constraints on Executive | - | - | - | - | - | - | x | - | - | - | - | - |
| 25 | Electoral Integrity / Fraud Perception | - | - | - | - | - | - | x | - | - | - | - | x |
| 26 | Civil Society Density / Union Membership | - | - | - | - | x | - | x | - | - | x | - | - |
| 27 | Youth Unemployment / Disconnection | - | - | - | - | - | x | - | x | - | - | x | - |
| 28 | Household Debt / Leverage | - | - | x | - | - | - | - | - | x | - | - | - |
| 29 | Media Trust / Partisan Media Trust Gap | - | - | - | - | x | - | - | - | - | - | - | - |
| 30 | Voter Access Restrictions / Partisan Gerrymandering | - | - | - | - | - | - | - | - | - | - | - | x |
| 31 | Democratic Commitment (Attitudinal) | - | - | - | - | - | - | x | - | - | - | - | - |
| 32 | Anti-System Party Vote Share | - | - | - | - | - | - | - | - | x | - | - | - |
| 33 | Executive Aggrandizement | - | - | - | - | - | - | x | - | - | - | - | - |
| 34 | State Capacity / Institutional Quality | - | - | - | x | x | x | x | x | - | - | - | - |
| 35 | Cost of Living Pressure (Composite) | - | x | - | - | - | - | - | - | - | - | x | - |

### Weak-Rated Variables (10)

| # | Variable | PSI | PLI | FSP | PITF | FSI | CH | VDem | KM | FST | Chen | Geo | Grum |
|---|----------|-----|-----|-----|------|-----|----|------|----|----|------|-----|------|
| 36 | Misinformation Prevalence | - | - | - | - | - | - | - | - | - | - | - | - |
| 37 | Conspiratorial Thinking Prevalence | - | - | - | - | - | - | - | - | - | - | - | - |
| 38 | Social Media Political Engagement | - | - | - | - | - | - | - | - | - | - | - | - |
| 39 | Protest Diffusion / Contagion | - | - | - | - | - | - | - | - | - | x | - | - |
| 40 | Prior Protest Experience | - | - | - | - | - | - | - | - | - | x | - | - |
| 41 | Neighborhood / Diffusion Effects | - | - | - | x | - | - | - | - | - | - | - | - |
| 42 | Institutional Legitimacy Denial | - | - | - | - | - | - | - | - | - | - | - | - |
| 43 | Political Efficacy Beliefs | - | - | - | - | - | - | - | - | - | x | - | - |
| 44 | Information Fragmentation / Echo Chambers | - | - | - | - | - | - | - | - | - | - | - | - |
| 45 | Cross-Class Coalition Formation | - | - | - | - | - | - | - | - | - | x | - | - |

### Framework Coverage Summary

| Framework | Variables Used | Strong | Moderate | Weak | Focus Area |
|-----------|--------------|--------|----------|------|------------|
| PSI (existing) | 5 | 4 | 1 | 0 | Structural-demographic (MMP, EMP, SFD) |
| PLI (existing) | 5 | 2 | 3 | 0 | Perceived economic losses across life domains |
| FSP (existing) | 4 | 3 | 1 | 0 | Financial crisis -> political stress transmission |
| PITF | 4 | 3 | 1 | 0 | Regime type + state capacity |
| FSI | 14 | 7 | 7 | 0 | Multidimensional state fragility (broadest) |
| Collier-Hoeffler | 4 | 2 | 2 | 0 | Economic opportunity for rebellion |
| V-Dem ERT | 10 | 3 | 7 | 0 | Democratic quality across multiple dimensions |
| Korotayev-Medvedev ML | 8 | 5 | 3 | 0 | Data-driven factor ranking |
| FST | 5 | 3 | 2 | 0 | Financial crisis -> far-right voting |
| Chenoweth | 5 | 1 | 1 | 3 | Campaign mobilization and success |
| Georgescu SDT | 5 | 2 | 3 | 0 | SDT adapted for industrialized societies |
| Grumbach | 3 | 1 | 2 | 0 | Subnational democratic health |

**Key observations from the mapping:**

1. **High-consensus variables** (used by 4+ frameworks): Unemployment rate (6), GDP growth rate (5), regime type/institutional quality (5), political polarization (4), state fiscal distress (4), financial crisis/systemic stress (4). These variables have the strongest cross-framework consensus for inclusion in any political stress model.

2. **Unique-contribution variables**: Georgescu SDT is the only framework that operationalizes elite overproduction through education-job mismatch rather than income concentration. Grumbach is the only framework capturing subnational democratic variation. Chenoweth is the only framework with a quantitative mobilization threshold (3.5%).

3. **Orphan variables** (used by no framework in the map): Misinformation prevalence, conspiratorial thinking, social media political engagement, institutional legitimacy denial, and information fragmentation/echo chambers. All are Weak-rated with contested evidence, suggesting their theoretical importance may exceed their measurable predictive power.

4. **Existing model coverage**: The three existing models (PSI + PLI + FSP) collectively cover 12 of 45 variables (27%), primarily in economic and structural-demographic domains. The institutional/democratic quality dimension (judicial independence, legislative constraints, electoral integrity, executive aggrandizement, voter access) is entirely uncovered by the existing models -- a significant gap given that V-Dem and PITF research identifies these as central to instability risk.

---

## Evidence Strength Overview

### Rating Distribution

| Rating | Count | Percentage |
|--------|-------|------------|
| Strong | 14 | 31% |
| Moderate | 21 | 47% |
| Weak | 10 | 22% |
| Contested (cross-cutting marker) | 4 | 9% |

This distribution provides useful discrimination for downstream model selection. The 14 Strong-rated variables represent the evidence base's highest-confidence predictors, supported by statistically significant coefficients in 2+ independent quantitative studies. The 21 Moderate variables are viable candidates contingent on data availability. The 10 Weak variables are theoretically motivated but lack quantitative validation and are primarily candidates for future research rather than immediate model inclusion.

### Evidence Strength by Variable Category

| Category | Variables | Strong | Moderate | Weak |
|----------|-----------|--------|----------|------|
| Economic | Income inequality, real wages, financial crisis, GDP, unemployment, fiscal distress, inflation, housing, consumer confidence, household debt, middle-class share, cost of living, wealth concentration | 7 | 6 | 0 |
| Political/Institutional | Polarization (congressional + affective), regime type, judicial independence, legislative constraints, electoral integrity, voter access, executive aggrandizement, democratic commitment, anti-system voting | 3 | 7 | 0 |
| Elite Dynamics | Elite overproduction, elite factionalism, intra-elite wealth gap | 2 | 1 | 0 |
| Social/Mobilization | Government trust, protest frequency, civil society density, youth unemployment, prior protest, political efficacy, cross-class coalition | 2 | 3 | 2 |
| Information/Media | Media trust, misinformation, conspiratorial thinking, social media engagement, information fragmentation, institutional legitimacy denial | 0 | 1 | 5 |
| Contextual | Horizontal inequality, relative deprivation, state capacity, neighborhood/diffusion, protest diffusion | 0 | 3 | 2 |

**Key finding:** Economic variables have the strongest evidence base (7 of 13 rated Strong), followed by elite dynamics (2 of 3 Strong). Political/institutional variables are predominantly Moderate, reflecting that their measurement approaches (V-Dem expert coding, surveys) introduce more methodological uncertainty than economic indicators derived from objective data (FRED series). Information/media variables are overwhelmingly Weak -- a major gap between their perceived political importance and their empirical evidence base for predicting instability.

### Contested Variables

Four variables received the Contested marker, indicating significant disagreement in the literature:

1. **Income/Wealth Inequality**: Collier-Hoeffler (2004) find inequality is not significant when growth/income level is included. Cederman et al. (2013) argue aggregate measures miss the politically relevant horizontal dimension. The debate suggests *dynamic* inequality (rate of change) and *between-group* inequality may be more predictive than static aggregate measures.

2. **State Fiscal Distress**: Japan demonstrates that very high debt-to-GDP (250%+) need not produce fiscal crisis when debt is domestically held. Debt *level* may matter less than debt *servicing cost* or debt *trajectory*.

3. **Regime Type / Institutional Quality**: The application of PITF regime type categories to the US is heavily debated. Svolik (2019), Levitsky and Ziblatt (2018), and Przeworski (2019) argue US institutional depth makes it categorically different from the PITF training sample. V-Dem's coding of the US as "autocratizing" is also contested.

4. **Misinformation / Social Media / Information Fragmentation**: Three separate variables share the contested marker. Guess et al. (2019) found misinformation consumption is highly concentrated among a small minority. Boxell et al. (2017) found polarization increased most among demographics using social media least. The "filter bubble" thesis is largely rejected by empirical evidence.

---

## Data Availability Overview

### Distribution of Data Availability Tags

| Tag | Count | Percentage | Description |
|-----|-------|------------|-------------|
| fed-data | 18 | 40% | Known federal API source (FRED, BLS, BEA, Census, Treasury) |
| other-data | 21 | 47% | Known non-federal source (V-Dem, WID, ACLED, Pew, Gallup) |
| unknown | 6 | 13% | No identified data source |

### Data Availability by Variable Category

| Category | fed-data | other-data | unknown |
|----------|----------|------------|---------|
| Economic (13 vars) | 11 | 2 | 0 |
| Political/Institutional (10 vars) | 1 | 9 | 0 |
| Elite Dynamics (3 vars) | 1 (partial) | 2 | 0 |
| Social/Mobilization (7 vars) | 2 | 5 | 0 |
| Information/Media (6 vars) | 0 | 3 | 3 |
| Contextual (5 vars) | 2 | 3 | 0 |

**Key finding:** Economic variables are overwhelmingly available through federal APIs -- 11 of 13 are tagged `fed-data`. This means the economic dimension of any instability model can be built almost entirely from FRED/BLS/BEA/Census data with automated pipelines. Political/institutional variables are overwhelmingly `other-data`, requiring V-Dem, Polity, and academic datasets that update annually with lags. Information/media variables have the worst data availability -- 3 of 6 are `unknown`, reflecting both measurement immaturity and platform API restrictions since 2023.

### Federal API Coverage Highlights

The strongest federal data coverage exists for:
- **Labor market**: unemployment (U-3, U-6), labor share, real wages, youth unemployment, JOLTS job openings -- all monthly or quarterly via FRED/BLS
- **Financial stress**: STLFSI4 (weekly), NFCI (weekly), credit spreads (daily), VIX (daily), mortgage delinquency (quarterly) -- all via FRED
- **Fiscal health**: debt-to-GDP (quarterly), deficit/GDP (monthly), interest payments/revenue -- all via FRED/Treasury
- **Housing**: affordability index (monthly), home price indices (monthly), rent burden (annual) -- via FRED/HUD
- **Inflation**: CPI-U (monthly), core CPI (monthly), PCE (monthly), CPI components (monthly) -- all via BLS/FRED
- **Income distribution**: Gini (annual), quintile shares (annual), wealth distribution (quarterly) -- via Census/Federal Reserve

The weakest federal coverage exists for:
- **Democratic quality**: V-Dem is the primary source, updated annually with 1-2 year lag. No federal equivalent.
- **Polarization**: DW-NOMINATE (other-data) is the gold standard for congressional polarization. No FRED series.
- **Trust/legitimacy**: Gallup and Pew surveys are the primary sources. No federal survey tracks government trust continuously.
- **Protest activity**: ACLED (since 2020) and Mass Mobilization Project (1990-2020). No federal data source.

---

## Identified Gaps

### Theory Gaps

Variables where theory suggests importance but no established measurement exists:

1. **Revolutionary consciousness** (Foran 2005): The subjective readiness to participate in revolutionary action. Theoretically central to all five generations of revolution studies, but no standardized quantitative measure exists. The closest proxies are survey questions about revolution justifiability (WVS) and institutional legitimacy denial (PRRI), both measured periodically rather than continuously.

2. **Preference falsification gap** (Kuran 1991): The difference between privately held political views and publicly expressed ones. By definition, concealed preferences cannot be directly measured. The sudden collapse of preference falsification is the mechanism behind "unthinkable" revolutions (Kurzman 2004). No measurement approach has been proposed that could operate as a continuous time-series indicator.

3. **Frame resonance** (Snow and Benford 1986): The degree to which a social movement's framing of grievances resonates with the broader public. Central to social movement theory but no standardized quantitative operationalization exists. Protest participation growth rates may serve as a rough behavioral proxy.

4. **Spiral of silence strength** (Noelle-Neumann 1974): The extent to which perceived social pressure suppresses minority opinion expression. Theoretically important for understanding when preference falsification breaks down, but no established measurement methodology exists for continuous monitoring.

5. **Elite coordination capacity**: The ability of counter-elites to organize, communicate, and coordinate opposition. Turchin and Goldstone emphasize elite organization as a necessary condition for instability, but no quantitative measure captures this beyond crude proxies like anti-system party vote share or third-party candidacies.

### Data Gaps

Variables with known measurement approaches but no known US data source:

1. **Security force loyalty/defection indicators** (Chenoweth and Stephan 2011): A critical variable in the civil resistance literature -- campaigns succeed when security forces defect. No systematic quantitative measure exists for the US. Qualitative assessments of military/police political neutrality are available but not as time-series data.

2. **Campaign diversity metrics**: The cross-demographic breadth of protest participation. Could be constructed from protest demographic surveys but no existing time-series. ACLED provides event-level data from 2020 but without systematic demographic coding.

3. **Social media political content volume**: Theoretically relevant for tracking digital mobilization capacity, but platform API restrictions since 2023 (Twitter/X, Meta) have made systematic measurement increasingly difficult. FEC political ad spending provides a narrow proxy.

4. **Misinformation prevalence at population scale**: Multiple survey-based point estimates exist (Pew, PRRI) but no continuous time-series. Platform-level measurement is increasingly restricted. The gap between the theoretical importance attributed to misinformation and the ability to measure it systematically is one of the widest in the literature.

5. **Cross-class coalition formation indicators**: Wickham-Crowley (1992) and Foran (2005) identify cross-class alliances as necessary for revolutionary success, but no established measurement approach captures this as a continuous variable. Protest participation diversity by income/education could serve as a proxy but requires survey data not regularly collected.

6. **State-level democratic quality (real-time)**: Grumbach's (2023) State Democracy Index captures subnational variation but updates annually and requires assembling data across 50 states from multiple sources. No automated, real-time tracking of state-level democratic quality exists.

### Coverage Gaps

Areas where the 6 domain reviews may have missed important literature:

1. **Computational social science approaches**: The reviews covered ML factor ranking (Korotayev-Medvedev) but may have missed computational approaches using natural language processing of political speech, social network analysis of political communication, or agent-based modeling of mobilization dynamics. These approaches are methodologically distinct from the variable-based frameworks reviewed.

2. **Non-Western developed democracy literature**: The US-first lens appropriately prioritized literature studying the US and peer democracies, but may have underweighted instability dynamics in non-Western developed democracies (Japan's political turbulence, South Korea's democratic consolidation, Taiwan's democratization) that could offer relevant parallels.

3. **Psychological/individual-level mechanisms**: The reviews focused on structural, economic, and institutional variables. The individual-level psychology of radicalization, authoritarian personality dynamics (Stenner 2005), and moral foundations theory (Haidt 2012) were not systematically covered. These may offer mediating mechanisms that explain *why* structural stress produces political behavior in some contexts but not others.

4. **Climate/environmental stress literature**: The growing literature on climate change as a conflict multiplier was not systematically covered. While climate variables were excluded by the US-first lens (the US is not a climate-vulnerable state in the conflict literature sense), climate-related economic disruption (natural disaster costs, agricultural stress, energy price shocks) may merit inclusion as economic precondition variables.

5. **Post-2024 developments**: The reviews relied on Claude's training data supplemented by available information. Very recent publications (2025 and later) may offer updates to key findings, particularly regarding US democratic trajectory post-2024 election.

---

## Addressing Phase 1 Open Questions

### Open Question 1: Updated Turchin PSI operationalizations since End Times (2023)

**Finding: No post-2023 update found.** The Domain 1 (revolution prediction) review searched for publications, blog posts, or working papers updating Turchin's PSI operationalization since the publication of *End Times* in June 2023. No updated operationalization was identified. Turchin continues to publish on the Cliodynamica blog and the Seshat databank project, but these focus on historical secular cycle analysis rather than updated contemporary US PSI formulas.

**Implication:** The simplified 3-proxy operationalization in the codebase (labor share for MMP, top 1% income for EMP, debt-to-GDP for SFD) remains the best available approximation of Turchin's framework, with the caveat that it significantly simplifies the multi-factor composites described in Turchin's academic publications. The most promising alternative operationalization is Georgescu's (2023) education-job mismatch proxy for elite overproduction, which is more theoretically faithful to the "frustrated aspirant" mechanism than income concentration.

**Resolution status:** Phase 1 Open Question #1 is resolved. No update exists; the Georgescu operationalization is the most relevant recent development.

### Open Question 2: Other prospect theory applications to political risk

**Finding: Limited but growing.** The Domain 4 (economic preconditions) review identified Passarelli and Del Ponte (2020), "Prospect Theory and Political Behavior" in the *Oxford Research Encyclopedia of Politics*, which provides the most systematic treatment of prospect theory applied to aggregate political behavior. They confirm that loss aversion operates at the population level: voters punish incumbents more for economic losses than they reward them for equivalent gains. However, the application to revolution prediction specifically (as opposed to electoral behavior) is genuinely novel -- the PLI model's use of Kahneman-Tversky parameters to compute a political stress score from perceived losses appears to be without direct precedent in the published literature.

The closest parallel is Funke et al. (2016), which documents a loss-asymmetric political response to financial crises (far-right gains of ~30% vs. no comparable response to equivalent economic booms). This empirically demonstrates loss aversion at work in political outcomes, even though the authors do not frame their findings using prospect theory terminology.

**Implication:** The PLI model's theoretical foundation is on firmer ground than initially assessed in Phase 1. While no one has published a prospect-theory-based political stress index, the underlying mechanism (loss aversion driving political behavior) is well-documented. The PLI's novel contribution is the operationalization, not the theory.

**Resolution status:** Open Question #2 is resolved. The PLI approach is novel in form but grounded in documented mechanisms.

### Open Question 3: Financial stress -> political mobilization evidence

**Finding: Strong empirical base with documented lag structure.** The synthesis of Domain 3 (historical case studies), Domain 4 (economic preconditions), and the framework assessment provides substantial evidence:

- **Funke, Schularick, and Trebesch (2016)**: The single strongest empirical finding. Systemic financial crises (not normal recessions) produce a ~30% increase in far-right vote share, peaking 5-10 years after crisis onset. Based on 800+ elections across 20 advanced democracies, 1870-2014. This is the most rigorous quantitative study of the financial crisis -> political extremism transmission.

- **Mian, Sufi, and Trebbi (2014)**: Financial crises with household debt overhang increase political polarization and fractionalization. The mechanism operates through mortgage-related economic hardship concentrated in specific geographies.

- **De Bromhead, Eichengreen, and O'Rourke (2013)**: The 1930s specifically -- interwar financial crisis produced far-right gains across European democracies. Confirms the FST pattern is not unique to the post-WWII period.

- **Algan et al. (2017)**: Low institutional trust amplifies the financial crisis -> political transmission. When trust is low, financial crises produce larger political shifts than when trust provides a legitimacy buffer.

- **The 2008-2021 quasi-validation**: The sequence GFC (2008) -> Tea Party/Occupy (2010-2011) -> Trump/Sanders populism (2015-2016) -> January 6 (2021) fits the FST model's predicted lag structure (5-10 years from crisis to peak political effect) with remarkable precision.

**Implication:** The FSP model's causal chain is well-grounded empirically. The evidence supports three specific design decisions: (1) distinguish systemic financial crises from normal recessions in the trigger mechanism; (2) implement a 5-10 year lag window for the financial stress -> political stress transmission; (3) include institutional trust as a moderating variable that amplifies or dampens the transmission.

**Resolution status:** Open Question #3 is resolved with strong empirical support for the FSP's theoretical foundation.

### Open Question 4: Alternative data sources for discontinued series

**Finding: The OECD Consumer Confidence series (CSCICP03USM665S) discontinuation is the primary data gap.** The variable catalog and framework assessment provide the following alternatives:

- **University of Michigan Consumer Sentiment Index (UMCSENT)**: Available on FRED, monthly, 1978-present. The most direct replacement. However, UMCSENT is already used in the PLI model's consumer confidence/sentiment domain, so using it in the FSP would violate the project's zero-overlap design principle.

- **Conference Board Consumer Confidence Index**: Available through the Conference Board (other-data), monthly. Not on FRED, so requires a separate data pipeline. A viable replacement that preserves zero-overlap.

- **OECD Key Short-Term Economic Indicators (KSTEI)**: The OECD restructured its Main Economic Indicators program into KSTEI. A replacement series may be published to FRED under a different series ID. This requires verification in Phase 3.

- **Consumer Expectations sub-index (MICH)**: Available on FRED as a sub-component of the Michigan survey. Captures the forward-looking dimension of consumer sentiment, which may be more relevant for detecting J-curve dynamics than backward-looking confidence measures.

**Implication for Phase 3:** Prioritize verifying whether an OECD KSTEI replacement series has been published to FRED. If not, the Conference Board index is the recommended replacement to preserve zero-overlap. If zero-overlap is relaxed as a design constraint in Phase 4, UMCSENT is the simplest substitution.

**Resolution status:** Open Question #4 is resolved with multiple alternative options identified. Final selection is a Phase 3/4 implementation decision.

### Open Question 5: Normalization methods for trending series

**Finding: Multiple established approaches exist.** The framework assessment (FSI methodology, COINr reference) and Domain 4 review provide specific recommendations:

- **Rolling z-scores** (already used in FSP): The standard approach for trending macroeconomic series. A 20-year rolling window z-score centers the variable at its recent historical mean and measures deviations in standard deviations. This is what the FSP model already implements and is well-understood. The key decision is window length -- shorter windows (10 years) are more responsive but noisier; longer windows (30 years) are smoother but slower to detect shifts.

- **Percentile rank** (exists in codebase but unused): The `percentile_rank_series` function in normalization.py computes where each observation falls in the historical distribution. This directly solves the min-max pinning problem (a monotonically rising series would not be pinned at 1.0 because the percentile is relative to the full distribution). This is the simplest fix for the PSI normalization bug.

- **COINr approach** (from FSI methodology): The Composite Indicator Construction and Analysis in R (COINr) package implements multiple normalization methods specifically designed for composite indicators: min-max with rolling windows, rank-based transformation, distance-to-best-performer, and standardized (z-score) approaches. The package also includes built-in tools for comparing normalization methods and their impact on final scores.

- **Deviation-from-trend**: Fit a trend line (linear, HP filter, or Hodrick-Prescott) and measure deviations from trend. This separates the structural trend from cyclical variation, which may be more informative than absolute levels for detecting stress (a debt-to-GDP of 120% on a rising trend is less alarming than 120% after a sharp jump).

**Implication:** The min-max normalization bug in PSI (Phase 1 Critical Bug #1) has multiple established solutions. The simplest fix is to switch to the percentile rank function already in the codebase. For Phase 4, a systematic comparison of normalization methods (rolling z-score vs. percentile rank vs. deviation-from-trend) across all three models would be valuable -- different normalization choices can change model output more than the underlying theory.

**Resolution status:** Open Question #5 is resolved with specific normalization alternatives identified. The recommendation is: rolling z-scores for financial indicators (FSP), percentile rank for structural indicators (PSI), and the COINr package methodology for Phase 4 systematic comparison.

### Open Question 6: Frameworks beyond the existing 3 models

**Finding: 9 candidate frameworks assessed; 2 strongly recommended, 1 recommended, 6 documented for reference.** This question was definitively addressed by the framework assessment document (Plan 05). Summary:

**Strongly recommended for Phase 4:**
- **Georgescu SDT** (2023): Education-job mismatch proxy for elite overproduction, constructible from federal data (Census + BLS JOLTS). Most directly relevant to the existing PSI model -- offers a more theoretically faithful operationalization than the current top 1% income share proxy.
- **V-Dem ERT**: 483 indicators with comprehensive US coding from 1789 to present. The Liberal Democracy Index decline (0.89 to 0.72, 2015-2022) demonstrates within-democracy variation that other frameworks cannot detect. Fills the institutional/democratic quality gap in the existing models.

**Recommended for consideration:**
- **Grumbach State Democracy Index** (2023): Captures subnational democratic variation invisible to national-level measures. US democratic erosion is occurring at the state level (Grumbach APSR 2023). More labor-intensive to construct but fills a unique niche.

**Documented but not recommended as standalone:**
- PITF: US falls in low-risk cell on all variables; elements (factionalism concept) may transfer.
- FSI: Useful conceptual template but designed for fragile states, not stable democracies.
- Collier-Hoeffler: Core mechanism (resource financing) inapplicable to US.
- Korotayev-Medvedev ML: Useful as validation cross-check, not standalone model.
- FST: Directly supports existing FSP model's theoretical foundation; not a separate model but a validation anchor.
- Chenoweth: Campaign-level unit of analysis; provides threshold reference (3.5% rule) rather than continuous monitoring.

**Resolution status:** Open Question #6 is definitively resolved. See `literature/framework-assessment.md` for full details.

### Open Question 7: Sensitivity analysis methods for composite indicators

**Finding: COINr approach recommended for the Revolution Index's parameter space.** This question was partially addressed in the framework assessment (Plan 05) and is consolidated here:

The Revolution Index has 50+ parameters (weights, windows, thresholds) across three models, none empirically derived. The following sensitivity analysis methods were identified across assessed frameworks:

| Method | Source | Applicability to Revolution Index |
|--------|--------|----------------------------------|
| Morris screening | COINr/FSI methodology | **Primary recommendation** -- efficient initial screening to identify which of the 50+ parameters matter. O(p+1) model evaluations where p = number of parameters. |
| Sobol indices | COINr/FSI methodology | **Secondary recommendation** -- full global sensitivity analysis for the parameters Morris screening identifies as important. More computationally expensive but provides variance decomposition. |
| Bootstrap resampling | PITF | Appropriate for confidence intervals on the final score, but does not address parameter sensitivity. |
| Bayesian IRT | V-Dem | Appropriate for expert-coded indicators with measurement uncertainty. Not directly applicable to FRED-based objective data. |
| Monte Carlo simulation | Collier-Hoeffler | Standard for parametric models. Feasible as an alternative to Sobol but less informative about parameter interactions. |
| Permutation importance / Shapley values | Korotayev-Medvedev ML | ML-specific. Useful if Phase 4 adopts ML components. |
| Cross-validation (k-fold, leave-one-out) | PITF, Collier-Hoeffler | Appropriate for predictive accuracy but the zero-event problem limits applicability for the US. |

**Recommended protocol for Phase 4:**
1. **Morris screening first** (cheap): Run Morris screening across all 50+ parameters to identify which ones actually affect the output. Expect that many parameters will be shown to have negligible impact -- this reduces the dimensionality of the sensitivity problem.
2. **Sobol indices second** (expensive): For the parameters Morris identifies as influential (likely 10-15), compute Sobol first-order and total-effect indices to decompose output variance by parameter contribution.
3. **Bootstrap confidence intervals** (standard): Compute bootstrap intervals for the final composite score using the parameter ranges identified by Sobol as plausible.

The COINr R package (Becker et al. 2022) implements this full pipeline and is specifically designed for composite indicators. It can be invoked from Python via rpy2 or its methodology can be reimplemented directly.

**Resolution status:** Open Question #7 is definitively resolved with a concrete three-step protocol.

---

## Recommendations for Phase 3: Data Sourcing

### Priority 1: Strong-rated variables with fed-data tags (immediate sourcing)

The following 7 variables should be the first sourcing targets because they have the strongest evidence AND known federal data sources:

| Variable | Rating | Fed Source | Key Series |
|----------|--------|-----------|------------|
| Income/Wealth Inequality | Strong (Contested) | Census ACS, Federal Reserve DFA | Gini, wealth distribution |
| Real Wage Growth / Labor Share | Strong | FRED | W270RE1A156NBEA, real median earnings |
| State Fiscal Distress | Strong (Contested) | FRED, Treasury | GFDEGDQ188S, deficit/GDP |
| Financial Crisis / Systemic Stress | Strong | FRED | STLFSI4, NFCI, credit spreads |
| Elite Overproduction | Strong | Census + BLS JOLTS | Education-job mismatch (constructible) |
| Unemployment Rate | Strong | FRED/BLS | UNRATE, U6RATE |
| GDP Growth Rate | Strong | FRED/BEA | Real GDP growth |

### Priority 2: Strong-rated variables with other-data tags (secondary sourcing)

These variables have strong evidence but require non-federal data sources:

| Variable | Rating | Source | Access |
|----------|--------|--------|--------|
| Political Polarization (Congressional) | Strong | VoteView | Free download, 1789-present |
| Affective Polarization | Strong | ANES | Free download, 1968-present |
| Government Trust / State Legitimacy | Strong | Pew/Gallup | Free with limitations |
| Elite Factionalism | Strong | VoteView/V-Dem | Free download |
| Protest Frequency | Strong | ACLED | Free registration, 2020-present |
| Regime Type / Institutional Quality | Strong (Contested) | V-Dem | Free download, 1789-present |
| Wealth Concentration (Top 0.1%) | Strong | WID/Fed Reserve | Free download |

### Priority 3: Moderate variables needed for gap coverage

These Moderate-rated variables fill dimensions not covered by Strong variables:

| Variable | Why Include | Source |
|----------|-----------|--------|
| Housing Affordability | US analog to food price triggers; unique dimension | FRED (FIXHAI) |
| Household Debt / Leverage | Leading indicator of financial crisis | FRED (HDTGPDUSQ163N) |
| Youth Unemployment | Mobilization potential amplifier | FRED/BLS |
| Consumer Confidence | Captures subjective economic experience | FRED (UMCSENT or replacement) |
| Judicial Independence | Key democratic guardrail, currently uncovered | V-Dem (v2juhcind) |
| Electoral Integrity | Post-2020 salience, currently uncovered | Electoral Integrity Project |

### Data Pipeline Architecture Recommendation

Phase 3 should design the data pipeline around two tiers:
1. **Automated tier** (monthly/quarterly): Variables available through FRED and BLS APIs that can be pulled programmatically. Target: ~20 variables with monthly or quarterly updates.
2. **Manual tier** (annual): Variables from V-Dem, WID, ANES, and academic datasets that require periodic manual download. Target: ~10 variables with annual updates.

### Specific Action Items

1. **Verify OECD KSTEI replacement series** on FRED for CSCICP03USM665S discontinuation
2. **Test WID API endpoint** (two inconsistent URLs in wid_loader.py -- Phase 1 flagged issue)
3. **Assess Georgescu education-job mismatch constructibility**: Determine whether Census education attainment + BLS JOLTS occupational data can produce a reliable quarterly or annual proxy for elite overproduction
4. **Download and assess V-Dem v14**: Check US coding through 2023, extract key indices for backtesting
5. **Register for ACLED access** and assess US event data completeness since 2020
6. **Resolve the CSCICP03USM665S replacement** -- Conference Board or OECD KSTEI

---

## Recommendations for Phase 4: Model Building

### Framework Integration

The evidence supports a hybrid approach that retains the existing 3-model structure while incorporating findings from the literature review:

1. **Enhance PSI with Georgescu operationalization**: Replace or supplement the top 1% income share EMP proxy with an education-job mismatch metric constructible from Census and BLS data. This is the single most actionable improvement the literature suggests -- it makes the elite overproduction component more theoretically faithful to Turchin's concept of "frustrated aspirants."

2. **Add an institutional health dimension**: The existing 3 models completely miss the institutional/democratic quality variables (judicial independence, legislative constraints, executive aggrandizement, electoral integrity) that V-Dem and PITF research identifies as central to instability risk. Consider adding a fourth model or dimension that draws on V-Dem indicators to capture institutional erosion that economic and structural-demographic variables do not detect.

3. **Retain FSP with FST calibration**: The Funke-Schularick-Trebesch findings validate the FSP model's theoretical foundation. Use the documented 5-10 year lag structure for calibrating when financial stress should produce political stress. Critically, ensure the trigger mechanism distinguishes systemic financial crises from normal recessions -- normal recessions do not produce the FST-documented political response.

4. **PLI refinement**: The prospect theory framework is sound and novel. Phase 4 should address the undocumented sqrt transformation (either document the rationale or revert to the spec formula) and fix the velocity bonus to compute actual rate of change rather than magnitude. The housing affordability domain should be considered for inclusion given its status as the US analog to food price triggers.

### Normalization Strategy

Standardize normalization across models based on the evidence review:
- **Rolling z-scores** for financial and economic indicators (already used in FSP; extend to PSI's fiscal distress component)
- **Percentile rank** for structural indicators on long secular trends (labor share, inequality measures)
- **Deviation-from-trend** for variables where the trajectory matters more than the level (debt-to-GDP, wage growth)
- **COINr systematic comparison** to validate normalization choices against each other before finalizing

### Architecture Decisions the Evidence Does NOT Support

The synthesis deliberately does not recommend:
- **Selecting a single best framework**: The evidence shows that different frameworks capture different dimensions. No single framework covers all important variables.
- **ML-based prediction**: The zero-event problem makes supervised ML fundamentally inappropriate for US-specific instability prediction. ML factor rankings (Korotayev-Medvedev) are useful for variable selection, not model architecture.
- **Binary prediction**: Instability is a spectrum, not a binary outcome. The composite indicator approach (producing a 0-100 score) is more appropriate than binary classification.
- **Discarding the existing 3 models**: All three have sound theoretical foundations. The evidence supports enhancing them, not replacing them.

---

## Recommendations for Phase 5: Validation

### The Multi-Source Validation Strategy

Given the zero-event constraint (the US has never experienced a revolution), validation must use four complementary approaches:

**1. Sub-crisis backtesting against known US stress periods:**
Use the following episodes as validation targets, with expected severity tiers:

| Episode | Year(s) | Expected Stress Level | Primary Dimension |
|---------|---------|----------------------|-------------------|
| Late 1960s (urban riots, assassinations, Vietnam) | 1965-1970 | High | Social mobilization + institutional trust |
| Watergate | 1973-1974 | Moderate-High | Institutional trust + elite factionalism |
| Stagflation | 1979-1982 | Moderate | Economic stress |
| LA riots / early 1990s recession | 1991-1992 | Moderate | Economic + social mobilization |
| September 11 aftermath | 2001-2003 | Moderate (economic) | Financial + institutional |
| Global Financial Crisis | 2008-2010 | High | Financial crisis transmission |
| BLM / pandemic / election crisis | 2020-2021 | High | Multi-dimensional |

The model should detect at least 4 of these 7 as elevated stress periods AND should show lower scores during quiet periods (mid-1990s stability, mid-2010s pre-Trump).

**2. Cross-national threshold calibration from NAVCO and PITF:**
Use datasets like NAVCO (389 campaigns), PITF (state failure events), and V-Dem (autocratization episodes) to establish what levels of structural stress preceded instability events in other countries. The US stress scores can then be contextualized: "the US is currently at X% of the level that preceded instability in [comparison countries]." This is not prediction -- it is calibration.

Specifically:
- V-Dem: Compare US Liberal Democracy Index trajectory to Hungary (2010-2024), Poland (2015-2023), Turkey (2010-2020), and Venezuela (1998-2015) autocratization trajectories.
- NAVCO: Establish participation thresholds -- what fraction of population was mobilized in campaigns that succeeded? US protest participation is far below the 3.5% threshold.
- Reinhart-Rogoff: Calibrate financial stress thresholds against documented banking crisis episodes.

**3. Financial crisis calibration from Reinhart-Rogoff:**
Use the ~10 documented US banking/financial crises (Panic of 1907, Great Depression, S&L Crisis, GFC) to test whether the FSP model correctly identifies elevated financial stress in the years surrounding these events. This provides a modest but genuine validation sample for the financial dimension specifically.

**4. Attitudinal corroboration from ANES and WVS:**
Use the ANES trust-in-government time series (1958-present) and partisan feeling thermometer gap (1968-present) as external validators. If the Revolution Index shows rising stress, trust should be declining and affective polarization should be rising. If the model shows stress but trust is stable, something is wrong with the model.

### Specific Dataset Assignments

| Dataset | Validation Use | Access |
|---------|---------------|--------|
| V-Dem | Democratic quality backtesting (1789-present); autocratization comparison | Free (v-dem.net) |
| ACLED | US protest event validation (2020-present); mobilization component | Free (registration) |
| ANES | Attitudinal validation; affective polarization trend; trust time-series | Free (electionstudies.org) |
| Mass Mobilization Project | Historical US protest trends (1990-2020) | Free (Harvard Dataverse) |
| Reinhart-Rogoff | Financial crisis identification for FSP calibration | Published data |
| World Values Survey | Cross-national attitudinal comparison; revolution justifiability | Free (worldvaluessurvey.org) |
| Polity5 | Long-run regime type reference (limited US variation) | Free (systemicpeace.org) |

### Handling the Zero-Event Problem Honestly

The validation report must explicitly state:
- The model CANNOT be validated using standard ML metrics (precision, recall, F1) because there are no positive US revolution events to predict.
- Sub-crisis backtesting validates that the model detects *elevated stress*, not that it predicts *revolution*.
- Cross-national calibration provides *context*, not *prediction*.
- The model's honest claim is: "This is the level of political stress in the US as measured by variables that academic research has linked to instability in other contexts." It is NOT: "This predicts the probability of a US revolution."

---

## Cross-Domain Variable Categories

Variables from the 6 domain reviews cluster into thematic categories that cut across individual domains. These categories represent the analytical dimensions of political instability:

### Category 1: Economic Foundations (13 variables)

The economic dimension has the strongest evidence base and the best data availability. Variables include both level indicators (inequality, GDP, unemployment) and dynamic indicators (wage growth, financial crisis, household debt trajectory). The key insight from the literature is that *change* matters more than *level* -- the J-curve (Davies 1962), prospect theory (Kahneman and Tversky 1979), and the FST model (Funke et al. 2016) all emphasize that deterioration from a reference point is more politically destabilizing than absolute deprivation.

Variables: Income/wealth inequality, real wage growth/labor share, state fiscal distress, financial crisis/systemic stress, unemployment rate, GDP growth rate, housing affordability, inflation rate, consumer confidence/sentiment, household debt/leverage, middle-class income share, cost of living pressure, wealth concentration (top 0.1%).

### Category 2: Elite Dynamics (3 variables)

The smallest category but theoretically central. Turchin's structural-demographic theory and Goldstone's demographic-structural model both identify elite dynamics -- overproduction of aspirants, fragmentation of the ruling class, intra-elite wealth divergence -- as necessary conditions for instability. The key US-specific insight is that elite overproduction manifests as credential inflation (Georgescu 2023): law graduates unable to find legal employment, PhD holders in adjunct positions, MBA holders in entry-level jobs.

Variables: Elite overproduction, elite factionalism/fragmentation, intra-elite wealth gap.

### Category 3: Political/Institutional Health (10 variables)

The institutional dimension captures the democratic guardrails that prevent structural stress from producing regime breakdown. V-Dem and PITF research identifies this as central, but it is almost entirely absent from the existing 3 models. Variables in this category are predominantly Moderate-rated and rely on V-Dem expert coding or survey data -- making them more subjective but arguably more politically informative than objective economic indicators.

Variables: Political polarization (congressional), affective polarization, regime type/institutional quality, judicial independence, freedom of expression/media independence, legislative constraints on executive, electoral integrity/fraud perception, voter access restrictions/gerrymandering, democratic commitment (attitudinal), executive aggrandizement, anti-system party vote share.

### Category 4: Social Mobilization (7 variables)

The mobilization dimension captures whether structural grievances translate into collective action. The social movement literature (Tarrow 1994; McAdam 1982; McCarthy and Zald 1977) emphasizes that grievances alone do not produce mobilization -- organizational infrastructure, protest experience, and political efficacy beliefs are necessary mediating conditions. The key variable here is government trust/state legitimacy, which modulates the transmission of structural stress into political instability.

Variables: Government trust/state legitimacy, protest frequency and participation, civil society density/union membership, youth unemployment/disconnection, prior protest experience, political efficacy beliefs, cross-class coalition formation.

### Category 5: Information Environment (6 variables)

The newest and weakest category by evidence standards. All six variables are either Weak-rated or have contested evidence. The gap between the perceived political importance of misinformation, social media, and information fragmentation and the ability to measure their causal impact on political behavior is the single widest gap in the literature. Platform API restrictions since 2023 have further degraded measurement feasibility.

Variables: Media trust/partisan media trust gap, misinformation prevalence, conspiratorial thinking, social media political engagement, information fragmentation/echo chambers, institutional legitimacy denial.

### Category 6: Contextual/Structural (5 variables)

These variables provide structural context that moderates the relationship between stress and instability. State capacity determines whether structural pressures translate into instability or are absorbed by institutional responses. Horizontal inequality captures the politically relevant between-group dimension that aggregate measures miss. Neighborhood/diffusion effects capture the international context.

Variables: Relative deprivation/expectation-reality gap, horizontal inequality (between-group), state capacity/institutional quality, neighborhood/diffusion effects, protest diffusion/contagion.

---

## Limitations and Caveats

### LLM-Assisted Review Limitations

This literature review was conducted by Claude (an LLM) using its training data, supplemented by available web search results. This methodology has specific and important limitations:

1. **Potential hallucinated citations**: Claude can confidently cite papers that do not exist or misattribute findings to the wrong authors. Every citation in the domain reviews, variable catalog, framework assessment, and this synthesis should be independently verified before reliance. Papers marked [UNVERIFIED] in any document flag cases where the citation could not be independently confirmed.

2. **Training data cutoff effects**: Claude's training data has a knowledge cutoff that may miss very recent publications (2025+). The review used web search to supplement training data for recent developments, but coverage of the most recent literature is necessarily incomplete.

3. **Systematic coverage gaps**: A traditional systematic review uses database searches (Web of Science, Scopus, JSTOR) with defined search terms and inclusion/exclusion criteria to ensure comprehensive coverage. This LLM-assisted review used the training data's existing coverage of political science, economics, and conflict studies, which may systematically underrepresent certain journals, languages, or subfields.

4. **No adversarial testing**: The review was conducted by a single agent without peer review, replication, or adversarial critique by domain experts. In a traditional systematic review, multiple reviewers independently screen papers and resolve disagreements through discussion.

5. **Potential bias toward well-known authors**: Claude's training data likely overrepresents frequently-cited authors (Turchin, Goldstone, Chenoweth, Piketty) and underrepresents less-cited researchers who may have important contradictory findings.

### US Applicability Constraints

The majority of the revolution prediction and state failure literature studies developing countries, not established democracies. Variables that are strong predictors globally (regime type, infant mortality, ethnic fractionalization, resource dependence, military loyalty) may not discriminate meaningfully within the US context. The literature on democratic backsliding in established democracies (Bermeo 2016; Haggard and Kaufman 2021; Levitsky and Ziblatt 2018) is more directly applicable but is a younger and smaller body of research.

### Measurement Uncertainty

Many variables in the catalog rely on expert coding (V-Dem), periodic surveys (ANES, Pew, Gallup), or academic datasets with limited update frequency. These measurement approaches introduce uncertainty that is qualitatively different from the measurement error in economic time-series (FRED data). Expert-coded variables like V-Dem judicial independence scores reflect subjective assessments that may disagree across coders, while FRED unemployment rates reflect objective administrative counts. This measurement heterogeneity should be documented in the final model and propagated through uncertainty analysis.

### The Fundamental Uncertainty

The most important caveat is also the simplest: **the US has never experienced a revolution, and no model can validate against events that have not occurred.** The Revolution Index's honest claim is that it measures the level of political stress using variables that academic research has linked to instability in other contexts. It cannot and should not claim to predict the probability of a US revolution. The composite score is a thermometer, not a crystal ball.

---

## Bibliography

Acemoglu, Daron, and James A. Robinson. 2006. *Economic Origins of Dictatorship and Democracy*. Cambridge University Press.

Alesina, Alberto, and Roberto Perotti. 1996. "Income Distribution, Political Instability, and Investment." *European Economic Review* 40(6): 1203-1228.

Algan, Yann, Sergei Guriev, Elias Papaioannou, and Evgenia Passari. 2017. "The European Trust Crisis and the Rise of Populism." *Brookings Papers on Economic Activity* 2017(2): 309-400.

Bail, Christopher A., et al. 2018. "Exposure to Opposing Views on Social Media Can Increase Political Polarization." *Proceedings of the National Academy of Sciences* 115(37): 9216-9221.

Becker, William, et al. 2022. "COINr: An R Package for Developing Composite Indicators." *Journal of Open Source Software* 7(78): 4567.

Bermeo, Nancy. 2016. "On Democratic Backsliding." *Journal of Democracy* 27(1): 5-19.

Boxell, Levi, Matthew Gentzkow, and Jesse M. Shapiro. 2017. "Greater Internet Use Is Not Associated with Faster Growth in Political Polarization." *Proceedings of the National Academy of Sciences* 114(40): 10612-10617.

Brinton, Crane. 1938. *The Anatomy of Revolution*. Vintage Books.

Campante, Filipe R., and Davin Chor. 2012. "Why Was the Arab World Poised for Revolution?" *Journal of Economic Perspectives* 26(2): 167-188.

Cederman, Lars-Erik, Kristian S. Gleditsch, and Halvard Buhaug. 2013. *Inequality, Grievances, and Civil War*. Cambridge University Press.

Chenoweth, Erica, and Maria J. Stephan. 2011. *Why Civil Resistance Works*. Columbia University Press.

Clark, David, and Patrick Regan. 2016. "Mass Mobilization Protest Data." Harvard Dataverse.

Collier, Paul, and Anke Hoeffler. 2004. "Greed and Grievance in Civil War." *Oxford Economic Papers* 56(4): 563-595.

Coppedge, Michael, et al. 2023. "V-Dem Dataset v13." Varieties of Democracy (V-Dem) Project.

Davies, James C. 1962. "Toward a Theory of Revolution." *American Sociological Review* 27(1): 5-19.

De Bromhead, Alan, Barry Eichengreen, and Kevin H. O'Rourke. 2013. "Political Extremism in the 1920s and 1930s." *Economic Journal* 123(571): F371-F406.

Foa, Roberto Stefan, and Yascha Mounk. 2016. "The Danger of Deconsolidation." *Journal of Democracy* 27(3): 5-17.

Foran, John. 2005. *Taking Power*. Cambridge University Press.

Funke, Manuel, Moritz Schularick, and Christoph Trebesch. 2016. "Going to Extremes: Politics After Financial Crises, 1870-2014." *European Economic Review* 88: 227-260.

Georgescu, Petru A. 2023. "Structural-Demographic Theory Revisited: Evidence from Industrialized Societies." *PLoS ONE* 18(11).

Goldstone, Jack A. 1991. *Revolution and Rebellion in the Early Modern World*. University of California Press.

Goldstone, Jack A., et al. 2010. "A Global Model for Forecasting Political Instability." *American Journal of Political Science* 54(1): 190-208.

Grumbach, Jacob M. 2023. "Laboratories of Democratic Backsliding." *American Political Science Review* 117(3): 967-984.

Guess, Andrew, Brendan Nyhan, and Jason Reifler. 2019. "Exposure to Untrustworthy Websites in the 2016 US Election." *Nature Human Behaviour* 4: 472-480.

Gurr, Ted Robert. 1970. *Why Men Rebel*. Princeton University Press.

Haggard, Stephan, and Robert Kaufman. 2021. *Backsliding*. Cambridge University Press.

Kahneman, Daniel, and Amos Tversky. 1979. "Prospect Theory: An Analysis of Decision under Risk." *Econometrica* 47(2): 263-291.

Korotayev, Andrey, Victor Ustyuzhanin, Leonid Grinin, and Alina Fain. 2025. "Five Generations of Revolution Studies." *Comparative Sociology* 24(1): 1-45.

Kuran, Timur. 1991. "Now Out of Never: The Element of Surprise in the East European Revolution of 1989." *World Politics* 44(1): 7-48.

Kurzman, Charles. 2004. *The Unthinkable Revolution in Iran*. Harvard University Press.

Levitsky, Steven, and Daniel Ziblatt. 2018. *How Democracies Die*. Crown Publishing.

McAdam, Doug. 1982. *Political Process and the Development of Black Insurgency*. University of Chicago Press.

McCarty, Nolan, Keith T. Poole, and Howard Rosenthal. 2006. *Polarized America*. MIT Press.

McCoy, Jennifer, and Murat Somer. 2019. "Toward a Theory of Pernicious Polarization." *Annals of the American Academy of Political and Social Science* 681(1): 234-271.

McCarthy, John D., and Mayer N. Zald. 1977. "Resource Mobilization and Social Movements." *American Journal of Sociology* 82(6): 1212-1241.

Mian, Atif, Amir Sufi, and Francesco Trebbi. 2014. "Resolving Debt Overhang." *American Economic Journal: Macroeconomics* 6(2): 1-28.

Mounk, Yascha. 2018. *The People vs. Democracy*. Harvard University Press.

Noelle-Neumann, Elisabeth. 1974. "The Spiral of Silence: A Theory of Public Opinion." *Journal of Communication* 24(2): 43-51.

Norris, Pippa. 2011. *Democratic Deficit*. Cambridge University Press.

Passarelli, Francesco, and Giacomo Del Ponte. 2020. "Prospect Theory and Political Behavior." *Oxford Research Encyclopedia of Politics*.

Piketty, Thomas. 2014. *Capital in the Twenty-First Century*. Harvard University Press.

Piketty, Thomas, and Emmanuel Saez. 2003. "Income Inequality in the United States." *Quarterly Journal of Economics* 118(1): 1-41.

Reinhart, Carmen M., and Kenneth S. Rogoff. 2009. *This Time Is Different*. Princeton University Press.

Saez, Emmanuel, and Gabriel Zucman. 2016. "Wealth Inequality in the United States since 1913." *Quarterly Journal of Economics* 131(2): 519-578.

Skocpol, Theda. 1979. *States and Social Revolutions*. Cambridge University Press.

Snow, David A., and Robert D. Benford. 1986. "Ideology, Frame Resonance, and Participant Mobilization." *International Social Movement Research* 1: 197-217.

Tarrow, Sidney. 1994. *Power in Movement*. Cambridge University Press.

Turchin, Peter. 2003. *Historical Dynamics*. Princeton University Press.

Turchin, Peter. 2023. *End Times*. Penguin Press.

Tversky, Amos, and Daniel Kahneman. 1992. "Advances in Prospect Theory: Cumulative Representation of Uncertainty." *Journal of Risk and Uncertainty* 5(4): 297-323.

V-Dem Institute. 2023. *Democracy Report 2023*. University of Gothenburg.

Walter, Barbara F. 2022. *How Civil Wars Start*. Crown Publishing.

Wickham-Crowley, Timothy P. 1992. *Guerrillas and Revolution in Latin America*. Princeton University Press.
