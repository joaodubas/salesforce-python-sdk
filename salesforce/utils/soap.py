# encoding: utf-8
SOAP_ENV = '''<?xml version="1.0" encoding="utf-8" ?>
<soapenv:Envelope
    xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:urn="urn:partner.soap.sforce.com"
    xmlns:urn1="urn:sobject.partner.soap.sforce.com"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    {header}
    {body}
</soapenv:Envelope>'''

SOAP_HEADER = '''<soapenv:Header>
    <urn:SessionHeader>
        <urn:sessionId>{access_token}</urn:sessionId>
    </urn:SessionHeader>
</soapenv:Header>'''

SOAP_BODY = '''<soapenv:Body>
    <urn:{method}>
        {request}
    </urn:{method}>
</soapenv:Body>'''

SOAP_LOGIN_BODY = '''<soapenv:Body>
    {request}
</soapenv:Body>'''

SOAP_BODY_LOGIN = '''<n1:login xmlns:n1="urn:partner.soap.sforce.com">
    <n1:username>{username}</n1:username>
    <n1:password>{password}</n1:password>
</n1:login>'''

SOAP_QUERY_BODY = '<urn:queryString>{query_string}</urn:queryString>'

SOAP_QUERY_MORE_BODY = '<urn:queryLocator>{query_string}</urn:queryLocator>'

SOAP_SEARCH_BODY = '<urn:searchString>{query_string}</urn:searchString>'

SOAP_DESCRIBE_BODY = '<urn:sObjectType>{sobject}</urn:sObjectType>'


def xml_content_headers(length, action):
    return {
        'Content-Type': 'text/xml',
        'charset': 'utf-8',
        'Content-length': '{}'.format(length),
        'SOAPAction': action,
    }


def get_soap_env(header=None, body=None):
    return SOAP_ENV.format(**as_params(header=header, body=body))


def get_soap_header(access_token=None):
    return SOAP_HEADER.format(**as_params(access_token=access_token))


def get_soap_body(method=None, request=None):
    return SOAP_BODY.format(**as_params(method=method, request=request))


def get_login_soap_body(request=None):
    return SOAP_LOGIN_BODY.format(**as_params(request=request))


def get_soap_login_body(username, password):
    return SOAP_BODY_LOGIN.format(**as_params(
        username=username,
        password=password
    ))


def soap_login_header(request=None):
    return get_soap_env(header='', body=get_login_soap_body(request=request))


def soap_request_header(access_token=None, method=None, request=None):
    return get_soap_env(
        header=get_soap_header(access_token=access_token),
        body=get_soap_body(method=method, request=request)
    )


def get_soap_query_body(query_string):
    return SOAP_QUERY_BODY.format(**as_params(query_string=query_string))


def get_soap_query_more_body(query_string):
    return SOAP_QUERY_MORE_BODY.format(**as_params(query_string=query_string))


def get_soap_search_body(search_string):
    return SOAP_SEARCH_BODY.format(**as_params(query_string=search_string))


def get_soap_describe_body(sobject):
    return SOAP_DESCRIBE_BODY.format(**as_params(sobject=sobject))


def get_soap_create_body(sobject, data):
    create_body = ''

    for item in data:
        create_body += '<urn:sObjects xsi:type="urn1:{0}"> \n'.format(sobject)

        for key, value in item.iteritems():
            create_body += '<{0}>{1}</{0}> \n'.format(key, value)

        create_body += '</urn:sObjects> \n'

    return create_body


def get_soap_delete_body(ids):
    delete_body = ''

    for sf_id in ids:
        delete_body += '<urn:Ids>{0}</urn:Ids>'.format(sf_id)

    return delete_body


def get_soap_update_body(sobject, data):
    update_body = ''

    for item in data:
        if not isinstance(item, list):
            raise TypeError('`update` require a parameter type `list of lists`')

        update_body += '<urn:sObjects xsi:type="urn1:{0}"> \n'.format(sobject)
        update_body += '<urn:Id>{0}</urn:Id>'.format(item[0])

        for key, value in item[1].iteritems():
            update_body += '<urn:{0}>{1}</urn:{0}> \n'.format(key, value)

        update_body += '</urn:sObjects> \n'

    return update_body


def get_element_by_name(xml_string, element_name):
    elements = xml_string.getElementsByTagName(element_name)

    if len(elements):
        return elements.item(0).firstChild.nodeValue

    return None


def as_params(**kwargs):
    """as_params -- Remove all ``None`` values from named params.

    Args:
        kwargs (**dict): named parameters to be cleaned.

    Returns:
        (dict): containing only non ``None`` values.

    """
    return {k: v for k, v in kwargs.iteritems() if v is not None}
