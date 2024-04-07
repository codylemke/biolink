from datetime import datetime
import logging
from pathlib import Path
import subprocess
from typing import List
import psutil

class Mafft:
    logger = logging.getLogger("Mafft")
    
    def __init__(self, input_dir: str, output_dir: str):
        # Fields
        self._input_dir: Path
        self._output_dir: Path
        
        # Constructor
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
    
    
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
    def output_dir(self) -> str:
        return str(self._output_dir.absolute())
    
    @output_dir.setter
    def output_dir(self, value: str) -> None:
        self._output_dir = Path(value)
    
    
    # Public Methods
    @staticmethod
    async def run(input_file: str, output_file: str, *args, **kwargs) -> str:
        Mafft.logger.info(f"Starting Mafft.run for {input_file}")
        cli_command = [
            "mafft",
        ]
        if "max-threads" in args:
            threads = psutil.cpu_count(logical=True) - 1
            kwargs["thread"] = threads
            args = tuple(arg for arg in args if arg != "max-threads")
        for arg in args:
            cli_command.append(f"--{arg}")
        for key, value in kwargs.items():
            cli_command.append(f"--{key}")
            cli_command.append(str(value))
        cli_command.append(input_file)
        stdout = subprocess.run(cli_command, capture_output=True, text=True, check=True).stdout
        with open(output_file, 'w') as file:
            file.write(stdout)
        return stdout
    
    
    @staticmethod
    async def align(input_file: str, output_dir: str, *args, **kwargs) -> str:
        input_filename = Path(input_file).stem
        formatted_datetime = datetime.now().strftime("%Y-%m-%d-%H%M%S")
        output_filename = f"{formatted_datetime}_MSA-mafft-{input_filename}.fasta"
        output_file = str((Path(output_dir) / output_filename).absolute())
        return Mafft.run(input_file, output_file, *args, **kwargs)
        
    # async def align(self, filename: str, *args, **kwargs) -> str:
    #     input_file = str((self._input_dir / filename).absolute())
    #     return Mafft.align(input_file, self.output_dir, *args, **kwargs)
    
    
    @staticmethod
    async def merge(alignments: List[str], output_dir: str, *args, **kwargs) -> str:
        formatted_datetime = datetime.now().strftime("%Y-%m-%d-%H%M%S")
        input_filename = f"{formatted_datetime}_MSA-mafft-merge.txt"
        input_path = Path(output_dir / input_filename)
        input_file = str(input_path.absolute())
        output_filename = f"{formatted_datetime}_MSA-mafft-merge.fasta"
        output_file = str((Path(output_dir) / output_filename).absolute())
        with input_path.open('w') as file:
            file.writelines(alignments)
        args = args + ("merge",)
        return Mafft.run(input_file, output_file, *args, **kwargs)
        