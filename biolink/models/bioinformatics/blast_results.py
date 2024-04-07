from __future__ import annotations
from typing import List
from .blast_hit import BlastHit

class BlastResults:
    
    def __init__(self, blast_output: str):
        # Fields
        self.metadata
        self.hits: List[BlastHit]
        
        # Constructor
        self.metadata = {}
        self.hits = []
        for line in blast_output.splitlines():
            if line.startswith('#'):
                self._parse_header_line(line[1:])
            elif line.isspace():
                continue
            else:
                self.hits.append(BlastHit(line))
    
    
    # Internal Methods
    def _parse_header_line(self, header: str):
        key, value = header.strip().split(': ', 1)
        self.metadata[key] = value
    
    
    # Properties
    @property
    def hit_accessions(self):
        return [hit.subject_accession for hit in self.hits]
    
    
    # Public Methods
    @classmethod
    def parse_file(cls, file: str) -> BlastResults:
        with open(file, 'r') as file:
            blast_results = cls(file.read())
        return blast_results