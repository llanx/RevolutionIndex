---
phase: 05-validation
profiled: 2026-03-04T18:00:00Z
status: issues_found
overall_score: 6.8/10
files_analyzed: 11
blockers: 3
warnings: 7
tools_used:
  opengrep: false
  lizard: false
  jscpd: false
previous_score: 7.5/10
score_delta: -0.7
blockers_resolved: 0
new_issues: 3
quality_gaps:
  - truth: "Functions must not exceed 120 lines (2x the 60-line threshold)"
    status: failed
    reason: "write_validation_report() in validate.py is 498 lines; main() in validate.py is 174 lines; main() in run.py remains 201 lines (unchanged from phase 04)"
    source: quality
    artifacts:
      - path: "models/validate.py"
        issue: "Lines 1201-1699: write_validation_report() = 498 lines (threshold: 120)"
      - path: "models/validate.py"
        issue: "Lines 1726-1899: main() = 174 lines (threshold: 120)"
      - path: "models/run.py"
        issue: "Lines 33-233: main() = 201 lines (threshold: 120)"
    missing:
      - "Split write_validation_report() into section-writer helpers: _write_episode_section(), _write_sensitivity_section(), _write_spurious_section(), _write_verdict_section(), _write_limitations_section()"
      - "Split validate.py main() into _load_history_mode(), _run_full_mode(), _run_all_diagnostics(), _collect_results() helpers"
      - "Split run.py main() per phase-04 QUALITY.md guidance (unchanged since last profile)"
  - truth: "Functions must not exceed 120 lines (2x the 60-line threshold)"
    status: failed
    reason: "check_spurious_trends() is 156 lines; compute_overall_verdict() is 127 lines; run_weight_sensitivity() is 93 lines"
    source: quality
    artifacts:
      - path: "models/validate.py"
        issue: "Lines 694-849: check_spurious_trends() = 156 lines (threshold: 120)"
      - path: "models/validate.py"
        issue: "Lines 409-535: compute_overall_verdict() = 127 lines (threshold: 120)"
    missing:
      - "Split check_spurious_trends() into _check_monotonic_trend(), _check_boundary_jumps(), _check_saturation(), _build_decade_summary() — each returns its sub-result"
      - "Split compute_overall_verdict() by extracting _assess_zone_accuracy() and _assess_calibration_residuals() returning sub-criterion dicts"
  - truth: "Functions must not exceed 120 lines (2x the 60-line threshold)"
    status: failed
    reason: "compute_ensemble() in ensemble.py is 121 lines; _build_in_sample_episodes() in validate.py is 87 lines but uses a 4-level nested conditional that could be a lookup table"
    source: quality
    artifacts:
      - path: "models/ensemble.py"
        issue: "Lines 53-172: compute_ensemble() = 121 lines (threshold: 120, borderline)"
      - path: "models/validate.py"
        issue: "Lines 58-144: _build_in_sample_episodes() has zone-range derivation pattern with if/elif chain repeated verbatim"
    missing:
      - "compute_ensemble() extract _compute_current_domain_scores() and _compute_factor_directions() helpers per phase-04 QUALITY.md warning (unchanged)"
      - "_build_in_sample_episodes() replace 4-branch if/elif zone range logic with ZONE_RANGES dict lookup"
---

# Phase 05: Validation Quality Report

**Phase Goal:** Determine whether the model(s) produce meaningful signal by testing against historical ground truth, answering "should we trust this score?"
**Profiled:** 2026-03-04T18:00:00Z
**Status:** issues_found
**Overall Score:** 6.8/10

## File Scores

