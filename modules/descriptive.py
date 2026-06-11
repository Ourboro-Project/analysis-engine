import pandas as pd
import numpy as np

def calculate_group_statistics(
    df: pd.DataFrame,
    group_col: str,
    dv: str
) -> pd.DataFrame:
    """
    Calculate group-level descriptive statistics for ANOVA.

    Args:
        df: input dataset
        group_col: grouping variable (IV)
        dv: dependent variable (DV)

    Returns:
        DataFrame with group-level statistics: 
            N: number of samples per group
            Mean: average value of the dependent variable
            SD: standard deviation within each group
            SE: standard error of the mean (SD / sqrt(N)), uncertainty of mean estimate
    """
    summary = (
        df.groupby(group_col)[dv]
        .agg(N="count", Mean="mean", SD="std")
        .reset_index()
    )

    summary["SE"] = summary["SD"] / np.sqrt(summary["N"])

    return summary

def calculate_year_means(
    df: pd.DataFrame,
    group_col: str,
    year_col: str,
    dv: str
) -> pd.DataFrame:
    """
    Calculate mean of DV by group and year.
    Returns a pivot table: rows = groups, columns = years.
    """
    return (
        df.groupby([group_col, year_col])[dv]
        .mean()
        .round(4)
        .unstack(level=year_col)
    )