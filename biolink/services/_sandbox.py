import asyncio
import json
import logging
from pathlib import Path
from biolink.integrations import Blast, UniprotClient, Mafft, ClustalO
from biolink.models.bioinformatics import FastaFile, ProteinAlignment, BlastResults
from biolink.models.biology import Protein

# Configure Logging
log_level = logging.INFO
log_format = "[%(asctime)s|%(levelname)s|%(name)s] - %(message)s"
date_format = "%Y-%m-%d|%H:%M:%S"
formatter = logging.Formatter(fmt=log_format, datefmt=date_format)
console_log_handler = logging.StreamHandler()
console_log_handler.setLevel(log_level)
console_log_handler.setFormatter(formatter)
root_logger = logging.getLogger()
root_logger.setLevel(log_level)
root_logger.addHandler(console_log_handler)


data_dir = Path(r"E:\data")
uniprot_client = UniprotClient()

async def main():
    # Fetch Input Sequences Accessions
    input_accessions_file = data_dir / "input_accessions.txt"
    with input_accessions_file.open('r') as file:
        accessions = [line.strip() for line in file if line.strip()]
    
    # Fetch Input Sequences Fasta Files
    input_sequences_file = data_dir / "uniprot" / "input_sequences.fasta"
    input_sequences = await uniprot_client.get_entries(accessions)
    input_sequences_fasta_file = FastaFile(input_sequences)
    input_sequences_fasta_file.save(str(input_sequences_file))
    input_fasta_files = []
    for entry in input_sequences_fasta_file:
        input_sequence_file = data_dir / "uniprot" / f"{entry.accession}.fasta"
        input_sequence_fasta_file = FastaFile(str(entry))
        input_sequence_fasta_file.save(str(input_sequence_file))
        input_fasta_files.append(input_sequence_fasta_file)
    
    # # Fetch Input Sequences Protein Data
    # input_protein_data = await uniprot_client.get_entries(accessions, outfmt="json")
    # proteins = [Protein.parse_uniprot_details(entry) for entry in json.loads(input_protein_data)]
    
    # # Sort Input Proteins
    # input_plant_proteins = [protein for protein in proteins if "Viridiplantae" in protein.organism.taxonomy_list]
    # input_bacterial_proteins = [protein for protein in proteins if "Bacteria" in protein.organism.taxonomy_list]
    # input_fungal_proteins = [protein for protein in proteins if "Fungi" in protein.organism.taxonomy_list]
    
    # # Sort Input Sequences
    # input_plant_accessions = [protein.uniprot_id for protein in input_plant_proteins]
    # input_bacterial_accessions = [protein.uniprot_id for protein in input_bacterial_proteins]
    # input_fungal_accessions = [protein.uniprot_id for protein in input_fungal_proteins]
    # input_plant_sequences_fasta_entries = []
    # input_bacterial_sequences_fasta_entries = []
    # input_fungal_sequences_fasta_entries = []
    # for entry in input_sequences_fasta_file:
    #     if entry.accession in input_plant_accessions:
    #         input_plant_sequences_fasta_entries.append(str(entry))
    #     elif entry.accession in input_bacterial_accessions:
    #         input_bacterial_sequences_fasta_entries.append(str(entry))
    #     elif entry.accession in input_fungal_accessions:
    #         input_fungal_sequences_fasta_entries.append(str(entry))
    #     else:
    #         raise Exception(f"Accession could not be sorted: {entry.accession}")
    # input_plant_sequences_fasta_file = FastaFile('\n'.join(input_plant_sequences_fasta_entries))
    # input_bacterial_sequences_fasta_file = FastaFile('\n'.join(input_bacterial_sequences_fasta_entries))
    # input_fungal_sequences_fasta_file = FastaFile('\n'.join(input_fungal_sequences_fasta_entries))
    # input_plant_sequences_file = data_dir / "uniprot" / "input_plant_sequences.fasta"
    # input_bacterial_sequences_file = data_dir / "uniprot" / "input_bacterial_sequences.fasta"
    # input_fungal_sequences_file = data_dir / "uniprot" / "input_fungal_sequences.fasta"
    # input_plant_sequences_fasta_file.save(input_plant_sequences_file)
    # input_bacterial_sequences_fasta_file.save(input_bacterial_sequences_file)
    # input_fungal_sequences_fasta_file.save(input_fungal_sequences_file)
    
    # # Generate Input Alignments
    # input_plant_alignment_file = data_dir / "clustalo" / "input_plant_sequence_alignment.fasta"
    # input_bacterial_alignment_file = data_dir / "clustalo" / "input_bacterial_sequence_alignment.fasta"
    # input_fungal_alignment_file = data_dir / "clustalo" / "input_fungal_sequence_alignment.fasta"
    # await ClustalO.run(str(input_plant_sequences_file), str(input_plant_alignment_file), "auto", "max-threads")
    # await ClustalO.run(str(input_bacterial_sequences_file), str(input_bacterial_alignment_file), "auto", "max-threads")
    # await ClustalO.run(str(input_fungal_sequences_file), str(input_fungal_alignment_file), "auto", "max-threads")
    # input_plant_alignment = ProteinAlignment.parse_fasta(input_plant_alignment_file)
    # input_bacterial_alignment = ProteinAlignment.parse_fasta(input_bacterial_alignment_file)
    # input_fungal_alignment = ProteinAlignment.parse_fasta(input_fungal_alignment_file)
    
    # # Trim Input Plant Alignment
    # plant_truncation_index = input_plant_alignment.get_alignment_index("Q38802", 'Q', 84)
    # for accession, sequence in input_plant_alignment.data.items():
    #     input_plant_alignment.data[accession] = sequence[plant_truncation_index:]
    # input_plant_alignment.file.save()
    
    # # Calculate Input Alignment Statistics
    # input_plant_alignment_profile = input_plant_alignment.get_alignment_profile()
    # input_bacterial_alignment_profile = input_bacterial_alignment.get_alignment_profile()
    # input_fungal_alignment_profile = input_fungal_alignment.get_alignment_profile()
    
    # # Align All Sequences    
    # input_alignment_file = data_dir / "mafft" / "input_sequence_alignment.fasta"
    # await Mafft.run(str(input_sequences_file), str(input_alignment_file), "auto", "max-threads")
    # input_alignment = ProteinAlignment.parse_fasta(input_alignment_file)
    
    # # Calculate Alignment Statistics
    # input_alignment_profile = input_alignment.get_alignment_profile()    

    # Blast Input Sequences Against UniRef100
    database = str(data_dir / "blast_dbs" / "UniRef100-2024_02")
    output_dir = data_dir / "blast"
    # for file in input_fasta_files:
    #     await Blast.blastp(file.file_path, database, output_dir, "max-threads")
    uniref100_accessions = set()
    for file in output_dir.iterdir():
        uniref100_accessions.update(BlastResults.parse_file(file).hit_accessions)
    uniref100_accessions = list(uniref100_accessions)
    
    # Map Accessions To UniProtKB
    output_protein_data = await uniprot_client.get_entries(uniref100_accessions, outfmt="json", outfile=str(data_dir / "uniprot" / "test.json"))
    print("success")
    return
    output_protein_json_data = json.loads(output_protein_data)
    output_proteins = []
    for result in output_protein_json_data["results"]:
        output_proteins.append(Protein.parse_uniprot_details(result["to"]))
    uniparc_ids = []
    remaining_ids = []
    for failed_id in output_protein_json_data["failedIds"]:
        if "UniRef100_UPI" in failed_id:
            uniparc_ids.append(failed_id.split('_')[1])
        else:
            remaining_ids.append(failed_id)
    new_output_protein_data = await uniprot_client.run_id_mapping(uniparc_ids, "UniParc", "UniProtKB", outfmt="json", outfile=str(data_dir / "uniprot" / "test.json"))
    root_logger.info(f"Remaining Ids: {remaining_ids}")
    return
        
    
    
    # Sort Output Proteins
    output_plant_proteins = [protein for protein in output_proteins if "Viridiplantae" in protein.organism.taxonomy_list]
    output_bacterial_proteins = [protein for protein in output_proteins if "Bacteria" in protein.organism.taxonomy_list]
    output_fungal_proteins = [protein for protein in output_proteins if "Fungi" in protein.organism.taxonomy_list]
    
    # Sort Output Sequences
    output_sequences_file = data_dir / "uniprot" / "output_sequences.fasta"
    output_sequences = await uniprot_client.run_id_mapping(uniref100_accessions, "UniRef100", "UniProtKB", outfmt="fasta")
    output_sequences_fasta_file = FastaFile(output_sequences)
    output_sequences_fasta_file.save(str(output_sequences_file))
    output_plant_accessions = [protein.uniprot_id for protein in output_plant_proteins]
    output_bacterial_accessions = [protein.uniprot_id for protein in output_bacterial_proteins]
    output_fungal_accessions = [protein.uniprot_id for protein in output_fungal_proteins]
    output_plant_sequences_fasta_entries = []
    output_bacterial_sequences_fasta_entries = []
    output_fungal_sequences_fasta_entries = []
    for entry in output_sequences_fasta_file:
        if entry.accession in output_plant_accessions:
            output_plant_sequences_fasta_entries.append(str(entry))
        elif entry.accession in output_bacterial_accessions:
            output_bacterial_sequences_fasta_entries.append(str(entry))
        elif entry.accession in output_fungal_accessions:
            output_fungal_sequences_fasta_entries.append(str(entry))
        else:
            raise Exception(f"Accession could not be sorted: {entry.accession}")
    output_plant_sequences_fasta_file = FastaFile('\n'.join(output_plant_sequences_fasta_entries))
    output_bacterial_sequences_fasta_file = FastaFile('\n'.join(output_bacterial_sequences_fasta_entries))
    output_fungal_sequences_fasta_file = FastaFile('\n'.join(output_fungal_sequences_fasta_entries))
    output_plant_sequences_file = data_dir / "uniprot" / "output_plant_sequences.fasta"
    output_bacterial_sequences_file = data_dir / "uniprot" / "output_bacterial_sequences.fasta"
    output_fungal_sequences_file = data_dir / "uniprot" / "output_fungal_sequences.fasta"
    output_plant_sequences_fasta_file.save(output_plant_sequences_file)
    output_bacterial_sequences_fasta_file.save(output_bacterial_sequences_file)
    output_fungal_sequences_fasta_file.save(output_fungal_sequences_file)
    
   # Generate Output Alignments
    output_plant_alignment_file = data_dir / "clustalo" / "output_plant_sequence_alignment.fasta"
    output_bacterial_alignment_file = data_dir / "clustalo" / "output_bacterial_sequence_alignment.fasta"
    output_fungal_alignment_file = data_dir / "clustalo" / "output_fungal_sequence_alignment.fasta"
    await Mafft.run(output_plant_sequences_file, output_plant_alignment_file, "auto", "max-threads")
    await Mafft.run(output_bacterial_sequences_file, output_bacterial_alignment_file, "auto", "max-threads")
    await Mafft.run(output_fungal_sequences_file, output_fungal_alignment_file, "auto", "max-threads")
    output_plant_alignment = ProteinAlignment.parse_fasta(output_plant_alignment_file)
    output_bacterial_alignment = ProteinAlignment.parse_fasta(output_bacterial_alignment_file)
    output_fungal_alignment = ProteinAlignment.parse_fasta(output_fungal_alignment_file)
    
    # Trim Output Plant Alignment
    plant_truncation_index = output_plant_alignment.get_alignment_index("Q38802", 'Q', 84)
    for accession, sequence in output_plant_alignment.data.items():
        output_plant_alignment.data[accession] = sequence[plant_truncation_index:]
    output_plant_alignment.file.save()
    
    # Calculate Output Alignment Statistics
    output_plant_alignment_profile = output_plant_alignment.get_alignment_profile()
    output_bacterial_alignment_profile = output_bacterial_alignment.get_alignment_profile()
    output_fungal_alignment_profile = output_fungal_alignment.get_alignment_profile()
    
    # Align all alignments
    output_alignment_input_file = data_dir / "mafft" / "output_alignment.txt"
    output_alignments = [
        str(output_plant_alignment_file),
        str(output_bacterial_alignment_file),
        str(output_fungal_alignment_file)
    ]
    with open(output_alignment_input_file, 'w') as file:
        file.writelines(output_alignments)
    output_alignment_file = data_dir / "mafft" / "output_sequence_alignment.fasta"
    Mafft.run(output_alignment_input_file, output_alignment_file, "auto", "max-threads")
    output_alignment = ProteinAlignment.parse_fasta(output_alignment_file)
    
    # Calculate Alignment Statistics
    output_alignment_profile = output_alignment.get_alignment_profile()
    
    # Filter Sequences
    # (TODO - May require significant amount of work)
    # (TODO - Be able to save statistics data to a file)
    
    # Count the number of plant, bacterial, and fungal sequences left, and calculate percentages
    
    # Acquire data surrounding sequence representation of each domain
    
    # Normalize the representation percentages
    
    # Create BlastDB
    
if __name__ == "__main__":
    asyncio.run(main())