# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapeItem(scrapy.Item):
    # define the fields for your item here like:
    id_vid = scrapy.Field()
    title=scrapy.Field()
    views = scrapy.Field()
    duration = scrapy.Field()
    description = scrapy.Field()
    url=scrapy.Field()
    
    
