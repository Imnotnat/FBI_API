"""Data models for the FBI API responses."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class WantedPerson:
    """Represents a wanted person entry from the FBI API."""

    uid: str
    title: str
    description: Optional[str]
    url: str
    images: List[str]
    subjects: List[str]
    field_offices: List[str]
    reward_text: Optional[str]
    details: Optional[str]
    caution: Optional[str]
    status: Optional[str]
    nationality: Optional[str]
    age_range: Optional[str]
    hair: Optional[str]
    eyes: Optional[str]
    height_min: Optional[int]
    height_max: Optional[int]
    weight_min: Optional[int]
    weight_max: Optional[int]

    @classmethod
    def from_dict(cls, data: dict) -> "WantedPerson":
        """Create a WantedPerson from a raw API response dictionary."""
        images = [
            url
            for img in (data.get("images") or [])
            if img
            for url in [img.get("large") or img.get("thumb") or img.get("original", "")]
            if url
        ]
        return cls(
            uid=data.get("uid", ""),
            title=data.get("title", ""),
            description=data.get("description"),
            url=data.get("url", ""),
            images=images,
            subjects=data.get("subjects") or [],
            field_offices=data.get("field_offices") or [],
            reward_text=data.get("reward_text"),
            details=data.get("details"),
            caution=data.get("caution"),
            status=data.get("status"),
            nationality=data.get("nationality"),
            age_range=data.get("age_range"),
            hair=data.get("hair"),
            eyes=data.get("eyes"),
            height_min=data.get("height_min"),
            height_max=data.get("height_max"),
            weight_min=data.get("weight_min"),
            weight_max=data.get("weight_max"),
        )


@dataclass
class SearchResults:
    """Represents a paginated search response from the FBI API."""

    total: int
    items: List[WantedPerson]
    page: int = 1

    @classmethod
    def from_dict(cls, data: dict, page: int = 1) -> "SearchResults":
        """Create SearchResults from a raw API response dictionary."""
        items = [WantedPerson.from_dict(item) for item in (data.get("items") or [])]
        return cls(
            total=data.get("total", 0),
            items=items,
            page=page,
        )
