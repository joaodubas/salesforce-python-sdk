# encoding: utf-8


def json_content_headers(access_token):
    return {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token,
        'X-PrettyPrint': '1',
        'Accept': 'application/json'
    }
