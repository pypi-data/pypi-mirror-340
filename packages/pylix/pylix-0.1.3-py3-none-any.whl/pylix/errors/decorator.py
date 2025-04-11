import sys
import functools
import warnings

from pylix.errors import BaseError, BaseCodes

if hasattr(functools, "deprecated"):
    deprecated = functools.deprecated  # Use built-in in Python 3.13+
else:
    def deprecated(reason=None):
        """Fallback decorator for @deprecated in Python < 3.13."""
        def decorator(func):
            msg = f"'{func.__name__}' is deprecated."
            if reason:
                msg += f" Reason: {reason}"

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                warnings.warn(msg, category=DeprecationWarning, stacklevel=2)
                return func(*args, **kwargs)

            return wrapper
        return decorator

def TODO(func):
    def wrapper(*args, **kwargs):
        raise BaseError(BaseCodes.TODO, "This function has yet to be fully or partially implemented!")
    return wrapper
