from typing import List

class CodonUsageTable:
    def __init__(self):
        self.taxid: int
        self.url: str
        self.codons: List[str]
        self.frequency: List[float]
        self.total_number: int
    
    @staticmethod
    def fetch(taxid: str):
        pass