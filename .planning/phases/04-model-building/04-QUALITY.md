---
phase: 04-model-building
profiled: 2026-03-04T12:00:00Z
status: issues_found
overall_score: 7.5/10
files_analyzed: 14
blockers: 2
warnings: 9
tools_used:
  opengrep: false
  lizard: false
  jscpd: false
previous_score: 7.5/10
score_delta: +0.0
blockers_resolved: 0
new_issues: 0
quality_gaps:
  - truth: "Functions must not exceed 120 lines (2x the 60-line threshold)"
    status: failed
    reason: "fetch_all() in pipeline.py is 125 lines; main() in run.py is 140 lines"
    source: quality
    artifacts:
      - path: "models/pipeline.py"
        issue: "Lines 356-480: fetch_all() = 125 lines (threshold: 120)"
      - path: "models/run.py"
        issue: "Lines 33-172: main() = 140 lines (threshold: 120)"
    missing:
      - "Split fetch_all() into _fetch_fred_data(), _load_manual_data(), _construct_proxies(), and _align_and_normalize() subfunctions called from a thin orchestrator"
      - "Split main() in run.py by extracting _run_pipeline(), _print_summary(), and _write_outputs() helper functions"
---

# Phase 04: Model Building Quality Report

**Phase Goal:** Produce working model(s) that compute a 0-100 political stress score from the sourced data, with interpretable factor breakdowns and an automated data pipeline
**Profiled:** 2026-03-04T12:00:00Z
**Status:** issues_found
**Overall Score:** 7.5/10

## File Scores

| File | Complexity | Performance | Style | Idiom | Overall | Issues |
|------|-----------|-------------|-------|-------|---------|--------|
| `models/config.py` | 9/10 | 9/10 | 9/10 | 9/10 | 9.0/10 | 0B 0W |
| `models/pipeline.py` | 6/10 | 7/10 | 7/10 | 8/10 | 6.9/10 | 2B 2W |
| `models/normalize.py` | 9/10 | 9/10 | 9/10 | 9/10 | 9.0/10 | 0B 0W |
| `models/models.py` | 10/10 | 10/10 | 10/10 | 10/10 | 10.0/10 | 0B 0W |
| `models/model_psi.py` | 7/10 | 7/10 | 6/10 | 8/10 | 7.0/10 | 0B 1W |
| `models/model_pli.py` | 6/10 | 7/10 | 6/10 | 8/10 | 6.7/10 | 0B 2W |
| `models/model_fsp.py` | 7/10 | 7/10 | 6/10 | 8/10 | 7.0/10 | 0B 1W |
| `models/model_georgescu.py` | 7/10 | 7/10 | 6/10 | 8/10 | 7.0/10 | 0B 1W |
| `models/model_vdem.py` | 6/10 | 7/10 | 6/10 | 8/10 | 6.7/10 | 0B 2W |
| `models/ensemble.py` | 8/10 | 7/10 | 8/10 | 9/10 | 7.9/10 | 0B 1W |
| `models/calibrate.py` | 7/10 | 7/10 | 6/10 | 9/10 | 7.0/10 | 0B 2W |
| `models/output.py` | 8/10 | 8/10 | 8/10 | 9/10 | 8.3/10 | 0B 0W |
| `models/run.py` | 6/10 | 8/10 | 7/10 | 8/10 | 7.2/10 | 1B 1W |
| `src/lib/data.ts` | 9/10 | 9/10 | 9/10 | 9/10 | 9.0/10 | 0B 0W |

### Score Trend

**Previous Score:** 7.5/10 -> **Current Score:** 7.5/10 (+0.0)
**Blockers Resolved:** 0 | **New Issues:** 0

Plan 04 addressed data-quality artifacts in `history.json` and corrected the bootstrap n value in `current.json`. The MIN_DOMAINS_REQUIRED guard added to `_build_raw_history()` is a meaningful correctness fix. No code quality blockers were resolved: `fetch_all()` at 125 lines and `main()` at 140 lines remain above the 2x threshold. Ensemble.py is slightly improved with `_build_raw_history` now at 46 lines (within threshold after adding the domain-count guard).

## Cross-File Architecture

