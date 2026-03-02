# Mathematical Fix Checklist

## Overview

This checklist tracks every issue raised in the two critical reviews of the Revolution Index Research project and their resolution status. It covers 15 spec-level issues from `critical-review-model-specs.md` and 12 implementation-level issues from `revolution-index/critical-review-implementation.md`, for a total of 27 tracked items.

**Date:** 2026-03-01
**Scope:** All issues from both critical reviews, mapped to the 3 selected models (PSI, PLI, FSP) and 3 deferred models (RVI, PITF, CSD)

---

## Spec-Level Issues (from critical-review-model-specs.md)

| Review ID | Severity | Model | Issue | Recommended Fix | Applied? | Correct? | New Issues? | Status |
|-----------|----------|-------|-------|-----------------|----------|----------|-------------|--------|
| A1 | Must Fix | PSI | PSI multiplication crushes mid-range values — three 0.70 inputs yield 0.343 | Switch to geometric mean `(MMP×EMP×SFD)^(1/3)` | YES | YES | NONE from geometric mean itself; however implementation review A1 found min-max normalization pins trending series to 1.0 | RESOLVED |
| A2 | Must Fix | PLI | PLI scaling broken — output clusters at 0 or 100 during any recession due to large K constants and multiplicative amplifiers | Reduce K by 5-10x; change breadth/velocity to additive bonuses | YES | PARTIAL | sqrt compression (`np.sqrt(-V*K)*10`) added beyond review scope; `*10` multiplier undocumented; combined K/10+sqrt may double-correct causing underreporting | OPEN |
| A3 | Moderate | RVI (Deferred) | RVI constellation bonus values (0,5,12,22,35) are arbitrary — not derived from formula or theory | Derive from generating function or label as tunable hyperparameters | N/A | N/A | N/A | DEFERRED |
| A4 | Must Fix | PITF (Deferred) | PITF coefficients are fiction — made-up logistic regression coefficients presented as statistical estimates | Drop logistic framing, use actual published PITF coefficients, or re-estimate from data | N/A | N/A | N/A | DEFERRED |
| B1 | High | All | Mixing data frequencies without interpolation strategy — daily to triennial data combined without specifying method | Specify LOCF for most series; align to slowest critical input | YES | YES | NONE | RESOLVED |
| B2 | Moderate | All | Historical distribution lengths wildly inconsistent — percentile rank against 6 years vs. 237 years means different things | Common reference window (e.g., 1970-present) or minimum history requirement | PARTIAL | YES | Expanding window still includes current value (overlaps with impl A1) | RESOLVED |
| B3 | Moderate | PSI (SFD), PLI, RVI | Pew trust series is not continuous — methodology and wording changed multiple times since 1958 | Use ANES cumulative for consistency; supplement with Pew | N/A | N/A | N/A — trust variable dropped in simplified models | DEFERRED |
| B4 | Moderate | All | No missing data strategy — no imputation, carry-forward, or graceful degradation specified | Specify data freshness indicators, imputation rules, recency weighting | PARTIAL | YES | NONE — LOCF and freshness tracking implemented but no graceful degradation | OPEN |
| C1 | High | All | Massive metric overlap / double-counting — same phenomena (trust, inequality, employment, housing) appear in multiple models | Map data dependencies; consider 3 orthogonal models instead of 6; report inter-model correlation | PARTIAL | YES | Construct-level overlap remains (labor share / employment ratio / unemployment measure same underlying construct) | OPEN |
| C2 | Moderate | FSP | FS-PIP lag structure based on N=2 usable data points (2008, 2020) | Be honest about N=2; add more episodes; report uncertainty bands on lag estimates | PARTIAL | YES | NONE — cross-correlation analysis is more honest than hardcoded lags | RESOLVED |
| C3 | Low | RVI (Deferred) | Union density scoring incoherent — declining density scored as "less mobilization capacity" but may indicate destabilizing loss of institutional channels | Split institutional vs. decentralized mobilization | N/A | N/A | N/A | DEFERRED |
| C4 | Moderate | CSD (Deferred) | CSD may detect secular trends, not tipping points — rolling variance/autocorrelation naturally increase in trending series | Detrend input series before CSD analysis; report both raw and detrended | N/A | N/A | N/A | DEFERRED |
| D1 | Must Fix | All | No backtesting protocol — no defined true positives, false positive tolerance, or evaluation metrics | Define historical episodes, expected score levels, evaluation framework | YES | PARTIAL | Backtesting framework exists but treats all 6 episodes as equal severity (impl B3) | OPEN |
| D2 | Must Fix | All | No sensitivity analysis protocol — 50+ weights, 20+ windows, 10+ thresholds, none empirically derived | Systematic parameter variation and output stability testing | NO | N/A | N/A | OPEN |
| D3 | Must Fix | All | No uncertainty quantification — all models produce point estimates without confidence intervals | Add confidence intervals reflecting measurement error, parameter uncertainty, and structural uncertainty | PARTIAL | PARTIAL | Bootstrap only perturbs reference window for PSI (too narrow); K-range for PLI dominates; labeled "parameter sensitivity" not "model uncertainty" | OPEN |

---

## Implementation-Level Issues (from critical-review-implementation.md)

