import json
from unittest.mock import AsyncMock, MagicMock

import aiohttp
import pytest

from fragapi.client import FragAPI
from fragapi.session.base import BaseSession


@pytest.fixture
def session_mock() -> MagicMock:
    mock = MagicMock(spec=BaseSession)
    mock.request = AsyncMock()
    return mock


FAKE_API_TOKEN = "fg_Duyjuv6x7mMOAKtdI4XIX20x1KxFLI3KSoRo33gu7jj"


@pytest.fixture
def client(session_mock: MagicMock) -> FragAPI:
    return FragAPI(token=FAKE_API_TOKEN, session=session_mock)


def get_aiohttp_response_session_mock(response: dict) -> MagicMock:
    aiohttp_session_mock = MagicMock(spec=aiohttp.ClientSession)
    text_mock = AsyncMock()
    text_mock.text.return_value = json.dumps(response, separators=",:")
    aiohttp_session_mock.request = AsyncMock(return_value=text_mock)

    return aiohttp_session_mock
