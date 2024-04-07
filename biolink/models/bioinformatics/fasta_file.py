from __future__ import annotations
import json
from pathlib import Path
from typing import Dict, List, TextIO
from .fasta_entry import FastaEntry

class FastaFile:
    
    def __init__(self, contents: str):
        # Fields
        self._file: Path
        self.entries: List[FastaEntry]
        
        # Constructor
        self._file = None
        self._entries = []
        entry_lines = []
        for line in contents.splitlines():
            if line.startswith('>') and entry_lines:
                entry_str = '\n'.join(entry_lines)
                self.entries.append(FastaEntry(entry_str))
                entry_lines = [line.strip()]
            else:
                entry_lines.append(line.strip())
        if entry_lines:
            entry_str = '\n'.join(entry_lines)
            self.entries.append(FastaEntry(entry_str))
            
    
    
    # Internal Methods       
    def __len__(self):
        return len(self.entries)
    
    def __iter__(self):
        return iter(self.entries)
    
    def __getitem__(self, key):
        if isinstance(key, int):
            return self.entries[key]
        elif isinstance(key, str):
            return self.entries[self.accessions.index(key)]
        else:
            raise Exception()
        
    
    # Properties
    @property
    def accessions(self):
        return [entry.accession for entry in self.entries]
    
    
    # Public Methods  
    def append(self, entry: FastaEntry) -> None:
        self._entries.append(entry)
        
    
    @classmethod
    def parse_file(cls, file_path: str) -> FastaFile:    
        with open(file_path, 'r') as file:
            fasta_file = cls(file.read())
        return fasta_file
    
    
    def save(self, file=None) -> None:
        if file is not None:
            self._file = file
        if self._file is None:
            raise Exception("The file path was not specified.")
        with self._file.open("w") as file:
            for entry in self._entries:
                file.write(str(entry))