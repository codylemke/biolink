import logging
import httpx
from bs4 import BeautifulSoup

class NCBIClient:
    logger = logging.getLogger("NCBIClient")
    
    def __init__(self):
        # Fields
        self._client: httpx.AsyncClient
        
        # Constructors
        self._client = httpx.AsyncClient()
        
    
    # Internal Methods 
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._client.aclose()
    
    
    # Properties
    # N/A
    
    
    # Public Methods
    def get_taxonomy(self, taxon_id: str):
        url = f'https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id={taxon_id}'
        response = self._client.get(url)
        soup = BeautifulSoup(response.text, 'lxml-html')
        root = soup.find('html')
        body = root.find('body', recursive=False)
        entry_data = body.title.find_next_sibling('table', recursive=False)
        tables  = entry_data.find_all('td')
        organism_table = tables[0]
        entrez_table = tables[1]
        response = {}
        # (TODO) - Get current name, NCBI Blast name, Rank, Genetic Code, and Mitochondrial genetic code
        # (TODO) - Switch to using the E-utilities API https://www.ncbi.nlm.nih.gov/books/NBK25501/
        
        # Parse Lineage
        lineage = {}
        phylogenies = organism_table.find('dl', recursive=False).find('dd', recursive=False).find_all('a', recursive=False)
        for phylogeny in phylogenies:
            level = phylogeny.get('title')
            classification = phylogeny.text
            lineage[level] = classification
        response["lineage"] = lineage
        # Parse Entrez Record Count
        records = {}
        entrez_records = entrez_table.find_all('tr')
        for entrez_record in entrez_records[2:]:
            columns = entrez_record.find_all('td', recursive=False)
            database_name = columns[0].find('span', recursive=False).text
            records[database_name] = {}
            records[database_name]["direct_links"] = int(columns[0].find('a', recursive=False).find('span', recursive=False).text)
            records[database_name]["link"] = columns[0].find('a', recursive=False).get('href')
        response["records"] = records
        return response