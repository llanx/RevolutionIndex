# Pitfalls Research

**Domain:** Political instability prediction / revolution probability dashboard
**Researched:** 2026-03-01
**Confidence:** HIGH (grounded in project's own critical review and gap analysis documents)

## Critical Pitfalls

### P1: Index vs Probability Confusion (CRITICAL)

**What:** The 0-100 scale invites users to interpret the composite score as a calibrated probability ("47% chance of revolution"). It is not. It's a weighted composite of normalized indicators — an index, not a probability. The prior work's logistic regression framing with fabricated coefficients compounds this risk.

**Warning signs:**
- Documentation or UI labels use the word "probability" for the composite score
- Users treat small score changes (e.g., 45 → 47) as meaningful when they're within noise range
- Score appears without confidence intervals

**Prevention strategy:**
- Label as "Political Stress Index" or "Structural Pressure Index," not "Revolution Probability"
- Always display confidence intervals alongside point estimates
- Use integer scores (no decimals — false precision)
- Include a persistent "What this score means" tooltip

**Phase mapping:** Phase 1 (framing/naming) and Dashboard phase (UI labels)

---

### P2: Overfitting to N=6 Historical Episodes (CRITICAL)

**What:** With 50+ tunable parameters and only 6 US-specific historical episodes for backtesting (1968, 1970, 1992, 2001, 2008, 2020), any parameter fit is a tautology. The model can perfectly "predict" 6 events with enough knobs.

**Warning signs:**
- Perfect backtesting scores (100% sensitivity, 100% specificity)
- Parameters tuned to optimize backtest results
- No out-of-sample validation

**Prevention strategy:**
- Freeze all parameters BEFORE running backtests (document parameter choices with theoretical justification, not empirical optimization)
- Use sensitivity analysis as the primary validation tool, not point accuracy
- Cross-validate against non-US countries if possible (but see P5)
- Report sensitivity to parameter perturbation honestly

**Phase mapping:** Validation phase — this is the critical quality gate

---

### P3: Spurious Upward Trends (CRITICAL)

**What:** Most input variables trend in the same direction over 50+ years: inequality up, institutional trust down, debt-to-GDP up, life expectancy flattening. A simple composite will mechanically trend upward regardless of actual instability dynamics. This makes the index look like it's "predicting" growing crisis when it's just reflecting secular trends.

**Warning signs:**
- Composite score rises monotonically over the historical period
- Score correlates heavily with time itself
- No quiet periods (e.g., 1990s) show low scores

**Prevention strategy:**
- Compute detrended variant alongside raw score
- Run placebo tests: does the model produce high scores during genuinely stable periods?
- Use expanding-window normalization (percentile rank against all prior history) rather than fixed reference
- The backtesting quiet-period evaluation is essential — the model MUST produce low scores during the 1990s

**Phase mapping:** Model building phase and validation phase

---

### P4: Dashboard Before Model Validation (CRITICAL)

**What:** Building a polished dashboard before confirming the models produce meaningful signal. If models fail backtesting, all dashboard work is wasted.

**Warning signs:**
- Dashboard wireframes or code exist before backtesting results are reviewed
- Model bugs discovered after dashboard is partially built
- "Just put something on screen" mentality overrides validation discipline

**Prevention strategy:**
- Set an explicit validation gate: models must pass backtesting (detect ≥4/6 crises, score low during ≥1/2 quiet periods) before any dashboard code is written
- v1.0 output should be a Jupyter notebook or static HTML report, not a live dashboard
- Dashboard is the LAST phase, not a parallel effort

**Phase mapping:** This is a phase ORDERING constraint, not a feature in any single phase

---

### P5: Wealthy Democracy Gap (CRITICAL)

**What:** Cross-national instability models (PITF, CoupCast) were developed for developing countries and authoritarian regimes. They either underpredict (US always looks stable by developing-world standards) or overpredict (US inequality exceeds many developing-world thresholds). The US is a unique case — wealthy, democratic, armed population, federalized — and cross-national calibration may be misleading.

**Warning signs:**
- Thresholds borrowed from cross-national literature without US-specific calibration
- Score consistently near 0 or consistently near 100 with no variation
- Model cannot distinguish between 1968 (riots) and 1995 (stability)

**Prevention strategy:**
- Define the target variable explicitly: "structural pressure relative to US historical baseline," NOT "revolution probability compared to global norms"
- Use US-only historical distribution for normalization (expanding window from 1970)
- Acknowledge this limitation prominently in methodology docs

**Phase mapping:** Phase 1 (target variable definition) — this must be resolved before any modeling begins

---

### P6: Data Source Fragility (HIGH)

**What:** FRED series get discontinued or redefined (e.g., STLFSI replaced by STLFSI4). WID.world has no SLA and may change API format. Annual data lags 6-18 months. Building a pipeline that assumes data sources are permanent is a recipe for silent failure.

**Warning signs:**
- Pipeline fails silently when a series returns empty
- No monitoring for series discontinuation or definition changes
- Annual series treated as "current" when they're 18 months stale

**Prevention strategy:**
- Build a data dependency matrix: for each model, which series are required vs. optional?
- Implement graceful degradation: if a series is unavailable, the model can still compute with reduced confidence
- Surface freshness metadata prominently (already designed in pipeline)
- Have fallback series identified for critical inputs

**Phase mapping:** Data pipeline phase

---

### P7: Uncalibrated Model Parameters (HIGH)

**What:** The 3 models have parameters (weights, thresholds, normalization windows) that were set by theoretical reasoning, not empirical estimation. Critical review D2 identified this as a major issue — the parameters look precise but are actually researcher degrees of freedom.

**Warning signs:**
- Parameters specified to 2+ decimal places without empirical justification
- Sensitivity analysis shows score swings wildly with small parameter changes
- Different "reasonable" parameter choices produce contradictory conclusions

**Prevention strategy:**
- Document the theoretical justification for every parameter
- Run sensitivity analysis across plausible parameter ranges
- Present sensitivity ranges (not just point estimates) as the primary output
- Consider the score a "central estimate within a band," not a precise measurement

**Phase mapping:** Model building and validation phases

---

### P8: Ensemble Interpretation Failure (MODERATE)

**What:** When three models are averaged, the composite score can mask important information. If Financial Stress says 80 and the other two say 20, the average of 40 obscures that financial markets are screaming. Model divergence is a signal, not noise to be averaged away.

**Warning signs:**
- Large spread between model scores (>20 points) without any alert
- Users only see the composite, never individual model scores
- A crisis in one domain (financial) gets diluted by stability in others

**Prevention strategy:**
- Always show per-model scores alongside the composite
- Implement divergence alerting (already designed: alert when spread >20 points)
- Consider reporting "highest model score" alongside average as a "worst-case" indicator
- The factor breakdown must go model-by-model, not just top-level components

**Phase mapping:** Ensemble/scoring phase and dashboard phase

---

### P9: Mixed-Frequency False Precision (MODERATE)

**What:** When daily VIX data is combined with annual life expectancy data (carried forward 11 months via LOCF), the composite appears to have daily resolution but most of its inputs are stale. A score change driven entirely by VIX movement is presented alongside unchanged annual data as if both are "current."

**Warning signs:**
- Score changes daily but only 2-3 of 18 series actually updated
- Users interpret weekly score changes as "new information" when it's just financial market noise
- No indication of which components are based on fresh vs. stale data

**Prevention strategy:**
- Separate indicators into "fast" (daily/weekly financial) and "slow" (monthly/quarterly/annual structural)
- Display freshness per-component in the dashboard
- Consider weighting more recent data higher, or at least flagging when a score change is driven by a single fast-moving series
- Weekly cadence already helps — don't go faster

**Phase mapping:** Data pipeline phase (freshness tracking) and dashboard phase (display)

---

### P10: Irresponsible Score Communication (MODERATE)

**What:** Even as a personal research tool, presenting a "revolution score" without context invites misinterpretation if anyone else ever sees it. Screenshots get shared. Dashboards get bookmarked.

**Warning signs:**
- Score displayed without methodology context
- No disclaimers visible on the main page
- Score presented as prediction rather than indicator

**Prevention strategy:**
- Include a persistent "What this is / What this isn't" section on every page
- Frame as "Political Stress Index" not "Revolution Probability"
- Include confidence intervals on every score display
- v1 as personal research tool reduces this risk, but plan for responsible framing before going public

**Phase mapping:** Dashboard phase and future public-facing phase

## Integration Gotchas

| Gotcha | Context | Mitigation |
|--------|---------|------------|
| FRED rate limits | 120 requests/minute, but large batch fetches can hit limits | Already handled in existing fred_client.py with rate limiting. Verify rate limiter works for full 17-series historical backfill. |
| FRED series redefinition | STLFSI → STLFSI4 already happened once | Maintain a series alias map in config. Test for empty/discontinued series in pipeline. |
| WID.world API instability | No guaranteed uptime or API stability | Implement manual CSV fallback. Cache aggressively. Don't depend on WID for weekly pipeline health. |
| pandas 3.0 breaking changes | If upgrading from 2.x, deprecation warnings become errors | Pin pandas version. Test before upgrading. The prior code targets 2.x. |
| Plotly 6.x breaking changes | Major version bump from 5.x | Test gauge chart (go.Indicator) works with Plotly 6 + Streamlit before committing to stack. |
| DuckDB concurrent access | DuckDB supports concurrent reads but only one writer | Pipeline must complete writes before dashboard reads. Not a real problem with weekly batch + on-demand dashboard reads. |
| Bootstrap uncertainty performance | 500 samples × 3 models × full historical range = slow | Limit to latest-date-only for weekly runs. Full historical uncertainty only during backfill/validation. |

## Technical Debt Patterns to Avoid

| Pattern | Risk | Prevention |
|---------|------|------------|
| Hardcoded series IDs in model code | Breaks when adding/removing data sources | All series IDs in config.py, models read from config |
| Model weights diverging from config | Already a documented bug (ETI weights in critical-review-implementation.md) | Single source of truth: weights ONLY in config, never in model code |
| Raw data files in git | Repo bloat, merge conflicts on binary files | .gitignore all data/ directories. Document how to regenerate from APIs. |
| Notebook-as-pipeline | Jupyter notebooks used for production data processing | Notebooks for exploration only. Pipeline is Python scripts/modules. |
| Implicit column name dependencies | Model code assumes specific DataFrame column names without validation | Use an explicit data contract (Pydantic model or typed dict) between pipeline and models |

---

## Sources

- **Project internal:** `critical-review-model-specs.md`, `critical-review-implementation.md`, `gap-analysis-literature-review.md` — these directly document known issues with the prior approach (HIGH confidence)
- **Existing codebase:** `revolution-index/` — bugs and design decisions inspected directly (HIGH confidence)
- **Academic literature:** Turchin SDT, Goldstone PITF, Kuran preference falsification, Davies J-curve — referenced in project's literature review (HIGH confidence for theoretical grounding)
- **Data engineering patterns:** Training data knowledge of common pitfalls in ETL pipelines, composite index construction, and dashboard systems (MEDIUM confidence)

---
*Pitfalls research for: Revolution Probability Tracker*
*Researched: 2026-03-01*
