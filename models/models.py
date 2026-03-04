"""
Shared model output types and model registry.
All models return ModelOutput. The registry enables iteration over all models.
"""
from dataclasses import dataclass, field
from typing import Callable
import pandas as pd


@dataclass
class ComponentScore:
    """A named sub-score within a model."""
    name: str
    value: float          # 0.0-1.0
    variables_used: list[str] = field(default_factory=list)


@dataclass
class ModelOutput:
    """Standardized output from any model's compute function."""
    model_id: str
    model_name: str
    score: float          # 0.0-100.0
    components: list[ComponentScore] = field(default_factory=list)
    domain_contributions: dict[str, float] = field(default_factory=dict)
    timestamp: str = ""
    variables_used: list[int] = field(default_factory=list)


# Model function signature: (DataFrame) -> ModelOutput
ModelFn = Callable[[pd.DataFrame], ModelOutput]

# Registry populated by model files
MODEL_REGISTRY: dict[str, ModelFn] = {}


def register_model(model_id: str):
    """Decorator to register a model function."""
    def decorator(fn: ModelFn) -> ModelFn:
        MODEL_REGISTRY[model_id] = fn
        return fn
    return decorator
