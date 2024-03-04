from datetime import datetime
import os
from pathlib import Path
import subprocess
from typing import List
from .blast_database import BlastDatabase
from biolink.models import SystemInfo, FastaEntry


class BlastClient:
    def __init__(self, input_dir: str, database_dir: str, output_dir: str):
        self.input_dir: Path = Path(input_dir).resolve()
        self.database_dir: Path = Path(database_dir).resolve()
        self.output_dir: Path = Path(output_dir).resolve()

    
    def makeblastdb(self, input_file: str, db_name: str) -> None:
        # Determine protein or nucleotide
        db_type = 'prot'
        db_path = self.database_dir / db_name
        makeblastdb_command = [
            'makeblastdb',
                '-dbtype', db_type,
                '-in', input_file,
                '-title', db_name,
                '-out', str(db_path),
                '-logfile', str(db_path) + '.log',
                '-parse_seqids',
                '-hash_index'
        ]
        subprocess.run(makeblastdb_command, check=True)
    
    
    def get_fasta_entry(self, database: str, entry: str, outfile: str = None) -> str:
        database_path = self.database_dir / database
        blastdbcmd_command = [
            'blastdbcmd',
            '-db', database_path,
            '-entry', entry,
        ]
        stdout = subprocess.run(blastdbcmd_command, capture_output=True, text=True, check=True).stdout
        if outfile != None:
            output_file = Path(outfile).resolve()
            with output_file.open('w') as file:
                file.write(stdout)
        return stdout
    
    
    def get_fasta_entries(self, database: str, entries: List[str], outfile:str=None) -> str:
        database_path = self.database_dir / database
        batch_size = 250
        batches = (entries[i:i + batch_size] for i in range(0, len(entries), batch_size))
        fasta_entries = []
        for batch in batches:
            batch_str = ','.join(batch)
            blastdbcmd_command = [
            'blastdbcmd',
            '-db', str(database_path),
            '-entry', batch_str,
        ]
            stdout = subprocess.run(blastdbcmd_command, capture_output=True, text=True, check=True).stdout
            fasta_entries.append(stdout)
        fasta_entries_string = ''.join(fasta_entries)
        if outfile != None:
            output_file = Path(outfile).resolve()
            with output_file.open('w') as file:
                file.write(fasta_entries_string)
        return fasta_entries_string
    
    
    def get_blast_version(self):
        result = subprocess.run(['blastp', '-version'], capture_output=True, text=True)
        return result.stdout.split("\n")[1].split(':')[1].strip()
    
    
    def blastp(self,
               input_file: str,
               database: str,
               e_value: float = 10,
               max_target_seqs: int = 1000,
               num_threads: int = 0,
               scoring_matrix: str = 'BLOSUM62',
               gap_open_penalty: int = 11,
               gap_extension_penalty: int = 1,
               word_size: int = 3) -> None:
        input_path = self.input_dir / input_file
        database_path = self.database_dir / database
        output_file = f'blastp-{os.path.splitext(os.path.basename(input_file))[0]}-{database}.csv'
        output_path = self.output_dir / output_file
        input_fasta_entry = FastaEntry(Path(input_path).read_text())
        blast_database = BlastDatabase(str(database_path))
        system_info = SystemInfo()
        blast_version = self.get_blast_version()
        if num_threads == 0:
            num_threads = system_info.cpu_info.total_cores - 1
        blastp_command = [
            'blastp',
            '-query', str(input_path),
            '-db', str(database_path),
            '-evalue', str(e_value),
            '-outfmt', '10 sacc pident ppos length slen qcovs gapopen qstart qend sstart send evalue bitscore',
            '-num_threads', str(num_threads),
            '-max_target_seqs', str(max_target_seqs),
            '-matrix', scoring_matrix,
            '-gapopen', str(gap_open_penalty),
            '-gapextend', str(gap_extension_penalty),
            '-word_size', str(word_size)
        ]
        headers = [
            f'# Search Algorithm: blastp',
            f'# Blast Version: {blast_version}',
            f'# Datetime: {datetime.now()}',
            f'# Input: {input_path}',
            f'# Query Accession: {input_fasta_entry.accession}',
            f'# Query Sequence: {input_fasta_entry.sequence}',
            f'# Query Length: {len(input_fasta_entry)}',
            f'# Database: {database_path}',
            f'# Database Sequences: {blast_database.sequence_count}',
            f'# Database Residues: {blast_database.residue_count}',
            f'# Database Longest Sequence: {blast_database.longest_sequence}',
            f'# BlastDB Version: {blast_database.blastdb_version}',
            f'# E-Value: {e_value}',
            f'# Scoring Matrix: {scoring_matrix}',
            f'# Gap Open Penalty: {gap_open_penalty}',
            f'# Gap Extension Penalty: {gap_extension_penalty}',
            f'# Word Size: {word_size}',
            f'# Max Target Sequences: {max_target_seqs}',
            # Query Coverage,
            # Percent Identity Filters,
            f'# Thread Count: {num_threads}',
            f'# Working Directory: {os.getcwd()}',
            f'# Blastp Command: {self.print_command(blastp_command)}',
            f'# Output: {output_path}',
            f'# OS: {system_info.os_info.os}',
            f'# OS Release: {system_info.os_info.release}',
            f'# OS Version: {system_info.os_info.version}',
            f'# OS Architecture: {system_info.os_info.architecture}',
            f'# CPU Physical Cores: {system_info.cpu_info.physical_cores}',
            f'# CPU Total Cores: {system_info.cpu_info.total_cores}',
            f'# CPU Max Frequency: {system_info.cpu_info.max_frequency}',
            f'# CPU Min Frequency: {system_info.cpu_info.min_frequency}',
            f'# Memory Total: {system_info.memory_info.total}',
            f'# Memory Available: {system_info.memory_info.available}',
            #f'# Disk Total Size: {system_info.memory_info.available}',
            #f'# Disk Available: {system_info.memory_info.available}',
            
            #f'# Execution Time: {system_info.memory_info.available}',
            #f'# Memory Used: {system_info.memory_info.used}',
            #f'# Memory Percent Used: {system_info.memory_info.percent_used}',
            #f'# CPU Current Frequency: {system_info.cpu_info.current_frequency}',
            f'# Fields: SubjectAccession,PercentIdentity,PercentPositive,AlignmentLength,SubjectLength,QueryCoverage,GapOpenings,QueryStart,QueryEnd,SubjectStart,EValue,BitScore',
        ]
        with open(output_path, 'w') as file:
            for header in headers:
                file.write(header + '\n')
        with open(output_path, 'a') as file:
            subprocess.run(blastp_command, stdout=file, check=True)


    def print_command(self, command_list: List[str]) -> str:
        return ' '.join(f'"{arg}"' if ' ' in arg or any(c in arg for c in ['*', '?', '$']) else arg for arg in command_list)