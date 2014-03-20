# -*- coding: utf-8 -*-
from .base import ApiBase


class Info(ApiBase):
    path = 'query.cgi'
    namespace = 'SYNO.API.Info'
    methods = 'query'


class Auth(ApiBase):
    path = 'auth.cgi'
    namespace = 'SYNO.API.Auth'
    methods = ('login', 'logout')


class DownloadStationInfo(ApiBase):
    path = 'DownloadStation/info.cgi'
    namespace = 'SYNO.DownloadStation.Info'
    methods = [
        ('getinfo', 'get_info'),
        ('getconfig', 'get_config'),
        ('setserverconfig', 'set_server_config')
    ]


class DownloadStationSchedule(ApiBase):
    path = 'DownloadStation/schedule.cgi'
    namespace = 'SYNO.DownloadStation.Schedule'
    methods = [('getconfig', 'get_config'), ('setconfig', 'set_config')]


class DownloadStationTask(ApiBase):
    path = 'DownloadStation/task.cgi'
    namespace = 'SYNO.DownloadStation.Task'
    methods = [
        'list', 'pause', 'resume', 'delete',
        ('getinfo', 'get_info'),
        ('create', 'create', 'POST')
    ]


