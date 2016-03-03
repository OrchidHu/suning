# coding = utf8
from django import template
import time
register = template.Library()


@register.filter(name='formatTime')
def formatTime(t):
    if not t: return ""
    strT = time.strftime("%Y-%m-%d %H:%M", time.localtime(t))
    return strT
register.filter('formatTime', formatTime)

