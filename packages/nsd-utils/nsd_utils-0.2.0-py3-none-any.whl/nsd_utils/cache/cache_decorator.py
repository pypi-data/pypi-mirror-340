# nsd_utils/cache/cache_decorator.py

import functools
import time
from typing import Callable
from nsd_utils.cache.cache_core import cache_get, cache_set

def cached_result(ttl: int = 10):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = f"{func.__qualname__}|{args}|{kwargs}"
            found = cache_get(key)
            if found is not None:
                return found
            result = func(*args, **kwargs)
            cache_set(key, result, ttl)
            return result
        return wrapper
    return decorator
