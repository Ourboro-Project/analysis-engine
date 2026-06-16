import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, "/mnt/podman-data/mjhan")

from anova_analysis.strategies.one_way import run_anova 
from anova_analysis.reporting.report import generate_report, generate_apa_report, generate_html_report


BASE_DIR = Path(__file__).resolve().parent

def load_data(filename: str) -> pd.DataFrame:
    return pd.read_csv(BASE_DIR / "datasets" / filename)


def run_anova_service():
    data = load_data("sample_anova_input.csv")

    iv = "cluster"
    wave = "wave"
    dv_list = ["happiness", "down_payment"]

    results = [
        run_anova(data, iv, dv, wave)
        for dv in dv_list
    ]

    return results, dv_list

results, dv_list = run_anova_service()

for r in results:
    print(f"Report:\n\n{generate_report(r)}")
    print(f"APA Style Report:\n\n{generate_apa_report(r)}\n")


html_reports = []

for r, dv in zip(results, dv_list):
    report_html = generate_html_report(r)

    html_reports.append(f"""
    <details>
      <summary> DV: {dv}</summary>
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

# with open("anova_report.html", "w", encoding="utf-8") as f:
#     f.write(full_html)

OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

with open(OUTPUT_DIR / "anova_report.html", "w", encoding="utf-8") as f:
    f.write(full_html)
