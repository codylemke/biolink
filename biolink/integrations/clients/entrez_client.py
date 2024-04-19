import logging
import httpx

class EntrezClient:
    logger = logging.getLogger("EntrezClient")
    
    def __init__(self):
        # Fields
        self._client: httpx.AsyncClient
        self.base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
        
        # Constructor
        self._client = httpx.AsyncClient()
        
    
    # Internal Methods
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._client.aclose()
        
    
    # Properties
    # N/A
    
    
    # Public Methods
    async def esearch(self, database: str, term: str, outfile: str=None) -> str:
        url = f"{self.base_url}/esearch.fcgi"
        params = {
            "db": database,
            "term": term,
        }
        response = await self._client.get(url, params=params)
        if not response.status_code == 200:
            raise httpx.HTTPError(f'{response.status_code}')
        data = response.text
        if outfile != None:
            with open(outfile, 'w') as file:
                file.write(data)
        return data
    
    
    async def esummary(self, database: str, id_list: str, outfile: str=None) -> str:
        url = f"{self.base_url}/esummary.fcgi"
        params = {
            "db": database,
            "id": id_list,
        }
        response = await self._client.get(url, params=params)
        if not response.status_code == 200:
            raise httpx.HTTPError(f'{response.status_code}')
        data = response.text
        if outfile != None:
            with open(outfile, 'w') as file:
                file.write(data)
        return data
    
    
    async def efetch(self, database: str, id_list: str, rettype: str=None, retmode: str=None, outfile: str=None) -> str:
        url = f"{self.base_url}/efetch.fcgi"
        params = {
            "db": database,
            "id": id_list,
        }
        if rettype is not None:
            params["rettype"] = rettype
        if retmode is not None:
            params["retmode"] = retmode
        response = await self._client.get(url, params=params)
        if not response.status_code == 200:
            raise httpx.HTTPError(f'{response.status_code}')
        data = response.text
        if outfile != None:
            with open(outfile, 'w') as file:
                file.write(data)
        return data
    
    
    async def elink(self, source_db: str, destination_db: str, id_list: str, outfile: str=None) -> str:
        url = f"{self.base_url}/elink.fcgi"
        params = {
            "dbfrom": source_db,
            "db": destination_db,
            "id": id_list,
        }
        response = await self._client.get(url, params=params)
        if not response.status_code == 200:
            raise httpx.HTTPError(f'{response.status_code}')
        data = response.text
        if outfile != None:
            with open(outfile, 'w') as file:
                file.write(data)
        return data
    
    
    async def einfo(self, db: str, outfile: str=None) -> str:
        url = f"{self.base_url}/einfo.fcgi"
        params = {
            "db": db
        }
        response = await self._client.get(url, params=params)
        if not response.status_code == 200:
            raise httpx.HTTPError(f'{response.status_code}')
        data = response.text
        if outfile != None:
            with open(outfile, 'w') as file:
                file.write(data)
        return data
    
    
    async def egquery(self, term: str, outfile: str=None) -> str:
        url = f"{self.base_url}/egquery.fcgi"
        params = {
            "term": term
        }
        response = await self._client.get(url, params=params)
        if not response.status_code == 200:
            raise httpx.HTTPError(f'{response.status_code}')
        data = response.text
        if outfile != None:
            with open(outfile, 'w') as file:
                file.write(data)
        return data
    
    
    async def espell(self, term: str, db: str, outfile: str=None) -> str:
        url = f"{self.base_url}/espell.fcgi"
        params = {
            "term": term,
            "db": db
        }
        response = await self._client.get(url, params=params)
        if not response.status_code == 200:
            raise httpx.HTTPError(f'{response.status_code}')
        data = response.text
        if outfile != None:
            with open(outfile, 'w') as file:
                file.write(data)
        return data
    