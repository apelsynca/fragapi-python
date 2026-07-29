from typing import TYPE_CHECKING

from fragapi import loggers
from fragapi._methods import Methods
from fragapi.session import AiohttpSession, BaseSession

if TYPE_CHECKING:
    from fragapi._methods import FragAPIMethod
    from fragapi.types import _FragAPIType


DEFAULT_BASE_URL = "https://api.fragapi.com/v1"


class FragAPI(Methods):
    def __init__(
        self,
        token: str,
        *,
        base_url: str = DEFAULT_BASE_URL,
        session: BaseSession | None = None,
    ) -> None:
        if not token or not isinstance(token, str):
            raise TypeError("API token (api_token) must be a non-empty string.")

        if not token.startswith("fg_"):
            raise ValueError("Invalid API token format. Tokens must start with 'fg_'.")

        self._token = token
        self.base_url = base_url.rstrip("/")
        self.session = session if session else AiohttpSession()

    async def __call__(self, method: "FragAPIMethod[_FragAPIType]") -> "_FragAPIType":
        loggers.client.debug(
            "Requesting: /%s with payload %s",
            method.__method__,
            method.model_dump_json(),
        )
        return await self.session.request(client=self, method=method)
