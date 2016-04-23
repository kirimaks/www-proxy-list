import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class GetProxy(object):
    def __init__(self):
        self.connect = sqlite3.connect(os.path.join(BASE_DIR, "data.db"))
        self.cursor = self.connect.cursor()

    def __del__(self):
        self.connect.commit()
        self.connect.close()

    def get_proxy(self):
        self.cursor.execute("SELECT * FROM proxy_list ORDER BY random() LIMIT 1")
        out = self.cursor.fetchone()
        pattern = "{protocol}://{addr}:{port}"
        return pattern.format(protocol=out[4].strip(), addr=out[1].strip(), port=out[2].strip())
