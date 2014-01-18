# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
from scrapy.contrib.exporter import CsvItemExporter
from scrapy.exceptions import DropItem


class PointacrePipeline(object):
    def __init__(self):
        pass
        # self.file=open('export.csv','wb')
        # self.exporter=CsvItemExporter(self.file)
    def process_item(self, item, spider):
        if item['username']:
            # self.exporter.export_item(item)
            return item
        else:
            raise DropItem("Chinese name %s dropped." % item)
