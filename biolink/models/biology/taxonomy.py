from __future__ import annotations
import logging
from typing import List, Dict
from lxml import etree

class Taxonomy:
    logger = logging.getLogger("Taxonomy")
    
    def __init__(self):
        # Fields
        self.scientific_name: str
        self.other_names: List[str]
        self.parent: str
        self.rank: str
        self.division: str
        self.genetic_code: int
        self.mitochondrial_genetic_code: int
        self.lineage = Dict[str, str]
        
        # Constructor
        self.other_names = []
        self.lineage = {}
    
    # Internal Methods
    # N/A
    
    # Properties
    # N/A
    
    # Public Methods
    @classmethod
    def from_entrez_xml(cls, xml: str) -> Taxonomy:
        obj = cls()
        root = etree.fromstring(xml)
        taxon = root.find('Taxon')
        if taxon is not None:
            obj.scientific_name = taxon.findtext('ScientificName', default="")
            obj.parent = taxon.findtext('ParentTaxId', default="")
            obj.rank = taxon.findtext('Rank', default="")
            obj.division = taxon.findtext('Division', default="")
            obj.genetic_code = int(taxon.find('.//GeneticCode/GCId').text if taxon.find('.//GeneticCode/GCId') is not None else 0)
            obj.mitochondrial_genetic_code = int(taxon.find('.//MitoGeneticCode/MGCId').text if taxon.find('.//MitoGeneticCode/MGCId') is not None else 0)
            other_names = taxon.find('OtherNames')
            if other_names is not None:
                for synonym in other_names.findall('Synonym'):
                    obj.other_names.append(synonym.text)
            for lineage_taxon in taxon.findall('.//LineageEx/Taxon'):
                rank = lineage_taxon.findtext('Rank')
                name = lineage_taxon.findtext('ScientificName')
                if rank and name:
                    obj.lineage[rank] = name
        return obj