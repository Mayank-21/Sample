# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class AjioItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # Url = scrapy.Field()
    # BrandName = scrapy.Field()
    # Name = scrapy.Field()
    # Standard_Price = scrapy.Field()
    # Actual_Price = scrapy.Field()
    # Discount = scrapy.Field()
    # Images = scrapy.Field()
    # Color = scrapy.Field()
    # OutofStock_Status = scrapy.Field()
    # Gender = scrapy.Field()
    # Category = scrapy.Field()
    # ProductHighlights = scrapy.Field()
    SERIALNUMBER = scrapy.Field()
    ProductNAME = scrapy.Field()
    CATEGORY = scrapy.Field()
    Description = scrapy.Field()
    IMAGE = scrapy.Field()
    FABRIC = scrapy.Field()
    SIZE = scrapy.Field()
    COLOUR = scrapy.Field()
    color_temp = scrapy.Field()
    ProductID = scrapy.Field()
    PRICE = scrapy.Field()
    WEBSITENAME = scrapy.Field()
    pass

class AjioItem1(scrapy.Item):
    Url = scrapy.Field()
    Status=scrapy.Field()
    Category=scrapy.Field()
