"""
Backtesting framework for Revolution Index models.

Evaluates model outputs against known historical episodes (true positives)
and quiet periods (true negatives) to assess:
1. Sensitivity: does the model spike during crises?
2. Specificity: does it return to baseline during quiet periods?
3. Information content: meaningful variation or flatline/saturation?
4. Inter-model correlation: are models independent or redundant?

Reference: critical-review-model-specs.md D1 (no backtesting protocol)
"""

import numpy as np
import pandas as pd

from config import HISTORICAL_EPISODES, QUIET_PERIODS, SCORE_THRESHOLDS


class Backtester:
    """Evaluate model time series against historical episodes."""

    def __init__(self, detection_threshold: float = 45.0):
        """
        Args:
            detection_threshold: Score above which an episode is "detected".
                Default 45 = bottom of "elevated" range.
        """
        self.detection_threshold = detection_threshold

    def evaluate_episodes(self, model_series: pd.Series) -> pd.DataFrame:
        """
        Evaluate a model's time series against all historical crisis episodes.

        For each episode, reports:
        - max_score: highest score during the episode window
        - score_at_peak: score at the designated peak date
        - detected: whether max_score exceeded detection threshold
        - mean_score: average score during the episode window
        """
        results = []
        for name, ep in HISTORICAL_EPISODES.items():
            start, end = ep["start"], ep["end"]
            peak = ep["peak"]
            label = ep["label"]

            window = model_series.loc[start:end].dropna()
            if window.empty:
                results.append({
                    "episode": name,
                    "label": label,
                    "max_score": None,
                    "score_at_peak": None,
                    "mean_score": None,
                    "detected": False,
                    "data_available": False,
                })
                continue

            max_score = float(window.max())
            mean_score = float(window.mean())

            # Find closest date to peak
            peak_dt = pd.Timestamp(peak)
            closest_idx = window.index.get_indexer([peak_dt], method="nearest")[0]
            score_at_peak = float(window.iloc[closest_idx]) if closest_idx >= 0 else None

            results.append({
                "episode": name,
                "label": label,
                "max_score": max_score,
                "score_at_peak": score_at_peak,
                "mean_score": mean_score,
                "detected": max_score > self.detection_threshold,
                "data_available": True,
            })

        return pd.DataFrame(results)

    def evaluate_quiet_periods(self, model_series: pd.Series) -> pd.DataFrame:
        """
        Evaluate model during known quiet periods (expected true negatives).

        For each quiet period, reports:
        - max_score: highest score (should be low)
        - mean_score: average score
        - false_alarm: whether max exceeded detection threshold
        """
        results = []
        for name, period in QUIET_PERIODS.items():
            start, end = period["start"], period["end"]
            label = period["label"]

            window = model_series.loc[start:end].dropna()
            if window.empty:
                results.append({
                    "period": name,
                    "label": label,
                    "max_score": None,
                    "mean_score": None,
                    "false_alarm": False,
                    "data_available": False,
                })
                continue

            max_score = float(window.max())
            mean_score = float(window.mean())

            results.append({
                "period": name,
                "label": label,
                "max_score": max_score,
                "mean_score": mean_score,
                "false_alarm": max_score > self.detection_threshold,
                "data_available": True,
            })

        return pd.DataFrame(results)

    def evaluate_distribution(self, model_series: pd.Series) -> dict:
        """
        Assess whether model output has meaningful variation.

        A model that flatlines at 0 or saturates at 100 has no
        information content. Returns distribution statistics.
        """
        clean = model_series.dropna()
        if len(clean) == 0:
            return {"error": "No data"}

        return {
            "mean": float(clean.mean()),
            "median": float(clean.median()),
            "std": float(clean.std()),
            "min": float(clean.min()),
            "max": float(clean.max()),
            "pct_below_10": float((clean < 10).mean() * 100),
            "pct_above_90": float((clean > 90).mean() * 100),
            "pct_in_20_80": float(((clean >= 20) & (clean <= 80)).mean() * 100),
            "unique_deciles": len(set((clean // 10).astype(int))),
            "information_content": "good" if clean.std() > 10 else "poor",
        }

    def compute_inter_model_correlation(
        self, model_series: dict[str, pd.Series]
    ) -> pd.DataFrame:
        """
        Compute pairwise Pearson correlation between model outputs.

        If r > 0.85, models are not providing independent information
        (critical review C1: metric overlap problem).
        """
        df = pd.DataFrame(model_series)
        corr = df.corr()
        return corr

    def full_report(
        self,
        model_series: dict[str, pd.Series],
    ) -> dict:
        """
        Generate a complete backtesting report for all models.

        Returns dict with:
        - episodes: per-model episode detection results
        - quiet_periods: per-model quiet period results
        - distributions: per-model output distribution statistics
        - correlations: inter-model correlation matrix
        - summary: overall pass/fail assessment
        """
        report = {
            "episodes": {},
            "quiet_periods": {},
            "distributions": {},
            "summary": {},
        }

        for model_name, series in model_series.items():
            report["episodes"][model_name] = self.evaluate_episodes(series)
            report["quiet_periods"][model_name] = self.evaluate_quiet_periods(series)
            report["distributions"][model_name] = self.evaluate_distribution(series)

        report["correlations"] = self.compute_inter_model_correlation(model_series)

        # Summary assessment
        for model_name, series in model_series.items():
            ep_df = report["episodes"][model_name]
            qp_df = report["quiet_periods"][model_name]
            dist = report["distributions"][model_name]

            available_episodes = ep_df[ep_df["data_available"]]
            detected = available_episodes["detected"].sum() if len(available_episodes) > 0 else 0
            total_episodes = len(available_episodes)

            available_quiet = qp_df[qp_df["data_available"]]
            false_alarms = available_quiet["false_alarm"].sum() if len(available_quiet) > 0 else 0
            total_quiet = len(available_quiet)

            report["summary"][model_name] = {
                "episodes_detected": f"{detected}/{total_episodes}",
                "false_alarms": f"{false_alarms}/{total_quiet}",
                "distribution_quality": dist.get("information_content", "unknown"),
                "score_range": f"{dist.get('min', 0):.0f}-{dist.get('max', 0):.0f}",
            }

        return report
