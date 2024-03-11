from typing import List, Any, Tuple
import pandas as pd

class NumericalDescriptiveStatistics:
    
    def __init__(self, series: pd.Series):
        # Fields
        self.series
        self.count: int
        self.min: Any
        self.max: Any
        self.sum: Any
        self.mean: float
        self.median: float
        self.mode: float
        self.standard_deviation: float
        self.variance: float
        self.range: float
        self.quartiles: Tuple[int]
        self.interquartile_range: float
        self.skewness: float
        self.kurtosis: float
        
        # Constructor
        self.series = series
        self.count = len(series)
        self.min = series.min()
        self.max = series.max()
        self.sum = series.sum()
        self.mean = series.mean()
        self.median = series.median()
        self.mode = series.mode()
        self.standard_deviation = series.std()
        self.variance = series.var()
        self.range = self.max - self.min
        self.quartiles = series.quantile([0.25, 0.5, 0.75])
        self.interquartile_range = self.quartiles[0.75] - self.quartiles[0.25]
        self.skewness = None
        self.kurtosis = None
        
    
    # Internal Methods
    def __len__(self):
        return len(self.series)