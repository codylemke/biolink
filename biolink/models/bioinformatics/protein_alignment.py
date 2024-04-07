from __future__ import annotations
import logging
from typing import List, Dict, Any
from biolink.models.bioinformatics.fasta_file import FastaFile
from biolink.models.bioinformatics.protein_alignment_position_profile import ProteinAlignmentPositionProfile

class ProteinAlignment:
    logger = logging.getLogger("ProteinAlignment")
    
    def __init__(self):
        # Fields
        self.file: FastaFile
        self.data: Dict[str, str]
        
        # Constructor
        self.data = {}
        
        
    # Internal Methods
    def __len__(self) -> int:
        return len(self.data)
    
    
    # Properties
    @property
    def accessions(self) -> List[str]:
        return self.data.keys()
    
    @property
    def sequences(self) -> List[str]:
        return self.data.values()
    
    
    # Public Methods
    @classmethod
    def parse_fasta(cls, file_path:str) -> ProteinAlignment:
        alignment = cls()
        alignment.file = FastaFile.parse_file(file_path)        
        for entry in alignment.file.entries:
            alignment.data[entry.accession] = entry.sequence
        return alignment
    
    @classmethod
    def parse_clustal(cls, file_path:str) -> ProteinAlignment:
        alignment = cls()
        raise Exception("Not implemented yet")
    
    @classmethod
    def parse_msf(cls, file_path:str) -> ProteinAlignment:
        alignment = cls()
        raise Exception("Not implemented yet")
    
    @classmethod
    def parse_phylip(cls, file_path:str) -> ProteinAlignment:
        alignment = cls()
        raise Exception("Not implemented yet")
    
    @classmethod
    def parse_selex(cls, file_path:str) -> ProteinAlignment:
        alignment = cls()
        raise Exception("Not implemented yet")
    
    @classmethod
    def parse_stockholm(cls, file_path:str) -> ProteinAlignment:
        alignment = cls()
        raise Exception("Not implemented yet")
    
    # Instance Methods
    def get_alignment_index(self, accession: str, amino_acid: str, amino_acid_position: int) -> int:
        count = 0
        for index, char in enumerate(self.data[accession]):
            if char != '-':
                if count == amino_acid_position - 1:
                    if char == amino_acid:
                        return index
                    else:
                        raise Exception(f"{amino_acid} was expected at amino acid position {amino_acid_position} but {char} was found.")
                count += 1
        return None
    
    def get_alignment_sequence(self, accession: str) -> str:
        return self.data[accession]
    
    def get_protein_sequence(self, accession: str) -> str:
        return self.get_alignment_sequence(accession).replace('-', '')
    
    def get_position_alignment(self, position: int) -> List[str]:
        return [sequence[position - 1] for sequence in self.sequences]
    
    def get_alignment_position_profile(self, position: int) -> ProteinAlignmentPositionProfile:
        return ProteinAlignmentPositionProfile(self.get_position_alignment(position))
        
    def get_alignment_profile(self) -> List[ProteinAlignmentPositionProfile]:
        alignment_profile = []
        sequence_length = len(next(iter(self.sequences)))
        for index in range(sequence_length):
            alignment_profile.append(self.get_alignment_position_profile(index + 1))
        return alignment_profile
    
    # def save_alignment_profile(self, file_path: str) -> None:
    #     with open(file_path, 'w') as file:
    #         for position in self.get_alignment_profile():
    #             file.write