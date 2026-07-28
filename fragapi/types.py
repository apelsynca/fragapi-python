from typing import TYPE_CHECKING, TypeVar

from pydantic import BaseModel, ConfigDict, PrivateAttr

if TYPE_CHECKING:
    from fragapi.client import FragAPI

_FragAPIType = TypeVar(
    "_FragAPIType",
    bound="FragAPIObject | list | bool",
)


class FragAPIObject(BaseModel):
    _client: "FragAPI" = PrivateAttr()

    model_config = ConfigDict(
        extra="allow",
    )


__all__ = ["FragAPIObject", "_FragAPIType"]
