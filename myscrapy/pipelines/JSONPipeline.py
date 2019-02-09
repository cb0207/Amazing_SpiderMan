# -*- coding: utf-8 -*-

from scrapy.exceptions import NotConfigured
import json
# ITEM_PIPELINES = {
#     # 'Amazing_SpiderMan.myscrapy.pipelines.JSONPipeline.JSONPipeline': 300,
# }
# JSON_ADDR = '/Users/cb/Downloads/Project/Project_crawler job/Project/Result Data/jobsearch.json'


class JSONPipeline(object):

    def __init__(self, json_addr):
        self.file = open(json_addr, 'a', encoding='utf-8')


    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.get('JSON_ADDR'):
            raise NotConfigured
        return cls(
            json_addr=crawler.settings.get('JSON_ADDR'),
        )

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        i = json.dumps(dict(item), ensure_ascii=False) + '\n'

        self.file.writelines(i)
        self.file.flush()
        return item

