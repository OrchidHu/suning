# coding:utf8
import MySQLdb
import MySQLdb.cursors
import time
import subprocess

while True:
    conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='123', db='suning', port=3306, charset='utf8', cursorclass=MySQLdb.cursors.DictCursor)
    cursor = conn.cursor()
    spiders = cursor.execute('SELECT cycle,url,start_time,user_id from blog_spider')
    if spiders:
        spiders = cursor.fetchmany(spiders)
        for spider in spiders:
            now_time = time.time()
            if (int(now_time)-int(float(spider["start_time"]))) % int(spider["cycle"]) == 0:
                subprocess.Popen('scrapy crawl updata -a urls=%s -a user_id=%s' % (spider["url"], spider["user_id"]), shell=True)
    time.sleep(1)
