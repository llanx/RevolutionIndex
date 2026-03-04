# Literature Review: Social Movement Theory and Collective Action

## Scope

This review covers the adjacent domain of social movement theory and collective action research. While the core revolution prediction domains (Plans 01-04) ask "what structural conditions produce instability?", this domain asks the complementary question: **"what determines whether structural conditions translate into actual collective action?"**

The domain encompasses:
- **Protest and social movements**: Why people mobilize, how movements form, what determines their scale and persistence
- **Civil resistance and nonviolent campaigns**: Large-scale organized challenges to authority, effectiveness conditions
- **Mobilization dynamics**: Thresholds, cascades, tipping points in participation decisions
- **Collective action theory**: The free-rider problem, selective incentives, identity-based mobilization

**Boundary with core domains**: Revolution prediction (Domain 1) studies outcomes -- regime change, state collapse. This domain studies the *mechanism* through which grievances become action. Democratic backsliding (Domain 2) studies institutional erosion from above; this domain studies pressure from below. Historical case studies (Domain 3) analyze full revolutionary episodes; this domain isolates the mobilization component.

**Value for the Revolution Index**: This domain contributes variables that measure *mobilization capacity* and *recent mobilization history* -- the transmission mechanism between structural stress (measured by PSI, PLI, FSP-type variables) and actual political instability. A country can have severe structural stress but no instability if mobilization capacity is low; conversely, modest structural stress can produce significant instability when mobilization infrastructure is strong and recently activated.

---

## Foundational Works

### Mancur Olson -- The Logic of Collective Action (1965)

Olson established the fundamental paradox of collective action: rational, self-interested individuals will not voluntarily contribute to a public good (like political change) because they can free-ride on others' efforts. This framing dominated the field for two decades and forced all subsequent theorists to explain *how* mobilization overcomes the free-rider problem.

**Key contribution**: The collective action problem is the baseline against which all mobilization variables must be evaluated. Variables that measure how groups solve this problem (selective incentives, organizational infrastructure, identity-based motivation) are theoretically grounded in Olson's framework.

### McCarthy and Zald -- Resource Mobilization Theory (1977)

McCarthy and Zald shifted the study of social movements away from grievance-based explanations (people rebel because they are angry) toward organizational and resource-based explanations. They argued that grievances are nearly constant -- what varies is the availability of resources (money, labor, legitimacy, organizational infrastructure) that allow movements to form and sustain themselves.

**Key variables introduced**: Organizational density, resource availability, professional movement organizations, elite patronage of movements.

**Implication for Revolution Index**: If resource mobilization theory is correct, structural grievances (measured by PSI-type variables) are necessary but insufficient. Organizational infrastructure variables must be measured independently.

### McAdam -- Political Process Model (1982)

McAdam proposed three necessary conditions for social movement emergence: (1) expanding political opportunities (openings in the political system), (2) indigenous organizational strength (pre-existing organizations and networks), and (3) cognitive liberation (the collective belief that change is possible and action is worthwhile).

**Key variables introduced**: Political opportunity structure, organizational readiness, insurgent consciousness.

**Empirical basis**: McAdam's study of the Black civil rights movement (1930-1970) showed that organizational infrastructure (Black churches, NAACP chapters, historically Black colleges) was essential for translating grievances into sustained mobilization.

### Tarrow -- Power in Movement (1994, 2011)

Tarrow synthesized resource mobilization and political process approaches, emphasizing **cycles of contention** -- periods when political opportunities, mobilizing structures, and cultural frames align to produce waves of collective action that spread across groups and issues.

**Key variables introduced**: Protest cycles (frequency and clustering of contentious episodes), modular repertoires of contention (transferable protest tactics), political opportunity structure (elite divisions, institutional access, alignment of allies).

**Relevance**: Tarrow's concept of protest cycles is directly measurable via protest event data (ACLED, Mass Mobilization Project). The clustering of protest activity may be a leading indicator distinct from any single protest event.

### Tilly -- Contentious Politics (2004, with Tarrow)

Tilly and Tarrow's synthetic framework argues that contentious politics (including protest, social movements, civil war, and revolution) shares common causal mechanisms: brokerage (connecting previously unconnected actors), diffusion (spread of contention), coordinated action, category formation, and certification (validation by external authorities).

**Key contribution**: The framework treats protest, social movements, and revolution as points on a continuum of contentious politics, not distinct phenomena. This supports the Revolution Index approach of measuring mobilization dynamics as a component of broader instability risk.

