from pathlib import Path
from typing import List

class ClustalFile:
    
    def __init__(self, file_path: str):
        # Fields
        self._file_path: Path
        self._entries: List[str]
        
        # Constructor
        self._file_path = Path(file_path).resolve()
        if not self._file_path.exists():
            self._file_path.touch()