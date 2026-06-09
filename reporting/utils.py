import pandas as pd

def format_p(p: float) -> str:
    """
    Format p-value in a readable way.
    
    Args: 
        p: p-value to format
    Returns:    
        Formatted p-value string
    
    """
    if p < 0.001:
        return "p < 0.001"
    elif p < 0.01:
        return "p < 0.01"
    elif p < 0.05:
        return "p < 0.05"
    else:
        return f"p = {p:.3f} (ns)"
    
def interpret_eta_squared(eta: float) -> str:
    if eta >= 0.14:
        return "Large Effect"
    elif eta >= 0.06:
        return "Medium Effect"
    else:
        return "Small Effect"


def format_posthoc_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert raw Tukey output into standardized analysis table.
    Args:

    """

    result = pd.DataFrame()

    result["Group A"] = df["A"]
    result["Group B"] = df["B"]
    result["Mean Diff"] = df["diff"].round(2)   
    result["p-value"] = df["p_tukey"].apply(format_p)
    result["Effect size(Hedges g)"] = df["hedges"].round(2)
    result["t"] = df["T"].round(2)
    result["SE"] = df["se"].round(3)

    return result