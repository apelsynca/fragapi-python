from typing import TYPE_CHECKING

from pydantic import Field

from fragapi._methods.base import FragAPIMethod
from fragapi.types import Deposit, DepositsSorting, ListResource, TonDeposit, TonMemoDeposit

if TYPE_CHECKING:
    from fragapi._typing import ClientProtocol


class Deposits:
    class RequestTonDeposit(FragAPIMethod):
        amount: float = Field(gt=0)

        __return_type__ = TonDeposit
        # The API reads amount from the query string, even on POST
        __method__ = "deposits/ton?amount={amount}"
        __request_method__ = "POST"

    async def request_ton_deposit(self: "ClientProtocol", *, amount: float) -> TonDeposit:
        """
        deposits/ton method.

        Use this method to top up your balance with a base64 payload.
        On success, returns :class:`fragapi.types.TonDeposit`.

        Source: https://docs.fragapi.com/ru/docs/api/deposit/request_ton_deposit

        :param amount: Amount in GRAM.
        :return: :class:`fragapi.types.TonDeposit` object.
        """
        return await self(self.RequestTonDeposit(amount=amount))

    class RequestTonDepositViaMemo(FragAPIMethod):
        amount: float = Field(gt=0)

        __return_type__ = TonMemoDeposit
        # The API reads amount from the query string, even on POST
        __method__ = "deposits/ton/memo?amount={amount}"
        __request_method__ = "POST"

    async def request_ton_deposit_via_memo(
        self: "ClientProtocol", *, amount: float
    ) -> TonMemoDeposit:
        """
        deposits/ton/memo method.

        Use this method to top up your balance with a plain text memo.
        On success, returns :class:`fragapi.types.TonMemoDeposit`.

        Source: https://docs.fragapi.com/ru/docs/api/deposit/request_ton_deposit_via_memo

        :param amount: Amount in GRAM.
        :return: :class:`fragapi.types.TonMemoDeposit` object.
        """
        return await self(self.RequestTonDepositViaMemo(amount=amount))

    class ListDeposits(FragAPIMethod):
        page: int | None = None
        limit: int | None = Field(default=None, gt=0, le=100)
        sorting: list[DepositsSorting] | None = None

        __return_type__ = ListResource[Deposit]
        __method__ = "deposits/"

    async def list_deposits(
        self: "ClientProtocol",
        *,
        page: int | None = None,
        limit: int | None = None,
        sorting: list[DepositsSorting] | None = None,
    ) -> ListResource[Deposit]:
        """
        deposits/ method.

        Use this method to get a page of your deposits.
        On success, returns :class:`fragapi.types.ListResource` of
        :class:`fragapi.types.Deposit`.

        Source: https://docs.fragapi.com/ru/docs/api/deposit/get_list

        :param page: *Optional*. Page number, API defaults to 1.
        :param limit: *Optional*. Items in a page, up to 100. API defaults to 10.
        :param sorting: *Optional*. Sorting criteria, applied in order. API defaults to newest.
        :return: :class:`fragapi.types.ListResource` of :class:`fragapi.types.Deposit`.
        """
        return await self(self.ListDeposits(page=page, limit=limit, sorting=sorting))
