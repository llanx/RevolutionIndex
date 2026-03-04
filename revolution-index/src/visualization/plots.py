"""
Visualization module for Revolution Index models.

Produces:
1. Multi-panel historical time series with episode shading
2. Component breakdowns for each model
3. Cross-correlation lag plots for financial stress pathway
4. Current-state dashboard summary
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle

from config import HISTORICAL_EPISODES, QUIET_PERIODS, SCORE_THRESHOLDS


# Color palette
COLORS = {
    "turchin_psi": "#2c7bb6",
    "prospect_theory": "#d7191c",
    "financial_stress": "#fdae61",
    "composite": "#1a1a1a",
    "ci_band": "#cccccc",
    "episode": "#ffcccc",
    "quiet": "#ccffcc",
}

COMPONENT_COLORS = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]


def _add_episode_shading(ax, alpha=0.15):
    """Add shaded bands for historical episodes and quiet periods."""
    for name, ep in HISTORICAL_EPISODES.items():
        start = pd.Timestamp(ep["start"])
        end = pd.Timestamp(ep["end"])
        ax.axvspan(start, end, alpha=alpha, color="#ff6666", zorder=0)

    for name, qp in QUIET_PERIODS.items():
        start = pd.Timestamp(qp["start"])
        end = pd.Timestamp(qp["end"])
        ax.axvspan(start, end, alpha=alpha * 0.7, color="#66ff66", zorder=0)


def _add_threshold_lines(ax, alpha=0.3):
    """Add horizontal threshold lines."""
    for label, (low, high) in SCORE_THRESHOLDS.items():
        if label in ("elevated", "high"):
            ax.axhline(y=low, color="gray", linestyle="--", alpha=alpha, linewidth=0.5)


def plot_multi_panel(
    model_results: dict[str, pd.DataFrame],
    composite: pd.Series | None = None,
    ci_lower: pd.Series | None = None,
    ci_upper: pd.Series | None = None,
    title: str = "Revolution Index — Historical Model Outputs",
    save_path: str | None = None,
):
    """
    Create the primary multi-panel visualization.

    Panel 1: Turchin PSI with MMP/EMP/SFD components
    Panel 2: Prospect Theory PLI with domain scores
    Panel 3: Financial Stress FSSI and ETI
    Panel 4: Composite with confidence band

    Args:
        model_results: dict of {model_name: DataFrame with 'score' + component columns}
        composite: optional composite score series
        ci_lower/ci_upper: optional confidence interval bands
        save_path: if provided, save figure to this path
    """
    n_panels = len(model_results) + (1 if composite is not None else 0)
    fig, axes = plt.subplots(n_panels, 1, figsize=(16, 4 * n_panels), sharex=True)
    if n_panels == 1:
        axes = [axes]

    panel_idx = 0

    # Panel: Turchin PSI
    if "turchin_psi" in model_results:
        ax = axes[panel_idx]
        df = model_results["turchin_psi"]

        ax.plot(df.index, df["score"], color=COLORS["turchin_psi"], linewidth=1.5, label="PSI")

        for i, comp in enumerate(["MMP", "EMP", "SFD"]):
            if comp in df.columns:
                ax.plot(df.index, df[comp], color=COMPONENT_COLORS[i],
                       linewidth=0.8, alpha=0.6, linestyle="--", label=comp)

        _add_episode_shading(ax)
        _add_threshold_lines(ax)
        ax.set_ylabel("Score (0-100)")
        ax.set_title("Turchin PSI (Structural-Demographic)")
        ax.legend(loc="upper left", fontsize=8)
        ax.set_ylim(0, 100)
        panel_idx += 1

    # Panel: Prospect Theory PLI
    if "prospect_theory" in model_results:
        ax = axes[panel_idx]
        df = model_results["prospect_theory"]

        ax.plot(df.index, df["score"], color=COLORS["prospect_theory"], linewidth=1.5, label="PLI")

        domain_cols = [c for c in df.columns if c.endswith("_loss")]
        for i, col in enumerate(domain_cols):
            ax.plot(df.index, df[col], color=COMPONENT_COLORS[i % len(COMPONENT_COLORS)],
                   linewidth=0.8, alpha=0.5, linestyle="--",
                   label=col.replace("_loss", ""))

        _add_episode_shading(ax)
        _add_threshold_lines(ax)
        ax.set_ylabel("Score (0-100)")
        ax.set_title("Prospect Theory PLI (Perceived Loss)")
        ax.legend(loc="upper left", fontsize=8)
        ax.set_ylim(0, 100)
        panel_idx += 1

    # Panel: Financial Stress Pathway
    if "financial_stress" in model_results:
        ax = axes[panel_idx]
        df = model_results["financial_stress"]

        ax.plot(df.index, df["score"], color=COLORS["financial_stress"],
               linewidth=1.5, label="Combined")

        if "FSSI" in df.columns:
            ax.plot(df.index, df["FSSI"], color="#e41a1c",
                   linewidth=1.0, alpha=0.7, label="FSSI (Financial)")
        if "ETI" in df.columns:
            ax.plot(df.index, df["ETI"], color="#377eb8",
                   linewidth=1.0, alpha=0.7, label="ETI (Economic)")

        _add_episode_shading(ax)
        _add_threshold_lines(ax)
        ax.set_ylabel("Score (0-100)")
        ax.set_title("Financial Stress Pathway (Stages 1-2)")
        ax.legend(loc="upper left", fontsize=8)
        ax.set_ylim(0, 100)
        panel_idx += 1

    # Panel: Composite
    if composite is not None:
        ax = axes[panel_idx]

        if ci_lower is not None and ci_upper is not None:
            ax.fill_between(composite.index, ci_lower, ci_upper,
                          alpha=0.2, color=COLORS["ci_band"], label="95% CI")

        ax.plot(composite.index, composite, color=COLORS["composite"],
               linewidth=2.0, label="Composite")

        _add_episode_shading(ax)
        _add_threshold_lines(ax)
        ax.set_ylabel("Score (0-100)")
        ax.set_title("Composite Revolution Index")
        ax.legend(loc="upper left", fontsize=8)
        ax.set_ylim(0, 100)
        panel_idx += 1

    # Format x-axis
    axes[-1].xaxis.set_major_locator(mdates.YearLocator(5))
    axes[-1].xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    axes[-1].set_xlabel("Year")

    fig.suptitle(title, fontsize=14, fontweight="bold", y=1.01)
    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")

    return fig


def plot_lag_analysis(
    lag_df: pd.DataFrame,
    title: str = "FSSI-ETI Cross-Correlation (Lag Analysis)",
    save_path: str | None = None,
):
    """
    Plot cross-correlation between FSSI and ETI at various lags.

    Highlights the hypothesized 3-12 month transmission window.
    """
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.bar(lag_df["lag_months"], lag_df["correlation"], color="#2c7bb6", alpha=0.7)
    ax.axhspan(0, 0, color="gray", linewidth=0.5)

    # Highlight hypothesized window
    ax.axvspan(3, 12, alpha=0.1, color="orange", label="Hypothesized 3-12 month lag")

    # Mark peak correlation
    if len(lag_df) > 0:
        peak_idx = lag_df["correlation"].idxmax()
        peak_lag = lag_df.loc[peak_idx, "lag_months"]
        peak_corr = lag_df.loc[peak_idx, "correlation"]
        ax.annotate(
            f"Peak: {peak_lag}mo (r={peak_corr:.3f})",
            xy=(peak_lag, peak_corr),
            xytext=(peak_lag + 2, peak_corr + 0.05),
            arrowprops=dict(arrowstyle="->", color="black"),
            fontsize=10,
        )

    ax.set_xlabel("Lag (months, FSSI leading ETI)")
    ax.set_ylabel("Pearson Correlation")
    ax.set_title(title)
    ax.legend()

    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")

    return fig


def plot_backtesting_summary(
    report: dict,
    save_path: str | None = None,
):
    """
    Plot backtesting results as a heatmap-style summary.

    Rows = episodes/quiet periods
    Columns = models
    Cells = max score during that period
    """
    model_names = list(report["episodes"].keys())

    # Collect all episode scores
    episode_names = []
    episode_labels = []
    score_matrix = []

    for ep_name, ep in HISTORICAL_EPISODES.items():
        episode_names.append(ep_name)
        episode_labels.append(ep["label"])
        row = []
        for model in model_names:
            ep_df = report["episodes"][model]
            match = ep_df[ep_df["episode"] == ep_name]
            if len(match) > 0 and match.iloc[0]["data_available"]:
                row.append(match.iloc[0]["max_score"])
            else:
                row.append(np.nan)
        score_matrix.append(row)

    for qp_name, qp in QUIET_PERIODS.items():
        episode_names.append(qp_name)
        episode_labels.append(f"[Quiet] {qp['label']}")
        row = []
        for model in model_names:
            qp_df = report["quiet_periods"][model]
            match = qp_df[qp_df["period"] == qp_name]
            if len(match) > 0 and match.iloc[0]["data_available"]:
                row.append(match.iloc[0]["max_score"])
            else:
                row.append(np.nan)
        score_matrix.append(row)

    score_df = pd.DataFrame(score_matrix, index=episode_labels, columns=model_names)

    fig, ax = plt.subplots(figsize=(10, 6))
    im = ax.imshow(score_df.values, cmap="RdYlGn_r", vmin=0, vmax=100, aspect="auto")

    ax.set_xticks(range(len(model_names)))
    ax.set_xticklabels(model_names, rotation=45, ha="right")
    ax.set_yticks(range(len(episode_labels)))
    ax.set_yticklabels(episode_labels, fontsize=9)

    # Add text annotations
    for i in range(len(episode_labels)):
        for j in range(len(model_names)):
            val = score_df.values[i, j]
            if not np.isnan(val):
                color = "white" if val > 60 else "black"
                ax.text(j, i, f"{val:.0f}", ha="center", va="center",
                       color=color, fontsize=10, fontweight="bold")
            else:
                ax.text(j, i, "N/A", ha="center", va="center",
                       color="gray", fontsize=9)

    plt.colorbar(im, ax=ax, label="Max Score (0-100)")
    ax.set_title("Backtesting: Max Score per Model per Episode", fontweight="bold")
    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")

    return fig
