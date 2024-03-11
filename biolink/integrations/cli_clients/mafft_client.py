import subprocess
from pathlib import Path
from biolink.models.system_info import SystemInfo

class MafftClient:
    def __init__(self, input_dir: Path, output_dir: Path):
        self.input_dir = input_dir
        self.output_dir = output_dir
        
    async def align(self, input_file: str):
        system_info = SystemInfo()
        thread_count = system_info.cpu_info.total_cores - 1
        input_path = self.input_dir / input_file
        output_path = self.output_dir / f'{input_path.stem}_alignment.fasta'
        mafft_command = [
            'mafft',
            '--auto',
            '--thread', str(thread_count),
            input_path
        ]
        with open(output_path, 'w') as output_file:
            subprocess.run(mafft_command, stdout=output_file, check=True)