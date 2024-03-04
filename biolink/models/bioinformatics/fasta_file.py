import json
from pathlib import Path
from typing import Dict, List, TextIO
from .fasta_entry import FastaEntry

class FastaFile:
    def __init__(self, path: str):
        # Fields
        self._file_path: Path
        self._entries: List[FastaEntry]
        
        # Constructor
        self._file_path = Path(path).resolve()
        if not self._file_path.exists():
            self._file_path.touch()
        with self._file_path.open('r') as file:
            lines = ''.join(file.readlines())
            self._entries = [FastaEntry('>' + entry.rstrip()) for entry in lines.split('>')[1:]]
    
    
    # Internal Methods       
    def __len__(self):
        return len(self._entries)
    
    def __iter__(self):
        return iter(self._entries)
    
    def __getitem__(self, key):
        if isinstance(key, int):
            return self._entries[key]
        elif isinstance(key, str):
            return self._entries[self.accessions.index(key)]
        else:
            raise Exception()
        
    
    # Properties
    @property
    def accessions(self):
        return [entry.accession for entry in self._entries]
    
    @property
    def entries(self):
        return self._entries
    
    
    # Public Methods  
    def append(self, entry: FastaEntry) -> None:
        self._entries.append(entry)
            