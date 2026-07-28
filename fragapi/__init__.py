from .__meta__ import __version__
from .client import FragAPI


def hello() -> str:
    return "Hello from fragapi-python!"


__all__ = ["FragAPI", "__version__", "hello"]
