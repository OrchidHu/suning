# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SuningItem(scrapy.Item):
    # define the fields for your item here like:
    title=scrapy.Field()
    name = scrapy.Field()
    comment=scrapy.Field()
    link=scrapy.Field()
    price=scrapy.Field()
    last_price=scrapy.Field()
    ident=scrapy.Field()
    crawl_time=scrapy.Field()