### Snow and Benford -- Frame Alignment Theory (1986, 1988)

Snow and Benford argued that successful mobilization requires "frame alignment" between a movement's message and potential participants' beliefs. They identified four alignment processes: frame bridging, frame amplification, frame extension, and frame transformation. Effective framing involves diagnostic framing (identifying the problem), prognostic framing (proposing a solution), and motivational framing (providing a rationale for action).

**Key variables introduced**: Frame resonance, cultural compatibility of movement messaging.

**Measurement challenge**: Framing resonance is difficult to measure quantitatively. Indirect proxies include movement media coverage tone, public opinion alignment with movement goals, and social media engagement with movement narratives.

---

## Core Empirical Studies

### Chenoweth and Stephan -- Why Civil Resistance Works (2011)

The most influential quantitative study in the field. Using the NAVCO 1.0 dataset covering 323 major resistance campaigns from 1900-2006, Chenoweth and Stephan found that nonviolent campaigns succeeded 53% of the time versus 26% for violent campaigns. The study identified campaign participation size as the single strongest predictor of success.

**Key findings:**
- Campaigns achieving participation of at least 3.5% of the population always succeeded (the "3.5% rule")
- Security force defections were a critical mechanism: nonviolent campaigns were more likely to produce loyalty shifts in military and police
- Campaign diversity (participation across demographics, regions, and social classes) independently predicted success
- Nonviolent discipline (maintaining nonviolence despite repression) increased success probability

**Variables extracted**: Campaign participation rate, security force loyalty/defection, campaign diversity/coalition breadth, nonviolent discipline maintenance.

**Limitations**: The unit of analysis is the campaign, not the country-year. The 3.5% threshold operates at the level of organized campaigns, not as a continuous time-series predictor. The dataset codes maximalist campaigns (regime change, territorial independence, anti-occupation), not routine protest.

### NAVCO Dataset Extensions

The Nonviolent and Violent Campaigns and Outcomes (NAVCO) project has expanded through multiple versions:

- **NAVCO 1.1** (Chenoweth and Lewis 2013): Updated to 389 campaigns through 2013 with additional covariates
- **NAVCO 2.1** (Chenoweth and Shay 2020 [UNVERIFIED]): Annual-level data for campaigns, enabling within-campaign longitudinal analysis
- **NAVCO 3.0** (Chenoweth and Pinckney 2021 [UNVERIFIED]): Event-level data for 21 countries, 1991-2012, with over 100,000 events

**Relevance**: NAVCO data is coded at the campaign level, making it most useful for understanding what drives campaign outcomes. For the Revolution Index (which operates at the country-year level), NAVCO's primary value is establishing which variables predict campaign emergence and escalation.

### Beissinger -- Nationalist Mobilization and the Collapse of the Soviet State (2002)

Beissinger's study of the Soviet collapse is the seminal work on **diffusion and contagion** in mobilization. He showed that protest events in one Soviet republic increased the probability of protest in neighboring republics, with a decay function based on temporal and spatial distance.

**Key findings:**
- Demonstration effects: successful protests in one context embolden actors in similar contexts
- Tide effects: mobilization waves build momentum; early risers face higher costs, later joiners face lower costs as the regime weakens
- Threshold dynamics: there is a critical mass of early mobilization beyond which cascading effects take over

**Variables extracted**: Protest contagion/diffusion (spatial and temporal clustering), prior protest success rate, protest momentum (acceleration in event frequency).

### Kuran -- Now Out of Never: The Element of Surprise in the East European Revolution of 1989 (1991)

Kuran's model of **preference falsification** explains why revolutions appear sudden. In repressive contexts, individuals conceal their true preferences (opposition to the regime). The public distribution of expressed preferences vastly understates actual opposition. When some exogenous event (economic crisis, leadership transition, external pressure) reduces the cost of dissent, a preference cascade can occur: a few courageous individuals express opposition, which lowers the threshold for others, who in turn lower it further.

**Key variables introduced**: Preference falsification gap (difference between expressed and actual preferences), threshold heterogeneity (distribution of individual willingness to participate), triggering events.

**Measurement challenge**: Preference falsification is inherently difficult to measure because the entire phenomenon involves concealment. Indirect proxies include sudden opinion poll shifts, gap between survey responses and actual behavior, and rapid changes in protest participation.

