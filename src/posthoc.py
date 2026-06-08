import pingouin as pg
import pandas as pd

def run_posthoc(df, group_col, dv) -> pd.DataFrame:
    """
    Run Tukey HSD post-hoc analysis.
    Only called when ANOVA is significant.
    """
    return pg.pairwise_tukey(data=df, dv=dv, between=group_col)