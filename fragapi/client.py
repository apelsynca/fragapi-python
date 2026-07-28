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

DEFAULT_BASE_URL = "https://api/fragapi.com/v1"


class FragAPI(Methods):
    def __init__(
        self,
        token: str,
        *,
        base_url: str = DEFAULT_BASE_URL,
        session: aiohttp.ClientSession | None = None,
    ) -> None:
        if not token or not isinstance(token, str):
            raise TypeError("API token (api_token) must be a non-empty string.")

        if not token.startswith("fg_"):
            raise ValueError("Invalid API token format. Tokens must start with 'fg_'.")

        self._token = token
        self.base_url = base_url.rstrip("/")
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
        response = await self.session.request(
            method="GET",
            url=f"{self.base_url}/{method.__method__}",
            headers={
                "Authorization": f"Bearer {self._token}",
                "Content-Type": "application/json",
                "User-Agent": f"{SERVER_SOFTWARE} fragapi/{__version__}",
            },
        )

        json = await response.json()

        return method.__return_type__.model_validate(json)