**US relevance**: While preference falsification is most extreme under authoritarian repression, it operates in democratic contexts through social desirability bias, spiral of silence effects, and "shy voter" phenomena. The gap between poll predictions and election outcomes may be a weak proxy.

### Lohmann -- The Dynamics of Informational Cascades (1994)

Lohmann's formal model of protest participation treats protests as signals about regime vulnerability. Each protest event provides information to potential participants about the likelihood of regime change. As more people protest, the perceived probability of success increases, lowering the threshold for additional participation.

**Key variables introduced**: Information signal strength (size and visibility of prior protests), regime uncertainty (how much new information each protest reveals).

**Relevance**: Lohmann's model supports the intuition that protest frequency and size are leading indicators: rising protest signals regime vulnerability and lowers mobilization thresholds for subsequent action.

### Granovetter -- Threshold Models of Collective Behavior (1978)

Granovetter's threshold model formalizes the intuition that individuals differ in their willingness to participate in collective action. Each person has a threshold -- the proportion of others who must participate before they will join. The distribution of these thresholds in a population determines whether a small spark can produce a cascade or will fizzle.

**Key insight**: Two populations with identical average grievances can have radically different mobilization outcomes depending on the distribution of individual thresholds. A population with many low-threshold individuals (willing to act early) can produce cascading mobilization; a population where most people have high thresholds will remain quiescent even under severe structural stress.

**Measurement implications**: Direct threshold measurement is impractical. Proxies include prior protest participation (individuals who have protested before have lower thresholds for future action), union membership (pre-committed participants), and political engagement measures.

### Klandermans -- The Social Psychology of Protest (1997, 2004)

Klandermans synthesized social-psychological approaches to protest participation, identifying four key determinants: (1) perceived grievance injustice, (2) perceived efficacy (belief that participation can make a difference), (3) social identification with the aggrieved group, and (4) emotional engagement (anger, moral outrage).

**Key contribution**: This framework explains why structural conditions alone do not predict mobilization -- the subjective interpretation of conditions matters. Two populations experiencing the same economic decline may respond differently depending on whether they perceive it as unjust (vs. natural/inevitable) and whether they believe collective action can address it.

**Variables extracted**: Perceived injustice levels (survey-based), political efficacy beliefs, group identity strength.

---

## Recent Developments (2020-2025)

### BLM 2020: Largest Protest Movement in US History

The Black Lives Matter protests following the killing of George Floyd in May 2020 became the largest protest movement in US history by participation. Estimates suggest 15-26 million people participated in the US alone (Buchanan, Bui, and Patel 2020, New York Times).

**Key findings from BLM 2020 research:**
- **Scale**: Participation far exceeded the 3.5% threshold at the national level (approximately 5-8% of the US population participated in at least one event), though this was dispersed across hundreds of localities rather than concentrated in a single campaign [UNVERIFIED precise percentage]
- **Decentralized mobilization**: BLM 2020 was notable for the absence of central coordination; social media and local networks drove mobilization independently (Fisher et al. 2022 [UNVERIFIED])
- **Sustained duration**: Protests continued for months, with major events in over 2,000 cities and towns across the US
- **Counter-mobilization**: BLM 2020 also generated significant counter-mobilization, highlighting polarization as a factor in protest dynamics

**Relevance for Revolution Index**: BLM 2020 demonstrates that the US is fully capable of mass mobilization at historically unprecedented levels. The variables that predicted BLM participation -- racial justice grievances, social media activation, prior protest experience, pandemic-driven availability -- are measurable.

### COVID-Era Protest Dynamics

The COVID-19 pandemic produced a complex protest environment:
- **Lockdown protests** (anti-mask, anti-vaccine, re-open movements) mobilized a different demographic than BLM
- **Pandemic-driven availability**: Lockdowns, unemployment, and remote work may have lowered the opportunity cost of protest participation (Barber and English 2021 [UNVERIFIED])
- **January 6, 2021**: The US Capitol attack represents a distinct mobilization pathway -- elite-directed, heavily mediated through social media and conspiratorial narratives, resulting in violent collective action aimed at disrupting institutional processes

**Variables extracted**: Pandemic-disrupted routine (availability for protest), digital mobilization infrastructure, elite-directed vs. grassroots mobilization pathways.

### The 3.5% Rule: Debate and Updates

Chenoweth's 3.5% threshold has faced sustained academic scrutiny:

