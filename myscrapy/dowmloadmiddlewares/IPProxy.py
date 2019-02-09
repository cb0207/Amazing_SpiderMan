"""
IPProxy downloadmiddlewares

See documentation in OneNote
"""

import requests
import json
import random
from scrapy.exceptions import NotConfigured

# DOWNLOADER_MIDDLEWARES = {
#     'Amazing_SpiderMan.myscrapy.dowmloadmiddlewares.IPProxy.IPProxyMiddleware': 125,
# }
# IPPROXY_ENABLED = True

class IPProxyMiddleware(object):
    """
    Active IPProxy Service first
    then add 'IPPROXY_ENABLED' in setting and 'myscrapy.dowmloadmiddlewares.IPProxy' in middleware

    """

    def __init__(self):
        res = requests.get('http://127.0.0.1:8000/?types=0&count=50&protocol=0')
        res = json.loads(res.text)
        self.httplist = [str(x[0]) + ':' + str(x[1]) for x in res]

        res = requests.get('http://127.0.0.1:8000/?types=0&count=50&protocol=1')
        res = json.loads(res.text)
        self.httpslist = [str(x[0]) + ':' + str(x[1]) for x in res]

        res = requests.get('http://127.0.0.1:8000/?types=0&count=50&protocol=2')
        res = json.loads(res.text)
        self.httplist.extend([str(x[0]) + ':' + str(x[1]) for x in res])
        self.httpslist.extend([str(x[0]) + ':' + str(x[1]) for x in res])

    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool('IPPROXY_ENABLED'):
            raise NotConfigured

        return cls()

    def process_request(self, request, spider):
        '''
        ip proxy handling,
        :param request:
        :param spider:
        :return:
        '''

        if request.url[0:5] == 'https':
            self.thisip = 'https://' + random.choice(self.httpslist)
        else:
            self.thisip = 'http://' + random.choice(self.httplist)
        print('当前使用ip是: ' + self.thisip)
        request.meta['proxy'] = self.thisip