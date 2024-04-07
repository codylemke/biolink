from __future__ import annotations
from .taxonomy import Taxonomy
from typing import Dict, Any, List

class Organism:
    
    def __init__(self):
        # Fields
        self.taxon_id: int
        self.scientific_name: str
        self.common_name: str
        self.taxonomy_list = List[str]
        self.taxonomy: Taxonomy
        
        # Constructor
        # self.taxon_id = taxon_id
        # self.taxonomy = Taxonomy.fetch(taxon_id)
        
    # Internal Methods
    # N/A
    
    # Properties
    # N/A
    
    # Public Methods
    @classmethod
    def parse_uniprot_json(cls, json: Dict[str, Any]) -> Organism:
        organism = cls()
        organism.taxon_id = json["taxonId"]
        organism.scientific_name = json["scientificName"]
        organism.common_name = json.get("commonName")
        organism.taxonomy_list = json["lineage"]
        return organism
    
    
    def fetch_taxonomy(self) -> None:
        self.taxonomy = Taxonomy.fetch(self.taxon_id)