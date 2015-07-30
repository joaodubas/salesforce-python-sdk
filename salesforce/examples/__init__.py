# encoding: utf-8
from ..http_client import Requests
from ..rest_api import SalesForceRestAPI
from ..url_resources import RestUrlResources


class Auth(object):
    def is_authenticated(self):
        return True


api = SalesForceRestAPI(
    httplib=Requests(),
    url_resources=RestUrlResources(
        domain='sample.com',
        version='1.0',
        sandbox=True
    ),
    auth=Auth()
)
