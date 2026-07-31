from typing import TYPE_CHECKING, Literal

from fragapi._methods.base import FragAPIMethod
from fragapi.types import BuyPremiumResponse, PremiumRecipient

if TYPE_CHECKING:
    from fragapi._typing import ClientProtocol


class Premium:
    class GetPremiumRecipient(FragAPIMethod):
        username: str

        __return_type__ = PremiumRecipient
        __method__ = "premium/recipient/{username}"

    class BuyPremium(FragAPIMethod):
        username: str
        months: Literal[3, 6, 12]
        show_sender: bool | None = None

        __return_type__ = BuyPremiumResponse
        __method__ = "premium/buy"
        __request_method__ = "POST"

    async def get_premium_recipient(
        self: "ClientProtocol", *, username: str, quantity: int | None = None
    ) -> PremiumRecipient:
        """
        premium/recipient/ method.

        Use this method to get info about premium recipient before gifting premium.
        On success, returns :class:`fragapi.types.PremiumRecipient`.

        Source: https://docs.fragapi.com/ru/docs/api/premium/get_recipient

        :param username: Username of the premium recipient. For example: `synca`.
        :return: :class:`fragapi.types.PremiumRecipient` object.
        """

        return await self(self.GetPremiumRecipient(username=username, quantity=quantity))

    async def buy_premium(
        self: "ClientProtocol",
        *,
        username: str,
        months: Literal[3, 6, 12],
        show_sender: bool = False,
    ):
        """
        premium/buy method.

        Use this method to buy premium to the specific user.
        On success, returns :class:`fragapi.types.BuyPremiumResponse`.

        Source: https://docs.fragapi.com/ru/docs/api/premium/buy_premium

        :param username: Username of the premium recipient. For example: `synca`.
        :param months: Number of premim months, 3 | 6 | 12
        :param show_sender: *Optional*. Whether show sender of the premium to the recipient.
        :return: :class:`fragapi.types.BuyPremiumResponse` object.
        """

        return await self(
            self.BuyPremiumResponse(username=username, months=months, show_sender=show_sender)
        )
