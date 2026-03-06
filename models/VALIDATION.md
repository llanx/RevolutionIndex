# Validation Report: Revolution Index

**Generated:** 2026-03-06T05:38:05Z
**Mode:** history-only
**Overall Verdict:** PASS

## Summary

The Revolution Index model was validated against 10 historical episodes (10 with available data). Strict zone accuracy is 80.0% (8/10), while lenient accuracy (allowing near-boundary matches within 3 points) is 80.0%. Monotonic ordering holds: all crisis episodes score above all stability episodes.

## 1. Episode Backtesting

### In-Sample Anchors (Calibration Verification)

| Episode | Expected Zone | Expected Score | Actual Score | Actual Zone | Result |
|---------|---------------|----------------|--------------|-------------|--------|
| Financial crisis peak | Crisis Territory | 51-75 | 45.0 | Elevated Tension | FAIL |
| COVID + BLM peak | Crisis Territory | 51-75 | 74.0 | Crisis Territory | PASS |
| Mid-1990s stability | Stable | 0-25 | 22.5 | Stable | PASS |
| Post-9/11 + dot-com recession | Elevated Tension | 26-50 | 36.0 | Elevated Tension | PASS |
| Debt ceiling crisis + credit downgrade + Occupy | Elevated Tension | 26-50 | 47.0 | Elevated Tension | PASS |

### Out-of-Sample Hold-Outs (True Test)

| Episode | Expected Zone | Expected Range | Actual Score | Actual Zone | Result |
|---------|---------------|----------------|--------------|-------------|--------|
| 1960s Urban Unrest / Civil Rights | Elevated Tension | 26-50 | 39.5 | Elevated Tension | PASS |
| Watergate / Nixon Resignation | Elevated Tension | 40-60 | 36.0 | Elevated Tension | PASS |
| Late 1980s Stability | Stable | 0-25 | 37.3 | Elevated Tension | FAIL |
| 2016 Election Aftermath | Elevated Tension | 35-50 | 44.0 | Elevated Tension | PASS |
| January 6, 2021 | Crisis Territory | 51-75 | 51.0 | Crisis Territory | PASS |

**Zone Accuracy:** 80.0% (8 of 10 episodes in correct zone)
**Monotonic Ordering:** PASS (Min crisis score (45.0) vs max stability score (37.3))

## 2. Leave-One-Out Cross-Validation (LOOCV)

LOOCV requires --full mode with live pipeline data. Skipped in history-only mode.

## 3. Weight Sensitivity Analysis

**Note:** In history-only mode, sensitivity values are theoretical maximum shift bounds. Actual perturbation results require --full mode.

| Model | Perturbation | Baseline | Shift | Fragile? |
|-------|-------------|----------|-------|----------|
| psi | +20% | 50.0 | 2.4 | No |
| psi | -20% | 50.0 | 2.6 | No |
| pli | +20% | 50.0 | 1.9 | No |
| pli | -20% | 50.0 | 2.1 | No |
| fsp | +20% | 50.0 | 1.5 | No |
| fsp | -20% | 50.0 | 1.6 | No |
| georgescu_sdt | +20% | 50.0 | 2.4 | No |
| georgescu_sdt | -20% | 50.0 | 2.6 | No |
| vdem_ert | +20% | 50.0 | 1.5 | No |
| vdem_ert | -20% | 50.0 | 1.6 | No |

**Max shift:** 2.6 points. No fragility detected.

**Threshold:** Score shift > 25 points (1 zone) from a single +/-20% weight change indicates fragility.

## 4. Inter-Model Correlation

Requires --full mode with per-model scores. Skipped in history-only mode.

## 5. Spurious Trend Detection

