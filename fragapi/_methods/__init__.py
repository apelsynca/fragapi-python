from fragapi._methods.base import FragAPIMethod
from fragapi._methods.get_me import GetMe
from fragapi._methods.premium import Premium
from fragapi._methods.stars import Stars


class Methods(GetMe, Stars, Premium):
    pass


__all__ = ["FragAPIMethod", "Methods"]
