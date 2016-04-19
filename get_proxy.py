import ConfigParser
import psycopg2
import logging

class GetProxyTools(object):
    def __init__(self, cursor):
        self.cursor = cursor

    def get_proxy(self): 
        self.cursor.execute("SELECT * FROM proxy_list ORDER BY random() LIMIT 1")
        out = self.cursor.fetchone()
        return "{protocol}://{addr}:{port}".format(protocol = out[4].strip(), addr=out[1].strip(), port=out[2].strip())

class GetProxy(object):
    def __init__(self, loglevel=30, *pargs, **kargs):
        logging.basicConfig(level=loglevel)
        logging.debug("Parse config")
        
        iniparser = ConfigParser.ConfigParser()
        iniparser.read("proxy_list.ini")

        self.db_name = iniparser.get("Database", "database")
        self.db_user = iniparser.get("Database", "user")
        self.db_pass = iniparser.get("Database", "pass")

    def __enter__(self):
        logging.debug("Connect to database")
        self.connect = psycopg2.connect("dbname={0} user={1} password={2}".format(self.db_name, self.db_user, self.db_pass))
        self.cursor = self.connect.cursor()
        return GetProxyTools(self.cursor)

    def __exit__(self, exc_type, exc_value, traceback):
        logging.debug("Close connection")
        self.connect.commit()
        self.cursor.close()
        self.connect.close()

with GetProxy(loglevel=0) as gp:
    for i in range(15):
        print(gp.get_proxy())
