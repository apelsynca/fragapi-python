from enum import Enum

from fragapi.types.base import FragAPIObject


class Transaction(FragAPIObject):
    pass


class TransactionsSorting(str, Enum):
    newest = "-created_at"
    oldest = "created_at"
    amount_desc = "-amount"
    amount = "amount"
