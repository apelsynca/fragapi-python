from fragapi.types.base import FragAPIObject


class FragUser(FragAPIObject):
    id: int
    balance: float
    first_name: str
    last_name: str | None
    username: str | None
