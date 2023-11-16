# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsArticle(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    link = scrapy.Field()
    website = scrapy.Field()
    datetime_written = scrapy.Field()
    image_link = scrapy.Field()
    datetime_scraped = scrapy.Field()
