from datetime import datetime
import subprocess
import re

class BlastDatabase:
    def __init__(self, database_path: str):
        # Fields
        self.database_path = database_path
        self.name: str
        self.sequence_count: int
        self.residue_count: int
        self.created_datetime: datetime
        self.longest_sequence: int
        self.blastdb_versio: int
        # Constructor
        info = str(subprocess.run(['blastdbcmd', '-db', database_path, '-info'], check=True, capture_output=True, text=True))
        sequence_count_pattern = r'(\d{1,3}(?:,\d{3})*)(?= sequences;)'
        self.sequence_count = re.search(sequence_count_pattern, info).group(0)
        residue_count_pattern = r'(\d{1,3}(?:,\d{3})*)(?= total residues)'
        self.residue_count = re.search(residue_count_pattern, info).group(0)
        created_date_pattern = r'(?<=Date: )([\w\s,:]+)(?=\sLongest)'
        #datetime_string = re.search(created_date_pattern, info).group(0)
        #self.created_datetime = datetime.strptime(datetime_string, "%b %d, %Y  %I:%M %p")
        longest_sequence_pattern = r'(?<=Longest sequence: )(\d{1,3}(?:,\d{3})*)(?= residues)'
        self.longest_sequence = re.search(longest_sequence_pattern, info).group(0)
        blastdb_version_pattern = r'(?<=BLASTDB Version: )(\d+)'
        self.blastdb_version = re.search(blastdb_version_pattern, info).group(0)
        
    def query(self, accession: str):
        blastdbcmd_command = [
            'blastdbcmd',
            '-db', self.database_path,
            '-entry', accession,
        ]
        subprocess.run(blastdbcmd_command, check=True)
