from typing import TYPE_CHECKING

from pydantic import Field

from fragapi._methods.base import FragAPIMethod
from fragapi.types import ListResource, Transaction, TransactionsSorting

if TYPE_CHECKING:
    from fragapi._typing import ClientProtocol


class Transactions:
    class ListTransactions(FragAPIMethod):
        page: int | None = None
        limit: int | None = Field(default=None, gt=0, le=100)
        sorting: list[TransactionsSorting] | None = None

        __return_type__ = ListResource[Transaction]
        __method__ = "transactions"

    async def list_transactions(
        self: "ClientProtocol",
        *,
        page: int | None = None,
        limit: int | None = None,
        sorting: list[TransactionsSorting] | None = None,
    ) -> ListResource[Transaction]:
        """
        transactions method.

        Use this method to get a page of your Fragment transactions.
        On success, returns :class:`fragapi.types.ListResource` of
        :class:`fragapi.types.Transaction`.

        Source: https://docs.fragapi.com/ru/docs/api/transactions/list_transactions

        :param page: *Optional*. Page number, API defaults to 1.
        :param limit: *Optional*. Items in a page, up to 100. API defaults to 10.
        :param sorting: *Optional*. Sorting criteria, applied in order. API defaults to newest.
        :return: :class:`fragapi.types.ListResource` of :class:`fragapi.types.Transaction`.
        """
        return await self(self.ListTransactions(page=page, limit=limit, sorting=sorting))
