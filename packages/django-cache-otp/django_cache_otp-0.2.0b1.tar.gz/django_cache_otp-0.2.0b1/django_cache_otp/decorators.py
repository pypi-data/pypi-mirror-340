from functools import wraps

from django.core.cache import cache


def skip_if_exists(func):
    @wraps(func)
    def wrapper(username: str, *args, **kwargs):
        if cache.get(username):
            return
        return func(username, *args, **kwargs)
    return wrapper
