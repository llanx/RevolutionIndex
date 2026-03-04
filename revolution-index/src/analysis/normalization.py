"""
Normalization functions for the Revolution Index.

All normalization against historical distributions is centralized here
to ensure consistency across models.

Design decisions (from critical review):
- Common reference period: 1970-present for percentile normalization (B2)
- All functions accept a reference series to normalize against
- No implicit global state; all state passed explicitly
"""

import numpy as np
import pandas as pd


def percentile_rank(value: float, reference: pd.Series) -> float:
    """
    Compute the percentile rank of a value within a reference distribution.

    Returns a value in [0, 1] where 0 means the value is below all
    reference observations and 1 means it's above all.

    Args:
        value: The value to rank
        reference: Historical distribution to rank against (NaN-safe)
    """
    ref = reference.dropna()
    if len(ref) == 0:
        return 0.5
    return float((ref < value).mean())


def minmax_normalize(value: float, reference: pd.Series) -> float:
    """
    Min-max normalize a value to [0, 1] using reference distribution bounds.

    Args:
        value: The value to normalize
        reference: Historical distribution providing min/max bounds (NaN-safe)
    """
    ref = reference.dropna()
    if len(ref) == 0:
        return 0.5
    rmin = ref.min()
    rmax = ref.max()
    if rmax == rmin:
        return 0.5
    result = (value - rmin) / (rmax - rmin)
    return float(np.clip(result, 0.0, 1.0))


def zscore(value: float, reference: pd.Series) -> float:
    """
    Z-score standardization: (value - mean) / std.

    Args:
        value: The value to standardize
        reference: Historical distribution providing mean/std (NaN-safe)
    """
    ref = reference.dropna()
    if len(ref) < 2:
        return 0.0
    std = ref.std()
    if std == 0:
        return 0.0
    return float((value - ref.mean()) / std)


def rolling_zscore(
    series: pd.Series,
    window_years: int = 20,
) -> pd.Series:
    """
    Compute rolling z-score with a specified window.

    Used by the Financial Stress Pathway model for z-scoring
    against a 20-year rolling window.

    Args:
        series: Time series to z-score (monthly frequency expected)
        window_years: Window size in years (converted to months internally)
    """
    window = window_years * 12
    rolling_mean = series.rolling(window=window, min_periods=max(24, window // 4)).mean()
    rolling_std = series.rolling(window=window, min_periods=max(24, window // 4)).std()
    z = (series - rolling_mean) / rolling_std.replace(0, np.nan)
    return z


def percentile_rank_series(
    series: pd.Series,
    reference_start: str = "1970-01-01",
) -> pd.Series:
    """
    Compute expanding percentile rank for each point in a series.

    At each time t, the percentile rank is computed against all values
    from reference_start to t. This gives a time-varying percentile
    that incorporates all available history up to that point.

    Args:
        series: Time series to rank
        reference_start: Start date for the reference period
    """
    ref = series.loc[reference_start:]
    result = pd.Series(index=ref.index, dtype=float)

    for i, (dt, val) in enumerate(ref.items()):
        if pd.isna(val):
            result.iloc[i] = np.nan
            continue
        history = ref.iloc[:i + 1].dropna()
        if len(history) < 2:
            result.iloc[i] = 0.5
        else:
            result.iloc[i] = float((history < val).mean())

    return result


def minmax_normalize_series(
    series: pd.Series,
    reference_start: str = "1970-01-01",
) -> pd.Series:
    """
    Compute expanding min-max normalization for each point in a series.

    At each time t, normalization uses min/max from reference_start to t.

    Args:
        series: Time series to normalize
        reference_start: Start date for the reference period
    """
    ref = series.loc[reference_start:]
    expanding_min = ref.expanding().min()
    expanding_max = ref.expanding().max()
    range_vals = expanding_max - expanding_min
    # Avoid division by zero
    range_vals = range_vals.replace(0, np.nan)
    result = (ref - expanding_min) / range_vals
    return result.clip(0.0, 1.0)
