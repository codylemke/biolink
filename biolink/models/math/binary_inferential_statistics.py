import logging
import numpy as np
from scipy import stats
from biolink.models.math import BinaryDescriptiveStatistics

class BinaryInferentialStatistics:
    logger = logging.getLogger("BinaryInferentialStatistics")
    
    def __init__(self, stats_1: BinaryDescriptiveStatistics, stats_2: BinaryDescriptiveStatistics):
        # Fields
        self.proportional_difference: float
        self.chi_square_test: None
        self.z_stat: None
        self.odds_ratio: None
        self.phi_coefficient: None
        
        # Constructor
        n1, n2 = len(stats_1), len(stats_2)
        prop1, prop2 = np.mean(stats_1), np.mean(stats_2)
        self.prop_diff = prop1 - prop2
        self.z_stat, self.z_pvalue = stats.proportions_ztest([sum(stats_1), sum(stats_2)], [n1, n2])
        self.odds_ratio, self.or_pvalue = stats.fisher_exact(self.z_stat ** 2 / (n1 + n2))
        self.phi_coefficient = np.sqrt(self.z_stat ** 2 / (n1 + n2))
    