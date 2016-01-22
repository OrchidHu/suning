#coding:utf8
import scrapy,re,urllib,MySQLdb,time
from suning_scrapy.items import SuningItem
from scrapy.http import Request

class MySpider(scrapy.Spider):
    name = 'updata'
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
            ident=sel.xpath('div/div[@class="i-price limit clearfix"]/p/@datasku').extract()
            name=sel.xpath('div/div[@class="i-name limit clearfix"]/a/@title').extract()
            link=sel.xpath('div/div[@class="i-name limit clearfix"]/a/@href').extract()
            comment=sel.xpath('div/div[@class="i-stock limit clearfix"]/a/span/text()').extract()
            if len(ident)==1:
                item=SuningItem()
                ident=re.search(r'([\d]+)',ident[0]).group()
                item['ident']=ident
                item['title']=title
                item['name']=name
                item['link']=link
                item['comment']=comment
                tm=time.time()
                item['crawl_time']=tm
                item_url='http://ds.suning.cn/ds/prices/000000000'+ident+'-9265--1-SES.product.priceCenterCallBack.jsonp'
                yield scrapy.Request(url=item_url, meta={'item': item},callback=self.parse_price)
        
        #翻页处理
        next_url=response.xpath('//div/a[@class="next fl"]/@href').extract()
        if next_url:
            next_url='http://list.suning.com'+next_url[0]
            yield scrapy.Request(url=next_url, meta={'title':title},callback=self.parse)
    #解析价格
    def parse_price(self, response):
        conn=MySQLdb.connect(host='localhost',user='root',passwd='huwei',db='suning',port=3306,charset='utf8')
        cur=conn.cursor()
        item=response.meta['item']
        price=re.search(r'"price":"([\d]+.[\d]+)',response.body)
        #只抓当地有货的商品
        if price:
            old_price=cur.execute('select price from suning.blog_shopping where ident=%s'%item['ident'])
            if old_price:
                old_price=cur.fetchmany(old_price)
            price=price.group(1)
            item['price']=price
            if old_price:
                if price!=old_price[0][0]:
                    cur.execute("UPDATE suning.blog_shopping SET price=%s,crawl_time=%s WHERE ident=%s"%(price,item['crawl_time'],item['ident']))
                    conn.commit()
                    item['last_price']=old_price[0][0]
                    #每解析完一个商品后, 有价格变化就入库
                    yield item
            else:
                cur.execute('INSERT INTO blog_shopping(ident,title,name,price,crawl_time,comment,link)VALUES(%s,%s,%s,%s,%s,%s,%s)',(item['ident'],item['title'],item['name'][0],item['price'],item['crawl_time'],item['comment'][0],item['link'][0]))
                conn.commit()

                
            
                    
                        
            
            

