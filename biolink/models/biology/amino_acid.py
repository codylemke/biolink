import logging
import json
from pathlib import Path
from typing import Dict, Any, List, Tuple

file_path = Path(__file__).resolve()

class AminoAcid:
    logger = logging.getLogger("Blast")
    # https://www.sigmaaldrich.com/US/en/technical-documents/technical-article/protein-biology/protein-structural-analysis/amino-acid-reference-chart
    # https://proteinsandproteomics.org/content/free/tables_1/table08.pdf
    initialized = False
    amino_acid_data: Dict[str, Dict[str, Any]]
    one_letter_code_map: Dict[str, str]
    three_letter_code_map: Dict[str, str]
    valid_one_letter_codes: List[str]
    valid_three_letter_codes: List[str]
    
    @classmethod
    def _initialize_class(cls):
        amino_acid_data_path = file_path.parent / "amino_acid.json"
        with amino_acid_data_path.open('r') as file:
            cls.amino_acid_data = json.load(file)
        cls.one_letter_code_map = {key: cls.amino_acid_data[key]["three_letter_code"] for key in cls.amino_acid_data.keys()}
        cls.three_letter_code_map = {value: key for key, value in cls.one_letter_code_map.items()}
        cls.valid_one_letter_codes = list(cls.one_letter_code_map.keys())
        cls.valid_three_letter_codes = list(cls.three_letter_code_map.keys())
    
    def __init__(self, amino_acid_code: str):
        # Fields
        self.one_letter_code: str
    
        # Constructor
        if self.initialized == False:
            AminoAcid._initialize_class()
        self.one_letter_code = self.process_amino_acid_code(amino_acid_code)
        
    
    # Internal Methods
    # N/A
    
    
    # Properties
    @property
    def amino_acid_details(self) -> Dict[str, Any]:
        return AminoAcid.amino_acid_data[self.one_letter_code]
    
    @property
    def name(self) -> str:
        return self.amino_acid_details["name"]
    
    @property
    def three_letter_code(self) -> str:
        return self.amino_acid_details["three_letter_code"]
    
    @property
    def molecular_formula(self) -> str:
        return self.amino_acid_details["molecular_formula"]
    
    @property
    def molecular_weight(self) -> float:
        return self.amino_acid_details["molecular_weight"]
    
    @property
    def residue_formula(self) -> str:
        return self.amino_acid_details["residue_formula"]
    
    @property
    def residue_weight(self) -> float:
        return self.amino_acid_details["residue_weight"]
    
    @property
    def pka(self) -> float:
        return self.amino_acid_details["pka"]
    
    @property
    def pkb(self) -> float:
        return self.amino_acid_details["pkb"]
    
    @property
    def pkx(self) -> float:
        return self.amino_acid_details["pkx"]
    
    @property
    def pi(self) -> float:
        return self.amino_acid_details["pi"]

    @property
    def relative_hydrophobicity_at_ph2(self) -> int:
        return self.amino_acid_details["relative_hydrophobicity_at_ph2"]
    
    @property
    def relative_hydrophobicity_at_ph7(self) -> int:
        return self.amino_acid_details["relative_hydrophobicity_at_ph7"]

    # Darby and Creighton (1993)
    @property
    def van_der_waals_volume(self) -> float:
        return self.amino_acid_details["van_der_waals_volume"]
    
    @property
    def is_acidic(self) -> bool:
        return self.one_letter_code in ['D','E']
    
    @property
    def is_basic(self) -> bool:
        return self.one_letter_code in ['R','K','H']
    
    @property
    def is_charged(self) -> bool:
        return self.is_basic or self.is_acidic
    
    @property
    def is_aromatic(self) -> bool:
        return self.one_letter_code in ['F','W','Y']
    
    @property
    def is_aliphatic(self) -> bool:
        return self.one_letter_code in ['A','I','L','M','V']
    
    @property
    def is_polar(self) -> bool:
        return self.one_letter_code in ['N','C','Q','S','T','Y','D','E','H','K','R']
    
    @property
    def is_hydrophobic(self) -> bool:
        return self.relative_hydrophobicity_at_ph7 > 0
    
    @property
    def is_small(self) -> bool:
        return self.one_letter_code in ['A','G','C','S','T']
    
    @property
    def is_large(self) -> bool:
        return self.one_letter_code in ['F','W','Y','R','H']
    
    @property
    def is_flexible(self) -> bool:
        return self.one_letter_code in ['G','P']
    
    @property
    def can_be_phosphorylated(self) -> bool:
        return self.one_letter_code in ['S','T','Y']
    
    @property
    def can_be_glycosylated(self) -> bool:
        return self.one_letter_code in ['N','S','T','Q']
    
    @property
    def is_proton_acceptor_or_donor(self) -> bool:
        return self.one_letter_code == 'H'
    
    @property
    def can_bind_metal_ions(self) -> bool:
        return self.one_letter_code in ['C','D','E','H']
    
    @property
    def is_bcaa(self) -> bool:
        return self.one_letter_code in ['V','L','I']
    
    @property
    def can_be_ubiquitinated(self) -> bool:
        return self.one_letter_code == 'K'
    
    @property
    def can_form_special_bonds(self) -> bool:
        return self.one_letter_code in ['C', 'S', 'T', 'Y', 'K', 'R', 'D', 'E']
    
    @property
    def can_form_disulfide_bonds(self) -> bool:
        return self.one_letter_code == 'C'
    
    @property
    def in_structural_motifs(self) -> bool:
        return self.one_letter_code in ['C','H','N','K']
    
    @property
    def prefers_alpha_helix(self) -> bool:
        return self.one_letter_code in ['A','L','M','F','H','K']
    
    @property
    def prefers_beta_sheets(self) -> bool:
        return self.one_letter_code in ['V','I','T','Y']
    
    @property
    def is_human_essential(self) -> bool:
        return self.one_letter_code in ['H', 'I', 'L', 'K', 'M', 'F', 'T', 'W', 'V']
    
    @property
    def is_human_conditionally_essential(self) -> bool:
        return self.one_letter_code in ['R', 'C', 'Q', 'Y', 'G', 'P', 'S']
    
    # Public Methods
    @classmethod
    def process_amino_acid_code(cls, code: str, code_output_type:int=1) -> str:
        # Validate Code Output Type
        if code_output_type not in [1, 3]:
            raise Exception(f"Invalid code_output_type argument provided: {code_output_type}. Valid code_output_type: 1 or 3")
        # Validate and Process Code
        if len(code) == 1:
            code_type = 1
            code = code.upper()
            if code not in cls.valid_one_letter_codes:
                raise Exception(f"Invalid one-letter-code argument provided: {code}")
        elif len(code) == 3:
            code_type = 3
            split_code = code.split()
            code = ''.join([split_code[0].upper(), split_code[1].lower(), split_code[2].lower()])
            if code not in cls.valid_three_letter_codes:
                raise Exception(f"Invalid three-letter-code argument provided: {code}")
        else:
            raise Exception(f"Invalid code argument provided: {code}")
        # Return Desired Value
        if code_type == 1 and code_output_type == 1:
            return code
        elif code_type == 1 and code_output_type == 3:
            return cls.one_letter_code_map[code]
        elif code_type == 3 and code_output_type == 1:
            return cls.three_letter_code_map[code]
        elif code_type == 3 and code_output_type == 3:
            return code
        else:
            raise Exception(f"Invalid arguments: code_type: {code_type}, code_output_type: {code_output_type}")
