import sys
import re
import time

import subprocess

urls = sys.argv[2]
# reg = re.compile(r"([\d]+)")
# data = re.search(reg, sys.argv[1]).group(1)
data = int(sys.argv[1])
user_id = sys.argv[3]
incre_time = data
while incre_time % data == 0:
    proc = subprocess.Popen('scrapy crawl updata -a urls=%s -a user_id=%s' % (urls, user_id), shell=True)
    if proc.poll() == 0:
        proc.kill()
    sys.stdout.flush()
    incre_time += 1
    time.sleep(1)
