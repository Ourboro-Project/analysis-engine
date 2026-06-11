import sys

sys.path.insert(0, "/mnt/podman-data/mjhan")

from anova_analysis.strategies.one_way import run_anova 
from anova_analysis.reporting.report import generate_report
from anova_analysis.tests.conftest import load_data 

data = load_data("sample_anova_input.csv")
result = run_anova(data, "cluster", "happiness", "year")
print(generate_report(result))

print("POSTHOC DF COLUMNS:")
print(result.posthoc_df.columns)

print("\nPOSTHOC DF HEAD:")
print(result.posthoc_df.head())


