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
    return Response(response = '<h4>Error</h4>', status = 200)

@app.route('/api/v1/search', methods = ['POST'])
def api_v1_post_search():
    print(request.form)
    kv_pair = request.form
    html = '<tbody id=\"table-body\">'
    html += '</tbody>'
    if not kv_pair.get('key'):
        return Response(response = html, status = 200)


    result = Api.Search(kv_pair['key'])
    if not result:
        return Response(response = html, status = 200)

    path = os.path.abspath('web/template/table.template')
    html_template = Template()
    html_template.load_from_file(path)

    html = '<tbody id=\"table-body\">'
    for x in result:
        display = x['songname'] + ' - ' + Api.Singer(x)
        url = Api.GetMediaUrl(x['songid'])
        html += html_template.render(_id = x['songid'], name = display, url = url)
    html += '</tbody>'

    return Response(response = html, status = 200)

@app.route('/api/v1/download', methods = ['POST'])
def api_v1_post_download():
    print(request.form)
    kv_pair = request.form
    if not kv_pair.get('id'):
        return api_v1_error()

    url = Api.GetMediaUrl(kv_pair['id'])
    print(url)
    if not url:
        return api_v1_error()

    binary_data = urllib.request.urlopen(url).read()
    print('Get')
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

    url = Api.GetMediaUrl(kv_pair['id'])
    if not url:
        return api_v1_error()

    binary_data = urllib.request.urlopen(url).read()
    if not binary_data:
        return api_v1_error()

    byte_buffer = io.BytesIO(binary_data)
    response = send_file(byte_buffer, mimetype = 'audio/mpeg')
    response.headers['Content-Length'] = len(byte_buffer.getbuffer())
    return response

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
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











