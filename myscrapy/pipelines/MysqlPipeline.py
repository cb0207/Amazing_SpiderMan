# -*- coding: utf-8 -*-


from scrapy.exceptions import NotConfigured

# ITEM_PIPELINES = {
#     # 'Amazing_SpiderMan.myscrapy.pipelines.MysqlPipeline.MysqlPipeline': 300,
# }
# # MYSQL host
# MYSQL_URI = 'localhost:3306'

# # MYSQL database
# MYSQL_DATABASE = 'job'

# # MYSQL table
# MYSQL_TABLE = 'jobsearch'

# # MYSQL use
# MYSQL_USER = 'jobsearch'

# # MYSQL password
# MYSQL_PASS = 'jobsearch'

from ...DBConsole.DBConsole.DataStore import Database


class MysqlPipeline(object):

    def __init__(self, mysql_url, mysql_db, mysql_table, mysql_user, mysql_pass):
        self.INIT_DEFAULT = {
            'dbtype': 'mysql',
            'addr': mysql_url,
            'database': mysql_db,
            'table': mysql_table,
            'user': mysql_user,
            'password': mysql_pass,
            'col': {}
        }

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.get('MYSQL_URI'):
            raise NotConfigured
        return cls(
            mysql_url=crawler.settings.get('MYSQL_URI'),
            mysql_db=crawler.settings.get('MYSQL_DATABASE'),
            mysql_table=crawler.settings.get('MYSQL_TABLE'),
            mysql_user=crawler.settings.get('MYSQL_USER'),
            mysql_pass=crawler.settings.get('MYSQL_PASS')
        )

    def open_spider(self, spider):
        self.client = ''

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if not self.client:
            self.INIT_DEFAULT['col'] = dict(item)
            self.client = Database(**self.INIT_DEFAULT)

        self.client.store_data(dict(item))
        return item

