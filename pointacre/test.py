# -*- coding: utf-8 -*-
from lxml import etree
from scrapy.selector import Selector

__author__ = 'zym'
from scrapy.contrib.loader.processor import MapCompose
import re
import csv
reader=csv.reader(file(r'D:\PythonWorkspace\PythonCrawler\pointacre\export.csv','rb'))
for line in reader:
    username=line[0].decode('gbk')
    print username