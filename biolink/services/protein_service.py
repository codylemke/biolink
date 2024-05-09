import json
from typing import List, Dict
from biolink.models import Protein, FastaFile, ProteinAlignment, Taxonomy
from biolink.integrations import UniprotClient, EntrezClient, ClustalO, Mafft
from lxml import etree

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
        proteins = [Protein.parse_uniprotkb_details(entry) for entry in json.loads(protein_data)]
        fasta_data = await uniprot_client.get_entries(accessions, outfmt="fasta")
        fasta_data_file = FastaFile(fasta_data)
        ordered_accessions = [protein.uniprot_id for protein in proteins]
        for protein, fasta_entry in zip(proteins, fasta_data_file):
            if protein.uniprot_id == fasta_entry.accession:
                protein.fasta_file = FastaFile(str(fasta_entry))
            else:
                protein_index = ordered_accessions.index(fasta_entry.accession)
                proteins[protein_index].fasta_file = FastaFile(str(fasta_entry))
        entrez_client = EntrezClient()
        taxids = [protein.organism.taxon_id for protein in proteins]
        organism_data = await entrez_client.efetch("taxonomy", ','.join(taxids))
        root = etree.fromstring(organism_data)
        organism_xmls = []
        for taxon in root.findall(".//Taxon"):
            taxon_str = etree.tostring(taxon, pretty_print=True, encoding='unicode')
            organism_xmls.append(taxon_str)
        organisms = [Taxonomy.from_entrez_xml(organism_xml) for organism_xml in organism_xmls]
        for protein, organism in zip(proteins, organisms):
            if protein.organism.taxon_id == organism.id:
                protein.organism = organism
            else:
                protein_index = taxids.index(organism.id)
                proteins[protein_index].organism = organism
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
        fasta_strings = [str(protein.fasta_file) for protein in proteins]
        fasta_file = FastaFile('\n'.join(fasta_strings))
        fasta_file.save(file)
        return fasta_file
    
    async def align_proteins_clustalo(proteins: List[Protein], working_directory: str, aligment_name: str) -> ProteinAlignment:
        for protein in proteins:
            protein.fasta_file
        alignment = await ClustalO.align()
        pass
    
    async def align_proteins_mafft(proteins: List[Protein], file: str) -> ProteinAlignment:
        pass
    