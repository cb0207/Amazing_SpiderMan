# -*- coding: utf-8 -*-

from influxdb import InfluxDBClient


from BasicSql import BasicSql


class InfluxItem(BasicSql):

    def __init__(self, kwargs):
        ip = kwargs['addr'].split(':')[0]
        port = kwargs['addr'].split(':')[1]
        self.client = InfluxDBClient(host=ip, port=port, database=kwargs['database'], username=kwargs['user'], password=kwargs['password'])
        self.jsonbody = {
            "measurement": kwargs['table'],
            "tags": {},
            "fields": {}
        }
        self.coltype = self.detect_data(kwargs['col'])


    def detect_data(self, col):
        '''

        :param col:
        :return: 1, cols = {'tags': xx, 'field':xx}; 2, without identify 'tags' and 'fields'
        '''
        a = 0
        if col.get("tags"):
            a += 1
        if col.get("fields"):
            a += 1

        if a == 2:
            self.jsonbody['tags'] = col['tags']
            self.jsonbody['fields'] = col['fields']
            return 1
        elif a == 0:
            # digit default fields, rest are tags if not defined
            for j, k in col.items():
                if isinstance(k, int) or isinstance(k, float):
                    self.jsonbody['fields'][j] = k
                else:
                    self.jsonbody['tags'][j] = k
            return 2
        else:
            print('Missing one of tags/fields')

    def init_db(self):
        pass

    def insert(self, value):
        if self.coltype == 1:
            self.jsonbody['tags'] = value['tags']
            self.jsonbody['fields'] = value['fields']
        elif self.coltype == 2:
            for j in self.jsonbody['tags'].keys():
                self.jsonbody['tags'][j] = value.get(j)
            for j in self.jsonbody['fields'].keys():
                self.jsonbody['fields'][j] = value.get(j)

        self.client.write_points([self.jsonbody])

    def close(self):
        self.client.close()