import pandas as pd
from ..strategies.one_way import run_anova

def run_anova_service(df, iv, dv_list, wave_col):
    """
    Run One-Way ANOVA for multiple dependent variables across each wave.

    Args:
        df: input dataset containing IV, DV(s), and wave column
        iv: independent variable (clustering variable)
        dv_list: list of dependent variables to analyze
        wave_col: survey wave/time indicator

    Returns:
        list of dicts, one per DV, each containing:
        - dv: dependent variable name
        - wave_means: summary of per-wave means across all waves (DataFrame)
        - by_wave: dict of {wave: ANOVAResult} for each wave
    """
    # split into per-wave subsets before run_anova, so validated here
    if wave_col not in df.columns:
        raise ValueError(f"wave_col '{wave_col}' not found in DataFrame")
    
    results = []
    waves = sorted(df[wave_col].unique())

    for dv in dv_list:

        wave_results = {}
        for wave in waves:
            wave_df = df[df[wave_col] == wave]
            r = run_anova(wave_df, iv, dv)
            r.wave_label = wave
            wave_results[wave] = r

        wave_means = pd.DataFrame(
            {wave: r.group_stats.set_index(iv)["Mean"]
             for wave, r in wave_results.items()
             }).round(4)

        results.append({
            "dv": dv,
            "wave_means": wave_means,
            "by_wave": wave_results  # {"Y0": ANOVAResult, "Y1": ..., "Y2": ...}
        })

    return results