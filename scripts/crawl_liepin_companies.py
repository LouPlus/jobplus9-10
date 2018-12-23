import scrapy

class CompanySpider(scrapy.Spider):
    name = 'companies'

    company_ids = ['7983148','1072424','7877799','8076624','970775','7904498','8613331','7863254','7857467','8463490','6429309','1337351','884492']

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