# -*- coding: utf-8 -*-

# coding:utf-8
import datetime
from sqlalchemy import Column, Integer, String, DateTime, Numeric, create_engine, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from ..exceptions import NotDictType, NotMatchTable

from ..BasicSql import BasicSql


BaseModel = declarative_base()


class SqlItem(BasicSql):

    # def __init__(self, type, addr, database, table, user, password, col):
    def __init__(self, kwargs):
        '''
        kwargs is initiate the setup, format as INIT_DEFAULT in settings
        :param kwargs:
        '''

        if 'sqlite' in kwargs['dbtype']:
            connect_args = {'check_same_thread': False}
            con_string = 'sqlite:///' + kwargs['addr']
            self.engine = create_engine(con_string, echo=False, connect_args=connect_args)
        else:
            con_string = 'mysql+pymysql://%s:%s@%s/%s?charset=utf8' % (kwargs['user'], kwargs['password'], kwargs['addr'], kwargs['database'])
            self.engine = create_engine(con_string, echo=False)
        DB_Session = sessionmaker(bind=self.engine)
        self.session = DB_Session()
        self.init_table(kwargs['table'], kwargs['col'])

    def detect_data(self, col):
        if isinstance(col, bool):
            return Column(Boolean, nullable=False)
        elif isinstance(col,float):
            return Column(Float, nullable=False)
        elif isinstance(col, int):
            return Column(Integer, nullable=False)
        elif isinstance(col, str):
            return Column(VARCHAR(100), nullable=False)
        elif isinstance(col, datetime.datetime):
            return Column(DateTime())

    def init_table(self, table, col):
        self.params = {k: self.detect_data(j) for k, j in col.items()}

        class datafram(BaseModel):
            __tablename__ = table
            id = Column(Integer, primary_key=True, autoincrement=True)

            __table_args__ = {'mysql_charset': 'utf8', 'keep_existing':True}

        for j,k in self.params.items():
            if not hasattr(datafram, j):
                setattr(datafram, j, k)

        self.dataobj = datafram

    # def init_col(self, col):
    #     self.params = {k: self.detect_data(j) for k, j in col.items()}
    #     for j,k in self.params.items():
    #         if not hasattr(self.dataobj, j):
    #             setattr(self.dataobj, j, k)

    def init_db(self):
        BaseModel.metadata.create_all(self.engine)

    def drop_db(self):
        BaseModel.metadata.drop_all(self.engine)

    def insert(self, value):
        if isinstance(value, dict):
            if value.keys() != self.params.keys():
                return NotMatchTable

            temdt = self.dataobj(**value)

            self.session.add(temdt)
            self.session.commit()

        else:
            raise NotDictType

    # def delete(self, conditions=None):
    #     if conditions:
    #         conditon_list = []
    #         for key in list(conditions.keys()):
    #             if self.params.get(key, None):
    #                 conditon_list.append(self.params.get(key) == conditions.get(key))
    #         conditions = conditon_list
    #         query = self.session.query(Proxy)
    #         for condition in conditions:
    #             query = query.filter(condition)
    #         deleteNum = query.delete()
    #         self.session.commit()
    #     else:
    #         deleteNum = 0
    #     return ('deleteNum', deleteNum)
    #
    #
    # def update(self, conditions=None, value=None):
    #     '''
    #     conditions的格式是个字典。类似self.params
    #     :param conditions:
    #     :param value:也是个字典：{'ip':192.168.0.1}
    #     :return:
    #     '''
    #     if conditions and value:
    #         conditon_list = []
    #         for key in list(conditions.keys()):
    #             if self.params.get(key, None):
    #                 conditon_list.append(self.params.get(key) == conditions.get(key))
    #         conditions = conditon_list
    #         query = self.session.query(Proxy)
    #         for condition in conditions:
    #             query = query.filter(condition)
    #         updatevalue = {}
    #         for key in list(value.keys()):
    #             if self.params.get(key, None):
    #                 updatevalue[self.params.get(key, None)] = value.get(key)
    #         updateNum = query.update(updatevalue)
    #         self.session.commit()
    #     else:
    #         updateNum = 0
    #     return {'updateNum': updateNum}
    #
    #
    # def select(self, count=None, conditions=None):
    #     '''
    #     conditions的格式是个字典。类似self.params
    #     :param count:
    #     :param conditions:
    #     :return:
    #     '''
    #     if conditions:
    #         conditon_list = []
    #         for key in list(conditions.keys()):
    #             if self.params.get(key, None):
    #                 conditon_list.append(self.params.get(key) == conditions.get(key))
    #         conditions = conditon_list
    #     else:
    #         conditions = []
    #
    #     query = self.session.query(Proxy.ip, Proxy.port, Proxy.score, Proxy.name)
    #     if len(conditions) > 0 and count:
    #         for condition in conditions:
    #             query = query.filter(condition)
    #         return query.order_by(Proxy.score.desc(), Proxy.speed).limit(count).all()
    #     elif count:
    #         return query.order_by(Proxy.score.desc(), Proxy.speed).limit(count).all()
    #     elif len(conditions) > 0:
    #         for condition in conditions:
    #             query = query.filter(condition)
    #         return query.order_by(Proxy.score.desc(), Proxy.speed).all()
    #     else:
    #         return query.order_by(Proxy.score.desc(), Proxy.speed).all()


    def close(self):
        self.session.close()


if __name__ == '__main__':
    sqlhelper = SqlHelper()
    sqlhelper.init_db()
    proxy = {'ip': '192.168.1.1', 'port': 80, 'type': 0, 'protocol': 0, 'country': '中国', 'area': '广州', 'speed': 11.123, 'types': '', 'name': 'xx'}
    sqlhelper.insert(proxy)
    sqlhelper.update({'ip': '192.168.1.1', 'port': 80}, {'score': 10})
    print(sqlhelper.select(1))

