# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class KoolDataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
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
    Location = scrapy.Field()
    Offense = scrapy.Field()
    TDD_SDD = scrapy.Field()
    Commitment_Date = scrapy.Field()
    Recall_Date = scrapy.Field()
    Mandatory_Minimum = scrapy.Field()
    Supervision_Status = scrapy.Field()
    Offense_Class = scrapy.Field()
    County_of_Commitment = scrapy.Field()
    End_Date = scrapy.Field()
    pass
