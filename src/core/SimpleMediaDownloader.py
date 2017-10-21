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

@app.route('/api/v1/search', methods = ['POST'])
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
        info = {'SONG_NAME' : x['songname'] + ' - ' + Api.Singer(x),
                'ORDER'    : order,
                'SOURCE'   : 'QQ',
                'PLAY_URL'  : '/play/' + x['songid']}
        song = DB.get_song(x['songid'])
        if not song:
            qqmusicurl = Api.GetMediaUrl(x['songid'])
            if not qqmusicurl:
                continue

            info['SONG_URL'] = Api.RewriteUrl(qqmusicurl)
            DB.put_song(songid = x['songid'], songname = x['songname'],
                        songurl = info['SONG_URL'], singername = Api.Singer(x),
                        songimageurl = x['albumurl'])
        else:
            info['SONG_URL'] = song[2]

        html += st.render(info)
        order += 1

    html += '</tbody>'
    return Response(response = html, status = 200)

@app.route('/api/v1/play/<_id>', methods = ['GET'])
def api_v1_get_play(_id):
    if not _id:
        return api_v1_error()
    song = DB.get_song(_id)
    if not song:
        return api_v1_error()

    st = SimpleTemplate()
    st.load_from_file('../site/template/player.jinja2')
    var = {'SONG_NAME' : song[1],
           'SONG_URL'  : song[2],
           'SONG_IMAGE': song[3],
           'SINGER'    : song[4]}
    return Response(response = st.render(var), status = 200)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help="Web server port", type=int)
    args = parser.parse_args()

    DB.init_schema()
    if args.port:
        try:
            app.run(port = args.port)
        except PermissionError as e:
            logging.error('Permission denied')
    else:
        logging.info('Use default port')
        app.run()











