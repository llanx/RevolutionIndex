"""
Model 2: Prospect Theory Perceived Loss Index (PLI)

Applies Kahneman & Tversky's prospect theory to measure perceived losses
across 5 life domains relative to recent peaks.

Domains (reduced from 8 in spec — dropped V-Dem, Opportunity Insights, Pew trust):
1. Wages (real median household income)
2. Housing (affordability index)
3. Health (life expectancy)
4. Employment (prime-age employment-population ratio)
5. Security/Sentiment (consumer sentiment index)

Fixes from critical review A2:
- K constants reduced by 10x (originals saturated at 100 during any recession)
- Breadth and velocity multipliers changed to additive bonuses (capped)
- sqrt compression on loss scores to prevent saturation

Reference: model-specifications.md lines 261-469
Fix: critical-review-model-specs.md A2
"""

import numpy as np
import pandas as pd

from src.models.base_model import BaseModel, ModelOutput
from config import REFERENCE_START, PLI_PARAMS


class ProspectTheoryPLI(BaseModel):
    """Perceived Loss Index using prospect theory across 5 domains."""

    name = "prospect_theory"

    # Domain definitions: series_id, K constant, whether higher is better
    DOMAINS = {
        "wages": {
            "series": "MEHOINUSA672N",
            "higher_is_better": True,
        },
        "housing": {
            "series": "FIXHAI",
            "higher_is_better": True,  # Higher affordability index = more affordable
        },
        "health": {
            "series": "SPDYNLE00INUSA",
            "higher_is_better": True,
        },
        "employment": {
            "series": "LNS12300060",
            "higher_is_better": True,
        },
        "security": {
            "series": "UMCSENT",
            "higher_is_better": True,  # Higher sentiment = better
        },
    }

    def __init__(
        self,
        lambda_: float | None = None,
        alpha: float | None = None,
        domain_K: dict[str, float] | None = None,
        reference_window_years: int | None = None,
        max_breadth_bonus: float | None = None,
        max_velocity_bonus: float | None = None,
    ):
        self.lambda_ = lambda_ or PLI_PARAMS["lambda_loss_aversion"]
        self.alpha = alpha or PLI_PARAMS["alpha_diminishing_sensitivity"]
        self.domain_K = domain_K or PLI_PARAMS["domain_K"].copy()
        self.ref_window_years = reference_window_years or PLI_PARAMS["reference_window_years"]
        self.max_breadth_bonus = max_breadth_bonus or PLI_PARAMS["max_breadth_bonus"]
        self.max_velocity_bonus = max_velocity_bonus or PLI_PARAMS["max_velocity_bonus"]

    def required_series(self) -> list[str]:
        return [d["series"] for d in self.DOMAINS.values()]

    def _compute_domain_loss(
        self,
        series: pd.Series,
        date: pd.Timestamp,
        domain_name: str,
        higher_is_better: bool,
    ) -> tuple[float, float, str | None]:
        """
        Compute the loss score for a single domain.

        Uses the trailing peak (over ref_window_years) as the reference point.
        Loss aversion (lambda) amplifies negative deviations.
        Diminishing sensitivity (alpha < 1) means each additional unit of loss
        hurts less than the previous one.

        Returns:
            (loss_score, deviation_pct, flag_or_none)
        """
        available = series.loc[:date].dropna()
        if len(available) < 2:
            return 0.0, 0.0, None

        current = available.iloc[-1]

        # Reference point: trailing peak over reference window
        window_start = date - pd.DateOffset(years=self.ref_window_years)
        window = available.loc[window_start:date]
        if len(window) == 0:
            window = available

        if higher_is_better:
            reference = window.max()
        else:
            reference = window.min()

        if reference == 0:
            return 0.0, 0.0, None

        # Deviation as proportion of reference
        if higher_is_better:
            deviation = (current - reference) / abs(reference)
        else:
            deviation = (reference - current) / abs(reference)

        # Apply prospect theory value function
        flag = None
        if deviation < 0:
            # LOSS domain: apply loss aversion and diminishing sensitivity
            abs_dev = abs(deviation)
            V = -self.lambda_ * (abs_dev ** self.alpha)

            # sqrt compression + reduced K constant (critical review A2 fix)
            K = self.domain_K.get(domain_name, 10.0)
            loss_score = min(100.0, max(0.0, np.sqrt(-V * K) * 10))

            # Flag rapid deterioration
            if len(available) > 12:
                prev_12m = available.iloc[-13] if len(available) > 12 else available.iloc[0]
                if prev_12m != 0:
                    twelve_month_change = (current - prev_12m) / abs(prev_12m)
                    if higher_is_better and twelve_month_change < -0.05:
                        flag = f"{domain_name}_RAPID_DECLINE"
                    elif not higher_is_better and twelve_month_change > 0.05:
                        flag = f"{domain_name}_RAPID_INCREASE"
        else:
            # GAIN or at peak: no perceived loss
            loss_score = 0.0

        return float(loss_score), float(deviation), flag

    def compute(self, data: pd.DataFrame, date: pd.Timestamp) -> ModelOutput:
        """Compute PLI across all domains for a single date."""
        loss_scores = {}
        deviations = {}
        flags = []

        for domain_name, config in self.DOMAINS.items():
            series_id = config["series"]
            if series_id not in data.columns:
                continue

            series = data[series_id]
            score, dev, flag = self._compute_domain_loss(
                series, date, domain_name, config["higher_is_better"]
            )
            loss_scores[domain_name] = score
            deviations[domain_name] = dev
            if flag:
                flags.append(flag)

        if not loss_scores:
            raise ValueError(f"No domain data available for PLI at {date}")

        # Mean of domain loss scores
        mean_loss = np.mean(list(loss_scores.values()))

        # Breadth bonus: how many domains are simultaneously in loss
        n_losses = sum(1 for d in deviations.values() if d < 0)
        breadth_bonus = min(
            self.max_breadth_bonus,
            max(0.0, (n_losses - 1) * (self.max_breadth_bonus / (len(self.DOMAINS) - 1)))
        )

        # Velocity bonus: are losses accelerating?
        # Compute 12-month change in loss scores (requires historical computation)
        # For single-date computation, use deviation magnitude as proxy
        avg_loss_magnitude = np.mean([abs(d) for d in deviations.values() if d < 0]) if n_losses > 0 else 0
        velocity_bonus = min(self.max_velocity_bonus, max(0.0, avg_loss_magnitude * 100))

        # Final PLI (additive, not multiplicative — critical review A2 fix)
        pli = float(np.clip(mean_loss + breadth_bonus + velocity_bonus, 0, 100))

        if n_losses >= 4:
            flags.append("MULTI_DOMAIN_LOSS")
        if pli > 65:
            flags.append("HIGH_PERCEIVED_LOSS")

        # Data quality
        quality = {}
        for domain_name, config in self.DOMAINS.items():
            series_id = config["series"]
            if series_id in data.columns:
                available = data.loc[:date, series_id].dropna()
                if len(available) > 0:
                    quality[f"{domain_name}_latest"] = str(available.index[-1].date())

        return ModelOutput(
            score=pli,
            components={
                **{f"{k}_loss": v for k, v in loss_scores.items()},
                "breadth_bonus": breadth_bonus,
                "velocity_bonus": velocity_bonus,
                "n_domains_in_loss": float(n_losses),
            },
            data_quality=quality,
            flags=flags,
        )
