from ..models import ANOVAResult
from .utils import format_p, interpret_eta_squared, format_posthoc_table, format_descriptive_table, format_year_means_table
import pandas as pd

def generate_report(result: ANOVAResult) -> str:
        """
        Generate a console-friendly ANOVA report.

        This report includes all computed statistical results
        from the ANOVA analysis pipeline for debugging and validation purposes.
        """
        sig_text = (
            "statistically significant"
            if result.is_significant
            else "not statistically significant"
        )

        group_stats_text = (
             format_descriptive_table(result.group_stats)
             .to_string(index=False)
             )
        
        dv_title = result.dv.replace("_", " ").title()

        year_means_text = (
             format_year_means_table(result.year_means)
             .to_string(index=False)
             if result.year_means is not None
             else "Year means not available"
        )       
        
        result_text = f"""

One-Way ANOVA Report
==============================

- Descriptive Statistics
{group_stats_text}


- {dv_title} Index Mean Values
{year_means_text}


- ANOVA Results
F({result.df_between}, {result.df_within}) = {result.F:.3f}
{format_p(result.p)}
Result: {sig_text} (alpha = {result.alpha})
"""

        # effect size, posthoc only if significant
        if result.is_significant:

            effect_text = (
                f"Eta² = {result.eta_squared:.4f} ({interpret_eta_squared(result.eta_squared)})"
                if result.eta_squared is not None
                else "eta_squared: not available"
            )

            posthoc_text = (
                 format_posthoc_table(result.posthoc_df)
                 .to_string(index=False)
            )

            result_text += f"""

- Effect Size (Eta Squared)
{effect_text}

* Note: Interpretation based on commonly used Cohen-style guidelines (0.01 small, 0.06 medium, 0.14 large).


- Post-hoc (Tukey HSD)
{posthoc_text}
"""

        result_text += "\n==============================\n"

        return result_text


def build_anova_summary_table(result: ANOVAResult) -> pd.DataFrame:

    return pd.DataFrame([
        {"Source": "Between Groups", "SS": round(result.SSB, 2), "df": result.df_between,
         "MS": round(result.MSB, 2), "F": round(result.F, 2), "p": format_p(result.p, with_prefix=False)},
        {"Source": "Within Groups",  "SS": round(result.SSW, 2), "df": result.df_within,
         "MS": round(result.MSW, 2), "F": "", "p": ""},
        {"Source": "Total",          "SS": round(result.SST, 2),
         "df": result.df_between + result.df_within, "MS": "", "F": "", "p": ""},
    ])


def generate_apa_report(result: ANOVAResult) -> str:
    """
    Generate an APA-style ANOVA report.
    """

    # Table 1: Descriptive stats 
    desc_df = format_descriptive_table(result.group_stats)
    dv_title = result.dv.replace("_", " ").title()

    table1 = f"""
Table 1 
Clusters and {dv_title} ANOVA

{dv_title} Index Mean Trends by Wave
F = {result.F:.3f} (difference between groups)
{format_p(result.p)}

{desc_df.to_string(index=False)}
""".strip()
    
    # Table 2: Year means
    if result.year_means is not None:
        year_df = format_year_means_table(result.year_means)
        table2_body = year_df.to_string(index=False)
    else:
        table2_body = "Year means not available"

    table2 = f"""
Table 2
{dv_title} Index Mean Values by Year

{table2_body}
""".strip()
    
    # Table 3: ANOVA summary table
    anova_df = build_anova_summary_table(result).to_string(index=False)

    table3 = f"""
Table 3
ANOVA Summary Table

{anova_df}
""".strip()

    # Table 4: Post-hoc (only if significant)
    if result.is_significant and result.posthoc_df is not None:
        posthoc_df = format_posthoc_table(result.posthoc_df)

        posthoc_df = posthoc_df.drop(columns=["Tukey_Statistic", "Effect size (Hedges’ g)"], errors="ignore")
    
        table4 = f"""
Table 4 
Post-hoc Comparisons (Tukey HSD)

{posthoc_df.to_string(index=False)}
""".strip()
        
    # APA-style summary text   
    eta_str = f", η² = {result.eta_squared:.3f}" if result.eta_squared else ""

    interpretation = f"""
A one-way ANOVA was conducted to examine differences in {dv_title} across groups.

Results indicated a {'statistically significant' if result.is_significant else 'non-significant'} effect of group on {dv_title}, 
F({result.df_between}, {result.df_within}) = {result.F:.2f}, {format_p(result.p)}{eta_str}.
""".strip()

    return "\n\n".join(
         block for block in [
              interpretation,
              table1,
              table2,
              table3,
              table4 if table4 else None
         ] if block
    )


def generate_html_report(result: ANOVAResult) -> str:
    dv_title = result.dv.replace("_", " ").title()
    eta_str = f", Eta Squared = {result.eta_squared:.3f}" if result.eta_squared else ""

    # interpretation text
    interpretation = (
        f"<p>A one-way ANOVA was conducted to examine differences in {dv_title} across groups.</p>"
        f"<p>Results indicated a "
        f"{'statistically significant' if result.is_significant else 'non-significant'} "
        f"effect of group on {dv_title}, "
        f"F({result.df_between}, {result.df_within}) = {result.F:.2f}, "
        f"{format_p(result.p, with_prefix=False)}{eta_str}.</p>"
    )

    # Table 1
    desc_html = format_descriptive_table(result.group_stats).to_html(index=False, classes="apa-table")
    table1 = f"""
    <h3>Table 1. Clusters and {dv_title} ANOVA</h3>
    <p>{dv_title} Index Mean Values<br>
       F = {result.F:.3f} (difference between groups), {format_p(result.p)}</p>
    {desc_html}
    """

    # Table 2
    if result.year_means is not None:
        year_df = format_year_means_table(result.year_means)
        year_df.index.name = None
        year_df.columns.name = None

        year_html = year_df.to_html(index=False, classes="apa-table")
    else:
        year_html = "<p>Year means not available</p>"

    table2 = f"""
    <h3>Table 2. {dv_title} Index Mean Trends by Wave</h3>
    {year_html}
    """

    # Table 3
    anova_html = build_anova_summary_table(result).to_html(index=False, classes="apa-table")
    table3 = f"""
    <h3>Table 3. One-Way ANOVA Results</h3>
    {anova_html}
    """

    # Table 4
    table4 = ""
    if result.is_significant and result.posthoc_df is not None:
        posthoc_df = format_posthoc_table(result.posthoc_df)
        posthoc_df = posthoc_df.drop(columns=["Tukey_Statistic", "Effect size (Hedges’ g)"], errors="ignore")
        posthoc_html = posthoc_df.to_html(index=False, classes="apa-table")
        table4 = f"""
        <h3>Table 4. Post-hoc Comparisons (Tukey HSD)</h3>
        {posthoc_html}
        """

    return f"""
    <div class="anova-report">
        {interpretation}
        {table1}
        {table2}
        {table3}
        {table4}
    </div>
    """
