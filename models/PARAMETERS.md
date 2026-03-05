# Model Parameters Reference

All hardcoded parameters in the Revolution Index model pipeline, with source justification and sensitivity classification.

## Sensitivity Classification
- **HIGH**: Changing by 20% shifts the composite score by >5 points
- **MEDIUM**: Changing by 20% shifts the composite score by 2-5 points
- **LOW**: Changing by 20% shifts the composite score by <2 points

## Ensemble Weights (config.py)

| Parameter | Value | Source | Sensitivity |
|-----------|-------|--------|-------------|
| PSI weight | 0.25 | Turchin (2003-2023) validation history | HIGH |
| PLI weight | 0.20 | Prospect theory framework (Kahneman & Tversky 1979) | HIGH |
| FSP weight | 0.15 | Funke et al. (2016) empirical mechanism | HIGH |
| Georgescu SDT weight | 0.25 | Georgescu (2023) developed-economy applicability | HIGH |
| V-Dem ERT weight | 0.15 | Diagnostic (not predictive), institutional coverage | HIGH |

## PSI Parameters (model_psi.py)

| Parameter | Value | Source | Sensitivity |
|-----------|-------|--------|-------------|
| Geometric mean floor | 0.01 | Prevents zero-collapse from data gaps | MEDIUM |
| Evidence weight: Strong | 3.0 | Literature consensus weighting | MEDIUM |
| Evidence weight: Moderate | 2.0 | Literature consensus weighting | LOW |
| Evidence weight: Weak | 1.0 | Literature consensus weighting | LOW |

## PLI Parameters (model_pli.py)

| Parameter | Value | Source | Sensitivity |
|-----------|-------|--------|-------------|
| Lambda (loss aversion) | 2.25 | Tversky & Kahneman (1992) | HIGH |
| Alpha (diminishing sensitivity) | 0.88 | Tversky & Kahneman (1992) | MEDIUM |
| K: Wage/Income | 50.0 | Spec A2 fix (500/10) | HIGH |
| K: Employment | 3.5 | Spec A2 fix (35/10) | MEDIUM |
| K: Cost-of-Living | 10.0 | Spec A2 fix (100/10) | MEDIUM |
| K: Financial | 1.0 | Spec A2 fix (10/10) | LOW |
| Max breadth bonus | 20.0 | Additive cap (critical review A2) | MEDIUM |
| Max velocity bonus | 15.0 | Additive cap (critical review A2) | MEDIUM |
| Velocity lookback | 12 periods | Rate-of-change window | LOW |

## FSP Parameters (model_fsp.py)

| Parameter | Value | Source | Sensitivity |
|-----------|-------|--------|-------------|
| Transmission lag | 60 months | Funke et al. (2016): 5-10 year lag | MEDIUM |
| Leading/trailing edge weights | 0.6 / 0.4 | Early warning sensitivity tradeoff | MEDIUM |
| Transmission coefficient range | [0.5, 1.5] | Bounded amplification | LOW |
| ETI: Unemployment weight | 0.38 | Redistributed from CSCICP03USM665S removal | MEDIUM |
| ETI: Labor share weight | 0.30 | Redistributed from CSCICP03USM665S removal | MEDIUM |
| ETI: Inflation weight | 0.22 | New component (partial CSCICP weight) | LOW |
| ETI: Household debt weight | 0.10 | New component (debt burden channel) | LOW |

## Georgescu SDT Parameters (model_georgescu.py)

| Parameter | Value | Source | Sensitivity |
|-----------|-------|--------|-------------|
| Elite overproduction weight | 0.35 | Georgescu (2023) empirical correlation | HIGH |
| Mass immiseration weight | 0.40 | Georgescu (2023) most variable component | HIGH |
| State fiscal distress weight | 0.25 | Georgescu (2023) persistent but slow-moving | MEDIUM |

## V-Dem ERT Parameters (model_vdem.py)

| Parameter | Value | Source | Sensitivity |
|-----------|-------|--------|-------------|
| Rate-of-change window | 5 years | Standard ERT assessment window | MEDIUM |
| Sigmoid scale factor | 10.0 | Calibrated: -0.17 change (US 2015-2022) maps to ~0.85 stress | HIGH |
| Liberal Democracy weight | 0.25 | Primary composite measure | MEDIUM |
| Judicial Independence weight | 0.20 | Rule of law backbone | MEDIUM |
| Freedom of Expression weight | 0.15 | Information environment | LOW |
| Legislative Constraints weight | 0.15 | Checks on executive | LOW |
| Electoral Integrity weight | 0.15 | Procedural democracy | LOW |
| Executive Aggrandizement weight | 0.10 | Executive overreach | LOW |
| State Capacity weight | 0.10 | Level indicator (not ROC) | LOW |
| Voter Access weight | 0.05 | Level indicator (not ROC) | LOW |

## Calibration Parameters (calibrate.py)

| Parameter | Value | Source | Sensitivity |
|-----------|-------|--------|-------------|
| 2008-10 anchor target | 65 | Mid Crisis Territory (51-75) | HIGH |
| 2020-06 anchor target | 65 | Mid Crisis Territory (51-75) | HIGH |
| 1994-1997 anchor target | 20 | Mid Stable (0-25) | HIGH |
| 2001-09 anchor target | 42 | Elevated Tension (post-9/11 + dot-com) | MEDIUM |
| 2011-08 anchor target | 47 | High Elevated (debt ceiling + credit downgrade) | MEDIUM |
| Calibration method | Least-squares linear | N-2 degrees of freedom | HIGH |
| Bootstrap iterations | 1000 | Sufficient for 90% CI stability | LOW |
| CI width | 0.90 | Standard 90% confidence interval | LOW |

## Pipeline Parameters (config.py, pipeline.py)

| Parameter | Value | Source | Sensitivity |
|-----------|-------|--------|-------------|
| Rolling window (normalization) | 240 months (20 years) | Long-term baseline for z-scores | MEDIUM |
| Short series fallback | percentile_rank | For series starting after 2000 | LOW |
| MIN_DOMAINS_REQUIRED | 2 | Minimum domains for history inclusion | LOW |
| Stale data threshold | 30 days | Freshness tracking | LOW |
