from __future__ import annotations
import logging
from typing import List, Dict, Any
from .organism import Organism
from .amino_acid import AminoAcid

class Protein:
    logger = logging.getLogger("Protein")
    
    def __init__(self):
        # Fields
        self.uniprot_id: str
        self.uniprot_entry_type: str
        self.uniprot_secondary_accessions: List[str]
        self.uniprotkb_id = str
        self.embl_id: str
        self.refseq_id: str
        self.alphafold_id: str
        self.kegg_id: str
        self.interpro_ids: List[str] = []
        self.pfam_id: str
        self.supfam_id: str
        self.sequence: str
        self.uniparc_id: str
        self.organism: Organism
        
        # Constructor
        # N/A
    
    # Internal Methods
    # N/A
    
    # Properties
    @property
    def amino_acids(self) -> List[AminoAcid]:
        return [AminoAcid(amino_acid) for amino_acid in self.sequence]
    
    
    # Public Methods
    @classmethod
    def parse_uniprotkb_details(cls, details: Dict[str, Any]) -> Protein:
        protein = cls()
        protein.uniprot_id = details["primaryAccession"]
        protein.uniprot_entry_type = details["entryType"]
        protein.uniprot_secondary_accessions = details.get("secondaryAccessions")
        protein.uniprotkb_id = details["uniProtkbId"]
        for cross_reference in details["uniProtKBCrossReferences"]:
            if cross_reference["database"] == "EMBL":
                protein.embl_id = cross_reference["id"]
            elif cross_reference["database"] == "RefSeq":
                protein.refseq_id = cross_reference["id"]
            elif cross_reference["database"] == "AlphaFoldDB":
                protein.alphafold_id = cross_reference["id"]
            elif cross_reference["database"] == "KEGG":
                protein.kegg_id = cross_reference["id"]
            elif cross_reference["database"] == "InterPro":
                protein.interpro_ids.append(cross_reference["id"])
            elif cross_reference["database"] == "Pfam":
                protein.pfam_id = cross_reference["id"]
            elif cross_reference["database"] == "SUPFAM":
                protein.supfam_id = cross_reference["id"]
        protein.sequence = details["sequence"]["value"]
        protein.uniparc_id = details.get("uniParcId")
        protein.organism = Organism.parse_uniprot_json(details["organism"])
        return protein
    
    @classmethod
    def parse_uniref_details(cls, details: Dict[str, Any]) -> Protein:
        protein = cls()
        protein.uniprot_id = details["primaryAccession"]
        protein.uniprot_entry_type = details["entryType"]
        protein.uniprot_secondary_accessions = details.get("secondaryAccessions")
        protein.uniprotkb_id = details["uniProtkbId"]
        for cross_reference in details["uniProtKBCrossReferences"]:
            if cross_reference["database"] == "EMBL":
                protein.embl_id = cross_reference["id"]
            elif cross_reference["database"] == "RefSeq":
                protein.refseq_id = cross_reference["id"]
            elif cross_reference["database"] == "AlphaFoldDB":
                protein.alphafold_id = cross_reference["id"]
            elif cross_reference["database"] == "KEGG":
                protein.kegg_id = cross_reference["id"]
            elif cross_reference["database"] == "InterPro":
                protein.interpro_ids.append(cross_reference["id"])
            elif cross_reference["database"] == "Pfam":
                protein.pfam_id = cross_reference["id"]
            elif cross_reference["database"] == "SUPFAM":
                protein.supfam_id = cross_reference["id"]
        protein.sequence = details["sequence"]["value"]
        protein.uniparc_id = details.get("uniParcId")
        protein.organism = Organism.parse_uniprot_json(details["organism"])
        return protein
    
    @classmethod
    def parse_uniparc_details(cls, details: Dict[str, Any]) -> Protein:
        protein = cls()
        protein.uniprot_id = details["primaryAccession"]
        protein.uniprot_entry_type = details["entryType"]
        protein.uniprot_secondary_accessions = details.get("secondaryAccessions")
        protein.uniprotkb_id = details["uniProtkbId"]
        for cross_reference in details["uniProtKBCrossReferences"]:
            if cross_reference["database"] == "EMBL":
                protein.embl_id = cross_reference["id"]
            elif cross_reference["database"] == "RefSeq":
                protein.refseq_id = cross_reference["id"]
            elif cross_reference["database"] == "AlphaFoldDB":
                protein.alphafold_id = cross_reference["id"]
            elif cross_reference["database"] == "KEGG":
                protein.kegg_id = cross_reference["id"]
            elif cross_reference["database"] == "InterPro":
                protein.interpro_ids.append(cross_reference["id"])
            elif cross_reference["database"] == "Pfam":
                protein.pfam_id = cross_reference["id"]
            elif cross_reference["database"] == "SUPFAM":
                protein.supfam_id = cross_reference["id"]
        protein.sequence = details["sequence"]["value"]
        protein.uniparc_id = details.get("uniParcId")
        protein.organism = Organism.parse_uniprot_json(details["organism"])
        return protein
    