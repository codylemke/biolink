from typing import List
from .blast_hit import BlastHit


class BlastResults:
    def __init__(self, input_file: str):
        # Fields
        self.metadata = {}
        self.hits: List[BlastHit] = []
        
        # Constructor
        with open(input_file, 'r') as file:
            header_lines = []
            for line in file:
                if line.startswith('#'):
                    self._parse_header_line(line[1:])
                elif line.isspace():
                    continue
                else:
                    self.hits.append(BlastHit(line))
                    break
            for line in file:
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
    # N/A
