# -*- coding: utf-8 -*-
__author__ = 'zym'
from pointacre.items import LoginItem
from pointacre.items import UserItem
from pointacre.item_loader import UserLoader
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request, FormRequest


class UsernameSpider(Spider):
    name="1point3acres.username"
    start_urls=["http://www.1point3acres.com/bbs/"]

    def parse(self, response):
        request=[]
        selector=Selector(response)
        xpath='//*[@id="category_38"]/table/tr[1]/td[2]/dl/dt/a/@href'
        new_urls=selector.xpath(xpath).extract()
        for url in new_urls:
            r=Request(url,callback=self.parse_forum)
            request.append(r)
        return request

    def parse_forum(self,response):
        items=[]
        selector=Selector(response)
        xpath='//table[@summary="forum_27"]/tbody//tr//td[@class="by"]/cite/a/text()[1]'
        names=selector.xpath(xpath).extract()
        for name in names:
            loader=UserLoader(UserItem(),response=response)
            loader.add_value('username',name)
            item=loader.load_item()
            items.append(item)
        return items

class LoginSpider(Spider):
    name="1point3acres.login"
    start_urls=["http://1point3acres.com/bbs"]

    def parse(self, response):
        request_url="http://1point3acres.com/bbs/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1"
        return [FormRequest(url=request_url,
                    formdata={'username': 'test', 'password': 'test'},
                    callback=self.after_login)]

    def after_login(self,response):
        # check login succeed before going on
        print "Return is:%s" % response.body
        item=LoginItem()
        selector=Selector(response)
        selector.xpath('/').extract()
        pass