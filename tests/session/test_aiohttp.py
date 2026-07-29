import pytest
from aiohttp.http import SERVER_SOFTWARE
from pytest_mock import MockerFixture

from fragapi import __version__
from fragapi._methods.users import GetMe
from fragapi.client import FragAPI
from fragapi.exceptions import DeserializationError
from fragapi.session.aiohttp import AiohttpSession
from tests.conftest import get_aiohttp_response_session_mock

# When resp is -> {"error":"Unauthorized","detail":"Unauthorized"}


@pytest.mark.asyncio
async def test_request_right_data(mocker: MockerFixture) -> None:
    aiohttp_session_mock = get_aiohttp_response_session_mock(
        {
            "balance": "13.37",
            "id": 123321,
            "firstName": "SomeFirstName",
            "lastName": None,
            "username": None,
        },
    )
    mocker.patch(
        "fragapi.session.aiohttp.ClientSession.__aenter__", return_value=aiohttp_session_mock
    )

    client = FragAPI(token="fg_MyApiTokenSuperSecret", session=aiohttp_session_mock)
    session = AiohttpSession()

    me = await session.request(client=client, method=GetMe.GetMeMethod)

    assert me.balance == 13.37
    assert me.id == 123321

    aiohttp_session_mock.request.assert_awaited_once_with(
        method="GET",
        url="https://api.fragapi.com/v1/users/me",
        headers={
            "Authorization": "Bearer fg_MyApiTokenSuperSecret",
            "Content-Type": "application/json",
            "User-Agent": f"{SERVER_SOFTWARE} fragapi/{__version__}",
        },
    )


@pytest.mark.asyncio
async def test_request_raises_validation_on_error(mocker: MockerFixture) -> None:
    aiohttp_session_mock = get_aiohttp_response_session_mock({"somebullshiet": "respi"})
    mocker.patch(
        "fragapi.session.aiohttp.ClientSession.__aenter__", return_value=aiohttp_session_mock
    )

    client = FragAPI(token="fg_MyApiTokenSuperSecret", session=aiohttp_session_mock)
    session = AiohttpSession()

    with pytest.raises(DeserializationError):
        await session.request(client=client, method=GetMe.GetMeMethod)
