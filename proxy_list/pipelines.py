# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os.path
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def create_table(cursor):
    cursor.execute("""CREATE TABLE IF NOT EXISTS \"proxy_list\"(
        pid         INTEGER PRIMARY KEY AUTOINCREMENT,
        address     TEXT NOT NULL,
        port        TEXT NOT NULL,
        country     TEXT NOT NULL,
        protocol    TEXT NOT NULL,
        added       TEXT
    )""")


def write_proxy(cursor, item):
    cursor.execute("""INSERT INTO \"proxy_list\"(address, port, country, protocol, added)
        VALUES('{addr}', '{port}', '{country}', '{protocol}', datetime() )""".format(
            addr=item['address'],
            port=item['port'],
            country=item['country'],
            protocol=item['protocol']
        )
    )


def clear_table(cursor):
    cursor.execute("DELETE FROM \"proxy_list\"")


class ProxyListPipeline(object):
    def __init__(self):
        pass

    def process_item(self, item, spider):
        write_proxy(self.cursor, item)

    def open_spider(self, spider):
        self.connect = sqlite3.connect("data.db")
        self.cursor = self.connect.cursor()
        create_table(self.cursor)
        clear_table(self.cursor)

    def close_spider(self, spider):
        self.connect.commit()
        self.cursor.close()
        self.connect.close()
