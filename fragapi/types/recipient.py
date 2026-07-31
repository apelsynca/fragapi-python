from fragapi.types.base import FragAPIObject


class BaseRecipient(FragAPIObject):
    recipient: str
    photo: str
    name: str
    avatar_url: str


class StarsRecipient(BaseRecipient):
    pass


class PremiumRecipient(BaseRecipient):
    pass
