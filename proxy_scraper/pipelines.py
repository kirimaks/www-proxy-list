# -*- coding: utf-8 -*-

import pymongo
from pymongo.errors import DuplicateKeyError


class MongoPipe:
    def open_spider(self, spider):
        self.client = pymongo.MongoClient("mongodb")
        self.db = self.client['proxy_list']
        self.collection = self.db['proxy']

    def close_spider(self, spider):
        self.client.close()


    def process_item(self, item, spider):
        if item['protocol'] != "https":
            return None

        try:
            self.collection.insert(dict(item))
        except DuplicateKeyError:
            spider.logger.info("{} exists, skipping..".format(item['address']))

        return item
