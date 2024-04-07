import logging
from biolink.models.chemistry.reaction import Reaction

class EnzymeClass:
    logger = logging.getLogger("Blast")
    
    def __init__(self):
        # Fields
        self.ec_number: int
        self.reaction: Reaction
        
        # Constructor
        # N/A
    
    # Internal Methods
    # N/A
    
    # Properties
    # N/A
    
    # Public Methods
    # N/A