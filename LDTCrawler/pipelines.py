# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from LDTCrawler import settings
from LDTCrawler.items import Astro108Item


class LdtcrawlerPipeline(object):

    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        if item.__class__ == Astro108Item:
            self.cursor.execute(
                """insert into crawler_astro(astro_code, title_zh, date, source,
        score_all, score_money, score_work, score_love,
        content_all, content_money, content_work, content_love, created_at, updated_at)
                  value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (
                    item['astro_code'],
                    item['title_zh'],
                    item['date'],
                    item['source'],
                    item['score_all'],
                    item['score_money'],
                    item['score_work'],
                    item['score_love'],
                    item['content_all'],
                    item['content_money'],
                    item['content_work'],
                    item['content_love'],
                    item['created_at'],
                    item['updated_at'],
                ))
            self.connect.commit()

            pass
