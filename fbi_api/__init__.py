"""
FBI API - Python client for the FBI Wanted Persons API.

Usage:
    from fbi_api import FBIClient

    client = FBIClient()
    results = client.search_wanted()
    for person in results.items:
        print(person.title)
"""

from .client import FBIClient
from .models import WantedPerson, SearchResults
from .exceptions import FBIAPIError, FBIAPIConnectionError, FBIAPIResponseError

__version__ = "0.1.0"
__all__ = [
    "FBIClient",
    "WantedPerson",
    "SearchResults",
    "FBIAPIError",
    "FBIAPIConnectionError",
    "FBIAPIResponseError",
]
