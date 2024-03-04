import asyncio
from pathlib import Path
from biolink.integrations import BlastClient
from biolink.models import FastaFile

fasta_file = FastaFile("/home/codylemke/repos/biolink/tests/models/assets/input_sequences.fasta")
print(fasta_file._file_path)