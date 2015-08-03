# encoding: utf-8
import requests
from ..exception import RequestFailed


def verify_response(response):
    if response.status_code >= requests.codes.multiple_choices:
        error_code = response.status_code
        message = response.text

        raise RequestFailed(error_code, message)


def send_request(method, httplib, url, headers, **kwargs):
    print '{}: Sending request to {}\n'.format(method, url)

    response = httplib(
        method,
        url,
        headers=headers,
        **kwargs
    )
    try:
        verify_response(response)
    except RequestFailed:
        raise

    if headers and 'SOAPAction' in headers:
        return response
    else:
        return response.json()


def get_request_url(url, instance_url, resource_url):
    if url.startswith(instance_url + resource_url):
        return url
    elif url.startswith(resource_url):
        return '{0}{1}'.format(instance_url, url)
    return '{0}{1}{2}'.format(instance_url, resource_url, url)
