#!/bin/bash

# Define Paths
FTP_URL="https://ftp.uniprot.org/pub/databases/uniprot/current_release"
S3_PATH="s3://codylemke-hpc/uniprot/ftp"

# Download gz files to S3
curl "$FTP_URL/relnotes.txt" | aws s3 cp - "$S3_PATH/relnotes.txt"
curl "$FTP_URL/knowledgebase/complete/uniprot_sprot.fasta.gz" | aws s3 cp - "$S3_PATH/uniprot_sprot.fasta.gz"
curl "$FTP_URL/knowledgebase/complete/uniprot_trembl.fasta.gz" | aws s3 cp - "$S3_PATH/uniprot_trembl.fasta.gz" --expected-size 70000000000
curl "$FTP_URL/uniref/uniref100/uniref100.fasta.gz" | aws s3 cp - "$S3_PATH/uniref100.fasta.gz" --expected-size 100000000000

# Load files, extract them, create blast database, compress them, and reupload them
aws s3 cp "$S3_PATH/uniprot_sprot.fasta.gz" "/tmp/uniprot_sprot.fasta.gz"
gzip -d "/tmp/uniprot_sprot.fasta.gz"


aws s3 cp "$S3_PATH/uniprot_trembl.fasta.gz" "/tmp/uniprot_trembl.fasta.gz"
gzip -d "/tmp/uniprot_trembl.fasta.gz"


aws s3 cp "$S3_PATH/uniref100.fasta.gz" "/tmp/uniref100.fasta.gz"
gzip -d "/tmp/uniref100.fasta.gz"
