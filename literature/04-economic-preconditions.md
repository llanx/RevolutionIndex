# Literature Review: Economic Preconditions for Political Instability

## Scope

This domain covers economic theories and empirical evidence linking economic conditions to political instability, unrest, and regime change. The focus is on understanding **which economic variables predict political stress, through what mechanisms, and with what strength of evidence.**

**Boundaries:**
- Overlaps with Domain 1 (Revolution Prediction Theory) where economic variables appear in revolution models, but this domain goes deeper into the economic mechanisms, evidence base, and measurement approaches.
- Overlaps with Domain 3 (Historical Case Studies) where specific economic conditions preceded revolutions, but this domain synthesizes the economic evidence across cases rather than analyzing individual episodes.
- Covers: inequality dynamics, fiscal health, financial crises, cost of living, labor market conditions, and their transmission pathways to political outcomes.
- Does NOT cover: non-economic predictors (ideology, regime type, military dynamics) except where they moderate economic effects.

**Key questions this review addresses:**
1. What is the causal pathway from economic distress to political instability?
2. Which economic variables have the strongest empirical association with political outcomes?
3. How applicable are these findings to the United States specifically?
4. What are the lag structures between economic shocks and political responses?

**Phase 1 Open Questions addressed:**
- **#2:** Applications of prospect theory to aggregate political risk
- **#3:** Evidence for financial stress -> political mobilization transmission
- **#5 (partial):** Normalization approaches for trending macroeconomic series

---

## Foundational Works

### James C. Davies -- The J-Curve Theory (1962)

Davies proposed that revolutions occur not during periods of absolute deprivation but during periods of **reversal after improvement** -- when rising expectations are suddenly dashed. The "J-curve" describes a period of improving conditions followed by a sharp downturn, creating a widening gap between expected and actual need satisfaction.

- **Mechanism:** Societies that have experienced sustained improvement develop expectations of continued improvement. When conditions reverse (economic recession after growth, political repression after liberalization), the gap between expectations and reality creates intense frustration that can fuel collective action.
- **Evidence base:** Davies (1962) applied this framework to Dorr's Rebellion (1842), the Russian Revolution (1917), and the Egyptian revolution (1952). The evidence was illustrative rather than quantitative.
- **Variable extracted:** Gap between expected and actual economic trajectory -- measurable as deviation from trend GDP growth, consumer sentiment relative to actual conditions, or income growth deceleration.
- **Criticism:** The J-curve lacks precise thresholds (how large must the gap be? how quickly must reversal occur?) and faces the "always on" problem -- many reversals occur without revolution (Gurr 1970).

