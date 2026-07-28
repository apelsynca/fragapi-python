from typing import TYPE_CHECKING

from fragapi._methods.base import FragAPIMethod
from fragapi.types import FragAPIObject

if TYPE_CHECKING:
    from fragapi._typing import ClientProtocol


class FragUser(FragAPIObject):
    id: int
    balance: float
    first_name: str
    last_name: str | None
    username: str | None


class GetMe:
    class GetMeMethod(FragAPIMethod):
        __return_type__ = FragUser
        __method__ = "users/me"

    async def get_me(self: "ClientProtocol"):
        return await self(self.GetMeMethod())
