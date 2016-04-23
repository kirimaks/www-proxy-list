import sqlite3
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class GetProxy(object):
    def __init__(self):
        self.dbname = "data.db"

        if not os.path.exists(os.path.join(BASE_DIR, self.dbname)):
            print("[%s] doesn't exists. Run create_proxy_list.py" % self.dbname)
            sys.exit(1)
        self.connect = sqlite3.connect(os.path.join(BASE_DIR, self.dbname))
        self.cursor = self.connect.cursor()

    def __del__(self):
        if hasattr(self, "commit"):
            self.connect.commit()
            self.connect.close()

    def get_proxy(self):
        try:
            self.cursor.execute("SELECT * FROM proxy_list ORDER BY random() LIMIT 1")
        except sqlite3.OperationalError:
            print("Something wrong with database, run create_proxy.py, exit...")
            sys.exit(2)

        out = self.cursor.fetchone()
        pattern = "{protocol}://{addr}:{port}"
        return pattern.format(protocol=out[4].strip(), addr=out[1].strip(), port=out[2].strip())
