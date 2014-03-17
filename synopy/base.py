# -*- coding: utf-8 -*-
import json
from urlparse import urljoin

import requests

from errors import format_error


class Authentication(object):
    def __init__(self, sid, format='cookie'):
        assert format in ('cookie', 'sid'), "invalid sid format"

        self.sid = sid
        self.format = format

    def build_params(self):
        auth = {}
        sid_key = self.format == 'cookie' and 'id' or '_id'
        auth[sid_key] = self.sid
        return auth


class RequestManager(object):
    def __init__(self, protocol, domain, auth=None, port=80):
        assert protocol in ('http', 'https'), "invalid protocol"
        assert int(port), "port number must be integer"

        self.protocol = protocol
        self.domain = domain
        self.auth = auth
        self.port = str(port)

    def build_url(self, path):
        base_path = u'://'.join([self.protocol, self.domain])
        base_path = u':'.join([base_path, self.port])
        return urljoin(base_path, path)

    def build_request_options(self, http_method, params, use_auth=False):
        opts = {'params' if http_method == 'get' else 'data': params}
        if use_auth:
            if self.auth.format == 'sid':
                # pass the sid along with the get params
                opts['params'].update(self.auth.build_params())
            else:
                # pass it as a cookie
                opts['cookies'] = self.auth.build_params()
        return opts

    def run(self, path, http_method, namespace, params, use_auth=False):
        http_method = http_method.lower()
        assert http_method in ('get', 'post'), "invalid http method"

        url = self.build_url(path)
        opts = self.build_request_options(http_method, params, use_auth=use_auth)
        if http_method == 'get':
            resp = requests.get(url, **opts)
        else:
            resp = requests.post(url, **opts)
        return self.handle_response(resp, namespace)

    def handle_response(self, resp, namespace):
        response = Response(resp)
        if response.status_code == 200:
            if not response.is_success():
                errno = response.error_code
                response.error_message = format_error(errno, namespace)
        return response


class Response(object):
    def __init__(self, resp):
        # the ``requests`` library response object
        self.raw_response = resp
        # the http status code
        self.status_code = resp.status_code
        # the url that initiated this response
        self.url = resp.url
        # the deserialized json data
        self.payload = resp.status_code == 200 and json.loads(resp.content) or {}
        # user friendly message
        self.error_message = None

    def is_success(self):
        return self.payload.get('success') is True

    @property
    def error_code(self):
        return self.payload.get('error') and self.payload['error']['code'] or None
