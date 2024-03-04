from pathlib import Path
import boto3
import subprocess
from biolink.integrations import BlastClient, UniprotClient, MafftClient, PigzClient, ClustalOmegaClient, ZstdClient
from biolink.models import FastaFile, MSA
from biolink.integrations.blast_client import BlastResults

root_dir = Path(__file__).parent.parent
data_dir = root_dir / "data"


# Create Clients
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


# Implement downloading and extraction of database from S3
s3_client = boto3.client("s3")
obj = s3_client.get_object("codylemke-hpc", "biolink/uniprot/relnotes.txt")
first_line = obj['Body']._raw_stream.readline().decode('utf-8').strip()
downloaded_release = first_line.split(' ')[2]
downloaded_release_year, downloaded_release_version = map(int, downloaded_release.split('_'))
available_release_year, available_release_version = map(int, uniprot_client.release.split('_'))
update_available = False
if available_release_year > downloaded_release_year:
    update_available = True
elif available_release_year < downloaded_release_year:
    update_available = False
else:
    if available_release_version > downloaded_release_version:
        update_available = True
    else:
        update_available = False
if update_available:
    uniprot_client.download_relnotes("/tmp/relnotes")
    uniprot_client.download_uniprot_sprot("/tmp/uniprot_sprot.fasta.gz")
    PigzClient.decompress("/tmp/uniprot_sprot.fasta.gz")
    blast_client.makeblastdb("/tmp/uniprot_sprot.fasta", f"swissprot-{uniprot_client.release}")
    subprocess.run(f"tar --zstd -cf swissprot-{uniprot_client.release}.tar.zst /tmp/*swissprot-{uniprot_client.release}")
    s3_client.upload_file(f"/tmp/swissprot-{uniprot_client.release}.tar.zst", "codylemke-hpc", "biolink/uniprot")
    uniprot_client.download_uniprot_trembl("/tmp/uniprot_trembl.fasta.gz")
    PigzClient.decompress("/tmp/uniprot_trembl.fasta.gz")
    with open("/tmp/uniprotkb.fasta", 'a') as uniprotkb_file:
        with open("/tmp/uniprot_sprot.fasta", 'r') as sprot_file:
            uniprotkb_file.writelines(sprot_file.readlines())
        with open("/tmp/uniprot_trembl.fasta", 'r') as trembl_file:
            uniprotkb_file.writelines(trembl_file.readlines())
    blast_client.makeblastdb("/tmp/uniprotkb.fasta", f"uniprotkb-{uniprot_client.release}")
    subprocess.run(f"tar --zstd -cf uniprotkb-{uniprot_client.release}.tar.zst /tmp/*uniprotkb-{uniprot_client.release}")
    s3_client.upload_file(f"/tmp/uniprotkb-{uniprot_client.release}.tar.zst", "codylemke-hpc", "biolink/uniprot")
    uniprot_client.download_uniref100("/tmp/uniref100.fasta.gz")
    PigzClient.decompress("/tmp/uniref100.fasta.gz")
    blast_client.makeblastdb("/tmp/uniref100.fasta", f"uniref100-{uniprot_client.release}")
    subprocess.run(f"tar --zstd -cf uniref100-{uniprot_client.release}.tar.zst /tmp/*uniref100-{uniprot_client.release}")
    s3_client.upload_file(f"/tmp/uniref100-{uniprot_client.release}.tar.zst", "codylemke-hpc", "biolink/uniprot")
    # Delete all temporary files

# Gather all input sequences
print("Gathering input sequences")
with open(data_dir / "input_accessions.txt", 'r') as file:
    input_accessions = [line.strip() for line in file.readlines() if line.strip()]
for accession in input_accessions:
    blast_client.get_fasta_entry(f"uniprot_kb-{uniprot_client.release}", accession, input_dir / f"{accession}.fasta")

# Sort Accessions By Kingdom
print("Sorting Accessions By Kingdom")
accessions_detail = uniprot_client.get_entries_details(input_accessions)
plant_accessions = [entry['primaryAccession'] for entry in accessions_detail if entry['organism']['lineage'][1] == 'Viridiplantae']
bacterial_accessions = [entry['primaryAccession'] for entry in accessions_detail if entry['organism']['lineage'][0] == 'Bacteria']
fungal_accessions = [entry['primaryAccession'] for entry in accessions_detail if entry['organism']['lineage'][1] == 'Fungi']

# Align sequences in each kingdom
print("Aligning sequences within each kingdom")
blast_client.get_fasta_entries(f"uniprot_kb-{uniprot_client.release}", plant_accessions, data_dir / "plant_sequences.fasta")
blast_client.get_fasta_entries(f"uniprot_kb-{uniprot_client.release}", bacterial_accessions, data_dir / "bacterial_sequences.fasta")
blast_client.get_fasta_entries(f"uniprot_kb-{uniprot_client.release}", fungal_accessions, data_dir / "fungal_sequences.fasta")
clustalo_client.align(data_dir / "plant_sequences.fasta", data_dir / "plant_sequences_alignment.fasta")
clustalo_client.align(data_dir / "bacterial_sequences.fasta", data_dir / "bacterial_sequences_alignment.fasta")
clustalo_client.align(data_dir / "fungal_sequences.fasta", data_dir / "fungal_sequences_alignment.fasta")

# Determine End Trimming of sequences for Blast Searches


# Blast all query sequences
print("Blasting all query sequences")
for fasta_file in blast_client.input_dir.glob("*.fasta"):
    blast_client.blastp(str(file), f"uniref100-{uniprot_client.release}")

# Create Set with all blast hits
print("Creating set with all blast hits")
output_files = [file for file in output_dir.iterdir() if file.is_file()]
hits = set()
for file in output_files:
    results = BlastResults(str(file))
    hits.update(set(results.hit_accessions))

# Create fasta file with all blast hits
print("Creating fasta file with all blast hits")
with open(root_dir / "hits.fasta", 'w') as file:
    fasta_entries = blast_client.get_fasta_entries(database, list(hits))
    file.write(fasta_entries)

# Align sequences in fasta file with MAFFT
mafftClient = MafftClient(output_dir, output_dir)
mafftClient.align("hits.fasta")
