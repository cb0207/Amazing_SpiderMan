# -*- coding: utf-8 -*-

# import sys
from Amazing_SpiderMan.DBConsole.DBConsole.settings import INIT_DEFAULT
from Amazing_SpiderMan.DBConsole.DBConsole.exceptions import NotConfigured #Con_DB_Fail
import pprint


class Database(object):

    def __init__(self, **kwargs):
    # def __init__(self, dbtype=None, addr=None, database=None, table=None, user=None, password=None, col=None):
        '''
        provide col with sample data to init database connection
        col = {'ip': '123.4.5.5', 'score':10, 'name':'abc' }
        :param self:
        :param type: mysql, sqlite3, mongo, redis, csv, txt
        :param addr: file address or db ip+port
        :param database:
        :param table: one table one object
        :param user:
        :param password:
        :param col: column in data, dict, {'ip': column()}
        :return:
        '''

        if not kwargs:
            kwargs = INIT_DEFAULT

        if kwargs.keys() != INIT_DEFAULT.keys():
            print("Your init key is incorrect, pls use INIT_DEFAULT:\n %s" % pprint.pformat(INIT_DEFAULT))
            return


        if kwargs['dbtype'] == ('mysql' or 'sqlite3'):
            from Amazing_SpiderMan.DBConsole.DBConsole.DBtype.SqlItem import SqlItem as DB
        elif kwargs['dbtype'] == 'influx':
            from Amazing_SpiderMan.DBConsole.DBConsole.DBtype.InfluxItem import InfluxItem as DB
        elif kwargs['dbtype'] == 'mongo':
            from Amazing_SpiderMan.DBConsole.DBConsole.DBtype.MongoItem import MongoItem as DB
        elif kwargs['dbtype'] == 'redis':
            from Amazing_SpiderMan.DBConsole.DBConsole.DBtype.RedisItem import RedisItem as DB
        elif kwargs['dbtype'] == ('csv' or 'txt'):
            from Amazing_SpiderMan.DBConsole.DBConsole.DBtype.FileItem import FileItem as DB
        else:
            raise NotConfigured

        self.DBmanager = DB(kwargs)
        self.DBmanager.init_db()
        self.colkey = kwargs['col'].keys()

    def store_data(self, data):
        '''

        :param data: dict
        :return:
        '''

        if isinstance(data, dict) and self.colkey == data.keys():
            self.DBmanager.insert(data)
        else:
            for i in data:
                self.DBmanager.insert(i)



    def close(self):
        self.DBmanager.close()


if __name__ == '__main__':
    #sql test
    # data = {'ip':'192.168.0.2', 'port': 800, 'name': 'cb', 'area':'beijin'}
    # db = Database('mysql', 'localhost:3306', 'text', 'text', 'root', '10ily1314',data)
    # db.store_data(data)
    # db.store_data(data)
    #
    # data1 = {'ip': '192.168.0.3', 'port': 800, 'name': 'cb', 'area': 'beijin', 'country': 'china'}
    # db.store_data(data1)
    # db.store_data(data)

    # mongo test
    # data = {'ip':'192.168.0.2', 'port': 800, 'name': 'cb', 'area':'beijin'}
    # db = Database('mongo', 'localhost:27017', 'test', 'testdb', 'root', '10ily1314',data)
    # db.store_data(data)
    # db.store_data(data)
    #
    # data1 = {'ip': '192.168.0.3', 'port': 800, 'name': 'cb', 'area': 'beijin', 'country': 'china'}
    # db.store_data(data1)
    # db.store_data(data)
    #
    # db.close()

    # # csv test
    # data = {'ip':'192.168.0.2', 'port': 800, 'name': 'cb', 'area':'beijin'}
    # db = Database()
    # db.store_data(data)
    # db.store_data(data)

    # inlufx test
    data = {'ip':'192.168.0.2', 'port': 800, 'name': 'cb', 'area':'beijin'}
    db = Database()
    db.store_data([data for i in range(3)])


    db.close()