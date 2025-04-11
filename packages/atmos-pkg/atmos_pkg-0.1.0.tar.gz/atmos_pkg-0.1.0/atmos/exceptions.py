"""
Exceptions for the Atmos API.
"""


class AtmosError(Exception):
    """Base exception for all Atmos errors."""
    pass


class AtmosAuthError(AtmosError):
    """Exception raised when authentication fails."""
    pass


class AtmosAPIError(AtmosError):
    """Exception raised when the API returns an error."""

    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")
