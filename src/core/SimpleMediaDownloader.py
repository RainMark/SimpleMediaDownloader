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
from SQLiteDB import SQLiteDB

app = Flask(__name__)
Api = MusicApi()
DB  = SQLiteDB()
DB.init_schema()
CORS(app)

def api_v1_error():
    error_message = 'Unexpected error'
    return Response(response = error_message, status = 404)

@app.route('/search', methods = ['POST'])
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

    path = os.path.abspath('../site/template/search.html')
    html_template = Template()
    html_template.load_from_file(path)

    html = '<tbody id=\"table-body\">'
    order = 1
    for x in result:
        display_name = x['songname'] + ' - ' + Api.Singer(x)
        qqmusicurl = Api.GetMediaUrl(x['songmid'], x['media_mid'])
        if not qqmusicurl:
            continue

        url = '/qqmusic' + qqmusicurl.split('dl.stream.qqmusic.qq.com')[1]
        html += html_template.render_search_html(order = order, song_name = display_name, download_url = url,
                                                 play_url = '/play/{}'.format(x['songmid']))
        DB.put_song(songmid = x['songmid'], media_mid = x['media_mid'], songname = display_name,
                    songurl = url, singername = Api.Singer(x), songimageurl = Api.Image(x))
        order += 1
    html += '</tbody>'

    return Response(response = html, status = 200)

@app.route('/play/<_id>', methods = ['GET'])
def api_v1_get_play(_id):
    logging.info(_id)
    if not _id:
        return api_v1_error()
    template = Template()
    template.load_from_file('../site/template/player.html')
    info = DB.get_song(_id)
    if not info:
        return api_v1_error()
    html = template.render_player_html(song_name = info[2], download_url = info[3],
                                song_image = info[4], singer_name = info[5])
    return Response(response = html, status = 200)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
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











