# -*- coding: utf-8 -*-

import os

# default init db config
INIT_DEFAULT = {
    'dbtype': 'influx',
    'addr': 'localhost:8086',
    'database': 'testDB',
    'table': 'text',
    'user': 'root',
    'password': 'root',
    'col': {'ip':'192.168.0.2', 'port': 800, 'name': 'cb', 'area':'beijin'}
}


# default data type is csv, can be txt, mysql, sqlite3, mongo, redis, influx
STORETYPE = 'csv'

# table column
COL = []

# setup for file
FILE = True
FILEADDR = os.path.dirname(__file__) + '/Storage/'
FILENAME = 'data'


# setup for database
DBUSE = False
DBPORT = ''
DBUSER = ''
DBPW = ''






