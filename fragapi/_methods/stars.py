from typing import TYPE_CHECKING

from pydantic import Field

from fragapi._methods.base import FragAPIMethod
from fragapi.types import BuyStarsResponse, StarsRecipient

if TYPE_CHECKING:
    from fragapi._typing import ClientProtocol


class Stars:
    class GetStarsRecipient(FragAPIMethod):
        username: str
        quantity: int | None = None

        __return_type__ = StarsRecipient
        __method__ = "stars/recipient/{username}"

    class BuyStars(FragAPIMethod):
        username: str
        quantity: int = Field(ge=50, le=10_000_000)
        show_sender: bool | None = None

        __return_type__ = BuyStarsResponse
        __method__ = "stars/buy"
        __request_method__ = "POST"

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

    async def buy_stars(
        self: "ClientProtocol", *, username: str, quantity: int, show_sender: bool = False
    ):
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
