from typing import List

class Protein:
    def __init__(self):
        self.uniprot_id: str
        self.uniprot_secondary_accessions: str
        self.embl_id: str
        self.refseq_id: str
        self.alphafold_id: str
        self.keqq_id: str
        self.interpro_ids: List[str]
        self.pfam: str
        self.supfam: str
        
        self.sequence: str
        self.uniParcId: str
        
    @staticmethod
    def fetch(uniprot_id: str):
        pass