from LDTCrawler.items import Astro108Item

import scrapy, time, datetime


from urllib.parse import unquote, urlparse;

def str_after(subject, search):
    return subject.split(search)[1]

class Astore108Spider(scrapy.Spider):
    name = 'Astore108Crawler'
    allowed_domains = ['click108.com.tw']
    start_urls = ['http://astro.click108.com.tw/']
    
    astro_title = {
        10: '水瓶座',
        11: '雙魚座',
        0: '牡羊座',
        1: '金牛座',
        2: '雙子座',
        3: '巨蟹座',
        4: '獅子座',
        5: '處女座',
        6: '天秤座',
        7: '天蠍座',
        8: '射手座',
        9: '摩羯座',
    }

    def parse(self, response):
        item = Astro108Item();
        xpath = '//div[contains(@class, \'STAR12_BOX\')]/ul/li/a';
        stars = response.selector.xpath(xpath)
        for star in stars:
            # get-title
            # title_zh = star.xpath('./text()').extract_first()

            # get-link
            initHref = star.xpath('./@href').extract_first()
            url = unquote(str_after(initHref, 'RedirectTo='))

            # get astroCode from query
            res = urlparse(url)
            astroCode = str_after(res.query, '=')

            yield scrapy.Request(url=url, callback=self.parse_detail, meta={'item': item})

    def parse_detail(self, response):
        item = response.meta['item']
        # 1.獲取運勢指數
        xpath  = '//div[contains(@class,\'STAR_LIGHT\')]/img';
        scores = response.selector.xpath(xpath)
        for score in scores:
            #parse score
            imgSrc = score.xpath('./@src').extract_first()
            imgInfo = str_after(imgSrc, 'SUB/').split('/')

            itemKey = 'score_' + imgInfo[0]
            itemVal = filter(str.isdigit, imgInfo[1])
            itemVal = ''.join(list(itemVal))

            item[itemKey] = int(itemVal);
        # 2.獲取運勢分析
        xpath = '//div[contains(@class,\'TODAY_CONTENT\')]/p';
        contents = response.selector.xpath(xpath)
        contentArr = {
            1 : 'all',
            3 : 'love',
            5 : 'work',
            7 : 'money',
        }
        i = 0;
        for content in contents:
            contentText = content.xpath('./text()').extract_first()

            if (contentText != None) :
                contentName = contentArr.get(i);
                itemKey = 'content_' + contentName
                item[itemKey] = contentText;
                pass
            i += 1
        # 3.獲取頁面時間
        xpath = '//select[@name=\'iAcDay\']/option[@selected=\'selected\']/text()';
        date = response.selector.xpath(xpath).extract_first();
        item['date'] = time.mktime(datetime.datetime.strptime(date, '%Y-%m-%d').timetuple())
        # 4.
        res = urlparse(response.url)
        astroCode = int(str_after(res.query, '='))

        item['astro_code'] = astroCode
        item['title_zh'] = self.astro_title.get(astroCode, '')
        item['source'] = 1  # 1:python
        item['created_at'] = item['updated_at'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        yield item