| Issue | Type | Files | Severity |
|-------|------|-------|----------|
| `_variable_lookup()` defined identically in 5 model files | coupling | `model_psi.py`, `model_pli.py`, `model_fsp.py`, `model_georgescu.py`, `model_vdem.py` | Warning |
| Domain contribution normalization pattern copy-pasted into 5 model files | coupling | all model files | Warning |
| `_compute_component()` defined separately in `model_psi.py` and `model_georgescu.py` with identical logic | coupling | `model_psi.py`, `model_georgescu.py` | Warning |

## Issues by Severity

### Blockers

#### 1. fetch_all() exceeds 2x function length threshold

**File:** `models/pipeline.py` lines 356-480
**Problem:** `fetch_all()` is 125 lines (threshold: 60, blocker threshold: 120). The function performs five distinct pipeline phases (FRED fetching, CPI component fetching, manual loading, proxy construction, frequency alignment and normalization) in a single monolithic body. Each phase is already labeled with a comment, making extraction natural. Functions exceeding 2x the threshold are blockers because they are untestable as units, and any error in one phase is entangled with all others.

**Current:**
```python
def fetch_all(api_key: str, start_year: int = 1947) -> pd.DataFrame:
    _ensure_dirs()
    start_date = f"{start_year}-01-01"

    # Phase 1: Fetch all FRED series first (needed for constructed variables)
    raw_data: dict[str, pd.Series] = {}
    fred_vars = [v for v in VARIABLES if v.source_type == SourceType.FRED_API]
    print(f"Fetching {len(fred_vars)} FRED series...")
    for var in fred_vars:
        try:
            series = fetch_fred_series(var.series_id, api_key, start_date)
            raw_data[var.series_id] = series
            ...
        except Exception as e:
            ...
    # Also fetch CPI component series needed for constructed variable #40
    cpi_components = ["CUSR0000SAH1", "CPIFABSL", "CPIENGSL", "CPIMEDSL"]
    for sid in cpi_components:
        ...  # 8 more lines

    # Phase 2: Load manual download data
    manual_vars = [v for v in VARIABLES if v.source_type == SourceType.MANUAL_DOWNLOAD]
    ...  # 12 lines

    # Phase 3: Construct proxy variables
    constructed_vars = [...]
    ...  # 12 lines

    # Phase 4: Align all series to monthly and normalize
    ...  # 22 lines

    # Phase 5: Combine into unified DataFrame
    ...  # 8 lines
```

