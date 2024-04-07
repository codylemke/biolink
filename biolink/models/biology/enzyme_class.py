from biolink.models.chemistry.reaction import Reaction

class EnzymeClass:
    def __init__(self):
        self.ec_number: int
        self.reaction: Reaction