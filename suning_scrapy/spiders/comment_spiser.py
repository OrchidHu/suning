# coding:utf8

import re
import datetime
import sys
import scrapy
import MySQLdb
from suning_scrapy.items import SuningItem


class MySpider(scrapy.Spider):
    name = 'updata'
    allowed_domains = []
    start_urls = None
    # 解析出所有品牌

    def __init__(self, urls=None, user_id=None, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.start_urls = urls.split(',')
        self.user_id = user_id
        self.conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='123', db='suning', port=3306, charset='utf8')
        self.cursor = self.conn.cursor()
        self.var = 1

    # 解析每个品牌手机的具体信息

    def parse(self, response):
        ident = re.search(r'([\d]{9}).html', response.url).group(1)
        item = SuningItem()
        item['ident'] = ident
        item['user_id'] = self.user_id
        item['name'] = response.xpath('//div[@class="proinfo-title"]/h1/text()').extract()
        item['crawl_time'] = datetime.datetime.now()
        price_url = 'http://ds.suning.cn/ds/prices/000000000' + ident + '-9265--1-SES.product.priceCenterCallBack.jsonp'
        yield scrapy.Request(url=price_url, meta={'item': item}, callback=self.parse_price)
        is_exist = self.cursor.execute('select * from blog_comment where ident=%s' % ident)
        self.conn.commit()
        # 是否已存有该商品编号的评论

        # 商品是否有评论
        comment_url = "http://review.suning.com/ajax/review_lists/style-000000000%s--total-1-default-10-----reviewList.htm?callback=reviewList" % str(ident)
        yield scrapy.Request(url=comment_url, meta={'ident': ident}, callback=self.parse_comment)
        if self.var == 1:
            self.cursor.execute('CREATE TABLE IF NOT EXISTS tb%s(comment text)' % ident)
            self.cursor.execute('INSERT INTO blog_comment(ident)VALUES(%s)' % ident)

    def parse_price(self, response):
        item = response.meta['item']
        price = re.search(r'"price":"([\d]+.[\d]+)', response.body)
        if price:
            price = price.group(1)
            item['price'] = price
            yield item

    def exist_comment(self, response):
        not_message = re.search(r'"commodityReviews":\[]', response.body)
        if not_message:
            self.var = -1

    def parse_comment(self, response):
        #__import__("pdb").set_trace()
        ident = response.meta['ident']
        not_message = re.search(r'"commodityReviews":\[]', response.body)
        if not_message:
            self.var = -1
        comments = response.body.split("content")
        for comment in comments:
            word = re.match(r'":(.*)","publishTime":', comment)
            if word:
                word = re.search(r'"(.*)', word.group(1)).group(1)
                self.cursor.execute('INSERT INTO suning.tb%s(comment)VALUES("%s")' % (ident, word))
                self.conn.commit()
        if self.var > 0:
            self.var += 1
            comment_url = "http://review.suning.com/ajax/review_lists/style-000000000%s--total-%s-default-10-----reviewList.htm?callback=reviewList" % (str(ident), str(self.var))
            yield scrapy.Request(url=comment_url, meta={'ident': ident}, callback=self.parse_comment)