| Review ID | Severity | Model | Issue | Applied? | Status |
|-----------|----------|-------|-------|----------|--------|
| A1 | High | PSI | Min-max normalization against expanding window pins trending series to 1.0 — SFD permanently maxed, EMP near-maxed | NO — `percentile_rank_series` exists in normalization.py:91-119 but is not used | OPEN |
| A2 | Moderate | PLI | Velocity bonus uses deviation magnitude, not actual velocity — redundant with mean loss score | NO — code at prospect_theory.py:184 computes `avg_loss_magnitude`, not rate of change | OPEN |
| A3 | Moderate | FSP | Config ETI weights (6 series, sum 1.0) don't match code weights (4 series, sum 1.0) — ghost entries `debt_service` and `food_energy_cpi` | NO — config and code still diverge | OPEN |
| A4 | Moderate | PSI | WID API URL likely wrong/untested — two inconsistent URLs in wid_loader.py (lines 29 and 82) | NO — neither URL tested against live API | OPEN |
| B1 | High (conceptual) | All | "Zero data overlap" claim misleading — series IDs don't overlap but constructs do (labor share ↔ employment ratio ↔ unemployment) | NO — claim not retracted; inter-model correlation not yet measured | OPEN |
| B2 | Moderate | PSI | PSI with 3 simplified proxies may not measure what Turchin measures — labor share ≠ relative wages, income share ≠ elite overproduction, debt level ≠ fiscal distress | NO — model not labeled as "PSI-Simple" | OPEN |
| B3 | Moderate | All | Backtesting treats all 6 episodes as equal true positives — 1968/2020 (mass mobilization) scored same as 1979 (pure economic stress) | NO — all episodes use threshold 45 | OPEN |
| B4 | Moderate | PSI, PLI | Bootstrap uncertainty too narrow — PSI only varies reference window (±5 years); K-range dominates PLI | NO — not documented as "parameter sensitivity" vs. "model uncertainty" | OPEN |
| C1 | Moderate | All | No tests — tests/ directory contains only empty `__init__.py` | NO — no unit or integration tests | OPEN |
| C2 | Low | All | Config `invert` field defined but never used — models hardcode their own inversion logic | NO — invert field still unused | OPEN |
| C3 | Low-Moderate | FSP | `compute_historical` is O(n²) — recomputes rolling z-score for every date in Python loop | NO — performance issue not addressed | OPEN |
| C4 | Low | FSP | Food/energy CPI planned but not implemented — config references it, code doesn't compute it | NO — ghost configuration remains | OPEN |

---

## Cross-Reference: Issues Appearing in Both Reviews

Five issues were identified in both the spec review and the implementation review, representing problems at the theory level that also manifest in the code:

| Spec Issue | Impl Issue | Nature | Current State |
|------------|-----------|--------|---------------|
| A1: PSI multiplication crushes mid-range values | A1: Min-max normalization pins trending series to 1.0 | **Fix applied, new bug introduced.** The geometric mean fix (spec A1) is correctly applied, but the normalization method (impl A1) creates a separate problem that makes 2 of 3 components near-constant. | Spec A1: RESOLVED. Impl A1: OPEN. |
| A2: PLI scaling broken, clusters at 0/100 | A2: Velocity bonus is magnitude, not velocity | **Fix applied, separate bug present.** K/10 and additive bonuses address the saturation (spec A2), but the velocity computation has an independent bug (impl A2) making it redundant with loss magnitude. | Spec A2: OPEN (undocumented sqrt). Impl A2: OPEN. |
| B1: No interpolation strategy | (Addressed by data pipeline LOCF) | **Fix applied correctly.** LOCF implemented in data_pipeline.py; freshness tracking added. This is the cleanest fix in the codebase. | RESOLVED in both. |
| B2: Inconsistent historical distribution lengths | (Partially addressed by common 1970 reference) | **Fix partially applied.** Common reference period (1970-present) addresses the distribution length concern, but the expanding window that includes the current value (impl A1) creates a related problem for trending series. | Spec B2: RESOLVED. Impl overlap with A1: OPEN. |
| C1: Massive metric overlap across 6 models | B1: "Zero overlap" claim misleading at construct level | **Partially addressed.** The 3-model selection reduces overlap from the 6-model version. But construct-level overlap remains (labor share / employment ratio / unemployment). The implementation review correctly notes the independence claim should be dropped until empirically verified. | OPEN — needs inter-model correlation analysis in Phase 4. |

---

## Summary Statistics

| Category | Total | Resolved | Open | Deferred |
|----------|-------|----------|------|----------|
| Spec-level (A1-D3) | 15 | 4 | 6 | 5 |
| Implementation-level (A1-C4) | 12 | 0 | 12 | 0 |
| **Combined Total** | **27** | **4** | **18** | **5** |

**Note:** "Resolved" means the fix is applied and correct with no new issues. "Open" means the issue needs attention in Phase 4 (model building) — either the fix wasn't applied, was applied with new issues, or was only partially applied. "Deferred" means the issue affects models not selected for the 3-model implementation (RVI, PITF, CSD).

### Priority Open Items for Phase 4

1. **Impl A1: Min-max normalization on trending series** — CRITICAL. SFD permanently 1.0, EMP near 1.0. Switch to `percentile_rank_series` or z-scores.
2. **Spec A2 / Impl A2: PLI undocumented formula + velocity bug** — Two separate issues. Document or remove the sqrt+`*10` transformation; fix velocity to compute actual rate of change.
3. **Impl A3: FSP config/code weight divergence** — Remove ghost config entries or make model read from config.
4. **Spec D2: No sensitivity analysis protocol** — Define systematic parameter variation framework.
5. **Spec D3: Uncertainty quantification incomplete** — Broaden bootstrap beyond reference window; document as parameter sensitivity.
6. **Impl B1: Construct-level overlap claim** — Drop "zero overlap" marketing; let correlation analysis speak.
7. **Impl A4: WID API untested** — Test live or switch to CSV-only interface.
8. **Spec D1 / Impl B3: Backtesting episodes not tiered** — Assign expected severity levels to historical episodes.
