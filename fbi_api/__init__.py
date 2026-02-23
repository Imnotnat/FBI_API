"""
FBI API - Python client for the FBI Wanted Persons API.
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
