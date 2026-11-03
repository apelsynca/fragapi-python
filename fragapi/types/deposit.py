from datetime import datetime
from enum import Enum

from fragapi.types.base import FragAPIObject
from fragapi.types.transactions import TonTransaction


class TonDeposit(FragAPIObject):
    address: str
    amount: str
    payload: str


class TonMemoDeposit(FragAPIObject):
    address: str
    amount: float
    memo: str


class DepositStatus(str, Enum):
    pending = "pending"
    failed = "failed"
    completed = "completed"


class Deposit(FragAPIObject):
    amount: float
    created_at: datetime
    status: DepositStatus
    ton_transaction: TonTransaction | None


class DepositsSorting(str, Enum):
    newest = "-created_at"
    oldest = "created_at"
