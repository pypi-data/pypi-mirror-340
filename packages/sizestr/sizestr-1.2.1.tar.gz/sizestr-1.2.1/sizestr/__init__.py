from math import isfinite, log

__version__ = '1.2.1'

_SUFFIXES = (' KiB', ' MiB', ' GiB', ' TiB', ' PiB', ' EiB', ' ZiB')


def sizestr(size: float) -> str:
    """
    Convert byte size to human-readable string.

    >>> sizestr(10_000)
    '9.77 KiB'
    """
    # Handle non-finite values
    if not isfinite(size):
        return f'({size})'

    # Handle sign
    prefix = '-' if size < 0 else ''
    size = abs(size)

    # Fast path for small values
    if size < 1024:
        return f'{prefix}{int(size)} B'

    exp = int(log(size, 1024))
    if exp > 7:
        return '(too large to display)'

    size /= 1024**exp
    precision = 2 if size < 10 else 1
    return f'{prefix}{size:.{precision}f}{_SUFFIXES[exp - 1]}'
