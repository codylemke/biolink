from __future__ import annotations
from typing import List

class BinaryDescriptiveStatistics:
    
    def __init__(self, data: List[bool]):
        # Fields
        self.data: List[bool]
        self.count: int
        self.count_true: int
        self.count_false: int
        self.proportion_true: float
        
        # Constructor
        self.data = data
        self.count = len(data)
        self.count_true = sum(data)
        self.count_false = self.count - self.count_true
        self.proportion_true = self.count_true / self.count
        
    
    # Internal Methods
    def __len__(self) -> int:
        return self.count
    
    
    # Properties
    # N/A
    
    # Public Methods
    # N/A