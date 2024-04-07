from datetime import datetime
import logging
from pathlib import Path
import subprocess
import psutil

class ClustalO:
    logger = logging.getLogger("ClustalO")
    
    def __init__(self, input_dir: str, output_dir: str):
        # Fields
        self._input_dir: Path
        self._output_dir: Path
        
        # Constructor
        self.input_dir = input_dir
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
    def output_dir(self) -> str:
        return str(self._output_dir.absolute())
    
    @output_dir.setter
    def output_dir(self, value: str) -> None:
        self._output_dir = Path(value)
    
    
    # Public Methods
    @staticmethod
    async def run(input_file: str, output_file: str=None, *args, **kwargs) -> str:
        ClustalO.logger.info(f"Starting ClustalO run for {input_file}")
        cli_command = [
            "clustalo",
            "-i", input_file
        ]
        if "max-threads" in args:
            threads = psutil.cpu_count(logical=True) - 1
            kwargs["threads"] = threads
            args = tuple(arg for arg in args if arg != "max-threads")
        for arg in args:
            cli_command.append(f"--{arg}")
        for key, value in kwargs.items():
            cli_command.append(f"--{key}={value}")
        stdout = subprocess.run(cli_command, capture_output=True, text=True, check=True).stdout
        if output_file != None:
            with open(output_file, 'w') as file:
                file.write(stdout)
        return stdout
    
    # async def run(self, filename: str, *args, **kwargs) -> str:
    #     input_file = str((self._input_dir / filename).absolute())
    #     return ClustalO.run(input_file, self.output_dir, *args, **kwargs)
    
    
    @staticmethod
    async def align(input_file: str, output_dir: str, *args, **kwargs) -> str:
        input_filename = Path(input_file).stem
        formatted_datetime = datetime.now().strftime("%Y-%m-%d-%H%M%S")
        output_filename = f"{formatted_datetime}_MSA-clustalo-{input_filename}.fasta"
        output_file = str((Path(output_dir) / output_filename).absolute())
        return ClustalO.run(input_file, output_file, *args, **kwargs)
