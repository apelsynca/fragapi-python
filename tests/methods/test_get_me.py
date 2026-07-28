from unittest.mock import AsyncMock, MagicMock

import pytest
from aiohttp import ClientResponse
from aiohttp.http import SERVER_SOFTWARE

from fragapi.__meta__ import __version__
from fragapi._methods.users import GetMe
from fragapi.client import FragAPI


@pytest.mark.asyncio
async def test_get_me_and_calls_with_right_data(
    client: FragAPI, client_session_mock: MagicMock
) -> None:
    resp_mock = MagicMock(spec=ClientResponse)
    resp_mock.json.return_value = {
        "balance": 1.25,
        "firstName": "Homo",
        "id": 91919,
        "lastName": None,
        "username": "synca",
    }
    client_session_mock.request = AsyncMock(return_value=resp_mock)

    me = await client.get_me()

    assert me.balance == 1.25
    assert me.first_name == "Homo"
    assert me.id == 91919
    assert me.last_name is None
    assert me.username == "synca"

    # Todo: test that separatelly
    client_session_mock.request.assert_awaited_once_with(
        method="GET",
        url=f"{client.base_url}/{GetMe.GetMeMethod.__method__}",
        headers={
            "Authorization": f"Bearer {client._token}",
            "Content-Type": "application/json",
            "User-Agent": f"{SERVER_SOFTWARE} fragapi/{__version__}",
        },
    )
