# -*- coding: utf-8 -*-
__author__ = 'zym'
from scrapy.contrib.loader.processor import MapCompose
import re
def name_filter(input):
    if re.match('^[\w]+$',input,re.I):
        return input
    else:
        return None
proc=MapCompose(name_filter)
print proc([u'test\u817f\u6bdb\u5f2f\u5f2f',u'Shirleyyuan'])
