# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import psycopg2

def create_table(cursor):
    cursor.execute("""CREATE TABLE IF NOT EXISTS \"proxy_list\"(
        pid         SERIAL PRIMARY KEY,
        address     CHAR(16) NOT NULL,
        port        CHAR(8) NOT NULL,
        country     CHAR(32) NOT NULL,    
        protocol    CHAR(8) NOT NULL
    )""")

def write_proxy(cursor, item):
    cursor.execute("""INSERT INTO \"proxy_list\"(address, port, country, protocol) 
        VALUES('{addr}', '{port}', '{country}', '{protocol}' )""".format(
            addr = item['address'],
            port = item['port'],
            country = item['country'],
            protocol = item['protocol']
        )
    )   

def clear_table(cursor):
    cursor.execute("DELETE FROM \"proxy_list\"")

class ProxyListPipeline(object):
    def process_item(self, item, spider):
        write_proxy(self.cursor, item)

    def open_spider(self, spider):
        self.connect = psycopg2.connect("dbname=site_db user=db_user password=1234")
        self.cursor = self.connect.cursor()
        create_table(self.cursor)
        clear_table(self.cursor)

    def close_spider(self, spider):
        self.connect.commit()
        self.cursor.close()
        self.connect.close()
    
