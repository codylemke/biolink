from typing import List, Any, Tuple
from numpy.typing import NDArray
import numpy as np
from scipy import stats

class NumericalDescriptiveStatistics:
    
    def __init__(self, data: list[float]):
        # Fields
        self.data = NDArray[np.float_]
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
        self.kurtosis_excess: float
        
        # Constructor
        self.data = np.array(data)
        self.count = len(data)
        self.min = np.min(self.data)
        self.max = np.max(self.data)
        self.sum = np.sum(self.data)
        self.mean = np.mean(self.data)
        self.median = np.median(self.data)
        self.mode = stats.mode(self.data)
        self.standard_deviation = np.std(self.data)
        self.variance = np.var(self.data)
        self.range = self.max - self.min
        q1 = np.percentile(self.data, 25)
        q2 = np.percentile(self.data, 50)
        q3 = np.percentile(self.data, 75)
        self.quartiles = [q1, q2, q3]
        self.interquartile_range = q3 - q1
        self.skewness = stats.skew(data)
        self.kurtosis = stats.kurtosis(data)
        self.kurtosis = stats.kurtosis(data, fisher=False)
        
    
    # Internal Methods
    def __len__(self):
        return self.count
    
    # Properties
    # N/A
    
    # Public Methods
    # N/A