# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os.path
import sqlite3
import logging
import ConfigParser

BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ini_config  = ConfigParser.ConfigParser()
ini_config.read(os.path.join(BASE_DIR, "proxy_list.cfg"))
DB_NAME     = ini_config.get("Database", "db_name")
DB_PATH     = os.path.join(BASE_DIR, DB_NAME)

def create_table(cursor):
    cursor.execute("""CREATE TABLE IF NOT EXISTS \"proxy_list\"(
        address     TEXT NOT NULL,
        port        TEXT NOT NULL,
        country     TEXT NOT NULL,
        protocol    TEXT NOT NULL,
        added       TEXT NOT NULL,
        UNIQUE(address, port)
    )""")


def write_proxy(cursor, item, logger):
    try:
        cursor.execute(u"""INSERT INTO \"proxy_list\"(address, port, country, protocol, added)
            VALUES('{addr}', '{port}', '{country}', '{protocol}', datetime('now', 'localtime') )""".format(
            addr=item['address'],
            port=item['port'],
            country=item['country'],
            protocol=item['protocol']
            )
        )
    except sqlite3.IntegrityError:
        logger.warning("Attem to write a proxy that already exists. Skipped...")


def clear_table(cursor):
    cursor.execute("DELETE FROM \"proxy_list\"")


class ProxyListPipeline(object):
    def __init__(self):
        self.logger = logging.getLogger()

    def process_item(self, item, spider):
        write_proxy(self.cursor, item, self.logger)
        return item

    def open_spider(self, spider):
        self.connect = sqlite3.connect(DB_PATH)
        self.cursor = self.connect.cursor()
        create_table(self.cursor)
        clear_table(self.cursor)

    def close_spider(self, spider):
        self.connect.commit()
        self.cursor.close()
        self.connect.close()