- **Nepstad (2011, 2015)**: Argued that security force defections, not participation size alone, are the critical mechanism. Campaigns can fail despite large participation if the military remains loyal.
- **Pinckney (2020) [UNVERIFIED]**: Examined the role of organized labor in civil resistance, finding that labor union participation significantly increases campaign success probability independent of overall participation size.
- **Chenoweth (2020, "The Future of Civil Resistance")**: Updated and qualified the threshold, acknowledging it as a descriptive pattern rather than a deterministic law. Context, regime type, campaign strategy, and security force behavior all moderate the relationship between participation and success.

**Current consensus**: Large-scale participation matters, but the specific 3.5% number is better understood as a rough empirical regularity than a universal law. The underlying mechanism (regime costs increase faster than linearly with participation) is widely accepted.

### Digital Mobilization Research

The role of social media in protest mobilization has produced a substantial body of research:

- **Tufekci (2017, "Twitter and Tear Gas")**: Argued that digital tools enable rapid mobilization but may weaken organizational capacity. "Tactical frivolity" -- easy mobilization without the hard organizational work that builds durable movements.
- **Jost et al. (2018) [UNVERIFIED]**: Meta-analysis of social media and collective action; found social media facilitates coordination but does not replace pre-existing organizational infrastructure.
- **Gonzalez-Bailon et al. (2011)**: Studied protest cascades on social media, finding that broadcast messages from central nodes (not peer-to-peer diffusion) drive most recruitment.
- **Steinert-Threlkeld et al. (2015) [UNVERIFIED]**: Used geolocated tweets to predict protest participation, finding that social media coordination signals predicted next-day protest size.

**Key variable implications**: Social media political engagement is measurable (Twitter/X political content volume, protest-related hashtag frequency) but the causal direction is debated -- social media may reflect mobilization rather than cause it.

### Mass Mobilization Project Findings

The Mass Mobilization Project (Clark and Regan 2016) codes over 10,000 protest events across 162 countries from 1990-2020, focusing on protests with 50+ participants against the government.

**Key findings relevant to the US:**
- Protest frequency has increased globally since the mid-2000s, with a sharp acceleration after 2010
- Economic grievances (wages, cost of living, employment) are the most common protest demands globally, but political/civil rights demands dominate in established democracies
- Government response type (accommodation, ignore, arrests, violence) predicts subsequent protest escalation
- Protest clustering (events occurring in rapid succession) is a stronger predictor of political instability than isolated large events

---

## Variables Discovered

| Variable | Measurement/Proxy | Studies | Direction | Notes |
|----------|-------------------|---------|-----------|-------|
| Protest frequency | Count of protest events per period (ACLED, Mass Mobilization Project, Count Love for US) | Tarrow 1994; Clark and Regan 2016; ACLED data | Higher frequency -> higher instability risk | Directly measurable for US via ACLED and Count Love databases; annual and monthly counts available |
| Protest size/participation | Estimated participants per event or total participants per period | Chenoweth and Stephan 2011; Buchanan et al. 2020 | Larger participation -> higher instability risk | Measurement is noisy -- crowd size estimates vary by factor of 2-5x; trend matters more than absolute level |
| Organizational density | Count of civil society organizations, NGOs, unions, associations per capita | McCarthy and Zald 1977; McAdam 1982 | Higher density -> higher mobilization capacity (not directly instability, but amplifies structural grievances) | Union membership from BLS is the most reliable US proxy; broader NGO counts harder to measure systematically |
| Union membership/density | Union members as % of labor force | Pinckney 2020 [UNVERIFIED]; historical US labor data (BLS) | Declining union density may indicate lower organized mobilization capacity but higher unorganized grievance | BLS publishes annual data; US union density declined from 35% (1954) to ~10% (2024); complex relationship -- both very high and very low density may be associated with instability |
| Prior protest experience | Proportion of population with recent protest participation history | Klandermans 1997; Granovetter 1978 (threshold models) | Higher prior participation -> lower thresholds for future mobilization | Measurable via survey data (Pew, ANES); BLM 2020 produced a large cohort of first-time protesters |
| Security force behavior | Military/police response to protests (accommodation vs. repression) | Chenoweth and Stephan 2011; Nepstad 2011 | Defection/accommodation -> higher regime vulnerability; repression -> mixed (can deter or escalate) | Not directly measurable via federal data; proxy indicators might include police use-of-force incidents, military morale surveys |
| Coalition breadth/diversity | Cross-demographic, cross-class, cross-regional participation in movements | Chenoweth and Stephan 2011 | Broader coalitions -> more effective campaigns, higher instability risk | Measurable only during active campaigns via event coding; not a continuous time-series variable |
| Protest diffusion/contagion | Spatial and temporal clustering of protest events | Beissinger 2002; Gonzalez-Bailon et al. 2011 | Clustering/acceleration -> cascade risk, higher instability | Measurable from ACLED/protest event data using event sequence analysis; requires event-level (not annual) data |
| Political efficacy beliefs | Survey-measured belief that collective action can influence outcomes | Klandermans 1997, 2004 | Higher efficacy -> more mobilization willingness | Measurable via ANES, Pew; but surveys are intermittent, not continuous time-series |
| Movement framing resonance | Alignment between movement messaging and public grievances | Snow and Benford 1986; Tarrow 1994 | Higher resonance -> more effective mobilization | Very difficult to measure quantitatively; social media engagement with movement content may be a weak proxy |
| Preference falsification gap | Difference between expressed and actual political preferences | Kuran 1991 | Larger gap -> higher surprise cascade risk | Inherently difficult to measure; poll prediction errors and "shy voter" effects are indirect proxies |
| Digital mobilization capacity | Social media political engagement, protest coordination via digital platforms | Tufekci 2017; Gonzalez-Bailon et al. 2011; Steinert-Threlkeld et al. 2015 [UNVERIFIED] | Higher digital engagement -> faster mobilization, but potentially weaker organizational depth | Measurable via social media APIs (with increasing restrictions); not available from federal data sources |

