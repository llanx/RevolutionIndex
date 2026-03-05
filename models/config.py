"""
Pipeline configuration: variable-to-source mapping, domain groupings,
evidence weights, and normalization parameters.

Source: data-sources/data-source-inventory.md (Phase 3)
Evidence ratings: literature/variable-catalog.md (Phase 2)
"""
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Domain(Enum):
    ECONOMIC_STRESS = "economic_stress"
    POLITICAL_POLARIZATION = "political_polarization"
    INSTITUTIONAL_QUALITY = "institutional_quality"
    SOCIAL_MOBILIZATION = "social_mobilization"
    INFORMATION_MEDIA = "information_media"


class SourceType(Enum):
    FRED_API = "fred_api"
    MANUAL_DOWNLOAD = "manual_download"
    CONSTRUCTED = "constructed"


class EvidenceRating(Enum):
    STRONG = "strong"
    MODERATE = "moderate"
    WEAK = "weak"


class NormDirection(Enum):
    HIGHER_IS_WORSE = "higher_is_worse"  # higher raw value = more stress
    LOWER_IS_WORSE = "lower_is_worse"    # lower raw value = more stress


@dataclass
class Variable:
    catalog_number: int
    name: str
    domain: Domain
    source_type: SourceType
    series_id: Optional[str]        # FRED series ID or None for manual/constructed
    evidence_rating: EvidenceRating
    norm_direction: NormDirection
    frequency: str                   # monthly, quarterly, annual, biennial, etc.
    coverage_start: int              # start year
    short_series: bool               # True if coverage starts after 2000
    construction_recipe: Optional[str]  # for constructed variables
    manual_source: Optional[str]     # download URL for manual sources


# Weight within domain: Strong=3, Moderate=2, Weak=1 (then normalized to sum to 1.0)
EVIDENCE_WEIGHTS = {
    EvidenceRating.STRONG: 3.0,
    EvidenceRating.MODERATE: 2.0,
    EvidenceRating.WEAK: 1.0,
}

# Inter-domain weights: used ONLY for factor display values in current.json
# (the "value" field of each factor). All scoring (current score, history,
# bootstrap CI) uses MODEL_WEIGHTS via the 5 model functions in ensemble.py.
# Do NOT use DOMAIN_WEIGHTS for computing composite scores.
DOMAIN_WEIGHTS = {
    Domain.ECONOMIC_STRESS: 0.30,        # 7 Strong variables, highest evidence density
    Domain.POLITICAL_POLARIZATION: 0.22, # 4 Strong variables, central to all frameworks
    Domain.INSTITUTIONAL_QUALITY: 0.20,  # 1 Strong variable but critical dimension
    Domain.SOCIAL_MOBILIZATION: 0.18,    # 2 Strong variables, mobilization/trust
    Domain.INFORMATION_MEDIA: 0.10,      # 0 Strong variables, weakest evidence
}
# Must sum to 1.0

# Model ensemble weights: used for ALL scoring (current, history, bootstrap).
# Each model function consumes specific variables and produces a 0-100 score.
# The ensemble combines these with these weights.
MODEL_WEIGHTS = {
    "psi": 0.25,
    "pli": 0.20,
    "fsp": 0.15,
    "georgescu_sdt": 0.25,
    "vdem_ert": 0.15,
}

# Freshness tracking configuration
FRESHNESS_CONFIG = {
    "cache_dir": "data/raw",
    "freshness_file": "data/freshness.json",
    "stale_threshold_days": 30,
}

# Normalization parameters
NORMALIZATION_CONFIG = {
    "default_method": "rolling_zscore",
    "rolling_window_months": 240,  # 20 years
    "short_series_fallback": "percentile_rank",
}


# ---------------------------------------------------------------------------
# Variable definitions: 41 measurable variables (45 total minus 4 unavailable)
#
# Unavailable (all weak-rated, excluded entirely):
#   #33 Misinformation Prevalence (unknown source, no standardized measure)
#   #35 Social Media Political Engagement (unknown source, no standardized measure)
#   #43 Information Fragmentation / Echo Chambers (unknown source)
#   #44 Cross-Class Coalition Formation (no direct measure or strong proxy)
# ---------------------------------------------------------------------------

