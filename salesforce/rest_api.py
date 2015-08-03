# encoding: utf-8
import json

from .common_api import SalesForceAPI
from .exception import AuthenticationFailed
from .login import LoginWithRestAPI
from .s_object import SObject
from .url_resources import ResourcesName
from .utils import (
    required_auth,
    json_content_headers,
    get_request_url,
    send_request
)


class SalesForceRestAPI(SalesForceAPI):
    """SalesForceRestAPI -- """
    def __init__(self, httplib, url_resources, auth=None):
        """__init__ -- """
        super(SalesForceRestAPI, self).__init__(url_resources, httplib, auth)
        self.__login_api = None

    def authenticate(self, **kwargs):
        """authenticate -- """
        if 'code' in kwargs:
            if not self.__login_api:
                raise AuthenticationFailed(
                    'You first need to use the get_auth_uri() to get the `code`'
                )

        else:
            self.__login_api = LoginWithRestAPI(
                self.httplib,
                self.url_resources,
                **kwargs
            )

        return self.__login_api.authenticate(**kwargs)

    def get_auth_uri(self, **kwargs):
        """get_auth_uri -- """
        self.__login_api = LoginWithRestAPI(
            self.httplib,
            self.url_resources,
            **kwargs
        )

        return self.__login_api.get_auth_uri()

    @required_auth
    def query(self, query_string):
        """query -- """
        query_url = self.url_resources.get_full_resource_url(
            self.auth.instance_url,
            ResourcesName.get_resource_name("query"))

        params = {'q': query_string}
        return self.get(query_url, params)

    @required_auth
    def query_all(self, query_string):
        """query_all -- """
        query_url = self.url_resources.get_full_resource_url(
            self.auth.instance_url,
            ResourcesName.get_resource_name("queryAll")
        )

        params = {'q': query_string}
        resp = self.get(query_url, params)

        def do_query_all(response):
            if response['done']:
                return response
            else:
                result = self.query_more(response['nextRecordsUrl'])

                response['done'] = result['done']
                response['totalSize'] += result['totalSize']
                response['records'].extend(result['records'])

                return do_query_all(response)

        return do_query_all(resp)

    @required_auth
    def query_more(self, url):
        """query_more -- """
        query_url = self.url_resources.get_full_resource_url(
            self.auth.instance_url,
            ResourcesName.get_resource_name("query")
        )

        if url.startswith(query_url, len(self.auth.instance_url)):
            get_url = '{0}/{1}'.format(self.auth.instance_url, url)
        else:
            get_url = '{0}/{1}'.format(query_url, url)

        return self.get(get_url)

    @required_auth
    def search(self, search_string):
        """search -- """
        search_url = self.url_resources.get_full_resource_url(
            self.auth.instance_url,
            ResourcesName.get_resource_name("search")
        )

        params = {'q': search_string}

        return self.get(search_url, params)

    @required_auth
    def quick_search(self, search_string):
        """quick_search -- """
        return self.search('FIND {%s}' % search_string)

    @required_auth
    def get(self, get_url, params=None):
        """get -- """
        return self.__send_request(
            'GET',
            get_url,
            params=params
        )

    @required_auth
    def post(self, post_url, data):
        """post -- """
        return self.__send_request(
            'POST',
            post_url,
            data=json.dumps(data)
        )

    @required_auth
    def __getattr__(self, name):
        """__getattr__ -- """
        if not name[0].isalpha():
            return object.__getattribute__(self, name)

        return RestSObject(
            name,
            self.httplib,
            self.auth,
            self.url_resources
        )

    def __send_request(self, method, url, **kwargs):
        """__send_request -- """
        headers = json_content_headers(self.auth.access_token)

        request_url = get_request_url(
            url,
            self.auth.instance_url,
            self.url_resources.get_resource_url()
        )

        return send_request(
            method,
            self.httplib,
            request_url,
            headers,
            **kwargs
        )


class RestSObject(SObject):
    """RestSObject -- """
    def __init__(self, name, httplib, auth, url_resources):
        """__init__ -- """
        super(RestSObject, self).__init__(httplib, auth, url_resources)

        self.__name = name

    @required_auth
    def describe(self):
        """describe -- """
        return self.get('/describe')

    @required_auth
    def create(self, data):
        """create -- """
        return self.post(data)

    @required_auth
    def update(self, data):
        """update -- """
        if not isinstance(data, list):
            raise TypeError('`update` require a parameter type `list`')

        record_id = data[0]
        records = data[1]

        update_url = '{0}/{1}'.format(
            self.url_resources.get_resource_sobject_url(
                self.auth.instance_url,
                ResourcesName.get_resource_name('sobject'),
                self.__name
            ),
            record_id
        )

        return self.__send_request(
            'PATCH',
            update_url,
            data=json.dumps(records)
        )

    @required_auth
    def delete(self, record_id):
        """delete -- """
        delete_url = '{0}/{1}'.format(
            self.url_resources.get_resource_sobject_url(
                self.auth.instance_url,
                ResourcesName.get_resource_name('sobject'),
                self.__name
            ),
            record_id
        )

        return self.__send_request(
            'DELETE',
            delete_url
        )

    @required_auth
    def post(self, data, record_id=None):
        """post -- """
        post_url = self.url_resources.get_resource_sobject_url(
            self.auth.instance_url,
            ResourcesName.get_resource_name('sobject'),
            self.__name
        )

        if record_id is not None:
            post_url += '/' + record_id

        return self.__send_request(
            'POST',
            post_url,
            data=json.dumps(data)
        )

    @required_auth
    def get(self, url=None, params=None):
        """get -- """
        get_url = self.url_resources.get_resource_sobject_url(
            self.auth.instance_url,
            ResourcesName.get_resource_name('sobject'),
            self.__name
        )

        if url is not None:
            get_url += url

        return self.__send_request(
            'GET',
            get_url,
            params=params
        )

    def __send_request(self, method, url, **kwargs):
        """__send_request -- """
        headers = json_content_headers(self.auth.access_token)

        request_url = get_request_url(
            url,
            self.auth.instance_url,
            self.url_resources.get_resource_url()
        )

        return send_request(
            method,
            self.httplib,
            request_url,
            headers,
            **kwargs
        )
