import re

class FastaEntry:
    
    def __init__(self, text: str):
        # Fields
        self._header: str
        self._database: str
        self.sequence: str
        
        # Constructor
        content = text.split('\n')
        self._header = content[0]
        self._database = None
        self.sequence = ''.join(content[1:])
    
    
    # Internal Functions
    def __len__(self):
        return len(self.sequence)
    
    def __str__(self):
        split_sequence = []
        for i in range(0, len(self.sequence), 80):
            split_sequence.append(self.sequence[i:i+80])
        return f"{self._header}\n{'\n'.join(split_sequence)}"
    
    
    # Properties
    @property
    def database(self) -> str:
        if self._database is None:
            if self._header.startswith(">sp"):
                self._database = "SwissProt"
            elif self._header.startswith(">tr"):
                self._database = "TrEMBL"
            elif self._header.startswith(">UniRef100"):
                self._database = "UniRef100"
            elif self._header.startswith(">UniRef90"):
                self._database = "UniRef90"
            elif self._header.startswith(">UniRef50"):
                self._database = "UniRef50"
            elif "NM_" in self._header or "NP_" in self._header or "XM_" in self._header or "XP_" in self._header:
                self._database = "RefSeq"
            elif self._header.startswith(">ENST") or self._header.startswith(">ENSP") or self._header.startswith(">ENA"):
                self._database = "Ensembl"
            else:
                self._database = "Generic"
        else:
            return self._database
    
    @property
    def accession(self) -> str:
        if self.database == "SwissProt" or self.database == "TrEMBL":
            return re.search(r'\|(.*?)\|', self._header).group(0)
        elif self.database.startswith("UniRef"):
            return re.search(r'^>(UniRef\d+_[A-Za-z0-9]+)', self._header).group(0)
        elif self.database == "RefSeq":
            return re.search(r'^>(.*?) ', self._header).group(0)
        elif self.database == "Ensembl":
            raise Exception("Ensembl fasta header parser is not yet written")
        elif self.database == "Generic":
            return re.search(r'^>(.*?) ', self._header).group(0)
        
    @property
    def name(self) -> str:
        if self.database == "SwissProt" or self.database == "TrEMBL":
            return re.search(r'\|(.*?) ', self._header).group(0)
        else:
            return self.accession
    
    @property
    def description(self) -> str:
        if self.database == "SwissProt" or self.database == "TrEMBL":
            return re.search(r' (.*?) OS=', self._header).group(0)
        elif self.database.startswith("UniRef"):
            return re.search(r' (.*?) n=', self._header).group(0)
        elif self.database == "RefSeq":
            return re.search(r' (.*)', self._header).group(0)
        elif self.database == "Ensembl":
            raise Exception("Ensembl fasta header parser is not yet written")
        elif self.database == "Generic":
            return re.search(r' (.*)', self._header).group(0)
    
    @property
    def species(self) -> str:
        if self.database == "SwissProt" or self.database == "TrEMBL":
            return re.search(r'OS=(.*?) OX=', self._header).group(0)
        elif self.database.startswith("UniRef"):
            return re.search(r'Tax=(.*?) TaxID=', self._header).group(0)
        elif self.database == "RefSeq":
            return None
        elif self.database == "Ensembl":
            raise Exception("Ensembl fasta header parser is not yet written")
        elif self.database == "Generic":
            return None
    
    @property
    def taxid(self) -> str:
        if self.database == "SwissProt" or self.database == "TrEMBL":
            return re.search(r'OX=(\d+) GN=', self._header).group(0)
        elif self.database.startswith("UniRef"):
            return re.search(r'TaxID=(\d+) RepID=', self._header).group(0)
        elif self.database == "RefSeq":
            return None
        elif self.database == "Ensembl":
            raise Exception("Ensembl fasta header parser is not yet written")
        elif self.database == "Generic":
            return None
    
    @property
    def gene_name(self) -> str:
        if self.database == "SwissProt" or self.database == "TrEMBL":
            return re.search(r'GN=(.*?) PE=', self._header).group(0)
        elif self.database.startswith("UniRef"):
            return None
        elif self.database == "RefSeq":
            return None
        elif self.database == "Ensembl":
            raise Exception("Ensembl fasta header parser is not yet written")
        elif self.database == "Generic":
            return None
    
    @property
    def protein_existence(self) -> int:
        if self.database == "SwissProt" or self.database == "TrEMBL":
            return int(re.search(r' PE=(\d+) ', self._header).group(0))
        elif self.database.startswith("UniRef"):
            return None
        elif self.database == "RefSeq":
            return None
        elif self.database == "Ensembl":
            raise Exception("Ensembl fasta header parser is not yet written")
        elif self.database == "Generic":
            return None
    
    @property
    def sequence_version(self) -> int:
        if self.database == "SwissProt" or self.database == "TrEMBL":
            return int(re.search(r'SV=(\d+)$', self._header).group(0))
        elif self.database.startswith("UniRef"):
            return None
        elif self.database == "RefSeq":
            return None
        elif self.database == "Ensembl":
            raise Exception("Ensembl fasta header parser is not yet written")
        elif self.database == "Generic":
            return None
        
    @property
    def sequences_in_cluster(self) -> int:
        if self.database == "SwissProt" or self.database == "TrEMBL":
            return None
        elif self.database.startswith("UniRef"):
            return int(re.search(r'n=(\d+) Tax=', self._header).group(0))
        elif self.database == "RefSeq":
            return None
        elif self.database == "Ensembl":
            raise Exception("Ensembl fasta header parser is not yet written")
        elif self.database == "Generic":
            return None
        
    @property
    def rep_id(self) -> str:
        if self.database == "SwissProt" or self.database == "TrEMBL":
            return None
        elif self.database.startswith("UniRef"):
            return int(re.search(r'RepID=(.*?)$', self._header).group(0))
        elif self.database == "RefSeq":
            return None
        elif self.database == "Ensembl":
            raise Exception("Ensembl fasta header parser is not yet written")
        elif self.database == "Generic":
            return None
    
    
    # Public Methods
    # N/A
            