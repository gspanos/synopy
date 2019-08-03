# -*- coding: utf-8 -*-
import json
from urlparse import urljoin

import requests

from .errors import format_error


WEBAPI_PREFIX = 'webapi'


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


class Connection(object):
    def __init__(self, protocol, domain, auth=None, port=80, verify=True):
        assert protocol in ('http', 'https'), "invalid protocol"
        assert int(port), "port number must be integer"

        self.protocol = protocol
        self.domain = domain
        self.auth = auth
        self.port = str(port)
        self.verify = verify

    def build_url(self, path):
        base_path = u'://'.join([self.protocol, self.domain])
        base_path = u':'.join([base_path, self.port])
        return urljoin(base_path, path)

    def build_request_options(self, http_method, params):
        opts = {'params' if http_method == 'get' else 'data': params}
        if self.auth:
            # if we have credentials, then use them.
            auth_params = self.auth.build_params()
            if self.auth.format == 'sid':
                # pass the sid along with the get params
                opts['params'].update(auth_params)
            else:
                # pass it as a cookie
                opts['cookies'] = auth_params
        opts['verify'] = self.verify
        return opts

    def send(self, path, http_method, namespace, params, caller=None):
        api_method = params['method']
        http_method = http_method.lower()
        assert http_method in ('get', 'post'), "invalid http method"

        url = self.build_url(path)
        opts = self.build_request_options(http_method, params)
        if http_method == 'get':
            resp = requests.get(url, **opts)
        else:
            resp = requests.post(url, **opts)

        response = self.handle_response(resp, namespace)
        if caller and caller.has_handler_for(api_method):
            return caller.get_handler_for(api_method)(response)
        return response

    def handle_response(self, resp, namespace):
        response = Response(resp)
        if response.status_code == 200:
            if not response.is_success():
                errno = response.error_code
                response.error_message = format_error(errno, namespace)
        return response

    def authenticate(self, account, passwd):
        path = u'/'.join([WEBAPI_PREFIX, 'auth.cgi'])
        params = {
            'method': 'login',
            'account': account,
            'passwd': passwd,
            'version': 2,
            'api': 'SYNO.API.Auth',
            'format': 'sid',
            'session': 'DownloadStation'
        }
        resp = self.send(path, 'GET', 'SYNO.API.Auth', params)
        if resp.is_success():
            sid = resp.cookies['id']
            self.auth = Authentication(sid)
        else:
            raise ValueError(u"Wrong account name or password")


class Response(object):
    def __init__(self, resp):
        # the ``requests`` library response object
        self.raw_response = resp
        # response headers
        self.headers = resp.headers
        # response coolies
        self.cookies = resp.cookies
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


def _send_command(self, api_method, http_method, params):
    all_params = self.base_params
    all_params['method'] = api_method
    all_params.update(params)
    return self.conn.send(
        self.path,
        http_method,
        self.namespace,
        all_params,
        caller=self
    )


class ApiBaseMeta(type):
    def __init__(cls, name, bases, attrs):
        super(ApiBaseMeta, cls).__init__(name, bases, attrs)
        parents = [b for b in bases if isinstance(b, ApiBaseMeta)]
        if not parents:
            return
        api_methods = attrs.pop('methods')
        if isinstance(api_methods, basestring):
            api_methods = [api_methods]

        for api_method in api_methods:
            cls.add_api_method(api_method)

    def add_api_method(cls, api_method):

        def wrapped_send(_api_method_name, _http_method):
            def _wrapped(self, **params):
                return _send_command(self, _api_method_name, _http_method, params)
            return _wrapped

        if isinstance(api_method, basestring):
            api_method_name, func_name, http_method = api_method, api_method, 'GET'
        elif isinstance(api_method, (list, tuple)):
            if len(api_method) == 3:
                api_method_name, func_name, http_method = api_method
                assert isinstance(api_method_name, basestring), "Invalid API method name"

                func_name = func_name or api_method
                http_method = http_method or 'GET'
            elif len(api_method) == 2:
                api_method_name, func_name = api_method
                assert isinstance(api_method_name, basestring), "Invalid API method name"

                func_name = func_name or api_method
                http_method = 'GET'
            elif len(api_method) == 1:
                api_method_name = api_method[0]
                assert isinstance(api_method_name, basestring), "Invalid API method name"

                func_name = api_method_name
                http_method = 'GET'
            else:
                raise ValueError("Invalid API method definition: {} parameters!"
                                 .format(len(api_method)))
        else:
            raise TypeError("Invalid API method type: {!r}".format(type(api_method)))

        setattr(
            cls,
            func_name,
            wrapped_send(api_method_name, http_method)
        )


class ApiBase(object):
    __metaclass__ = ApiBaseMeta
    path = None
    namespace = None
    methods = None

    def __init__(self, connection, version, namespace_prefix=WEBAPI_PREFIX):
        assert int(version), "version number must be integer"

        self.conn = connection
        self.version = str(version)
        self.prefix = namespace_prefix or u''
        self.path = u'/'.join([self.prefix, self.path])
        self._handlers = {}

    @property
    def base_params(self):
        return {
            'api': self.namespace,
            'version': self.version
        }

    def set_handler_for(self, api_method, handler):
        self._handlers[api_method] = handler

    def has_handler_for(self, api_method):
        return api_method in self._handlers

    def get_handler_for(self, api_method):
        return self._handlers[api_method]

    def remove_handler_for(self, api_method):
        del self._handlers[api_method]