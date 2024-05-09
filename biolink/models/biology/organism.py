from __future__ import annotations
import logging
from .taxonomy import Taxonomy
from typing import Dict, Any, List

class Organism:
    logger = logging.getLogger("Organism")
    
    def __init__(self):
        # Fields
        self.taxon_id: int
        self.scientific_name: str
        self.common_name: str
        self.taxonomy: Taxonomy
        
        # Constructor
        # N/A
        
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
        return organism
    
    