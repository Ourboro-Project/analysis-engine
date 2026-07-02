import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from ..models import ANOVAResult
from matplotlib.lines import Line2D
from .utils import format_p_star

# Default plot style for all figures
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Helvetica", "Arial"],
    "font.size": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": False
})

def plot_group_means(result: ANOVAResult, iv: str) -> plt.Figure:
    """
    Plot group means with error bars (±1 SE) for a single wave ANOVA result.
    """
    df:pd.DataFrame = result.group_stats
    dv_title = result.dv.replace("_", " ").title()

    fig, ax = plt.subplots(figsize=(8, 5))

    x = np.arange(len(df)) * 1.0

    colors = plt.cm.Set2(np.linspace(0, 1, len(df)))

    ax.bar(
        x,
        df["Mean"],
        yerr=df["SE"],
        capsize=3,
        color=colors,
        edgecolor = colors,
        linewidth=3,
        width=0.5,
        alpha=0.9
    )

    ax.set_xticks(x)
    ax.set_xticklabels(df[iv], rotation=0, ha="center")
    ax.set_title(f"{dv_title} by Cluster - (Wave {result.wave_label})", pad=16, fontsize=12, fontweight='bold')
    ax.set_ylabel(f"{dv_title} (Mean)", fontsize=10)
   
    legend = [
        Line2D(
            [0], [0],
            marker='s',
            color='w',
            markerfacecolor=colors[0],
            markersize=10,
            label='Mean │ ±1  Standard Error'
        )
    ]

    ax.legend(
        handles=legend,
        loc="upper left",
        frameon=False
    )

    plt.tight_layout()
    
    return fig



def plot_mean_trend(wave_means: pd.DataFrame, dv: str) -> plt.Figure:
    """
    Plot mean trend lines across waves (Y0–Y2) for each cluster.
    """

    dv_title = dv.replace("_", " ").title()

    fig, ax = plt.subplots(figsize=(9, 5))

    x = np.array([0, 1, 2])
    wave_labels = ["Y0", "Y1", "Y2"]
    n_groups = len(wave_means)
    colors = plt.cm.Set2(np.linspace(0, 1, n_groups))
    markers = ["o", "s", "^", "D", "v", "P", "X"]

    for i, (cluster, row) in enumerate(wave_means.iterrows()):
        # Extract wave means in order
        y = [row["Y0"], row["Y1"], row["Y2"]]

        ax.plot(
            x,
            y,
            color=colors[i],
            marker=markers[i % len(markers)],
            linewidth=2,
            markersize=6,
            label=cluster
        )

    ax.set_xticks(x)
    ax.set_xticklabels(wave_labels)
    ax.set_xlabel("Survey Wave")
    ax.set_ylabel(f"{dv_title} Mean", fontsize=10)
    ax.set_title(f"{dv_title} Mean Trend by Cluster Over Time", pad=16, fontsize=12, fontweight='bold')
    ax.legend(loc="center left", bbox_to_anchor=(1.02, 0.5), frameon=False, fontsize=9.5)

    plt.tight_layout()
    plt.subplots_adjust(right=0.75)

    return fig

    

def plot_tukey_heatmap(result: ANOVAResult) -> plt.Figure:
    """
    Tukey HSD post-hoc pairwise comparison heatmap.
    Shows mean differences and significance levels.
    """
    df: pd.DataFrame = result.posthoc_df.copy()
    dv_title = result.dv.replace("_", " ").title()

    # Get unique clusters from pairwise comparisons
    groups = sorted(set(df["A"]).union(set(df["B"])))

    diff_matrix = pd.DataFrame(0.0, index=groups, columns=groups)
    p_matrix = pd.DataFrame(1.0, index=groups, columns=groups)

    for _, row in df.iterrows():
        g1, g2 = row["A"], row["B"]
        diff, pval = row["diff"], row["p_tukey"]
        
        diff_matrix.loc[g1, g2] = diff
        diff_matrix.loc[g2, g1] = -diff
        
        p_matrix.loc[g1, g2] = pval
        p_matrix.loc[g2, g1] = pval

    annot_matrix = pd.DataFrame("", index=groups, columns=groups)
    for i in groups:
        for j in groups:
            if i == j:
                annot_matrix.loc[i, j] = "-" 
                continue
            diff_val = diff_matrix.loc[i, j]
            p_val = p_matrix.loc[i, j]
            stars = format_p_star(p_val)
            annot_matrix.loc[i, j] = f"{diff_val:+.2f}\n{stars}"

    fig, ax = plt.subplots(figsize=(8, 6.5))

    max_val = np.max(np.abs(diff_matrix.values))
    
    sns.heatmap(
        diff_matrix,
        annot=annot_matrix,     
        fmt="",                 
        cmap="RdBu_r",           
        center=0,
        vmin=-max_val,
        vmax=max_val,
        linewidths=0.5,         
        linecolor="#f0f0f0",
        cbar_kws={"shrink": 0.8},
        annot_kws={"size": 9.5},
        ax=ax
    )
    cbar = ax.collections[0].colorbar
    cbar.set_label("Pairwise Mean Difference", labelpad=10)

    new_labels = ["\n".join(label.split()) for label in groups]

    ax.set_xticklabels(new_labels, rotation=0, ha="center")
    ax.set_yticklabels(groups, rotation=0, va="center")
    ax.set_title(f"{dv_title} Tukey HSD Post-hoc - (Wave {result.wave_label})", pad=16, fontsize=12, fontweight='bold')   
    # Statistical significance legend
    ax.text(
        0.0, -0.15, 
        "* p < 0.05, ** p < 0.01, *** p < 0.001, ns: non-significant", 
        transform=ax.transAxes, 
        ha="left", 
        fontsize=9,
        color="#555555"
    )

    plt.tight_layout()
    
    return fig