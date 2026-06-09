import matplotlib.pyplot as plt
import pandas as pd

def plot_group_means(group_stats: pd.DataFrame, group_col: str, dv: str):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(group_stats[group_col], group_stats["Mean"],
           yerr=group_stats["SE"], capsize=5)
    ax.set_xlabel(group_col)
    ax.set_ylabel(dv)
    ax.set_title("Group Means with SE")
    return fig

def plot_posthoc_heatmap(posthoc_df: pd.DataFrame):
    import seaborn as sns
    pivot = posthoc_df.pivot(index="Group A", columns="Group B", values="Mean Diff")
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(pivot, annot=True, fmt=".2f", ax=ax)
    ax.set_title("Posthoc Mean Differences")
    return fig