**Suggested:**
```python
def _fetch_fred_data(api_key: str, start_date: str) -> dict[str, pd.Series]:
    """Fetch all FRED API series plus CPI components needed for constructed vars."""
    raw_data: dict[str, pd.Series] = {}
    fred_vars = [v for v in VARIABLES if v.source_type == SourceType.FRED_API]
    print(f"Fetching {len(fred_vars)} FRED series...")
    for var in fred_vars:
        try:
            series = fetch_fred_series(var.series_id, api_key, start_date)
            raw_data[var.series_id] = series
            print(f"  [{var.catalog_number}] {var.series_id}: {len(series)} observations")
        except Exception as e:
            print(f"  [{var.catalog_number}] {var.series_id}: FAILED - {e}")
    for sid in ["CUSR0000SAH1", "CPIFABSL", "CPIENGSL", "CPIMEDSL"]:
        if sid not in raw_data:
            try:
                raw_data[sid] = fetch_fred_series(sid, api_key, start_date)
            except Exception as e:
                print(f"  [CPI component] {sid}: FAILED - {e}")
    return raw_data


def _load_manual_data(raw_data: dict[str, pd.Series]) -> None:
    """Load manually-downloaded variable data into raw_data in-place."""
    manual_vars = [v for v in VARIABLES if v.source_type == SourceType.MANUAL_DOWNLOAD]
    print(f"\nLoading {len(manual_vars)} manual download variables...")
    for var in manual_vars:
        series = load_manual_source(var)
        if series is not None:
            raw_data[str(var.catalog_number)] = series
            print(f"  [{var.catalog_number}] {var.name}: {len(series)} observations")
        else:
            print(f"  [{var.catalog_number}] {var.name}: NOT FOUND (place data in data/raw/var_{var.catalog_number}/)")


def _construct_proxies(raw_data: dict[str, pd.Series]) -> None:
    """Construct derived proxy variables from component series in-place."""
    constructed_vars = [v for v in VARIABLES if v.source_type == SourceType.CONSTRUCTED]
    print(f"\nConstructing {len(constructed_vars)} proxy variables...")
    for var in constructed_vars:
        series = construct_proxy(var, raw_data)
        if series is not None:
            raw_data[str(var.catalog_number)] = series
        else:
            print(f"  [{var.catalog_number}] {var.name}: MISSING COMPONENTS")


def _align_and_normalize(raw_data: dict[str, pd.Series], window: int) -> dict[str, pd.Series]:
    """Align all series to monthly frequency and normalize to 0-1 stress."""
    print("\nAligning to monthly frequency and normalizing...")
    normalized: dict[str, pd.Series] = {}
    for var in VARIABLES:
        key = var.series_id if var.source_type == SourceType.FRED_API else str(var.catalog_number)
        if key not in raw_data:
            print(f"  [{var.catalog_number}] SKIPPED (no data)")
            continue
        monthly = align_to_monthly(raw_data[key], var.frequency)
        stress = normalize_variable(monthly, direction=var.norm_direction.value, window=window)
        normalized[str(var.catalog_number)] = stress
        print(f"  [{var.catalog_number}] {var.name}: {stress.dropna().shape[0]} normalized observations")
    return normalized


def fetch_all(api_key: str, start_year: int = 1947) -> pd.DataFrame:
    """Main pipeline entry point. Fetches, constructs, aligns, and normalizes all variables."""
    _ensure_dirs()
    start_date = f"{start_year}-01-01"
    window = NORMALIZATION_CONFIG["rolling_window_months"]

    raw_data = _fetch_fred_data(api_key, start_date)
    _load_manual_data(raw_data)
    _construct_proxies(raw_data)
    normalized = _align_and_normalize(raw_data, window)

    if not normalized:
        print("\nWARNING: No variables were successfully processed.")
        return pd.DataFrame()

    unified = pd.DataFrame(normalized).sort_index()
    print(f"\nUnified DataFrame: {unified.shape[0]} months x {unified.shape[1]} variables")
    print(f"Date range: {unified.index.min()} to {unified.index.max()}")
    return unified
```

**Improvement:** 125 lines -> 5 small focused functions (15-25 lines each). Each phase is independently testable and readable in isolation.

---

#### 2. main() in run.py exceeds 2x function length threshold

**File:** `models/run.py` lines 33-172
**Problem:** `main()` is 140 lines (threshold: 60, blocker threshold: 120). It handles argument parsing, data fetching, domain scoring, ensemble running, calibration, bootstrap CI, output writing, and summary printing. These are seven distinct responsibilities. Additionally, `from models.config import MODEL_WEIGHTS` is imported at line 125 inside the function body inside a printing loop, which is an unusual deferred import that runs on every call to `main()` after the loop starts.

**Current:**
```python
def main():
    parser = argparse.ArgumentParser(description="Revolution Index Pipeline")
    # ... argparse setup (8 lines)
    api_key = os.environ.get("FRED_API_KEY", "")
    # ... error handling (10 lines)
    from models.pipeline import fetch_all, compute_domain_scores
    unified_df = fetch_all(...)
    # ... emptiness check (4 lines)
    domain_scores_df = compute_domain_scores(unified_df)
    from models.ensemble import compute_ensemble
    ensemble_result = compute_ensemble(unified_df)
    from models.calibrate import calibrate, compute_bootstrap_ci, score_to_zone
    # ... calibration (8 lines)
    # ... 25-line summary print block including inner import of MODEL_WEIGHTS
    if not args.dry_run:
        # ... 28-line JSON writing block
    # ... freshness summary (4 lines)
```

