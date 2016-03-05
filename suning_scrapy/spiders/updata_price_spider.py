# coding:utf8

import re
import time
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

    def parse(self, response):
        ident = re.search(r'([\d]{9}).html', response.url).group(1)
        item = SuningItem()
        item['ident'] = ident
        item['url'] = response.url
        item['user_id'] = self.user_id
        item['name'] = response.xpath('//div[@class="proinfo-title"]/h1/text()').extract()[0]
        item['crawl_time'] = time.time()
        item['image_url'] = "http://image5.suning.cn/b2c/catentries/000000000%s_1_120x120.jpg" % ident
        price_url = 'http://ds.suning.cn/ds/prices/000000000' + ident + '-9265--1-SES.product.priceCenterCallBack.jsonp'
        yield scrapy.Request(url=price_url, meta={'item': item}, callback=self.parse_price)
        is_exist = self.cursor.execute('SELECT * FROM blog_comment WHERE ident=%s' % ident)
        if is_exist == 0:
            self.cursor.execute('INSERT INTO blog_comment(ident)VALUES(%s)' % ident)
            self.conn.commit()

    def parse_price(self, response):
        item = response.meta['item']
        price = re.search(r'"price":"([\d]+.[\d]+)', response.body)
        if price:
            price = price.group(1)
            datas = self.cursor.execute(
                'SELECT id,price FROM blog_shopping WHERE ident=%s AND user_id=%s' % (item['ident'], item['user_id']))
            item['price'] = price
            if datas:
                datas = self.cursor.fetchmany(datas)[-1:]
                data_id = datas[0][0]
                old_price = datas[0][1]
                if price != old_price:
                    if price > old_price.pop():
                        item['ch_price'] = 'up'
                    else:
                        item['ch_price'] = 'down'
                    yield item
                self.cursor.execute(
                    "UPDATE suning.blog_shopping SET crawl_time=%s WHERE ID=%s" % (time.time(), data_id))
                self.conn.commit()
            else:
                item['ch_price'] = 'stable'
                yield item
                yield item
