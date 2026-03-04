# Literature Review: Democratic Backsliding and State Failure

## Scope

This review covers the academic literature on democratic backsliding, democratic erosion, state failure prediction, and regime transition. The domain encompasses institutional decline in established democracies, the measurement of democratic quality over time, quantitative models that forecast state failure, and the structural conditions that make democratic breakdown -- and by extension revolution -- possible.

**Boundaries with other domains:**
- **Revolution prediction** (Domain 1) covers revolution theory and quantitative forecasting of revolutionary episodes. This domain covers the conditions that precede revolution -- institutional erosion, declining democratic quality, state capacity loss -- rather than revolution itself.
- **Historical case studies** (Domain 3) examines specific episodes of democratic breakdown and state failure in depth; this review draws on those cases for variable identification but focuses on the theoretical and empirical literature rather than case narratives.
- **Economic preconditions** (Domain 4) covers economic variables in depth; this review references economic variables as they appear in state failure models but does not provide deep economic analysis.
- **Social movement theory** (Domain 5) covers mobilization dynamics; this review addresses the institutional context in which mobilization occurs.

This review focuses on: (1) theories of why democracies die or erode, (2) quantitative models that measure and predict democratic decline and state failure, (3) the specific measurable variables those theories and models identify, and (4) the applicability of those variables to the contemporary United States, which is the central case for this project.

---

## Foundational Works

### Classical Theories of Democratic Breakdown (pre-2000)

**Juan J. Linz: The Breakdown of Democratic Regimes (1978):** Linz's foundational study identified the conditions under which democratic regimes collapse. He emphasized the role of "disloyal opposition" -- political actors who reject democratic rules and seek to undermine the system from within -- and "semi-loyal" actors who tolerate disloyal behavior. Linz argued that democratic breakdown is typically a process rather than an event: it begins with a legitimacy crisis, proceeds through polarization and the rise of disloyal opposition, and culminates when moderate elites fail to defend democratic institutions. Key variables: regime legitimacy, presence of disloyal opposition, elite commitment to democratic norms, and the efficacy of democratic problem-solving (Linz 1978).

**Juan Linz and Alfred Stepan: Problems of Democratic Transition and Consolidation (1996):** Linz and Stepan extended the analysis to democratic consolidation, arguing that democracy is "consolidated" when it becomes "the only game in town" -- behaviorally (no significant actors try to overthrow it), attitudinally (a strong majority believes democracy is the best form of government), and constitutionally (all actors are habituated to resolving conflicts within democratic rules). They identified five arenas of consolidated democracy: civil society, political society, rule of law, state apparatus, and economic society. Deconsolidation occurs when any of these arenas weakens substantially (Linz and Stepan 1996).

**Samuel P. Huntington: The Third Wave (1991):** Huntington identified three waves of democratization (1828-1926, 1943-1962, 1974-present) and two "reverse waves" (1922-1942, 1958-1975). His analysis of reverse waves identified key risk factors: weak democratic legitimacy, economic crisis, authoritarian nostalgia, demonstration effects from neighboring authoritarian regimes, and the intervention of external powers. The "two-turnover test" -- democracy is consolidated when power has been peacefully transferred between parties twice -- became a standard benchmark. Huntington's framework generated variables including economic performance legitimacy, turnover history, and regional democratic density (Huntington 1991).

**Guillermo O'Donnell and Philippe C. Schmitter: Transitions from Authoritarian Rule (1986):** O'Donnell and Schmitter's seminal study of democratic transitions established key concepts for understanding regime change: liberalization (opening within an authoritarian regime), democratization (establishment of democratic institutions), and consolidation (routinization of democratic practices). Their analysis emphasized the uncertainty inherent in transitions and the critical role of pact-making between regime softliners and opposition moderates. For democratic backsliding, the reverse process is relevant: what happens when pacts break down, when hardliners gain ascendancy, and when democratic institutions are hollowed out from within (O'Donnell and Schmitter 1986).

### Early Quantitative Approaches to State Failure

**The Political Instability Task Force (PITF), 1994-present:** Originally called the State Failure Task Force, PITF was established by the CIA to develop early-warning models for state instability. The initial PITF reports (Esty et al. 1995; Goldstone et al. 2000) tested hundreds of variables and established that a parsimonious model based on regime type, quality of life (infant mortality), and ethnic/communal factors could predict state failure onset with reasonable accuracy. The PITF's key methodological innovation was treating state failure as a categorical event (onset/no onset in a given 2-year window) rather than a continuous score, enabling logistic regression approaches that could be evaluated for predictive accuracy (Esty et al. 1995; Goldstone et al. 2000).

---

## Core Empirical Studies

### Goldstone et al.: PITF State Failure Model (2010)

The definitive published version of the PITF model tested a parsimonious set of variables against a comprehensive global dataset of state failure episodes (1955-2003). The final model uses four variables:

