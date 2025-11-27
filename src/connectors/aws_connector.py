from typing import List, Dict

class AWSConnector:
    """Handles connection to AWS using boto3"""

    def __init__(self, config):
        self.config = config
        # Will use boto3 to connect to AWS services