VARIABLES: list[Variable] = [
    # =========================================================================
    # DOMAIN 1: ECONOMIC STRESS (13 variables)
    # =========================================================================

    # #1 Income / Wealth Inequality
    Variable(
        catalog_number=1,
        name="Income / Wealth Inequality (Gini)",
        domain=Domain.ECONOMIC_STRESS,
        source_type=SourceType.FRED_API,
        series_id="SIPOVGINIUSA",
        evidence_rating=EvidenceRating.STRONG,
        norm_direction=NormDirection.HIGHER_IS_WORSE,
        frequency="annual",
        coverage_start=1963,
        short_series=False,
        construction_recipe=None,
        manual_source=None,
    ),

    # #2 Real Wage Growth / Labor Share
    Variable(
        catalog_number=2,
        name="Real Wage Growth / Labor Share",
        domain=Domain.ECONOMIC_STRESS,
        source_type=SourceType.FRED_API,
        series_id="PRS85006173",
        evidence_rating=EvidenceRating.STRONG,
        norm_direction=NormDirection.LOWER_IS_WORSE,
        frequency="quarterly",
        coverage_start=1947,
        short_series=False,
        construction_recipe=None,
        manual_source=None,
    ),

    # #5 State Fiscal Distress (Debt / Deficit)
    Variable(
        catalog_number=5,
        name="State Fiscal Distress (Debt/GDP)",
        domain=Domain.ECONOMIC_STRESS,
        source_type=SourceType.FRED_API,
        series_id="GFDEGDQ188S",
        evidence_rating=EvidenceRating.STRONG,
        norm_direction=NormDirection.HIGHER_IS_WORSE,
        frequency="quarterly",
        coverage_start=1966,
        short_series=False,
        construction_recipe=None,
        manual_source=None,
    ),

    # #6 Financial Crisis / Systemic Stress
    Variable(
        catalog_number=6,
        name="Financial Crisis / Systemic Stress",
        domain=Domain.ECONOMIC_STRESS,
        source_type=SourceType.FRED_API,
        series_id="STLFSI4",
        evidence_rating=EvidenceRating.STRONG,
        norm_direction=NormDirection.HIGHER_IS_WORSE,
        frequency="weekly",
        coverage_start=1993,
        short_series=False,
        construction_recipe=None,
        manual_source=None,
    ),

    # #8 Elite Overproduction (Georgescu education-job mismatch proxy)
    Variable(
        catalog_number=8,
        name="Elite Overproduction (Education-Job Mismatch)",
        domain=Domain.ECONOMIC_STRESS,
        source_type=SourceType.CONSTRUCTED,
        series_id=None,
        evidence_rating=EvidenceRating.STRONG,
        norm_direction=NormDirection.HIGHER_IS_WORSE,
        frequency="annual",
        coverage_start=2005,
        short_series=True,
        construction_recipe=(
            "Census ACS B15003: Sum B15003_023E (master's) + B15003_024E "
            "(professional) + B15003_025E (doctorate) for total advanced degree "
            "holders. Normalize to population (B15003_001E). BLS JOLTS: Use "
            "JTS540000000000000JOR (professional/business openings rate) "
            "annualized. Ratio: (advanced degree holders per capita) / "
            "(professional openings rate). Higher = more overproduction."
        ),
        manual_source="Census ACS + BLS JOLTS",
    ),

    # #9 Unemployment Rate
    Variable(
        catalog_number=9,
        name="Unemployment Rate (U-3)",
        domain=Domain.ECONOMIC_STRESS,
        source_type=SourceType.FRED_API,
        series_id="UNRATE",
        evidence_rating=EvidenceRating.STRONG,
        norm_direction=NormDirection.HIGHER_IS_WORSE,
        frequency="monthly",
        coverage_start=1948,
        short_series=False,
        construction_recipe=None,
        manual_source=None,
    ),

    # #10 GDP Growth Rate
    Variable(
        catalog_number=10,
        name="GDP Growth Rate (Real, Annualized Quarterly)",
        domain=Domain.ECONOMIC_STRESS,
        source_type=SourceType.FRED_API,
        series_id="A191RL1Q225SBEA",
        evidence_rating=EvidenceRating.STRONG,
        norm_direction=NormDirection.LOWER_IS_WORSE,
        frequency="quarterly",
        coverage_start=1947,
        short_series=False,
        construction_recipe=None,
        manual_source=None,
    ),

    # #14 Relative Deprivation / Expectation-Reality Gap
    Variable(
        catalog_number=14,
        name="Relative Deprivation (Sentiment-Reality Gap)",
        domain=Domain.ECONOMIC_STRESS,
        source_type=SourceType.CONSTRUCTED,
        series_id=None,
        evidence_rating=EvidenceRating.MODERATE,
        norm_direction=NormDirection.HIGHER_IS_WORSE,
        frequency="monthly",
        coverage_start=1952,
        short_series=False,
        construction_recipe=(
            "Normalize UMCSENT to z-scores over rolling 10-year window. "
            "Normalize actual GDP growth to z-scores over same window. "
            "Gap = sentiment z-score minus actual performance z-score. "
            "Positive gap = expectations above reality (J-curve vulnerability). "
            "Negative gap = perceived deprivation beyond actual deterioration."
        ),
        manual_source=None,
    ),

    # #16 Housing Affordability
    Variable(
        catalog_number=16,
        name="Housing Affordability Index",
        domain=Domain.ECONOMIC_STRESS,
        source_type=SourceType.FRED_API,
        series_id="FIXHAI",
        evidence_rating=EvidenceRating.MODERATE,
        norm_direction=NormDirection.LOWER_IS_WORSE,
        frequency="monthly",
        coverage_start=1971,
        short_series=False,
        construction_recipe=None,
        manual_source=None,
    ),

    # #17 Inflation Rate
    Variable(
        catalog_number=17,
        name="Inflation Rate (CPI-U YoY)",
        domain=Domain.ECONOMIC_STRESS,
        source_type=SourceType.FRED_API,
        series_id="CPIAUCSL",
        evidence_rating=EvidenceRating.MODERATE,
        norm_direction=NormDirection.HIGHER_IS_WORSE,
        frequency="monthly",
        coverage_start=1947,
        short_series=False,
        construction_recipe=None,
        manual_source=None,
    ),

    # #18 Consumer Confidence / Sentiment
    Variable(
        catalog_number=18,
        name="Consumer Sentiment Index",
        domain=Domain.ECONOMIC_STRESS,
        source_type=SourceType.FRED_API,
        series_id="UMCSENT",
        evidence_rating=EvidenceRating.MODERATE,
        norm_direction=NormDirection.LOWER_IS_WORSE,
        frequency="monthly",
        coverage_start=1952,
        short_series=False,
        construction_recipe=None,
        manual_source=None,
    ),

    # #27 Household Debt / Leverage
    Variable(
        catalog_number=27,
        name="Household Debt Service Ratio",
        domain=Domain.ECONOMIC_STRESS,
        source_type=SourceType.FRED_API,
        series_id="TDSP",
        evidence_rating=EvidenceRating.MODERATE,
        norm_direction=NormDirection.HIGHER_IS_WORSE,
        frequency="quarterly",
        coverage_start=1980,
        short_series=False,
        construction_recipe=None,
        manual_source=None,
    ),

    # #40 Cost of Living Pressure (Composite)
    Variable(
        catalog_number=40,
        name="Cost of Living Pressure (Composite)",
        domain=Domain.ECONOMIC_STRESS,
        source_type=SourceType.CONSTRUCTED,
        series_id=None,
        evidence_rating=EvidenceRating.MODERATE,
        norm_direction=NormDirection.HIGHER_IS_WORSE,
        frequency="monthly",
        coverage_start=1957,
        short_series=False,
        construction_recipe=(
            "Compute YoY growth rate for CPI components: CUSR0000SAH1 (shelter), "
            "CPIFABSL (food), CPIENGSL (energy), CPIMEDSL (medical care). "
            "Weight by budget share: shelter 33%, food 13%, energy 7%, "
            "healthcare 9%, other from CPIAUCSL remainder. "
            "Weighted average = essential cost pressure index."
        ),
        manual_source=None,
    ),

    # =========================================================================
    # DOMAIN 2: POLITICAL POLARIZATION & ELITE DYNAMICS (8 variables)
    # =========================================================================

    # #3 Political Polarization (Congressional)
    Variable(
        catalog_number=3,
        name="Political Polarization (Congressional DW-NOMINATE)",
        domain=Domain.POLITICAL_POLARIZATION,
        source_type=SourceType.MANUAL_DOWNLOAD,
        series_id=None,
        evidence_rating=EvidenceRating.STRONG,
        norm_direction=NormDirection.HIGHER_IS_WORSE,
        frequency="biennial",
        coverage_start=1789,
        short_series=False,
        construction_recipe=(
            "VoteView HSall_members.csv: |mean(Republican dim1) - "
            "mean(Democrat dim1)| per Congress. Higher = more polarized."
        ),
        manual_source="https://voteview.com/data",
    ),

    # #4 Affective Polarization
    Variable(
        catalog_number=4,
        name="Affective Polarization (ANES Feeling Thermometer Gap)",
        domain=Domain.POLITICAL_POLARIZATION,
        source_type=SourceType.MANUAL_DOWNLOAD,
        series_id=None,
        evidence_rating=EvidenceRating.STRONG,
        norm_direction=NormDirection.HIGHER_IS_WORSE,
        frequency="biennial",
        coverage_start=1948,
        short_series=False,
        construction_recipe=(
            "ANES Cumulative File: mean(VCF0218 in-party thermometer) - "
            "mean(VCF0224 out-party thermometer). Higher gap = more "
            "affective polarization."
        ),
        manual_source="https://electionstudies.org/data-center/",
    ),

    # #11 Elite Factionalism / Fragmentation
    Variable(
        catalog_number=11,
        name="Elite Factionalism (Intra-Party DW-NOMINATE SD)",
        domain=Domain.POLITICAL_POLARIZATION,
        source_type=SourceType.CONSTRUCTED,
        series_id=None,
        evidence_rating=EvidenceRating.STRONG,
        norm_direction=NormDirection.HIGHER_IS_WORSE,
        frequency="biennial",
        coverage_start=1789,
        short_series=False,
        construction_recipe=(
            "VoteView HSall_members.csv: Compute SD of nominate_dim1 within "
            "each party per Congress. Factionalism = max(SD_R, SD_D). "
            "Higher SD = more internal fragmentation."
        ),
        manual_source="https://voteview.com/data",
    ),

    # #15 Horizontal Inequality (Between-Group)
    Variable(
        catalog_number=15,
        name="Horizontal Inequality (Racial Income Ratio)",
        domain=Domain.POLITICAL_POLARIZATION,
        source_type=SourceType.MANUAL_DOWNLOAD,
        series_id=None,
        evidence_rating=EvidenceRating.MODERATE,
        norm_direction=NormDirection.LOWER_IS_WORSE,
        frequency="annual",
        coverage_start=1967,
        short_series=False,
        construction_recipe=(
            "Census historical tables H-5/H-9: (Black median HH income) / "
            "(White median HH income). Declining ratio = increasing "
            "horizontal inequality."
        ),
        manual_source="https://www.census.gov/data/tables/time-series/demo/income-poverty/historical-income-households.html",
    ),

    # #19 Intra-Elite Wealth Gap
    Variable(
        catalog_number=19,
        name="Intra-Elite Wealth Gap (Top 0.1% Concentration)",
        domain=Domain.POLITICAL_POLARIZATION,
        source_type=SourceType.CONSTRUCTED,
        series_id=None,
        evidence_rating=EvidenceRating.MODERATE,
        norm_direction=NormDirection.HIGHER_IS_WORSE,
        frequency="quarterly",
        coverage_start=1989,
        short_series=False,
        construction_recipe=(
            "Intra-elite ratio: WFRBSTP1300 / (WFRBST01134 - WFRBSTP1300). "
            "Higher ratio = more concentration within top 1%. "
            "Requires WFRBST01134 as component."
        ),
        manual_source=None,
    ),

    # #20 Middle-Class Income Share
    Variable(
        catalog_number=20,
        name="Middle-Class Income Share (Census Quintiles)",
        domain=Domain.POLITICAL_POLARIZATION,
        source_type=SourceType.MANUAL_DOWNLOAD,
        series_id=None,
        evidence_rating=EvidenceRating.MODERATE,
        norm_direction=NormDirection.LOWER_IS_WORSE,
        frequency="annual",
        coverage_start=1967,
        short_series=False,
        construction_recipe=(
            "Census Table H-2: Sum 2nd + 3rd + 4th quintile income shares. "
            "Declining share = middle-class squeeze."
        ),
        manual_source="https://www.census.gov/data/tables/time-series/demo/income-poverty/historical-income-households.html",
    ),

    # #31 Anti-System Party Vote Share
    Variable(
        catalog_number=31,
        name="Anti-System Party Vote Share",
        domain=Domain.POLITICAL_POLARIZATION,
        source_type=SourceType.MANUAL_DOWNLOAD,
        series_id=None,
        evidence_rating=EvidenceRating.MODERATE,
        norm_direction=NormDirection.HIGHER_IS_WORSE,
        frequency="biennial",
        coverage_start=1789,
        short_series=False,
        construction_recipe=(
            "MIT Election Lab returns: third-party + anti-system candidate "
            "vote share. Coding decision for 'anti-system' classification "
            "deferred to Phase 4 implementation."
        ),
        manual_source="https://electionlab.mit.edu/data",
    ),

    # #45 Wealth Concentration (Top 0.1%)
    Variable(
        catalog_number=45,
        name="Wealth Concentration (Top 0.1% Net Worth Share)",
        domain=Domain.POLITICAL_POLARIZATION,
        source_type=SourceType.FRED_API,
        series_id="WFRBSTP1300",
        evidence_rating=EvidenceRating.STRONG,
        norm_direction=NormDirection.HIGHER_IS_WORSE,
        frequency="quarterly",
        coverage_start=1989,
        short_series=False,
        construction_recipe=None,
        manual_source=None,
    ),

    # =========================================================================
    # DOMAIN 3: INSTITUTIONAL / DEMOCRATIC QUALITY (8 variables)
    # =========================================================================

    # #13 Regime Type / Institutional Quality
    Variable(
        catalog_number=13,
        name="Regime Type / Institutional Quality (V-Dem Liberal Democracy)",
        domain=Domain.INSTITUTIONAL_QUALITY,
        source_type=SourceType.MANUAL_DOWNLOAD,
        series_id=None,
        evidence_rating=EvidenceRating.STRONG,
        norm_direction=NormDirection.LOWER_IS_WORSE,
        frequency="annual",
        coverage_start=1789,
        short_series=False,
        construction_recipe=None,
        manual_source="https://v-dem.net/data/the-v-dem-dataset/",
    ),

    # #21 Judicial Independence
    Variable(
        catalog_number=21,
        name="Judicial Independence (V-Dem Judicial Constraints)",
        domain=Domain.INSTITUTIONAL_QUALITY,
        source_type=SourceType.MANUAL_DOWNLOAD,
        series_id=None,
        evidence_rating=EvidenceRating.MODERATE,
        norm_direction=NormDirection.LOWER_IS_WORSE,
        frequency="annual",
        coverage_start=1789,
        short_series=False,
        construction_recipe=None,
        manual_source="https://v-dem.net/data/the-v-dem-dataset/",
    ),

    # #22 Freedom of Expression / Media Independence
    Variable(
        catalog_number=22,
        name="Freedom of Expression (V-Dem FreeExp+AltInfo)",
        domain=Domain.INSTITUTIONAL_QUALITY,
        source_type=SourceType.MANUAL_DOWNLOAD,
        series_id=None,
        evidence_rating=EvidenceRating.MODERATE,
        norm_direction=NormDirection.LOWER_IS_WORSE,
        frequency="annual",
        coverage_start=1789,
        short_series=False,
        construction_recipe=None,
        manual_source="https://v-dem.net/data/the-v-dem-dataset/",
    ),

    # #23 Legislative Constraints on Executive
    Variable(
        catalog_number=23,
        name="Legislative Constraints on Executive (V-Dem)",
        domain=Domain.INSTITUTIONAL_QUALITY,
        source_type=SourceType.MANUAL_DOWNLOAD,
        series_id=None,
        evidence_rating=EvidenceRating.MODERATE,
        norm_direction=NormDirection.LOWER_IS_WORSE,
        frequency="annual",
        coverage_start=1789,
        short_series=False,
        construction_recipe=None,
        manual_source="https://v-dem.net/data/the-v-dem-dataset/",
    ),

    # #24 Electoral Integrity / Fraud Perception
    Variable(
        catalog_number=24,
        name="Electoral Integrity (V-Dem Clean Elections)",
        domain=Domain.INSTITUTIONAL_QUALITY,
        source_type=SourceType.MANUAL_DOWNLOAD,
        series_id=None,
        evidence_rating=EvidenceRating.MODERATE,
        norm_direction=NormDirection.LOWER_IS_WORSE,
        frequency="annual",
        coverage_start=1789,
        short_series=False,
        construction_recipe=None,
        manual_source="https://v-dem.net/data/the-v-dem-dataset/",
    ),

    # #29 Voter Access Restrictions / Partisan Gerrymandering
    Variable(
        catalog_number=29,
        name="Voter Access / Gerrymandering (Grumbach SDI)",
        domain=Domain.INSTITUTIONAL_QUALITY,
        source_type=SourceType.MANUAL_DOWNLOAD,
        series_id=None,
        evidence_rating=EvidenceRating.MODERATE,
        norm_direction=NormDirection.LOWER_IS_WORSE,
        frequency="annual",
        coverage_start=2000,
        short_series=True,
        construction_recipe=(
            "Grumbach SDI: population-weighted national average across "
            "all states. Declining = more voter restrictions."
        ),
        manual_source="https://dataverse.harvard.edu/",
    ),

    # #32 Executive Aggrandizement
    Variable(
        catalog_number=32,
        name="Executive Aggrandizement (V-Dem Executive Respect Constitution)",
        domain=Domain.INSTITUTIONAL_QUALITY,
        source_type=SourceType.MANUAL_DOWNLOAD,
        series_id=None,
        evidence_rating=EvidenceRating.MODERATE,
        norm_direction=NormDirection.LOWER_IS_WORSE,
        frequency="annual",
        coverage_start=1789,
        short_series=False,
        construction_recipe=None,
        manual_source="https://v-dem.net/data/the-v-dem-dataset/",
    ),

    # #38 State Capacity / Institutional Quality
    Variable(
        catalog_number=38,
        name="State Capacity (World Bank WGI Government Effectiveness)",
        domain=Domain.INSTITUTIONAL_QUALITY,
        source_type=SourceType.MANUAL_DOWNLOAD,
        series_id=None,
        evidence_rating=EvidenceRating.MODERATE,
        norm_direction=NormDirection.LOWER_IS_WORSE,
        frequency="annual",
        coverage_start=1996,
        short_series=False,
        construction_recipe=None,
        manual_source="https://info.worldbank.org/governance/wgi/",
    ),

    # #39 Neighborhood / Diffusion Effects (Allied Democracies)
    Variable(
        catalog_number=39,
        name="Neighborhood Effects (Allied Democracy Quality)",
        domain=Domain.INSTITUTIONAL_QUALITY,
        source_type=SourceType.MANUAL_DOWNLOAD,
        series_id=None,
        evidence_rating=EvidenceRating.WEAK,
        norm_direction=NormDirection.LOWER_IS_WORSE,
        frequency="annual",
        coverage_start=1789,
        short_series=False,
        construction_recipe=(
            "V-Dem v2x_libdem: compute mean liberal democracy score across "
            "OECD/NATO member democracies. Declining average = democratic "
            "neighborhood deterioration. Uses same V-Dem v15 dataset as "
            "Domain 3 institutional variables."
        ),
        manual_source="https://v-dem.net/data/the-v-dem-dataset/",
    ),

    # =========================================================================
    # DOMAIN 4: SOCIAL MOBILIZATION & TRUST (10 variables)
    # (11 in catalog minus #44 Cross-Class Coalition which is Unavailable)
    # =========================================================================

    # #7 Government Trust / State Legitimacy
    Variable(
        catalog_number=7,
        name="Government Trust (ANES VCF0604)",
        domain=Domain.SOCIAL_MOBILIZATION,
        source_type=SourceType.MANUAL_DOWNLOAD,
        series_id=None,
        evidence_rating=EvidenceRating.STRONG,
        norm_direction=NormDirection.LOWER_IS_WORSE,
        frequency="biennial",
        coverage_start=1958,
        short_series=False,
        construction_recipe=None,
        manual_source="https://electionstudies.org/data-center/",
    ),

    # #12 Protest Frequency and Participation
    Variable(
        catalog_number=12,
        name="Protest Frequency and Participation (ACLED US)",
        domain=Domain.SOCIAL_MOBILIZATION,
        source_type=SourceType.MANUAL_DOWNLOAD,
        series_id=None,
        evidence_rating=EvidenceRating.STRONG,
        norm_direction=NormDirection.HIGHER_IS_WORSE,
        frequency="monthly",
        coverage_start=2020,
        short_series=True,
        construction_recipe=None,
        manual_source="https://acleddata.com/",
    ),

    # #25 Civil Society Density / Union Membership
    Variable(
        catalog_number=25,
        name="Civil Society Density / Union Membership Rate",
        domain=Domain.SOCIAL_MOBILIZATION,
        source_type=SourceType.MANUAL_DOWNLOAD,
        series_id=None,
        evidence_rating=EvidenceRating.MODERATE,
        norm_direction=NormDirection.LOWER_IS_WORSE,
        frequency="annual",
        coverage_start=1983,
        short_series=False,
        construction_recipe=None,
        manual_source="https://www.bls.gov/news.release/union2.htm",
    ),

    # #26 Youth Unemployment / Disconnection
    Variable(
        catalog_number=26,
        name="Youth Unemployment Rate (16-19)",
        domain=Domain.SOCIAL_MOBILIZATION,
        source_type=SourceType.FRED_API,
        series_id="LNS14000012",
        evidence_rating=EvidenceRating.MODERATE,
        norm_direction=NormDirection.HIGHER_IS_WORSE,
        frequency="monthly",
        coverage_start=1948,
        short_series=False,
        construction_recipe=None,
        manual_source=None,
    ),

    # #30 Democratic Commitment (Attitudinal)
    Variable(
        catalog_number=30,
        name="Democratic Commitment (WVS + ANES)",
        domain=Domain.SOCIAL_MOBILIZATION,
        source_type=SourceType.MANUAL_DOWNLOAD,
        series_id=None,
        evidence_rating=EvidenceRating.MODERATE,
        norm_direction=NormDirection.LOWER_IS_WORSE,
        frequency="irregular",
        coverage_start=1981,
        short_series=False,
        construction_recipe=None,
        manual_source="https://www.worldvaluessurvey.org/",
    ),

    # #34 Conspiratorial Thinking Prevalence
    Variable(
        catalog_number=34,
        name="Conspiratorial Thinking Prevalence (PRRI)",
        domain=Domain.SOCIAL_MOBILIZATION,
        source_type=SourceType.MANUAL_DOWNLOAD,
        series_id=None,
        evidence_rating=EvidenceRating.WEAK,
        norm_direction=NormDirection.HIGHER_IS_WORSE,
        frequency="annual",
        coverage_start=2020,
        short_series=True,
        construction_recipe=None,
        manual_source="https://www.prri.org/",
    ),

    # #36 Protest Diffusion / Contagion
    Variable(
        catalog_number=36,
        name="Protest Diffusion / Contagion (ACLED-derived)",
        domain=Domain.SOCIAL_MOBILIZATION,
        source_type=SourceType.CONSTRUCTED,
        series_id=None,
        evidence_rating=EvidenceRating.WEAK,
        norm_direction=NormDirection.HIGHER_IS_WORSE,
        frequency="monthly",
        coverage_start=2020,
        short_series=True,
        construction_recipe=(
            "ACLED US events: spatial-temporal clustering analysis. "
            "Count 'daughter' events within 500km and 30 days of initial event. "
            "Higher = faster/wider geographic spread."
        ),
        manual_source="https://acleddata.com/",
    ),

    # #37 Prior Protest Experience
    Variable(
        catalog_number=37,
        name="Prior Protest Experience (ACLED-derived cumulative)",
        domain=Domain.SOCIAL_MOBILIZATION,
        source_type=SourceType.CONSTRUCTED,
        series_id=None,
        evidence_rating=EvidenceRating.WEAK,
        norm_direction=NormDirection.HIGHER_IS_WORSE,
        frequency="monthly",
        coverage_start=2020,
        short_series=True,
        construction_recipe=(
            "ACLED US events: cumulative event counts per region. "
            "log(1 + cumulative events in region over prior N years). "
            "Higher = more protest infrastructure."
        ),
        manual_source="https://acleddata.com/",
    ),

    # #41 Institutional Legitimacy Denial
    Variable(
        catalog_number=41,
        name="Institutional Legitimacy Denial (Bright Line Watch)",
        domain=Domain.SOCIAL_MOBILIZATION,
        source_type=SourceType.MANUAL_DOWNLOAD,
        series_id=None,
        evidence_rating=EvidenceRating.WEAK,
        norm_direction=NormDirection.HIGHER_IS_WORSE,
        frequency="quarterly",
        coverage_start=2017,
        short_series=True,
        construction_recipe=None,
        manual_source="https://brightlinewatch.org/",
    ),

    # #42 Political Efficacy Beliefs
    Variable(
        catalog_number=42,
        name="Political Efficacy Beliefs (ANES VCF0613/VCF0614)",
        domain=Domain.SOCIAL_MOBILIZATION,
        source_type=SourceType.MANUAL_DOWNLOAD,
        series_id=None,
        evidence_rating=EvidenceRating.WEAK,
        norm_direction=NormDirection.LOWER_IS_WORSE,
        frequency="biennial",
        coverage_start=1952,
        short_series=False,
        construction_recipe=None,
        manual_source="https://electionstudies.org/data-center/",
    ),

    # =========================================================================
    # DOMAIN 5: INFORMATION / MEDIA ECOSYSTEM (1 variable)
    # (4 in catalog minus 3 unavailable: #33, #35, #43)
    # =========================================================================

    # #28 Media Trust / Partisan Media Trust Gap
    Variable(
        catalog_number=28,
        name="Media Trust / Partisan Trust Gap (Gallup + Pew)",
        domain=Domain.INFORMATION_MEDIA,
        source_type=SourceType.MANUAL_DOWNLOAD,
        series_id=None,
        evidence_rating=EvidenceRating.MODERATE,
        norm_direction=NormDirection.LOWER_IS_WORSE,
        frequency="annual",
        coverage_start=1973,
        short_series=False,
        construction_recipe=(
            "Gallup 'Confidence in Mass Media' aggregate (1973-present). "
            "Supplement with Pew partisan trust gap: Dem trust % - Rep trust % "
            "(2014-present). Increasing gap = more polarized info environment."
        ),
        manual_source="https://gallup.com/",
    ),
]


