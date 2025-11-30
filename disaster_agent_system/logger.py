"""
Logging utilities
"""

import time
from typing import List

LOGS: List[str] = []

def log_message(msg: str):
    ts = time.strftime("%H:%M:%S")
    entry = f"{ts} - {msg}"
    LOGS.append(entry)
    print(entry)
