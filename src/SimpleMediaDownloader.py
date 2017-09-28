#!/usr/bin/python3

import os, sys, logging
import argparse

from flask import Flask
from flask import request
from flask import Response
from flask import send_file
from flask_cors import CORS

from Searcher import Searcher
from Downloader import Downloader
from Template import Template

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
CORS(app)

def api_v1_error():
    return Response(response = '<h4>Error</h4>', status = 200)

@app.route('/api/v1/search', methods = ['POST'])
def api_v1_search():
    print(request.form)
    kv_pair = request.form
    if not kv_pair.get('key'):
        return api_v1_error()


    result = downloader.searcher.Search(kv_pair['key'])
    if not result:
        return api_v1_error()

    path = os.path.abspath('web/template/table.template')
    html_template = Template()
    html_template.load_from_file(path)

    html = '<tbody id=\"table-body\">'
    for x in result:
        name = list(x.keys())[0]
        _id = list(x[name].keys())[0];
        html += html_template.render(_id = _id, name = name)
    html += '</tbody>'

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












