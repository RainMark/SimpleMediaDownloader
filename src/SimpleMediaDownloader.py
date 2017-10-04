#!/usr/bin/python3

import os, sys, logging
import argparse, io

from urllib import parse
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
                k = x[1]
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
def api_v1_post_search():
    print(request.form)
    kv_pair = request.form
    html = '<tbody id=\"table-body\">'
    html += '</tbody>'
    if not kv_pair.get('key'):
        return Response(response = html, status = 200)


    result = downloader.searcher.Search(kv_pair['key'])
    if not result:
        return Response(response = html, status = 200)

    path = os.path.abspath('web/template/table.template')
    html_template = Template()
    html_template.load_from_file(path)

    html = '<tbody id=\"table-body\">'
    for x in result:
        html += html_template.render(_id = x[0], name = x[1])
    html += '</tbody>'

    return Response(response = html, status = 200)

@app.route('/api/v1/download', methods = ['POST'])
def api_v1_post_download():
    print(request.form)
    kv_pair = request.form
    if not kv_pair.get('id'):
        return api_v1_error()

    url = downloader.searcher.api.GetSongUri(kv_pair['id'])
    if not url:
        return api_v1_error()

    binary_data = downloader.searcher.api.open_url(url[kv_pair['id']])
    if not binary_data:
        return api_v1_error()

    byte_buffer = io.BytesIO(binary_data)
    response = send_file(byte_buffer, mimetype = 'audio/mpeg')
    response.headers['Content-Length'] = len(byte_buffer.getbuffer())
    return response

@app.route('/api/v1/download/<_id>', methods = ['GET'])
def api_v1_get_download(_id):
    if not _id:
        return api_v1_error()

    url_dict = downloader.searcher.api.GetSongUri(_id)
    if not url_dict:
        return api_v1_error()

    binary_data = downloader.searcher.api.open_url(url_dict[_id])
    if not binary_data:
        return api_v1_error()

    byte_buffer = io.BytesIO(binary_data)
    response = send_file(byte_buffer, mimetype = 'audio/mpeg')
    response.headers['Content-Length'] = len(byte_buffer.getbuffer())
    return response


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