1. **Regime type (5 categories):** Full autocracies, partial autocracies without factionalism, partial autocracies with factionalism, partial democracies without factionalism, partial democracies with factionalism, and full democracies. The key finding is that partial democracies (anocracies) with factionalism -- particularly ethnic factionalism -- have the highest instability risk, approximately 10-15 times that of full democracies.
2. **Infant mortality rate:** A composite proxy for state capacity, development level, and the quality of governance. Countries in the top quintile globally have dramatically elevated risk.
3. **Ethnic discrimination:** The presence of state-led discrimination against ethnic minorities, coded using the Minorities at Risk (MAR) dataset.
4. **Neighborhood conflict:** Whether any neighboring state is experiencing armed conflict.

The model achieves over 80% accuracy in out-of-sample testing with a 2-year prediction window. The most powerful predictor is regime type: the interaction of partial democracy and factionalism (Goldstone et al. 2010).

**For Plan 05 assessment:** The PITF model is a candidate framework for detailed evaluation. Its strengths are rigorous validation and parsimony. Its limitations for the US project are that infant mortality and ethnic discrimination (as coded in MAR) do not discriminate within the US context, and the model was trained on events (coups, civil wars, genocide) that are categorically different from the forms of instability most likely in the US (democratic erosion, political violence, institutional breakdown).

### V-Dem: Episodes of Regime Transformation (ERT)

The Varieties of Democracy (V-Dem) project, based at the University of Gothenburg, represents the most comprehensive attempt to measure democratic quality across time and space. The V-Dem dataset includes 483 indicators coded by country experts for 202 countries from 1900 to the present. Key indices include:

- **Liberal Democracy Index (v2x_libdem):** Combines electoral democracy with liberal components (judicial independence, legislative constraints on executive, civil liberties).
- **Electoral Democracy Index (v2x_polyarchy):** Based on Dahl's polyarchy concept -- freedom of expression, freedom of association, suffrage, clean elections, elected officials.
- **Egalitarian Democracy Index:** Adds equality of access and resources.
- **Participatory Democracy Index:** Adds direct participation beyond elections.
- **Deliberative Democracy Index:** Adds quality of public reason-giving.

**Episodes of Regime Transformation (ERT):** V-Dem identifies discrete episodes of autocratization and democratization. For the United States, V-Dem has coded a decline in the Liberal Democracy Index beginning around 2016, placing the US in the "autocratizing" category in some specifications. The US Liberal Democracy Index declined from approximately 0.89 in 2015 to approximately 0.72 by 2022 -- a significant drop, though still well above the "autocracy" threshold. The components driving the decline include freedom of expression, media independence, judicial independence, and legislative constraints on the executive (Luhrmann and Lindberg 2019; V-Dem Institute 2023).

**Variables from V-Dem relevant to this project:**
- Judicial independence (v2juhcind)
- Legislative constraints on executive (v2xlg_legcon)
- Freedom of expression (v2x_freexp_altinf)
- Government censorship of media (v2mecenefm)
- Political polarization (v2cacamps, v2smpolsoc)
- Civil society participation (v2x_cspart)
- Government attacks on judiciary (v2jupoatck)
- Executive respect for constitution (v2exrescon)

**For Plan 05 assessment:** V-Dem ERT is a candidate framework for detailed evaluation. Its strengths are extraordinary granularity (483 indicators), global coverage, and explicit coding of the US over time. Its limitations include reliance on expert coding (subjective), annual frequency (cannot detect within-year changes), and the fact that small absolute changes in V-Dem scores for developed democracies may be within measurement error.

### Fragile States Index (FSI)

The Fund for Peace publishes the Fragile States Index (formerly Failed States Index) annually since 2005, rating 178 countries on 12 indicators across four dimensions:

**Cohesion indicators:**
- C1: Security Apparatus (state monopoly on use of force)
- C2: Factionalized Elites (elite fragmentation along ethnic, class, or religious lines)
- C3: Group Grievance (tensions between social groups)

**Economic indicators:**
- E1: Economic Decline (GDP growth, per capita income, inflation)
- E2: Uneven Economic Development (Gini, urban-rural gap, group-based inequality)
- E3: Human Flight and Brain Drain (emigration of educated professionals)

**Political indicators:**
- P1: State Legitimacy (public confidence in state institutions, elections, political processes)
- P2: Public Services (government capacity to deliver basic services)
- P3: Human Rights and Rule of Law (civil liberties, judicial independence, press freedom)

**Social indicators:**
- S1: Demographic Pressures (population growth, food scarcity, disease)
- S2: Refugees and IDPs (displacement pressures)

**Cross-cutting indicator:**
- X1: External Intervention (foreign military, economic, or political intervention)

Each indicator is scored 0-10 (10 = most fragile), producing a composite 0-120 score. The US typically scores in the "Sustainable" or "More Stable" range (total around 35-45 out of 120), ranking near the bottom of fragility. However, individual component scores for Factionalized Elites (C2), State Legitimacy (P1), and Group Grievance (C3) have shown notable increases since 2016 (Fund for Peace 2023).

