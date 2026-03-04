"""
Base model class and output dataclass for all Revolution Index models.

All models inherit from BaseModel and return ModelOutput instances.
This ensures consistent interfaces for backtesting, ensemble combination,
and uncertainty quantification.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field

import numpy as np
import pandas as pd


@dataclass
class ModelOutput:
    """Standard output from any Revolution Index model."""

    # Core score (0-100 scale)
    score: float

    # Confidence interval (from bootstrap or analytical)
    ci_lower: float = 0.0
    ci_upper: float = 100.0

    # Sub-component scores (model-specific)
    components: dict[str, float] = field(default_factory=dict)

    # Data quality flags
    data_quality: dict[str, object] = field(default_factory=dict)

    # Alert flags (rapid deterioration, J-curve, etc.)
    flags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "score": self.score,
            "ci_lower": self.ci_lower,
            "ci_upper": self.ci_upper,
            "components": self.components,
            "data_quality": self.data_quality,
            "flags": self.flags,
        }


class BaseModel(ABC):
    """Abstract base class for all Revolution Index models."""

    name: str = "base"

    @abstractmethod
    def compute(self, data: pd.DataFrame, date: pd.Timestamp) -> ModelOutput:
        """
        Compute the model score for a single date.

        Args:
            data: Unified monthly DataFrame (columns = series IDs)
            date: The date to compute the score for

        Returns:
            ModelOutput with score, components, and metadata
        """
        ...

    def compute_historical(
        self,
        data: pd.DataFrame,
        start: str | None = None,
        end: str | None = None,
    ) -> pd.DataFrame:
        """
        Compute the model for an entire date range.

        Returns DataFrame with columns:
        - score: the model score (0-100)
        - ci_lower, ci_upper: confidence bounds
        - plus one column per component
        """
        if start:
            data = data.loc[start:]
        if end:
            data = data.loc[:end]

        results = []
        for date in data.index:
            try:
                output = self.compute(data, date)
                row = {
                    "date": date,
                    "score": output.score,
                    "ci_lower": output.ci_lower,
                    "ci_upper": output.ci_upper,
                }
                for comp_name, comp_val in output.components.items():
                    row[comp_name] = comp_val
                results.append(row)
            except (KeyError, ValueError):
                # Skip dates where required data is missing
                continue

        if not results:
            return pd.DataFrame()

        df = pd.DataFrame(results).set_index("date")
        return df

    def required_series(self) -> list[str]:
        """Return list of series IDs required by this model."""
        return []

    def check_data_availability(self, data: pd.DataFrame) -> dict[str, bool]:
        """Check which required series are available in the data."""
        return {
            sid: sid in data.columns and data[sid].notna().any()
            for sid in self.required_series()
        }
