# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class FincrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    timestamp = scrapy.Field()
    date = scrapy.Field() # Date
    guru = scrapy.Field() # Predictor
    stockname = scrapy.Field() # Stock
    advice = scrapy.Field() # Adviced strategy
    goal = scrapy.Field() # Optional - target value for advice
    currency = scrapy.Field() # Currency of the goal
    website = scrapy.Field() # Website fetched from
    stockticker = scrapy.Field() # Ticker for stockname
    # url = scrapy.Field() # Scraped url
    # exchange = scrapy.Field() # Exchange on which stock is listed
    # index = scrapy.Field() # Index of the exchange on which the stock is listed