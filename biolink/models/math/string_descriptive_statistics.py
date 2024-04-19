import logging
from typing import Dict, List

class StringDescriptiveStatistics:
    logger = logging.getLogger("StringDescriptiveStatistics")
    
    def __init__(self, data: List[str]):
        # Fields
        self.data: List[str]
        self.count: int
        self.mode: str
        self.frequency: Dict[str: float]
    
        # Constructor
        self.data = data
        self.count = len(self.data)
        #self.mode = np.array(self.data).mode()
        self.frequency = {i: data.count(i) for i in set(data)}
        