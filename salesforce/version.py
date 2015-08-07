# encoding: utf-8
from .utils import send_request


class Version(object):
    VERSION_PATH = "http://na1.salesforce.com/services/data/"

    def __init__(self):
        super(Version, self).__init__()

    @classmethod
    def get_latest_version(cls, httplib):
        version_api_url = cls.VERSION_PATH
        latest_version = 0

        response = send_request(
            'GET',
            httplib,
            version_api_url,
            None
        )

        latest_version = max(
            latest_version,
            *[float(v['version']) for v in response]
        )

        return latest_version