---

## Key Debates and Contested Findings

### The 3.5% Threshold: Universal Law or Empirical Regularity?

**Position 1 (Chenoweth and Stephan 2011)**: No campaign that achieved active participation of 3.5% of the population failed to achieve its stated objectives. This implies a near-deterministic relationship between participation and success at sufficiently high levels.

**Position 2 (Nepstad 2011, 2015; Chenoweth 2020 update)**: The 3.5% figure is a descriptive finding from historical campaigns, not a causal law. The mechanism is mediated by security force loyalty, regime type, international context, and campaign strategy. Campaigns with 1-2% participation have succeeded when security forces defected; campaigns exceeding 3.5% could theoretically fail if the military remains cohesive and loyal.

**Current status**: The debate has shifted from "is 3.5% the right number?" to "what mechanisms make large participation effective?" The academic consensus accepts that participation size matters but rejects simple threshold models. For the Revolution Index, this means protest participation is a continuous variable, not a binary threshold trigger.

### Resource Mobilization vs. Grievance-Driven Models

**Resource mobilization (McCarthy and Zald 1977; McAdam 1982)**: Grievances are nearly constant; organizational resources determine whether mobilization occurs. The prediction: mobilization capacity variables (organizational density, resources, leadership) are more important than grievance variables (inequality, deprivation).

**Grievance-driven models (Gurr 1970; Turchin 2003)**: Structural conditions -- particularly relative deprivation and the gap between expectations and reality -- are the primary drivers. Resources modulate the form and effectiveness of mobilization but do not determine whether it occurs.

**Synthesis (Tarrow 1994; McAdam, Tarrow, and Tilly 2001)**: Both matter. Structural conditions create the potential for mobilization; organizational infrastructure and political opportunities determine whether and how that potential is realized. The "contentious politics" synthesis treats grievances, resources, and opportunities as jointly necessary.

**Implications for Revolution Index**: This debate supports including *both* structural grievance variables (from core domains) *and* mobilization capacity variables (from this domain) in the model. Neither alone is sufficient. The synthesis view suggests interaction effects may be important -- organizational density matters more when grievances are high.

### Online vs. Offline Mobilization Effectiveness

**Digital optimists (Shirky 2008)**: Social media dramatically lowers the cost of coordination, enabling rapid large-scale mobilization. The Arab Spring and BLM 2020 demonstrate that digital tools can produce mass movements without traditional organizational infrastructure.

**Digital skeptics (Gladwell 2010; Morozov 2011)**: "Slacktivism" -- online engagement produces shallow commitment. Digital mobilization lacks the strong ties and organizational discipline that sustain movements under repression. Easy in, easy out.

**Nuanced middle (Tufekci 2017)**: Digital tools accelerate the early stages of mobilization (awareness, coordination, tactical communication) but may short-circuit the organizational development that builds durable movements. Movements mobilized primarily through social media may be "organizationally fragile" -- large but easily disrupted.

