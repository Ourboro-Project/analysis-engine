import sys
sys.path.insert(0, "/mnt/podman-data/mjhan")

from anova_analysis.strategies.one_way import run_anova
from anova_analysis.reporting.report import generate_spss_report
from anova_analysis.tests.conftest import load_data

data   = load_data("sample_anova_input.csv")
result = run_anova(data, "cluster", "happiness")
print(generate_spss_report(result))