| File | Complexity | Performance | Style | Idiom | Overall | Issues |
|------|-----------|-------------|-------|-------|---------|--------|
| `models/validate.py` | 4/10 | 7/10 | 6/10 | 8/10 | 5.9/10 | 3B 3W |
| `models/VALIDATION.md` | N/A | N/A | N/A | N/A | N/A | (doc) |
| `models/config.py` | 9/10 | 9/10 | 9/10 | 9/10 | 9.0/10 | 0B 0W |
| `models/ensemble.py` | 6/10 | 7/10 | 7/10 | 8/10 | 6.9/10 | 1B 1W |
| `models/calibrate.py` | 7/10 | 7/10 | 8/10 | 9/10 | 7.6/10 | 0B 1W |
| `models/model_psi.py` | 7/10 | 7/10 | 7/10 | 8/10 | 7.2/10 | 0B 1W |
| `models/model_pli.py` | 8/10 | 8/10 | 7/10 | 8/10 | 7.7/10 | 0B 0W |
| `models/model_fsp.py` | 8/10 | 7/10 | 8/10 | 8/10 | 7.8/10 | 0B 0W |
| `models/model_georgescu.py` | 8/10 | 8/10 | 8/10 | 8/10 | 8.0/10 | 0B 0W |
| `models/model_vdem.py` | 8/10 | 7/10 | 8/10 | 8/10 | 7.8/10 | 0B 1W |
| `models/output.py` | 8/10 | 8/10 | 8/10 | 9/10 | 8.3/10 | 0B 0W |
| `models/pipeline.py` | 5/10 | 6/10 | 7/10 | 8/10 | 6.2/10 | 1B 1W |
| `models/run.py` | 4/10 | 8/10 | 7/10 | 8/10 | 6.2/10 | 1B 0W |

### Score Trend

**Previous Score:** 7.5/10 -> **Current Score:** 6.8/10 (-0.7)
**Blockers Resolved:** 0 | **New Issues:** 3

Phase 05 added `models/validate.py` (1899 lines) which introduces 3 new blocker-level function length violations. The phase-04 blockers in `pipeline.py` (`fetch_all` at 144 lines) and `run.py` (`main` at 201 lines) remain unresolved. The 4 model review fixes applied in plan 05-03 are correctness improvements, not quality improvements, so they do not affect the score. The `calibrate.py` refactoring (bootstrap perturbation split into generate/apply) is a genuine quality improvement that reduces `compute_bootstrap_ci` from 87 lines to 110 lines (not an improvement in length, but the logic is now clearly separated).

## Cross-File Architecture

| Issue | Type | Files | Severity |
|-------|------|-------|----------|
| `_variable_lookup()` defined identically in 5 model files (unchanged from phase 04) | coupling | `model_psi.py`, `model_pli.py`, `model_fsp.py`, `model_georgescu.py`, `model_vdem.py` | Warning |
| Domain contribution normalization copy-pasted in 5 model files (unchanged from phase 04) | coupling | all 5 model files | Warning |
| `validate.py` imports private calibrate.py functions (`_fit_calibration`, `_get_anchor_raw_score`) | layer-violation | `validate.py`, `calibrate.py` | Warning |
| `run_weight_sensitivity()` monkey-patches `config_module.MODEL_WEIGHTS` at runtime | coupling | `validate.py`, `config.py` | Warning |

## Issues by Severity

### Blockers

#### 1. write_validation_report() is 498 lines — far exceeds 2x threshold

**File:** `models/validate.py` lines 1201-1699
**Problem:** `write_validation_report()` is 498 lines (threshold: 60, blocker threshold: 120 — this is 4x the blocker threshold). The function contains 6 distinct report sections, each with its own table-building loop and formatting logic. The inner `add()` closure is defined inside the function, which makes it impossible to test any section independently. Every call rebuilds the entire document in a single function scope. Adding a new validation section requires editing a 498-line monolith.

**Current:**
```python
def write_validation_report(validation_results: dict) -> None:
    lines = []

    def add(text=""):
        lines.append(text)

    # --- Header ---
    add("# Validation Report: Revolution Index")
    # ... 40 lines of header and summary ...

    # --- Section 1: Episode Backtesting ---
    add("## 1. Episode Backtesting")
    # ... 55 lines of episode table generation ...

    # --- Section 2: LOOCV ---
    add("## 2. Leave-One-Out Cross-Validation (LOOCV)")
    # ... 25 lines ...

    # --- Section 3: Weight Sensitivity ---
    # ... 38 lines ...

    # --- Section 4: Inter-Model Correlation ---
    # ... 22 lines ...

    # --- Section 5: Spurious Trend Detection ---
    # ... 65 lines ...

    # --- Section 6: Bootstrap CI Width ---
    # ... 26 lines ...

    # --- Pass/Fail Criteria Table ---
    # ... 65 lines ...

    # --- Overall Verdict ---
    # ... 40 lines ...

    # --- Limitations + Methodology ---
    # ... 45 lines ...

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
```

