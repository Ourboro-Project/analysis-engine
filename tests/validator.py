from scipy.stats import f_oneway
from ..models import ANOVAResult
import numpy as np

def validate_anova(manual_result: ANOVAResult, df, iv, dv) -> dict:
    """
    Validate manual ANOVA results using SciPy's f_oneway as a reference.

    Args:
        manual_result: ANOVAResult object from manual calculation
        df: input dataset
        iv: independent variable (clustering variable)
        dv: dependent variable 

    Returns:
        F_match: whether F-values match
        p_match: whether p-values match
        manual_F: F-value from manual calculation
        ref_F: F-value from SciPy reference
    """
    
    groups = [g[dv].values for _, g in df.groupby(iv)]
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

