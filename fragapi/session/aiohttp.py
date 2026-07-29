import ssl
from typing import TYPE_CHECKING

import certifi
from aiohttp import ClientSession, ClientTimeout, TCPConnector
from aiohttp.http import SERVER_SOFTWARE

from fragapi.__meta__ import __version__
from fragapi.session.base import BaseSession

if TYPE_CHECKING:
    from fragapi._methods import FragAPIMethod
    from fragapi.client import FragAPI
    from fragapi.types import _FragAPIType


class AiohttpSession(BaseSession):
    async def request(
        self, client: "FragAPI", method: "FragAPIMethod[_FragAPIType]"
    ) -> "_FragAPIType":
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        async with ClientSession(
            timeout=ClientTimeout(self.timeout),
            connector=TCPConnector(
                ssl=ssl_context,
            ),
        ) as session:
            response = await session.request(
                method="GET",
                url=f"{client.base_url}/{method.__method__}",
                headers={
                    "Authorization": f"Bearer {client._token}",
                    "Content-Type": "application/json",
                    "User-Agent": f"{SERVER_SOFTWARE} fragapi/{__version__}",
                },
            )

            content = await response.text()

            return self._check_response(client=client, method=method, content=content)
