from typing import List, Dict

class NetworkScanner:
    def __init__(self, connector):
        self.connector = connector
    async def scan(self) -> List[Dict]:
        return []
