from typing import Dict, List
import pandas as pd

class StringDescriptiveStatistics:
    
    def __init__(self, data: List[str]):
        # Fields
        self.data: pd.Series
        self.count: int
        self.mode: str
        self.frequency: Dict[str: float]
    
        # Constructor
        self.data = pd.Series(data)
        self.count = len(self.data)
        self.mode = self.data.mode()
        self.frequency = {i: data.count(i) for i in set(data)}
        