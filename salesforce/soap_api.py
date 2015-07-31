# encoding: utf-8
import xml.dom.minidom

from .common_api import SalesForceAPI
from .login import LoginWithSoapAPI
from .s_object import SObject
from .utils import (
    authenticate as u_auth,
    xml_content_headers,
    get_element_by_name,
    get_soap_query_body,
    get_soap_query_more_body,
    get_soap_search_body,
    get_soap_describe_body,
    get_soap_create_body,
    get_soap_update_body,
    get_soap_delete_body,
    soap_request_header,
    get_request_url,
    send_request
)


class SalesForceSoapAPI(SalesForceAPI):
    """SalesForceSoapAPI -- """
    def __init__(self, httplib, url_resources, auth=None):
        """__init__ -- """
        super(SalesForceSoapAPI, self).__init__(url_resources, httplib, auth)
        self.__login_api = None

    def authenticate(self, **kwargs):
        """authenticate -- """
        self.__login_api = LoginWithSoapAPI(
            self.httplib,
            self.url_resources,
            **kwargs)

        return self.__login_api.authenticate()

    @u_auth
    def query(self, query_string):
        """query -- """
        return self.post(query_string, self.Action.QUERY)

    @u_auth
    def query_all(self, query_string):
        """query_all -- """
        response = self.post(query_string, self.Action.QUERYALL)
        xml_resp_value = xml.dom.minidom.parseString(response.text)

        def do_query_all(resp):
            done = get_element_by_name(resp, 'done')
            if done:
                return response
            else:
                query_locator = get_element_by_name(resp, 'queryLocator')
                result = self.query_more(query_locator)
                xml_result_value = xml.dom.minidom.parseString(result.text)

                done = get_element_by_name(xml_result_value, 'done')
                done_node = resp.getElementsByTagName('done').item(0)
                done_node.firstChild.nodeValue = done

                total_size = get_element_by_name(xml_result_value, 'totalSize')
                total_size_node = resp.getElementsByTagName('totalSize').item(0)
                total_size_node.firstChild.nodeValue += total_size

                records = get_element_by_name(xml_result_value, 'records')
                records_node = resp.getElementsByTagName('records')
                records_node.appendChild(records)

                return do_query_all(resp)

        return do_query_all(xml_resp_value)

    @u_auth
    def query_more(self, query_string):
        """query_more -- """
        return self.post(query_string, self.Action.QUERYMORE)

    @u_auth
    def search(self, search_string):
        """search -- """
        return self.post(search_string, self.Action.SEARCH)

    @u_auth
    def quick_search(self, search_string):
        """quick_search -- """
        return self.search('FIND {%s}' % search_string)

    @u_auth
    def post(self, data, action):
        """post -- """
        strategies = {
            self.Action.QUERY: get_soap_query_body,
            self.Action.QUERYMORE: get_soap_query_more_body,
            self.Action.QUERYALL: get_soap_query_body,
            self.Action.SEARCH: get_soap_search_body
        }

        body = strategies.get(action, lambda *a, **kw: None)(data)
        if body is None:
            raise ValueError('`action` {} is not supported!'.format(action))

        request_body = soap_request_header().format(
            access_token=self.auth.access_token,
            method=action,
            request=body
        )

        post_url = self.url_resources.get_full_resource_url(
            self.auth.instance_url
        )

        return self.__send_request(
            'POST',
            post_url,
            action,
            data=request_body
        )

    @u_auth
    def get(self, get_url, params=None):
        """get -- """
        pass

    @u_auth
    def __getattr__(self, name):
        """__getattr__ -- """
        if not name[0].isalpha():
            return object.__getattribute__(self, name)

        return SoapSObject(
            name,
            self.httplib,
            self.auth,
            self.url_resources
        )

    def __getstate__(self):
        """__getstate__ -- """
        return self.__dict__

    def __setstate__(self, d):
        """__setstate__ -- """
        self.__dict__.update(d)

    def __send_request(self, method, url, action, **kwargs):
        """__send_request -- """
        headers = xml_content_headers(len(kwargs['data']), action)

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

    class Action(object):
        """Action -- """
        QUERY = 'query'
        QUERYALL = 'queryAll'
        QUERYMORE = 'queryMore'
        SEARCH = 'search'


class SoapSObject(SObject):
    """SoapSObject -- """
    def __init__(self, name, httplib, auth, url_resources):
        """__init__ -- """
        super(SoapSObject, self).__init__(httplib, auth, url_resources)

        self.__name = name

    @u_auth
    def describe(self):
        return self.post(None, self.Action.DESCRIBE)

    @u_auth
    def create(self, data):
        if not isinstance(data, list):
            raise TypeError('`create` require a parameter type `list`')

        return self.post(data, self.Action.CREATE)

    @u_auth
    def update(self, data):
        if not isinstance(data, list):
            raise TypeError('`update` require a parameter type `list of lists`')

        return self.post(data, self.Action.UPDATE)

    @u_auth
    def delete(self, record_ids):
        if not isinstance(record_ids, list):
            raise TypeError('`update` require a parameter type `list of lists`')

        return self.post(record_ids, SoapSObject.Action.DELETE)

    @u_auth
    def post(self, data, action):
        """post -- """
        if action != self.Action.DESCRIBE and not isinstance(data, list):
            raise TypeError('`create` require a parameter type `list`')

        body = ''
        if action == SoapSObject.Action.DESCRIBE:
            body = get_soap_describe_body(self.__name)

        elif action == SoapSObject.Action.CREATE:
            body = get_soap_create_body(self.__name, data)

        elif action == SoapSObject.Action.UPDATE:
            body = get_soap_update_body(self.__name, data)

        elif action == SoapSObject.Action.DELETE:
            body = get_soap_delete_body(data)

        else:
            raise ValueError('`action` {} is not supported!'.format(action))

        request_body = soap_request_header().format(
            access_token=self.auth.access_token,
            method=action,
            request=body
        )

        post_url = self.url_resources.get_full_resource_url(
            self.auth.instance_url
        )

        return self.__send_request(
            'POST',
            post_url,
            action,
            data=request_body
        )

    @u_auth
    def get(self, record_id=None, params=None):
        """get -- """
        pass

    def __send_request(self, method, url, action, **kwargs):
        """_send_request -- """
        headers = xml_content_headers(len(kwargs['data']), action)

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

    class Action(object):
        """Action -- """
        DESCRIBE = 'describeSObject'
        CREATE = 'create'
        DELETE = 'delete'
        UPDATE = 'update'
