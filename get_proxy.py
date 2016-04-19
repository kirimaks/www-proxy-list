import ConfigParser
import psycopg2

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class GetProxy(object):
    def __init__(self, loglevel=30, *pargs, **kargs):
        iniparser = ConfigParser.ConfigParser()
        iniparser.read(os.path.join(BASE_DIR, "proxy_list.ini"))

        self.db_name = iniparser.get("Database", "database")
        self.db_user = iniparser.get("Database", "user")
        self.db_pass = iniparser.get("Database", "pass")

        if __debug__: print("*** Connect to database ***")
        self.connect = psycopg2.connect("dbname={0} user={1} password={2}".format(self.db_name, self.db_user, self.db_pass))
        self.cursor = self.connect.cursor()

    def __del__(self):
        if __debug__: print("*** Close connection ***")
        self.connect.commit()
        self.cursor.close()
        self.connect.close()

    def get_proxy(self): 
        if __debug__: print("*** Generate new proxy ***")
        self.cursor.execute("SELECT * FROM proxy_list ORDER BY random() LIMIT 1")
        out = self.cursor.fetchone()
        return "{protocol}://{addr}:{port}".format(protocol = out[4].strip(), addr=out[1].strip(), port=out[2].strip())


if __name__ == "__main__":
    px = GetProxy(0)
    for i in range(5):
        print(px.get_proxy())