**Suggested:**
```python
def _parse_args():
    parser = argparse.ArgumentParser(description="Revolution Index Pipeline")
    parser.add_argument("--cached-only", action="store_true", help="Skip API fetching")
    parser.add_argument("--dry-run", action="store_true", help="Compute but don't write JSON")
    return parser.parse_args()


def _run_pipeline(api_key: str):
    """Fetch, score, calibrate. Returns (unified_df, domain_scores_df, ensemble_result, calibrated_history, bootstrap_ci)."""
    from models.pipeline import fetch_all, compute_domain_scores
    from models.ensemble import compute_ensemble
    from models.calibrate import calibrate, compute_bootstrap_ci

    print("Phase 1: Fetching data...")
    unified_df = fetch_all(api_key=api_key, start_year=1947)
    if unified_df.empty:
        print("\nERROR: Pipeline produced no data.")
        sys.exit(1)

    print("\nPhase 2: Computing domain scores...")
    domain_scores_df = compute_domain_scores(unified_df)

    print("\nPhase 3: Running ensemble models...")
    ensemble_result = compute_ensemble(unified_df)

    print("\nPhase 4: Calibrating scores...")
    raw_history = pd.Series({row["date"]: row["score"] for row in ensemble_result["history"]})
    calibrated_history = calibrate(raw_history)

    print("\nPhase 5: Computing bootstrap confidence intervals...")
    bootstrap_ci = compute_bootstrap_ci(unified_df)

    return unified_df, domain_scores_df, ensemble_result, calibrated_history, bootstrap_ci


def _print_summary(ensemble_result: dict, current_score: int, current_zone: str, bootstrap_ci: dict) -> None:
    from models.config import MODEL_WEIGHTS
    print("=" * 70)
    print("Pipeline Results")
    print("=" * 70)
    print(f"  Composite Score: {current_score}")
    print(f"  Zone: {current_zone}")
    print(f"  Bootstrap 90% CI: [{bootstrap_ci['ci_lower']:.1f}, {bootstrap_ci['ci_upper']:.1f}]")
    for domain_id, score in ensemble_result["domain_scores"].items():
        direction = ensemble_result["factor_directions"].get(domain_id, "neutral")
        arrow = {"up": "^", "down": "v", "neutral": "="}[direction]
        print(f"    {domain_id}: {score:.3f} [{arrow}]")
    for model_id, output in ensemble_result["model_outputs"].items():
        weight = MODEL_WEIGHTS.get(model_id, 0.0)
        print(f"    {output.model_name} ({model_id}): {output.score:.1f} (weight={weight})")


def _write_outputs(ensemble_result, domain_scores_df, calibrated_history, bootstrap_ci,
                   current_score, current_zone, timestamp):
    from models.output import write_current_json, write_history_json, write_factors_json
    from models.config import DOMAIN_WEIGHTS as DW
    domain_weights = {d.value: w for d, w in DW.items()}
    write_current_json(current_score, current_zone, ensemble_result["domain_scores"],
                       ensemble_result["factor_directions"], domain_weights, timestamp, bootstrap_ci)
    write_history_json(build_history_entries(calibrated_history))
    write_factors_json(ensemble_result["domain_scores"], build_domain_history(domain_scores_df))
    print("\n  JSON files written to public/data/")


def main():
    args = _parse_args()
    api_key = os.environ.get("FRED_API_KEY", "")
    if not api_key and not args.cached_only:
        print("ERROR: FRED_API_KEY not set. Run: export FRED_API_KEY=your_key_here")
        sys.exit(1)

    print("=" * 70)
    print("Revolution Index Pipeline")
    print("=" * 70)

    unified_df, domain_scores_df, ensemble_result, calibrated_history, bootstrap_ci = _run_pipeline(api_key)
    current_score = max(0, min(100, int(round(float(calibrated_history.iloc[-1])))))
    current_zone = score_to_zone(current_score)
    timestamp = datetime.now(timezone.utc).isoformat()

    _print_summary(ensemble_result, current_score, current_zone, bootstrap_ci)

    if not args.dry_run:
        print("\nPhase 6: Writing JSON output...")
        _write_outputs(ensemble_result, domain_scores_df, calibrated_history, bootstrap_ci,
                       current_score, current_zone, timestamp)
    else:
        print("\n  --dry-run: JSON output not written.")

    from models.pipeline import get_freshness
    freshness = get_freshness()
    print(f"\n  Data freshness: {len(freshness)} sources tracked\nPipeline complete.")
```

**Improvement:** 140 lines -> 4 focused functions (20-30 lines each). `main()` drops to ~25 lines. `MODEL_WEIGHTS` import moved out of inner loop to top of `_print_summary`.

---

### Warnings

#### 1. _variable_lookup() defined identically in 5 model files

