# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class InstagramScraperItem(scrapy.Item):
    id = scrapy.Field()
    timestamp = scrapy.Field()
    user = scrapy.Field()
    likes = scrapy.Field()
    comments = scrapy.Field()
    text = scrapy.Field()
    photo_low = scrapy.Field()
    hashtags = scrapy.Field()
