from typing import List, Dict
from pathlib import Path
import pandas
from . import FastaFile, AminoAcid
from __future__ import annotations

class ProteinAlignment:
    def __init__(self, file_path):
        # Fields
        self.file_path: Path
        self.dataframe: pandas.DataFrame
        
        
        # Constructor
        self.file_path = Path(file_path).resolve()
        # file_extension = self.file_path.suffix
        # match file_extension:
        #     case ".fasta":
        #         ProteinAlignment.parse_fasta(file_path)
        #     case ".clustal":
        #         ProteinAlignment.parse_clustal(file_path)
        #     case ".msf":
        #         ProteinAlignment.parse_msf(file_path)
        #     case ".phylip":
        #         ProteinAlignment.parse_phylip(file_path)
        #     case ".slx":
        #         ProteinAlignment.parse_selex(file_path)
        #     case ".sth":
        #         ProteinAlignment.parse_stockholm(file_path)
        #     case _:
        #         raise Exception(f"Alignment file type is invalid {file_extension}")
        
        
        
    # Internal Methods
    def __len__(self) -> int:
        return len(self.dataframe.iloc[1].tolist())
    
    # Properties
    @property
    def accessions(self) -> List[str]:
        return self.dataframe.columns.tolist()
    
    
    # Public Methods
    @classmethod
    def parse_fasta(cls, file_path:str) -> ProteinAlignment:
        alignment = cls(file_path)
        fasta_file = FastaFile(file_path)
        data = {entry.accession: entry.sequence for entry in fasta_file}
        alignment.dataframe = pandas.DataFrame(data)
        return alignment
    
    @classmethod
    def parse_clustal(cls, file_path:str) -> ProteinAlignment:
        alignment = cls(file_path)
        raise Exception("Not implemented yet")
    
    @classmethod
    def parse_msf(cls, file_path:str) -> ProteinAlignment:
        alignment = cls(file_path)
        raise Exception("Not implemented yet")
    
    @classmethod
    def parse_phylip(cls, file_path:str) -> ProteinAlignment:
        alignment = cls(file_path)
        raise Exception("Not implemented yet")
    
    @classmethod
    def parse_selex(cls, file_path:str) -> ProteinAlignment:
        alignment = cls(file_path)
        raise Exception("Not implemented yet")
    
    @classmethod
    def parse_stockholm(cls, file_path:str) -> ProteinAlignment:
        alignment = cls(file_path)
        raise Exception("Not implemented yet")
    
    def get_aligned_sequence(self, accession: str) -> str:
        return self.dataframe[accession]
    
    def get_sequence(self, accession: str) -> str:
        return self.get_aligned_sequence(accession).replace('-', '')
    
    def get_alignment_position(self, index) -> pandas.Series:
        return self.dataframe.iloc[index]
    
    def get_alignment_region(self, start_index: int, end_index: int) -> pandas.DataFrame:
        return self.dataframe.iloc[start_index:end_index]
    
    def get_alignment_position_distribution(self, index) -> Dict[str, float]:
        position_series = self.get_alignment_position(index)
        entries = len(position_series)
        present_one_letter_codes = set(position_series.to_list())
        distribution = {}
        for one_letter_code in present_one_letter_codes:
            count = (position_series == one_letter_code).sum()
            distribution[one_letter_code] = count / entries
        distribution = dict(sorted(distribution.items(), key=lambda item: item[1]))
        return distribution
    
    # hydrophobicity_ph7_range
    # hydrophobicity_ph7_mean
    # hydrophobicity_ph7_median
    # hydrophobicity_ph7_stdev
    # hydrophobicity_ph2_range
    # hydrophobicity_ph2_mean
    # hydrophobicity_ph2_median
    # hydrophobicity_ph2_stdev
    # pka_range
    # pka_mean
    # pka_median
    # pka_stdev
    # pkb_range
    # pkb_mean
    # pkb_median
    # pkb_stdev
    # pkx_range
    # pkx_mean
    # pkx_median
    # pkx_stdev
    # pi_range
    # pi_mean
    # pi_median
    # pi_stdev
    # van_der_waals_volume_range
    # van_der_waals_volume_median
    # van_der_waals_volume_mean
    # van_der_waals_volume_stdev
    # molecular_weight_range
    # molecular_weight_median
    # molecular_weight_mean
    # molecular_weight_stdev
    # residue_weight_range
    # residue_weight_median
    # residue_weight_mean
    # residue_weight_stdev
    # number_of_residues_present (variability)
    # amino_acid_frequency (for each residue)
    # gap_frequency
    # accessions_with_gaps
    # accessions_without_gaps
    # aromatic_frequency
    # aliphatic_frequency
    # polar_frequency
    # proline_frequency
    # glycine_frequency
    
    # mean
    # median
    # mode
    # range
    # interquartile range
    # variance
    # standard deviation
    # coefficient of variation
    # skewness
    # kurtosis
    
    # consider heatmaps, box plots, histograms, and scatter plots
    # consider trying to get ramachandran data for amino acids
    
    
    
    # Quartiles and intraquartile range?
    # Shannon entropy?
    # Will eventually need to look at evolution of residues in the context of a phylogenetic tree
    