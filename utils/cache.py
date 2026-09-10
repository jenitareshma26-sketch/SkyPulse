from __future__ import annotations
import json, time
from pathlib import Path
class JsonCache:
    """Small, fault-tolerant disk cache for network responses."""
    def __init__(self, path: Path): self.path = path
    def get(self, key: str, ttl: int):
        try:
            data = json.loads(self.path.read_text())
            item = data.get(key)
            return item["value"] if item and time.time() - item["time"] < ttl else None
        except (OSError, ValueError, KeyError): return None
    def set(self, key: str, value: object) -> None:
        try:
            data = json.loads(self.path.read_text()) if self.path.exists() else {}
            data[key] = {"time": time.time(), "value": value}; self.path.write_text(json.dumps(data))
        except OSError: pass

