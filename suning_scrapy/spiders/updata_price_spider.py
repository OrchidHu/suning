# coding:utf8

import re, redis
import time
import datetime
import scrapy
import MySQLdb
from suning_scrapy.items import SuningItem
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib


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
        item['image_url'] = "http://image5.suning.cn/b2c/catentries/000000000%s_1_100x100.jpg" % ident
        price_url = 'http://ds.suning.cn/ds/prices/000000000' + ident + '-9265--1-SES.product.priceCenterCallBack.jsonp'
        yield scrapy.Request(url=price_url, meta={'item': item}, callback=self.parse_price)
        is_exist = self.cursor.execute('SELECT * FROM blog_comment WHERE ident=%s' % ident)
        if is_exist == 0:
	    tb_name = "tb"+str(ident)
	    self.cursor.execute('INSERT INTO blog_comment(ident, tb_name)VALUES(%s,"%s")' % (ident, tb_name))
            self.conn.commit()

    def parse_price(self, response):
        item = response.meta['item']
        price = re.search(r'"price":"([\d]+.[\d]+)', response.body)
        if price:
            price = price.group(1)
            datas = self.cursor.execute(
                'SELECT id,price,crawl_time FROM blog_shopping WHERE ident=%s AND user_id=%s' % (
                item['ident'], item['user_id'])
            )
            item['price'] = price
            if datas:
                data = self.cursor.fetchmany(datas)[-2:]
                data_id = data[1][0]
                old_price = data[1][1]
                if price != old_price:
		    redisClient = redis.StrictRedis(host='127.0.0.1',port=6379,db=0)
                    if price > old_price:
			redisClient.set(item['ident'], 1)
                        item['ch_price'] = 'up'
                    else:
			redisClient.set(item['ident'], -1)
                        item['ch_price'] = 'down'
		    redisClient.expire(item['ident'], 60*2)
                    yield item
                    email = self.cursor.execute(
                        'SELECT email FROM blog_spider WHERE user_id=%s' % item['user_id']
                    )
                    if email:
                        email = self.cursor.fetchmany(email)[-1:][0][0]
                        self.send_email(email)
                else:
                    crawl_time = data[0][2]
                    if time.time()-float(crawl_time) > 24*3600:
                        stable = "stable"
                        self.cursor.execute(
                            "UPDATE suning.blog_shopping SET ch_price='%s' WHERE ID=%s" % (stable, data_id)
                        )
                self.cursor.execute(
                    "UPDATE suning.blog_shopping SET crawl_time=%s WHERE ID=%s" % (time.time(), data_id))
                self.conn.commit()
            else:
                item['ch_price'] = 'stable'
                yield item
                yield item

    def send_email(self, email):
        from_addr = '826446178@qq.com'
        password = "nxnansojlwqxbbba"
        to_addr = "%s" % email
        url = 'http://121.42.174.207/blog/'
        msg = MIMEText('您好!\n       您特定的商品有价格变动,请点击下方的链接查看:\n       %s' % url, 'plain', 'utf-8')
        msg['From'] = self._format_addr(u'小虫子 <%s>' % from_addr)
        msg['To'] = self._format_addr(u'管理员 <%s>' % to_addr)
        msg['Subject'] = Header(u'商品价格变动通知', 'utf-8').encode()

        smtp_server = 'smtp.qq.com'
        smtp_port = 587
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        # server.set_debuglevel(1)
        server.login(from_addr, password)
        server.sendmail(from_addr, [to_addr], msg.as_string())
        server.quit()

    def _format_addr(self, s):
        name, addr = parseaddr(s)
        return formataddr(( \
                              Header(name, 'utf-8').encode(), \
                              addr.encode('utf-8') if isinstance(addr, unicode) else addr))
