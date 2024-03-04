import subprocess
from biolink.models.system_info import SystemInfo


class ClustalOmegaClient:
    def __init__(self):
        self.system_info = SystemInfo()
        pass
    
    def align(self, input_fasta:str, output_fasta:str, iterations:int=0, thread_count:int=0, use_kimura:bool=False, full:bool=False, full_iter:bool=False):
        if thread_count == 0:
            thread_count = self.system_info.cpu_info.total_cores - 1
        command = [
            "clustalo",
            "-i", input_fasta,
            "-o", output_fasta,
            f"--threads={thread_count}",
        ]
        if iterations != 0:
            command.append(f"--iterations={iterations}")
        if use_kimura == True:
            command.append("--use-kimura")
        if full == True:
            command.append("--full")
        if full_iter == True:
            command.append("--full-iter")
        subprocess.run(command, check=True)