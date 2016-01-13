#coding:utf8
import scrapy,re,urllib,time
from suning_scrapy.items import SuningItem
from scrapy.http import Request

class MySpider(scrapy.Spider):
    name = 'dmoz'
    allowed_domains = []
    def start_requests(self):
        yield scrapy.Request('http://list.suning.com/0-20006-0-0-0-9265.html#sourceUrl4Sa=http://www.suning.com/?utm_source=sogou&utm_medium=brand&utm_campaign=title', self.parse_url)

    #解析出所有品牌
    def parse_url(self,response):
        for sel in response.xpath('//div[@class="attr-list"]/ul//li'):
            title=sel.xpath('@title').extract()[0]
            url='http://list.suning.com'+sel.xpath('a/@href').extract()[0]

            #每获得一个品牌的路径,调用一次parse函数,解析出该名牌的所有手机信息
            yield scrapy.Request(url,meta={'title':title},callback=self.parse)

    #解析每个品牌手机的具体信息
    def parse(self, response):
        title=response.meta['title']
        for sel in response.xpath('//ul/li'):
            item=SuningItem()
            name=sel.xpath('div/div[@class="i-name limit clearfix"]/a/@title').extract()
            link=sel.xpath('div/div[@class="i-name limit clearfix"]/a/@href').extract()
            ident=sel.xpath('div/div[@class="i-price limit clearfix"]/p/@datasku').extract()
            comment=sel.xpath('div/div[@class="i-stock limit clearfix"]/a/span/text()').extract()
            if len(name)==1:
                item['crawl_time']=time.time()
                item['title']=title
                item['name']=name
                item['link']=link 
                item['comment']=comment
                ident=re.search(r'([\d]+)',ident[0]).group()
                item['ident']=ident
                item_url='http://ds.suning.cn/ds/prices/000000000'+ident+'-9265--1-SES.product.priceCenterCallBack.jsonp'
                #获得价格的js文件路径,调用解析价格函数(parse_price),把item值传输过去
                yield scrapy.Request(url=item_url, meta={'item': item},callback=self.parse_price)
        
        #翻页处理
        next_url=response.xpath('//div/a[@class="next fl"]/@href').extract()
        if next_url:
            next_url='http://list.suning.com'+next_url[0]
            yield scrapy.Request(url=next_url, meta={'title':title},callback=self.parse)
    #解析价格
    def parse_price(self, response):
        item=response.meta['item']
        price=re.search(r'"price":"([\d]+.[\d]+)',response.body)
        #只抓当地有货的商品
        if price:
            item['price']=price.group(1)
            #每解析完一个商品后, 返回item 到管道进行入库处理
            yield item


