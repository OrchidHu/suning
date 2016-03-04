# coding:utf8
import MySQLdb
import time
import subprocess

while True:
    conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='123', db='suning', port=3306, charset='utf8')
    cursor = conn.cursor()
    spiders = cursor.execute('SELECT * from blog_spider')
    if spiders:
        spiders = cursor.fetchmany(spiders)
        for spider in spiders:
            now_time = time.time()
            if (int(now_time)-int(float(spider[4]))) % int(spider[2]) == 0:
                subprocess.Popen('scrapy crawl updata -a urls=%s -a user_id=%s' % (spider[1], spider[3]), shell=True)
    time.sleep(1)
