# encoding: utf-8
from .http_client import Requests, HTTPConnection
from .login import Authentication


class SalesForceAPI(object):
    """SalesForceAPI -- """
    def __init__(self, url_resources, httplib=Requests(), auth=None):
        """__init__ -- """
        super(SalesForceAPI, self).__init__()

        self.__httplib = httplib
        self.__url_resources = url_resources
        self.__auth = auth
        self.__login = None

    @property
    def url_resources(self):
        """url_resources -- """
        return self.__url_resources

    @property
    def auth(self):
        """auth -- """
        return self.__auth

    @auth.setter
    def auth(self, auth):
        """auth -- """
        if not isinstance(auth, Authentication):
            raise TypeError('Must be a subclass of Authentication!')

        self.__auth = auth

    @property
    def httplib(self):
        """httplib -- """
        return self.__httplib

    @httplib.setter
    def httplib(self, httplib):
        """httplib -- """
        if not isinstance(httplib, HTTPConnection):
            raise TypeError('Must be a subclass of HTTPConnection!')

        self.__httplib = httplib

    def __getattr__(self, name):
        """__getattr__"""
        raise NotImplementedError

    def authenticate(self, **kwargs):
        """authenticate -- """
        raise NotImplementedError

    def query(self, query_string):
        """query -- """
        raise NotImplementedError

    def query_all(self, query_string):
        """query_all -- """
        raise NotImplementedError

    def query_more(self, query_url):
        """query_more -- """
        raise NotImplementedError

    def search(self, search_string):
        """search -- """
        raise NotImplementedError

    def get(self, params, **kwargs):
        """get -- """
        raise NotImplementedError

    def post(self, data, url_or_action):
        """post -- """
        raise NotImplementedError
