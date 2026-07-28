from unittest.mock import AsyncMock, MagicMock

import pytest
from aiohttp import ClientSession

from fragapi.client import FragAPI


@pytest.fixture
def client_session_mock() -> MagicMock:
    return MagicMock(spec=ClientSession)


@pytest.fixture
def client(client_session_mock: MagicMock) -> FragAPI:
    return FragAPI(client_session_mock)


@pytest.mark.asyncio
async def test_get_me(client: FragAPI, client_session_mock: MagicMock) -> None:
    client_session_mock.request = AsyncMock(return_value={"balance": 1.25})

    me = await client.get_me()
    client_session_mock.request.assert_called_once()

    assert me["balance"] == 1.25
