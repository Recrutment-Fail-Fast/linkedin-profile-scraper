from typing import TypedDict


class ProspectData(TypedDict):
    id: str
    linkedin_url: str


class ProspectError(Exception):
    """Base exception for prospect-related errors"""
    pass


class NoProspectsAvailableError(ProspectError):
    """Raised when no prospects are available for scraping"""
    pass


class StorageError(ProspectError):
    """Raised when there's an error storing data in the database"""
    pass