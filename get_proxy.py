import sqlite3
import os
import sys
import ConfigParser

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ini_config  = ConfigParser.ConfigParser()
ini_config.read(os.path.join(BASE_DIR, "proxy_list.cfg"))
DB_NAME     = ini_config.get("Database", "db_name")
DB_PATH     = os.path.join(BASE_DIR, DB_NAME)

class GetProxy(object):
    def __init__(self):
        if not os.path.exists(DB_PATH):
            print("[%s] doesn't exists. Run create_proxy_list.py" % DB_PATH)
            sys.exit(1)
        self.connect = sqlite3.connect(DB_PATH)
        self.cursor = self.connect.cursor()

    def __del__(self):
        if hasattr(self, "commit"):
            self.connect.commit()
            self.connect.close()

    def get_proxy(self):
        query = "SELECT * FROM proxy_list ORDER BY random() LIMIT 1"
        return self.make_query(query)

    def get_https_proxy(self):
        query = "SELECT * FROM proxy_list WHERE protocol = 'https' ORDER BY random() LIMIT 1"
        return self.make_query(query)

    def make_query(self, query):
        try:
            self.cursor.execute(query)
        except sqlite3.OperationalError:
            print("Something wrong with database, run create_proxy.py, exit...")
            sys.exit(2)

        out = self.cursor.fetchone()
        pattern = u"{protocol}://{addr}:{port}"
        return pattern.format(protocol=out[3].strip(), addr=out[0].strip(), port=out[1].strip())




