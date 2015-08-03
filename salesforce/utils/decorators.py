# encoding: utf-8
from functools import wraps
from ..exception import AuthenticationFailed


def authenticate(func):
    @wraps(func)
    def authenticate_and_call(self, *args, **kwargs):
        if self.auth is None or not self.auth.is_authenticated():
            raise AuthenticationFailed('You need to first authenticate!')
        return func(self, *args, **kwargs)
    return authenticate_and_call
