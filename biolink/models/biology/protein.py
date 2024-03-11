from typing import List
from . import AminoAcid

class Protein:
    def __init__(self, sequence):
        # Fields
        self.uniprot_id: str
        self.uniprot_secondary_accessions: str
        self.embl_id: str
        self.refseq_id: str
        self.alphafold_id: str
        self.keqq_id: str
        self.interpro_ids: List[str]
        self.pfam: str
        self.supfam: str
        
        self.sequence: List[AminoAcid] = []
        self.uniParcId: str
            
        # Constructor
        for character in sequence:
            self.sequence.append(AminoAcid(character))
        
    @staticmethod
    def get_details(uniprot_id: str):
        pass