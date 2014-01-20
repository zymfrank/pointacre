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
        self.user_file=open('users.csv','wb')
        self.user_exporter=CsvItemExporter(self.user_file)
        self.psw_file=open('passwd.csv','wb')
        self.psw_exporter=CsvItemExporter(self.psw_file)

    def process_item(self, item, spider):
        if spider.name=="1point3acres.user":
            if item.has_key('uid') and item['uid']:
                uid=item['uid'][0]
                if uid not in PointacrePipeline.users:
                    PointacrePipeline.users[uid]=True
                    self.user_exporter.export_item(item)
                else:
                    raise DropItem()
        elif spider.name=="1point3acres.login":
            self.psw_exporter.export_item(item)
        else:
            return item