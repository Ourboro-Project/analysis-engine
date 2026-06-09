from scipy.stats import f
import pandas as pd
import numpy as np


def calculate_sum_of_squares(
    df: pd.DataFrame,
    group_col: str,
    dv: str
) -> dict:
    """
    Calculate sum of squares decomposition for ANOVA.

    Args:
        df: input dataset
        group_col: grouping variable (IV)
        dv: dependent variable (DV)

    Returns:
        SSB: between-group variation (explained by group differences)
        SSW: within-group variation (unexplained variation)
        SST: total variation 
    """

    grand_mean = df[dv].mean()

    SSB = 0.0
    SSW = 0.0

    for _, g in df.groupby(group_col):
        values = g[dv].values
        group_mean = values.mean()
        n = len(values)

        # between-group variation
        SSB += n * (group_mean - grand_mean) ** 2

        # within-group variation
        SSW += np.sum((values - group_mean) ** 2)

    # total variation (definition-based)
    # Using NumPy vectorization for element-wise computation (no explicit loop)
    SST = np.sum((df[dv] - grand_mean) ** 2)

    return {
        "SSB": SSB,
        "SSW": SSW,
        "SST": SST
    }



def calculate_anova_statistics(ss, n_groups, n_samples) -> dict:
    """
        Calculate ANOVA test statistics from sum of squares.

        This function calculates degrees of freedom, mean squares,
        F-statistic, and p-value based on the provided SS values.

        Args:
            ss: dictionary containing sum of squares values (SSB, SSW, SST)
            n_groups: number of groups (IV)
            n_samples: total number of data points

        Returns:
            dict containing:
                df_between: degrees of freedom between groups
                df_within: degrees of freedom within groups
                MSB: mean square between groups
                MSW: mean square within groups
                F: F-statistic (MSB / MSW)
                p: p-value from F-distribution (SciPy)
        """
    df_between = n_groups - 1
    df_within = n_samples - n_groups

    msb = ss["SSB"] / df_between
    msw = ss["SSW"] / df_within

    F = msb / msw

    # 1st approach: Calculate p-value using SciPy's F-distribution CDF (Cumulative Distribution Function)
    # p = 1 - f.cdf(F, df_between, df_within)

    # 2nd approach: Calculate p-value using SciPy's F-distribution SF (Survival Function), which is more accurate for small p-values
    # sf is used instead of 1 - cdf to prevent floating-point precision loss
    p = f.sf(F, df_between, df_within)  

    return {
        "df_between": df_between,
        "df_within": df_within,
        "MSB": msb,
        "MSW": msw,
        "F": F,
        "p": p
    }

# print("ANOVA Statistics:\n")
# ss = calculate_sum_of_squares(data, "cluster", "happiness")
# n_groups = data["cluster"].nunique()
# n_samples = len(data)
# print(f"SS: {ss}")
# print(f"n_groups: {n_groups}")
# print(f"n_samples: {n_samples}")
# print(calculate_anova_statistics(ss, n_groups, n_samples))