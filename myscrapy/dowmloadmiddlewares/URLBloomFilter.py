# -*- coding: utf-8 -*-


from scrapy.dupefilters import RFPDupeFilter
from pybloom import ScalableBloomFilter
import hashlib
from w3lib.url import canonicalize_url

# DUPEFILTER_CLASS = 'Amazing_SpiderMan.myscrapy.downloadmiddlewares.URLBloomFilter.URLBloomFilter'

class URLBloomFilter(RFPDupeFilter):

    def __init__(self, path=None, debug=False):
        self.urls_sbf = ScalableBloomFilter(mode=ScalableBloomFilter.SMALL_SET_GROWTH)
        RFPDupeFilter.__init__(self, path)

    def request_seen(self, request):
        fp = hashlib.sha1()
        fp.update(canonicalize_url(request.url).encode('utf-8'))
        url_sha1 = fp.hexdigest()
        if url_sha1 in self.urls_sbf:
            return True
        else:
            self.urls_sbf.add(url_sha1)