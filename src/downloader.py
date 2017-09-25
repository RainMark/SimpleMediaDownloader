#!/usr/bin/python3

import os, json, shutil, logging
from urllib import request, parse

import musicapi

class Downloader(object):
    def __init__(self, download_dir):
        self.download_dir = os.path.expanduser(download_dir)
        retval = os.path.isdir(self.download_dir)
        if not retval:
            os.mkdir(self.download_dir)

    @musicapi.MusicApi.network_check
    def DownloadSingle(self, filename,  url):
        path = os.path.join(self.download_dir, filename + '.mp3')
        with request.urlopen(url) as f:
            with open(path, 'wb') as out_file:
                shutil.copyfileobj(f, out_file)

    def Download(self, url_list):
        for url in url_list:
            for k, v in url.items():
                for kid, vurl in v.items():
                    info = 'Start to download {} ...'.format(k)
                    logging.info(info)
                    self.DownloadSingle(k, vurl)
                    info = 'Download {} success.'.format(k)
                    logging.info(info)

if __name__ == '__main__':
    d = Downloader()
