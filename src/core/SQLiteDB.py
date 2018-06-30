#!/usr/bin/python3

import sqlite3, logging

class SQLiteDB(object):
    def __init__(self, db_path = './data.sqlite'):
        try:
            self.connect = sqlite3.connect(db_path)
        except sqlite3.Error as e:
            logging.error('init database error')

        self.cursor = self.connect.cursor()

    def init_schema(self):
        sql = """
            CREATE TABLE IF NOT EXISTS song(
            songmid text PRIMARY KEY NOT NULL,
            media_mid text NOT NULL,
            songname text NOT NULL,
            songurl text NOT NULL,
            singername text NOT NULL,
            songimageurl text NOT NULL)
        """
        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except e:
            logging.error(e)

    def get_song(self, _id):
        sql = 'SELECT songmid, media_mid, songname, songurl, songimageurl, singername FROM song WHERE songmid = ?'
        try:
            self.cursor.execute(sql, (_id, ))
        except sqlite3.Error as e:
            logging.error(e)
        return self.cursor.fetchone()

    def put_song(self, songmid, media_mid, songname, songurl, singername, songimageurl):
        data = (songmid, media_mid, songname, songurl, singername, songimageurl)
        sql = 'INSERT INTO song VALUES(?,?,?,?,?,?)'
        try:
            self.cursor.execute(sql, data)
            self.connect.commit()
        except sqlite3.Error as e:
            logging.info(e)

    def close(self):
        self.connect.close()

if __name__ == '__main__':
    logging.basicConfig(level = logging.INFO)
    s = SQLiteDB('/tmp/sqlite3.test')
    s.init_schema()
    s.put_song('M800004XoG1L4J03df', 'media_id', 'songname', 'play_url', 'https://images.xxx', 'singername')
    s.get_song('M800004VoG1L4J03df')
    s.connect.close()
