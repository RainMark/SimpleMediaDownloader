#!/usr/bin/python3

import json, sys, random
from Network import Network

class QQApi(object):
    def __init__(self):
        self.search_url = 'https://c.y.qq.com/soso/fcgi-bin/search_cp?'
        self.musicexpress_url = 'https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?'
        self.download_url = 'http://dl.stream.qqmusic.qq.com/'
        self.album_url = 'https://y.gtimg.cn/music/photo_new/T002R300x300M000'
        self.network = Network()

    def Search(self, keyword, page, limit = 8):
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
            simple_song_dict['albumurl'] = self.album_url + x['albummid'] + '.jpg'
            simple_song_dict['songmid'] = x['songmid']
            simple_singer_list = []
            for k in x['singer']:
                simple_singer_list.append(k['name'])
            simple_song_dict['singername'] = simple_singer_list
            simple_song_list.append(simple_song_dict)

        return simple_song_list

    def GetMediaUrl(self, songmid, media_mid):
        uin = int(random.random() * 1000000000)
        guid = int(random.random() * 1000000000)
        filename = 'C400' + str(media_mid) + '.m4a'
        param = {
            'cid' : '205361747',
            'format': 'json',
            'uin': uin,
            'songmid': songmid,
            'filename': filename,
            'guid': guid}
        uri = self.musicexpress_url + self.network.urlencode(param)
        js_data = self.network.urlrequest(uri)
        if not js_data:
            return None
        length = len(js_data)
        data = json.loads(js_data)['data']
        url = self.download_url + filename + '?'
        param = {
            'uin': uin,
            'vkey': data['items'][0]['vkey'],
            'guid': guid,
            'fromtag': 66}
        return url + self.network.urlencode(param)

if __name__ == '__main__':
    Api = QQApi()
    songlist = Api.Search('醒来', 1)
    if not songlist:
        sys.exit()

    for x in songlist:
        print(x)
        url = Api.GetMediaUrl(x['songmid'], x['media_mid'])
        print(url)











