from fragapi._methods.base import FragAPIMethod
from fragapi._methods.users import GetMe


class Methods(GetMe):
    pass


__all__ = ["FragAPIMethod", "Methods"]
