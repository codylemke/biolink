# from typing import List, Dict
# import pandas as pd
# from biolink.models.biology import AminoAcid

# class AlignmentPositionProfile:
#     def __init__(self, series: pd.Series[AminoAcid]):
#         # Fields
#         self.series: pd.Series
#         self.count: int
#         self.mode: str
#         self.gap_count: int
#         self.observed_residues: List[str]
#         self.diversity: float # Shannon Entropy
#         self.frequencies: Dict[str, float]
#         self.hydrophobicity_ph7_statistics: DescriptiveStatistics
#         self.hydrophobicity_ph2_statistics: DescriptiveStatistics
#         self.pka_statistics: DescriptiveStatistics
#         self.pkb_statistics: DescriptiveStatistics
#         self.pkx_statistics: DescriptiveStatistics
#         self.pi_statistics: DescriptiveStatistics
#         self.van_der_waals_volume_statistics: DescriptiveStatistics
#         self.molecular_weight_statistics: DescriptiveStatistics
#         self.residue_weight_statistics: DescriptiveStatistics    
        
#         # Constructor
#         self.series = series
#         self.count = len(series)
#         self.mode = series.mode()
#         self.gap_count = series.str.count('-')
#         self.observed_residues = list(series.unique())
#         for residue in self.observed_residues:
#             residue = AminoAcid(residue)
#             residue_count = series.str.count(residue.one_letter_code)
#             frequency = residue_count / self.count
#             self.frequencies[residue] = frequency
#         molecular_weights = series.apply(lambda x: x.molecular_weight)
#         residue_weights = series.apply(lambda x: x.residue_weight)
#         self.pka_statistics(series.apply(lambda x: x.pka))
#         self.pkb_statistics(series.apply(lambda x: x.pkb))
#         self.pkx_statistics = DescriptiveStatistics(series.apply(lambda x: x.pkx))
#         self.pi_statistics = DescriptiveStatistics(series.apply(lambda x: x.pi))
#         self.hydrophobicity_ph2_statistics = DescriptiveStatistics(series.apply(lambda x: x.relative_hydrophobicities_at_ph2))
#         self.hydrophobicity_ph7_statistics = DescriptiveStatistics(series.apply(lambda x: x.relative_hydrophobicities_at_ph7))
#         self.van_der_waals_volume_statistics = DescriptiveStatistics(series.apply(lambda x: x.van_der_waals_volume))
        
#         is_acidics = series.apply(lambda x: x.is_acidic)
#         is_basics = series.apply(lambda x: x.is_basic)
#         is_chargeds = series.apply(lambda x: x.is_charged)
#         is_aromatics = series.apply(lambda x: x.is_aromatic)
#         is_aliphatics = series.apply(lambda x: x.is_aliphatic)
#         is_polars = series.apply(lambda x: x.is_polar)
#         is_hydrophobics = series.apply(lambda x: x.is_hydrophobic)
#         is_smalls = series.apply(lambda x: x.is_small)
#         is_larges = series.apply(lambda x: x.is_large)
#         is_flexibles = series.apply(lambda x: x.is_flexible)
#         can_be_phosphorylateds = series.apply(lambda x: x.can_be_phosphorylated)
#         can_be_glycosylated = series.apply(lambda x: x.can_be_glycosylated)
#         is_protein_acceptor_or_donors = series.apply(lambda x: x.is_protein_acceptor_or_donors)
#         can_bind_metal_ions = series.apply(lambda x: x.can_bind_metal_ions)
#         is_bcaas = series.apply(lambda x: x.is_bcaa)
#         can_be_ubiquinateds = series.apply(lambda x: x.can_be_ubiquinated)
#         can_form_special_bonds = series.apply(lambda x: x.can_form_special_bonds)
#         involved_in_disulfide_bonds = series.apply(lambda x: x.involved_in_disulfide_bonds)
#         prefers_alpha_helix = series.apply(lambda x: x.prefers_alpha_helix)
#         prefers_beta_sheets = series.apply(lambda x: x.prefers_beta_sheets)
#         in_structural_motifs = series.apply(lambda x: x.in_structural_motifs)            
        
        
#     def calculate_frequencies(self):
#         pass
        