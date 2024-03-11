from biolink.models.math import NumericalDescriptiveStatistics
import numpy as np
from scipy import stats

class NumericalInferentialStatistics:
    
    def __init__(self, set_1: NumericalDescriptiveStatistics, set_2: NumericalDescriptiveStatistics):
        # Fields
        self.mean_difference: float
        self.t_test: bool
        self.correlation_coefficient: float
        self.cohens_d: float
        self.regresssion: None
        
        # Constructor
        self.mean_difference = set_1.mean - set_2.mean
        self.t_test = stats.ttest_ind(set_1, set_2)
        self.correlation_coefficient = np.corrcoef(set_1, set_2)[0, 1]
        self.cohens_d = (np.mean(set_1) - np.mean(set_2)) / (np.sqrt((np.std(set_1) ** 2 + np.std(set_2) **2) / 2))
        