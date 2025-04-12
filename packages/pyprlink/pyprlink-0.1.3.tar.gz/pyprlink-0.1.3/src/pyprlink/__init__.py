"""
PyPrLink - A TCP/IP client for communicating with local services
"""
try:
    from importlib.metadata import version, PackageNotFoundError
    try:
        __version__ = version("pyprlink")
    except PackageNotFoundError:
        # package is not installed
        __version__ = "unknown"
except ImportError:
    # Python < 3.8
    __version__ = "unknown"