"""Tests for fbi_api.models."""

import pytest

from fbi_api.models import SearchResults, WantedPerson


PERSON_DATA = {
    "uid": "abc123",
    "title": "John Doe",
    "description": "Armed and dangerous",
    "url": "https://www.fbi.gov/wanted/wanted_terrorists/john-doe",
    "images": [
        {"large": "https://example.com/large.jpg", "thumb": "https://example.com/thumb.jpg"}
    ],
    "subjects": ["Terrorism"],
    "field_offices": ["dallas"],
    "reward_text": "$25,000",
    "details": "Some details",
    "caution": "Considered dangerous",
    "status": "na",
    "nationality": "Unknown",
    "age_range": "30 to 40",
    "hair": "Black",
    "eyes": "Brown",
    "height_min": 70,
    "height_max": 72,
    "weight_min": 170,
    "weight_max": 190,
}

SEARCH_DATA = {
    "total": 1,
    "items": [PERSON_DATA],
}


class TestWantedPerson:
    def test_from_dict_basic(self):
        person = WantedPerson.from_dict(PERSON_DATA)
        assert person.uid == "abc123"
        assert person.title == "John Doe"
        assert person.description == "Armed and dangerous"
        assert person.url == "https://www.fbi.gov/wanted/wanted_terrorists/john-doe"

    def test_from_dict_images(self):
        person = WantedPerson.from_dict(PERSON_DATA)
        assert person.images == ["https://example.com/large.jpg"]

    def test_from_dict_images_fallback_to_thumb(self):
        data = {**PERSON_DATA, "images": [{"thumb": "https://example.com/thumb.jpg"}]}
        person = WantedPerson.from_dict(data)
        assert person.images == ["https://example.com/thumb.jpg"]

    def test_from_dict_empty_images(self):
        data = {**PERSON_DATA, "images": None}
        person = WantedPerson.from_dict(data)
        assert person.images == []

    def test_from_dict_subjects_and_offices(self):
        person = WantedPerson.from_dict(PERSON_DATA)
        assert person.subjects == ["Terrorism"]
        assert person.field_offices == ["dallas"]

    def test_from_dict_physical_attributes(self):
        person = WantedPerson.from_dict(PERSON_DATA)
        assert person.hair == "Black"
        assert person.eyes == "Brown"
        assert person.height_min == 70
        assert person.weight_max == 190

    def test_from_dict_missing_optional_fields(self):
        minimal = {"uid": "xyz", "title": "Jane Doe", "url": "https://fbi.gov"}
        person = WantedPerson.from_dict(minimal)
        assert person.uid == "xyz"
        assert person.description is None
        assert person.subjects == []
        assert person.images == []


class TestSearchResults:
    def test_from_dict_basic(self):
        results = SearchResults.from_dict(SEARCH_DATA, page=1)
        assert results.total == 1
        assert results.page == 1
        assert len(results.items) == 1

    def test_from_dict_items_are_wanted_persons(self):
        results = SearchResults.from_dict(SEARCH_DATA)
        assert isinstance(results.items[0], WantedPerson)
        assert results.items[0].uid == "abc123"

    def test_from_dict_empty_items(self):
        results = SearchResults.from_dict({"total": 0, "items": []})
        assert results.total == 0
        assert results.items == []

    def test_from_dict_page_defaults_to_1(self):
        results = SearchResults.from_dict(SEARCH_DATA)
        assert results.page == 1
