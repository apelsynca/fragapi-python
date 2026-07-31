import pytest
from pytest_mock import MockerFixture

from fragapi import FragAPI
from fragapi._methods.get_me import GetMe
from fragapi.session.aiohttp import AiohttpSession


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
async def test_client_call_calls_session(mocker: MockerFixture) -> None:
    fragapi = FragAPI(token="fg_SomeSmallLenghtToken")
    session_mock = mocker.patch.object(fragapi, "session", spec=AiohttpSession)

    await fragapi(method=GetMe.GetMeMethod())

    session_mock.request.assert_called_once_with(client=fragapi, method=GetMe.GetMeMethod())
