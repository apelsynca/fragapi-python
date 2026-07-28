from typing import ClassVar, Generic

from pydantic import BaseModel, ConfigDict

from fragapi.types import _FragAPIType


class FragAPIMethod(BaseModel, Generic[_FragAPIType]):
    """Base `Frag API` method class."""

    model_config = ConfigDict(
        extra="ignore",
        frozen=True,
    )

    __return_type__: ClassVar[_FragAPIType]
    __method__: ClassVar[str]