**File:** `models/model_psi.py:58-60`, `models/model_pli.py:79-81`, `models/model_fsp.py:76-78`, `models/model_georgescu.py:71-73`, `models/model_vdem.py:111-113`
**Problem:** Each model file defines the same one-liner: `return {v.catalog_number: v for v in VARIABLES}`. Every model call rebuilds this dict from scratch on each invocation. With 41 variables iterated 5 times per ensemble run, this is needless repeated work and a maintenance hazard: any change to the lookup behavior would need to be made in 5 places.

**Suggestion:** Add a module-level constant to `models/config.py` after the `VARIABLES` definition:
```python
# In models/config.py, after VARIABLES definition:
VARIABLE_LOOKUP: dict[int, Variable] = {v.catalog_number: v for v in VARIABLES}
```
Then in each model file: `from models.config import VARIABLE_LOOKUP` and remove the `_variable_lookup()` function entirely.

---

#### 2. Domain contribution normalization pattern copy-pasted into 5 model files

**File:** `models/model_psi.py:179-191`, `models/model_pli.py:281-291`, `models/model_fsp.py:273-283`, `models/model_georgescu.py:193-201`, `models/model_vdem.py:331-341`
**Problem:** Every model ends with the same 12-line block: loop over variable numbers, group by domain, count variables per domain, normalize to proportions.

**Suggestion:** Extract to `models/models.py`:
```python
def compute_domain_contributions(var_nums: list[int], var_lookup: dict) -> dict[str, float]:
    """Compute proportional domain contributions from a list of variable numbers."""
    counts: dict[str, float] = {}
    for vnum in var_nums:
        var_info = var_lookup.get(vnum)
        if var_info:
            did = var_info.domain.value
            counts[did] = counts.get(did, 0.0) + 1.0
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()} if total > 0 else counts
```
All 5 model files replace their 12-line block with one call:
```python
domain_contributions = compute_domain_contributions(all_var_nums, var_lookup)
```

---

#### 3. _compute_component() duplicated between model_psi.py and model_georgescu.py

**File:** `models/model_psi.py:68-113`, `models/model_georgescu.py:76-116`
**Problem:** Both define an identical 45-line `_compute_component()` function: evidence-weighted average of constituent variables from the unified_df. FSP's `_compute_eti()` is also structurally near-identical. A future change to how missing variables are handled would require editing 3 files.

**Suggestion:** Move the canonical implementation to `models/models.py`:
```python
def compute_weighted_component(
    unified_df: pd.DataFrame,
    var_numbers: list[int],
    var_lookup: dict,
) -> tuple[float, list[str]]:
    """Compute evidence-weighted average of normalized variables. Returns (score, names_used)."""
    weighted_sum = total_weight = 0.0
    variables_used = []
    for vnum in var_numbers:
        col = f"var_{vnum}"
        series = unified_df.get(col, pd.Series(dtype=float)).dropna()
        if series.empty:
            continue
        latest = float(series.iloc[-1])
        if np.isnan(latest):
            continue
        var_info = var_lookup.get(vnum)
        if var_info is None:
            continue
        weight = EVIDENCE_WEIGHTS[var_info.evidence_rating]
        weighted_sum += latest * weight
        total_weight += weight
        variables_used.append(var_info.name)
    if total_weight == 0.0:
        return 0.0, variables_used
    return weighted_sum / total_weight, variables_used
```

---

#### 4. _compute_composite_from_latest() and _bootstrap_one_iteration() are near-identical

**File:** `models/calibrate.py:243-283`, `models/calibrate.py:286-333`
**Problem:** Both loop over domains, compute evidence-weighted averages of latest values, then compute the DOMAIN_WEIGHTS-weighted composite. The bootstrap version adds one line: `rng.choice(cols, ...)` resampling. The inner weighted-sum loop (16 lines) and the domain-composite aggregation (10 lines) are copy-pasted verbatim.

