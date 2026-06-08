from anova_result import ANOVAResult

def calculate_effect_size(result: ANOVAResult) -> float:
    """
    Calculate eta squared (η²) as effect size.
    
    η² = SSB / SST
    interpretation:
        0.01 = small
        0.06 = medium
        0.14 = large
    """
    return result.SSB / result.SST