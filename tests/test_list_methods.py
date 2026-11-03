from datetime import datetime, timezone

import pydantic
import pytest
from pytest_mock import MockerFixture
from yarl import URL

from fragapi import FragAPI
from fragapi._methods import Methods
from fragapi.session.aiohttp import AiohttpSession
from fragapi.types import DepositsSorting, DepositStatus, GiftModelsSorting, TransactionsSorting
from tests.conftest import get_aiohttp_response_session_mock

PAGINATION = {"totalCount": 1, "maxPage": 1}


def make_client(mocker: MockerFixture, response: dict) -> tuple[FragAPI, object]:
    aiohttp_session_mock = get_aiohttp_response_session_mock(response)
    mocker.patch(
        "fragapi.session.aiohttp.ClientSession.__aenter__", return_value=aiohttp_session_mock
    )
    return FragAPI(token="fg_MyApiTokenSuperSecret", session=AiohttpSession()), aiohttp_session_mock


@pytest.mark.asyncio
async def test_list_transactions(mocker: MockerFixture) -> None:
    client, http = make_client(
        mocker,
        {
            "items": [
                {
                    "createdAt": "2026-11-03T10:00:00Z",
                    "modifiedAt": None,
                    "amount": 1.5,
                    "reason": "stars",
                    "recipient": "abc",
                    "recipientUsername": "synca",
                    "starsAmount": 50,
                    "premiumMonths": None,
                    "tonTransaction": {"hash": None},
                }
            ],
            "pagination": PAGINATION,
        },
    )

    result = await client.list_transactions(
        limit=10, sorting=[TransactionsSorting.amount_desc, TransactionsSorting.newest]
    )

    item = result.items[0]
    assert item.created_at == datetime(2026, 11, 3, 10, tzinfo=timezone.utc)
    assert item.recipient_username == "synca"
    assert item.stars_amount == 50
    assert result.pagination.max_page == 1

    kwargs = http.request.await_args.kwargs
    assert kwargs["url"] == "https://api.fragapi.com/v1/transactions"
    assert kwargs["params"] == {"limit": 10, "sorting": ["-amount", "-created_at"]}
    # real yarl must emit the API's values, not the enum's repr
    assert URL("https://a/").with_query(kwargs["params"]).query.getall("sorting") == [
        "-amount",
        "-created_at",
    ]


@pytest.mark.asyncio
async def test_list_deposits(mocker: MockerFixture) -> None:
    client, http = make_client(
        mocker,
        {
            "items": [
                {
                    "amount": 2.0,
                    "createdAt": "2026-11-03T10:00:00Z",
                    "status": "pending",
                    "tonTransaction": None,
                }
            ],
            "pagination": PAGINATION,
        },
    )

    result = await client.list_deposits(page=2, sorting=[DepositsSorting.oldest])

    assert result.items[0].status is DepositStatus.pending
    assert result.items[0].ton_transaction is None

    kwargs = http.request.await_args.kwargs
    assert kwargs["method"] == "GET"
    assert kwargs["url"] == "https://api.fragapi.com/v1/deposits/"
    assert kwargs["params"] == {"page": 2, "sorting": ["created_at"]}


@pytest.mark.parametrize("method", [Methods.ListDeposits, Methods.ListTransactions])
@pytest.mark.parametrize("limit", [0, 101])
def test_list_rejects_limit_out_of_range(method: type, limit: int) -> None:
    with pytest.raises(pydantic.ValidationError):
        method(limit=limit)


@pytest.mark.parametrize(
    ("method", "path"),
    [("buy_stars", "stars/buy"), ("buy_premium", "premium/buy")],
)
@pytest.mark.asyncio
async def test_buy_sends_show_sender_in_camel_case(
    mocker: MockerFixture, method: str, path: str
) -> None:
    client, http = make_client(
        mocker,
        {
            "messageHash": "h",
            "transactionId": "3f2b8c1e-6d4a-4b7e-9a1c-2e5d8f0b7a34",
            "name": "n",
            "amount": 1.0,
            "avatarUrl": "u",
        },
    )
    size = {"quantity": 50} if method == "buy_stars" else {"months": 3}

    await getattr(client, method)(username="synca", show_sender=True, **size)

    kwargs = http.request.await_args.kwargs
    assert kwargs["url"] == f"https://api.fragapi.com/v1/{path}"
    assert kwargs["json"] == {"username": "synca", "showSender": True, **size}


@pytest.mark.asyncio
async def test_gift_models_sorting(mocker: MockerFixture) -> None:
    client, http = make_client(
        mocker,
        [{"name": "Frog", "floor": 1.5, "count": 3, "imageUrl": "u"}],  # type: ignore[arg-type]
    )

    models = await client.get_collection_gift_models("plushpepe", sorting=[GiftModelsSorting.floor])

    assert models[0].image_url == "u"

    kwargs = http.request.await_args.kwargs
    assert kwargs["url"] == "https://api.fragapi.com/v1/gifts/plushpepe/models"
    assert kwargs["params"] == {"sorting": ["floor"]}


@pytest.mark.asyncio
async def test_snake_case_url_field_still_fills_gift_url(mocker: MockerFixture) -> None:
    client, http = make_client(mocker, [])  # type: ignore[arg-type]

    await client.get_collection_gift_model_names(short_name="plushpepe")

    kwargs = http.request.await_args.kwargs
    assert kwargs["url"] == "https://api.fragapi.com/v1/gifts/plushpepe/short-models"
    assert kwargs["params"] is None
