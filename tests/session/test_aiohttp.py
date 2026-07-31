import pytest
from aiohttp.http import SERVER_SOFTWARE
from pytest_mock import MockerFixture

from fragapi import __version__
from fragapi._methods import Methods
from fragapi._methods.base import FragAPIMethod
from fragapi.client import FragAPI
from fragapi.exceptions import DeserializationError
from fragapi.session.aiohttp import AiohttpSession
from fragapi.types.base import FragAPIObject
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

    me = await session.request(client=client, method=Methods.GetMeMethod())

    assert me.balance == 13.37
    assert me.id == 123321

    aiohttp_session_mock.request.assert_awaited_once_with(
        method="GET",
        url="https://api.fragapi.com/v1/users/me",
        params=None,
        json=None,
        headers={
            "Authorization": "Bearer fg_MyApiTokenSuperSecret",
            "Content-Type": "application/json",
            "User-Agent": f"{SERVER_SOFTWARE} fragapi/{__version__}",
        },
    )


class FunnyResponse(FragAPIObject):
    something: float


class Funny:
    class FunnyMethod(FragAPIMethod):
        some_data: int
        other_data: float | None = None

        __return_type__ = FunnyResponse
        __method__ = "custom"
        __request_method__ = "POST"


@pytest.mark.asyncio
async def test_request_respects_http_method_of_the_method(mocker: MockerFixture) -> None:
    aiohttp_session_mock = get_aiohttp_response_session_mock({"something": 42.4242})
    mocker.patch(
        "fragapi.session.aiohttp.ClientSession.__aenter__", return_value=aiohttp_session_mock
    )

    client = FragAPI(token="fg_MyApiTokenSuperSecret", session=aiohttp_session_mock)
    session = AiohttpSession()

    funny_resp = await session.request(client=client, method=Funny.FunnyMethod(some_data=999))

    assert funny_resp.something == 42.4242

    aiohttp_session_mock.request.assert_awaited_once_with(
        method="POST",
        url="https://api.fragapi.com/v1/custom",
        params=None,
        json={"someData": 999},
        headers={
            "Authorization": "Bearer fg_MyApiTokenSuperSecret",
            "Content-Type": "application/json",
            "User-Agent": f"{SERVER_SOFTWARE} fragapi/{__version__}",
        },
    )


@pytest.mark.asyncio
async def test_request_fills_key_fields_in_url(mocker: MockerFixture) -> None:
    response_data = {
        "recipient": "SomeRec",
        "photo": "does-not-matter",
        "name": "DoesNotMatter",
        "avatarUrl": "https://some.avatar.com/url/img.jpg",
    }
    aiohttp_session_mock = get_aiohttp_response_session_mock(response_data)
    mocker.patch(
        "fragapi.session.aiohttp.ClientSession.__aenter__", return_value=aiohttp_session_mock
    )

    client = FragAPI(token="fg_MyOtherSuperSecret_Token919", session=aiohttp_session_mock)
    session = AiohttpSession()

    await session.request(
        client=client, method=Methods.GetStarsRecipient(username="monk", quantity=52)
    )

    aiohttp_session_mock.request.assert_awaited_once_with(
        method="GET",
        url="https://api.fragapi.com/v1/stars/recipient/monk",
        params={"quantity": 52},
        json=None,
        headers={
            "Authorization": "Bearer fg_MyOtherSuperSecret_Token919",
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
        await session.request(client=client, method=Methods.GetMeMethod())
