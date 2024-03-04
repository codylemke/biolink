import httpx
from bs4 import BeautifulSoup
from biolink.models import Taxonomy

class NCBIClient:
    def __init__(self):
        self._client: httpx.AsyncClient = httpx.AsyncClient()
        self._client.get()
    
    # Internal Methods 
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._client.aclose()
        
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
        taxonomy = Taxonomy()
        # Parse Phylogeny
        lineage = organism_table.find('dl', recursive=False).find('dd', recursive=False).find_all('a', recursive=False)
        for phylogeny in lineage:
            level = phylogeny.get('title')
            classification = phylogeny.text
            match level:
                case 'no rank':
                    pass
                case 'superkingdom':
                    taxonomy.superkingdom = classification
                case 'kingdom':
                    taxonomy.kingdom = classification
                case 'subkingdom':
                    taxonomy.subkingdom = classification
                case 'superphylum':
                    taxonomy.superphylum = classification
                case 'phylum':
                    taxonomy.phylum = classification
                case 'subphylum':
                    taxonomy.subphylum = classification
                case 'superclass':
                    taxonomy.superclass = classification
                case 'class':
                    taxonomy._class = classification
                case 'subclass':
                    taxonomy.subclass = classification
                case 'infraclass':
                    taxonomy.infraclass = classification
                case 'cohort':
                    taxonomy.cohort = classification
                case 'superorder':
                    taxonomy.superorder = classification
                case 'order':
                    taxonomy.order = classification
                case 'suborder':
                    taxonomy.suborder = classification
                case 'infraorder':
                    taxonomy.infraorder = classification
                case 'parvorder':
                    taxonomy.parvorder = classification
                case 'superfamily':
                    taxonomy.superfamily = classification
                case 'family':
                    taxonomy.family = classification
                case 'subfamily':
                    taxonomy.subfamily = classification
                case 'supertribe':
                    taxonomy.supertribe = classification
                case 'tribe':
                    taxonomy.tribe = classification
                case 'subtribe':
                    taxonomy.subtribe = classification
                case 'genus':
                    taxonomy.genus = classification
                case 'subgenus':
                    taxonomy.subgenus = classification
                case 'species_group':
                    taxonomy.species_group = classification
                case 'species_subgroup':
                    taxonomy.species_subgroup = classification
                case 'species':
                    taxonomy.species = classification
                case 'subspecies':
                    taxonomy.subspecies = classification
                case 'clade':
                    taxonomy.clades.append(classification)
                case _:
                    raise Exception(f"Unknown level: {level}")
        # Parse Entrez Record Count
        entrez_records = entrez_table.find_all('tr')
        for entrez_record in entrez_records[2:]:
            columns = entrez_record.find_all('td', recursive=False)
            database_name = columns[0].find('span', recursive=False).text
            direct_links = columns[0].find('a', recursive=False).find('span', recursive=False).text
            link = columns[0].find('a', recursive=False).get('href')
            taxonomy.entrez_records[database_name] = direct_links
        return taxonomy