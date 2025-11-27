from typing import List, Dict

class AzureConnector:
    """Azure cloud connector using azure-sdk"""

    def __init__(self, config):
        self.config = config
        # Setup Azure SDK connection
