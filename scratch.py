import asyncio
from pathlib import Path
from biolink.integrations import Mafft

data_dir = Path("/home/codylemke/repos/biolink/data")

async def main():
    input_sequences_file = data_dir / "uniprot" / "input_sequences.fasta"
    input_alignment_file = data_dir / "mafft" / "input_sequence_alignment.fasta"
    await Mafft.run(str(input_sequences_file), str(input_alignment_file), "auto", "max-threads")
    
if __name__ == "__main__":
    asyncio.run(main())