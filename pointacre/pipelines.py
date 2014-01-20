# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
from scrapy.contrib.exporter import CsvItemExporter
from scrapy.exceptions import DropItem


class PointacrePipeline(object):
    users={}
    def __init__(self):
        self.file=open('export.csv','wb')
        self.exporter=CsvItemExporter(self.file)

    def process_item(self, item, spider):
        if spider.name=="1point3acres.user":
            if item.has_key('uid') and item['uid']:
                uid=item['uid'][0]
                if uid not in PointacrePipeline.users:
                    PointacrePipeline.users[uid]=True
                    self.exporter.export_item(item)
                else:
                    raise DropItem()
        else:
            return item