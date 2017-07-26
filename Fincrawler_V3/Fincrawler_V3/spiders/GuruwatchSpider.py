import scrapy
from Fincrawler_V3.items import FincrawlerItem

class GuruwatchSpider(scrapy.Spider):
    name = "guruwatch.nl"
    allowed_domains = ["guruwatch.nl"]
    start_urls = ["https://www.guruwatch.nl/adviezen/default.aspx"
                  ]

    def parse(self, response):
        for row in response.xpath("//html/body/form/div/div/table/tbody/tr"):
            item = FincrawlerItem()
            item['date'] = row.xpath("td[1]/span/text()").extract()
            item['guru'] = row.xpath("td[2]/a/text()").extract()
            item['stock'] = row.xpath("td[3]/a/text()").extract()
            item['advice'] = row.xpath("td[@class][4]/span/text()").extract()
            item['goal'] = row.xpath("td[6]/span/text()").extract()
            yield item