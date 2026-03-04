# Revolution Index: Model Architecture Selection

**Date:** 2026-03-04
**Phase:** 04 - Model Building
**Requirement:** MOD-01 (Architecture Selection Document)

## Architecture: 5-Model Evidence-Weighted Ensemble

The Revolution Index uses a **5-model evidence-weighted ensemble** producing a composite 0-100 score. Each model captures a distinct theoretical dimension of political instability, and the ensemble combines them via weighted average to produce a single composite score.

## Model Selection and Rationale

### Why 5 Models?

Phase 2 literature mining (6 domain reviews, 45 variables cataloged) revealed that the original 3 models (Turchin PSI, Prospect Theory PLI, Financial Stress Pathway) cover only **12 of 45 identified variables (27%)**. Two critical dimensions were entirely uncovered:

1. **Elite overproduction via education-job mismatch** (Georgescu SDT) provides a more US-applicable operationalization than top 1% income share
2. **Institutional/democratic quality** (V-Dem ERT) was identified as a missing dimension across all existing models

Adding Georgescu SDT and V-Dem ERT extends coverage across all 5 identified domains.

### Models Selected

| # | Model | Theoretical Basis | Primary Domain | Key Variables |
|---|-------|------------------|----------------|---------------|
| 1 | **Turchin PSI** | Structural-Demographic Theory (Turchin 2003, 2023) | Economic Stress | Labor share, debt/GDP, elite overproduction |
| 2 | **Prospect Theory PLI** | Prospect Theory (Kahneman & Tversky), applied by Passarelli & Del Ponte (2020) | Economic Stress / Social Mobilization | Consumer sentiment, unemployment, real wages, financial stress |
| 3 | **Financial Stress Pathway** | Funke et al. (2016) financial crisis transmission | Economic Stress | STLFSI4, credit spreads, bank lending standards |
| 4 | **Georgescu SDT** | Structural-Demographic Theory for industrialized societies (Georgescu 2023) | Political Polarization / Economic Stress | Education-job mismatch, intra-elite wealth gap, youth unemployment |
| 5 | **V-Dem ERT** | Episodes of Regime Transformation (V-Dem Institute 2023) | Institutional Quality | Liberal democracy index, judicial independence, legislative constraints, electoral integrity |

### Phase 1 Fixes Incorporated

Each model incorporates fixes identified during Phase 1 validation:

- **PSI:** Geometric mean aggregation (not arithmetic), corrected min-max normalization replaced with rolling z-score (fixes the pinning bug at impl A1)
- **PLI:** K constant corrections per Passarelli & Del Ponte specification, sqrt+*10 transformation documented and preserved
- **FSP:** CSCICP03USM665S weight dropped from ETI and redistributed (series discontinued Jan 2024)

## Ensemble Weights (Provisional)

| Model | Weight | Rationale |
|-------|--------|-----------|
| Turchin PSI | 0.25 | Strong evidence, long validation history (Turchin 2003, 2023), covers structural-demographic fundamentals |
| Prospect Theory PLI | 0.20 | Strong economic evidence, prospect theory well-validated (Kahneman & Tversky 1979), captures subjective economic experience |
| Financial Stress Pathway | 0.15 | Transmission mechanism well-documented (Funke et al. 2016: 30% far-right vote increase post-crisis), but narrower scope |
| Georgescu SDT | 0.25 | Most directly applicable to developed democracies (Georgescu 2023 OECD validation), fills elite overproduction gap with better US proxy |
| V-Dem ERT | 0.15 | Primarily diagnostic rather than predictive, but captures the institutional dimension entirely missing from other models |

**Note:** These weights are provisional. Phase 5 validation (backtesting against 7 historical episodes) may adjust them based on empirical performance.

## Data Availability

- **41 of 45 variables measurable (91%)** from Phase 3 data source inventory
- **4 unavailable variables** (all weak-rated, dropped): #33 Misinformation Prevalence, #35 Social Media Political Engagement, #43 Information Fragmentation/Echo Chambers, #44 Cross-Class Coalition Formation
- **6 proxy-needed variables** have documented construction recipes in the data source inventory
- **15 free API sources** (primarily FRED), **20 manual download sources**, **6 constructed proxies**

## Domain Factor Groupings

The 5 domains from Phase 3 inventory serve as the factor groups displayed on the dashboard:

