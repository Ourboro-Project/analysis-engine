import sys
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")                           # Use 'Agg' backend to generate plots as images without a display screen

sys.path.insert(0, "/mnt/podman-data/mjhan")    # Temporary path: To be removed after packaging setup (pip install -e .)

from anova_analysis.strategies.one_way import run_anova
from anova_analysis.reporting.exporter import export_anova_to_csv, export_anova_to_docx

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

df = pd.read_csv(BASE_DIR / "datasets" / "sample_anova_input.csv")

def run_anova_service(df, iv, dv_list, wave_col):
    results = []
    waves = sorted(df[wave_col].unique())

    for dv in dv_list:
        wave_results = {}

        for wave in waves:
            wave_df = df[df[wave_col] == wave]
            r = run_anova(wave_df, iv, dv)
            r.wave_label = wave
            wave_results[wave] = r

        wave_means = pd.DataFrame({
            wave: r.group_stats.set_index(iv)["Mean"]
            for wave, r in wave_results.items()
        }).round(4)

        results.append({"dv": dv, "wave_means": wave_means, "by_wave": wave_results})
    return results

anova_results = run_anova_service(
    df, 
    iv="cluster_label", 
    dv_list=["happiness", "down_payment"], 
    wave_col="wave"
    )


export_anova_to_csv(anova_results, OUTPUT_DIR)

export_anova_to_docx(anova_results, OUTPUT_DIR)

