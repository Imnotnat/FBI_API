"""Tests for fbi_api.client using mocked HTTP responses."""

import pytest
import responses as responses_lib

from fbi_api.client import FBIClient, _BASE_URL
from fbi_api.exceptions import FBIAPIConnectionError, FBIAPIResponseError
from fbi_api.models import SearchResults, WantedPerson


MOCK_ITEM = {
    "uid": "abc123",
    "title": "John Doe",
    "description": None,
    "url": "https://www.fbi.gov/wanted/abc123",
    "images": [],
    "subjects": ["Terrorism"],
    "field_offices": ["miami"],
    "reward_text": None,
    "details": None,
    "caution": None,
    "status": "na",
    "nationality": None,
    "age_range": None,
    "hair": None,
    "eyes": None,
    "height_min": None,
    "height_max": None,
    "weight_min": None,
    "weight_max": None,
}

MOCK_LIST_RESPONSE = {"total": 1, "items": [MOCK_ITEM]}


@responses_lib.activate
def test_search_wanted_returns_search_results():
    responses_lib.add(
        responses_lib.GET,
        f"{_BASE_URL}/list",
        json=MOCK_LIST_RESPONSE,
        status=200,
    )
    client = FBIClient()
    results = client.search_wanted()
    assert isinstance(results, SearchResults)
    assert results.total == 1
    assert len(results.items) == 1


@responses_lib.activate
def test_search_wanted_passes_filters():
    responses_lib.add(
        responses_lib.GET,
        f"{_BASE_URL}/list",
        json=MOCK_LIST_RESPONSE,
        status=200,
    )
    client = FBIClient()
    client.search_wanted(title="John", field_office="miami", subject="Terrorism", status="na")
    request = responses_lib.calls[0].request
    assert "title=John" in request.url
    assert "field_offices=miami" in request.url
    assert "subject=Terrorism" in request.url
    assert "status=na" in request.url


@responses_lib.activate
def test_search_wanted_passes_pagination():
    responses_lib.add(
        responses_lib.GET,
        f"{_BASE_URL}/list",
        json=MOCK_LIST_RESPONSE,
        status=200,
    )
    client = FBIClient()
    client.search_wanted(page=3, page_size=10)
    request = responses_lib.calls[0].request
    assert "page=3" in request.url
    assert "pageSize=10" in request.url


@responses_lib.activate
def test_get_person_returns_wanted_person():
    responses_lib.add(
        responses_lib.GET,
        f"{_BASE_URL}/abc123",
        json=MOCK_ITEM,
        status=200,
    )
    client = FBIClient()
    person = client.get_person("abc123")
    assert isinstance(person, WantedPerson)
    assert person.uid == "abc123"
    assert person.title == "John Doe"


@responses_lib.activate
def test_get_person_raises_on_404():
    responses_lib.add(
        responses_lib.GET,
        f"{_BASE_URL}/unknown",
        json={"error": "not found"},
        status=404,
    )
    client = FBIClient()
    with pytest.raises(FBIAPIResponseError) as exc_info:
        client.get_person("unknown")
    assert exc_info.value.status_code == 404


@responses_lib.activate
def test_search_wanted_raises_on_server_error():
    responses_lib.add(
        responses_lib.GET,
        f"{_BASE_URL}/list",
        json={"error": "internal error"},
        status=500,
    )
    client = FBIClient()
    with pytest.raises(FBIAPIResponseError) as exc_info:
        client.search_wanted()
    assert exc_info.value.status_code == 500


@responses_lib.activate
def test_connection_error_raises_fbi_connection_error():
    import requests as req_lib

    responses_lib.add(
        responses_lib.GET,
        f"{_BASE_URL}/list",
        body=req_lib.exceptions.ConnectionError("network failure"),
    )
    client = FBIClient()
    with pytest.raises(FBIAPIConnectionError):
        client.search_wanted()


def test_custom_base_url_is_used():
    custom_url = "https://my-mock-api.local/v1"
    client = FBIClient(base_url=custom_url)
    assert client._base_url == custom_url
