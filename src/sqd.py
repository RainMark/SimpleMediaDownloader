#!/usr/bin/python3

import os, sys, logging
import searcher, downloader

logging.basicConfig(level=logging.INFO)
class SimpleQQDownloader(object):
    def __init__(self, download_dir = '~/sqdownload'):
        self.downloader = downloader.Downloader(download_dir)
        self.searcher = searcher.Searcher()

    def Download(self, download_numbers, songs):
        url_list = list()
        for i in download_numbers:
            url_list.append(songs[int(i)])
        self.downloader.Download(url_list)

    def run(self):
        quit_loop = False
        while not quit_loop:
            print("What do you want to listen?<\'quit\' to quit shell>")
            key = sys.stdin.readline().strip()
            if key == 'quit':
                quit_loop = True
                break

            print("Searching...")
            songs = self.searcher.Search(key)
            print("I find some music ^0^")
            i = 0
            for x in songs:
                k = list(x.keys())[0]
                output = "{}、{}".format(i, k)
                i += 1
                print(output)
            print("Choose number to download<split by space/default all>")
            numbers = sys.stdin.readline().strip()
            download_list = numbers.split(' ')
            if len(download_list) == 0 or '' == download_list[0]:
                download_list = range(0, len(songs))
            self.Download(download_list, songs)

if __name__ == '__main__':
    app = SimpleQQDownloader()
    app.run()
