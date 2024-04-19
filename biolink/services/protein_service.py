import json
from typing import List, Dict
from biolink.models import Protein, FastaFile, ProteinAlignment
from biolink.integrations import UniprotClient

class ProteinService:
    
    def __init__(self):
        # Fields
        
        # Constructor
        pass
    
    # Internal Methods
    async def _uniprotkb_accessions_to_proteins():
        pass
    
    async def _uniref_accessions_to_proteins():
        pass
    
    async def _uniparc_accessions_to_proteins():
        pass
    
    # Properties
    # N/A
    
    # Public Methods
    async def accessions_to_proteins(accessions: List[str]) -> List[Protein]:
        uniprot_client = UniprotClient()
        protein_data = await uniprot_client.get_entries(accessions, outfmt="json")
        # Get Fasta Data
        # Get Organism Data
        proteins = [Protein.parse_uniprotkb_details(entry) for entry in json.loads(protein_data)]
        return proteins
    
    
    async def sort_proteins_by_kingdom(proteins: List[Protein]) -> Dict[List[Protein]]:
        sorted_proteins = {}
        for protein in proteins:
            kingdom = protein.organism.taxonomy["Kingdom"]
            if kingdom not in sorted_proteins.keys():
                sorted_proteins[kingdom] = []
            sorted_proteins[kingdom].append(protein)
        return sorted_proteins
    
    
    async def proteins_to_fasta_file(proteins: List[Protein], file: str) -> FastaFile:
        pass
    
    async def align_proteins(proteins: List[Protein], file: str) -> ProteinAlignment:
        pass
    
    