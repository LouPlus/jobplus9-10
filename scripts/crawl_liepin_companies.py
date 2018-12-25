import scrapy

class CompanySpider(scrapy.Spider):
    name = 'companies'

    company_ids = [
        '7983148', '1072424', '7877799', '8076624', '970775', '7904498', '8613331', '7863254', '7857467', '8463490', '6429309', '1337351', '884492',
        '7946594', '7995350', '8075159', '8157392', '8173268', '8179276', '8210905', '8212146', '8260075', '8271739', '8292581', '8297294',
         '8317411', '8351379', '8362323', '8369326', '8373917', '8374288', '8381526', '8383170'
        ]

    start_urls = ['{}/{}'.format("https://www.liepin.com/company", company_id) for company_id in company_ids]

    def parse(self, response):
        yield  {
            'name': response.xpath('.//div[@class="name-and-welfare"]/h1/text()').extract_first(),
            'logo': response.xpath('.//img[@class="bigELogo"]/@src').extract_first(),
            'description': response.xpath('.//div[contains(@class,"company-introduction")]/p[@class="profile"]/text()').extract_first().strip(),
            'addr': response.xpath('.//ul[@class="new-compintro"]/li/@title').extract_first(),
            'about': ''.join(response.xpath('.//div[contains(@class,"company-introduction")]/p[@class="profile"]/text()').extract()).strip(),
            'tags': ','.join(response.xpath('//div[@class="comp-summary-tag"]/a/text()').extract()),
            'welfares': ','.join(response.xpath('.//ul[contains(@class,"comp-tag-list")]/li/span/text()').extract())
        }