from enum import Enum
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


class BulkPurchaseStatus(str, Enum):
    pending = "pending"
    charged = "charged"
    done = "done"


class BulkBuyStarsItemResult(FragAPIObject):
    username: str
    quantity: int
    result: BuyStarsResponse | None = None
    error: Annotated[str | None, Field(description="Why this item was not bought")] = None


class BulkBuyStarsResponse(FragAPIObject):
    id: UUID4
    status: BulkPurchaseStatus
    items: Annotated[
        list[BulkBuyStarsItemResult], Field(description="Results in the requested order")
    ]