**Suggested:**
```python
def _write_episode_section(lines: list[str], episodes: list[dict], verdict_data: dict) -> None:
    """Write Section 1: Episode Backtesting table."""
    in_sample = [e for e in episodes if e.get("is_in_sample")]
    out_of_sample = [e for e in episodes if not e.get("is_in_sample")]
    lines.append("## 1. Episode Backtesting")
    lines.append("")
    lines.append("### In-Sample Anchors (Calibration Verification)")
    lines.append("")
    lines.append("| Episode | Expected Zone | Expected Score | Actual Score | Actual Zone | Result |")
    lines.append("|---------|---------------|----------------|--------------|-------------|--------|")
    for e in in_sample:
        lines.append(_format_episode_row(e))
    # ... ~20 lines per section


def _write_sensitivity_section(lines: list[str], sensitivity: list[dict]) -> None:
    """Write Section 3: Weight Sensitivity."""
    lines.append("## 3. Weight Sensitivity Analysis")
    # ... 25 lines


def _write_verdict_section(lines: list[str], verdict_data: dict, mode: str,
                           loocv: list, sensitivity: list, trend_data: dict) -> None:
    """Write Pass/Fail Criteria table and Overall Verdict."""
    # ... 60 lines


def write_validation_report(validation_results: dict) -> None:
    """Write models/VALIDATION.md with complete validation results."""
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    mode = validation_results.get("mode", "history-only")
    verdict_data = validation_results.get("verdict", {})
    episodes = validation_results.get("episodes", [])
    loocv = validation_results.get("loocv", None)
    sensitivity = validation_results.get("sensitivity_results", [])
    trend_data = validation_results.get("trend_results", {})

    lines: list[str] = []
    _write_header(lines, timestamp, mode, verdict_data, episodes)
    _write_episode_section(lines, episodes, verdict_data)
    _write_loocv_section(lines, loocv)
    _write_sensitivity_section(lines, sensitivity)
    _write_correlation_section(lines, validation_results.get("correlation_results", []))
    _write_spurious_section(lines, trend_data)
    _write_ci_section(lines, validation_results.get("ci_width", {}))
    _write_verdict_section(lines, verdict_data, mode, loocv, sensitivity, trend_data)
    _write_limitations(lines, episodes, trend_data)
    _write_methodology(lines)

    report_path = _SCRIPT_DIR / "VALIDATION.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
```

**Improvement:** 498-line monolith -> 10 focused helpers of 20-50 lines each. Each section is independently testable. Adding a new report section requires adding one helper, not editing a 500-line function.

---

#### 2. validate.py main() is 174 lines — exceeds 2x threshold

**File:** `models/validate.py` lines 1726-1899
**Problem:** `main()` is 174 lines (threshold: 60, blocker threshold: 120). It handles argument parsing, history loading, full pipeline execution (with fallback logic), running 6 diagnostic functions, printing results, computing the verdict, and writing the report. The fallback-to-history-only logic (lines 1769-1812) is itself 44 lines of nested try/except that belongs in a dedicated `_try_full_pipeline()` function.

**Current:**
```python
def main():
    parser = argparse.ArgumentParser(...)
    # argparse setup (8 lines)
    args = parser.parse_args()

    # print banner (5 lines)

    calibrated_history = load_history_json()
    # print loading status (5 lines)

    raw_scores = None
    unified_df = None
    # ... 6 more variable initializations

    if args.full:
        api_key = os.environ.get("FRED_API_KEY", "")
        if not api_key and not args.cached_only:
            # print warning, fall back (4 lines)
        else:
            print("Running full pipeline...")
            try:
                from models.pipeline import fetch_all
                # ... 20 more lines of pipeline setup and fallback
            except Exception as e:
                print(f"WARNING: Pipeline failed: {e}")
                args.full = False

    mode = "full" if args.full else "history-only"
    # ... print mode

    episode_results = run_episode_backtest(...)
    # ... 6 more diagnostic calls, each 4 lines

    verdict = compute_overall_verdict(...)
    # ... 6 more result-building calls

    write_validation_report(all_results)
    # ... print report path
```

