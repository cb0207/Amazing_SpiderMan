# -*- coding: utf-8 -*-

import pymongo
# from settings import DB_CONFIG, DEFAULT_SCORE

from Amazing_SpiderMan.DBConsole.DBConsole.BasicSql import BasicSql


class MongoItem(BasicSql):

    # def __init__(self, type, addr, database, table, user, password, col):
    def __init__(self, kwargs):

        con_string = "mongodb://%s/" %kwargs['addr']
        self.client = pymongo.MongoClient(con_string, connect=False)
        self.db = kwargs['database']
        self.coletn = kwargs['table']

    def init_db(self):
        self.db = self.client.get_database(self.db)
        self.coletn = self.db.get_collection(self.coletn)

    def drop_db(self):
        self.client.drop_database(self.db)

    def insert(self, value=None):
        try:
            if value:
                self.coletn.insert(value)
        except Exception as e:
            return e

    # def delete(self, conditions=None):
    #     if conditions:
    #         self.coletn.remove(conditions)
    #         return ('deleteNum', 'ok')
    #     else:
    #         return ('deleteNum', 'None')
    #
    # def update(self, conditions=None, value=None):
    #     # update({"UserName":"libing"},{"$set":{"Email":"libing@126.com","Password":"123"}})
    #     if conditions and value:
    #         self.coletn.update(conditions, {"$set": value})
    #         return {'updateNum': 'ok'}
    #     else:
    #         return {'updateNum': 'fail'}
    #
    # def select(self, count=None, conditions=None):
    #     if count:
    #         count = int(count)
    #     else:
    #         count = 0
    #     if conditions:
    #         conditions = dict(conditions)
    #         if 'count' in conditions:
    #             del conditions['count']
    #         conditions_name = ['types', 'protocol']
    #         for condition_name in conditions_name:
    #             value = conditions.get(condition_name, None)
    #             if value:
    #                 conditions[condition_name] = int(value)
    #     else:
    #         conditions = {}
    #     items = self.coletn.find(conditions, limit=count).sort(
    #         [("speed", pymongo.ASCENDING), ("score", pymongo.DESCENDING)])
    #     results = []
    #     for item in items:
    #         result = (item['ip'], item['port'], item['score'])
    #         results.append(result)
    #     return results

    def close(self):
        self.client.close()

if __name__ == '__main__':
    # from db.MongoHelper import MongoHelper as SqlHelper
    # sqlhelper = SqlHelper()
    # sqlhelper.init_db()
    # # print  sqlhelper.select(None,{'types':u'1'})
    # items= sqlhelper.proxys.find({'types':0})
    # for item in items:
    # print item
    # # # print sqlhelper.select(None,{'types':u'0'})
    pass
