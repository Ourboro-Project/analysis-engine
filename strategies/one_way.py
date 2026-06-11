from ..modules.stats import calculate_sum_of_squares, calculate_anova_statistics
from ..modules.descriptive import calculate_group_statistics, calculate_year_means
from ..modules.effect_size import calculate_effect_size
from ..modules.posthoc import run_posthoc
from ..models import ANOVAResult
import pandas as pd


def run_anova(df, group_col, dv, year_col: str | None = None, alpha: float = 0.05) -> ANOVAResult:
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
        year_col: optional column for grouped mean trends over an ordered variable (e.g., time, wave, stages)
        alpha: significance level for hypothesis testing (default: 0.05)

    Returns:
        Sum of Squares: SSB, SSW, SST
        Degrees of Freedom: df_between, df_within
        Mean Squares: MSB, MSW
        Inference: F-statistic, p-value and statistical decision (based on alpha)
    """

    if group_col not in df.columns:
        raise ValueError(f"group_col '{group_col}' not found in DataFrame")
    if dv not in df.columns:
        raise ValueError(f"dv '{dv}' not found in DataFrame")
    
    if not pd.api.types.is_numeric_dtype(df[dv]):
        raise ValueError(f"dv '{dv}' must be numeric")
    if pd.api.types.is_numeric_dtype(df[group_col]):
        raise ValueError(f"group_col '{group_col}' should be categorical, not numeric") #check

    if df[dv].isnull().any():
        raise ValueError(f"dv '{dv}' contains missing values")
    if df[group_col].isnull().any():
        raise ValueError(f"group_col '{group_col}' contains missing values")
    
    if df[group_col].nunique() < 2:
        raise ValueError("At least 2 groups are required for ANOVA")
    
    if len(df) < 10:
        raise ValueError("Sample size too small for ANOVA (minimum 10)")
    
    group_counts = df.groupby(group_col)[dv].count()
    if (group_counts < 2).any():
        small = group_counts[group_counts < 2].index.tolist()
        raise ValueError(f"Groups {small} have less than 2 samples")
    
    group_stds = df.groupby(group_col)[dv].std()
    if (group_stds == 0).any():
        zero_var = group_stds[group_stds == 0].index.tolist()
        raise ValueError(f"Groups {zero_var} have zero variance")
    

    # 1. SS calculation
    ss = calculate_sum_of_squares(df, group_col, dv)

    # 2. Summary stats
    n_groups = df[group_col].nunique()
    n_samples = len(df)

    # 3. Inference
    result = calculate_anova_statistics(ss, n_groups, n_samples)

    # 4. Build ANOVAResult and apply post-analysis if significant

    anova_result = ANOVAResult(
        group_stats = calculate_group_statistics(df, group_col, dv),
        dv = dv,
        year_means = calculate_year_means(df, group_col, year_col, dv) if year_col else None,
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

    if anova_result.is_significant:
        # p < 0.05 means the difference is statistically significant (unlikely to be caused by random chance)
        # but with large samples, even very small differences can become significant
        # so we also check effect size (eta_squared) to understand the real impact
        # if is_significant is True but eta_squared is small,
        # the practical difference between groups may still be small
        anova_result.eta_squared = calculate_effect_size(anova_result)
        anova_result.posthoc_df = run_posthoc(df, group_col, dv)

    return anova_result



