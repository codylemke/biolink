from typing import List

class AlignmentEntry:
    
    def __init__(self, text: str):
        # Fields
        self.header: str
        self.accession: str
        self.alignment_sequence: str
        self.sequence_map: List[int] = []
        
        # Constructor
        content = text.split('\n')
        self.header = content[0]
        self.accession = self.header.split('|')[1]
        self.alignment_sequence = ''.join(content[1:])
        position = 0
        for character in self.alignment_sequence:
            if character != '-':
                self.sequence_map.append(position)
            position += 1
        
    
    # Internal Methods
    def __len__(self) -> int:
        return len(self.alignment_sequence)
    
    
    # Properties
    @property
    def sequence(self):
        return self.alignment_sequence.replace('-', '')
    
    
    # Public Methods
    def get_alignment_position(self, sequence_position: int):
        return self.sequence_map[sequence_position]
    
    
    def get_residue(self, alignment_position: int):
        return self.alignment_sequence[alignment_position]
    
    
    