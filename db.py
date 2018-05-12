import sqlite3
import os


class ConnectionCM:
    def __init__(self):
        self.conn = sqlite3.connect('db.sqlite')

    def __enter__(self):
        return self.conn

    def __exit__(self, type, value, traceback):
        self.conn.close()


def init_db(token):
    try:
        os.remove('db.sqlite')
    except FileNotFoundError:
        pass

    with ConnectionCM() as conn:
        with conn:
            with open('db.sqlite.sql', 'r') as f:
                conn.executescript(f.read())

            conn.execute("INSERT INTO token (token) VALUES (?)", (token,))


def getToken():
    with ConnectionCM() as conn:
        c = conn.cursor()
        c.execute("SELECT (token) FROM token")
        return c.fetchone()[0]
