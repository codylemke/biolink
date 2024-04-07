from pathlib import Path
import subprocess
from biolink.integrations import BlastClient, UniprotClient, MafftClient, PigzClient, ClustalOmegaClient, ZstdClient
from biolink.models import FastaFile, MSA
from biolink.integrations import BlastResults

root_dir = Path(__file__).parent.parent
data_dir = root_dir / "data"

# Initialize --------------------------------------------------------------
print("Creating UniprotClient")
uniprot_client = UniprotClient()

print("Creating BlastClient")
input_dir = str(data_dir / "fasta_files")
database_dir = str(data_dir / "blast_databases")
output_dir = str(data_dir / "blast_results")
blast_client = BlastClient(input_dir, database_dir, output_dir)

print("Creating MafftClient")
mafft_client = MafftClient()

print("Creating Clustal Omega Client")
clustalo_client = ClustalOmegaClient()


# Prepare Blast Databases -----------------------------------------------------
subprocess.run(root_dir / "scripts" / "prepare_uniprot_blast_dbs.sh")


# Sort Input Accessions By Kingdom --------------------------------------------
print("Sorting Accessions By Kingdom")
with open(data_dir / "input_accessions.txt", 'r') as file:
    input_accessions = [line.strip() for line in file.readlines() if line.strip()]
accessions_detail = uniprot_client.get_entries_details(input_accessions)
plant_accessions = [entry['primaryAccession'] for entry in accessions_detail if entry['organism']['lineage'][1] == 'Viridiplantae']
bacterial_accessions = [entry['primaryAccession'] for entry in accessions_detail if entry['organism']['lineage'][0] == 'Bacteria']
fungal_accessions = [entry['primaryAccession'] for entry in accessions_detail if entry['organism']['lineage'][1] == 'Fungi']


# Get Fasta Files For Input Sequences -----------------------------------------
print("Gathering input sequences")
blast_client.get_fasta_entries(f"uniprotkb-{uniprot_client.release}", plant_accessions, data_dir / "plant_sequences.fasta")
blast_client.get_fasta_entries(f"uniprotkb-{uniprot_client.release}", bacterial_accessions, data_dir / "bacterial_sequences.fasta")
blast_client.get_fasta_entries(f"uniprotkb-{uniprot_client.release}", fungal_accessions, data_dir / "fungal_sequences.fasta")


# Align sequences in each kingdom ---------------------------------------------
print("Aligning sequences within each kingdom")
clustalo_client.align(data_dir / "plant_sequences.fasta", data_dir / "plant_sequences_alignment.fasta")
clustalo_client.align(data_dir / "bacterial_sequences.fasta", data_dir / "bacterial_sequences_alignment.fasta")
clustalo_client.align(data_dir / "fungal_sequences.fasta", data_dir / "fungal_sequences_alignment.fasta")


# Determine End Trimming of plant sequences -----------------------------------
# Based on the amino acid number of a designated sequence, trims the ends of the alignments


# Run consurf on all 3 alignments ---------------------------------------------


# Blast all query sequences ---------------------------------------------------
print("Blasting all query sequences")
for fasta_file in blast_client.input_dir.glob("*.fasta"):
    blast_client.blastp(str(file), f"uniref100-{uniprot_client.release}")

# Create Set with all blast hits ----------------------------------------------
print("Creating set with all blast hits")
output_files = [file for file in output_dir.iterdir() if file.is_file()]
hits = set()
for file in output_files:
    results = BlastResults(str(file))
    hits.update(set(results.hit_accessions))

# Fetch details for each accession --------------------------------------------


# Sort accessions by kingdoms -------------------------------------------------


# Align sequences in each kingdom with reference alignment --------------------


# Trim ends of plant sequences alignment where necessary ----------------------


# Run Consurf on each alignment -----------------------------------------------


# Perform advanced filtering on each alignmet for each blast sequence ---------------------------------


# Align All 3 MSAs ------------------------------------------------------------


# Run Consurf on each alignment -----------------------------------------------


# Perform advanced filtering for each blast sequence --------------------------

# Count the number of sequences in each kindom --------------------------------


# (TODO) - Get data on sequencing representation in databases to normalize DTC representation

# Build a phylogenetic tree

# Create fasta file of all sequences with gaps removed ------------------------
print("Creating fasta file with all blast hits")
with open(root_dir / "hits.fasta", 'w') as file:
    fasta_entries = blast_client.get_fasta_entries(database, list(hits))
    file.write(fasta_entries)

# Make a blast database with this fasta file

# Perform Many To Many Blast for each sequence ------------------------------------
mafftClient = MafftClient(output_dir, output_dir)
mafftClient.align("hits.fasta")

# Generate a sequence similarity network from the output data
