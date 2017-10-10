#!/usr/bin/python3

import sys, os, logging
from urllib import request, parse, error

class Network(object):
    def __init__(self):
        # Dirty hack.
        major, minor, _, _, _ = sys.version_info
        if major == 3 and minor < 5:
            self.has_quote_plus = False
        else:
            self.has_quote_plus = True

    def network_check(func):
        def wrapper(*args, **kw):
            try:
                return func(*args, **kw)
            except error.HTTPError as e1:
                logging.warning(e1)
            except error.URLError as e2:
                logging.warning(e2)
        return wrapper

    @network_check
    def urlrequest(self, url):
        raw_data = request.urlopen(url).read()
        if not raw_data:
            return None
        return raw_data.decode('utf-8')

    def urlencode(self, param_dict):
        if self.has_quote_plus:
            encode_data = parse.urlencode(param_dict, quote_via = parse.quote_plus)
        else:
            encode_data = parse.urlencode(param_dict)

        return encode_data
