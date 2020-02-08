# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

# default
# class LdtcrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass

class Astro108Item(scrapy.Item):
    # 星座代碼
    astro_code = scrapy.Field()
    # 星座名稱
    title_zh = scrapy.Field()
    # 爬取日期
    date = scrapy.Field()
    # 爬取來源
    source = scrapy.Field()
    # 運勢指數
    score_all = scrapy.Field()
    score_money = scrapy.Field()
    score_work = scrapy.Field()
    score_love = scrapy.Field()
    # 運勢內容
    content_all = scrapy.Field()
    content_money = scrapy.Field()
    content_work = scrapy.Field()
    content_love = scrapy.Field()
    created_at = scrapy.Field()
    updated_at = scrapy.Field()

