#!/usr/bin/python3

import json, sys, random
from Network import Network

class QQApi(object):
    def __init__(self):
        self.search_url = 'https://c.y.qq.com/soso/fcgi-bin/search_cp?'
        self.musicexpress_url = 'https://c.y.qq.com/base/fcgi-bin/fcg_musicexpress.fcg?'
        self.download_url = 'http://dl.stream.qqmusic.qq.com/'
        self.network = Network()
        self.size_map = {
            'size128':'M500',
            'size320':'M800'}

    def Search(self, keyword, page, limit = 10):
        param = {
            'p':page,
            'n':limit,
            'w':keyword,
            'aggr':1,
            'lossless':1,
            'cr':1}

        uri = self.search_url + self.network.urlencode(param)
        data = self.network.urlrequest(uri)
        if not data:
            return None

        return self.Parse(data)

    def Parse(self, js_data):
        size = len(js_data)
        raw_dict = json.loads(js_data[9:size - 1])
        data_dict = raw_dict['data']
        song_dict = data_dict['song']
        song_list = song_dict['list']
        simple_song_list = []
        for x in song_list:
            simple_song_dict = {}
            simple_song_dict['songname'] = x['songname']
            simple_song_dict['songid'] = x['songmid']
            simple_singer_list = []
            for k in x['singer']:
                simple_singer_list.append(k['name'])
            simple_song_dict['singername'] = simple_singer_list
            simple_song_list.append(simple_song_dict)

        return simple_song_list

    def GetMediaUrl(self, songid, size = 'size320'):
        guid = int(random.random() * 1000000000)
        param = {
            'json':3,
            'guid':guid}
        uri = self.musicexpress_url + self.network.urlencode(param)
        js_data = self.network.urlrequest(uri)
        if not js_data:
            return None
        length = len(js_data)
        data = json.loads(js_data[13:length - 2])
        url = self.download_url + self.size_map[size] + songid + '.mp3?'
        param = {
            'vkey':data['key'],
            'guid':guid,
            'fromtag':30}
        return url + self.network.urlencode(param)

if __name__ == '__main__':
    Api = QQApi()
    songlist = Api.Search('我是一只鱼', 1)
    if not songlist:
        sys.exit()

    for x in songlist:
        print(x)
        url = Api.GetMediaUrl(x['songid'])
        print(url)










