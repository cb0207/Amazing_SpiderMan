# -*- coding: utf-8 -*-

from Amazing_SpiderMan.DBConsole.DBConsole.BasicSql import BasicSql

import csv

from Amazing_SpiderMan.DBConsole.DBConsole.exceptions import NotMatchTable

class FileItem(BasicSql):

    def __init__(self, kwargs):
    # def __init__(self, type, addr, database=None, table=None, user=None, password=None, col):
        self.headers = list(kwargs['col'].keys())
        self.addr = kwargs['addr']

    def init_db(self):
        self.file = open(self.addr, 'a', encoding='utf-8')
        self.f_csv = csv.DictWriter(self.file, self.headers)
        self.f_csv.writeheader()

    def insert(self, value):
        if list(value.keys()) != self.headers
            return NotMatchTable
        self.f_csv.writerow(value)
        self.file.flush()

    def close(self):
        self.file.close()
