import aiohttp
import pytest

from fragapi import FragAPI


def test_raises_wrong_token() -> None:
    with pytest.raises(ValueError, match="Invalid API token"):
        FragAPI(token="abcdefsomeweird_format")


def test_raises_empty_token() -> None:
    with pytest.raises(TypeError, match=r"API token \(api_token\) must be a non-empty"):
        FragAPI(token="")


@pytest.mark.asyncio
async def test_inits_session() -> None:
    client = FragAPI(token="fg_Duyjuv6x7mMOAKtdI4XIX20x1KxFLI3KSoRoMoreLenghtGoing")
    assert client.session is not None


@pytest.mark.asyncio
async def test_available_in_context_manager() -> None:
    async with FragAPI(token="fg_SomeSmallLenghtToken") as client:
        assert isinstance(client.session, aiohttp.ClientSession)
