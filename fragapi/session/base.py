from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from pydantic import ValidationError

from fragapi.exceptions import DeserializationError

if TYPE_CHECKING:
    from fragapi._methods import FragAPIMethod
    from fragapi.client import FragAPI
    from fragapi.types import _FragAPIType


class BaseSession(ABC):
    """
    Abstract session class.

    If you want to implement your own session class,
    you should inherit this class.
    """

    def __init__(self, timeout: float = 300) -> None:
        self.timeout = timeout

    @abstractmethod
    async def request(
        self,
        client: "FragAPI",
        method: "FragAPIMethod[_FragAPIType]",
    ) -> "_FragAPIType":
        """Make http request."""
        raise NotImplementedError

    def _check_response(
        self,
        client: "FragAPI",
        method: "FragAPIMethod[_FragAPIType]",
        content: str,
    ) -> "_FragAPIType":
        # TODO: content -> ['error']

        try:
            response = method.__return_type__.model_validate_json(  # type: ignore[name-defined]
                content,
                context={"client": client},
            )
        except ValidationError as e:
            raise DeserializationError(
                method,
                "Failed to deserialize object",
            ) from e

        # if isinstance(response.result, ItemsList):
        #     response.result = response.result.items
        return response