**Suggestion:** Parameterize the shared logic:
```python
def _compute_composite_from_columns(
    df: pd.DataFrame,
    var_by_domain: dict[str, list[str]],
    var_evidence: dict[str, float],
    cols_override: dict[str, list[str]] | None = None,
) -> float:
    """Domain-weighted composite from given columns per domain. cols_override replaces var_by_domain."""
    domain_scores = {}
    for domain in Domain:
        domain_id = domain.value
        cols = (cols_override or var_by_domain).get(domain_id, [])
        if not cols:
            continue
        weighted_sum = total_weight = 0.0
        for col in cols:
            series = df[col].dropna()
            if series.empty:
                continue
            latest = float(series.iloc[-1])
            weight = var_evidence.get(col, 1.0)
            weighted_sum += latest * weight
            total_weight += weight
        if total_weight > 0:
            domain_scores[domain_id] = weighted_sum / total_weight
    composite_sum = composite_weight = 0.0
    for domain in Domain:
        domain_id = domain.value
        if domain_id in domain_scores:
            w = DOMAIN_WEIGHTS[domain]
            composite_sum += domain_scores[domain_id] * w
            composite_weight += w
    return (composite_sum / composite_weight) * 100.0 if composite_weight > 0 else 50.0
```
`_bootstrap_one_iteration` then becomes:
```python
def _bootstrap_one_iteration(df, var_by_domain, var_evidence, rng):
    resampled = {d: list(rng.choice(cols, size=len(cols), replace=True))
                 for d, cols in var_by_domain.items()}
    return _compute_composite_from_columns(df, var_by_domain, var_evidence, resampled)
```

---

#### 5. compute_ensemble() and compute_pli() exceed the function length threshold

**File:** `models/ensemble.py:56-149` (94 lines), `models/model_pli.py:199-300` (102 lines)
**Problem:** Both exceed the 60-line `max_function_lines` threshold. `compute_ensemble` mixes model running, domain scoring, direction determination, and history building. `compute_pli` mixes domain loss computation, breadth bonus, velocity bonus, and output construction.

**Suggestion for `compute_ensemble`:** Extract `_compute_factor_directions(domain_scores_df)` covering lines 116-138. 94 lines becomes two functions of ~30 and ~65 lines.

**Suggestion for `compute_pli`:** Extract the bonus computation block (lines 253-277) to `_compute_pli_bonuses(domain_scores, n_domains_in_loss, all_domain_vars, unified_df) -> tuple[float, float]`. 102 lines becomes ~60 and ~25 lines.

---

#### 6. compute_domain_scores() uses row-wise apply() on potentially large DataFrames

**File:** `models/pipeline.py:528-535`
**Problem:** The `weighted_mean` closure is passed to `domain_df.apply(weighted_mean, axis=1)`, which calls a Python function once per row. For a 930-month DataFrame with 13 Economic Stress variables, this is 930 Python-level function calls per domain (5 domains = ~4,650 total). Vectorized pandas operations would be significantly faster.

**Current:**
```python
def weighted_mean(row):
    valid = row.dropna()
    if len(valid) == 0:
        return np.nan
    w = weights.loc[valid.index]
    return (valid * w).sum() / w.sum()

domain_scores[domain.value] = domain_df.apply(weighted_mean, axis=1)
```

**Suggested:**
```python
# Vectorized: multiply each column by its weight, sum rows, divide by weight of present values
weighted_df = domain_df.mul(weights, axis=1)
weight_mask = domain_df.notna().mul(weights, axis=1)
domain_scores[domain.value] = weighted_df.sum(axis=1) / weight_mask.sum(axis=1)
# NaN where all variables are NaN is preserved naturally (0/0 = NaN in pandas)
```

**Improvement:** Row-wise Python closure O(n_months) -> vectorized pandas. Roughly 10-50x faster on 930-row DataFrames. Note: `0/0` produces `NaN` naturally in this vectorized form.

---

#### 7. _build_raw_history() iterates DatetimeIndex with Python loop

**File:** `models/ensemble.py:174-196`
**Problem:** The loop `for date_idx in domain_scores_df.index:` combined with `domain_scores_df.loc[date_idx]` performs O(n) Python-level row access. For a 930-row DataFrame, `loc[]` is called 930 times, each triggering a pandas label lookup. The MIN_DOMAINS_REQUIRED guard added in Plan 04 is correct logic but implemented in the slow Python loop.

