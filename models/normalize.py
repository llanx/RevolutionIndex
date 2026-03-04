"""
Normalization functions for mapping raw variable values to 0.0-1.0 stress intensity.

Uses rolling z-scores (recommended by Phase 2 literature review for trending US
macroeconomic series) as the primary approach, with percentile-rank fallback.

Design decisions:
  - Rolling z-score with 20-year window is the default (Phase 2 recommendation)
  - Standard normal CDF maps z-scores to 0.0-1.0 (avoids min-max pinning bug
    identified in Phase 1 for PSI)
  - Short series (< window observations) fall back to percentile rank
  - Direction parameter flips the mapping so that "higher raw value = higher stress"
    vs "lower raw value = higher stress" is handled correctly
"""
import numpy as np
import pandas as pd
from scipy import stats


def rolling_zscore(series: pd.Series, window: int = 240) -> pd.Series:
    """
    Rolling z-score normalization (recommended over min-max for trending series).

    For each observation, compute how many standard deviations it is from the
    rolling mean over the preceding `window` observations.

    Window default: 240 months (20 years) to capture secular trends while
    remaining sensitive to recent changes.

    Returns z-scores (unbounded). Use zscore_to_stress() to map to 0.0-1.0.

    Parameters
    ----------
    series : pd.Series
        Raw time series with numeric values. NaN values are preserved.
    window : int
        Rolling window size in observations (default 240 = 20 years monthly).

    Returns
    -------
    pd.Series
        Z-scores for each observation. The first `window - 1` observations
        will be NaN (insufficient history for rolling calculation).
    """
    rolling_mean = series.rolling(window=window, min_periods=max(window // 2, 1)).mean()
    rolling_std = series.rolling(window=window, min_periods=max(window // 2, 1)).std()

    # Avoid division by zero for constant series
    rolling_std = rolling_std.replace(0, np.nan)

    z_scores = (series - rolling_mean) / rolling_std
    return z_scores


def zscore_to_stress(z: pd.Series, direction: str = "higher_is_worse") -> pd.Series:
    """
    Map z-scores to 0.0-1.0 stress intensity using the standard normal CDF.

    For higher_is_worse: stress = CDF(z)
      - z = 0 maps to 0.5 (average)
      - z = +2 maps to ~0.977 (high stress)
      - z = -2 maps to ~0.023 (low stress)

    For lower_is_worse: stress = 1 - CDF(z)
      - z = 0 maps to 0.5 (average)
      - z = -2 maps to ~0.977 (high stress, because lower is worse)
      - z = +2 maps to ~0.023 (low stress)

    Parameters
    ----------
    z : pd.Series
        Z-score values (unbounded).
    direction : str
        Either "higher_is_worse" or "lower_is_worse".

    Returns
    -------
    pd.Series
        Stress intensity values in [0.0, 1.0].
    """
    cdf_values = pd.Series(stats.norm.cdf(z), index=z.index)

    if direction == "higher_is_worse":
        return cdf_values
    elif direction == "lower_is_worse":
        return 1.0 - cdf_values
    else:
        raise ValueError(
            f"Unknown direction '{direction}'. "
            "Must be 'higher_is_worse' or 'lower_is_worse'."
        )


def percentile_rank(series: pd.Series) -> pd.Series:
    """
    Percentile-rank normalization. Fallback for series too short for rolling z-score.

    Maps each observation to its rank within the full history, scaled to 0.0-1.0.
    Uses the average rank for tied values.

    Parameters
    ----------
    series : pd.Series
        Raw time series with numeric values.

    Returns
    -------
    pd.Series
        Percentile rank for each observation in [0.0, 1.0].
        NaN values in input are preserved as NaN in output.
    """
    # Drop NaN for ranking, then map back
    valid = series.dropna()
    if len(valid) == 0:
        return series.copy()

    # Rank with average method for ties, then scale to [0, 1]
    ranks = valid.rank(method="average")
    percentiles = (ranks - 1) / max(len(valid) - 1, 1)

    # Reindex to original series index, preserving NaN positions
    result = pd.Series(np.nan, index=series.index)
    result.loc[percentiles.index] = percentiles.values
    return result


def normalize_variable(
    raw_series: pd.Series,
    direction: str,
    method: str = "rolling_zscore",
    window: int = 240,
) -> pd.Series:
    """
    Main normalization entry point. Applies rolling z-score by default,
    falls back to percentile rank for short series (< window observations).

    Parameters
    ----------
    raw_series : pd.Series
        Raw time series with numeric values and DatetimeIndex.
    direction : str
        Either "higher_is_worse" or "lower_is_worse".
    method : str
        Normalization method: "rolling_zscore" (default) or "percentile_rank".
    window : int
        Rolling window size for z-score method (default 240 months).

    Returns
    -------
    pd.Series
        Normalized stress intensity values in 0.0-1.0 range.

    Notes
    -----
    - If the series has fewer non-NaN observations than `window`, the method
      automatically falls back to percentile rank normalization.
    - The direction parameter ensures that the output always represents
      "higher value = more stress" regardless of the raw variable's semantics.
    """
    valid_count = raw_series.dropna().shape[0]

    # Auto-fallback to percentile rank for short series
    if method == "rolling_zscore" and valid_count < window:
        method = "percentile_rank"

    if method == "rolling_zscore":
        z_scores = rolling_zscore(raw_series, window=window)
        stress = zscore_to_stress(z_scores, direction=direction)
        return stress

    elif method == "percentile_rank":
        pct = percentile_rank(raw_series)
        # For lower_is_worse, flip the percentile: higher rank = lower stress
        if direction == "lower_is_worse":
            pct = 1.0 - pct
        return pct

    else:
        raise ValueError(
            f"Unknown normalization method '{method}'. "
            "Must be 'rolling_zscore' or 'percentile_rank'."
        )