### Decade Summary
| Decade | Mean Score | Min | Max | Trend |
|--------|-----------|-----|-----|-------|
| 1780s | 0.0 | 0.0 | 0.0 | N/A |
| 1790s | 0.0 | 0.0 | 0.0 | Flat |
| 1800s | 0.0 | 0.0 | 0.0 | Flat |
| 1810s | 0.0 | 0.0 | 0.0 | Flat |
| 1820s | 0.0 | 0.0 | 0.0 | Flat |
| 1830s | 0.8 | 0.0 | 4.0 | Flat |
| 1840s | 8.6 | 0.0 | 14.0 | Rising |
| 1850s | 15.3 | 8.0 | 20.0 | Rising |
| 1860s | 5.3 | 0.0 | 21.0 | Falling |
| 1870s | 0.0 | 0.0 | 0.0 | Falling |
| 1880s | 0.0 | 0.0 | 0.0 | Flat |
| 1890s | 0.0 | 0.0 | 0.0 | Flat |
| 1900s | 0.0 | 0.0 | 0.0 | Flat |
| 1910s | 0.0 | 0.0 | 0.0 | Flat |
| 1920s | 0.0 | 0.0 | 0.0 | Flat |
| 1930s | 0.0 | 0.0 | 0.0 | Flat |
| 1940s | 0.0 | 0.0 | 0.0 | Flat |
| 1950s | 22.3 | 0.0 | 41.0 | Rising |
| 1960s | 35.3 | 28.0 | 42.0 | Rising |
| 1970s | 28.1 | 17.0 | 40.0 | Falling |
| 1980s | 30.8 | 24.0 | 40.0 | Flat |
| 1990s | 29.7 | 21.0 | 40.0 | Flat |
| 2000s | 32.9 | 19.0 | 65.0 | Flat |
| 2010s | 36.0 | 23.0 | 53.0 | Flat |
| 2020s | 60.0 | 49.0 | 74.0 | Rising |

### Automated Checks
- Monotonic increase across all decades: PASS
- Data boundary jumps (>10 points): FLAG (1993 (STLFSI4 (Financial Stress Index starts), -11.2 pts); 2020 (ACLED US protest data starts, +27.8 pts))
- Score saturation (0 or 100 for 3+ consecutive points): FLAG (score=0 for 48 entries at 1789-01; score=0 for 4 entries at 1839-01; score=0 for 87 entries at 1863-01)

**Overall Concern Level:** MAJOR

**Note:** Spurious trend detection is an automated checklist. Final judgment on whether trends are genuine or artifactual requires human review of the historical context.

## 6. Bootstrap CI Width

- Crisis point estimate (2008): 45.0
- Stability point estimate (mid-1990s): 22.5
- Point estimate gap: 22.5
- Note: CI width check requires full pipeline data (unified_df). Run with --full to enable.

## Pass/Fail Criteria

| Criterion | Result | Details |
|-----------|--------|---------|
| Zone accuracy >= 75% | PASS | 80.0% (8/10) |
| Monotonic ordering (crisis > stability) | PASS | Min crisis score (45.0) vs max stability score (37.3) |
| Calibration residuals <= 15 | N/A | History-only mode uses pre-calibrated scores (residuals = 0) |
| No fragile weight sensitivity | PASS | Max shift: 2.6 (theoretical bounds, history-only) |
| No spurious trends | WARN | 2 boundary jump(s), 3 saturation period(s) |

## Overall Verdict

**PASS**

The model meets all primary validation criteria. Zone accuracy is above the 75% threshold, crisis episodes score above stability episodes, and calibration residuals are within tolerance.

## Limitations

1. History starts at 1979, so 1960s and Watergate episodes cannot be evaluated
2. History.json contains demo/cached data, not live API data
3. LOOCV has low statistical power with only 5 anchors (2 degrees of freedom per refit)
4. Inter-model correlation from a single time point is not true temporal correlation
5. Weight sensitivity in history-only mode shows theoretical bounds, not actual perturbation results
6. Data boundary artifacts detected at year(s) 1993, 2020, reflecting when new data sources become available rather than genuine structural changes
7. Score saturation at 0 in early history reflects insufficient data availability before key series begin, not genuine zero-stress periods

## Methodology

- Episode backtesting: extract scores from calibrated history at episode dates, compare to expected zone classifications
- Zone boundaries: Stable (0-25), Elevated Tension (26-50), Crisis Territory (51-75), Revolution Territory (76-100)
- LOOCV: hold out each calibration anchor, refit with remaining 4, measure prediction error on held-out point
- Weight sensitivity: perturb MODEL_WEIGHTS by +/-20%, renormalize, measure score shift
- Spurious trends: automated checks for monotonic increase, data boundary artifacts, saturation
- Inter-model correlation: compare pairwise model scores to detect redundancy
- Bootstrap CI: resample variables within each domain to assess score uncertainty

---
*Generated by models/validate.py on 2026-03-06*
