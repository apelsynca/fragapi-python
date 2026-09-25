from typing import TYPE_CHECKING

from fragapi._methods.base import FragAPIMethod
from fragapi.types import GiftModel

if TYPE_CHECKING:
    from fragapi._typing import ClientProtocol


class Gifts:
    class GetGiftModelNamesMethod(FragAPIMethod):
        short_name: str

        __return_type__ = list[str]
        __method__ = "gifts/{short_name}/short-models"

    async def get_collection_gift_model_names(self: "ClientProtocol", short_name: str) -> list[str]:
        """
        Source: https://docs.fragapi.com/ru/docs/api/gifts/get_gift_models_short_names
        """
        return await self(self.GetGiftModelNamesMethod(short_name=short_name))

    class GetCollectionGiftModelsMethod(FragAPIMethod):
        short_name: str

        __return_type__ = list[GiftModel]
        __method__ = "gifts/{short_name}/models"

    async def get_collection_gift_models(
        self: "ClientProtocol", short_name: str
    ) -> list[GiftModel]:
        """
        https://docs.fragapi.com/ru/docs/api/gifts/get_collection_models
        """
        return await self(self.GetCollectionGiftModelsMethod(short_name=short_name))

    class GetGiftModelMethod(FragAPIMethod):
        short_name: str
        name: str

        __return_type__ = GiftModel
        __method__ = "gifts/{short_name}/models/{name}"

    async def get_gift_model(self: "ClientProtocol", short_name: str, name: str) -> GiftModel:
        """
        https://docs.fragapi.com/ru/docs/api/gifts/get_model
        """
        return await self(self.GetGiftModelMethod(short_name=short_name, name=name))
