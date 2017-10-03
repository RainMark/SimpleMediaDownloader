#!/usr/bin/python3

import json

from MusicApi import MusicApi

class Searcher(object):
    def __init__(self):
        self.api = MusicApi()

    def Search(self, key, limit = 8, page = 1):
        result = self.api.SearchRequest(key, limit, page)
        if not result or result['success'] != True:
            return

        song_list = result['songList']
        id_name_list = list()
        for song in song_list:
            filename = self.api.CreateFileNameFromJson(song)
            pair = [song['id'], filename]
            id_name_list.append(pair)
        return id_name_list

if __name__ == '__main__':
    s = Searcher()
    song_list = s.Search('叶炫清')
    for v in song_list:
        print(v)

    song_list = s.Search('叶炫清', 10, 2)
    for v in song_list:
        print(v)
