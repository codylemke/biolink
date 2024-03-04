import pytest
from pathlib import Path
from biolink.models import FastaFile

@pytest.fixture
def fasta_file():
    file_path = Path(__file__).resolve().parent / "assets/input_sequences.fasta"
    return FastaFile(str(file_path))

def test_file_path(fasta_file: FastaFile):
    actual = fasta_file._file_path
    assert str(actual) == "/home/codylemke/repos/biolink/tests/models/assets/input_sequences.fasta"

def test_get_item(fasta_file: FastaFile):
    actual = fasta_file[0]
    assert actual.accession == "A0A023VSF1"
    
def test_len(fasta_file):
    actual = len(fasta_file)
    assert actual == 92
    
def test_iter(fasta_file):
    count = 0
    for fasta_entry in fasta_file:
        count += 1
        assert len(fasta_entry.accession) > 0
    assert count == 92
    