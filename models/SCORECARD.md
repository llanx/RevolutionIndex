# Model Validation Scorecard

> Persistent tracking of model validation results across iterations.
> Updated manually after each validation run. See `VALIDATION.md` for detailed auto-generated output.

## Current Status

| Field | Value |
|-------|-------|
| **Verdict** | FAIL |
| **Last Run** | 2026-03-05 |
| **Mode** | full (live FRED pipeline) |
| **Variables** | 15 of 41 |
| **Primary Issue** | Score compression from missing data (26 manual-download variables unavailable) |

## Key Metrics

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Zone Accuracy (Strict) | 50.0% (5/10) | >= 75% | FAIL |
| Zone Accuracy (Lenient) | 70.0% (7/10) | informational | -- |
| Monotonic Ordering | FAIL (crisis min 45.2, stability max 46.0) | crisis > stability | FAIL |
| Max Calibration Residual | 26.0 | <= 15 | FAIL |
| Bootstrap CI Discriminability | No (gap 13.6, CI width 21.3) | gap > CI width | FAIL |
| Weight Sensitivity | 0.0 max shift | < 25 | PASS |
| Spurious Trends | None detected | no flags | PASS |

## Diagnosis

### What's Working

- **Directional signal is correct.** All zone misses are near-boundary cases (within 3 points of the correct zone). The model captures relative ordering of events even with limited data.
- **No fragility.** Weight perturbation (+/-20%) produces zero score shift, meaning no single model dominates the ensemble.
- **No spurious trends.** Decade-level analysis shows no monotonic drift, no data boundary artifacts, no saturation. Scores move with events, not with time.
- **History-only mode shows strong separation.** With pre-calibrated history data, crisis scores (62-77) cleanly separate from stability scores (1.7-20), confirming the calibration logic works.

### What's Failing

- **Score compression in full mode.** With only 15 of 41 variables available (all from FRED API), scores compress into a narrow band (~27-60) instead of spanning the full 0-100 calibrated range. This is the root cause of all three criterion failures.
- **Monotonic ordering breaks** because compressed scores can't separate crisis from stability episodes. The 2008 crisis scores 59.6 while mid-1990s stability scores 46.0, a gap of only 13.6 points.
- **Calibration residuals spike** because the live pipeline produces different raw scores than the history-only path, and the calibration anchors were tuned to the full 41-variable set.
- **Bootstrap CIs are too wide** relative to the crisis/stability gap, making zones statistically indistinguishable.

### Root Cause

The model architecture is sound but data-starved. Of the 41 configured variables:
- 12 are FRED API (auto-fetched, working)
- 7 are constructed from FRED components (~3 working, depends on component availability)
- 22 are manual-download (V-Dem, VoteView, ANES, ACLED, etc., all missing)

The 22 manual-download variables include most of the political polarization, institutional quality, and social mobilization indicators. Without them, 3 of 5 domains are severely underrepresented.

## Validation Run History

| Run | Date | Mode | Vars | Zone (Strict) | Zone (Lenient) | Monotonic | Max Residual | CI Gap | Verdict |
|-----|------|------|------|---------------|----------------|-----------|-------------|--------|---------|
| 1 | 2026-03-05 | history-only | 15/41 | 50.0% (4/8) | 87.5% (7/8) | PASS | N/A | N/A | FAIL |
| 2 | 2026-03-05 | full | 15/41 | 50.0% (5/10) | 70.0% (7/10) | FAIL | 26.0 | No | FAIL |

**Notes on Run 1 vs Run 2:**
- Run 1 (history-only) uses pre-calibrated scores from `history.json`, so monotonic ordering passes and scores span the full range. LOOCV and calibration residual tests are skipped in this mode.
- Run 2 (full) runs the live pipeline with only FRED data available, exposing the score compression problem. Two additional episodes (1960s, Watergate) become testable because the pipeline generates scores back to 1947.

## Next Steps

1. **Download manual data files (highest priority).** The 22 manual-download variables are the primary blocker. Prioritize:
   - V-Dem democracy indices (8 variables across domains 2-3)
   - VoteView polarization scores (2 variables, domain 2)
   - ANES trust/social cohesion surveys (3 variables, domain 4)
   - ACLED protest/unrest data (2 variables, domain 4)

2. **Re-run validation after each data addition.** Add a new row to this scorecard after each batch of manual data is integrated. Track whether zone accuracy and monotonic ordering improve incrementally.

3. **Recalibrate anchors with full data.** Once 30+ variables are available, re-run `calibrate.py` to re-fit the 5 calibration anchors. The current anchors assume all 41 variables contribute.

4. **Investigate 2016 Election overshoot.** Both runs score 2016 in Crisis Territory (54.0 history-only, 46.2 full) when it should be Elevated Tension (35-50). This may indicate the economic stress domain is over-weighted for that period.

5. **Address LOOCV overfitting flags.** Mid-1990s stability (residual 32.9) and Post-9/11 (residual 34.6) show high leave-one-out deviation. These anchors may need adjustment once more data is available.

---
*Last updated: 2026-03-05, Run 2*