| Domain | Factor ID | Variable Count | Strong-Rated | Key Variables |
|--------|-----------|---------------|--------------|---------------|
| Economic Stress | `economic_stress` | 13 | 7 (54%) | Gini, labor share, debt/GDP, STLFSI4, unemployment, GDP growth |
| Political Polarization | `political_polarization` | 8 | 4 (50%) | DW-NOMINATE distance, affective polarization, elite factionalism, wealth concentration |
| Institutional Quality | `institutional_quality` | 8 | 1 (13%) | V-Dem liberal democracy, judicial independence, legislative constraints, electoral integrity |
| Social Mobilization | `social_mobilization` | 11 | 2 (18%) | Government trust, protest frequency, union membership, youth unemployment |
| Information & Media | `information_media` | 1* | 0 (0%) | Media trust/partisan trust gap |

*Reduced from 4 after dropping 3 unavailable variables (#33, #35, #43)

## Score Calibration Approach

Historical anchor points for calibration (Phase 5):

| Episode | Expected Zone | Score Range |
|---------|--------------|-------------|
| Mid-1990s (stable period) | Stable | 0-25 |
| 2008 Financial Crisis | Crisis Territory | 51-75 |
| 2020 (pandemic + social unrest) | Crisis Territory | 51-75 |
| Pre-Civil War 1850s (if data available) | Revolution Territory | 76-100 |

Zone boundaries:
- 0-25: Stable
- 26-50: Elevated Tension
- 51-75: Crisis Territory
- 76-100: Revolution Territory

## Pipeline Architecture

```
Data Sources (FRED API, Manual Downloads, Constructed Proxies)
    |
    v
[pipeline.py] Fetch + Cache (data/raw/)
    |
    v
[pipeline.py] LOCF Frequency Alignment (all series -> monthly)
    |
    v
[normalize.py] Rolling Z-Score Normalization (0.0-1.0 stress intensity)
    |
    v
[pipeline.py] Domain Score Aggregation (evidence-weighted averages)
    |
    v
[Plan 02] Model Implementations (PSI, PLI, FSP, Georgescu, V-Dem ERT)
    |
    v
[Plan 03] Ensemble Scoring + JSON Output (current.json, history.json, factors.json)
```

## Key Design Decisions

1. **Rolling z-score over min-max normalization:** Phase 2 recommended rolling z-scores for trending US macroeconomic series. This avoids the pinning bug identified in Phase 1 for PSI (min-max pins 2 of 3 components near 1.0).

2. **LOCF frequency alignment:** All series converted to monthly via Last Observation Carried Forward. No interpolation (per project requirements). Quarterly data forward-filled to monthly; annual data forward-filled to monthly; biennial data forward-filled to monthly.

3. **Evidence-weighted domain aggregation:** Within each domain, variables are weighted by evidence rating (Strong=3, Moderate=2, Weak=1, normalized to sum to 1.0). This ensures strong-evidence variables have proportionally more influence.

4. **20-year rolling window:** The z-score window of 240 months captures secular trends while remaining sensitive to recent changes. Short series (< 240 observations) fall back to percentile rank normalization.

5. **CSCICP03USM665S handling:** Discontinued OECD consumer confidence series dropped from FSP ETI, weight redistributed to remaining inputs. UMCSENT not used as replacement to preserve zero-overlap design between models.

## References

- Turchin, P. (2003). *Historical Dynamics: Why States Rise and Fall*. Princeton University Press.
- Turchin, P. (2023). *End Times: Elites, Counter-Elites, and the Path of Political Disintegration*. Penguin Press.
- Georgescu, I. (2023). "Structural-Demographic Theory and the Political Instability of Industrialized Societies." *OECD Working Paper*.
- V-Dem Institute (2023). *Democracy Report 2023: Defiance in the Face of Autocratization*. University of Gothenburg.
- Funke, M., Schularick, M., & Trebesch, C. (2016). "Going to Extremes: Politics after Financial Crises, 1870-2014." *European Economic Review*, 88, 227-260.
- Passarelli, F. & Del Ponte, A. (2020). "Prospect Theory and Political Decision Making." *Oxford Research Encyclopedia of Politics*.
- Kahneman, D. & Tversky, A. (1979). "Prospect Theory: An Analysis of Decision under Risk." *Econometrica*, 47(2), 263-291.
- Goldstone, J. (1991). *Revolution and Rebellion in the Early Modern World*. University of California Press.
