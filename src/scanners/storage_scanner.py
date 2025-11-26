from typing import List, Dict

class StorageScanner:
    def __init__(self, connector):
        self.connector = connector
    async def scan(self) -> List[Dict]:
        return []
