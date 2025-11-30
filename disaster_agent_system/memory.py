"""
Long-term memory storage for disaster reports
"""

import time
from typing import List, Dict, Any
from .logger import log_message

class InMemLongTermMemory:
    def __init__(self):
        self.store: Dict[str, Dict[str, Any]] = {}
        log_message("🧠 Long-term memory initialized")

    def add_reports(self, reports: List[Dict[str, Any]]):
        for r in reports:
            if r.get('status') in ('SYNTHESIZED', 'LOCATED'):
                r_copy = r.copy()
                r_copy['timestamp'] = time.time()
                self.store[r_copy['id']] = r_copy

    def retrieve_recent(self, num_reports: int = 1) -> List[Dict[str, Any]]:
        return sorted(self.store.values(), key=lambda x: x.get('timestamp', 0), reverse=True)[:num_reports]
