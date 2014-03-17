# -*- coding: utf-8 -*-
import itertools as it
from collections import defaultdict

COMMON_ERROR_CODES = (
    u'',
    {
        100: 'Unknown error',
        101: 'Invalid parameter',
        102: 'The requested API does not exist',
        103: 'The requested method does not exist',
        104: 'The requested version does not support the functionality',
        105: 'The logged in session does not have permission',
        106: 'Session timeout',
        107: 'Session interrupted by duplicate login'
    }
)

AUTH_API_ERROR_CODES = (
    u'SYNO.API.Auth',
    {
        400: 'No such account or incorrect password',
        401: 'Guest account disabled',
        402: 'Account disabled',
        403: 'Wrong password',
        404: 'Permission denied'
    }
)

DS_API_ERROR_CODES = (
    u'SYNO.DownloadStation.Task',
    {
        400: 'File upload failed',
        401: 'Max number of tasks reached',
        402: 'Destination denied',
        403: 'Destination does not exist',
        404: 'Invalid task id',
        405: 'Invalid task action'
    }
)


def _build_error_map():
    all_errors = defaultdict(dict)
    for namespace, errors in it.chain([COMMON_ERROR_CODES, AUTH_API_ERROR_CODES,
                                       DS_API_ERROR_CODES]):
        for errno, msg in errors.iteritems():
            all_errors[errno][namespace] = msg
    return all_errors

ALL_ERROR_CODES = _build_error_map()


def get_error_msg(errno, namespace):
    assert int(errno), "error code must be integer"

    if errno not in ALL_ERROR_CODES:
        raise ValueError("Unknown error code")
    if 100 <= errno <= 107:
        # Common error
        namespace = u''
    return ALL_ERROR_CODES[errno][namespace]


def format_error(errno, namespace):
    msg = u'Error: {}'
    try:
        error_msg = get_error_msg(errno, namespace)
    except ValueError:
        error_msg = u'The server returned an unknown error code'
    return msg.format(error_msg)