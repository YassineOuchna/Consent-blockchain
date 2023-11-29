import sqlite3 as sq

conn = sq.connect('database.db')
cur = conn.cursor()


class contracts():
    def __init__(self):
        pass
