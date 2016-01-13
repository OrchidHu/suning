#-*- coding:utf8-*-
import MySQLdb,time
from scrapy import cmdline
##conn=MySQLdb.connect(host='localhost',user='root',passwd='826446178',db='suning_shopping2',port=3306,charset='utf8')
##cur=conn.cursor()
#cur.execute('drop table if exists blog_shopping')
cmdline.execute("scrapy crawl updata".split())
