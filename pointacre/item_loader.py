# -*- coding: utf-8 -*-
__author__ = 'zym'

from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Compose
import re
def encode_text(item):
    item=item.encode('gbk')
    return item

def name_filter(item):
    if not re.match('^[\w]+$',item,re.I):
        return None
    return item

class UserLoader(ItemLoader):
    username_in=MapCompose(encode_text)
    username_out=MapCompose(name_filter)