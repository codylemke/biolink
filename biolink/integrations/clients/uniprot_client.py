from ftplib import FTP
import asyncio
import logging
import time
import httpx
from typing import List
import json
import os
import re
import sys

class UniprotClient:
    logger = logging.getLogger("UniprotClient")
    semaphor = asyncio.Semaphore(10)
    
    def __init__(self):
        # Fields
        self._client: httpx.AsyncClient
        self._release: str
        
        # Constructure
        self._client = httpx.AsyncClient()
        self._release = None
    
    
    # Internal Methods 
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._client.aclose()
    
    async def _download_ftp_file(self, ftp_path: str, filename: str, local_path: str) -> None:
        def handle_binary(more_data):
            local_file.write(more_data)
            current_size = local_file.tell()
            percent_complete = (current_size / total_size) * 100
            sys.stdout.write(f"\rDownloading {filename}: {percent_complete:.2f}%")
            sys.stdout.flush()
        
        with FTP('ftp.uniprot.org') as ftp_client:
            ftp_client.login()
            ftp_client.cwd(ftp_path)
            total_size = ftp_client.size(filename)
            with open(os.path.join(local_path, filename), 'wb') as local_file:
                ftp_client.retrbinary(f'RETR {filename}', handle_binary)
                self.logger.info(f"\nDownloaded {filename} to {local_path}")
    
    
    # Properties
    @property
    def release(self):
        if self._release == None:
            self.release = UniprotClient.get_uniprot_release()
        return self._release
    
    
    # Public Methods
    @staticmethod
    def get_uniprot_release():
        content = []
        with FTP('ftp.uniprot.org') as ftp_client:
            ftp_client.login()
            ftp_path = '/pub/databases/uniprot/current_release'
            ftp_client.cwd(ftp_path)
            filename = 'relnotes.txt'
            ftp_client.retrlines(f'RETR {filename}', lambda line: content.append(line))
        return content[0].split(' ')[2]
    
    # FTP Methods
    async def download_relnotes(self, local_path: str) -> None:
        ftp_path = '/pub/databases/uniprot/current_release'
        filename = 'relnotes.txt'
        self._download_ftp_file(ftp_path, filename, local_path)
    
    async def download_uniprot_sprot(self, local_path: str) -> None:
        ftp_path = '/pub/databases/uniprot/current_release/knowledgebase/complete/'
        filename = 'uniprot_sprot.fasta.gz'
        self._download_ftp_file(ftp_path, filename, local_path)
    
    async def download_uniprot_trembl(self, local_path: str) -> None:
        ftp_path = '/pub/databases/uniprot/current_release/knowledgebase/complete/'
        filename = 'uniprot_trembl.fasta.gz'
        self._download_ftp_file(ftp_path, filename, local_path)
    
    async def download_uniref100(self, local_path: str) -> None:
        ftp_path = '/pub/databases/uniprot/current_release/uniref/uniref100/'
        filename = 'uniref100.fasta.gz'
        self._download_ftp_file(ftp_path, filename, local_path)
        
    async def download_uniref90(self, local_path: str) -> None:
        ftp_path = '/pub/databases/uniprot/current_release/uniref/uniref90/'
        filename = 'uniref90.fasta.gz'
        self._download_ftp_file(ftp_path, filename, local_path)
    
    async def download_uniref50(self, local_path: str) -> None:
        ftp_path = '/pub/databases/uniprot/current_release/uniref/uniref50/'
        filename = 'uniref50.fasta.gz'
        self._download_ftp_file(ftp_path, filename, local_path)
    
    # HTTP Methods
    async def get_entry(self, entry_id: str, outfmt: str="fasta", compressed: bool=False, outfile: str=None) -> str:
        if entry_id.startswith("UniRef"):
            database = 'uniref'
        elif entry_id.startswith('UPI'):
            database = 'uniparc'
        else:
            database = 'uniprotkb'
        url = f'https://rest.uniprot.org/{database}/{entry_id}'
        params = {
            'format': outfmt,
            'compressed': compressed,
        }
        response = await self._client.get(url, params=params)
        if not response.status_code == 200:
            raise httpx.HTTPError(f'{response.status_code}')
        data = response.text
        if outfile != None:
            with open(outfile, 'w') as file:
                file.write(data)
        return data
    
    
    async def get_entries(self, entry_ids: List[str], outfmt: str="fasta", compressed: bool=False, outfile: str=None) -> str:
        if entry_ids[0].startswith("UniRef100"):
            from_database = "UniRef100"
            to_database = "UniRef100"
        elif entry_ids[0].startswith("UniRef90"):
            from_database = "UniRef90"
            to_database = "UniRef90"
        elif entry_ids[0].startswith("UniRef50"):
            from_database = "UniRef50"
            to_database = "UniRef50"
        elif entry_ids[0].startswith('UPI'):
            from_database = "UniParc"
            to_database = "UniParc"
        else:
            from_database = "UniProtKB_AC-ID"
            to_database = "UniProtKB"
        return await self.run_id_mapping(entry_ids, from_database, to_database, outfmt=outfmt, compressed=compressed, outfile=outfile)
    
    
    async def query(self) -> str:
        pass
    
    
    async def run_id_mapping(self, entry_ids: List[str], from_database: str='UniProtKB_AC-ID', to_database: str='UniProtKB', outfmt: str="fasta", compressed: bool=False, outfile: str=None) -> str:
        # https://rest.uniprot.org/configure/idmapping/fields
        self.logger.info(f"Starting ID Mapping for {entry_ids}")
        batch_size = 9500
        batches = (entry_ids[i:i + batch_size] for i in range(0, len(entry_ids), batch_size))
        results = []
        failed_ids = []
        for batch in batches:
            # Run Request
            url = "https://rest.uniprot.org/idmapping/run"
            data = {
                'from': from_database,
                'to': to_database,
                'ids': batch
            }
            response = await self._client.post(url, data=data)
            json_response = json.loads(response.text)
            job_id = json_response['jobId']
            self.logger.info(f"Run request jobId: {job_id}")
            # Status Request
            url = f"https://rest.uniprot.org/idmapping/status/{job_id}"
            job_status = str()
            while job_status != 'FINISHED':
                response = await self._client.get(url)
                parsed_response = json.loads(response.text)
                job_status = parsed_response['jobStatus']
                time.sleep(1)
            # Results Request
            if to_database == "UniProtKB":
                rest_database = "uniprotkb"
            elif to_database.startswith("UniRef"):
                rest_database = "uniref"
            elif to_database == "UniParc":
                rest_database = "uniparc"
            else:
                raise Exception(f"? {to_database}")
            url = f'https://rest.uniprot.org/idmapping/{rest_database}/results/{job_id}'
            params = {
                'format': outfmt,
                'compressed': compressed,
                'size': 500,
            }
            response = await self._client.get(url, params=params)
            # Parse Paginated Results
            data = response.text
            if outfmt == "json":
                json_data = json.loads(data)
                if json_data.get("results"):
                    results.extend(json_data["results"])
                if json_data.get("failedIds"):
                    failed_ids.extend(json_data["failedIds"])
            else:
                results.append(data)
            while (link := response.headers.get("Link")) is not None:
                url = re.search(r'<([^>]+)>', link).group(1)
                response = await self._client.get(url, params=params)
                data = response.text
                if outfmt == "json":
                    json_data = json.loads(data)
                    if json_data.get("results"):
                        results.extend(json_data["results"])
                    if json_data.get("failedIds"):
                        failed_ids.extend(json_data["failedIds"])
                else:
                    results.append(data)
        if outfmt == "json":
            output = {}
            output["results"] = results
            output["failedIds"] = failed_ids
            output = json.dumps(output)
        else:
            output = "".join(results)
        if outfile != None:
            with open(outfile, 'w') as file:
                file.write(output)
        return output
    