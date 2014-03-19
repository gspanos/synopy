# -*- coding: utf-8 -*-


def extract_sid(resp):
    """ Extract the sid from a successful login response.

    example 'set-cookie' returned from SYNO.API.Auth:

        'id=pKz8slWFwaxBU;expires=Thu, 17-Apr-2014 20:10:44 GMT;path=/'
    """
    auth_cookie = resp.headers['set-cookie']
    cookie_vals = auth_cookie.split(';')
    sid_val = filter(lambda v: v.split('=')[0] == 'id', cookie_vals)
    return sid_val[0].split('=')[1]
