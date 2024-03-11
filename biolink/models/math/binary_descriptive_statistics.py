from typing import List
from __future__ import annotations
import pandas as pd
from biolink.models.math import BinaryInferentialStatistics

class BinaryDescriptiveStatistics:
    
    def __init__(self, data: List[bool]):
        # Fields
        self.data: pd.Series
        self._count: int
        self._count_true: int
        self._count_false: int
        self._proportion_true: float
        
        # Constructor
        self.data = pd.Series(data)
        
    
    # Internal Methods
    def __len__(self):
        return self.count
    
    
    # Properties
    @property
    def count(self):
        if self._count == None:
            self._count = len(self.data)
        return self._count
    
    @property
    def count_true(self):
        if self._count_true == None:
            self._count_true = sum(self.data)
        return self._count_true
    
    @property
    def count_false(self):
        if self._count_false == None:
            self._count_false = len(self.data) - sum(self.data)
        return self._count_false
    
    @property
    def proportion_true(self):
        if self._proportion_true == None:
            self._proportion_true = sum(self.data) - len(self.data)
        return self._proportion_true
    
    # Public Methods
    def compare(self, other: BinaryDescriptiveStatistics) -> BinaryInferentialStatistics:
        return BinaryInferentialStatistics(self, other)