# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import CsvItemExporter
import sqlite3
from scrapy import signals
from os import path
from scrapy.xlib.pydispatch import dispatcher

class SQLiteStorePipeline(object):
    filename = 'data.sqlite'

    def __init__(self):
        self.conn = None
        dispatcher.connect(self.initialize, signals.engine_started)
        dispatcher.connect(self.finalize, signals.engine_stopped)

    def process_item(self, item, spider):
        for key, value in item.items():  # Trim, change , to . etc. Replace ""
            try:
                item[key] = value[0].replace(',', '.').replace('"', '').strip() # Each item value is a list. Access the string in element [0] if it exists.
            except IndexError:
                item[key] = ""
        try:
            self.conn.execute('INSERT INTO scrapedata(\
            timestamp, \
            advice, \
            currency, \
            date, \
            goal, \
            guru, \
            website, \
            stockname, \
            stockticker) \
            VALUES(?,?,?,?,?,?,?,?)',
                              (
                                  item['advice'],
                                  item['currency'],
                                  item['date'], # Get date to dd/MM/yyyy value
                                  item['goal'],
                                  item['guru'],
                                  item['website'],
                                  item['stockname'],
                                  item['stockticker']
                              ))
        except:
            print('Failed to insert item: ' + item['date'] + " " + item['stockname'])
        return item

    def initialize(self):
        if path.exists(self.filename):
            self.conn = sqlite3.connect(self.filename)
        else:
            self.conn = self.create_table(self.filename)
            # self.conn = self.drop_table(self.filename)

    def finalize(self):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()
            self.conn = None

    def create_table(self, filename):
        conn = sqlite3.connect(filename) # Datevalues: yyyy-MM-dd HH:mm:ss
        conn.execute("CREATE TABLE IF NOT EXISTS scrapedata(id INTEGER PRIMARY KEY NOT NULL, \
            timestamp DATE, \
            advice TEXT, \
            currency REAL, \
            date TEXT, \
            goal REAL, \
            guru TEXT, \
            website TEXT, \
            stockname TEXT, \
            stockticker TEXT \
            )")
        conn.commit()
        return conn

    # def drop_table(self):
    #     self.conn.execute("DROP TABLE IF EXISTS scrapedata")
        # self.conn.execute("DROP TABLE IF EXISTS date AND stockname AND guru")
        # self.conn.execute("DELETE FROM scrapedata WHERE advice IS NULL")

# class FincrawlerV3Pipeline(object):
    # def __init__(self):
    #     self.file = open("FincrawlData.csv", 'wb') # a for append, wb for write in binary
    #     self.exporter = CsvItemExporter(self.file)
    #     self.exporter.start_exporting()
    #
    # def process_item(self, item, spider):
    #     # Add some code to trim, replace etc. all items to standardize output
    #     for key, value in item.items(): # Trim, change , to . etc. Replace ""
    #         try:
    #             item[key] = value[0].replace(',', '.').replace('"', '').strip() # Each item value is a list. Access the string in element [0] if it exists.
    #         except IndexError:
    #             item[key] = ""
    #     # Could add code to determine currency of the item['goal']
    #     self.exporter.export_item(item) # Export item
    #     return item
    #
    # def close_spider(self, spider):
    #     self.exporter.finish_exporting()
    #     self.file.close()