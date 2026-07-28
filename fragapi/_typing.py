from typing import Protocol

from fragapi._methods import FragAPIMethod
from fragapi.types import _FragAPIType


class ClientProtocol(Protocol):
    async def __call__(
        self,
        method: FragAPIMethod[_FragAPIType],
    ) -> _FragAPIType: ...
