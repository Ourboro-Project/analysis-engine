import pandas as pd

def format_p(p: float, with_prefix: bool = True) -> str:
    """
    Format p-value in a readable way.
    
    Args: 
        p: p-value to format
        with_prefix: Whether to include the "p = " prefix
    Returns:    
        Formatted p-value string
    """
    if p < 0.001:
        val = "< 0.001"
    elif p < 0.01:
        val = "< 0.01"
    elif p < 0.05:
        val = "< 0.05"
    else:
        val = f"= {p:.3f} (ns)"
    return f"p {val}" if with_prefix else val
    
def interpret_eta_squared(eta: float) -> str:
    if eta >= 0.14:
        return "Large Effect"
    elif eta >= 0.06:
        return "Medium Effect"
    else:
        return "Small Effect"

def format_descriptive_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert raw group statistics into standardized reporting table.
    
    """
    result = pd.DataFrame()

    result["Cluster"] = df["cluster_label"]
    result["N"] = df["N"].astype(int)
    result["Mean"] = df["Mean"].round(2)
    result["Std. Deviation"] = df["SD"].round(2)
    result["Std. Error"] = df["SE"].round(2)
    
    return result

def format_year_means_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert raw pivot table (group x year means) into standardized reporting format.
    
    """

    result = df.copy().round(2)

    result.index.name = "Cluster"
    result = result.reset_index()

    return result


def format_posthoc_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert raw Tukey output into standardized analysis table.

    """

    result = pd.DataFrame()

    result["Group 1"] = df["A"]
    result["Group 2"] = df["B"]
    result["Mean Difference"] = df["diff"].round(2)   
    result["p (Tukey)"] = df["p_tukey"].apply(format_p)
    result["Effect size (Hedges’ g)"] = df["hedges"].round(2)
    result["Tukey_Statistic"] = df["T"].round(2)
    result["Std. Error"] = df["se"].round(3)

    return result


def format_p_star(p):
    """
    Convert p-value to significance stars for Tukey HSD heatmap
    """
    if p < 0.001:
        return "***"
    elif p < 0.01:
        return "**"
    elif p < 0.05:
        return "*"
    else:
        return "ns"
