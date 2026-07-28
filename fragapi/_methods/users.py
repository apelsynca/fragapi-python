from typing import TYPE_CHECKING

from fragapi._methods.base import FragAPIMethod
from fragapi.types import FragAPIObject

if TYPE_CHECKING:
    from fragapi._typing import ClientProtocol


class Me(FragAPIObject):
    balance: float


class GetMe:
    class GetMeMethod(FragAPIMethod):
        __return_type__ = Me
        __method__ = "get_me"

    async def get_me(self: "ClientProtocol"):
        return await self(self.GetMeMethod())
