# encoding: utf-8
from functools import wraps
from ..exception import AuthenticationFailed


def required_auth(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.auth is None or not self.auth.is_authenticated():
            raise AuthenticationFailed('You need to first authenticate!')
        return func(self, *args, **kwargs)
    return wrapper
