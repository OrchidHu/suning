# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SuningItem(scrapy.Item):
    # define the fields for your item here like:
    ident = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    crawl_time = scrapy.Field()
    user_id = scrapy.Field()
    ch_price = scrapy.Field()
    image_url = scrapy.Field()
    url = scrapy.Field()
