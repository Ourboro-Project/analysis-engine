import sys
from pathlib import Path
import pandas as pd

import matplotlib
matplotlib.use('Agg')                           # Use 'Agg' backend to generate plots as images without a display screen

sys.path.insert(0, "/mnt/podman-data/mjhan")    # Temporary path: To be removed after packaging setup (pip install -e .)

from anova_analysis.strategies.one_way import run_anova
from anova_analysis.reporting.plotter import plot_group_means, plot_mean_trend, plot_tukey_heatmap

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

anova_results = run_anova_service(df, iv="cluster_label", dv_list=["happiness", "down_payment"], wave_col="wave")

for item in anova_results:
    for wave, r in item["by_wave"].items():
        fig = plot_group_means(r, iv="cluster_label")
        fig.savefig(OUTPUT_DIR / f"plot_group_means_{item['dv']}_{wave}.png")

for item in anova_results:
    fig = plot_mean_trend(item["wave_means"], dv=item["dv"])
    fig.savefig(OUTPUT_DIR / f"plot_mean_trend_{item['dv']}.png")

for item in anova_results:
    for wave, r in item["by_wave"].items():
        fig = plot_tukey_heatmap(r)
        fig.savefig(OUTPUT_DIR / f"tukey_heatmap_{item['dv']}_{wave}.png")
