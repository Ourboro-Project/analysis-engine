from dataclasses import dataclass, field
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
    
    # Descriptive statistics
    group_stats: pd.DataFrame
    dv: str 

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

    # Default significance level
    alpha: float = 0.05  

    # Year mean comparison (optional, for ordered group trends)
    year_means: pd.DataFrame | None = field(default=None, repr=False)
    
    # Optional post-analysis when significant
    eta_squared: float | None = None
    posthoc_df: pd.DataFrame | None = field(default=None, repr=False)


    @property
    def is_significant(self) -> bool:
        """
        Determine if the ANOVA result is statistically significant.
        True if p-value is smaller than alpha.
        
        """
        return self.p < self.alpha
    

    