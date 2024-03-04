import pytest
from lxml import etree
from biolink.integrations import UniprotClient

@pytest.fixture
def client_fixture() -> UniprotClient:
    return UniprotClient()

def test_get_uniprot_relnotes():
    release = UniprotClient.get_uniprot_release()
    assert release == '2024_01'


@pytest.mark.asyncio
@pytest.mark.parametrize("accession,expected", [
    ("P12345", "P12345"),
    ("P12346", "P12346")
])
async def test_get_entry(accession: str, expected: str, client_fixture: UniprotClient):
    fasta_entry = await client_fixture.get_entry(accession)
    assert fasta_entry.accession == expected


@pytest.mark.asyncio
@pytest.mark.parametrize("accession,expected", [
    ("P12345", "P12345"),
    ("P12346", "P12346")
])
async def test_get_entry_details(accession: str, expected: str, client_fixture: UniprotClient):
    actual = await client_fixture.get_entry_details(accession)
    assert actual['primaryAccession'] == expected

    
@pytest.mark.asyncio
async def test_get_entries(uniprot_client: UniprotClient):
    actual = await uniprot_client.get_entries(['P12345', 'P12346'])
    assert len(actual) == 2
    assert actual[0].accession == 'P12345'
    assert actual[1].accession == 'P12346'
    

@pytest.mark.asyncio
async def test_get_entries_details(uniprot_client: UniprotClient):
    actual = await uniprot_client.get_entries_details(['P12345', 'P12346'])
    assert len(actual) == 2
    assert actual[0]['primaryAccession'] == 'P12345'
    assert actual[1]['primaryAccession'] == 'P12346'