**Suggestion:** Use vectorized computation:
```python
def _build_raw_history(unified_df: pd.DataFrame, domain_scores_df: pd.DataFrame) -> list[dict]:
    weight_series = pd.Series({
        domain.value: DOMAIN_WEIGHTS[domain]
        for domain in Domain
        if domain.value in domain_scores_df.columns
    })
    aligned = domain_scores_df[weight_series.index]
    valid_count = aligned.notna().sum(axis=1)  # number of valid domains per row
    mask = aligned.notna()
    effective_weights = mask.mul(weight_series, axis=1)
    composite = aligned.mul(weight_series, axis=1).sum(axis=1) / effective_weights.sum(axis=1)
    composite = (composite * 100.0).where(valid_count >= MIN_DOMAINS_REQUIRED)
    composite = composite.dropna()
    return [
        {"date": idx.strftime("%Y-%m-%d"), "score": round(float(val), 2)}
        for idx, val in composite.items()
    ]
```

**Improvement:** 930 Python-level `loc[]` calls -> vectorized multiply-sum. Eliminates the Python loop entirely. The MIN_DOMAINS_REQUIRED guard is preserved via `.where()`.

---

#### 8. construct_proxy() uses if-chain by catalog number (will not scale)

**File:** `models/pipeline.py:171-264`
**Problem:** `construct_proxy()` is 94 lines of sequential `if cat_num == N:` checks. Adding a new constructed variable requires editing this function. The function also has mixed dispatch: some constructed variables call `load_manual_source()` (acting as manual-download aliases), while others perform actual computation.

**Suggestion:** Register construction functions in module scope:
```python
_PROXY_BUILDERS: dict[int, Callable] = {}

def register_proxy(cat_num: int):
    def decorator(fn):
        _PROXY_BUILDERS[cat_num] = fn
        return fn
    return decorator

@register_proxy(14)
def _build_var14_relative_deprivation(variable, raw_data):
    umcsent = raw_data.get("UMCSENT")
    gdp = raw_data.get("A191RL1Q225SBEA")
    ...

@register_proxy(40)
def _build_var40_cost_of_living(variable, raw_data):
    ...

def construct_proxy(variable, raw_data):
    builder = _PROXY_BUILDERS.get(variable.catalog_number)
    if builder:
        return builder(variable, raw_data)
    return load_manual_source(variable)
```

**Improvement:** 94-line if-chain -> O(1) dict dispatch. Each variable's construction logic is a named, independently testable function.

---

#### 9. calibrate() and compute_bootstrap_ci() exceed function length threshold

**File:** `models/calibrate.py:35-103` (69 lines), `models/calibrate.py:154-240` (87 lines)
**Problem:** Both exceed the 60-line threshold. `calibrate()` could be simplified by extracting anchor computation to a dedicated helper `_fit_linear_calibration(crisis_raw, stable_raw, crisis_target, stable_target) -> tuple[float, float]` returning `(a, b)`. `compute_bootstrap_ci()` mixes bootstrap setup (domain mapping) with iteration logic.

**Suggestion:** For `calibrate()`, extract `_fit_linear_calibration()` returning `(a, b)` (the linear coefficients). For `compute_bootstrap_ci()`, extract `_setup_bootstrap_domain_map(unified_df) -> tuple[dict, dict]` returning `(var_by_domain, var_evidence)`. Each would reduce the functions to under 50 lines.

---

### Info

- `models/pipeline.py:48-51` -- `_ensure_dirs()` is called redundantly in `fetch_fred_series()`, `load_manual_source()`, `update_freshness()`, and `fetch_all()`. Calling once at the top of `fetch_all()` and removing from sub-functions is cleaner.
- `models/output.py:91,154,213` -- `OUTPUT_DIR.mkdir(parents=True, exist_ok=True)` repeated in every write function. Extract to a module-level call at import time or a shared `_ensure_output_dir()` called once.
- `models/model_vdem.py:181-197` and `models/model_vdem.py:247-263` -- `_compute_roc_components` and `_compute_level_components` share 16 lines of nearly identical missing-data handling. The missing-variable guard could be extracted to a shared `_neutral_component(name)` helper.
- `models/run.py:125` -- `from models.config import MODEL_WEIGHTS` is imported inside the printing loop body (inside `main()`). This is a deferred import executed during iteration. Move to top of `main()` or extract to `_print_summary()`.
- `models/config.py` -- Variables #19 (WFRBSTP1300) and #45 (WFRBSTP1300) use the same FRED series_id. Variable #19's construction recipe references WFRBST01134 as a required component but this series is not explicitly fetched in the FRED loop in `fetch_all()` (only series IDs listed as `SourceType.FRED_API` are fetched automatically). Worth verifying that the intra-elite ratio for #19 is computed correctly in `construct_proxy()`.