**Suggested:**
```python
def _parse_validate_args():
    parser = argparse.ArgumentParser(description="Revolution Index Validation Script")
    parser.add_argument("--full", action="store_true")
    parser.add_argument("--cached-only", action="store_true")
    return parser.parse_args()


def _try_full_pipeline(args) -> tuple:
    """Attempt to run the full pipeline. Returns (unified_df, raw_df, raw_scores, cal_coeffs, anchor_residuals, calibrated_history) or None on failure."""
    import os
    api_key = os.environ.get("FRED_API_KEY", "")
    if not api_key and not args.cached_only:
        print("WARNING: FRED_API_KEY not set. Falling back to history-only mode.")
        return None
    try:
        from models.pipeline import fetch_all
        from models.ensemble import compute_ensemble
        from models.calibrate import calibrate, get_calibration_coefficients, _fit_calibration

        unified_df, raw_df = fetch_all(api_key=api_key, start_year=1947)
        if unified_df.empty:
            print("WARNING: Pipeline produced no data. Falling back to history-only.")
            return None

        ensemble_result = compute_ensemble(unified_df, raw_df=raw_df)
        raw_scores = pd.Series({row["date"]: row["score"] for row in ensemble_result["history"]})
        if not isinstance(raw_scores.index, pd.DatetimeIndex):
            raw_scores.index = pd.to_datetime(raw_scores.index)
        cal_coeffs = get_calibration_coefficients(raw_scores)
        _a, _b, anchor_residuals = _fit_calibration(raw_scores)
        calibrated_history = calibrate(raw_scores)
        return unified_df, raw_df, raw_scores, cal_coeffs, anchor_residuals, calibrated_history
    except Exception as e:
        print(f"WARNING: Pipeline failed: {e}. Falling back to history-only.")
        return None


def _run_all_diagnostics(calibrated_history, args, full_results: dict) -> dict:
    """Run all 6 diagnostic functions, collect results dict."""
    # Episode backtest, LOOCV (if full), CI width, weight sensitivity,
    # inter-model correlation, spurious trends, verdict
    # ~40 lines calling each function and storing results
    ...


def main():
    args = _parse_validate_args()
    _print_separator("=")
    print("REVOLUTION INDEX MODEL VALIDATION")
    _print_separator("=")

    calibrated_history = load_history_json()
    print(f"  Loaded {len(calibrated_history)} entries ...")

    pipeline_result = _try_full_pipeline(args) if args.full else None
    unified_df = raw_df = raw_scores = cal_coeffs = anchor_residuals = None
    if pipeline_result:
        unified_df, raw_df, raw_scores, cal_coeffs, anchor_residuals, calibrated_history = pipeline_result

    mode = "full" if (args.full and unified_df is not None) else "history-only"
    all_results = _run_all_diagnostics(calibrated_history, args, {
        "unified_df": unified_df, "raw_df": raw_df, "raw_scores": raw_scores,
        "cal_coeffs": cal_coeffs or (1.0, 0.0), "anchor_residuals": anchor_residuals,
    })
    all_results["mode"] = mode
    write_validation_report(all_results)
    print(f"Validation report written to models/VALIDATION.md")
```

**Improvement:** 174 lines -> 4 focused functions (~15, ~40, ~40, ~25 lines). The pipeline fallback logic is isolated and independently testable. `main()` drops to ~25 lines.

---

#### 3. run.py main() remains at 201 lines — unchanged from phase 04

**File:** `models/run.py` lines 33-233
**Problem:** `main()` is 201 lines (threshold: 60, blocker threshold: 120). This is the same blocker identified in phase-04 QUALITY.md and was not addressed in phase 05. The function handles 8 distinct pipeline phases plus progress reporting, confidence assessment, and JSON output writing. The `from models.config import MODEL_WEIGHTS` import at line 172 is still inside the for loop body, executing on every iteration.

See phase-04 QUALITY.md for the full suggested rewrite. Summary of needed extractions:
- `_parse_args()`: 8 lines
- `_run_pipeline(api_key)`: ~35 lines (phases 1-5, returns results tuple)
- `_print_summary(ensemble_result, score, zone, bootstrap_ci)`: ~30 lines
- `_write_outputs(...)`: ~25 lines
- `main()` drops to ~25 lines

**Improvement:** 201 lines -> 4 focused functions. `MODEL_WEIGHTS` import moves out of iteration loop.

---

### Warnings

#### 1. check_spurious_trends() is 156 lines — exceeds threshold

