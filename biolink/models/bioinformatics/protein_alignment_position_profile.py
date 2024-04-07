from typing import List
from biolink.models.biology.amino_acid import AminoAcid
from biolink.models.math import NumericalDescriptiveStatistics, BinaryDescriptiveStatistics

class ProteinAlignmentPositionProfile:
    
    def __init__(self, alignment_position: List[str]):
        # Fields
        self.molecular_weight_statistics: NumericalDescriptiveStatistics
        self.residue_weight_statistics: NumericalDescriptiveStatistics
        self.pka_statistics: NumericalDescriptiveStatistics
        self.pkb_statistics: NumericalDescriptiveStatistics
        self.pkx_statistics: NumericalDescriptiveStatistics
        self.pi_statistics: NumericalDescriptiveStatistics
        self.relative_hydrophobicity_at_ph2_statistics: NumericalDescriptiveStatistics
        self.relative_hydrophobicity_at_ph7_statistics: NumericalDescriptiveStatistics
        self.van_der_waals_volume_statistics: NumericalDescriptiveStatistics
        self.is_acidic_statistics: BinaryDescriptiveStatistics
        self.is_basic_statistics: BinaryDescriptiveStatistics
        self.is_charged_statistics: BinaryDescriptiveStatistics
        self.is_aromatic_statistics: BinaryDescriptiveStatistics
        self.is_aliphatc_statistics: BinaryDescriptiveStatistics
        self.is_polar_statistics: BinaryDescriptiveStatistics
        self.is_hydrophobic_statistics: BinaryDescriptiveStatistics
        self.is_small_statistics: BinaryDescriptiveStatistics
        self.is_large_statistics: BinaryDescriptiveStatistics
        self.is_flexible_statistics: BinaryDescriptiveStatistics
        self.can_be_phosphorylated_statistics: BinaryDescriptiveStatistics
        self.can_be_glycosylated_statistics: BinaryDescriptiveStatistics
        self.is_proton_acceptor_or_donor_statistics: BinaryDescriptiveStatistics
        self.can_bind_metal_ions_statistics: BinaryDescriptiveStatistics
        self.is_bcaa_statistics: BinaryDescriptiveStatistics
        self.can_be_ubiquitinated_statistics: BinaryDescriptiveStatistics
        self.can_form_special_bonds_statistics: BinaryDescriptiveStatistics
        self.can_form_disulfide_bonds_statistics: BinaryDescriptiveStatistics
        self.in_structural_motifs_statistics: BinaryDescriptiveStatistics
        
        # Constructor
        alignment_amino_acids = [AminoAcid(amino_acid_code) for amino_acid_code in alignment_position if amino_acid_code not in ['-', 'X']]
        self.molecular_weight_statistics = NumericalDescriptiveStatistics([amino_acid.molecular_weight for amino_acid in alignment_amino_acids])
        self.residue_weight_statistics = NumericalDescriptiveStatistics([amino_acid.residue_weight for amino_acid in alignment_amino_acids])
        self.pka_statistics = NumericalDescriptiveStatistics([amino_acid.pka for amino_acid in alignment_amino_acids])
        self.pkb_statistics = NumericalDescriptiveStatistics([amino_acid.pkb for amino_acid in alignment_amino_acids])
        pkx_values = [amino_acid.pkx for amino_acid in alignment_amino_acids if amino_acid.pkx is not None]
        if len(pkx_values) != 0:
            self.pkx_statistics = NumericalDescriptiveStatistics(pkx_values)
        else:
            self.pkx_statistics = None
        self.pi_statistics = NumericalDescriptiveStatistics([amino_acid.pi for amino_acid in alignment_amino_acids])
        self.relative_hydrophobicity_at_ph2_statistics = NumericalDescriptiveStatistics([amino_acid.relative_hydrophobicity_at_ph2 for amino_acid in alignment_amino_acids])
        self.relative_hydrophobicity_at_ph7_statistics = NumericalDescriptiveStatistics([amino_acid.relative_hydrophobicity_at_ph7 for amino_acid in alignment_amino_acids])
        self.van_der_waals_volume_statistics = NumericalDescriptiveStatistics([amino_acid.van_der_waals_volume for amino_acid in alignment_amino_acids])
        self.is_acidic_statistics = BinaryDescriptiveStatistics([amino_acid.is_acidic for amino_acid in alignment_amino_acids])
        self.is_basic_statistics = BinaryDescriptiveStatistics([amino_acid.is_basic for amino_acid in alignment_amino_acids])
        self.is_charged_statistics = BinaryDescriptiveStatistics([amino_acid.is_charged for amino_acid in alignment_amino_acids])
        self.is_aromatic_statistics = BinaryDescriptiveStatistics([amino_acid.is_aromatic for amino_acid in alignment_amino_acids])
        self.is_aliphatc_statistics = BinaryDescriptiveStatistics([amino_acid.is_aliphatic for amino_acid in alignment_amino_acids])
        self.is_polar_statistics = BinaryDescriptiveStatistics([amino_acid.is_polar for amino_acid in alignment_amino_acids])
        self.is_hydrophobic_statistics = BinaryDescriptiveStatistics([amino_acid.is_hydrophobic for amino_acid in alignment_amino_acids])
        self.is_small_statistics = BinaryDescriptiveStatistics([amino_acid.is_small for amino_acid in alignment_amino_acids])
        self.is_large_statistics = BinaryDescriptiveStatistics([amino_acid.is_large for amino_acid in alignment_amino_acids])
        self.is_flexible_statistics = BinaryDescriptiveStatistics([amino_acid.is_flexible for amino_acid in alignment_amino_acids])
        self.can_be_phosphorylated_statistics = BinaryDescriptiveStatistics([amino_acid.can_be_phosphorylated for amino_acid in alignment_amino_acids])
        self.can_be_glycosylated_statistics = BinaryDescriptiveStatistics([amino_acid.can_be_glycosylated for amino_acid in alignment_amino_acids])
        self.is_proton_acceptor_or_donor_statistics = BinaryDescriptiveStatistics([amino_acid.is_proton_acceptor_or_donor for amino_acid in alignment_amino_acids])
        self.can_bind_metal_ions_statistics = BinaryDescriptiveStatistics([amino_acid.can_bind_metal_ions for amino_acid in alignment_amino_acids])
        self.is_bcaa_statistics = BinaryDescriptiveStatistics([amino_acid.is_bcaa for amino_acid in alignment_amino_acids])
        self.can_be_ubiquitinated_statistics = BinaryDescriptiveStatistics([amino_acid.can_be_ubiquitinated for amino_acid in alignment_amino_acids])
        self.can_form_special_bonds_statistics = BinaryDescriptiveStatistics([amino_acid.can_form_special_bonds for amino_acid in alignment_amino_acids])
        self.can_form_disulfide_bonds_statistics = BinaryDescriptiveStatistics([amino_acid.can_form_disulfide_bonds for amino_acid in alignment_amino_acids])
        self.in_structural_motifs_statistics = BinaryDescriptiveStatistics([amino_acid.in_structural_motifs for amino_acid in alignment_amino_acids])
    