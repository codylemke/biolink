from __future__ import annotations
import logging
from pathlib import Path
from typing import List
from .fasta_entry import FastaEntry

class FastaFile:
    logger = logging.getLogger("FastaFile")
    
    def __init__(self, contents: str):
        # Fields
        self._logger: logging.Logger
        self._file_path: Path
        self.entries: List[FastaEntry]
        
        # Constructor
        self._logger = logging.getLogger(self.__class__.__name__)
        self._file_path = None
        self.entries = []
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
    def accessions(self) -> List[str]:
        return [entry.accession for entry in self.entries]
    
    @property
    def file_path(self) -> str:
        return str(self._file_path.absolute())
    
    @file_path.setter
    def file_path(self, value) -> None:
        self._file_path = Path(value)
    
    
    # Public Methods  
    def append(self, entry: FastaEntry) -> None:
        self.entries.append(entry)
        
    
    @classmethod
    def parse_file(cls, file_path: str) -> FastaFile:    
        with open(file_path, 'r') as file:
            fasta_file = cls(file.read())
            fasta_file.file_path = file_path
        return fasta_file
    
    
    def save(self, file_path: str=None) -> None:
        if file_path is not None:
            self.file_path = file_path
        if self._file_path is None:
            raise Exception("The file path was not specified.")
        with self._file_path.open("w") as file:
            for entry in self.entries:
                file.write(str(entry))
                file.write('\n')
                