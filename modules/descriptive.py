import pandas as pd
import numpy as np

def calculate_group_statistics(
    df: pd.DataFrame,
    iv: str,
    dv: str
) -> pd.DataFrame:
    """
    Calculate group-level descriptive statistics for ANOVA.

    Args:
        df: input dataset
        iv: independent variable (clustering variable)
        dv: dependent variable 

    Returns:
        DataFrame with group-level statistics: 
            N: number of samples per group
            Mean: average value of the dependent variable
            SD: standard deviation within each group
            SE: standard error of the mean (SD / sqrt(N)), uncertainty of mean estimate
    """
    summary = (
        df.groupby(iv)[dv]
        .agg(N="count", Mean="mean", SD="std")
        .reset_index()
    )

    summary["SE"] = summary["SD"] / np.sqrt(summary["N"])

    return summary

