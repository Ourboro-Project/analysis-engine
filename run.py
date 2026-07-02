import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, "/mnt/podman-data/mjhan") # Temporary path: To be removed after packaging setup (pip install -e .)

from anova_analysis.services.anova_service import run_anova_service 
from anova_analysis.reporting.report import generate_report, generate_apa_report, generate_html_report, format_year_means_table

def main():

    BASE_DIR = Path(__file__).resolve().parent
    OUTPUT_DIR = BASE_DIR / "outputs"
    OUTPUT_DIR.mkdir(exist_ok=True)

    df = pd.read_csv(BASE_DIR/"datasets"/"sample_anova_input.csv")

    # Run ANOVA separately for each wave (Y0, Y1, Y2)
    anova_results = run_anova_service(
        df, 
        iv="cluster_label", 
        dv_list=["happiness", "down_payment"], 
        wave_col="wave")

    # Generate console reports for validation and debugging
    for item in anova_results:
        for wave, r in item["by_wave"].items():
            print(f"\nDV: {item['dv']} | Wave: {wave}")
            # Console-friendly summary report (for quick debugging)
            print(generate_report(r)) 
            # APA-style formatted report (for validation / paper formatting check)
            print("========== APA STYLE REPORT ==========\n")
            print(generate_apa_report(r))

    html_reports = []
    # Create one HTML report section per dependent variable
    for item in anova_results:
        dv = item["dv"]
        dv_title = dv.replace("_", " ").title()

        # Table 1: mean trends across waves
        year_df = format_year_means_table(item["wave_means"])
        year_df.index.name = None
        year_df.columns.name = None
        wave_means_html = year_df.to_html(index=False, classes="apa-table")
        table_wave_trend = f"""
        <div class="wave-means-section">
            <h2>Overview Across Waves</h2>
            <h3>Table 1. {dv_title} Index Mean Trends by Wave</h3>
            {wave_means_html}
        </div>
        """

        wave_blocks = []
        for wave, r in item["by_wave"].items():
            wave_blocks.append(f"""
            <div class="wave-section">
                <h2>Detailed ANOVA Results by Wave</h2>
                <h3>Wave: {wave}</h3>             
                <h3>ANOVA Summary</h3>
                {generate_html_report(r)}
            </div>
            """)

        html_reports.append(f"""
        <details>
            <summary>DV: {dv}</summary>
            {table_wave_trend}
            {''.join(wave_blocks)}
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
    font-size: 16px;
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
.wave-section {{
    padding-bottom: 16px;
    margin: 16px 0;
    border-bottom: 2px solid #e6e6e6;
}}
.wave-means-section {{
    margin-top: 20px;
    padding-top: 12px;
    padding-bottom: 12px;
    border-top: 2px solid #e6e6e6;
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

if __name__ == "__main__":
    main()