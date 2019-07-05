# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DpscsStateItem(scrapy.Item):
    id = scrapy.Field()
    InmateLink = scrapy.Field()
    first_name = scrapy.Field()
    last_name = scrapy.Field()
    inmate_number = scrapy.Field()
    race = scrapy.Field()
    gender = scrapy.Field()
    dob = scrapy.Field()
    incarceration_term = scrapy.Field()
    release_date = scrapy.Field()
    facility = scrapy.Field()
    active = scrapy.Field()
    hair_color = scrapy.Field()
    eye_color = scrapy.Field()
    image = scrapy.Field()
    state = scrapy.Field()
    last_updated = scrapy.Field()
    Sid = scrapy.Field()
    MiddleName = scrapy.Field()
    HTML_Save_Path_data = scrapy.Field()
    pass
