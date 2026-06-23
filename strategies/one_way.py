from ..modules.stats import calculate_sum_of_squares, calculate_anova_statistics
from ..modules.descriptive import calculate_group_statistics
from ..modules.effect_size import calculate_effect_size
from ..modules.posthoc import run_posthoc
from ..models import ANOVAResult
import pandas as pd


def run_anova(df, iv, dv, alpha: float = 0.05) -> ANOVAResult:
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
        iv: independent variable (clustering variable)
        dv: dependent variable 
        alpha: significance level for hypothesis testing (default: 0.05)

    Returns:
        Sum of Squares: SSB, SSW, SST
        Degrees of Freedom: df_between, df_within
        Mean Squares: MSB, MSW
        Inference: F-statistic, p-value and statistical decision (based on alpha)
    """

    # Column existence checks
    if iv not in df.columns:
        raise ValueError(f"iv '{iv}' not found in DataFrame")
    if dv not in df.columns:
        raise ValueError(f"dv '{dv}' not found in DataFrame")
       
    # Type checks
    if not pd.api.types.is_numeric_dtype(df[dv]):
        raise ValueError(f"dv '{dv}' must be numeric")
    if iv == dv:
        raise ValueError("iv and dv cannot be the same column")

    # Missing values are not handled in this step; expected clean input
    if df[[iv, dv]].isnull().any().any():
        raise ValueError("Input data must be pre-cleaned (no missing values allowed)")
    
    # ANOVA requires at least 2 groups
    if df[iv].nunique() < 2:
        raise ValueError("At least 2 groups are required for ANOVA")
    
    # Each group must have at least 2 samples for variance estimation
    group_counts = df.groupby(iv)[dv].count()
    if (group_counts < 2).any():
        small = group_counts[group_counts < 2].index.tolist()
        raise ValueError(f"Groups {small} have less than 2 samples")
    
    # Prevents zero variance groups that would cause MSW=0 (division by zero) and invalid F-statistic
    group_stds = df.groupby(iv)[dv].std()
    if (group_stds == 0).any():
        zero_var = group_stds[group_stds == 0].index.tolist()
        raise ValueError(f"Groups {zero_var} have zero variance")
    

    # 1. SS calculation
    ss = calculate_sum_of_squares(df, iv, dv)

    # 2. Summary stats
    n_groups = df[iv].nunique()
    n_samples = len(df)

    # 3. Inference
    result = calculate_anova_statistics(ss, n_groups, n_samples)

    # 4. Build ANOVAResult and apply post-analysis if significant
    anova_result = ANOVAResult(
        group_stats = calculate_group_statistics(df, iv, dv),
        dv = dv,
        SSB = ss["SSB"],
        SSW = ss["SSW"],
        SST = ss["SST"],

        df_between = result["df_between"],
        df_within = result["df_within"],

        MSB = result["MSB"],
        MSW = result["MSW"],

        F = result["F"],
        p = result["p"],
        alpha = alpha 
    )

    if anova_result.is_significant and df[iv].nunique() >= 3:
        # p < 0.05 means the difference is statistically significant (unlikely to be caused by random chance)
        # but with large samples, even very small differences can become significant
        # so we also check effect size (eta_squared) to understand the real impact
        # if is_significant is True but eta_squared is small,
        # the practical difference between groups may still be small
        # Tukey HSD requires at least 3 groups for meaningful pairwise post-hoc comparisons
        anova_result.eta_squared = calculate_effect_size(anova_result)
        anova_result.posthoc_df = run_posthoc(df, iv, dv)

    return anova_result



