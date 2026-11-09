import asyncio
from typing import TYPE_CHECKING

from pydantic import UUID4, Field

from fragapi._methods.base import FragAPIMethod
from fragapi.types import (
    BulkBuyStarsResponse,
    BulkPurchaseStatus,
    BuyStarsResponse,
    StarsRecipient,
)

if TYPE_CHECKING:
    from fragapi._typing import ClientProtocol


class Stars:
    class GetStarsRecipient(FragAPIMethod):
        username: str
        quantity: int | None = None

        __return_type__ = StarsRecipient
        __method__ = "stars/recipient/{username}"

    async def get_stars_recipient(
        self: "ClientProtocol", *, username: str, quantity: int | None = None
    ) -> StarsRecipient:
        """
        stars/recipient/ method.

        Use this method to get info about stars recipient before buying stars.
        On success, returns :class:`fragapi.types.StarsRecipient`.

        Source: https://docs.fragapi.com/ru/docs/api/stars/get_recipient

        :param username: Username of the stars recipient. For example: `synca`.
        :param quantity: *Optional* Number of stars to buy pinned to the recipient search.
        :return: :class:`fragapi.types.StarsRecipient` object.
        """
        return await self(self.GetStarsRecipient(username=username, quantity=quantity))

    class BuyStars(FragAPIMethod):
        username: str
        quantity: int = Field(ge=50, le=10_000_000)
        show_sender: bool | None = None

        __return_type__ = BuyStarsResponse
        __method__ = "stars/buy"
        __request_method__ = "POST"

    async def buy_stars(
        self: "ClientProtocol", *, username: str, quantity: int, show_sender: bool = False
    ) -> BuyStarsResponse:
        """
        stars/buy method.

        Use this method to buy stars to the specific user.
        On success, returns :class:`fragapi.types.BuyStarsResponse`.

        Source: https://docs.fragapi.com/ru/docs/api/stars/buy_stars

        :param username: Username of the stars recipient. For example: `synca`.
        :param quantity: Number of stars to buy.
        :param show_sender: *Optional*. Whether show sender of the stars to the recipient.
        :return: :class:`fragapi.types.BuyStarsResponse` object.
        """
        return await self(
            self.BuyStars(username=username, quantity=quantity, show_sender=show_sender)
        )

    class BuyStarsBulk(FragAPIMethod):
        # Resolved lazily by pydantic: the enclosing class doesn't exist yet here
        items: list["Stars.BuyStars"] = Field(min_length=1, max_length=100)

        __return_type__ = BulkBuyStarsResponse
        __method__ = "stars/buy/bulk"
        __request_method__ = "POST"

    async def buy_stars_bulk(
        self: "ClientProtocol", *, items: "list[Stars.BuyStars]"
    ) -> BulkBuyStarsResponse:
        """
        stars/buy/bulk method.

        Use this method to buy stars for many users at once, sent in one wallet transaction.
        Returns right away with status `pending`; poll :meth:`get_buy_stars_bulk`
        or use :meth:`wait_buy_stars_bulk` to get each item's result.
        Only bought items are charged.
        On success, returns :class:`fragapi.types.BulkBuyStarsResponse`.

        :param items: 1 to 100 purchases, e.g. `[FragAPI.BuyStars(username="synca", quantity=50)]`.
        :return: :class:`fragapi.types.BulkBuyStarsResponse` object.
        """
        return await self(self.BuyStarsBulk(items=items))

    class GetBuyStarsBulk(FragAPIMethod):
        id: UUID4

        __return_type__ = BulkBuyStarsResponse
        __method__ = "stars/buy/bulk/{id}"

    async def get_buy_stars_bulk(self: "ClientProtocol", *, id: UUID4) -> BulkBuyStarsResponse:
        """
        stars/buy/bulk/{id} method.

        Use this method to get a stars bulk purchase and its items' results.
        On success, returns :class:`fragapi.types.BulkBuyStarsResponse`.

        :param id: ID of the bulk purchase, from :meth:`buy_stars_bulk`.
        :return: :class:`fragapi.types.BulkBuyStarsResponse` object.
        """
        return await self(self.GetBuyStarsBulk(id=id))

    async def wait_buy_stars_bulk(
        self: "ClientProtocol", *, id: UUID4, interval: float = 3.0
    ) -> BulkBuyStarsResponse:
        """
        Poll :meth:`get_buy_stars_bulk` until the bulk purchase is `done`.

        Wrap it in :func:`asyncio.wait_for` to set a timeout.

        :param id: ID of the bulk purchase, from :meth:`buy_stars_bulk`.
        :param interval: *Optional*. Seconds between polls.
        :return: :class:`fragapi.types.BulkBuyStarsResponse` object with status `done`.
        """
        while True:
            bulk = await self(self.GetBuyStarsBulk(id=id))
            if bulk.status is BulkPurchaseStatus.done:
                return bulk
            await asyncio.sleep(interval)
