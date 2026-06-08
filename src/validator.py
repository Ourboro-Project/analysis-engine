from scipy.stats import f_oneway
from anova_result import ANOVAResult
from anova_engine import load_data, run_anova
import numpy as np

def validate_anova(manual_result: ANOVAResult, df, group_col, dv) -> dict:
    """
    Validate manual ANOVA results using SciPy's f_oneway as a reference.

    Args:
        manual_result: ANOVAResult object from manual calculation
        df: input dataset
        group_col: grouping variable (IV)
        dv: dependent variable (DV)

    Returns:
        F_match: whether F-values match
        p_match: whether p-values match
        manual_F: F-value from manual calculation
        ref_F: F-value from SciPy reference
    """
    
    groups = [g[dv].values for _, g in df.groupby(group_col)]
    ref_F, ref_p = f_oneway(*groups)

    # rtol is used because floating-point calculations may have small rounding differences
    return {
        "F_match": np.isclose(manual_result.F, ref_F, rtol=1e-5),
        "p_match": np.isclose(manual_result.p, ref_p, rtol=1e-5),
        "manual_F": manual_result.F,
        "ref_F":    ref_F,
        "manual_p": manual_result.p,
        "ref_p":    ref_p
    }

data = load_data("sample_anova_input.csv")
manual_result = run_anova(data, "cluster", "happiness")
validation_result = validate_anova(manual_result, data, "cluster", "happiness")
print("\n=== VALIDATION RESULT ===")
for k, v in validation_result.items():
    print(f"{k:<15}: {v}")