# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import scrapy

class KoolproductdataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Name = scrapy.Field()
    inmate_number = scrapy.Field()
    Start_Date = scrapy.Field()
    End_Date = scrapy.Field()
    race = scrapy.Field()
    gender = scrapy.Field()
    hair_color = scrapy.Field()
    eye_color = scrapy.Field()
    age = scrapy.Field()
    height = scrapy.Field()
    weight = scrapy.Field()
    Risk_Assessment_Rating = scrapy.Field()
    imgUrl = scrapy.Field()
    ConvictionInformation = scrapy.Field()
    payrle_info = scrapy.Field()
    Location = scrapy.Field()
    pass
