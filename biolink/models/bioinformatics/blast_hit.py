class BlastHit:
    
    def __init__(self, line: str):
        # Fields
        self.subject_accession: str
        self.percent_identity: float
        self.percent_positive: float
        self.alignment_length: int
        self.subject_length: int
        self.query_coverage: float
        self.gap_openings: int
        self.query_start: int
        self.query_end: int
        self.subject_start: int
        self.subject_end: int
        self.e_value: float
        self.bit_score: float
        
        # Constructor
        data = line.strip().split(',')
        self.subject_accession = data[0]
        self.percent_identity = float(data[1])
        self.percent_positive = float(data[2])
        self.alignment_length = int(data[3])
        self.subject_length = int(data[4])
        self.query_coverage = float(data[5])
        self.gap_openings = int(data[6])
        self.query_start = int(data[7])
        self.query_end = int(data[8])
        self.subject_start = int(data[9])
        self.subject_end = int(data[10])
        self.e_value = float(data[11])
        self.bit_score = float(data[12])