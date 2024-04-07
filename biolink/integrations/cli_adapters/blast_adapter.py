from datetime import datetime
from pathlib import Path
import re
import subprocess
from typing import List, Dict
import psutil

class Blast:
    
    def __init__(self, input_dir: str, database_dir: str, output_dir: str):
        # Fields
        self._input_dir: Path
        self._database_dir: Path
        self._output_dir: Path
        
        # Constructor
        self.input_dir = input_dir
        self.database_dir = database_dir
        self.output_dir = output_dir
    
    
    # Internal Methods
    # N/A
    
    # Properties
    @property
    def input_dir(self) -> str:
        return str(self._input_dir.absolute())
    
    @input_dir.setter
    def input_dir(self, value: str) -> None:
        self._input_dir = Path(value)
    
    @property
    def database_dir(self) -> str:
        return str(self._database_dir.absolute())
    
    @database_dir.setter
    def database_dir(self, value: str) -> None:
        self._database_dir = Path(value)
    
    @property
    def output_dir(self) -> str:
        return str(self._output_dir.absolute())
    
    @output_dir.setter
    def output_dir(self, value: str) -> None:
        self._output_dir = Path(value)
    
    
    # Public Methods
    @staticmethod
    def get_blast_version(self):
        cli_command = [
            "blastp",
                "-version"
        ]
        stdout = subprocess.run(cli_command, capture_output=True, text=True, check=True).stdout
        return stdout.split("\n")[1].split(':')[1].strip()
    
    
    @staticmethod
    async def makeblastdb(input_file: str, output: str, db_type: str="prot") -> None:
        cli_command = [
            "makeblastdb",
                "-dbtype", db_type,
                "-in", input_file,
                "-title", Path(output).stem,
                "-out", output,
                "-logfile", f"{output}.log",
                "-parse_seqids",
                "-hash_index"
        ]
        subprocess.run(cli_command, check=True)
    
    # async def makeblastdb(self, input_file: str, db_name: str, db_type: str="prot") -> None:
    #     output = str((self._database_dir / db_name).absolute())
    #     Blast.makeblastdb(input_file, output, db_type)
    
    
    @staticmethod
    def get_db_info(database: str) -> Dict[str, str]:
        cli_command = [
            "blastdbcmd",
                "-db", database,
                "-info"
        ]
        stdout = subprocess.run(cli_command, capture_output=True, text=True, check=True).stdout
        sequence_count_pattern = r'(\d{1,3}(?:,\d{3})*)(?= sequences;)'
        residue_count_pattern = r'(\d{1,3}(?:,\d{3})*)(?= total residues)'
        created_date_pattern = r'(?<=Date: )([\w\s,:]+)(?=\sLongest)'
        longest_sequence_pattern = r'(?<=Longest sequence: )(\d{1,3}(?:,\d{3})*)(?= residues)'
        blastdb_version_pattern = r'(?<=BLASTDB Version: )(\d+)'
        db_info = {}
        db_info["sequence_count"] = re.search(sequence_count_pattern, stdout).group(0)
        db_info["residue_count"] = re.search(residue_count_pattern, stdout).group(0)
        db_info["created_date"] = re.search(created_date_pattern, stdout).group(0)
        db_info["longest_sequence"] = re.search(longest_sequence_pattern, stdout).group(0)
        db_info["blastdb_version"] = re.search(blastdb_version_pattern, stdout).group(0) 
        return db_info
    
    # def get_db_info(self, db_name: str) -> Dict[str, str]:
    #     database = str((self._database_dir / db_name).absolute())
    #     return Blast.get_db_info(database)
    
    
    @staticmethod
    def get_fasta_entry(entry: str, database: str, output_file: str=None) -> str:
        cli_command = [
            "blastdbcmd",
                "-db", database,
                "-entry", entry,
        ]
        stdout = subprocess.run(cli_command, capture_output=True, text=True, check=True).stdout
        if output_file != None:
            with open(output_file, 'w') as file:
                file.write(stdout)
        return stdout
    
    # def get_fasta_entry(self, entry: str, db_name: str, output_file: str=None) -> str:
    #     database = str((self._database_dir / db_name).absolute())
    #     return Blast.get_fasta_entry(entry, database, output_file)
    
    
    @staticmethod
    async def get_fasta_entries(entries: List[str], database: str, output_file: str=None) -> str:
        batch_size = 250
        batches = (entries[i:i + batch_size] for i in range(0, len(entries), batch_size))
        fasta_entries = []
        for batch in batches:
            entries_str = ','.join(batch)
            stdout = await Blast.get_fasta_entry(database, entries_str)
            fasta_entries.append(stdout)
        fasta_entries_str = ''.join(fasta_entries)
        if output_file != None:
            with open(output_file, 'w') as file:
                file.write(fasta_entries_str)
        return fasta_entries_str
    
    # async def get_fasta_entries(self, entries: List[str], db_name: str, output_file: str=None) -> str:
    #     database = str((self._database_dir / db_name).absolute())
    #     return Blast.get_fasta_entries(entries, database, output_file)
    
    
    @staticmethod
    async def blastp(input_file: str, database: str, output_dir: str, *args, **kwargs) -> str:
        formatted_datetime = datetime.now().strftime("%Y-%m-%d-%H%M%S")
        input_filename = Path(input_file).stem
        db_name = Path(database).stem
        output_filename = f"{formatted_datetime}_blastp-{db_name}-{input_filename}.csv"
        output_path = Path(output_dir) / output_filename
        cli_command = [
            "blastp",
                "-query", input_file,
                "-db", database,
        ]
        if kwargs.get("outfmt") == None:
            kwargs["outfmt"] = "10 sacc pident ppos length slen qcovs gapopen qstart qend sstart send evalue bitscore"
        for arg in args:
            cli_command.append(f"-{arg}")
        for key, value in kwargs.items():
            cli_command.append(f"-{key} {value}")
        stdout = subprocess.run(cli_command, capture_output=True, text=True, check=True).stdout
        with output_path.open('w') as file:
            file.write(stdout)
        return stdout

    # async def blastp(self, input_filename: str, db_name: str, *args, **kwargs) -> str:
    #     input_file = str((self._input_dir / input_filename).absolute())
    #     database = str((self._database_dir / db_name).absolute())
    #     return Blast.blastp(input_file, database, self.output_dir, *args, **kwargs)