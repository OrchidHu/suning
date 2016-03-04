# coding = utf8
from django import template
import time
register = template.Library()


@register.filter(name='formatTime')
def formatTime(t):
    if not t:
        return ""
    x = time.localtime(float(t))
    strT = time.strftime('%Y-%m-%d %H:%M:%S', x)
    return strT

