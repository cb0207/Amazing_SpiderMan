# Original Purpose of Building This Support
By leaning along web crawler(spider), most of cases need to setup many things from 0.
My point of view for the build up crawler step is analysis web, scrap data, data storage.
Additional function to crawler also need proxy pool, user agent pool, log...etc.
Furthermore, as a crawler maintainer also required to monitor crawler, system, database, web status to perform a good quality.
Therefore, i would like to centralize this kind of issue in one package to make it more easier to build up a spider.

On the other hand, as you may know famous project in crawler is Scrapy. It's a good project. 
So i would also build some plugin for scrapy in this package.

# User Guide

## DBConsole: Data Storage
```
1. initiate Database() or Database(config) object, if config not provided, then will use default in setting
2. config format follow INIT_DEFAULT in setting
3. To insert data, use method: Database().store_data(data)
4. data format in dict , dict in list
5. current support for mysql, sqlite3, inlufx, mongo, csv
```

## myscrapy: function for scrapy

#####downloadmiddlewares

```
1. IPProxy
    # DOWNLOADER_MIDDLEWARES = {
    #     'Amazing_SpiderMan.myscrapy.dowmloadmiddlewares.IPProxy.IPProxyMiddleware': 125,
    # }
    # IPPROXY_ENABLED = True

2. URLBloomFilter
    # DUPEFILTER_CLASS = 'Amazing_SpiderMan.myscrapy.downloadmiddlewares.URLBloomFilter.URLBloomFilter'


3. UserAgent
    # DOWNLOADER_MIDDLEWARES = {
    #     'Amazing_SpiderMan.myscrapy.dowmloadmiddlewares.UserAgent.UserAgent': 1,
    # }



```


##### extensions
add the extensions as below if you want it to be used for every scrapy projects. 
As the way of import base setting is different from project extension. 
Project extension expected in project. if you just put below extension in project, it will pop up error.
eg: 'scrapy.setting.default_settings ==> 
EXTENSIONS_BASE = {'Amazing_SpiderMan.myscrapy.extensions.StatsInflux.StatsInfluxdb': 300,}'
   
ps: another reason is i don't want to change the original import method. To avoid error occure.  

```
1. StatsInflux
   
```


##### pipelines

```
1. mysql pipeline
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
    
2. mongo pipeline

```


##### scrapy_redis : Redis BloomFilter

```
1. Scrapy_redis + BloomFilter
    In this function, will put the queue and dupfilter in redis, controlled by schedule.
    
    # 使用scrapy_redis的调度器
    # SCHEDULER = "Amazing_SpiderMan.myscrapy.scrapy_redis.scheduler.Scheduler"
    # SCHEDULER_QUEUE_CLASS = 'Amazing_SpiderMan.myscrapy.scrapy_redis.queue.SpiderPriorityQueue'
    
    # 在redis中保持scrapy-redis用到的各个队列，从而允许暂停和暂停后恢复
    # SCHEDULER_PERSIST = True
    
    
    # REDIS_HOST = '127.0.0.1'
    # REDIS_PORT = 6379
    # # 去重队列的信息
    # FILTER_URL = None
    # FILTER_HOST = 'localhost'
    # FILTER_PORT = 6379
    # FILTER_DB = 0

```


## Monitor


## Plugin


## Template





## Update history

-----------------------------2018-10-31----------------------------
<br/>
Add new pipeline in myscrapy
<br/>
New update:
```
1. CSVPipeline
2. JSONPipeline

```
-----------------------------2018-10-29----------------------------
<br/>
Update Sql insert object attribute 
<br/>
New update:
```
1. add an attribute '__table_args__ = 'to class datafram(BaseModel).
   data encoding incorrect, cause tableau couldn't import data.

```

-----------------------------2018-10-28----------------------------
<br/>
Add myscrapy project
<br/>
New update:

```
1. centralize all dowmloadmiddlewares/extension/pipeline/function into here if it can be used for all scrapy project
2. to use it, you can refer to remark which on top of the object file. 
   ps: if it contains more than one file, remark will be __init__ file.
   
   detail remark will be built later on
```


-----------------------------2018-10-27----------------------------
<br/>
Build up probject 'Amazing Spider Man'
<br/>
New update:
```
1. add influx database platform to DBConsole
2. Updategrade data insert format to multiple, eg: list, dict
   sample:
   "[{'ip':'192.168.0.2', 'port': 800, 'name': 'cb', 'area':'beijin'}, 
   {'ip':'192.168.0.2', 'port': 800, 'name': 'cb', 'area':'beijin'}]"
   
   "{'a': {'ip':'192.168.0.2', 'port': 800, 'name': 'cb', 'area':'beijin'}, 
   'b': {'ip':'192.168.0.2', 'port': 800, 'name': 'cb', 'area':'beijin'}}"
   
    original form is only dict allowed. 
3. influx can initiate database column in INIT_DEFAULT['col'] with specify 'tags'/'fields'. 
   If not, then will be identified by objself. Default number to fields, rest are 'tags'
```
