# -*- coding: utf-8 -*-


def extract_sid(resp):
    auth_cookie = resp.headers['set-cookie']
    cookie_vals = auth_cookie.split(';')
    sid_val = filter(lambda v: v.split('=')[0] == 'id', cookie_vals)
    return sid_val[0].split('=')[0]
