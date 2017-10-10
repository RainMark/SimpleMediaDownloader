#!/usr/bin/python3

from QQApi import QQApi
from Network import Network

class MusicApi(object):
    def __init__(self, api_type = 'qq'):
        self.api_type = api_type
        if 'qq' == api_type:
            self.Api = QQApi()
        else:
            self.Api = QQApi()

    def Search(self, search_key, page = 1, limit = 8):
        return self.Api.Search(search_key, page, limit)


    def GetMediaUrl(self, _id, size = 'size320'):
        return self.Api.GetMediaUrl(_id, size)

    def Singer(self, simple_song_dict):
        singer = simple_song_dict['singername']
        if not singer:
            return None
        if len(singer) == 1:
            return singer[0]

        display = singer[0]
        for x in singer[1:]:
            display += ','
            display += x
        return display

if __name__ == '__main__':
    Api = MusicApi()
    # songlist = Api.Search('胡桃夹子', 1, 10)
    # if not songlist:
    #     sys.exit()

    # for x in songlist:
    #     print(Api.Singer(x))
        # print(x)
        # url = Api.GetMediaUrl(x['songid'])
        # print(url)

    url = Api.GetMediaUrl('00467ZRM0dnbeq')
    print(url)
