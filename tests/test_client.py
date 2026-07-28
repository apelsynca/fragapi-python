import aiohttp
import pytest

from fragapi import FragAPI


@pytest.mark.asyncio
async def test_inits_session() -> None:
    client = FragAPI()
    assert client.session is not None


@pytest.mark.asyncio
async def test_available_in_context_manager() -> None:
    async with FragAPI() as client:
        assert isinstance(client.session, aiohttp.ClientSession)