**Current evidence**: BLM 2020 supports the nuanced view -- massive digital mobilization produced unprecedented scale but limited durable organizational infrastructure. The US Capitol attack on January 6 shows a different pattern: digital mobilization through closed platforms (Parler, private groups) can produce violent action but at much smaller scale.

**Implications**: Digital mobilization metrics (social media political engagement) capture something real but should not be treated as equivalent to organizational density. They may be better understood as amplifiers of underlying grievances and facilitators of tactical coordination rather than independent predictors.

---

## US Applicability Assessment

### Directly Applicable Variables

These variables are measurable for the US over time and have demonstrated variation:

| Variable | US Data Source | Coverage | Assessment |
|----------|---------------|----------|------------|
| Protest frequency | ACLED-US (2020-present), Count Love (2017-present), Mass Mobilization Project (1990-2020) | Monthly or event-level | Directly measurable; multiple overlapping sources |
| Union membership/density | BLS, Current Population Survey | Annual, 1973-present (earlier data available) | High-quality, continuous federal data series |
| Prior protest participation | ANES, Pew Research Center surveys | Biennial or periodic surveys | Survey-based; not continuous time-series |
| Political efficacy beliefs | ANES, Pew surveys | Biennial or periodic surveys | Survey-based; not continuous time-series |
| Protest size (estimated) | ACLED-US, Count Love, media reports | Event-level, 2017-present (systematic) | Measurement is noisy but trend direction is reliable |

### Applicable with Adaptation

These variables exist conceptually in the US but require adaptation of measurement approaches developed in other contexts:

| Variable | Adaptation Needed | Potential US Proxy |
|----------|-------------------|-------------------|
| Organizational density | Most measures developed for developing-country NGO landscapes | US could use IRS nonprofit registrations per capita, professional association membership rates |
| Protest diffusion/contagion | Models developed for Soviet collapse, Arab Spring | Apply spatial/temporal clustering analysis to ACLED-US event data |
| Security force behavior | Coded for military responses in autocracies | US proxy: police use-of-force trends, National Guard deployments, federal-local law enforcement conflicts |
| Preference falsification | Strongest in authoritarian contexts with severe repression | US proxy: poll prediction errors, social desirability bias measures, "shy voter" effects |
| Digital mobilization capacity | Rapidly changing platform landscape | Social media political content volume; platform-specific engagement metrics with access increasingly restricted |

### Not Directly Applicable

| Variable | Reason |
|----------|--------|
| Campaign-level NAVCO coding | NAVCO codes maximalist campaigns (regime change); the US does not have regime-change campaigns to code in the traditional sense |
| Military defection/loyalty shifts | The US military's relationship to civilian authority is fundamentally different from the autocratic contexts where this variable was developed |
| Coalition breadth (NAVCO-style) | Meaningful only during organized maximalist campaigns; the US has diffuse, overlapping movements, not unified campaigns |

### Key Observation

Social movement theory is **more directly applicable to the US than most core instability domains**. The US is arguably the most-studied case in the social movements literature -- the civil rights movement, labor movement, women's suffrage, anti-Vietnam War movement, Tea Party, Occupy, BLM, and the January 6 event are all empirically documented mobilization episodes with extensive quantitative data. The challenge is not applicability but rather translating campaign-level and event-level findings into continuous country-year variables suitable for an index.

---

## Bibliography

Barber, B. and A. English (2021). "Pandemic protests: How COVID-19 changed activism." [UNVERIFIED]

Beissinger, M.R. (2002). *Nationalist Mobilization and the Collapse of the Soviet State*. Cambridge: Cambridge University Press.

Buchanan, L., Q. Bui, and J.K. Patel (2020). "Black Lives Matter May Be the Largest Movement in U.S. History." *The New York Times*, July 3, 2020.

Chenoweth, E. (2020). "The Future of Nonviolent Resistance." *Journal of Democracy*, 31(3): 69-84.

Chenoweth, E. and M.J. Stephan (2011). *Why Civil Resistance Works: The Strategic Logic of Nonviolent Conflict*. New York: Columbia University Press.

Chenoweth, E. and O.A. Lewis (2013). "Unpacking nonviolent campaigns: Introducing the NAVCO 2.0 dataset." *Journal of Peace Research*, 50(3): 415-423.

