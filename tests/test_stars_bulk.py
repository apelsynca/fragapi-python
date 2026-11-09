import json
from unittest.mock import AsyncMock, MagicMock

import pydantic
import pytest
from pytest_mock import MockerFixture

from fragapi import FragAPI
from fragapi._methods import Methods
from fragapi.session.aiohttp import AiohttpSession
from fragapi.types import BulkBuyStarsResponse, BulkPurchaseStatus, BuyStarsResponse
from tests.conftest import get_aiohttp_response_session_mock

BULK_ID = "3f1c2b8e-7a4d-4c1e-9b2a-5d6e7f8a9b0c"


def bulk_response(status: str) -> dict:
    return {
        "id": BULK_ID,
        "status": status,
        "items": [
            {
                "username": "synca",
                "quantity": 50,
                "result": {
                    "messageHash": "abc",
                    "transactionId": "0b1c2d3e-4f50-4a1b-8c2d-3e4f5a6b7c8d",
                    "name": "Synca",
                    "amount": 0.5,
                    "avatarUrl": "https://example.com/a.png",
                },
                "error": None,
            },
            {"username": "nobody", "quantity": 100, "result": None, "error": "not found"},
        ],
    }


def make_client(mocker: MockerFixture, aiohttp_session_mock: MagicMock) -> FragAPI:
    mocker.patch(
        "fragapi.session.aiohttp.ClientSession.__aenter__", return_value=aiohttp_session_mock
    )
    return FragAPI(token="fg_MyApiTokenSuperSecret", session=AiohttpSession())


@pytest.mark.asyncio
async def test_buy_stars_bulk_sends_aliased_items(mocker: MockerFixture) -> None:
    aiohttp_session_mock = get_aiohttp_response_session_mock(bulk_response("pending"))
    client = make_client(mocker, aiohttp_session_mock)

    bulk = await client.buy_stars_bulk(
        items=[
            FragAPI.BuyStars(username="synca", quantity=50, show_sender=True),
            FragAPI.BuyStars(username="nobody", quantity=100),
        ]
    )

    assert isinstance(bulk, BulkBuyStarsResponse)
    assert isinstance(bulk.items[0].result, BuyStarsResponse)
    assert bulk.items[1].error == "not found"

    kwargs = aiohttp_session_mock.request.await_args.kwargs
    assert kwargs["method"] == "POST"
    assert kwargs["url"] == "https://api.fragapi.com/v1/stars/buy/bulk"
    assert kwargs["json"] == {
        "items": [
            {"username": "synca", "quantity": 50, "showSender": True},
            {"username": "nobody", "quantity": 100},
        ]
    }


@pytest.mark.asyncio
async def test_get_buy_stars_bulk_puts_id_in_path(mocker: MockerFixture) -> None:
    aiohttp_session_mock = get_aiohttp_response_session_mock(bulk_response("done"))
    client = make_client(mocker, aiohttp_session_mock)

    bulk = await client.get_buy_stars_bulk(id=BULK_ID)

    assert bulk.status is BulkPurchaseStatus.done
    kwargs = aiohttp_session_mock.request.await_args.kwargs
    assert kwargs["method"] == "GET"
    assert kwargs["url"] == f"https://api.fragapi.com/v1/stars/buy/bulk/{BULK_ID}"
    assert kwargs["params"] is None


@pytest.mark.asyncio
async def test_wait_buy_stars_bulk_polls_until_done(mocker: MockerFixture) -> None:
    aiohttp_session_mock = get_aiohttp_response_session_mock({})
    responses = [bulk_response(s) for s in ("pending", "charged", "done")]
    aiohttp_session_mock.request = AsyncMock(
        side_effect=[MagicMock(text=AsyncMock(return_value=json.dumps(r))) for r in responses]
    )
    client = make_client(mocker, aiohttp_session_mock)

    bulk = await client.wait_buy_stars_bulk(id=BULK_ID, interval=0)

    assert bulk.status is BulkPurchaseStatus.done
    assert aiohttp_session_mock.request.await_count == 3


@pytest.mark.parametrize("count", [0, 101])
def test_buy_stars_bulk_rejects_item_count(count: int) -> None:
    item = Methods.BuyStars(username="synca", quantity=50)
    with pytest.raises(pydantic.ValidationError):
        Methods.BuyStarsBulk(items=[item] * count)
