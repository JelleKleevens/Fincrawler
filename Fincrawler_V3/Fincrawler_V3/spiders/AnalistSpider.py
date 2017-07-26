import scrapy
from Fincrawler_V3.items import FincrawlerItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from datetime import datetime

class AnalistSpider(CrawlSpider): # scrapy runspider AnalistSpider.py
    name = "analist.nl"
    allowed_domains = ["analist.nl"]
    start_urls = ["http://www.analist.nl/adviezen"
                  ]

    # MAKE RULES FOR NEXT_PAGE CRAWLING
    rules = (
        Rule(LinkExtractor(restrict_xpaths=("//li[@class='next']")), callback="parse_start_url", follow=True), # The comma is needed, otherwise it's interpreted as a tuple
        Rule(LinkExtractor(restrict_xpaths=("//select[@id='index']/option")), callback="parse_item", follow=True),
        # Rule(LinkExtractor(restrict_xpaths=("//select[@id='exchange']/option")), callback="parse_item", follow=True), # Check for all exchanges (werkt niet)
    )

    def parse_start_url(self, response): # parse_start_url will make sure the first page scraped is the start_url
        for row in response.xpath("//html/body/div/div/div/div/table/tr"):  # WORKS AFTER LEAVING TBODY TAG OUT???
            item = FincrawlerItem()
            item['timestamp'] = [datetime.today().strftime("%Y%m%d")]
            item['date'] = row.xpath("td[1]/a/text()").extract()
            item['guru'] = row.xpath("td[2]/a/text()").extract()
            item['stockname'] = row.xpath("td[3]/a/text()").extract()
            item['advice'] = row.xpath("td[4]/text()").extract()
            item['goal'] = row.xpath("td[@class='text-right']/text()").extract()
            item['currency'] = ['EUR'] #Only yields 'E' without brackets --> specify to make 'EUR' the first list element
            item['website'] = ['analist.nl']
            item['stockticker'] = ['']
            yield item

        # Specific code to extract all urls for Analist.nl advice
        # Also add meta data to each item? By passing exchange and index

        for exchange in response.xpath("//select[@id='exchange']/option/@value").extract():
            url_part1 = "http://www.analist.nl/adviezen/{}/".format(exchange) # This gets the right text to create the Exchange part of the url
            for index in response.xpath("//select[@id='index']/option/@value").extract():
                url = url_part1 + index + "/" # This creates the full url !!! DOUBLE CHECK IF THEY ARE FROM THE RIGHT ONE...
                yield Request(url, callback=self.parse_start_url, meta={'url': url})
            yield Request(url_part1, callback=self.parse_start_url)

            # https://stackoverflow.com/questions/36784912/how-to-add-additional-urls-created-manually-in-scrapy-python
            # https://stackoverflow.com/questions/4835891/extract-value-of-attribute-node-via-xpath
            # http://www.analist.nl/adviezen/2-euronext-amsterdam
            # GET: IF EXCHANGE "//SELECT[@ID='EXCHANGE']/OPTION[@SELECTED='SELECTED'] THEN GET INDEX LIST
