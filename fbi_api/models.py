"""Data models for the FBI API responses."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class WantedPerson:
    """Represents a wanted person entry from the FBI API."""

    # TODO: define the fields that map to the API response
    # Example fields to consider:
    #   uid: str
    #   title: str
    #   description: Optional[str]
    #   url: str
    #   images: List[str]
    #   subjects: List[str]
    #   field_offices: List[str]
    #   status: Optional[str]
    #   ...

    @classmethod
    def from_dict(cls, data: dict) -> "WantedPerson":
        """Create a WantedPerson from a raw API response dictionary."""
        # TODO: parse the fields from `data` and return a WantedPerson instance
        raise NotImplementedError


@dataclass
class SearchResults:
    """Represents a paginated search response from the FBI API."""

    # TODO: define the fields (e.g. total, items, page)

    @classmethod
    def from_dict(cls, data: dict, page: int = 1) -> "SearchResults":
        """Create SearchResults from a raw API response dictionary."""
        # TODO: parse items list and total count from `data`
        raise NotImplementedError
