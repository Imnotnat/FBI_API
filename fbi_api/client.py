"""HTTP client for the FBI Wanted Persons API."""

from __future__ import annotations

from typing import Optional

import requests

from .exceptions import FBIAPIConnectionError, FBIAPIResponseError
from .models import SearchResults, WantedPerson

_BASE_URL = "https://api.fbi.gov/wanted/v1"


class FBIClient:
    """Client for the FBI Wanted Persons public API.

    Args:
        base_url: Override the default API base URL (useful for testing).
        timeout: Request timeout in seconds (default: 10).
        session: An existing ``requests.Session`` to reuse (optional).

    Example::

        from fbi_api import FBIClient

        client = FBIClient()

        # List the first page of wanted persons
        results = client.search_wanted()
        print(f"Total: {results.total}")
        for person in results.items:
            print(person.title)

        # Search by subject
        results = client.search_wanted(subject="terrorism")

        # Fetch a single person by UID
        person = client.get_person("7db4d4428c2045b6b04bf3e6af2be1ea")
        print(person.title)
    """

    def __init__(
        self,
        base_url: str = _BASE_URL,
        timeout: int = 10,
        session: Optional[requests.Session] = None,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._session = session or requests.Session()

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
        """Search the wanted persons list with optional filters.

        Args:
            title: Filter by person title / name (partial match).
            field_office: Filter by FBI field office slug (e.g. ``"dallas"``).
            subject: Filter by subject category (e.g. ``"terrorism"``).
            status: Filter by status (e.g. ``"na"`` for active).
            page: Page number, starting at 1.
            page_size: Number of results per page (max 50 per API limits).

        Returns:
            A :class:`~fbi_api.models.SearchResults` instance.
        """
        params: dict = {"page": page, "pageSize": page_size}
        if title:
            params["title"] = title
        if field_office:
            params["field_offices"] = field_office
        if subject:
            params["subject"] = subject
        if status:
            params["status"] = status

        data = self._get("/list", params=params)
        return SearchResults.from_dict(data, page=page)

    def get_person(self, uid: str) -> WantedPerson:
        """Retrieve a single wanted person by their UID.

        Args:
            uid: The unique identifier of the wanted person.

        Returns:
            A :class:`~fbi_api.models.WantedPerson` instance.

        Raises:
            :class:`~fbi_api.exceptions.FBIAPIResponseError`: If the person
                is not found (404) or any other HTTP error occurs.
        """
        data = self._get(f"/{uid}")
        return WantedPerson.from_dict(data)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get(self, path: str, params: Optional[dict] = None) -> dict:
        url = f"{self._base_url}{path}"
        try:
            response = self._session.get(url, params=params, timeout=self._timeout)
        except requests.exceptions.ConnectionError as exc:
            raise FBIAPIConnectionError(
                f"Could not connect to FBI API at {url}"
            ) from exc
        except requests.exceptions.Timeout as exc:
            raise FBIAPIConnectionError(
                f"Request to {url} timed out"
            ) from exc

        if not response.ok:
            raise FBIAPIResponseError(response.status_code, response.text)

        return response.json()
