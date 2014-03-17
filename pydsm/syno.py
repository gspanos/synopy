# -*- coding: utf-8 -*-

WEBAPI_PREFIX = 'webapi'


class ApiBase(object):
    path = None
    namespace = None

    def __init__(self, request_manager, version, namespace_prefix=WEBAPI_PREFIX):
        assert int(version), "port number must be integer"

        self.request_manager = request_manager
        self.version = str(version)
        self.prefix = namespace_prefix or u''
        self.path = u'/'.join([self.prefix, self.path])

    @property
    def base_params(self):
        return {
            'api': self.namespace,
            'version': self.version
        }


class ApiInfo(ApiBase):
    path = 'query.cgi'
    namespace = 'SYNO.API.Info'

    def query(self, *args):
        params = self.base_params
        params['method'] = 'query'
        params['query'] = u','.join(args)
        return self.request_manager.run(self.path, 'get', self.namespace, params)


class ApiAuth(ApiBase):
    path = 'auth.cgi'
    namespace = 'SYNO.API.Auth'

    def login(self, account, password):
        params = self.base_params
        params['method'] = 'login'
        params['account'] = account
        params['passwd'] = password
        return self.request_manager.run(self.path, 'get', self.namespace, params)

    def logout(self):
        return


class ApiDownloadStationInfo(ApiBase):
    path = 'DownloadStation/info.cgi'
    namespace = 'SYNO.DownloadStation.Info'

    def get_info(self):
        params = self.base_params
        params['method'] = 'getinfo'
        return self.request_manager.run(self.path, 'get', self.namespace,
                                        params, use_auth=True)

    def get_config(self):
        params = self.base_params
        params['method'] = 'getconfig'
        return self.request_manager.run(self.path, 'get', self.namespace,
                                        params, use_auth=True)

    def set_server_config(self, **kwargs):
        params = self.base_params
        params['method'] = 'setserverconfig'
        params.update(kwargs)
        return self.request_manager.run(self.path, 'get', self.namespace,
                                        params, use_auth=True)


class ApiDownloadStationTask(ApiBase):
    path = 'DownloadStation/task.cgi'
    namespace = 'SYNO.DownloadStation.Task'
