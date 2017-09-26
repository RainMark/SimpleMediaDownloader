#!/usr/bin/python3

import os, sys, logging
import argparse

from flask import Flask
from flask import request
from flask import Response
from flask import send_file
from jinja2 import Environment, PackageLoader, select_autoescape

from Searcher import Searcher
from Downloader import Downloader

class SimpleMediaDownloader(object):
    def __init__(self, download_dir = '~/sqdownload'):
        self.downloader = Downloader(download_dir)
        self.searcher = Searcher()

    def Download(self, download_numbers, songs):
        url_list = list()
        for i in download_numbers:
            url_list.append(songs[int(i)])
        self.downloader.Download(url_list)

    def terminal_run(self):
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





global downloader
app = Flask(__name__)

def api_v1_error():
    return Response(response = '<h4>Error</h4>', status = 200)

@app.route('/api/v1/search', methods = ['POST'])
def api_v1_search():
    print(request.form)
    kv_pair = request.form
    if not kv_pair.get('key'):
        return api_v1_error()


    result = downloader.searcher.Search(kv_pair['key'])
    env = Environment(loader = PackageLoader('SimpleMediaDownloader', 'templates'),
                      autoescape = select_autoescape(['html', 'xml']))
    template = env.get_template('web/template/table.jinja2')
    html = '<tbody id=\"table-body\">\n'
    for name, url_dict in result.items():
        html += template.render(ID = url_dict.values[0], NAME = name)

    html += '</tbody>\n'
    return Response(response = html, status = 200)




if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", help="Set download path")
    parser.add_argument("-s", "--server", help="Start as a web server")
    parser.add_argument("-p", "--port", help="Web server port", type=int)

    args = parser.parse_args()
    if args.directory and os.path.isdir(args.directory):
        downloader = SimpleMediaDownloader(args.directory)
    else:
        downloader = SimpleMediaDownloader()
        logging.info('Use default directory')

    if args.server and args.server == 'yes':
        if args.port:
            try:
                app.run(port = args.port)
            except PermissionError as e:
                logging.error('Permission denied')
        else:
            logging.info('Use default port')
            app.run()
    else:
        downloader.terminal_run()












