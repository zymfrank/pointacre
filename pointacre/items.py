# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from scrapy.contrib.loader.processor import MapCompose

from scrapy.item import Item, Field
import re



class UserItem(Item):
    # define the fields for your item here like:
    # name = Field()
    username=Field()
    passwrod=Field()

class LoginItem(Item):
    message=Field()
