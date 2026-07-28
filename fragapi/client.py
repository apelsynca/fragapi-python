import types
from typing import TYPE_CHECKING, TypeVar

import aiohttp
from aiohttp.http import SERVER_SOFTWARE

from fragapi.__meta__ import __version__
from fragapi._methods import Methods

if TYPE_CHECKING:
    from fragapi._methods import FragAPIMethod
    from fragapi.types import _FragAPIType

_Self = TypeVar("_Self", bound="FragAPI")


class FragAPI(Methods):
    def __init__(self, session: aiohttp.ClientSession | None = None) -> None:
        self.session = session if session else aiohttp.ClientSession()

    async def __aenter__(self) -> _Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: types.TracebackType | None,
    ) -> None:
        return

    async def __call__(self, method: "FragAPIMethod[_FragAPIType]") -> "_FragAPIType":
        return await self.session.request(
            method="GET",
            url=f"https://api.fragapi.com/v1/{method.__method__}",
            headers={
                "Content-Type": "application/json",
                "User-Agent": f"{SERVER_SOFTWARE} fragapi/{__version__}",
            },
        )