# ---------------------------------------------------------------------------
# Helper: domain groupings for quick lookup
# ---------------------------------------------------------------------------

def get_variables_by_domain(domain: Domain) -> list[Variable]:
    """Return all variables belonging to a given domain."""
    return [v for v in VARIABLES if v.domain == domain]


def get_fred_variables() -> list[Variable]:
    """Return all variables that can be fetched from the FRED API."""
    return [v for v in VARIABLES if v.source_type == SourceType.FRED_API]


def get_manual_variables() -> list[Variable]:
    """Return all variables requiring manual download."""
    return [v for v in VARIABLES if v.source_type == SourceType.MANUAL_DOWNLOAD]


def get_constructed_variables() -> list[Variable]:
    """Return all variables that must be constructed from components."""
    return [v for v in VARIABLES if v.source_type == SourceType.CONSTRUCTED]


# ---------------------------------------------------------------------------
# Validation: verify weight sums and variable count at import time
# ---------------------------------------------------------------------------

def _validate_config() -> None:
    """Verify configuration consistency at module load."""
    # Domain weights must sum to 1.0
    domain_sum = sum(DOMAIN_WEIGHTS.values())
    assert abs(domain_sum - 1.0) < 1e-9, (
        f"DOMAIN_WEIGHTS sum to {domain_sum}, expected 1.0"
    )

    # Model weights must sum to 1.0
    model_sum = sum(MODEL_WEIGHTS.values())
    assert abs(model_sum - 1.0) < 1e-9, (
        f"MODEL_WEIGHTS sum to {model_sum}, expected 1.0"
    )

    # Exactly 41 measurable variables
    assert len(VARIABLES) == 41, (
        f"Expected 41 variables, found {len(VARIABLES)}"
    )

    # Verify no excluded variable numbers are present
    excluded = {33, 35, 43, 44}
    present_numbers = {v.catalog_number for v in VARIABLES}
    overlap = excluded & present_numbers
    assert not overlap, (
        f"Unavailable variables should not be in VARIABLES: {overlap}"
    )


_validate_config()
