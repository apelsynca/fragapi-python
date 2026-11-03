from enum import Enum

from fragapi.types.base import FragAPIObject


class GiftModel(FragAPIObject):
    name: str
    floor: float
    count: int
    image_url: str


class GiftModelsSorting(str, Enum):
    floor_desc = "-floor"
    floor = "floor"
