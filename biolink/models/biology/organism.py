from .taxonomy import Taxonomy
from typing import Dict, Any

class Organism:
    def __init__(self):
        self.scientific_name: str
        self.common_name: str
        self.taxon_id: int
        self.lineage: Taxonomy
        
    def parse_uniprot_json(self, json: Dict[str, Any]):
        self.scientific_name = json['scientificName']
        self.common_name = json['commonName']
        self.taxon_id = json['taxonId']
        self.lineage = Taxonomy.fetch(json['taxonId'])