Chenoweth, E. and C. Pinckney (2021). "The NAVCO 3.0 Dataset." [UNVERIFIED exact publication venue]

Chenoweth, E. and C. Shay (2020). "NAVCO 2.1 Dataset." [UNVERIFIED exact publication details]

Clark, D. and P. Regan (2016). "Mass Mobilization Protest Data." Harvard Dataverse. https://massmobilization.github.io/

Fisher, D.R. et al. (2022). "The George Floyd protests: Research on participation and mobilization." [UNVERIFIED exact citation]

Gladwell, M. (2010). "Small Change: Why the Revolution Will Not Be Tweeted." *The New Yorker*, October 4, 2010.

Gonzalez-Bailon, S., J. Borge-Holthoefer, A. Rivero, and Y. Moreno (2011). "The Dynamics of Protest Recruitment through an Online Network." *Scientific Reports*, 1: 197.

Granovetter, M. (1978). "Threshold Models of Collective Behavior." *American Journal of Sociology*, 83(6): 1420-1443.

Gurr, T.R. (1970). *Why Men Rebel*. Princeton: Princeton University Press.

Jost, J.T. et al. (2018). "How Social Media Facilitates Political Protest: Information, Motivation, and Social Networks as Conditions of Political Action Online and Offline." *Advances in Political Psychology*, 39(S1). [UNVERIFIED exact volume/issue]

Klandermans, B. (1997). *The Social Psychology of Protest*. Oxford: Blackwell.

Klandermans, B. (2004). "The Demand and Supply of Participation: Social-Psychological Correlates of Participation in Social Movements." In D.A. Snow, S.A. Soule, and H. Kriesi (eds.), *The Blackwell Companion to Social Movements*, 360-379.

Kuran, T. (1991). "Now Out of Never: The Element of Surprise in the East European Revolution of 1989." *World Politics*, 44(1): 7-48.

Lohmann, S. (1994). "The Dynamics of Informational Cascades: The Monday Demonstrations in Leipzig, East Germany, 1989-91." *World Politics*, 47(1): 42-101.

McAdam, D. (1982). *Political Process and the Development of Black Insurgency, 1930-1970*. Chicago: University of Chicago Press.

McAdam, D., S. Tarrow, and C. Tilly (2001). *Dynamics of Contention*. Cambridge: Cambridge University Press.

McCarthy, J.D. and M.N. Zald (1977). "Resource Mobilization and Social Movements: A Partial Theory." *American Journal of Sociology*, 82(6): 1212-1241.

Morozov, E. (2011). *The Net Delusion: The Dark Side of Internet Freedom*. New York: PublicAffairs.

Nepstad, S.E. (2011). *Nonviolent Revolutions: Civil Resistance in the Late 20th Century*. New York: Oxford University Press.

Nepstad, S.E. (2015). "Nonviolent Resistance Research." *Mobilization*, 20(4): 415-426.

Olson, M. (1965). *The Logic of Collective Action: Public Goods and the Theory of Groups*. Cambridge: Harvard University Press.

Pinckney, J. (2020). "When Civil Resistance Succeeds: Building Democracy After Popular Nonviolent Uprisings." [UNVERIFIED - may be ICNC publication]

Shirky, C. (2008). *Here Comes Everybody: The Power of Organizing Without Organizations*. New York: Penguin.

Snow, D.A. and R.D. Benford (1986). "Ideology, Frame Resonance, and Participant Mobilization." *International Social Movement Research*, 1: 197-218.

Snow, D.A. and R.D. Benford (1988). "Ideology, Frame Resonance, and Participant Mobilization." In B. Klandermans, H. Kriesi, and S. Tarrow (eds.), *International Social Movement Research*, Vol. 1, 197-217.

Steinert-Threlkeld, Z.C., D. Moktan, and J. Vicks (2015). "Using geolocated tweets to predict protest participation." [UNVERIFIED exact publication details]

Tarrow, S. (1994). *Power in Movement: Social Movements, Collective Action and Politics*. Cambridge: Cambridge University Press.

Tarrow, S. (2011). *Power in Movement: Social Movements and Contentious Politics*. 3rd edition. Cambridge: Cambridge University Press.

Tilly, C. and S. Tarrow (2004). *Contentious Politics*. Boulder: Paradigm Publishers.

Tufekci, Z. (2017). *Twitter and Tear Gas: The Power and Fragility of Networked Protest*. New Haven: Yale University Press.
