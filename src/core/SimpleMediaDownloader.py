#!/usr/bin/python3

import os, sys, logging
import argparse, io, urllib

from flask import Flask
from flask import request
from flask import Response
from flask import send_file
from flask_cors import CORS

from MusicApi import MusicApi
from Template import Template

app = Flask(__name__)
Api = MusicApi()
CORS(app)

def api_v1_error():
    error_message = 'Unexpected error'
    return Response(response = error_message, status = 404)

@app.route('/api/v1/search', methods = ['POST'])
def api_v1_post_search():
    logging.info(request.form)
    kv_pair = request.form
    html = '<tbody id=\"table-body\">'
    html += '</tbody>'
    if not kv_pair.get('key'):
        return Response(response = html, status = 200)


    result = Api.Search(kv_pair['key'])
    if not result:
        return Response(response = html, status = 200)

    path = os.path.abspath('../site/template/table.template')
    html_template = Template()
    html_template.load_from_file(path)

    html = '<tbody id=\"table-body\">'
    __id = 1
    for x in result:
        display = x['songname'] + ' - ' + Api.Singer(x)
        qqmusicurl = Api.GetMediaUrl(x['songid'])
        if not qqmusicurl:
            url = ''
        else:
            url = '/qqmusic' + qqmusicurl.split('dl.stream.qqmusic.qq.com')[1]
        html += html_template.render(_id = __id, name = display, url = url)
        __id += 1
    html += '</tbody>'

    return Response(response = html, status = 200)


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help="Web server port", type=int)
    args = parser.parse_args()
    if args.port:
        try:
            app.run(port = args.port)
        except PermissionError as e:
            logging.error('Permission denied')
    else:
        logging.info('Use default port')
        app.run()











