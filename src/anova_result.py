from dataclasses import dataclass
import pandas as pd

@dataclass
class ANOVAResult:
    """
    Stores results of an ANOVA analysis.

    This is a general result container that can be used
    for different ANOVA types (one-way, two-way, etc.).

    A dataclass is used instead of a dictionary 
    for better readability, easier debugging, and future extensibility.
    """
    
    # Sum of Squares
    SSB: float
    SSW: float
    SST: float
    
    # Degrees of freedom
    df_between: int
    df_within: int
    
    # Mean squares
    MSB: float
    MSW: float
    
    # Inference (Test Results)
    F: float
    p: float

    # default significance level
    alpha: float = 0.05  
    
    # for the future: effect size and post-hoc results
    # eta_squared: float | None = None
    # posthoc_df: pd.DataFrame | None = field(default=None, repr=False)
    # group_stats: pd.DataFrame | None = field(default=None, repr=False)

    @property
    def is_significant(self) -> bool:
        """Determine if the ANOVA result is statistically significant."""
        return self.p < self.alpha