#!/usr/bin/python3

import os, hashlib, shutil, json, logging
from urllib import request, parse

class MusicApi(object):
    def __init__(self, api_type = 'qq'):
        self.api_type = api_type
        self.search_uri = r'https://music-api-pjheqeosjj.now.sh/api/search/song/{}?'.format(self.api_type)
        self.download_uri = r'https://music-api-pjheqeosjj.now.sh/api/get/song/{}?'.format(self.api_type)

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
    def SearchRequest(self, search_key, limit, page):
        data = dict()
        data['key'] = search_key
        data['limit'] = limit
        data['page'] = page
        encode_data = parse.urlencode(data, quote_via = parse.quote_plus)
        request_url = self.search_uri + encode_data
        json_data = request.urlopen(request_url).read()
        return json.loads(json_data)

    @network_check
    def GetSongUri(self, id):
        encode_data = parse.urlencode({'id':id}, quote_via = parse.quote_plus)
        request_url = self.download_uri + encode_data
        json_data = request.urlopen(request_url).read()
        loaded_data = json.loads(json_data)
        if loaded_data['success']:
            return {id:loaded_data['url']}

    def CreateFileNameFromJson(self, json_data):
        artists = json_data['artists'][0]['name']
        for v in json_data['artists'][1:]:
            artists = artists + ' + ' + v['name']
        return json_data['name'] + ' - ' + artists

if __name__ == '__main__':
    api = MusicApi('qq')
    data = api.SearchRequest('日落大道', 5, 1)
    song_url = api.GetSongUri('004N9Bzc2hAl0G')
    print(song_url)
    for k, v in song_url.items():
        print(k, v)
