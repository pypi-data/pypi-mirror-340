from importlib.metadata import PackageNotFoundError
from importlib.metadata import version
try:
    __version__ = version("once.releaser")
except PackageNotFoundError:
    try:
        __version__ = version("once-releaser")
    except PackageNotFoundError:
        __version__ = "unknown"