**File:** `models/validate.py` lines 694-849
**Problem:** 156 lines (threshold: 60). Four distinct sub-checks (monotonic trend, boundary jumps, saturation, decade summary) plus concern-level aggregation are all in one function. Each sub-check has its own state variables and iteration logic. The boundary-jump detection loop (lines 732-755) uses two separate filter passes over `calibrated_history` that could be combined.

**Suggestion:** Extract 4 helpers:
```python
def _check_monotonic_trend(calibrated_history: pd.Series) -> tuple[bool, dict]:
    """Returns (monotonic_flag, decade_means_dict)."""
    ...  # ~25 lines

def _check_boundary_jumps(calibrated_history: pd.Series) -> list[dict]:
    """Returns list of boundary jump dicts."""
    ...  # ~25 lines

def _check_saturation(calibrated_history: pd.Series) -> list[dict]:
    """Returns list of saturation period dicts."""
    ...  # ~25 lines

def _build_decade_summary(calibrated_history: pd.Series) -> dict:
    """Returns decade -> {mean, min, max, range, count} dict."""
    ...  # ~15 lines

def check_spurious_trends(calibrated_history: pd.Series) -> dict:
    """Aggregate all checks into one result dict."""
    monotonic_flag, decade_means = _check_monotonic_trend(calibrated_history)
    boundary_jumps = _check_boundary_jumps(calibrated_history)
    saturation_periods = _check_saturation(calibrated_history)
    decade_summary = _build_decade_summary(calibrated_history)
    # ... concern level aggregation (~10 lines)
    return {...}
```

**Improvement:** 156 lines -> 5 functions of 10-25 lines each. Each sub-check is independently testable.

---

#### 2. compute_overall_verdict() is 127 lines

**File:** `models/validate.py` lines 409-535
**Problem:** 127 lines (just above the 120-line blocker threshold). Three criterion assessments are computed sequentially but share no data, making them natural extraction candidates. The residual check (lines 468-498) handles two different input paths (anchor_residuals vs LOOCV fallback) with a 30-line if/elif block.

**Suggestion:** Extract `_assess_zone_accuracy(episode_results)` returning `(strict_pct, lenient_pct, strict_n, lenient_n, total, zone_pass)` and `_assess_calibration_residuals(anchor_residuals, loocv_results)` returning `(residual_max, residual_warn, residual_fail, residual_details)`. `compute_overall_verdict()` drops to ~30 lines.

---

#### 3. validate.py imports private functions from calibrate.py

**File:** `models/validate.py` lines 39-47
**Problem:** The validation script imports `_fit_calibration` and `_get_anchor_raw_score` — private functions denoted by underscore prefix. These are internals of the calibration module, not public API. If calibrate.py refactors its internals, validate.py silently breaks. LOOCV conceptually belongs in the validation layer but depends on calibration internals to refit with held-out anchors.

**Current:**
```python
from models.calibrate import (
    _fit_calibration,       # private
    _get_anchor_raw_score,  # private
    DEFAULT_ANCHORS,
    calibrate,
    get_calibration_coefficients,
    compute_bootstrap_ci,
    score_to_zone,
)
```

**Suggestion:** Add a public `refit_calibration(raw_scores, anchors)` function to `calibrate.py` that wraps `_fit_calibration` for external callers. Similarly, rename `_get_anchor_raw_score` to `get_anchor_score` and export it. This makes the public API explicit and keeps validate.py isolated from calibrate.py's internals.

---

#### 4. run_weight_sensitivity() monkey-patches config_module.MODEL_WEIGHTS

**File:** `models/validate.py` lines 583-589
**Problem:** In full mode, the function patches `config_module.MODEL_WEIGHTS` directly on the module object between calls to `_run_models_on_slice`, relying on the finally block for cleanup. This is fragile: if a threading scenario exists or if `_run_models_on_slice` itself internally re-imports the module, the patch may not apply. The global mutation means the patch affects any concurrent code reading `MODEL_WEIGHTS` during the perturbation window.

**Current:**
```python
try:
    config_module.MODEL_WEIGHTS = patched
    perturbed = _run_models_on_slice(model_df, raw_df_slice=raw_model_df)
finally:
    config_module.MODEL_WEIGHTS = original_weights
```

