from datetime import datetime
from enum import Enum

from fragapi.types.base import FragAPIObject


class TonTransaction(FragAPIObject):
    hash: str | None


class Transaction(FragAPIObject):
    created_at: datetime
    modified_at: datetime | None
    amount: float
    reason: str
    recipient: str
    recipient_username: str
    stars_amount: int | None
    premium_months: int | None
    ton_transaction: TonTransaction


class TransactionsSorting(str, Enum):
    newest = "-created_at"
    oldest = "created_at"
    amount_desc = "-amount"
    amount = "amount"
