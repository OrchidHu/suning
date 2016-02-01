import sys
import re
import time

import subprocess

print sys.argv[1]
reg = re.compile(r"([\d]+)")
data = re.search(reg, sys.argv[1]).group(1)
data = int(data)
incre_time = data
while incre_time % data == 0:
    proc = subprocess.Popen('python /home/huwei/suning/updataShoppingPrice.py', shell=True)
    if proc.poll() == 0:
        proc.kill()
    sys.stdout.flush()
    incre_time += 1
    time.sleep(1)
