from typing import Annotated

from pydantic import UUID4, Field

from fragapi.types.base import FragAPIObject


class BaseBuyResponse(FragAPIObject):
    message_hash: str
    transaction_id: UUID4
    name: str
    amount: Annotated[float, Field(gt=0, description="Amount that was reduced from your balance")]
    avatar_url: str


class BuyStarsResponse(BaseBuyResponse):
    pass


class BuyPremiumResponse(BaseBuyResponse):
    pass
