import logging
from scipy import stats
import pandas as pd
import numpy as np
from biolink.models.math import StringDescriptiveStatistics

class StringInferentialStatistics:
    logger = logging.getLogger("StringInferentialStatistics")
    
    def __init__(self, set_1: StringDescriptiveStatistics, set_2: StringDescriptiveStatistics):
        # Fields
        self.chi_square: None
        self.p: None
        self.dof: None
        self.contingency_table: None
        self.cramers_v: None
        
        # Constructors
        self.contingency_table = pd.crosstab(set_1, set_2)
        self.chi_square = self.p, self.dof, _ = stats.chi2_contingency(self.contingency_table)
        self.cramers_v = np.sqrt(self.chi_square / (len(set_1) + len(set_2)))