**Methodology relevance:** The FSI's normalization approach (0-10 expert-scaled with quantitative data normalized against own history) and its use of rate-of-change against historical baselines are methodologically relevant to the project's normalization challenges (Phase 1 Open Question #5). The FSI avoids the min-max pinning problem identified in the PSI model by measuring change relative to a country's own trajectory rather than against global extremes.

**For Plan 05 assessment:** The FSI methodology is a candidate framework. Its strength is comprehensiveness (12 indicators across all relevant dimensions). Its primary limitation for this project is that the US sits near the floor of the fragility scale, limiting discrimination. However, individual component scores and the rate-of-change methodology may still provide useful signal.

### Grumbach: Laboratories of Democratic Backsliding (2023)

Jacob Grumbach's research represents the most important US-specific contribution to the democratic backsliding literature. Rather than treating the US as a single national unit, Grumbach measures democratic quality at the state level, revealing substantial within-US variation that national-level measures obscure.

Grumbach developed a State Democracy Index combining variables across multiple dimensions:
- **Voter registration barriers** (voter ID requirements, registration restrictions, purge practices)
- **Electoral district manipulation** (partisan gerrymandering)
- **Ballot access** (early voting, mail voting, Election Day registration)
- **Electoral administration** (election official partisanship, audit procedures)

Key findings:
1. **Partisan control is the strongest predictor:** Republican trifecta control (governor + both legislative chambers) is associated with significant democratic backsliding at the state level, while Democratic trifecta control is associated with democratic expansion. This is a contested finding -- the pattern is clear in the data but its interpretation is debated.
2. **Backsliding accelerated after 2010:** Following the 2010 Census redistricting cycle and the *Shelby County v. Holder* (2013) Supreme Court decision weakening the Voting Rights Act, the pace of state-level democratic erosion increased.
3. **Subnational variation is enormous:** Some US states score comparably to established European democracies on democratic quality, while others score closer to hybrid regimes (Grumbach 2023).

**For Plan 05 assessment:** Grumbach's state-level approach is a candidate framework. Its unique strength is disaggregating US democracy below the national level, capturing variation that V-Dem and Polity miss. Its limitation is that it focuses primarily on electoral dimensions of democracy (voting access, gerrymandering) rather than broader indicators (judicial independence, civil liberties, state capacity).

### Levitsky and Ziblatt: How Democracies Die (2018)

Levitsky and Ziblatt's influential work identified two "guardrails" of American democracy: mutual toleration (accepting political opponents as legitimate) and institutional forbearance (restraint in using institutional prerogatives to their legal maximum). They argued that the erosion of these informal norms -- which had historically constrained political behavior beyond what formal rules required -- is the primary mechanism of democratic backsliding in the US.

Their framework identifies four behavioral warning signs of authoritarian leaders:
1. Rejection of (or weak commitment to) democratic rules of the game
2. Denial of the legitimacy of political opponents
3. Toleration or encouragement of political violence
4. Readiness to curtail the civil liberties of opponents, including media

**Variables generated:** Norm erosion is difficult to measure quantitatively, but proxies include: frequency of norm-breaking behavior by elected officials, rhetoric delegitimizing opponents, tolerance of political violence in public opinion surveys, and attacks on media and judicial independence. V-Dem's expert-coded measures of executive respect for constitution and government attacks on the judiciary capture some of these dynamics (Levitsky and Ziblatt 2018).

### Bermeo: On Democratic Backsliding (2016)

Nancy Bermeo's seminal article defined modern democratic backsliding as distinct from the classical coups and autogolpes of earlier eras. She identified three contemporary forms:

1. **Promissory coups:** Military seizures of power with promises of future elections (declining in frequency).
2. **Executive aggrandizement:** Elected leaders gradually dismantle democratic institutions through legal or quasi-legal means -- packing courts, weakening legislatures, restricting media, altering electoral rules. This is the dominant form of democratic backsliding in the 21st century.
3. **Strategic harassment and manipulation:** Incumbents use state resources, selective prosecution, and electoral manipulation to disadvantage opponents without formally abolishing elections.

Bermeo's key contribution was showing that modern backsliding is incremental rather than sudden -- it occurs through a series of small steps, each of which may appear legal or even democratic, but which cumulatively erode democratic quality. This makes it harder to detect and resist because there is no single obvious "bright line" that has been crossed (Bermeo 2016).

**Variables generated:** Frequency of executive aggrandizement actions (court packing, inspector general firings, executive order overreach); strategic harassment (selective prosecution, IRS targeting); electoral manipulation (gerrymandering, voter suppression). V-Dem's component indicators map closely to these categories.

### Kaufman and IGCC: Democratic Resilience (2021-2024)

Robert Kaufman and the UC San Diego Institute on Global Conflict and Cooperation (IGCC) have led a research program on democratic resilience -- the flip side of democratic backsliding. Rather than asking "why do democracies die?", they ask "why do democracies survive threats?"

Key findings from the resilience literature:
1. **Institutional depth matters:** Democracies with deep institutional infrastructure (independent judiciary, professional bureaucracy, federal structure, free press) are more resilient to democratic erosion than those with shallow institutions.
2. **Civil society as a buffer:** Active civil society organizations -- independent media, advocacy groups, professional associations, unions -- serve as early warning systems and mobilization platforms that constrain would-be authoritarians.
3. **Economic performance is conditional:** Economic crisis creates vulnerability, but its effect is mediated by institutional strength. Countries with strong institutions can weather economic crises without democratic erosion; countries with weak institutions cannot.
4. **Polarization is the key vulnerability:** Even strong institutions can be eroded when polarization reaches the point where a significant fraction of the population prioritizes partisan victory over democratic process (Kaufman and Haggard 2021; IGCC Democratic Resilience Reports 2022-2024).

**Variables generated:** Institutional depth (judiciary independence, bureaucratic quality, press freedom), civil society density, polarization level, economic performance under institutional stress.

---

## Recent Developments (2020-2025)

### V-Dem Annual Reports on the US (2020-2024)

The V-Dem Institute has increasingly focused on the United States in its annual "Democracy Report" publications. Key developments:

- **2020 report:** First coded the US as experiencing an "episode of autocratization" -- a sustained and significant decline in democratic attributes.
- **2021 report:** Placed the US in the "declining democracies" category alongside Brazil, India, and Poland.
- **2022-2023 reports:** Documented continued decline in the Liberal Democracy Index, driven primarily by deterioration in freedom of expression, judicial independence, and legislative constraints on the executive.
- **2024 report:** Noted partial stabilization in some indicators but continued concern about electoral integrity and partisan polarization.

The V-Dem coding of the US has been controversial. Critics argue that V-Dem expert coders may be influenced by political events (January 6, 2021) in ways that conflate dramatic episodes with underlying institutional change. Defenders argue that the indicators are measuring real institutional changes -- court-packing attempts, norm-breaking behavior, electoral interference -- that represent genuine democratic erosion regardless of whether they succeed (V-Dem Institute 2020, 2021, 2023, 2024).

### Haggard and Kaufman: Backsliding (2021)

Stephan Haggard and Robert Kaufman's *Backsliding: Democratic Regress in the Contemporary World* provides the most systematic comparative analysis of recent democratic backsliding episodes. Analyzing 16 cases of democratic regression (including Hungary, Poland, Turkey, Venezuela, Nicaragua, and tentatively the US), they identify common patterns:

1. **Executive aggrandizement as the dominant mechanism:** In 14 of 16 cases, elected executives gradually eroded checks and balances.
2. **Polarization as the enabling condition:** In all 16 cases, extreme political polarization preceded and enabled backsliding by making supporters willing to tolerate norm violations by their preferred leaders.
3. **Economic grievance as a catalyst:** In most cases, economic dissatisfaction or inequality created the conditions for populist leaders to gain power.
4. **Institutional weakness as a vulnerability:** Countries with less institutional depth (newer democracies, weaker judiciaries, less media independence) were more vulnerable.

Key variables: executive power concentration, partisan polarization, economic grievance, institutional strength/weakness (Haggard and Kaufman 2021).

### Mounk: The Great Experiment and Democratic Deconsolidation (2018, 2022)

Yascha Mounk's *The People vs. Democracy* (2018) introduced the concept of "democratic deconsolidation" -- the idea that citizens in established democracies are becoming less committed to democratic governance. Using World Values Survey and Eurobarometer data, Mounk showed:

1. Declining percentages of citizens (especially younger generations) who rate "living in a democracy" as essential.
2. Growing openness to authoritarian alternatives (military rule, rule by a strong leader not constrained by parliament).
3. Increasing willingness to support antisystem parties and movements.

Mounk's later work, *The Great Experiment* (2022), focused on the specific challenge of diverse democracies maintaining social cohesion across racial, ethnic, and religious lines -- directly relevant to the US case (Mounk 2018, 2022).

**Variables generated:** Democratic commitment (survey-based), openness to authoritarian alternatives, anti-system party vote share, generational attitude shifts.

### Ginsburg and Huq: How to Save a Constitutional Democracy (2018)

Tom Ginsburg and Aziz Huq distinguished between "authoritarian reversion" (sudden collapse, as in a coup) and "constitutional retrogression" (gradual erosion of democratic norms while maintaining the formal structure of democracy). They argued that constitutional retrogression is the primary threat to established democracies because:

1. It operates within legal bounds -- each step may be formally legal.
2. It is incremental -- no single step is dramatic enough to trigger mass resistance.
3. It targets the infrastructure of democracy (courts, electoral administration, information environment) rather than democracy's formal structures (elections, legislatures, constitutions).

Their framework identifies five domains of democratic infrastructure vulnerable to retrogression: (1) competitive elections, (2) political and civil rights of speech and association, (3) the rule of law, (4) institutional integrity of the bureaucracy, and (5) the capacity for democratic contestation and deliberation (Ginsburg and Huq 2018).

### McCoy and Somer: Pernicious Polarization (2019)

Jennifer McCoy and Murat Somer's comparative research on "pernicious polarization" identifies it as the single most important precondition for democratic backsliding. Pernicious polarization occurs when:

1. A society divides into two political camps with mutually exclusive identities.
2. Political disagreements become framed as existential threats to group survival.
3. Normal democratic competition is perceived as a zero-sum game where the other side's victory threatens core values and identity.

Analyzing cases from Bangladesh to Hungary to Turkey to the US, McCoy and Somer find that pernicious polarization is both a cause and consequence of democratic erosion -- creating a vicious cycle where polarization enables norm-breaking which deepens polarization. Their work generates measurable variables: affective polarization (partisan antipathy), social distance between party supporters, perception of the other party as a threat, and the degree to which political identity subsumes other identities (McCoy and Somer 2019).

---

## Variables Discovered

| Variable | Measurement/Proxy | Studies | Direction | Notes |
|----------|------------------|---------|-----------|-------|
| Regime type / anocracy score | Polity V score; V-Dem indices; Freedom House ratings | Goldstone et al. 2010; Marshall and Gurr 2020; Walter 2022 | Movement toward anocracy -> higher failure risk | PITF's strongest predictor; partial democracies with factionalism at highest risk |
| Judicial independence | V-Dem v2juhcind; World Justice Project Rule of Law Index | V-Dem Institute 2023; Ginsburg and Huq 2018; Levitsky and Ziblatt 2018 | Declining independence -> higher backsliding risk | US-relevant: Supreme Court legitimacy crisis, judicial appointment politicization |
| Political polarization (affective) | Pew partisan antipathy surveys; ANES thermometer ratings; V-Dem v2cacamps | McCoy and Somer 2019; Haggard and Kaufman 2021; Kaufman and Haggard 2021 | Increasing polarization -> higher backsliding risk | Most consistent predictor across all 16 Haggard-Kaufman cases |
| Legislative constraints on executive | V-Dem v2xlg_legcon; congressional oversight activity; checks and balances index | V-Dem Institute 2023; Ginsburg and Huq 2018 | Weakening constraints -> higher backsliding risk | Measurable through V-Dem expert coding and congressional activity data |
| Freedom of expression / media independence | V-Dem v2x_freexp_altinf; Reporters Without Borders Press Freedom Index | V-Dem Institute 2023; Bermeo 2016 | Declining media freedom -> higher backsliding risk | US press freedom ranking has declined in recent years |
| Factionalized elites | PITF factionalism coding; V-Dem; partisan sorting measures | Goldstone et al. 2010; McCoy and Somer 2019; Walter 2022 | Increasing factionalism -> higher risk | Distinct from polarization: measures elite fragmentation specifically along identity lines |
| Executive aggrandizement actions | Count of norm-breaking executive actions; court-packing attempts; executive order frequency | Bermeo 2016; Haggard and Kaufman 2021; Ginsburg and Huq 2018 | Increasing aggrandizement -> higher backsliding risk | Difficult to quantify consistently; V-Dem's executive respect for constitution (v2exrescon) is a proxy |
| State legitimacy / public confidence | Gallup/Pew trust in government; voter turnout; protest frequency against government | Fund for Peace (FSI P1); Norris 2011; Dalton 2004 | Declining legitimacy -> higher risk | US trust in government at historic lows (~20%); FSI component P1 shows US decline |
| Partisan gerrymandering | Efficiency gap; seats-votes curve deviation; court challenges to redistricting | Grumbach 2023; Stephanopoulos and McGhee 2015 | Increasing gerrymandering -> higher backsliding risk | US-specific: measurable through redistricting data and legal challenges |
| Voter access restrictions | Voter ID law stringency; registration barriers; polling place closures | Grumbach 2023; Haggard and Kaufman 2021 | Increasing restrictions -> higher backsliding risk | Significant state-level variation in the US; measurable through state election law databases |
| Democratic commitment (attitudinal) | World Values Survey "importance of democracy"; support for authoritarian alternatives | Mounk 2018; Foa and Mounk 2016; Norris 2011 | Declining commitment -> higher risk | Generational differences significant: younger cohorts show lower democratic commitment |
| Horizontal inequality (between groups) | Racial income gap; racial wealth gap; group-based Gini | Cederman et al. 2013; Stewart 2008; Chetty et al. 2020 | Greater between-group inequality -> higher risk | US racial wealth gap is large and has distinctive political salience |
| Civil society density / strength | Number of CSOs per capita; union membership; NGO activity | Kaufman and Haggard 2021; Linz and Stepan 1996; Putnam 2000 | Declining civil society -> higher vulnerability | US union membership has declined from ~35% (1950s) to ~10% (2020s) |
| Infant mortality rate (state capacity proxy) | National infant mortality rate; under-5 mortality | Goldstone et al. 2010 (PITF) | Higher mortality -> higher failure risk | Not discriminating for US at national level; potentially relevant at county/state level |
| Neighborhood democratic quality | Average V-Dem score of ally/neighbor democracies | Goldstone et al. 2010 (PITF); Huntington 1991 | Declining neighborhood democracy -> higher risk | For the US, relevant "neighbors" are allied democracies; EU and Five Eyes backsliding trends |
| Anti-system party vote share | Vote share for parties rejecting democratic norms; populist party strength | Mounk 2018; Funke et al. 2016; Norris and Inglehart 2019 | Increasing anti-system vote -> higher risk | Measurable through election data; definition of "anti-system" is contested |
| Electoral integrity | Perception of Electoral Integrity (PEI) index; election monitoring findings | Norris 2014; Grumbach 2023 | Declining integrity -> higher backsliding risk | US PEI score has declined; significant state-level variation |
| Bureaucratic / institutional quality | World Governance Indicators; V-Dem bureaucratic quality measures | Hanson and Sigman 2021; Linz and Stepan 1996; Ginsburg and Huq 2018 | Declining quality -> higher vulnerability | US variation slow-moving but measurable through agency performance metrics, government shutdown frequency |
| Ethnic discrimination (state-led) | Minorities at Risk (MAR) coding; CERD reports; racial profiling data | Goldstone et al. 2010 (PITF); Cederman et al. 2013 | Presence of discrimination -> higher risk | US has persistent racial discrimination; PITF coding may not capture the US form adequately |
| Social media polarization / information ecosystem | Platform polarization metrics; misinformation prevalence; algorithmic amplification | Walter 2022; McCoy and Somer 2019; Bail et al. 2018 | Increasing info ecosystem degradation -> higher risk | Newer variable; measurement approaches still developing; data availability: `unknown` |

---

## Key Debates and Contested Findings

### 1. Institutional vs. Cultural Explanations for Democratic Resilience

**Institutional position (Ginsburg and Huq 2018, Levitsky and Ziblatt 2018):** Democracy is sustained by institutional design -- checks and balances, judicial independence, federalism, free press. Democratic erosion is fundamentally an institutional problem: institutions are either strong enough to constrain would-be authoritarians or they are not. The solution is institutional reform and defense.

**Cultural position (Mounk 2018, Norris and Inglehart 2019, Putnam 2000):** Democracy is sustained by democratic culture -- civic engagement, social trust, democratic values, tolerance of diversity. Institutional structures are downstream of cultural attitudes: if citizens lose faith in democracy, institutions cannot save it. The root causes of backsliding are cultural -- declining social capital, rising tribalism, eroding democratic commitment.

**Implication for variable selection:** Both dimensions matter. The project should include institutional variables (V-Dem component scores, judicial independence) and cultural variables (democratic commitment, social trust, civic participation). The debate suggests that their interaction -- strong institutions in a polarized culture, or weak institutions in a civic culture -- may be more predictive than either alone.

### 2. Elite-Driven vs. Mass-Driven Backsliding

**Elite-driven (Bermeo 2016, Haggard and Kaufman 2021):** Democratic backsliding is overwhelmingly elite-driven. It is elected leaders who pack courts, restrict media, manipulate elections, and erode norms. Mass publics are largely passive or permissive -- they tolerate backsliding by their preferred leaders but do not demand it.

**Mass-driven (Mounk 2018, Norris and Inglehart 2019):** Democratic deconsolidation at the mass level creates the permissive conditions for elite-driven backsliding. When a significant share of the public is open to authoritarian alternatives, elites face no electoral punishment for norm-breaking behavior.

**Synthesis (McCoy and Somer 2019):** The relationship is bidirectional. Elites drive backsliding, but mass polarization enables it. Pernicious polarization is the mechanism that links mass attitudes to elite behavior -- when voters see the other side as an existential threat, they tolerate norm violations by their own side. The critical variable is not "who drives backsliding" but "what enables elites to get away with it."

### 3. Is the US Actually Backsliding?

**Yes (V-Dem Institute, Walter 2022, Diamond 2022, Levitsky and Ziblatt 2018):** The US has experienced measurable democratic erosion by multiple indicators. V-Dem codes a decline in the Liberal Democracy Index. Polity V registered a decline (and controversially restored the score after review). Press freedom rankings have fallen. Norm-breaking behavior by elected officials has increased. The January 6, 2021, assault on the Capitol was unprecedented in modern US history.

**No / it's complicated (Svolik 2019, Graham and Svolik 2020, Przeworski 2019):** The US has deep institutional infrastructure that makes it fundamentally different from the developing-country cases in the backsliding literature. The judiciary remains independent. The military is professional and apolitical. Federal structure provides multiple veto points. The US has experienced periods of worse democratic quality (Jim Crow era, McCarthyism) and recovered. Current trends may reflect normal democratic turbulence rather than systemic erosion.

**Conditional position (Grumbach 2023):** The US is backsliding -- but unevenly across states. National-level measures miss the critical variation: some states are becoming more democratic, others significantly less so. The relevant unit of analysis is the state, not the nation.

**Implication:** The project should include both national-level and state-level democratic quality measures. The debate about whether the US is "really" backsliding highlights the importance of transparent measurement -- using concrete, observable indicators rather than subjective assessments.

### 4. The Polarization Paradox

**Problem:** Political polarization is the most consistently cited predictor of democratic backsliding in the literature (McCoy and Somer 2019, Haggard and Kaufman 2021, Kaufman and Haggard 2021). But polarization also exists in healthy democracies as a normal feature of democratic competition. How to distinguish "normal" polarization from "pernicious" polarization that threatens democracy?

**Affective vs. ideological:** Some scholars argue that ideological polarization (disagreement on policy) is healthy, while affective polarization (visceral hostility toward the other party and its supporters) is dangerous. The US has experienced dramatic increases in affective polarization since the 1990s even as ideological polarization on many issues remains moderate (Iyengar et al. 2019; Mason 2018).

**Threshold effects:** McCoy and Somer (2019) argue that polarization becomes "pernicious" when it reaches a threshold where political identity subsumes all other identities and normal democratic competition is perceived as existential. There is no consensus on where this threshold lies numerically.

**Implication:** Polarization should be measured on multiple dimensions (affective, ideological, behavioral) and tracked as a trend rather than interpreted at any single level.

---

## US Applicability Assessment

### Tier 1: Directly Applicable (variable varies meaningfully over US history)

| Variable | US Variation | Key Data |
|----------|-------------|----------|
| Political polarization (affective) | Partisan antipathy doubled since 1994; social distance between partisans at record levels | Pew surveys, ANES, V-Dem |
| Judicial independence | Supreme Court legitimacy under stress; judicial appointment battles intensifying | V-Dem v2juhcind, approval ratings |
| Legislative constraints on executive | Varies with unified/divided government; executive power has expanded steadily | V-Dem v2xlg_legcon, executive orders |
| State legitimacy / government trust | Declined from ~75% (1960s) to ~20% (2020s) | Gallup, Pew |
| Factionalized elites | Congressional bipartisanship collapsed since 1990s; cross-party cooperation at historic lows | DW-NOMINATE, congressional vote data |
| Voter access / electoral integrity | Significant state-level variation; VRA weakening since 2013 | Grumbach State Democracy Index, NCSL data |
| Partisan gerrymandering | Major shifts with each redistricting cycle; efficiency gaps measurable | Redistricting data, court filings |
| Civil society density | Union membership declined from ~35% to ~10%; civic association membership declining | BLS, Putnam data, IRS nonprofit filings |
| Anti-system party vote share | Measurable through third-party votes and within-party anti-establishment candidates | FEC election data |
| Executive aggrandizement (proxy) | Executive order frequency; norm-breaking actions; V-Dem coding | V-Dem v2exrescon, executive records |
| Horizontal inequality (racial) | Persistent racial income and wealth gaps with temporal variation | Census, Fed SCF, BLS |
| Social media / information ecosystem | Platform polarization; misinformation prevalence growing | Pew media surveys, academic studies |

### Tier 2: Applicable with Adaptation (concept transfers but measurement needs US-specific proxy)

| Variable | Adaptation Needed | Suggested US Proxy |
|----------|------------------|--------------------|
| Regime type / anocracy | US Polity score is contested; blunt instrument for a complex democracy | V-Dem component scores; Grumbach state-level index; disaggregate into institutional dimensions rather than single score |
| Democratic commitment (attitudinal) | Survey data available but US-specific wording differs from WVS standard | ANES questions on democratic norms; Pew governance preferences; WVS with US-specific weighting |
| Bureaucratic quality | WGI has minimal US variation; need granular measures | Government shutdown frequency; agency staffing levels; inspector general independence; GAO reports |
| Freedom of expression / media | Reporters Without Borders captures US but at national level only | Media diversity indices; local news desert data; platform content moderation metrics |
| Neighborhood democratic quality | Geographic neighbors not relevant; ideological/alliance neighbors matter | Average V-Dem score for NATO/Five Eyes/G7 democracies; democratic erosion in allied states |

### Tier 3: Not Applicable (US at floor/ceiling, no meaningful variation)

| Variable | Why Not Applicable | US Status |
|----------|--------------------|-----------|
| Infant mortality (PITF proxy) | US consistently in low-mortality group globally; does not discriminate | Bottom quintile globally; state-level variation exists but small relative to PITF training range |
| Ethnic discrimination (PITF coding) | MAR coding scheme captures state-led legal discrimination; US has informal/structural rather than formal discrimination | US form of discrimination not well-captured by PITF's MAR-based measure |
| Neighborhood armed conflict (PITF) | No neighboring countries in armed conflict | Geographic neighbors (Canada, Mexico) not in PITF-defined conflict |
| Refugees/IDPs (FSI S2) | US does not have significant internal displacement pressures | Floor of the FSI scale for this component |
| Human flight/brain drain (FSI E3) | US remains a net attractor of talent | Floor of the FSI scale for this component |

---

## Bibliography

Bail, Christopher A., et al. 2018. "Exposure to Opposing Views on Social Media Can Increase Political Polarization." *Proceedings of the National Academy of Sciences* 115(37): 9216-9221.

Bermeo, Nancy. 2016. "On Democratic Backsliding." *Journal of Democracy* 27(1): 5-19.

Cederman, Lars-Erik, Kristian S. Gleditsch, and Halvard Buhaug. 2013. *Inequality, Grievances, and Civil War.* Cambridge University Press.

Chetty, Raj, et al. 2020. "Race and Economic Opportunity in the United States: An Intergenerational Perspective." *Quarterly Journal of Economics* 135(2): 711-783.

Dalton, Russell J. 2004. *Democratic Challenges, Democratic Choices: The Erosion of Political Support in Advanced Industrial Democracies.* Oxford University Press.

Diamond, Larry. 2022. "Democracy's Arc: From Resurgent to Imperiled." *Journal of Democracy* 33(1): 163-179.

Esty, Daniel C., et al. 1995. *State Failure Task Force Report.* Science Applications International Corporation.

Foa, Roberto Stefan, and Yascha Mounk. 2016. "The Danger of Deconsolidation: The Democratic Disconnect." *Journal of Democracy* 27(3): 5-17.

Fund for Peace. 2023. *Fragile States Index Annual Report 2023.* Washington, DC: Fund for Peace.

Ginsburg, Tom, and Aziz Z. Huq. 2018. *How to Save a Constitutional Democracy.* University of Chicago Press.

Goldstone, Jack A., et al. 2000. *State Failure Task Force Report: Phase III Findings.* Science Applications International Corporation.

Goldstone, Jack A., Robert H. Bates, David L. Epstein, Ted Robert Gurr, Michael B. Lustik, Monty G. Marshall, Jay Ulfelder, and Mark Woodward. 2010. "A Global Model for Forecasting Political Instability." *American Journal of Political Science* 54(1): 190-208.

Graham, Matthew H., and Milan W. Svolik. 2020. "Democracy in America? Partisanship, Polarization, and the Robustness of Support for Democracy in the United States." *American Political Science Review* 114(2): 392-409.

Grumbach, Jacob M. 2023. "Laboratories of Democratic Backsliding." *American Political Science Review* 117(3): 967-984.

Haggard, Stephan, and Robert Kaufman. 2021. *Backsliding: Democratic Regress in the Contemporary World.* Cambridge University Press.

Hanson, Jonathan K., and Rachel Sigman. 2021. "Leviathan's Latent Dimensions: Measuring State Capacity for Comparative Political Research." *Journal of Politics* 83(4): 1495-1510.

Huntington, Samuel P. 1991. *The Third Wave: Democratization in the Late Twentieth Century.* University of Oklahoma Press.

Iyengar, Shanto, Yphtach Lelkes, Matthew Levendusky, Neil Malhotra, and Sean J. Westwood. 2019. "The Origins and Consequences of Affective Polarization in the United States." *Annual Review of Political Science* 22: 129-146.

Kaufman, Robert, and Stephan Haggard. 2021. "Democratic Resilience." Annual Workshop Report, Institute on Global Conflict and Cooperation, UC San Diego.

Levitsky, Steven, and Daniel Ziblatt. 2018. *How Democracies Die.* Crown Publishing.

Linz, Juan J. 1978. *The Breakdown of Democratic Regimes: Crisis, Breakdown, and Reequilibration.* Johns Hopkins University Press.

Linz, Juan J., and Alfred Stepan. 1996. *Problems of Democratic Transition and Consolidation: Southern Europe, South America, and Post-Communist Europe.* Johns Hopkins University Press.

Luhrmann, Anna, and Staffan I. Lindberg. 2019. "A Third Wave of Autocratization Is Here: What Is New About It?" *Democratization* 26(7): 1095-1113.

Marshall, Monty G., and Ted Robert Gurr. 2020. *Polity5: Political Regime Characteristics and Transitions, 1800-2018.* Center for Systemic Peace.

Mason, Lilliana. 2018. *Uncivil Agreement: How Politics Became Our Identity.* University of Chicago Press.

McCoy, Jennifer, and Murat Somer. 2019. "Toward a Theory of Pernicious Polarization and How It Harms Democracies: Comparative Evidence and Possible Remedies." *Annals of the American Academy of Political and Social Science* 681(1): 234-271.

Mounk, Yascha. 2018. *The People vs. Democracy: Why Our Freedom Is in Danger and How to Save It.* Harvard University Press.

Mounk, Yascha. 2022. *The Great Experiment: Why Diverse Democracies Fall Apart and How They Can Endure.* Penguin Press.

Norris, Pippa. 2011. *Democratic Deficit: Critical Citizens Revisited.* Cambridge University Press.

Norris, Pippa. 2014. *Why Electoral Integrity Matters.* Cambridge University Press.

Norris, Pippa, and Ronald Inglehart. 2019. *Cultural Backlash: Trump, Brexit, and Authoritarian Populism.* Cambridge University Press.

O'Donnell, Guillermo, and Philippe C. Schmitter. 1986. *Transitions from Authoritarian Rule: Tentative Conclusions about Uncertain Democracies.* Johns Hopkins University Press.

Przeworski, Adam. 2019. *Crises of Democracy.* Cambridge University Press.

Putnam, Robert D. 2000. *Bowling Alone: The Collapse and Revival of American Community.* Simon & Schuster.

Stephanopoulos, Nicholas O., and Eric M. McGhee. 2015. "Partisan Gerrymandering and the Efficiency Gap." *University of Chicago Law Review* 82(2): 831-900.

Stewart, Frances. 2008. *Horizontal Inequalities and Conflict: Understanding Group Violence in Multiethnic Societies.* Palgrave Macmillan.

Svolik, Milan W. 2019. "Polarization versus Democracy." *Journal of Democracy* 30(3): 20-32.

V-Dem Institute. 2020. *Autocratization Surges -- Resistance Grows: Democracy Report 2020.* University of Gothenburg.

V-Dem Institute. 2021. *Autocratization Turns Viral: Democracy Report 2021.* University of Gothenburg.

V-Dem Institute. 2023. *Defiance in the Face of Autocratization: Democracy Report 2023.* University of Gothenburg.

V-Dem Institute. 2024. *Democracy Report 2024.* University of Gothenburg.

Walter, Barbara F. 2022. *How Civil Wars Start: And How to Stop Them.* Crown Publishing.
