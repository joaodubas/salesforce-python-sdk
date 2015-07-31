# encoding: utf-8


class SObject(object):
    "SObject -- """
    def __init__(self, httplib, auth, url_resources):
        """__init__ -- """
        super(SObject, self).__init__()

        self.__httplib = httplib
        self.__auth = auth
        self.__url_resources = url_resources

    @property
    def httplib(self):
        """httplib -- """
        return self.__httplib

    @property
    def auth(self):
        """auth -- """
        return self.__auth

    @property
    def url_resources(self):
        """url_resources -- """
        return self.__url_resources 

    def describe(self):
        """describe -- """
        raise NotImplementedError

    def create(self, data):
        """create -- """
        raise NotImplementedError

    def update(self, data):
        """update -- """
        raise NotImplementedError

    def delete(self, data):
        """delete -- """
        raise NotImplementedError

    def post(self, data, **kwargs):
        """post -- """
        raise NotImplementedError
