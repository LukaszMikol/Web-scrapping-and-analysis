# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PremierleagueStaticItem(scrapy.Item):
    # define the fields for your item here like:
    Position = scrapy.Field()
    Club = scrapy.Field()
    Played = scrapy.Field()
    Won = scrapy.Field()
    Drawn = scrapy.Field()
    Lost = scrapy.Field()
    GF = scrapy.Field()
    GA = scrapy.Field()
    GD = scrapy.Field()
    Points = scrapy.Field()