## Dimension Summaries

### Complexity

Most functions are appropriately sized. The two blockers (`fetch_all` at 125 lines, `main` at 140 lines) are the only genuine violations of the 2x threshold. Several functions in model files (`compute_pli` at 102 lines, `compute_ensemble` at 94 lines, `construct_proxy` at 94 lines) are warnings. The mathematical scoring logic itself is not overly complex; the length comes from thorough data-absent guards and print progress statements.

### Performance

The critical performance gap is `compute_domain_scores()` using row-wise `apply()` instead of vectorized pandas operations. For a monthly DataFrame spanning 1947-2025 (~930 rows x 5 domains), this is ~4,650 Python function calls that could be a single vectorized multiply. Similarly, `_build_raw_history()` in ensemble.py uses a Python row-iteration loop over ~930 DatetimeIndex entries, with the MIN_DOMAINS_REQUIRED guard now embedded inside that loop. Both are batch operations (not user-facing), so the impact is on pipeline run time, not latency. The bootstrap CI loop (1000 iterations x 930 domain-weight computations inside `_compute_composite_from_latest`) is the most computationally intensive section but is correctly factored.

### Style

The main style concern is systematic code duplication across model files. The `_variable_lookup()` function, the domain contribution normalization block, and the `_compute_component()` pattern are each copied 3-5 times with near-identical implementations. The duplication is low enough not to block, but represents maintenance risk: a future change to variable lookup behavior or domain contribution logic would require edits in 5 files. All functions have clear docstrings and consistent naming conventions throughout.

### Idiom

Python idioms are well-applied throughout. Dataclasses are used for `Variable`, `ModelOutput`, and `ComponentScore`. Enums are used for `Domain`, `SourceType`, `EvidenceRating`, and `NormDirection`. The `@register_model` decorator pattern for model discovery is idiomatic. Type hints are present on all public functions. The bootstrap uses `np.random.default_rng()` (the modern NumPy RNG API) with a fixed seed. One minor idiom gap: the `weighted_mean` closure in `compute_domain_scores()` triggers row-wise `apply()` when vectorized pandas operations are more idiomatic and significantly faster.

## Rewrite Priority

Priority-ordered list (highest impact first):

1. **`models/pipeline.py:356-480`** -- `fetch_all()` at 125 lines exceeds 2x threshold -> Extract 4 phase subfunctions (Blocker)
2. **`models/run.py:33-172`** -- `main()` at 140 lines exceeds 2x threshold -> Extract `_run_pipeline()`, `_print_summary()`, `_write_outputs()` (Blocker)
3. **`models/pipeline.py:528-535`** -- Row-wise `apply(weighted_mean)` -> Vectorized `mul/sum` in `compute_domain_scores()` (Warning, Performance)
4. **`models/ensemble.py:174-196`** -- Python loop over DatetimeIndex in `_build_raw_history()` -> Vectorized composite computation with `.where(valid_count >= MIN_DOMAINS_REQUIRED)` (Warning, Performance)
5. **All 5 model files** -- `_variable_lookup()` defined 5 times -> Module-level `VARIABLE_LOOKUP` constant in `config.py` (Warning, Style)
6. **All 5 model files** -- Domain contribution normalization block copy-pasted -> `compute_domain_contributions()` in `models.py` (Warning, Style)
7. **`models/model_psi.py`, `models/model_georgescu.py`** -- `_compute_component()` duplicated -> `compute_weighted_component()` in `models.py` (Warning, Style)
8. **`models/calibrate.py:243-333`** -- `_compute_composite_from_latest()` and `_bootstrap_one_iteration()` near-identical -> Parameterized shared function (Warning, Style)
9. **`models/pipeline.py:171-264`** -- `construct_proxy()` if-chain at 94 lines -> `@register_proxy` decorator dispatch (Warning, Complexity)

---
*Profiled: 2026-03-04T12:00:00Z*
*Profiler: Claude (gsd-profiler)*
