from pathlib import Path
from scipy.stats import f
from anova_result import ANOVAResult
from effect_size import calculate_effect_size
from posthoc import run_posthoc
import pandas as pd
import numpy as np



BASE_DIR = Path(__file__).resolve().parent.parent


def load_data(filename: str) -> pd.DataFrame:
    """
    Load a CSV dataset from the project's datasets folder.

    Args:
        filename: Name of the CSV file located in the datasets directory.

    Returns:
        pd.DataFrame: Loaded dataset as a pandas DataFrame.
    """
    file_path = BASE_DIR / "datasets" / filename
    return pd.read_csv(file_path)


# data = print(load_data("sample_anova_input.csv").head())


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


data = load_data("sample_anova_input.csv")
# print(calculate_group_statistics(data, "cluster", "happiness"))


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

# data = load_data("sample_anova_input.csv")
# print(calculate_group_statistics(data, "cluster", "happiness"))
# print(calculate_sum_of_squares(data, "cluster", "happiness"))


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


def run_anova(df, group_col, dv, alpha: float = 0.05) -> ANOVAResult:
    """
    Run a complete ANOVA analysis pipeline.

    Steps:
    1. Calculate sum of squares (SSB, SSW, SST)
    2. Calculate group and sample sizes
    3. Calculate ANOVA statistics (df, MS, F, p)
    4. Apply statistical decision (based on alpha)
    5. Optionally calculate effect size and post-hoc analysis
    6. Return results as an ANOVAResult object

    Args:
        df: input dataset
        group_col: grouping variable (IV)
        dv: dependent variable (DV)
        alpha: significance level for hypothesis testing (default: 0.05)

    Returns:
        Sum of Squares: SSB, SSW, SST
        Degrees of Freedom: df_between, df_within
        Mean Squares: MSB, MSW
        Inference: F-statistic, p-value and statistical decision (based on alpha)
    """
    # 1. SS calculation
    ss = calculate_sum_of_squares(df, group_col, dv)

    # 2. Summary stats
    n_groups = df[group_col].nunique()
    n_samples = len(df)

    # 3. Inference
    result = calculate_anova_statistics(ss, n_groups, n_samples)

    # 4. Build ANOVAResult and apply post-analysis if significant

    anova_result = ANOVAResult(
        SSB=ss["SSB"],
        SSW=ss["SSW"],
        SST=ss["SST"],

        df_between=result["df_between"],
        df_within=result["df_within"],

        MSB=result["MSB"],
        MSW=result["MSW"],

        F=result["F"],
        p=result["p"],
        alpha=alpha
    )

    if anova_result.is_significant:
        print(f"ANOVA result is significant (p < {alpha})")
        anova_result.eta_squared = calculate_effect_size(anova_result)
        anova_result.posthoc_df = run_posthoc(df, group_col, dv)

    return anova_result


print(run_anova(data, "cluster", "happiness"))