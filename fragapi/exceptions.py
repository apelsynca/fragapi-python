from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fragapi._methods.base import FragAPIMethod


class FragAPIError(Exception):
    """Base exceptions class"""


class DeserializationError(FragAPIError):
    """Exception for deserialization errors."""

    def __init__(self, method: "FragAPIMethod", message: str) -> None:
        self.method = method
        self.message = message

    def __str__(self) -> str:
        """Return a string representation of the exception."""
        return f"/{self.method.__method__} {self.message}"
