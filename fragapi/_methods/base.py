from typing import ClassVar, Generic, Literal

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from fragapi.types import _FragAPIType


class FragAPIMethod(BaseModel, Generic[_FragAPIType]):
    """Base `Frag API` method class."""

    model_config = ConfigDict(
        extra="ignore", frozen=True, alias_generator=to_camel, populate_by_name=True
    )

    __return_type__: ClassVar[_FragAPIType]
    __method__: ClassVar[str]
    __request_method__: Literal["GET", "POST"] = "GET"
