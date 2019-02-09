# -*- coding: utf-8 -*-

import pymongo
from scrapy.exceptions import NotConfigured

# ITEM_PIPELINES = {
#     # 'Amazing_SpiderMan.myscrapy.pipelines.MongoPipeline.MongoPipeline': 300,
# }
# # mongo host
# MONGO_URI = 'mongodb://127.0.0.1:27017,127.0.0.1:27018,127.0.0.1:27019'
#
# # replicaset
# REPLICASET = 'repset'
#
# # mongo database
# MONGO_DATABASE = 'job'

# # mongo collection
# MONGO_COLLECTION = 'jobsearch'


class MongoPipeline(object):


    def __init__(self, mongo_url, mongo_db, replicaset, mongo_collection):
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db
        self.replicaset = replicaset
        self.collection_name = mongo_collection

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.get('MONGO_URI'):
            raise NotConfigured
        return cls(
            mongo_url=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE'),
            replicaset=crawler.settings.get('REPLICASET'),
            mongo_collection=crawler.settings.get('MONGO_COLLECTION')
        )

    def open_spider(self, spider):
        if self.replicaset:
            self.client = pymongo.MongoClient(self.mongo_url, replicaset=self.replicaset)
        else:
            self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert(dict(item))
        return item
