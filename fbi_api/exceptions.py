"""Custom exceptions for the FBI API client."""


class FBIAPIError(Exception):
    """Base exception for all FBI API errors."""


class FBIAPIConnectionError(FBIAPIError):
    """Raised when a connection to the FBI API cannot be established."""

class FBIAPIAuthenticationError(FBIAPIError):
    """Raised when authentication with the FBI API fails."""
    def __init__(self, user) -> None:
        super().__init__(f"Failed to authenticate user '{user.username}'.")

class FBIAPIResponseError(FBIAPIError):
    """Raised when the FBI API returns an unexpected or error response."""

    def __init__(self, status_code: int, message: str = "") -> None:
        self.status_code = status_code
        super().__init__(f"HTTP {status_code}: {message}")
