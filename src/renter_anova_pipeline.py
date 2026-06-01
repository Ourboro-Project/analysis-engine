from pathlib import Path
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from statsmodels.stats.multicomp import pairwise_tukeyhsd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "datasets" / "renter_survey_long.csv"

df = pd.read_csv(DATA_PATH)

print(df.head())

group_col = "cluster"
year_col = "year"
metrics = ["age", "happiness", "down_payment"]

# p-value formatting
def format_p(p):
    if p < 0.001:
        return "p < 0.001"
    elif p < 0.01:
        return "p < 0.01"
    elif p < 0.05:
        return "p < 0.05"
    else:
        return f"p = {p:.3f} (ns)"
    
# ANOVA + Group table
def run_anova(df, dv):

    print("\n" + "="*60)
    print(f"METRIC: {dv}")
    print("="*60)

    # # -------------------------
    # # 1. Group summary table
    # # -------------------------
    # group_stats = (
    #     df.groupby(group_col)[dv]
    #     .agg(N="count", Mean="mean", SD="std")
    #     .reset_index()
    # )

    # group_stats["SE"] = group_stats["SD"] / np.sqrt(group_stats["N"])

    # # formatting
    # group_stats["Mean"] = group_stats["Mean"].round(2)
    # group_stats["SD"] = group_stats["SD"].round(2)
    # group_stats["SE"] = group_stats["SE"].round(2)


    # print("\n[Group Summary]")
    # print(group_stats)

    # -------------------------
    # 2. ANOVA (SciPy)
    # -------------------------
    groups = [g[dv].values for _, g in df.groupby(group_col)]
    F, p = stats.f_oneway(*groups)

    print("\n[ANOVA]")
    print(f"F = {F:.3f}")
    print(f"p = {format_p(p)}")

    # -------------------------
    # 3. Year means table
    # -------------------------
    year_means = (
        df.groupby([year_col, group_col])[dv]
        .mean()
        .unstack()
        
    )

    print("\n[Year Means]")
    print(year_means)

    # -------------------------
    # 4. Plot (Group mean)
    # -------------------------
    fig, ax = plt.subplots()

    group_stats.plot(
        x=group_col,
        y="Mean",
        kind="bar",
        yerr="SE",
        legend=False,
        ax=ax
    )

    ax.set_title(f"{dv} by Cluster")
    ax.set_ylabel(dv)
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()
    

def posthoc(df, dv):
    tukey = pairwise_tukeyhsd(
        endog=df[dv],
        groups=df[group_col],
        alpha=0.05
    )
    print("\n[Posthoc - Tukey HSD]")
    print(tukey)



def create_group_summary(df, group_col, dv):
    summary = (
        df.groupby(group_col)[dv]
        .agg(N="count", Mean="mean", SD="std")
        .reset_index()
    )
    summary["SE"] = summary["SD"] / np.sqrt(summary["N"])       # SE: Standard Error

    # formatting
    # summary["Mean"] = summary["Mean"].round(2)
    # summary["SD"] = summary["SD"].round(2)
    # summary["SE"] = summary["SE"].round(2)

    return summary









# Run for all metrics
for dv in metrics:
    run_anova(df, dv)
    posthoc(df, dv) 
