# -*- coding: utf-8 -*-



#
# class Test_URL_Fail(Exception):
#     def __str__(self):
#         str = "访问%s失败，请检查网络连接" % config.TEST_IP
#         return str
#
#
# class Con_DB_Fail(Exception):
#     def __str__(self):
#         str = "使用DB_CONNECT_STRING:%s--连接数据库失败" % config.DB_CONNECT_STRING
#         return str


class NotConfigured(Exception):
    def __str__(self):
        str = "New db/file type, Pls build type first"
        return str

class NotDictType(Exception):
    def __str__(self):
        str = "Data is not dict, must be dict"
        return str

class NotMatchTable(Exception):
    def __str__(self):
        str = "Your data is not match with database existing table, pls check first"
        return str