**US applicability:** HIGH. The J-curve concept maps well onto modern US political dynamics. The 2008-2009 financial crisis produced a classic J-curve: decades of rising prosperity, rapid reversal, and the expectation-reality gap arguably contributed to populist mobilization (Tea Party, Occupy Wall Street, and ultimately Trump's 2016 campaign built on "Make America Great Again" -- an explicit invocation of perceived decline from a better past).

### Ted Robert Gurr -- *Why Men Rebel* (1970)

Gurr formalized the concept of **relative deprivation** as the primary driver of political violence. Relative deprivation is the perceived discrepancy between what people believe they are entitled to (value expectations) and what they believe they can actually get (value capabilities).

- **Three types of relative deprivation:**
  1. **Decremental deprivation:** Capabilities decline while expectations remain constant (recession after stability).
  2. **Aspirational deprivation:** Expectations rise while capabilities remain constant (exposure to better-off reference groups via media).
  3. **Progressive deprivation:** Both rise, but expectations outpace capabilities (Davies' J-curve is a special case).

- **Key proposition:** The magnitude of political violence is a function of: (a) the intensity of relative deprivation, (b) the scope of relative deprivation (how many people feel it), and (c) the duration of relative deprivation (Gurr 1970, Chapter 2).

- **Variable extracted:** Relative deprivation intensity -- measurable via consumer sentiment indices relative to actual economic conditions, perceived vs. actual mobility, subjective economic assessments.

**US applicability:** HIGH. The concept of relative deprivation is directly applicable. The University of Michigan Consumer Sentiment Index (UMCSENT), Gallup's economic confidence index, and Pew's surveys on perceived financial well-being provide US-specific measures. The gap between perceived and actual economic conditions is measurable.

### Mancur Olson -- *The Logic of Collective Action* (1965)

Olson challenged the assumption that shared grievances automatically produce collective action. His key insight: **rational individuals have incentives to free-ride on others' efforts**, making collective action (including political protest and revolution) difficult to organize even when large groups share grievances.

- **Implications for instability prediction:** Economic grievances alone are insufficient; what matters is whether conditions create environments where collective action can overcome the free-rider problem. Olson identified three facilitators:
  1. **Small group size** (each individual's contribution matters)
  2. **Selective incentives** (participants get individual benefits beyond the collective good)
  3. **Coercion or social pressure** (organizations can compel participation)

- **Variable extracted:** Not a direct variable but a moderating mechanism. Suggests that economic distress translates to political instability more readily when organizational infrastructure exists (unions, parties, social movements) to solve the collective action problem.

**US applicability:** HIGH as a theoretical framework. Explains why economic distress sometimes produces mobilization (when organizations exist to channel grievances) and sometimes produces apathy (when collective action costs are high and organizations are weak).

### Edward Muller -- Income Inequality and Political Violence (1985, 1988)

Muller provided early quantitative evidence linking income inequality to political violence. Using cross-national data:

- **Key finding:** Countries with higher income inequality (measured by Gini coefficient and land Gini) had higher levels of political violence, controlling for regime type, economic development, and region (Muller 1985).
- **Mechanism:** Inequality creates grievances among the relatively deprived, reduces system legitimacy, and weakens cross-class social contracts.
- **Contested by:** Collier & Hoeffler (2004) found that inequality was not a significant predictor of civil war onset when economic opportunity variables (growth, income level) were included. This remains a live debate.

**Variable extracted:** Income inequality (Gini coefficient) -- direction: higher inequality associated with higher political violence, but the relationship may be non-linear and context-dependent.

### Alberto Alesina & Roberto Perotti -- Income Distribution, Political Instability, and Investment (1996)

Alesina and Perotti demonstrated a bidirectional relationship between inequality and political instability using a cross-national panel (1960-1985, 71 countries):

- **Key finding:** Income inequality, measured by the income share of the middle class, significantly predicted sociopolitical instability (assassinations, violent demonstrations, revolutions, coups). The middle-class share was a stronger predictor than the Gini coefficient (Alesina & Perotti 1996).
- **Transmission mechanism:** Inequality -> political instability -> reduced investment -> lower growth -> persistent inequality (a vicious cycle).
- **Innovation:** Emphasized the middle class specifically -- not absolute deprivation of the poor, but the relative position of the middle class, drives instability. A shrinking middle class signals rising political risk.

**Variable extracted:** Middle-class income share -- measurable via Census income distribution data, FRED median household income relative to GDP, income shares by quintile.

**US applicability:** HIGH. The US middle class has experienced well-documented hollowing since the 1970s. Median household income growth has lagged GDP growth. This variable is directly measurable and has clear theoretical links to political stress.

---

## Core Empirical Studies

### Funke, Schularick & Trebesch (2016) -- "Going to Extremes: Politics After Financial Crises"

This is the single most important empirical study linking financial crises to political outcomes in advanced democracies. Using a dataset spanning 20 advanced economies, 800+ elections, and 140+ years (1870-2014):

**Key findings:**
1. **Far-right vote share increases by approximately 30%** (relative to pre-crisis levels) in the five years following a systemic financial crisis. This effect is statistically significant and robust across specifications.
2. **Far-left parties also gain**, but the effect is smaller and less consistent.
3. **Government majorities shrink** after financial crises, making governing more difficult. Parliamentary fractionalization increases.
4. **The effect is specific to financial crises** -- normal recessions, even severe ones, do not produce comparable political polarization. The distinction is between "ordinary" economic downturns and systemic financial crises (banking panics, credit crunches, sovereign debt crises).
5. **Lag structure:** The political effects appear within 5 years of crisis onset and persist for approximately 10 years before fading. The peak effect on far-right voting is at years 5-7 post-crisis.
6. **Mechanism hypothesis:** Financial crises involve visible government intervention (bailouts, austerity) that politicizes economic hardship in ways that ordinary recessions do not. The perception that elites were rescued while ordinary people suffered drives anti-establishment mobilization.

**Methodological strengths:** Very long time span (140+ years), large country sample (20 advanced economies), well-defined treatment variable (systemic financial crisis, coded from established sources), extensive robustness checks including instrumental variable estimation.

**Limitations:** The study measures vote shares, not revolutions or regime change. The pathway from increased extremist voting to actual instability is theorized but not tested. Also, the 30% relative increase in far-right voting is from a low base in many countries -- going from 5% to 6.5% is very different from going from 20% to 26%.

**US applicability:** VERY HIGH. The US is included in the sample. The 2008 financial crisis and subsequent political polarization (Tea Party 2009, Occupy 2011, Trump 2016, Sanders 2016/2020) closely match the model's predictions. The study provides the strongest empirical evidence for the Financial Stress Pathway model in the codebase.

**Phase 1 Open Question #3 (financial stress -> political mobilization):** Funke et al. (2016) provides the core evidence. The transmission pathway is: systemic financial crisis -> visible government intervention (bailouts) -> perception of unfair rescue of elites -> anti-establishment mobilization -> far-right and far-left vote share gains -> parliamentary fragmentation -> governing difficulty. The lag structure is 5-10 years, with peak effects at years 5-7. Critically, this pathway is **specific to financial crises** -- not all economic downturns trigger it.

### Mian, Sufi & Trebbi (2014) -- "Resolving Debt Overhang: Political Economy Approach"

Complementing Funke et al., Mian, Sufi, and Trebbi analyzed the political consequences of household leverage and credit booms across 60+ countries (1920-2012):

- **Key finding:** Large increases in household debt-to-GDP are followed by a rise in government fractionalization and political polarization within 2-4 years. The effect operates through economic channels: household deleveraging reduces consumption, increases unemployment, and creates widespread economic distress (Mian, Sufi & Trebbi 2014).
- **Mechanism:** Unlike Funke et al.'s focus on financial system crises, Mian et al. emphasized the household balance sheet channel. When households are overleveraged, economic shocks produce deeper recessions and slower recoveries, extending the period of political stress.
- **Variable extracted:** Household debt-to-GDP ratio; household leverage growth rate. Direction: rapid growth in household leverage precedes both economic crisis and political polarization.

**US applicability:** HIGH. US household debt-to-GDP peaked at approximately 100% in 2007 before the financial crisis. The current trajectory (student debt, auto loans, credit card debt) is monitorable via FRED data.

### Thomas Piketty -- *Capital in the Twenty-First Century* (2014)

Piketty's central thesis -- that the rate of return on capital (r) exceeds the rate of economic growth (g) in the long run, leading to increasing wealth concentration -- provided a macroeconomic framework for understanding inequality dynamics:

- **Key empirical contribution:** Assembled historical data on income and wealth inequality spanning two centuries for 20+ countries, documenting the U-shaped trajectory of inequality (high in the Gilded Age, compressed during the mid-20th century "Great Compression," rising again since the 1980s).
- **Political implication:** Piketty argued that the mid-century compression was not natural but resulted from catastrophic wars, policy choices (progressive taxation, unions, welfare states), and that the return to high inequality creates political pressures analogous to the Gilded Age (Piketty 2014).
- **Variable extracted:** Wealth concentration (top 1% wealth share, top 10% wealth share); capital-to-income ratio. These provide long-run structural indicators of inequality trends.

**US applicability:** HIGH. The US top 1% income share has risen from approximately 8% (1970s) to approximately 18-20% (2020s). Piketty's data (available through WID -- World Inequality Database) provides the longest time series for tracking inequality dynamics relevant to political stress.

### Joseph Stiglitz -- *The Price of Inequality* (2012) and Related Work

Stiglitz linked inequality to political instability through institutional erosion:

- **Key argument:** Extreme inequality does not just create grievances -- it systematically distorts democratic institutions. Wealthy elites capture regulatory processes, shape tax policy, and defund public goods, creating a "vicious spiral" where inequality produces institutional capture which produces more inequality (Stiglitz 2012).
- **Mechanism for instability:** When democratic institutions are perceived as captured by elites, the legitimacy of the system erodes. Citizens who believe the system is rigged are more likely to support anti-system movements, whether populist left or populist right.
- **Variable extracted:** Institutional capture indicators -- regulatory capture, tax progressivity, lobbying expenditure. These are harder to quantify than income inequality but represent an important transmission mechanism.

**US applicability:** HIGH. Stiglitz's analysis is explicitly focused on the US. Campaign finance data (FEC), lobbying expenditure data, and tax progressivity measures are available via federal APIs.

### Acemoglu & Robinson -- *Economic Origins of Dictatorship and Democracy* (2006)

Acemoglu and Robinson modeled the relationship between inequality and political regime transitions:

- **Key model:** In highly unequal societies, the elite face a choice: repress (costly, risks revolution) or democratize (grants political power to the majority, enabling redistribution). Revolution occurs when inequality is high enough that the cost of accepting the status quo exceeds the cost of collective action against it (Acemoglu & Robinson 2006).
- **The "inverted U" hypothesis:** Neither very equal nor very unequal societies experience regime transitions. Very equal societies have no grievance. Very unequal societies are repressed effectively. The "danger zone" is intermediate inequality -- high enough to create grievances, not high enough to warrant maximal repression.
- **Variable extracted:** Inequality relative to repression capacity -- in a democracy, this translates to the question of whether democratic institutions can manage redistribution demands or whether frustration leads to extra-institutional mobilization.

**US applicability:** MODERATE. The US is not at risk of classic regime transition (democracy to dictatorship or vice versa). However, the concept of whether democratic institutions can manage redistribution demands is directly relevant. If democratic processes are perceived as failing to address inequality, support for extra-democratic action may increase.

---

## Recent Developments (2020-2025)

### Post-COVID Economic Stress and Political Attitudes

The COVID-19 pandemic and its economic aftermath produced natural experiments linking economic stress to political outcomes:

- **Inflation and political attitudes:** The 2021-2023 inflation episode (US CPI peaked at 9.1% in June 2022) produced widespread consumer dissatisfaction that correlated with declining government approval. Research has shown that inflation perceptions are asymmetric -- price increases are noticed and resented more than price stability or wage gains, consistent with prospect theory's loss aversion (Cavallo, Cruces & Perez-Truglia 2017).
- **Pandemic unemployment and extremism:** Fetzer (2019, updated for COVID) showed that local-level economic insecurity predicted support for populist and extremist parties across European democracies. The COVID unemployment shock replicated these patterns with accelerated timelines (Fetzer 2019) [UNVERIFIED for COVID extension].
- **Stimulus effects:** The rapid deployment of fiscal stimulus (CARES Act, American Rescue Plan) may have blunted the economic-to-political transmission pathway. This creates an important counterfactual question: did aggressive fiscal response prevent greater political instability? The evidence is suggestive but not definitive.

### Housing Affordability as a Political Variable

Housing costs have emerged as a major political grievance variable in wealthy democracies since 2020:

- **Evidence:** Ansell (2014) showed that housing market dynamics (price appreciation, mortgage exposure) significantly predict political attitudes and voting behavior. Homeowners who experience price appreciation shift right; renters facing affordability pressure shift left.
- **US data:** The US housing affordability index (NAR) reached record-low levels in 2023-2024. Median home prices relative to median household income exceeded 2006 bubble-era peaks in many markets. Rent burden (rent as percentage of income) has increased substantially for lower-income households (Joint Center for Housing Studies 2024) [UNVERIFIED].
- **Variable extracted:** Housing affordability index; median home price / median income ratio; rent burden (median rent / median renter income). Direction: declining affordability -> increased political grievance.

**US applicability:** VERY HIGH. Housing affordability is one of the most politically salient economic issues in the US. Measurable via FRED (mortgage rates, home prices), Census (rent burden, homeownership rates), and HUD (fair market rents, income limits).

### Wealth Inequality Trends and Political Consequences

Recent research has focused on wealth (not just income) inequality:

- **Saez & Zucman (2016, 2020):** Documented that US wealth concentration has returned to Gilded Age levels. The top 0.1% wealth share increased from approximately 7% (1978) to approximately 20% (2020). Wealth inequality is substantially more extreme than income inequality and may have independent political effects (Saez & Zucman 2016).
- **Wealth vs. income inequality:** Kuhn, Schularick, and Steins (2020) showed that wealth inequality is driven primarily by asset price appreciation (housing, equities) rather than income differences. This means that monetary policy decisions (interest rates, quantitative easing) that inflate asset prices have distributional consequences with political implications (Kuhn, Schularick & Steins 2020).
- **Variable extracted:** Wealth Gini; top 0.1% wealth share; asset price-to-income ratios. Data source: WID (World Inequality Database), Federal Reserve Distributional Financial Accounts (DFA).

### Prospect Theory Applications in Political Risk

**Phase 1 Open Question #2: Other applications of prospect theory to aggregate political risk?**

The Phase 1 validation report identified prospect theory as the theoretical basis for the PLI model and asked whether other researchers have applied prospect theory to aggregate political risk. The literature reveals several relevant applications:

- **Passarelli & Del Ponte (2020):** Surveyed applications of prospect theory to political behavior in the Oxford Research Encyclopedia of Politics. Key findings: prospect theory's loss aversion explains incumbency disadvantage (voters punish losses more than they reward gains), status quo bias in policy preferences, risk-seeking behavior among those who perceive themselves as being in a loss domain, and risk-averse behavior among those in a gains domain. They note that prospect theory has been applied at the individual voting level but rarely at the aggregate political risk level (Passarelli & Del Ponte 2020).
- **Vis (2011):** Applied prospect theory to policy-making, arguing that governments in a "domain of losses" (facing declining popularity, economic crisis) take riskier policy decisions than those in a "domain of gains." This has implications for instability: governments facing economic losses may gamble on risky policies (austerity, repression, foreign adventurism) that can backfire and increase instability (Vis 2011).
- **Mercer (2005):** Applied prospect theory to international relations, arguing that leaders' decisions about war, alliance, and crisis escalation are shaped by reference points and loss aversion. Leaders who perceive themselves as losing territory, status, or influence are more likely to take aggressive action (Mercer 2005).
- **Berejikian (2002):** Proposed a "prospect theory-informed model of political leadership" where leaders' policy choices depend on whether they frame their position as a gain or loss relative to reference points. This suggests that the framing of economic conditions (as decline from a better past vs. improvement from a worse past) matters as much as the objective conditions (Berejikian 2002).
- **Levy (2003):** Provided the definitive review of prospect theory applications in political science and international relations. Concluded that loss aversion is the most robust finding with the broadest applications: actors consistently value losses more than equivalent gains, leading to risk-seeking in loss domains and risk-averse in gain domains (Levy 2003).

**Assessment for this project:** The PLI model's application of prospect theory to aggregate political risk is theoretically novel -- most applications have been at the individual or leader level, not the population-aggregate level. The PLI's innovation of measuring perceived losses across multiple life domains (wages, housing, health, employment, security) relative to trailing peaks is a legitimate extension of prospect theory, but it lacks direct empirical validation. The theoretical basis is strong; the specific operationalization (lambda = 2.25, alpha = 0.88, 10-year trailing peaks) is reasonable but somewhat arbitrary.

### Financial Crisis -> Political Mobilization Transmission

**Phase 1 Open Question #3: What is the empirical evidence for financial stress -> political mobilization transmission?**

Beyond Funke et al. (2016) -- the anchor study -- the broader evidence includes:

- **De Bromhead, Eichengreen & O'Rourke (2013):** Analyzed the political consequences of the Great Depression across 28 countries (1919-1939). Found that countries experiencing banking crises shifted rightward, but the effect depended on institutional context: countries with proportional representation experienced larger shifts to the extreme right than majoritarian systems (De Bromhead, Eichengreen & O'Rourke 2013).
- **Funke & Trebesch (2018):** Extended the 2016 analysis to show that populist mobilization (both left and right) after financial crises follows a predictable sequence: initial anger at incumbents (election 1), rise of outsider candidates (election 2), consolidation of populist parties (election 3). The full cycle takes 10-15 years (Funke & Trebesch 2018).
- **Algan, Guriev, Papaioannou & Passari (2017):** Used European Social Survey data to show that the 2008-2013 financial crisis significantly decreased trust in national and European institutions, and that this trust decline was a proximate driver of populist vote shares. The trust-decline channel operated independently of direct economic hardship (Algan et al. 2017).
- **Guiso, Herrera, Morelli & Sonno (2019):** Analyzed European Parliament elections and found that economic insecurity (job loss risk, income decline) predicted demand for populism, but the effect was mediated by trust in institutions. Economic insecurity in high-trust environments produced less populism than in low-trust environments (Guiso et al. 2019).
- **Conditions under which financial crises do NOT produce political instability:**
  - **Rapid, effective government response** (US New Deal after 1933, US CARES Act after 2020) can blunt the economic-to-political transmission.
  - **Strong social safety nets** (Scandinavian countries experienced the 2008 crisis without significant populist shifts).
  - **High pre-crisis institutional trust** acts as a buffer (Guiso et al. 2019).
  - **Non-systemic financial stress** (stock market corrections, localized bank failures) does not trigger the populist mobilization pathway -- only systemic crises do.

**Lag structure synthesis:** Across studies, the financial crisis -> political outcome pathway operates on the following timeline:
- **0-2 years:** Immediate economic impact (unemployment, wealth destruction). Incumbent punishment in nearest election.
- **2-5 years:** Trust erosion becomes measurable. Anti-establishment rhetoric gains traction. New political movements or parties emerge.
- **5-10 years:** Peak effect on extremist/populist vote shares. Policy consequences (austerity backlash, trade protectionism). Institutional changes (regulatory reform or capture).
- **10-15 years:** Effects begin to fade if no second crisis occurs. Institutional adaptation or consolidation of new political alignments.

### Normalization Approaches in Economic Instability Indices

**Phase 1 Open Question #5 (partial): How do other researchers handle normalization for trending macroeconomic series?**

The literature on composite economic and political indices reveals several standard approaches:

| Method | Used By | Approach | Trending Series Handling |
|--------|---------|----------|------------------------|
| Rolling z-scores | STLFSI (Federal Reserve), FSP model | (x - rolling_mean) / rolling_std, window typically 10-20 years | De-trends automatically; measures deviation from recent history |
| Percentile ranks | COINr package, some V-Dem indicators | Rank-based normalization (0-100) | Handles trends and outliers; non-parametric |
| Year-over-year change | FRED diff-log transformations, many academic studies | First-difference or log-difference of raw series | Converts levels to changes; eliminates trends entirely |
| Deviation from trend | Hodrick-Prescott filter, Congressional Budget Office output gap | Series decomposed into trend + cyclical; cyclical component used | Distinguishes structural trends from cyclical deviations |
| Categorical binning | PITF (Polity categories), FSI (0-10 expert scale) | Convert continuous variable to ordinal categories | Avoids continuous normalization entirely |
| Distance to reference | World Bank relative poverty lines, OECD better life index | Measured relative to a fixed reference point (e.g., poverty line, OECD median) | Reference point provides anchor independent of own history |

**Recommendation for the project:** Rolling z-scores (20-year window) are the most appropriate default for trending US macroeconomic series. Percentile ranks are a good alternative for highly skewed distributions. Min-max normalization on raw values (as used by PSI) is known to produce the "pinning" problem identified in Phase 1 and should be avoided for any series with a secular trend.

---

## Variables Discovered

| Variable | Measurement/Proxy | Studies | Direction | Notes |
|----------|------------------|---------|-----------|-------|
| Income inequality (Gini) | Gini coefficient, Census ACS income data | Muller (1985), Alesina & Perotti (1996), Piketty (2014), Acemoglu & Robinson (2006) | Higher inequality -> higher instability risk | Strong evidence globally. US Gini has risen from 0.39 (1970) to ~0.49 (2022). Available via Census/FRED. |
| Top income concentration | Top 1% pre-tax income share; top 10% income share | Piketty (2014), Saez & Zucman (2016), Turchin (2003) | Higher concentration -> higher instability risk | US top 1% share doubled since 1980. Available via WID (other-data). |
| Wealth concentration | Top 1% wealth share; top 0.1% wealth share; wealth Gini | Saez & Zucman (2016, 2020), Kuhn et al. (2020) | Higher concentration -> higher instability risk | More extreme than income inequality. US top 0.1% wealth share ~20%. Federal Reserve DFA data (fed-data). |
| Middle-class income share | Income share of middle 3 quintiles (20th-80th percentile) | Alesina & Perotti (1996), Stiglitz (2012), Piketty (2014) | Declining middle-class share -> higher instability risk | Alesina & Perotti found this stronger than Gini. Measurable via Census income distribution. |
| Real wage growth | Median real hourly earnings; real wage index (1979=100) | Turchin (2003), Piketty (2014), Stiglitz (2012) | Stagnating/declining real wages -> higher instability risk | US median real wages were flat 1973-2014. Available via BLS/FRED. |
| Unemployment rate | BLS U-3 or U-6 unemployment rate | Campante & Chor (2012), Fetzer (2019), Alesina & Perotti (1996) | Higher unemployment -> higher instability risk | Standard labor market distress indicator. Directly available via BLS/FRED. Effect may be stronger for youth unemployment. |
| Youth unemployment / disconnection | Youth (16-24) unemployment rate; NEET rate (not in education, employment, or training) | Campante & Chor (2012), Urdal (2006), Goldstone (1991) | Higher youth unemployment -> higher instability risk | Young people have lower opportunity costs for mobilization. BLS youth unemployment available via FRED. |
| Inflation rate | CPI-U year-over-year; core CPI; PCE deflator | Cavallo et al. (2017), Rudé (1959), Gatrell (2005) | Rising inflation -> increased political grievance | Asymmetric perception (losses loom larger than gains). Available via BLS/FRED. US has never experienced hyperinflation (not applicable). |
| Housing affordability | Housing affordability index; median home price / median income; rent burden (rent / renter income) | Ansell (2014), Joint Center for Housing Studies (2024) | Declining affordability -> increased political grievance | Emerging as major US political variable. Available via FRED (FIXHAI, MSPUS), Census, HUD. |
| Consumer confidence / sentiment | University of Michigan CSCI; Conference Board CCI | Davies (1962), Gurr (1970), Cavallo et al. (2017) | Sharp declines in confidence -> short-term mobilization risk | Captures perceived economic trajectory. Available via FRED (UMCSENT). Note: OECD Consumer Confidence (CSCICP03USM665S) is DISCONTINUED -- use UMCSENT instead (see Phase 1 audit). |
| Government fiscal deficit | Federal deficit as % of GDP; primary budget balance | Brinton (1938), Skocpol (1979), Goldstone (1991), Turchin (2003) | Large persistent deficits -> higher instability risk (state weakness signal) | One of the most consistently cited preconditions across revolution literature. Available via FRED/Treasury. |
| Government debt level | Federal debt held by public as % of GDP; total debt / GDP | Turchin (2003), Mian et al. (2014), Reinhart & Rogoff (2010) | High/rising debt -> fiscal fragility -> higher instability risk | Contested: Japan demonstrates high debt without crisis. Debt LEVEL may matter less than debt SERVICE cost or debt TRAJECTORY. Available via FRED (GFDEGDQ188S). |
| Financial crisis occurrence | Systemic banking crisis indicator (Laeven & Valencia 2020); financial stress indices (STLFSI, NFCI) | Funke et al. (2016), De Bromhead et al. (2013), Mian et al. (2014) | Systemic financial crises -> 30% relative increase in extremist voting within 5 years | The single strongest empirically documented economic -> political pathway. Financial stress indices available via FRED (STLFSI4). |
| Household debt / leverage | Household debt-to-GDP; household debt-to-income; debt service ratio | Mian, Sufi & Trebbi (2014), Funke et al. (2016) | Rapid household leverage growth -> higher crisis and instability risk | Precursor to financial crises. Available via FRED (HDTGPDUSQ163N, TDSP). |
| Labor share of GDP | Compensation of employees as % of GDP; nonfarm business labor share | Turchin (2003), Piketty (2014), Stiglitz (2012) | Declining labor share -> rising inequality -> higher instability risk | US labor share declined from ~65% (1970) to ~57% (2014) before partial recovery. Available via FRED (W270RE1A156NBEA, PRS85006173). |
| Economic growth rate | Real GDP growth (annual, quarterly) | Davies (1962), Acemoglu & Robinson (2006), Collier & Hoeffler (2004) | Sharp growth deceleration or contraction -> higher instability risk | Not absolute level but change from trend. J-curve theory emphasizes reversal. Available via BEA/FRED. |
| Relative deprivation (perceived) | Gap between consumer expectations and actual conditions; perceived vs. actual inflation; subjective economic well-being | Gurr (1970), Davies (1962), Passarelli & Del Ponte (2020) | Larger perceived-actual gap -> higher instability risk | Theoretically important but requires survey data. Best proxy: UMCSENT expectations vs. actual GDP/employment. |
| Institutional trust (economic dimension) | Trust in banks, corporations, financial system | Algan et al. (2017), Guiso et al. (2019), Stiglitz (2012) | Declining trust -> removes buffer against economic-to-political transmission | Mediating variable: economic distress translates to political instability more readily when institutional trust is low. Gallup/Pew surveys (other-data). |
| Cost of living pressure | Real personal consumption expenditures; CPI components (food, energy, housing, healthcare, education) | Bellemare (2015), Lagi et al. (2011), Cavallo et al. (2017) | Rising essential costs relative to income -> increased grievance | Composite of multiple pressures. Individual CPI components available via FRED/BLS. |

---

## Key Debates and Contested Findings

### 1. Absolute vs. Relative Deprivation

- **Absolute deprivation view:** People rebel when they cannot meet basic needs (food, shelter, physical security). This view predicts that poverty and deprivation are the primary economic drivers of instability.
- **Relative deprivation view (Gurr 1970):** People rebel when they perceive a gap between what they expect and what they get. This means that wealthy societies can experience instability if expectations exceed reality, even when absolute conditions are good.
- **Current evidence:** For developing countries, absolute deprivation matters (food price spikes trigger unrest). For developed countries, relative deprivation dominates -- the US population is materially well-off by global standards but perceives declining relative position. The project should focus on relative deprivation measures for the US context.

### 2. Inequality as Cause vs. Symptom

- **Inequality causes instability:** Muller (1985), Alesina & Perotti (1996), and the SDT tradition (Turchin) argue that inequality directly creates revolutionary conditions.
- **Inequality is a symptom:** Some scholars (North, Wallis & Weingast 2009) argue that inequality and instability are both products of underlying institutional arrangements. Societies with extractive institutions produce both inequality and fragility; societies with inclusive institutions produce neither. In this view, targeting inequality is treating the symptom.
- **Resolution:** Both perspectives likely contain truth. The project should treat inequality as a measurable risk indicator without assuming it is the root cause. The causal chain may run: institutional quality -> inequality -> perceived unfairness -> mobilization potential.

### 3. Do Financial Crises Always Produce Political Extremism?

- **Yes, with qualifications (Funke et al. 2016):** The statistical relationship is robust across 140+ years and 20 countries. Financial crises consistently shift voting toward the far right.
- **No, context matters (Guiso et al. 2019, Algan et al. 2017):** The political impact of financial crises depends on mediating variables: pre-crisis institutional trust, quality of government response, strength of social safety nets, electoral system design. Scandinavian countries weathered 2008 without populist surges; Mediterranean countries saw significant ones.
- **Synthesis:** Financial crises create political risk, but the magnitude depends on institutional resilience. The project should track financial stress as a risk indicator while also tracking institutional trust as a moderating variable.

### 4. Do Economic Variables Predict Revolution or Just Protest?

- **Economic distress -> protest (well-established):** There is strong evidence that economic downturns increase protest frequency and participation.
- **Economic distress -> revolution (much weaker):** Most economic crises produce protest, not revolution. Revolution requires additional conditions (elite fragmentation, state fiscal crisis, military defection) beyond economic distress alone.
- **Implication for the project:** Economic variables should be understood as contributing to a "political stress" score rather than predicting "revolution" directly. The index measures conditions under which political instability becomes more likely, not the probability of revolution per se.

### 5. Short-Term Triggers vs. Long-Term Structural Trends

- **Short-term (recession, inflation spike, financial crisis):** These produce immediate political reactions (incumbent punishment, protest surges, populist mobilization). Effects are measurable within 1-5 years.
- **Long-term (rising inequality, declining labor share, mounting debt):** These create structural vulnerability that short-term triggers activate. Effects build over decades and are harder to attribute to specific outcomes.
- **The project needs both:** Short-term indicators (STLFSI, unemployment rate, CPI) for timely signal, and long-term indicators (inequality trends, debt trajectory, labor share) for structural context. The composite score should reflect both time horizons.

---

## US Applicability Assessment

### Directly Applicable (variable varies meaningfully in US, directly measurable)

| Variable | US Data Source | Historical Range | Recent Trend |
|----------|---------------|-----------------|--------------|
| Income inequality (Gini) | Census ACS (fed-data) | 0.39 (1970) to 0.49 (2022) | Rising steadily |
| Top 1% income share | WID (other-data) | 8% (1970s) to 18-20% (2020s) | Rising with plateaus |
| Real median wage growth | BLS/FRED (fed-data) | -1% to +4% annual range | Flat 1973-2014; modest growth since 2015 |
| Unemployment rate | BLS/FRED (fed-data) | 3.4% (2023) to 14.7% (Apr 2020) | Cyclically low |
| Housing affordability | FRED/Census/HUD (fed-data) | Record-low affordability (2023-2024) | Sharply declining |
| Consumer sentiment | UMCSENT, FRED (fed-data) | 50 (2022 low) to 112 (2000 high) | Depressed since 2021 |
| Federal deficit / GDP | FRED/Treasury (fed-data) | -1% to -15% of GDP | Large persistent deficits |
| Federal debt / GDP | FRED (fed-data) | 30% (2001) to 120%+ (2024) | Rising rapidly |
| Financial stress index | STLFSI4, FRED (fed-data) | -1.5 to +9 (2008 peak) | Near neutral |
| Household debt / GDP | FRED (fed-data) | ~60% to ~100% | Below 2008 peak but rising |
| Labor share of GDP | FRED (fed-data) | 57% to 65% | Partially recovered from 2014 trough |
| Inflation rate | BLS/FRED (fed-data) | -0.4% (2009) to 9.1% (2022) | Declining from 2022 peak |

### Applicable with Adaptation

| Variable | Adaptation | US Proxy | Data Source |
|----------|-----------|----------|-------------|
| Relative deprivation | Original concept is individual-level; need aggregate measure | UMCSENT expectations minus actual GDP/employment growth | FRED + calculation (fed-data) |
| Institutional trust (economic) | Survey-based; no federal API | Gallup confidence in banks/big business | Other-data (Gallup) |
| Wealth concentration | Available but requires specific dataset | Fed DFA top 1% wealth share | Fed-data (Federal Reserve DFA, quarterly) |
| Middle-class share | Census data requires calculation | Ratio of median household income to mean household income; or middle 60% income share | Census ACS (fed-data, annual) |
| Cost of living composite | No single series; requires construction | Weighted basket: CPI-shelter, CPI-food, CPI-medical, CPI-education relative to median income | BLS/FRED (fed-data, requires composition) |

### Not Applicable

| Variable | Reason | Notes |
|----------|--------|-------|
| Hyperinflation | US has never experienced hyperinflation; institutional safeguards (Fed independence) make it extremely unlikely | Even 9.1% (2022) is far below hyperinflation thresholds (50%+/month) |
| Sovereign default | US dollar is the global reserve currency; US has never defaulted on debt | The debt ceiling is a political mechanism, not a fiscal one. Market pricing of US default risk is near zero. |
| Capital flight | US is the global safe haven; capital flows INTO the US during crises | The direction of capital flow is reversed relative to developing countries experiencing instability |
| Subsistence crisis | US food insecurity exists but is not at subsistence level for most of the population | Food is ~10% of US household spending; government programs (SNAP, WIC) provide a safety net |

---

## Bibliography

Acemoglu, D., & Robinson, J. A. (2006). *Economic Origins of Dictatorship and Democracy*. Cambridge University Press.

Alesina, A., & Perotti, R. (1996). Income distribution, political instability, and investment. *European Economic Review*, 40(6), 1203-1228.

Algan, Y., Guriev, S., Papaioannou, E., & Passari, E. (2017). The European trust crisis and the rise of populism. *Brookings Papers on Economic Activity*, 2017(2), 309-400.

Ansell, B. W. (2014). The political economy of ownership: Housing markets and the welfare state. *American Political Science Review*, 108(2), 383-402.

Bellemare, M. F. (2015). Rising food prices, food price volatility, and social unrest. *American Journal of Agricultural Economics*, 97(1), 1-21.

Berejikian, J. D. (2002). A cognitive theory of deterrence. *Journal of Politics*, 64(2), 567-583.

Brinton, C. (1938/1965). *The Anatomy of Revolution*. Vintage Books.

Campante, F. R., & Chor, D. (2012). Why was the Arab world poised for revolution? Schooling, economic opportunities, and the Arab Spring. *Journal of Economic Perspectives*, 26(2), 167-188.

Cavallo, A., Cruces, G., & Perez-Truglia, R. (2017). Inflation expectations, learning, and supermarket prices: Evidence from survey experiments. *American Economic Journal: Macroeconomics*, 9(3), 1-35.

Collier, P., & Hoeffler, A. (2004). Greed and grievance in civil war. *Oxford Economic Papers*, 56(4), 563-595.

Davies, J. C. (1962). Toward a theory of revolution. *American Sociological Review*, 27(1), 5-19.

De Bromhead, A., Eichengreen, B., & O'Rourke, K. H. (2013). Political extremism in the 1920s and 1930s: Do German lessons generalize? *Journal of Economic History*, 73(2), 371-406.

Fetzer, T. (2019). Did austerity cause Brexit? *American Economic Review*, 109(11), 3849-3886.

Figes, O. (1996). *A People's Tragedy: The Russian Revolution, 1891-1924*. Jonathan Cape.

Funke, M., Schularick, M., & Trebesch, C. (2016). Going to extremes: Politics after financial crises, 1870-2014. *European Economic Review*, 88, 227-260.

Funke, M., & Trebesch, C. (2018). Financial crises and the populist right. ifo DICE Report, 16(1), 6-9. [UNVERIFIED -- specific publication details]

Gatrell, P. (2005). *Russia's First World War: A Social and Economic History*. Pearson.

Goldstone, J. A. (1991). *Revolution and Rebellion in the Early Modern World*. University of California Press.

Guiso, L., Herrera, H., Morelli, M., & Sonno, T. (2019). Global crises and populism: The role of Eurozone institutions. *Economic Policy*, 34(97), 95-139.

Gurr, T. R. (1970). *Why Men Rebel*. Princeton University Press.

Joint Center for Housing Studies of Harvard University. (2024). *The State of the Nation's Housing 2024*. [UNVERIFIED -- specific edition]

Kuhn, M., Schularick, M., & Steins, U. I. (2020). Income and wealth inequality in America, 1949-2016. *Journal of Political Economy*, 128(9), 3469-3519.

Lagi, M., Bertrand, K. Z., & Bar-Yam, Y. (2011). The food crises and political instability in North Africa and the Middle East. *arXiv preprint*, 1108.2455.

Levy, J. S. (2003). Applications of prospect theory to political science. *Synthese*, 135(2), 215-241.

Mercer, J. (2005). Prospect theory and political science. *Annual Review of Political Science*, 8, 1-21.

Mian, A., Sufi, A., & Trebbi, F. (2014). Resolving debt overhang: Political economy evidence. *NBER Working Paper*, No. 17831. [Published in *American Economic Journal: Macroeconomics*]

Muller, E. N. (1985). Income inequality, regime repressiveness, and political violence. *American Sociological Review*, 50(1), 47-61.

North, D. C., Wallis, J. J., & Weingast, B. R. (2009). *Violence and Social Orders: A Conceptual Framework for Interpreting Recorded Human History*. Cambridge University Press.

Olson, M. (1965). *The Logic of Collective Action: Public Goods and the Theory of Groups*. Harvard University Press.

Passarelli, F., & Del Ponte, A. (2020). Prospect theory and political behavior. In *Oxford Research Encyclopedia of Politics*. Oxford University Press.

Piketty, T. (2014). *Capital in the Twenty-First Century*. Harvard University Press.

Reinhart, C. M., & Rogoff, K. S. (2010). Growth in a time of debt. *American Economic Review*, 100(2), 573-578.

Rudé, G. (1959). *The Crowd in the French Revolution*. Oxford University Press.

Saez, E., & Zucman, G. (2016). Wealth inequality in the United States since 1913: Evidence from capitalized income tax data. *Quarterly Journal of Economics*, 131(2), 519-578.

Saez, E., & Zucman, G. (2020). The rise of income and wealth inequality in America: Evidence from distributional macroeconomic accounts. *Journal of Economic Perspectives*, 34(4), 3-26.

Skocpol, T. (1979). *States and Social Revolutions: A Comparative Analysis of France, Russia, and China*. Cambridge University Press.

Stiglitz, J. E. (2012). *The Price of Inequality: How Today's Divided Society Endangers Our Future*. W. W. Norton & Company.

Turchin, P. (2003). *Historical Dynamics: Why States Rise and Fall*. Princeton University Press.

Urdal, H. (2006). A clash of generations? Youth bulges and political violence. *International Studies Quarterly*, 50(3), 607-629.

Vis, B. (2011). Prospect theory and political decision making. *Political Studies Review*, 9(3), 334-343.
