import logging
from typing import List

class CodonUsageTable:
    logger = logging.getLogger("Blast")
    
    def __init__(self):
        # Fields
        self.taxid: int
        self.url: str
        self.codons: List[str]
        self.frequency: List[float]
        self.total_number: int
        
        # Constructor
    
    # Internal Methods
    # N/A
    
    
    # Properties
    # N/A
    
    
    # Public Methods
    @staticmethod
    def fetch(taxid: str):
        pass