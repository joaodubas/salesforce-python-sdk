# encoding: utf-8
from .soap_api import SalesForceSoapAPI
from .rest_api import SalesForceRestAPI
from .version import Version
from .http_client import HTTPConnection, Requests
from .url_resources import RestUrlResources, SoapUrlResources
from .utils import validate_boolean_input


class SalesForce(object):
    """SalesForce -- """
    def __init__(self, **kwargs):
        """__init__ -- """
        super(SalesForce, self).__init__()

        self.__api = None

        self.__sandbox = None
        self.__soap = None
        self.__httplib = None
        self.__version = None
        self.__domain = None

        self.sandbox = kwargs.pop('sandbox', False)
        self.soap = kwargs.pop('soap', False)
        self.httplib = kwargs.pop('httplib', Requests())
        self.domain = kwargs.pop('domain', 'test' if self.sandbox else 'login')
        self.version = kwargs.pop(
            'version',
            Version.get_latest_version(self.httplib)
        )

        self.__api = self.__get_api(self.soap)

    def get_auth_uri(self, **kwargs):
        """get_auth__uri -- """
        return self.__get_api(False).get_auth_uri(**kwargs)

    def authenticate(self, soap=None, **kwargs):
        """authenticate -- """
        self.__api.auth = self.__get_api(soap).authenticate(**kwargs)

    def query(self, query_string, soap=None):
        """query -- """
        return self.__get_api(soap).query(query_string)

    def query_all(self, query_string, soap=None):
        """query_all -- """
        return self.__get_api(soap).query_all(query_string)

    def query_more(self, query_url, soap=None):
        """query_more -- """
        return self.__get_api(soap).query_more(query_url)

    def search(self, search_string, soap=None):
        """search -- """
        return self.__get_api(soap).search(search_string)

    def get(self, get_url, params=None, soap=None, **kwargs):
        """get -- """
        return self.__get_api(soap).get(get_url, params)

    def post(self, post_url, data, soap=None):
        """post -- """
        return self.__get_api(soap).post(post_url, data)

    def __getattr__(self, name):
        """__getattr__ -- """
        if not name[0].isalpha():
            return super(SalesForce, self).__getattribute__(name)

        return SObjectFacade(
            name,
            self.__api,
            self.domain,
            self.sandbox,
            self.version,
            self.soap
        )

    @property
    def sandbox(self):
        """sandbox -- """
        return self.__sandbox

    @sandbox.setter
    def sandbox(self, sandbox):
        """sandbox -- """
        validate_boolean_input(sandbox, 'sanbox')

        self.__sandbox = sandbox

        if self.__api is not None:
            self.__api.url_resources.sandbox = sandbox
            self.__api.url_resources.domain = 'test' if self.sandbox else 'login'

    @property
    def soap(self):
        """soap -- """
        return self.__soap

    @soap.setter
    def soap(self, soap):
        """soap -- """
        validate_boolean_input(soap, 'soap')

        if self.__api is not None:
            self.__api = self.__get_api(soap)

        self.__soap = soap

    @property
    def httplib(self):
        """httplib -- """
        return self.__httplib

    @httplib.setter
    def httplib(self, httplib):
        """httplib -- """
        if not isinstance(httplib, HTTPConnection):
            raise TypeError("Must be a subclass of HTTPConnection!")

        self.__httplib = httplib

        if self.__api is not None:
            self.__api.httplib = httplib

    @property
    def version(self):
        """version -- """
        return self.__version

    @version.setter
    def version(self, version):
        """version -- """
        try:
            round_version = round(version, 1)
        except TypeError:
            raise TypeError('Version should be a number!')

        self.__version = round_version

        if self.__api is not None:
            self.__api.url_resources.version = round_version

    def __getstate__(self):
        """__getstate__ -- """
        return self.__dict__

    def __setstate__(self, d):
        """__setstate__ -- """
        self.__dict__.update(d)

    def __get_api(self, soap):
        """__get_api -- """
        if soap is None:
            soap = self.soap

        if soap == self.soap and self.__api is not None:
            return self.__api
        else:
            auth = None if self.__api is None else self.__api.auth

            if soap:
                url_resources = SoapUrlResources(
                    self.domain,
                    self.sandbox,
                    self.version
                )
                return SalesForceSoapAPI(
                    url_resources=url_resources,
                    httplib=self.httplib,
                    auth=auth
                )
            else:
                url_resources = RestUrlResources(
                    self.domain,
                    self.sandbox,
                    self.version
                )
                return SalesForceRestAPI(
                    url_resources=url_resources,
                    httplib=self.httplib,
                    auth=auth
                )


class SObjectFacade(object):
    """SObjectFacade -- """
    def __init__(self, name, api, domain, sandbox, version, soap):
        """__init__ -- """
        super(SObjectFacade, self).__init__()
        self.__api = api

        self.name = name
        self.domain = domain
        self.sandbox = sandbox
        self.version = version
        self.soap = soap

    def describe(self, soap=None):
        """describe -- """
        return self.__get_api(soap).__getattr__(self.name).describe()

    def create(self, data, soap=None):
        """create -- """
        return self.__get_api(soap).__getattr__(self.name).create(data)

    def update(self, data, soap=None):
        """update -- """
        return self.__get_api(soap).__getattr__(self.name).update(data)

    def delete(self, record_id, soap=None):
        """delete -- """
        return self.__get_api(soap).__getattr__(self.name).delete(record_id)

    def post(self, data, record_id=None, soap=None):
        """post -- """
        return self.__get_api(soap).__getattr__(self.name).post(data, record_id)

    def get(self, record_id=None, params=None, soap=None):
        """get -- """
        return self.__get_api(
            soap
        ).__getattr__(
            self.name
        ).get(
            record_id,
            params
        )

    def __get_api(self, soap):
        """__get_api -- """
        if soap is None:
            soap = self.soap

        if soap == self.soap and self.__api is not None:
            return self.__api
        else:
            if soap:
                url_resources = SoapUrlResources(
                    self.domain,
                    self.sandbox,
                    self.version
                )
                return SalesForceSoapAPI(
                    url_resources=url_resources,
                    httplib=self.__api.httplib,
                    auth=self.__api.auth
                )
            else:
                url_resources = RestUrlResources(
                    self.domain,
                    self.sandbox,
                    self.version
                )
                return SalesForceRestAPI(
                    url_resources=url_resources,
                    httplib=self.__api.httplib,
                    auth=self.__api.auth
                )
