import sys

sys.path.insert(0, "/mnt/podman-data/mjhan")

from anova_analysis.strategies.one_way import run_anova 
from anova_analysis.reporting.report import generate_report, generate_apa_report, generate_html_report
from anova_analysis.tests.conftest import load_data 

data = load_data("sample_anova_input.csv")
result = run_anova(data, "cluster", "happiness", "year")
print(f"Report:\n\n{generate_report(result)}")
print(f"APA Style Report:\n\n{generate_apa_report(result)}\n")

html_report = generate_html_report(result)

full_html = f"""
<html>
<head>
<meta charset="UTF-8">
<style>

body {{
    font-family: "Calibri", serif;
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
    font-family: "Calibri", serif;
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

</style>
</head>
<body>
<div class="anova-report">
{html_report}
</div>
</body>
</html>
"""

with open("anova_report.html", "w", encoding="utf-8") as f:
    f.write(full_html)

