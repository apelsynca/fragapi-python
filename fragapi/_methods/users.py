from typing import TYPE_CHECKING

from fragapi._methods.base import FragAPIMethod
from fragapi.types import FragUser

if TYPE_CHECKING:
    from fragapi._typing import ClientProtocol


class GetMe:
    class GetMeMethod(FragAPIMethod):
        __return_type__ = FragUser
        __method__ = "users/me"

    async def get_me(self: "ClientProtocol"):
        return await self(self.GetMeMethod())