**Suggestion:** Pass the weight dict as an explicit parameter to the scoring path rather than patching global state. Add `model_weights: dict = None` to `_run_models_on_slice()` in ensemble.py, defaulting to `MODEL_WEIGHTS` if None. Then sensitivity analysis passes the perturbed dict directly without touching global state.

---

#### 5. _check_ci_width() silently uses None-guarded expressions without short-circuit

**File:** `models/validate.py` lines 362-405
**Problem:** `result["point_estimate_gap"]` is conditionally computed at line 376, but then referenced at line 396 via `result["point_estimate_gap"]` which could be `None`. The guard `if result["point_estimate_gap"] is not None` is correct but the pattern of storing intermediate Nones in a result dict and then checking them repeatedly is error-prone. It also means the dict always has all keys regardless of whether data is available, making callers check None at every field access.

**Suggestion:** Use a two-phase result construction: compute all values first, then build the result dict only with keys that have values. Or use `Optional` typed dataclass for `CIWidthResult` so the None checks are explicit in the type signature.

---

#### 6. _build_in_sample_episodes() uses 4-branch if/elif for zone range derivation

**File:** `models/validate.py` lines 69-76
**Problem:** The zone-to-range mapping is a pure data lookup dressed as conditional logic. Any future addition of a new zone requires editing this function. The same ZONE_BOUNDARIES constant already exists at module level.

**Current:**
```python
if expected_zone == "Stable":
    expected_range = (0, 25)
elif expected_zone == "Elevated Tension":
    expected_range = (26, 50)
elif expected_zone == "Crisis Territory":
    expected_range = (51, 75)
else:
    expected_range = (76, 100)
```

**Suggestion:**
```python
# Module-level constant (co-locate with ZONE_BOUNDARIES)
ZONE_RANGES: dict[str, tuple[int, int]] = {
    "Stable": (0, 25),
    "Elevated Tension": (26, 50),
    "Crisis Territory": (51, 75),
    "Revolution Territory": (76, 100),
}

# In _build_in_sample_episodes():
expected_range = ZONE_RANGES.get(expected_zone, (0, 100))
```

**Improvement:** 4-branch if/elif -> 1-line dict lookup. Zone boundaries defined in one canonical place.

---

#### 7. compute_bootstrap_ci() is 110 lines — exceeds threshold

**File:** `models/calibrate.py` lines 195-302
**Problem:** 110 lines (threshold: 60). The function handles domain-to-variable mapping setup, DataFrame preparation, and the bootstrap loop proper. The domain mapping setup (lines 244-265) is 22 lines of its own that belongs in a `_build_var_by_domain(unified_df)` helper, matching the pattern established by `_generate_domain_swaps()` and `_apply_domain_swaps()`.

**Suggestion:** Extract `_build_var_by_domain(unified_df: pd.DataFrame) -> dict[str, list[str]]` covering lines 244-265. `compute_bootstrap_ci()` drops from 110 to ~85 lines. Still above threshold but materially better.

---

### Info

- `models/validate.py:1207` -- `timestamp` and `date_str` are both computed from `datetime.now(timezone.utc)` with different format strings. A single `now = datetime.now(timezone.utc)` would avoid the double system call.
- `models/validate.py:711-715` -- `check_spurious_trends()` builds the `decades` dict by iterating `calibrated_history.items()`, then builds `decade_means` by iterating `decades.items()`. Both passes could be merged into one `groupby` operation: `calibrated_history.groupby(calibrated_history.index.year // 10 * 10).mean()`.
- `models/validate.py:759-809` -- Saturation check tracks `consecutive_at_zero` and `consecutive_at_100` as parallel stateful variables with mirrored logic. This pattern is error-prone: any change to the zero-saturation branch must be replicated in the 100-saturation branch. Could be extracted to a `_find_saturation_runs(series, threshold_val, comparator)` helper called twice.
- `models/pipeline.py:379-522` -- `fetch_all()` is 144 lines (threshold: 60, blocker threshold 120). This was a phase-04 blocker. The function now also stores `raw_aligned` data in addition to `normalized`, which adds ~10 lines but the core structure is otherwise unchanged.
- `models/run.py:172` -- `from models.config import MODEL_WEIGHTS` import is inside the for-loop body at line 172. The module is cached by Python after first import so this is not a performance bug, but it is misleading style — it suggests a per-iteration dependency that does not exist. Move to top of `main()`.
- `models/ensemble.py:86-100` -- The TypeError-catch try/except pattern for models that don't accept `raw_df` is duplicated in `compute_ensemble()` (lines 86-100), `_run_models_on_slice()` (lines 186-195), and `check_inter_model_correlation()` in validate.py (lines 659-668). A small `_call_model(model_fn, model_df, raw_df)` helper would eliminate this triple-copy.

