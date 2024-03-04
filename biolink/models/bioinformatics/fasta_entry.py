class FastaEntry:
    def __init__(self, text: str):
        content = text.split('\n')
        self.header = content[0]
        self.accession = self.header.split('|')[1]
        self.sequence = ''.join(content[1:])
        self.type: str = ''
        
    # Internal Functions
    def __len__(self):
        return len(self.sequence)
    