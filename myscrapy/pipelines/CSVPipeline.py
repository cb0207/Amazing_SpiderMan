# -*- coding: utf-8 -*-

from scrapy.exceptions import NotConfigured
import csv
# ITEM_PIPELINES = {
#     # 'Amazing_SpiderMan.myscrapy.pipelines.CSVPipeline.CSVPipeline': 300,
# }
# CSV_ADDR = '/Users/cb/Downloads/Project/Project_crawler job/Project/Result Data/jobsearch.csv'


class CSVPipeline(object):

    def __init__(self, csv_addr):
        self.file = open(csv_addr, 'a', encoding='utf-8')
        self.f_csv = ''

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.get('CSV_ADDR'):
            raise NotConfigured
        return cls(
            csv_addr=crawler.settings.get('CSV_ADDR'),
        )

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        if not self.f_csv:
            self.f_csv = csv.DictWriter(self.file, dict(item).keys())

        self.f_csv.writerow(dict(item))
        self.file.flush()
        return item

