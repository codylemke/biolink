from ftplib import FTP
import time
import httpx
import asyncio
import re
from typing import Any, Dict, List
import math
from lxml import etree
import json
import os
import sys
from biolink.models import FastaEntry

class UniprotClient:
    def __init__(self):
        self._client: httpx.AsyncClient = httpx.AsyncClient()
        self._release: str = None
    
    # Internal Methods 
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._client.aclose()
    
    def _download_ftp_file(self, ftp_path: str, filename: str, local_path: str):
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
                print(f"\nDownloaded {filename} to {local_path}")
    
    async def _get_entry(self, entry_id:str, outfmt:str='fasta', compressed:bool=False, outfile=None) -> str:
        if 'uniref' in entry_id.lower():
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
            with open(f"{outfile}", 'w') as file:
                file.write(data)
        return data
        
    async def _run_id_mapping(self, entry_ids:List[str], from_database:str='UniProtKB_AC-ID', to_database:str='UniProtKB', outfmt:str="fasta", compressed:bool=False, outfile=None) -> List[str]:
        batch_size = 9500
        batches = (entry_ids[i:i + batch_size] for i in range(0, len(entry_ids), batch_size))
        results = []
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
            # Status Request
            url = f"https://rest.uniprot.org/idmapping/status/{job_id}"
            job_status = str()
            while job_status != 'FINISHED':
                response = await self._client.get(url)
                parsed_response = json.loads(response.text)
                job_status = parsed_response['jobStatus']
                time.sleep(1)
            # Results Request
            url = f'https://rest.uniprot.org/idmapping/uniprotkb/results/{job_id}'
            params = {
                'format': outfmt,
                'compressed': compressed,
            }
            response = await self._client.get(url, params=params)
            if outfile != None:
                with open(outfile, 'w') as file:
                    file.write(response.text)
            results.append(response.text)
        return ''.join(results)
    
    
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
    def download_relnotes(self, local_path: str):
        ftp_path = '/pub/databases/uniprot/current_release'
        filename = 'relnotes.txt'
        self._download_ftp_file(ftp_path, filename, local_path)
    
    def download_uniprot_sprot(self, local_path: str):
        ftp_path = '/pub/databases/uniprot/current_release/knowledgebase/complete/'
        filename = 'uniprot_sprot.fasta.gz'
        self._download_ftp_file(ftp_path, filename, local_path)
    
    def download_uniprot_trembl(self, local_path: str):
        ftp_path = '/pub/databases/uniprot/current_release/knowledgebase/complete/'
        filename = 'uniprot_trembl.fasta.gz'
        self._download_ftp_file(ftp_path, filename, local_path)
    
    def download_uniref100(self, local_path: str):
        ftp_path = '/pub/databases/uniprot/current_release/uniref/uniref100/'
        filename = 'uniref100.fasta.gz'
        self._download_ftp_file(ftp_path, filename, local_path)
        
    def download_uniref90(self, local_path: str):
        ftp_path = '/pub/databases/uniprot/current_release/uniref/uniref90/'
        filename = 'uniref90.fasta.gz'
        self._download_ftp_file(ftp_path, filename, local_path)
    
    def download_uniref50(self, local_path: str):
        ftp_path = '/pub/databases/uniprot/current_release/uniref/uniref50/'
        filename = 'uniref50.fasta.gz'
        self._download_ftp_file(ftp_path, filename, local_path)
    
    # HTTP Methods
    async def get_entry(self, entry_id:str, compressed:bool=False, outfile=None) -> FastaEntry:
        data = await self._get_entry(entry_id, 'fasta', compressed, outfile)
        return FastaEntry(data)
    
    async def get_entry_details(self, entry_id:str, compressed:bool=False, outfile=None) -> Dict[str, Any]:
        data = await self._get_entry(entry_id, 'json', compressed, outfile)
        return json.loads(data)
    
    async def get_entries(self, entry_ids: List[str], compressed: bool=False, outfile=None) -> List[FastaEntry]:
        data = await self._run_id_mapping(entry_ids, 'fasta', compressed, outfile)
        return data
    
    async def get_entries_details(self, entry_ids: List[str], compressed: bool=False, outfile=None) -> List[Dict[str, Any]]:
        data = await self._run_id_mapping(entry_ids, 'json', compressed, outfile)
        return json.loads(data)
