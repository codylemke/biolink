#!/bin/bash
# s3://codylemke-hpc/biolink/uniprot

# Validate Argument -------------------------------------------------------------------------------
if [ -z "$1" ]; then
    echo "Argument Null Error: Please provide the path to your s3 folder for storing blast databases." >&2
    exit 1
fi
if aws s3 ls "$1" > /dev/null; then
    echo "Connection to S3 bucket confirmed."
else
    echo "Argument Error: The s3 path provided is invalid or cannot be reached."
    exit 1
fi

# Define Run Constants ----------------------------------------------------------------------------
S3_BLAST_DIR="$1"
UNIPROT_FTP_URL="https://ftp.uniprot.org/pub/databases/uniprot/current_release"

# Check Status Of Prepared Blast Databases --------------------------------------------------------
current_uniprot_release=$(curl -s "${UNIPROT_FTP_URL}/relnotes.txt" | awk 'NR==1 {print $3}')
echo "Current Uniprot Release: $current_uniprot_release"
if aws s3 ls "${S3_BLAST_DIR}"/relnotes.txt; then
    prepared_databases_release=$(curl -s "${S3_BLAST_DIR}/relnotes.txt" | awk 'NR==1 {print $3}')
    echo "Prepared Blast Databases Release: $prepared_databases_release"
    if [[ $current_uniprot_release > $prepared_databases_release ]]; then
        echo "Prepared Databases are out of date"
        swissprot_db_updated=1
        trembl_db_updated=1
        uniprotkb_db_updated=1
        uniref100_db_updated=1
    elif [[ "$current_uniprot_release" == "$prepared_databases_release" ]]; then
        echo "Prepared Databases are up to date"
    else
        echo "An unknown error occurred when checking status of prepared blast databases."
    fi
fi
if aws s3 ls "${S3_BLAST_DIR}/swissprot-${current_uniprot_release}.tar.zst"; then
    echo "swissprot-${current_uniprot_release}.tar.zst was found"
    swissprot_db_updated=0
else
    echo "swissprot-${current_uniprot_release}.tar.zst was not found"
    swissprot_db_updated=1
fi
if aws s3 ls "${S3_BLAST_DIR}/trembl-${current_uniprot_release}.tar.zst"; then
    echo "trembl-${current_uniprot_release}.tar.zst was found"
    trembl_db_updated=0
else
    echo "trembl-${current_uniprot_release}.tar.zst was not found"
    trembl_db_updated=1
fi
if aws s3 ls "${S3_BLAST_DIR}/uniprotkb-${current_uniprot_release}.tar.zst"; then
    echo "uniprotkb-${current_uniprot_release}.tar.zst was found"
    uniprotkb_db_updated=0
else
    echo "uniprotkb-${current_uniprot_release}.tar.zst was not found"
    uniprotkb_db_updated=1
fi
if aws s3 ls "${S3_BLAST_DIR}/uniref100-${current_uniprot_release}.tar.zst"; then
    echo "uniref100-${current_uniprot_release}.tar.zst was found"
    uniref100_db_updated=0
else
    echo "uniref100-${current_uniprot_release}.tar.zst was not found"
    uniref100_db_updated=1
fi

