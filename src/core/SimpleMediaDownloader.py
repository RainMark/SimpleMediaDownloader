#!/usr/bin/python3

import os, sys, logging
import argparse, io, urllib

from flask import Flask
from flask import request
from flask import Response
from flask import send_file
from flask_cors import CORS

from MusicApi import MusicApi
from SimpleTemplate import SimpleTemplate
from SQLiteDB import SQLiteDB

app = Flask(__name__)
Api = MusicApi()
DB  = SQLiteDB()

CORS(app)

def api_v1_error():
    error_message = 'Unexpected error'
    return Response(response = error_message, status = 404)

@app.route('/search', methods = ['POST'])
def api_v1_post_search():
    logging.info(request.form)
    kv_pair = request.form

    html = '<tbody id=\"table-body\"></tbody>'
    if not kv_pair.get('key'):
        return Response(response = html, status = 200)
    result = Api.Search(kv_pair['key'])
    if not result:
        return Response(response = html, status = 200)

    st = SimpleTemplate()
    st.load_from_file('../site/template/list.jinja2')

    html = '<tbody id=\"table-body\">'
    order = 1
    for x in result:
        qqmusicurl = Api.GetMediaUrl(x['songid'])
        if not qqmusicurl:
            continue

        info = {'SONG_NAME' : x['songname'] + ' - ' + Api.Singer(x),
                'SONG_URL'  : Api.RewriteUrl(qqmusicurl),
                'PLAY_URL'  : '/play?songid=' + x['songmid'],
                'ORDER'     : order,
                'SOURCE'    : 'QQ'}
        DB.put_song(songmid = x['songmid'], media_mid = x['media_mid'], songname = x['songname'],
                    songurl = info['SONG_URL'], singername = Api.Singer(x),
                    songimageurl = x['albumurl'])
        html += st.render(info)
        order += 1
    html += '</tbody>'
    return Response(response = html, status = 200)

@app.route('/play', methods = ['GET'])
def api_v1_get_play():
    logging.debug(request.args)
    _id = request.args.get('songid')
    if not _id:
        return api_v1_error()
    song = DB.get_song(_id)
    if not song:
        return api_v1_error()

    st = SimpleTemplate()
    st.load_from_file('../site/template/player.jinja2')
    var = {'SONG_NAME' : song[2],
           'SONG_URL'  : song[3],
           'SONG_IMAGE': song[4],
           'SINGER'    : song[5]}
    return Response(response = st.render(var), status = 200)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help="Web server port", type=int)
    parser.add_argument("-d", "--debug", help="debug mode: yes/no")
    args = parser.parse_args()

    if args.debug and args.debug == 'yes':
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    logging.basicConfig(level=log_level)
    DB.init_schema()
    if args.port:
        try:
            app.run(port = args.port)
        except PermissionError as e:
            logging.error('Permission denied')
    else:
        logging.info('Use default port')
        app.run()











