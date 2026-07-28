from unittest.mock import MagicMock

import pytest
from aiohttp import ClientSession

from fragapi.client import FragAPI


@pytest.fixture
def client_session_mock() -> MagicMock:
    return MagicMock(spec=ClientSession)


@pytest.fixture
def client(client_session_mock: MagicMock) -> FragAPI:
    return FragAPI(
        token="fg_Duyjuv6x7mMOAKtdI4XIX20x1KxFLI3KSoRo33gu7jj", session=client_session_mock
    )