# Download .gz Files For Outdated Databases -------------------------------------------------------
if [[ $swissprot_db_updated -eq 1 ]]; then
    curl "${UNIPROT_FTP_URL}/knowledgebase/complete/uniprot_sprot.fasta.gz" -o "/tmp/uniprot_sprot.fasta.gz"
    gzip -d "/tmp/uniprot_sprot.fasta.gz"
    if makeblastdb -dbtype prot -in "/tmp/uniprot_sprot.fasta" -title "swissprot-${current_uniprot_release}" -out "/tmp/swissprot-${current_uniprot_release}" -logfile "/tmp/swissprot-${current_uniprot_release}.log" -parse_seqids -hash_index; then
        if [[ $uniprotkb_db_updated -eq 1 ]]; then
            touch "/tmp/uniprotkb.fasta"
            cat "/tmp/uniprot_sprot.fasta" > "/tmp/uniprotkb.fasta"
        fi
        rm "/tmp/uniprot_sprot.fasta"
    fi
    tar -cf - "/tmp/swissprot-${current_uniprot_release}"/* | zstd -o "/tmp/swissprot-${current_uniprot_release}.tar.zst"
    if aws s3 cp "/tmp/swissprot-${current_uniprot_release}.tar.zst" "${S3_BLAST_DIR}/swissprot-${current_uniprot_release}.tar.zst"; then
        rm "/tmp/swissprot-${current_uniprot_release}.tar.zst"
    fi
fi

if [[ $trembl_db_updated -eq 1 ]]; then
    curl "${UNIPROT_FTP_URL}/knowledgebase/complete/uniprot_trembl.fasta.gz" -o "/tmp/uniprot_trembl.fasta.gz"
    gzip -d "/tmp/uniprot_trembl.fasta.gz"
    if makeblastdb -dbtype prot -in "/tmp/uniprot_trembl.fasta" -title "trembl-${current_uniprot_release}" -out "/tmp/trembl-${current_uniprot_release}" -logfile "/tmp/trembl-${current_uniprot_release}.log" -parse_seqids -hash_index; then
        if [[ $uniprotkb_db_updated -eq 1 ]]; then
            cat "/tmp/uniprot_trembl.fasta" > "/tmp/uniprotkb.fasta"
        fi
        rm "/tmp/uniprot_trembl.fasta"
    fi
    tar -cf - "/tmp/trembl-${current_uniprot_release}"/* | zstd -o "/tmp/trembl-${current_uniprot_release}.tar.zst"
    if aws s3 cp "/tmp/trembl-${current_uniprot_release}.tar.zst" "${S3_BLAST_DIR}/trembl-${current_uniprot_release}.tar.zst"; then
        rm "/tmp/trembl-${current_uniprot_release}.tar.zst"
    fi
fi

if [[ $uniprotkb_db_updated -eq 1 ]]; then
    if makeblastdb -dbtype prot -in "/tmp/uniprotkb.fasta" -title "uniprotkb-${current_uniprot_release}" -out "/tmp/uniprotkb-${current_uniprot_release}" -logfile "/tmp/uniprotkb-${current_uniprot_release}.log" -parse_seqids -hash_index; then
        rm "/tmp/uniprotkb.fasta"
    fi
    tar -cf - "/tmp/uniprotkb-${current_uniprot_release}"/* | zstd -o "/tmp/uniprotkb-${current_uniprot_release}.tar.zst"
    if aws s3 cp "/tmp/uniprotkb-${current_uniprot_release}.tar.zst" "${S3_BLAST_DIR}/uniprotkb-${current_uniprot_release}.tar.zst"; then
        rm "/tmp/uniprotkb-${current_uniprot_release}.tar.zst"
    fi
fi

if [[ $uniref100_db_updated -eq 1 ]]; then
    curl "$UNIPROT_FTP_URL/uniref/uniref100/uniref100.fasta.gz" -o "/tmp/uniref100.fasta.gz"
    gzip -d "/tmp/uniref100.fasta.gz"
    if makeblastdb -dbtype prot -in "/tmp/uniref100.fasta" -title "uniref100-${current_uniprot_release}" -out "/tmp/uniref100-${current_uniprot_release}" -logfile "/tmp/uniref100-${current_uniprot_release}.log" -parse_seqids -hash_index; then
        rm "/tmp/uniref100.fasta"
    fi
    tar -cf - "/tmp/uniref100-${current_uniprot_release}"/* | zstd -o "/tmp/uniref100-${current_uniprot_release}.tar.zst"
    if aws s3 cp "/tmp/uniref100-${current_uniprot_release}.tar.zst" "${S3_BLAST_DIR}/uniref100-${current_uniprot_release}.tar.zst"; then
        rm "/tmp/uniref100-${current_uniprot_release}.tar.zst"
    fi
fi

curl "$UNIPROT_FTP_URL/relnotes.txt" | aws s3 cp - "$S3_BLAST_DIR/relnotes.txt"

echo "Blast Databases Prepared Successfully For Uniprot Release: $current_uniprot_release"