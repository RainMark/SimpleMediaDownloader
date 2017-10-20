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
            songid text PRIMARY KEY NOT NULL,
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
        sql = 'SELECT songid, songname, songurl, songimageurl, singername FROM song WHERE songid = ?'
        try:
            self.cursor.execute(sql, (_id, ))
            self.connect.commit()
        except sqlite3.Error as e:
            logging.error(e)
        line = self.cursor.fetchone()
        logging.debug(line)
        return line

    def put_song(self, songid, songname, songurl, singername, songimageurl):
        data = (songid, songname, songurl, singername, songimageurl)
        sql = 'INSERT INTO song VALUES(?,?,?,?,?)'
        try:
            self.cursor.execute(sql, data)
            self.connect.commit()
        except sqlite3.Error as e:
            logging.warning(e)

if __name__ == '__main__':
    logging.basicConfig(level = logging.INFO)
    s = SQLiteDB('/tmp/sqlite3.test')
    s.init_schema()
    s.put_song('M800004XoG1L4J03df', 'Get it on the floor', '/qqmusic/M800004XoG1L4J03df.mp3?fromtag=30&vkey=C95E2CC7099603F59784942B800A45CF2546623E5C245549CEB09549C31D2C2F1E8752D2E9B2878909500DDE2CF2A6BF7AB6048ACFE955E2&guid=775321321', 'VAVA', 'https://images.xxx')
    s.get_song('M800004XoG1L4J03df')
    s.get_song('M800004VoG1L4J03df')
    s.connect.close()
