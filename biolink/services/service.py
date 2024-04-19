import json
from biolink.models import FastaFile, Protein
from biolink.integrations import UniprotClient
from typing import List, Dict

class Service:
    
    def __init__(self):
        # Fields
        
        # Constructor
        pass
    
    # Internal Methods
    
    # Properties
    # N/A
    
    # Public Methods
    def accession_file_to_accessions(file: str) -> List[str]:
        with open(file, 'r') as file:
            accessions = [line.strip() for line in file if line.strip()]
        return accessions
    
    async def accessions_to_fasta_file(accessions: List[str], file: str) -> FastaFile:
        uniprot_client = UniprotClient()
        fasta_entries = await uniprot_client.get_entries(accessions)
        fasta_file = FastaFile(fasta_entries)
        fasta_file.save(file)
        return fasta_file
    
    async def accessions_to_proteins(accessions: List[str]) -> List[Protein]:
        uniprot_client = UniprotClient()
        protein_data = await uniprot_client.get_entries(accessions, outfmt="json")
        # Get Organism Data
        proteins = [Protein.parse_uniprotkb_details(entry) for entry in json.loads(protein_data)]
        return proteins
    
    
    
    async def sort_fasta_entries_by_kingdom(fasta_file: FastaFile) -> Dict[List[Protein]]:
        sorted_fasta_files = {}
        
    