"""Custom exceptions for the FBI API client."""


class FBIAPIError(Exception):
    """Base exception for all FBI API errors."""

    # TODO: add any shared logic here


class FBIAPIConnectionError(FBIAPIError):
    """Raised when a connection to the FBI API cannot be established."""

    # TODO: implement


class FBIAPIResponseError(FBIAPIError):
    """Raised when the FBI API returns an unexpected or error response."""

    # TODO: implement (e.g. store status_code, build message, call super().__init__)
