# coding = utf8
from django import template
import time
register = template.Library()


@register.filter(name='formatTime')
def formatTime(t):
    if not t:
        return ""
    T = time.localtime(float(t))
    strT = "%s-%s-%s %s:%s" % (T.tm_year, T.tm_mon, T.tm_mday, T.tm_hour, T.tm_min)
    return strT
register.filter('formatTime', formatTime)

