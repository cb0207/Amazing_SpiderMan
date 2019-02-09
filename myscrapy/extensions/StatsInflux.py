# -*- coding: utf-8 -*-

import logging
from scrapy import signals
from scrapy.exceptions import NotConfigured
from influxdb import InfluxDBClient
import datetime

# add extensions into 'scrapy.setting.default_settings' if you want it to be used for every scrapy project
# EXTENSIONS = {
#     'Amazing_SpiderMan.myscrapy.extensions.StatsInflux.StatsInfluxdb': 300,
#
# }
# Configure extensions
# InfluxDB Setting
# INFLUX_ENABLED = True
# INFLUX_NAME = 'scrapy'

class StatsInfluxdb(object):

    def __init__(self, ProjectName, InfluxDBname, stats):
        self.stats = stats
        self.client = InfluxDBClient(database=InfluxDBname)
        self.spiderinfo = {
                "measurement": "spdStatus",
                "tags": {
                    "Project": ProjectName,
                    "Name": "null"
                },
                "fields": {
                    "a_port": 'null',
                    "b1_status": "null",
                    "b2_target": 0,
                    "b_complete": 0.0,
                    "c_startTime": "null",
                    "d_endTime": "null",
                    "e1_reason": "null",
                    "e_speed": 0.0,
                    "f_request": 0,
                    "g_reqdrop": 0,
                    "h_response": 0,
                    "i_resdown": 0,
                    "j_item scrapped": 0,
                    "k_item dropped": 0,
                    "l_Error": 0
                }
        }

        self.requestinfo = {
                "measurement": "requestStatus",
                "tags": {
                    "Project": ProjectName,
                    "Spdname": "null",
                    "Status": "null",
                },
                "fields": {
                    "num": 1,
                    "Requrl": "null",
                    "Refer": "null"
                }
            }


        self.responseinfo = {
                "measurement": "responseStatus",
                "tags": {
                    "Project": ProjectName,
                    "Spdname": "null",
                    "Resurl": "null",
                    "Status": "null",
                    "ProxyIP": "null",
                    "stsCode": "null"
                },
                "fields": {
                    "stsCode": "null"
                }
            }

        self.errorl = {
                "measurement": "errorL",
                "tags": {
                    "Project": ProjectName,
                    "Spdname": "null",
                    "ProxyIP": "null",
                    "stsCode": "null"
                },
                "fields": {
                    "Resurl": "null",
                    "Reason": "null"
                }
            }

    @classmethod
    def from_crawler(cls, crawler):
        # first check if the extension should be enabled and raise
        # NotConfigured otherwise
        if not crawler.settings.getbool('INFLUX_ENABLED'):
            raise NotConfigured

        # get the number of items from settings
        InfluxDB_NAME = crawler.settings.get('INFLUX_NAME', 'scrapy')
        Project_NAME = crawler.settings.get('BOT_NAME')

        # instantiate the extension object
        ext = cls(Project_NAME, InfluxDB_NAME, crawler.stats)

        # connect the extension object to signals
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(ext.spider_error, signal=signals.spider_error)
        crawler.signals.connect(ext.item_scraped, signal=signals.item_scraped)
        crawler.signals.connect(ext.item_dropped, signal=signals.item_dropped)
        crawler.signals.connect(ext.request_scheduled, signal=signals.request_scheduled)
        crawler.signals.connect(ext.request_dropped, signal=signals.request_dropped)
        crawler.signals.connect(ext.response_received, signal=signals.response_received)
        crawler.signals.connect(ext.response_downloaded, signal=signals.response_downloaded)

        # return the extension object
        return ext

    def _getspidIP(self, spidname):
        '''

        :return: get the ip by spider name
        '''
        q = self.client.query("select LAST(*) from spiderIP where spdname='" + spidname + "'")
        return str(dict(q.raw['series'][0])['values'][0][1])

    def _getlatesStats(self, key=None):
        '''

        :param key: key in log dict
        :return: get log in scrapy log. In case no key, will return all
        '''
        if key:
            return self.stats.get_stats().get(key)
        return self.stats.get_stats()

    def _calspeed(self):
        '''

        :return: item scraped speed, unit in item scrapped/mins
        '''
        td = (datetime.datetime.now() - self.stats.get_stats().get("start_time")).seconds/60
        if self._getlatesStats("item_scraped_count"):
            return float(self._getlatesStats("item_scraped_count")/td)
        return 0.0

    def _calpec(self, target):
        '''
        item scraped / target
        :param target: total target
        :return: calculate complete percentage
        '''
        if self._getlatesStats("item_scraped_count"):
            return float(self._getlatesStats("item_scraped_count")/target)
        return 0.0

    def _updateSts(self):
        pass

    # def _getStsCode(self):
    #     '''
    #     get response (sts:num) into response status
    #     :return:
    #     '''
    #     for x,y in self.stats.items():
    #         if "downloader/response_status_count/" in x:
    #             self.responseinfo['fields'][x[-3:]] = y


    def spider_opened(self, spider):
        self.spiderinfo['tags']['Name'] = spider.name
        self.spiderinfo['fields']['b1_status'] = 'open'
        self.spiderinfo['fields']['e1_reason'] = 'start'
        self.spiderinfo['fields']['c_startTime'] = str(self._getlatesStats("start_time"))
        self.client.write_points([self.spiderinfo])

    def spider_closed(self, spider, reason):
        self.spiderinfo['tags']['Name'] = spider.name
        self.spiderinfo['fields']['b1_status'] = 'closed'
        self.spiderinfo['fields']['b2_target'] = spider.target
        self.spiderinfo['fields']['b_complete'] = self._calpec(spider.target)
        self.spiderinfo['fields']['e1_reason'] = reason
        self.spiderinfo['fields']['e_speed'] = self._calspeed()
        self.spiderinfo['fields']['d_endTime'] = str(self._getlatesStats("finish_time"))
        self.client.write_points([self.spiderinfo])

        self.client.close()

    def spider_error(self, failure, response, spider):
        self.spiderinfo['fields']['l_Error'] += 1
        self.client.write_points([self.spiderinfo])

        self.errorl["tags"]["Spdname"] = spider.name
        self.errorl["tags"]["ProxyIP"] = response.meta.get("proxy")
        self.errorl["tags"]["stsCode"] = str(response.status)
        self.errorl["fields"]["Resurl"] = response.request.url
        self.errorl["fields"]["Reason"] = str(failure.value)

        self.client.write_points([self.errorl])

    def item_scraped(self, item, spider):
        self.spiderinfo['fields']['j_item scrapped'] = self._getlatesStats("item_scraped_count")
        self.spiderinfo['fields']['e_speed'] = self._calspeed()
        self.spiderinfo['fields']['b2_target'] = spider.target
        self.spiderinfo['fields']['b_complete'] = self._calpec(spider.target)
        self.client.write_points([self.spiderinfo])

    def item_dropped(self, item, response, exception, spider):
        self.spiderinfo['fields']['k_item dropped'] = self._getlatesStats("item_dropped_count")
        self.client.write_points([self.spiderinfo])

    def request_scheduled(self, request, spider):
        if self.spiderinfo['fields']['a_port'] == 'null':
            self.spiderinfo['fields']['a_port'] = self._getspidIP(spider.name)
        self.spiderinfo['fields']['e_speed'] = self._calspeed()
        self.spiderinfo['fields']['f_request'] = self._getlatesStats("downloader/request_count")
        self.client.write_points([self.spiderinfo])

        self.requestinfo['tags']['Spdname'] = spider.name
        self.requestinfo['fields']['Requrl'] = request.url
        self.requestinfo['fields']['Refer'] = request.headers.get('Referer')
        self.requestinfo['tags']['Status'] = 'scheduled'
        self.client.write_points([self.requestinfo])

    def request_dropped(self, request, spider):
        self.spiderinfo['fields']['g_reqdrop'] += 1
        self.requestinfo['tags']['Spdname'] = spider.name
        self.requestinfo['fields']['Requrl'] = request.url
        self.requestinfo['fields']['Refer'] = request.headers.get('Referer')
        self.requestinfo['tags']['Status'] = 'dropped'
        self.client.write_points([self.requestinfo])

    def response_received(self, response, request, spider):
        self.spiderinfo['fields']['h_response'] = self._getlatesStats("response_received_count")
        self.client.write_points([self.spiderinfo])

        self.responseinfo['tags']['Spdname'] = spider.name
        self.responseinfo['tags']['Requrl'] = request.url
        self.responseinfo['tags']['Status'] = 'received'
        self.responseinfo['tags']['ProxyIP'] = request.meta.get("proxy")
        self.responseinfo['tags']['stsCode'] = str(response.status)
        self.responseinfo['fields']['stsCode'] = str(response.status)
        self.responseinfo['fields'][str(response.status)] = 1
        self.client.write_points([self.responseinfo])

        self.responseinfo['fields'].clear()

    def response_downloaded(self, response, request, spider):
        self.spiderinfo['fields']['e_speed'] = self._calspeed()
        self.spiderinfo['fields']['i_resdown'] = self._getlatesStats("downloader/response_count")
        self.client.write_points([self.spiderinfo])

        self.responseinfo['tags']['Spdname'] = spider.name
        self.responseinfo['tags']['Resurl'] = request.url
        self.responseinfo['tags']['Status'] = 'downloaded'
        self.responseinfo['tags']['ProxyIP'] = request.meta.get("proxy")
        self.responseinfo['tags']['stsCode'] = str(response.status)
        self.responseinfo['fields']['stsCode'] = str(response.status)
        self.responseinfo['fields'][str(response.status)] = 1
        self.client.write_points([self.responseinfo])

        self.responseinfo['fields'].clear()
