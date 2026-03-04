"""
Model 1: Turchin Structural-Demographic PSI (Political Stress Indicator)

Simplified version using three proxy variables:
- MMP (Mass Mobilization Potential): 1 - normalized labor share of GDP
- EMP (Elite Mobilization Potential): normalized top 1% income share
- SFD (State Fiscal Distress): normalized federal debt / GDP

Aggregation: geometric mean (critical review A1 fix)
  PSI = (MMP * EMP * SFD) ^ (1/3)

This preserves the multiplicative interaction logic (if any factor is zero,
PSI is zero — instability requires all three pressures simultaneously)
while keeping output in a human-readable range.

Reference: model-specifications.md lines 92-96, 137-141, 181-184
Fix: critical-review-model-specs.md A1 (geometric mean instead of product)
"""

import numpy as np
import pandas as pd

from src.models.base_model import BaseModel, ModelOutput
from src.analysis.normalization import minmax_normalize
from config import REFERENCE_START


class TurchinPSI(BaseModel):
    """Simplified Turchin Political Stress Indicator with geometric mean fix."""

    name = "turchin_psi"

    # Required data columns
    LABOR_SHARE = "W270RE1A156NBEA"
    TOP1_SHARE = "top_1pct_share"
    DEBT_GDP = "GFDEGDQ188S"

    def __init__(self, reference_start: str = REFERENCE_START):
        self.reference_start = reference_start

    def required_series(self) -> list[str]:
        return [self.LABOR_SHARE, self.TOP1_SHARE, self.DEBT_GDP]

    def compute(self, data: pd.DataFrame, date: pd.Timestamp) -> ModelOutput:
        """
        Compute PSI for a single date.

        Steps:
        1. Get current values for all three components
        2. Min-max normalize each against the reference period
        3. Invert labor share (lower share = higher MMP)
        4. Compute geometric mean
        5. Scale to 0-100
        """
        # Get reference period data (up to current date)
        ref = data.loc[self.reference_start:date]

        # Get latest available values (LOCF means they exist at any monthly date)
        labor_share = data.loc[:date, self.LABOR_SHARE].dropna()
        top1_share = data.loc[:date, self.TOP1_SHARE].dropna()
        debt_gdp = data.loc[:date, self.DEBT_GDP].dropna()

        if labor_share.empty or top1_share.empty or debt_gdp.empty:
            raise ValueError(f"Missing data for PSI computation at {date}")

        current_labor = labor_share.iloc[-1]
        current_top1 = top1_share.iloc[-1]
        current_debt = debt_gdp.iloc[-1]

        # Normalize against reference period
        ref_labor = ref[self.LABOR_SHARE].dropna()
        ref_top1 = ref[self.TOP1_SHARE].dropna()
        ref_debt = ref[self.DEBT_GDP].dropna()

        # MMP: inverted labor share (lower labor share = higher mass mobilization potential)
        mmp = 1.0 - minmax_normalize(current_labor, ref_labor)

        # EMP: top 1% income share (higher = more elite competition/overproduction)
        emp = minmax_normalize(current_top1, ref_top1)

        # SFD: debt to GDP (higher = more state fiscal distress)
        sfd = minmax_normalize(current_debt, ref_debt)

        # Geometric mean (critical review A1 fix)
        # Preserves: if any component is 0, PSI = 0
        # Fixes: three 0.70 values -> 0.70, not 0.343
        components_arr = np.array([mmp, emp, sfd])

        if np.any(components_arr == 0):
            psi_raw = 0.0
        else:
            psi_raw = np.power(np.prod(components_arr), 1.0 / 3.0)

        psi_score = float(np.clip(psi_raw * 100, 0, 100))

        # Check for flags
        flags = []
        if mmp > 0.8 and emp > 0.8 and sfd > 0.8:
            flags.append("ALL_COMPONENTS_ELEVATED")
        if psi_score > 65:
            flags.append("HIGH_STRUCTURAL_STRESS")

        # Data quality
        quality = {
            "labor_share_latest": str(labor_share.index[-1].date()),
            "top1_share_latest": str(top1_share.index[-1].date()),
            "debt_gdp_latest": str(debt_gdp.index[-1].date()),
        }

        return ModelOutput(
            score=psi_score,
            components={
                "MMP": float(mmp * 100),
                "EMP": float(emp * 100),
                "SFD": float(sfd * 100),
            },
            data_quality=quality,
            flags=flags,
        )
