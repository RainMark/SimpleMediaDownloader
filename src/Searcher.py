#!/usr/bin/python3

import json

from MusicApi import MusicApi

class Searcher(object):
    def __init__(self):
        self.api = MusicApi()

    def Search(self, key):
        result = self.api.SearchRequest(key, 5, 1)
        if not result or result['success'] != True:
            return

        song_list = result['songList']
        song_url_list = list()
        for song in song_list:
            filename = self.api.CreateFileNameFromJson(song)
            song_url = self.api.GetSongUri(song['id'])
            song_url_list.append({filename:song_url})

        return song_url_list

if __name__ == '__main__':
    s = Searcher()
    song_list = s.Search('林俊杰')
    for v in song_list:
        print(v)
