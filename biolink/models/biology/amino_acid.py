import json
from pathlib import Path
from typing import Dict, Any, List, Tuple

file_path = Path(__file__).resolve()

class AminoAcid:
    # https://www.sigmaaldrich.com/US/en/technical-documents/technical-article/protein-biology/protein-structural-analysis/amino-acid-reference-chart
    amino_acid_data: Dict[str, Dict[str, Any]] = None
    one_letter_code_map: Dict[str, str] = None
    three_letter_code_map: Dict[str, str] = None
    valid_one_letter_codes: List[str] = None
    valid_three_letter_codes: List[str] = None
    
    def __init__(self, amino_acid_code: str):
        # Fields
        self.one_letter_code: str
        
        # Constructor
        self.one_letter_code = self.process(amino_acid_code, 1)
        
    
    # Internal Methods
    # N/A
    
    
    # Properties
    @property
    def amino_acid_data(self) -> Dict[str, Any]:
        return AminoAcid.amino_acid_data[self.one_letter_code]
    
    @property
    def name(self) -> str:
        return self.amino_acid_data["name"]
    
    @property
    def three_letter_code(self) -> str:
        return self.amino_acid_data["three_letter_code"]
    
    @property
    def molecular_formula(self) -> str:
        return self.amino_acid_data["molecular_formula"]
    
    @property
    def molecular_weight(self) -> float:
        return self.amino_acid_data["molecular_weight"]
    
    @property
    def residue_formula(self) -> str:
        return self.amino_acid_data["residue_formula"]
    
    @property
    def residue_weight(self) -> float:
        return self.amino_acid_data["residue_weight"]
    
    @property
    def pka(self) -> float:
        return self.amino_acid_data["pka"]
    
    @property
    def pkb(self) -> float:
        return self.amino_acid_data["pkb"]
    
    @property
    def pkx(self) -> float:
        return self.amino_acid_data["pkx"]
    
    @property
    def pi(self) -> float:
        return self.amino_acid_data["pi"]
    
    @property
    def property(self) -> str:
        return self.amino_acid_data["property"]

    @property
    def relative_hydrophobicity_at_ph2(self) -> int:
        return self.amino_acid_data["relative_hydrophobicity_at_ph2"]
    
    @property
    def relative_hydrophobicity_at_ph7(self) -> int:
        return self.amino_acid_data["relative_hydrophobicity_at_ph7"]

    # Darby and Creighton (1993)
    @property
    def van_der_waals_volume(self) -> float:
        return self.amino_acid_data["van_der_waals_volume"]

    
    # Public Methods   
    @classmethod
    def process_code(cls, code: str, code_output_type:int=1) -> str:
        # Validate Code Output Type
        if code_output_type not in [1, 3]:
            raise Exception(f"Invalid code_output_type argument provided: {code_output_type}. Valid code_output_type: 1 or 3")
        # Validate and Process Code
        if len(code == 1):
            code_type = 1
            code = code.upper()
            if code not in cls.valid_one_letter_codes:
                raise Exception(f"Invalid one-letter-code argument provided: {code}")
        elif len(code == 3):
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
        

# Module Initialization
if AminoAcid.amino_acid_data is None:
    amino_acid_data_path = file_path.parent / "amino_acid.json"
    with amino_acid_data_path.open('r') as file:
        AminoAcid.amino_acid_data = json.load(file)
    AminoAcid.one_letter_code_map = {key: AminoAcid.amino_acid_data[key]["three_letter_code"] for key in AminoAcid.amino_acid_data.keys()}
    AminoAcid.three_letter_code_map = {value: key for key, value in AminoAcid.one_letter_code_map}
    AminoAcid.valid_one_letter_code = [code for code in AminoAcid.one_letter_code_map.keys()]
    AminoAcid.valid_three_letter_code = [code for code in AminoAcid.three_letter_code_map.keys()]
    