## Dimension Summaries

### Complexity

The dominant complexity issue is `validate.py`, which is 1899 lines and contains two functions at 498 and 174 lines respectively. `write_validation_report()` at 498 lines is the worst offender in the entire codebase, nearly 4x the blocker threshold and 8x the normal threshold. The five diagnostic functions (`check_spurious_trends` at 156 lines, `compute_overall_verdict` at 127 lines, `run_weight_sensitivity` at 93 lines, `check_ci_width` at 63 lines, `check_inter_model_correlation` at 65 lines) are all above or at the 60-line threshold. The phase-04 blockers in `run.py` (201 lines) and `pipeline.py` (144 lines) remain unresolved.

### Performance

No new O(n^2) or N+1 patterns introduced. `check_spurious_trends()` iterates `calibrated_history.items()` three separate times (once for decade grouping, once for boundary jump detection, once for saturation detection) when one pass could serve all three. For a 126-entry history this is negligible, but the pattern is worth noting. The phase-04 warning about row-wise `apply()` in `compute_domain_scores()` and the Python loop in `_build_raw_history()` are unchanged.

### Style

The `write_validation_report()` closure `add()` pattern (an inner function that appends to an outer `lines` list) is a functional approach but produces an untestable 500-line function with no natural seams. The print functions in validate.py (8 functions totaling ~350 lines) are appropriately sized and cleanly separated from logic. The module-level `DATA_BOUNDARY_YEARS` constant is properly placed. The TypeError-catch dual-try pattern for model function dispatch is copy-pasted in three places.

### Idiom

Python idioms are well-used throughout validate.py: `Optional` types, `isinstance` checks, `.dropna()` chaining, `pd.offsets.MonthEnd(0)` for month-end handling, and proper use of `np.random.default_rng()`. The monkey-patching of `config_module.MODEL_WEIGHTS` in `run_weight_sensitivity()` is the only significant idiom violation: Python convention for this pattern is to pass a parameter, not mutate global module state. The `_build_in_sample_episodes()` if/elif chain for zone ranges is a minor idiom issue (dict lookup is more idiomatic than a 4-branch conditional for pure data mapping).

## Rewrite Priority

Priority-ordered list of suggested rewrites (highest impact first):

1. **`models/validate.py:1201-1699`** -- `write_validation_report()` at 498 lines exceeds 4x threshold -> Extract 8 `_write_*_section()` helpers (Blocker)
2. **`models/run.py:33-233`** -- `main()` at 201 lines exceeds 2x threshold -> Extract `_run_pipeline()`, `_print_summary()`, `_write_outputs()` per phase-04 QUALITY.md (Blocker, unchanged)
3. **`models/validate.py:1726-1899`** -- `main()` at 174 lines exceeds 2x threshold -> Extract `_try_full_pipeline()`, `_run_all_diagnostics()` (Blocker)
4. **`models/validate.py:694-849`** -- `check_spurious_trends()` at 156 lines -> Extract 4 sub-check helpers (Warning, Complexity)
5. **`models/validate.py:409-535`** -- `compute_overall_verdict()` at 127 lines -> Extract `_assess_zone_accuracy()`, `_assess_calibration_residuals()` (Warning, Complexity)
6. **`models/validate.py:39-47`** -- Private calibrate.py imports -> Add public wrappers `refit_calibration()` and `get_anchor_score()` (Warning, Style)
7. **`models/validate.py:571-604`** -- `config_module.MODEL_WEIGHTS` monkey-patch -> Pass `model_weights` as explicit parameter to `_run_models_on_slice()` (Warning, Style)
8. **`models/calibrate.py:195-302`** -- `compute_bootstrap_ci()` at 110 lines -> Extract `_build_var_by_domain()` helper (Warning, Complexity)

---
*Profiled: 2026-03-04T18:00:00Z*
*Profiler: Claude (gsd-profiler)*
