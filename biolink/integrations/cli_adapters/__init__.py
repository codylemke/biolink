from .blast_adapter import Blast
from .clustalo_adapter import ClustalO
from .mafft_adapter import Mafft

# def _print_command(self, command_list: List[str]) -> str:
#         return ' '.join(f'"{arg}"' if ' ' in arg or any(c in arg for c in ['*', '?', '$']) else arg for arg in command_list)

# headers = [
        #     f'# Search Algorithm: blastp',
        #     f'# Blast Version: {blast_version}',
        #     f'# Datetime: {datetime.now()}',
        #     f'# Input: {input_path}',
        #     f'# Query Accession: {input_fasta_entry.accession}',
        #     f'# Query Sequence: {input_fasta_entry.sequence}',
        #     f'# Query Length: {len(input_fasta_entry)}',
        #     f'# Database: {database_path}',
        #     f'# Database Sequences: {blast_database.sequence_count}',
        #     f'# Database Residues: {blast_database.residue_count}',
        #     f'# Database Longest Sequence: {blast_database.longest_sequence}',
        #     f'# BlastDB Version: {blast_database.blastdb_version}',
        #     f'# E-Value: {e_value}',
        #     f'# Scoring Matrix: {scoring_matrix}',
        #     f'# Gap Open Penalty: {gap_open_penalty}',
        #     f'# Gap Extension Penalty: {gap_extension_penalty}',
        #     f'# Word Size: {word_size}',
        #     f'# Max Target Sequences: {max_target_seqs}',
        #     # Query Coverage,
        #     # Percent Identity Filters,
        #     f'# Thread Count: {num_threads}',
        #     f'# Working Directory: {os.getcwd()}',
        #     f'# Blastp Command: {self._print_command(blastp_command)}',
        #     f'# Output: {output_path}',
        #     f'# OS: {system_info.os_info.os}',
        #     f'# OS Release: {system_info.os_info.release}',
        #     f'# OS Version: {system_info.os_info.version}',
        #     f'# OS Architecture: {system_info.os_info.architecture}',
        #     f'# CPU Physical Cores: {system_info.cpu_info.physical_cores}',
        #     f'# CPU Total Cores: {system_info.cpu_info.total_cores}',
        #     f'# CPU Max Frequency: {system_info.cpu_info.max_frequency}',
        #     f'# CPU Min Frequency: {system_info.cpu_info.min_frequency}',
        #     f'# Memory Total: {system_info.memory_info.total}',
        #     f'# Memory Available: {system_info.memory_info.available}',
        #     #f'# Disk Total Size: {system_info.memory_info.available}',
        #     #f'# Disk Available: {system_info.memory_info.available}',
        #     #f'# Execution Time: {system_info.memory_info.available}',
        #     #f'# Memory Used: {system_info.memory_info.used}',
        #     #f'# Memory Percent Used: {system_info.memory_info.percent_used}',
        #     #f'# CPU Current Frequency: {system_info.cpu_info.current_frequency}',
        #     f'# Fields: SubjectAccession,PercentIdentity,PercentPositive,AlignmentLength,SubjectLength,QueryCoverage,GapOpenings,QueryStart,QueryEnd,SubjectStart,EValue,BitScore',
        # ]
        # with open(output_path, 'w') as file:
        #     for header in headers:
        #         file.write(header + '\n')