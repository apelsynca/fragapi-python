import ssl
import string
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
            raw_data = method.model_dump(exclude_none=True, by_alias=True)

            formatter = string.Formatter()
            keys_for_url = [
                field_name
                for _, field_name, _, _ in formatter.parse(method.__method__)
                if field_name is not None
            ]
            url_fill_data = {key: raw_data.pop(key) for key in keys_for_url if key in raw_data}
            url = f"{client.base_url}/{method.__method__.format(**url_fill_data)}"

            response = await session.request(
                method=method.__request_method__,
                params=raw_data if method.__request_method__ == "GET" and raw_data else None,
                json=raw_data if method.__request_method__ != "GET" else None,
                url=url,
                headers={
                    "Authorization": f"Bearer {client._token}",
                    "Content-Type": "application/json",
                    "User-Agent": f"{SERVER_SOFTWARE} fragapi/{__version__}",
                },
            )

            content = await response.text()

            return self._check_response(client=client, method=method, content=content)
