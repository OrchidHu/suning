# coding:utf8
import MySQLdb.cursors
import re
import datetime
import sys
import scrapy
import MySQLdb


class MySpider(scrapy.Spider):
    name = 'comment'
    allowed_domains = []
    urls = []
    def start_requests(self):
	self.conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='123', db='suning', port=3306, charset='utf8')
    	self.cursor = self.conn.cursor()
    	spiders = self.cursor.execute('SELECT ident from blog_comment')
    	self.var = 1
    	if spiders:
            spiders = self.cursor.fetchmany(spiders)
            for ident in spiders:
                ident = ident[0]
                self.cursor.execute('CREATE TABLE IF NOT EXISTS tb%s(comment text, pb_time Char(20))' % ident)
                yield scrapy.Request("http://review.suning.com/ajax/review_lists/style-000000000%s--total-1-default-10-----reviewList.htm?callback=reviewList" % ident, meta={'ident':ident},callback=self.parse)
   # conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='123', db='suning', port=3306, charset='utf8')
    #cursor = conn.cursor()
    #spiders = cursor.execute('SELECT ident from blog_comment')
    #var = 1
    #if spiders:
     #   spiders = cursor.fetchmany(spiders)
      #  for ident in spiders:
       #     urls.append("http://review.suning.com/ajax/review_lists/style-000000000%s--total-1-default-10-----reviewList.htm?callback=reviewList" % str(ident[0]))
	#    ident = ident[0]
         #   cursor.execute('CREATE TABLE IF NOT EXISTS tb%s(comment text)' % ident)
    #start_urls = [ 
#		"http://review.suning.com/ajax/review_lists/style-000000000102569240--total-1-default-10-----reviewList.htm?callback=reviewList",
#		"http://review.suning.com/ajax/review_lists/style-000000000103629871--total-1-default-10-----reviewList.htm?callback=reviewList"
#	]


    def parse(self, response):
	ident = response.meta['ident']
        not_message = re.search(r'"commodityReviews":\[]', response.body)
        if not_message:
            self.var = -1
        comments = response.body.split("content")
        for comment in comments:
            word = re.match(r'":(.*)","publishTime":', comment)
	    publish_time = re.search(r'"(.*)","deviceTy', comment)
            if word:
                word = re.search(r'"(.*)', word.group(1)).group(1)
		publish_time = re.search(r'"publishTime":"(.*)', publish_time.group(1)).group(1)
		self.cursor.execute('INSERT INTO suning.tb%s(comment, pb_time)VALUES("%s","%s")' % (ident, word.decode("utf-8"), publish_time.decode("utf-8")))
                self.conn.commit()
        if self.var > 0 and self.var < 10:
            self.var += 1
            comment_url = "http://review.suning.com/ajax/review_lists/style-000000000%s--total-%s-default-10-----reviewList.htm?callback=reviewList" % (str(ident), str(self.var))
            yield scrapy.Request(url=comment_url, meta={'ident': ident}, callback=self.parse)

