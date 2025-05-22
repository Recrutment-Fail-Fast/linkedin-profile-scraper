from dataclasses import dataclass
from models import Prospect

@dataclass
class ProspectStore:
    _instance = None
    prospect: Prospect = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

prospect_store = ProspectStore()   