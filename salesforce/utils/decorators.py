# encoding: utf-8
from functools import wraps
from ..exception import AuthenticationFailed


def required_auth(func):
    """required_auth -- Decorator that verifies if given class instance is
    authenticated.

    Args:
        func (function): callable to be decorated

    Raises:
        (AuthenticationFailed): when authentication check fails.

    Returns:
        (function): wrapped callable where auth verification will be done before
            calling decorated method.

    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.auth is None or not self.auth.is_authenticated():
            raise AuthenticationFailed('You need to first authenticate!')
        return func(self, *args, **kwargs)
    return wrapper
