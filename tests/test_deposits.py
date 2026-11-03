import pydantic
import pytest
from pytest_mock import MockerFixture

from fragapi import FragAPI
from fragapi._methods import Methods
from fragapi.session.aiohttp import AiohttpSession
from fragapi.types import TonDeposit, TonMemoDeposit
from tests.conftest import get_aiohttp_response_session_mock


@pytest.mark.parametrize(
    ("method_name", "path", "response", "return_type", "field"),
    [
        (
            "request_ton_deposit",
            "deposits/ton",
            {"address": "EQabc", "amount": "1500000000", "payload": "te6cc"},
            TonDeposit,
            "payload",
        ),
        (
            "request_ton_deposit_via_memo",
            "deposits/ton/memo",
            {"address": "EQabc", "amount": 1.5, "memo": "some-memo"},
            TonMemoDeposit,
            "memo",
        ),
    ],
)
@pytest.mark.asyncio
async def test_request_deposit_sends_amount_in_query(
    mocker: MockerFixture,
    method_name: str,
    path: str,
    response: dict,
    return_type: type,
    field: str,
) -> None:
    aiohttp_session_mock = get_aiohttp_response_session_mock(response)
    mocker.patch(
        "fragapi.session.aiohttp.ClientSession.__aenter__", return_value=aiohttp_session_mock
    )
    client = FragAPI(token="fg_MyApiTokenSuperSecret", session=AiohttpSession())

    deposit = await getattr(client, method_name)(amount=1.5)

    assert isinstance(deposit, return_type)
    assert getattr(deposit, field) == response[field]

    kwargs = aiohttp_session_mock.request.await_args.kwargs
    assert kwargs["method"] == "POST"
    assert kwargs["url"] == f"https://api.fragapi.com/v1/{path}?amount=1.5"
    assert not kwargs["json"]
    assert kwargs["params"] is None


@pytest.mark.parametrize("method", [Methods.RequestTonDeposit, Methods.RequestTonDepositViaMemo])
@pytest.mark.parametrize("amount", [0, -1])
def test_request_deposit_rejects_non_positive_amount(method: type, amount: float) -> None:
    with pytest.raises(pydantic.ValidationError):
        method(amount=amount)
