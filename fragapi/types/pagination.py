from typing import Generic, TypeVar

from fragapi.types.base import FragAPIObject

_Item = TypeVar("_Item", bound=FragAPIObject)


class Pagination(FragAPIObject):
    total_count: int
    max_page: int


class ListResource(FragAPIObject, Generic[_Item]):
    items: list[_Item]
    pagination: Pagination
