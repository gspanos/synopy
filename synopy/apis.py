# -*- coding: utf-8 -*-
from .base import ApiBase


class ApiInfo(ApiBase):
    path = 'query.cgi'
    namespace = 'SYNO.API.Info'
    methods = {
        'query': {'use_auth': False}
    }


class ApiAuth(ApiBase):
    path = 'auth.cgi'
    namespace = 'SYNO.API.Auth'
    methods = {
        'login': {'use_auth': False},
        'logout': {'use_auth': False}
    }


class ApiDownloadStationInfo(ApiBase):
    path = 'DownloadStation/info.cgi'
    namespace = 'SYNO.DownloadStation.Info'
    methods = {
        'getinfo': {'use_auth': True, 'func_name': 'get_info'},
        'getconfig': {'use_auth': True, 'func_name': 'get_config'},
        'setserverconfig': {'use_auth': True, 'func_name': 'set_server_config'}
    }


class ApiDownloadStationSchedule(ApiBase):
    path = 'DownloadStation/schedule.cgi'
    namespace = 'SYNO.DownloadStation.Schedule'
    methods = {
        'getconfig': {'use_auth': True, 'func_name': 'get_config'},
        'setconfig': {'use_auth': True, 'func_name': 'set_config'}
    }


class ApiDownloadStationTask(ApiBase):
    path = 'DownloadStation/task.cgi'
    namespace = 'SYNO.DownloadStation.Task'
    methods = {
        'list': {'use_auth': True},
        'pause': {'use_auth': True},
        'resume': {'use_auth': True},
        'delete': {'use_auth': True},
        'getinfo': {'use_auth': True, 'func_name': 'get_info'},
        'create': {'use_auth': True, 'http_method': 'POST'},
    }


