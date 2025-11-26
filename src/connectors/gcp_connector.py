from typing import List, Dict
import asyncio

class GCPConnector:
    def __init__(self, config):
        self.config = config
        self.project_id = config.project_id

    async def list_iam_policies(self) -> List[Dict]:
        return []

    async def list_compute_instances(self) -> List[Dict]:
        return []
