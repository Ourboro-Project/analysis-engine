from ..models import ANOVAResult
from .utils import format_p, interpret_eta_squared, format_posthoc_table

def generate_spss_report(result: ANOVAResult) -> str:
        sig_text = (
            "statistically significant"
            if result.is_significant
            else "not statistically significant"
        )

        result_text = f"""
==============================
ONE-WAY ANOVA RESULT
==============================

--- DESCRIPTIVE STATISTICS ---
{result.group_stats.to_string(index=False)}


--- ANOVA TABLE ---
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

            posthoc_text = format_posthoc_table(result.posthoc_df)

            result_text += f"""

--- EFFECT SIZE (Eta Squared) --- 
{effect_text}

* Note: Interpretation based on commonly used Cohen-style guidelines (0.01 small, 0.06 medium, 0.14 large).


--- POSTHOC (Tukey HSD) --- 
{posthoc_text}
"""

        result_text += "\n==============================\n"

        return result_text



def generate_apa_report(result: ANOVAResult) -> str:
    p_str  = "< .001" if result.p < 0.001 else f"= {result.p:.3f}"
    eta_str = f", η² = {result.eta_squared:.3f}" if result.eta_squared else ""

    lines = [
        f"A one-way ANOVA was conducted.",
        f"Results indicated a {'significant' if result.is_significant else 'non-significant'} effect,",
        f"F({result.df_between}, {result.df_within}) = {result.F:.2f}, p {p_str}{eta_str}.",
    ]

    if result.is_significant and result.posthoc_df is not None:
        lines.append("\nPost-hoc comparisons (Tukey HSD):")
        ph = format_posthoc_table(result.posthoc_df)
        for _, row in ph.iterrows():
            lines.append(
                f"  {row['Group A']} vs {row['Group B']}: "
                f"{row['p-value']}, g = {row['Effect size(Hedges g)']}"
            )

    return "\n".join(lines)