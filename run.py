import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, "/mnt/podman-data/mjhan") # Temporary path: To be removed after packaging setup (pip install -e .)

from anova_analysis.strategies.one_way import run_anova 
from anova_analysis.reporting.report import generate_report, generate_apa_report, generate_html_report

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

df = pd.read_csv(BASE_DIR/"datasets"/"sample_anova_input.csv")

def run_anova_service(df, iv, dv_list, wave):
    """
    Run One-Way ANOVA for multiple dependent variables.

    Args:
        df: input dataset containing IV, DV(s), and wave column
        iv: independent variable (clustering variable)
        dv_list: list of dependent variables to analyze
        wave: survey wave/time indicator

    Returns:
        list of ANOVA results, one per dependent variable
    """
    results = [
        run_anova(df, iv, dv, wave)
        for dv in dv_list
    ]

    return results

anova_results = run_anova_service( 
    df,
    "cluster_label",
    ["happiness", "down_payment"],
    "wave")

for r in anova_results:
    print(f"Report:\n\n{generate_report(r)}")
    print(f"APA Style Report:\n\n{generate_apa_report(r)}\n")


html_reports = []

for r in anova_results:
    report_html = generate_html_report(r)

    html_reports.append(f"""
    <details>
      <summary> DV: {r.dv}</summary>
      {report_html}
    </details>
    """)


full_html = f"""
<html>
<head>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<meta charset="UTF-8">
<style>

body {{
    font-family: "Inter", Arial, sans-serif;
    font-size: 12pt;
    line-height: 1.5;
    margin: 40px;
    color: #000;
}}

.anova-report {{
    max-width: 850px;
    margin: auto;
}}

.apa-table {{
    border-collapse: collapse;
    margin: 16px 0;
    width: 100%;
    font-family: "Inter", Arial, sans-serif;
}}

.apa-table th,
.apa-table td {{
    border: 1px solid #333;
    padding: 6px 10px;
    text-align: left;  
    vertical-align: top;
}}

.apa-table th {{
    font-weight: bold;  
    border-top: 2px solid #000;
    border-bottom: 1px solid #000;
}}

.apa-table tr:last-child td {{
    border-bottom: 2px solid #000;
}}

h2, h3 {{
    font-weight: bold;
    margin-top: 20px;
}}

p {{
    margin: 6px 0;
}}

details {{
    margin: 12px 0;
    border: 1px solid #e6e6e6;
    border-radius: 8px;
    background: #fafafa;
    overflow: hidden;
    padding: 10px 14px;
}}

summary {{
    font-size: 15px;
    font-weight: 600;
    padding: 10px 12px;
    cursor: pointer;
    
}}

summary:hover {{
    background: #f0f4ff;
}}

details[open] {{
    border-color: #1a73e8;
    background: #ffffff;
}}

details[open] summary {{
    color: #1a73e8;
}}

</style>
</head>
<body>
<div class="anova-report">
<h2>One-Way ANOVA Report</h2>
{''.join(html_reports)}
</div>
</body>
</html>
"""

with open(OUTPUT_DIR / "anova_report.html", "w", encoding="utf-8") as f:
    f.write(full_html)
