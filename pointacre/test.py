# -*- coding: utf-8 -*-
from lxml import etree
from scrapy.selector import Selector

__author__ = 'zym'
from scrapy.contrib.loader.processor import MapCompose
import re
import csv
users={}
if "123" not in users:
    users["123"]=True

print users