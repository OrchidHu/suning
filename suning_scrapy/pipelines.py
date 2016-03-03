# coding:utf-8

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import MySQLdb


class SuningPipeline(object):

    def __init__(self, mysql_host, mysql_db, mysql_user, mysql_passwd):
        self.mysql_host = host = '127.0.0.1'
        self.mysql_db = 'suning'
        self.mysql_user = 'root'
        self.mysql_passwd = '123'

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            mysql_host=str(crawler.settings.get('MYSQL_HOST')),
            mysql_user=str(crawler.settings.get('MYSQL_USER')),
            mysql_passwd=str(crawler.settings.get('MYSQL_PASSWD')),
            mysql_db=str(crawler.settings.get('MYSQL_DB'))
            )

    def open_spider(self, spider):
        self.conn=MySQLdb.connect(
            host=self.mysql_host,
            user=self.mysql_user,
            passwd=self.mysql_passwd,
            db=self.mysql_db,
            charset='utf8'
        )
        #self.conn=MySQLdb.connect(host='127.0.0.1',user='root',passwd='826446178',db='mydatabase',port=3306,charset='utf8')
        self.cursor=self.conn.cursor()
        #self.cursor.execute('CREATE TABLE blog_shopping(ident char(20),title char(20), name char(100) ,comment char(10),link char(100),price char(10),crawl_time char(20))')

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()
    # def process_item(self,item,spider):
    #     title=item['title']
    #     name=item['name'][0]
    #     crawl_time=item['crawl_time']
    #     price=item['price']
    #     comment=item['comment'][0]
    #     link=item['link'][0]
    #     ident = item['ident']
    #     self.cursor.execute(
    #         'INSERT INTO blog_shopping(ident,title,name,price,crawl_time,comment,link)VALUES(%s,%s,%s,%s,%s,%s,%s)',(ident, title, name, price, crawl_time, comment, link)
    #     )
    #     self.conn.commit()
    #     #log.msg("Question added to MySQLdb database!",level=log.DEBUG,spider=spider)
    #     return item

    def process_item(self, item, spider):
        ident = item['ident']
        name = item['name']
        price = item['price']
        crawl_time = item['crawl_time']
        user_id = item['user_id']
        ch_price = item['ch_price']
        image_url = item['image_url']
        self.cursor.execute('INSERT INTO blog_shopping(ident,name,price,crawl_time,user_id,ch_price,image_url)VALUES(%s,%s,%s,%s,%s,%s,%s)', (ident, name, price, crawl_time, user_id, ch_price, image_url))
        self.conn.commit()
        return item

