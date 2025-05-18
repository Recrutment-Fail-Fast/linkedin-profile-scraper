from dataclasses import dataclass
from typing import Optional, Dict

@dataclass
class ProspectStore:
    _instance = None
    prospect: Optional[Dict] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

prospect_store = ProspectStore()  # Create single instance 