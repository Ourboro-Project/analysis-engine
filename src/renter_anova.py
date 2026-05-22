from pathlib import Path
import pandas as pd
from scipy import stats
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "datasets" / "renter_survey.csv"

df = pd.read_csv(DATA_PATH)

group_col = "renter_cluster"
dv_list = ["age", "happiness", "down_payment"]  # Dependent variables to analyze


def format_p(p):
    if p < 0.001:
        return "p < 0.001"
    elif p < 0.01:
        return "p < 0.01"
    elif p < 0.05:
        return "p < 0.05"
    else:
        return f"p = {p:.3f} (ns)"


def run_anova(df, group_col, dv):

    # -------------------------
    # Group stats
    # -------------------------
    summary = (
        df.groupby(group_col)[dv]
        .agg(N="count", Mean="mean", SD="std")
        .reset_index()
    )

    summary["SE"] = summary["SD"] / np.sqrt(summary["N"])

    # -------------------------
    # ANOVA
    # -------------------------
    groups = [
        g[dv].values for _, g in df.groupby(group_col)
    ]

    F, p = stats.f_oneway(*groups)

    # -------------------------
    # Output
    # -------------------------
    print(f"\n===== {dv.upper()} ANOVA =====")
    print(f"F = {F:.3f}")
    print(f"p = {format_p(p)}")
    print(summary)


# run all DVs
for dv in dv_list:
    run_anova(df, group_col, dv)    