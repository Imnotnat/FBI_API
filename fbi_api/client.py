"""HTTP client for the FBI Wanted Persons API."""

from __future__ import annotations

from typing import Optional

import requests

from .exceptions import FBIAPIConnectionError, FBIAPIResponseError
from .models import SearchResults, WantedPerson

_BASE_URL = "https://api.fbi.gov/wanted/v1"


class FBIClient:
    """Client for the FBI Wanted Persons public API."""

    def __init__(
        self,
        base_url: str = _BASE_URL,
        timeout: int = 10,
        session: Optional[requests.Session] = None,
    ) -> None:
        # TODO: store base_url, timeout and session as instance attributes
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Public methods
    # ------------------------------------------------------------------

    def search_wanted(
        self,
        *,
        title: Optional[str] = None,
        field_office: Optional[str] = None,
        subject: Optional[str] = None,
        status: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> SearchResults:
        """Search the wanted persons list with optional filters."""
        # TODO: build query params dict, call self._get("/list", params=...),
        # and return SearchResults.from_dict(data, page=page)
        raise NotImplementedError

    def get_person(self, uid: str) -> WantedPerson:
        """Retrieve a single wanted person by their UID."""
        # TODO: call self._get(f"/{uid}") and return WantedPerson.from_dict(data)
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get(self, path: str, params: Optional[dict] = None) -> dict:
        # TODO: build the full URL, perform the GET request with self._session,
        # handle ConnectionError / Timeout (raise FBIAPIConnectionError),
        # raise FBIAPIResponseError on non-2xx, and return response.json()
        raise NotImplementedError
