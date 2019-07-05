# -*- coding: utf-8 -*-
import scrapy
from ajio.items import AjioItem,AjioItem1
import logging
import requests
from xml.dom.minidom import parseString
import time


class AjioLinkSpider(scrapy.Spider):
    name = 'ajio_link'
    allowed_domains = ['www.ajio.com']
    #start_urls = ['https://www.ajio.com/sitemap.xml']

    def start_requests(self):
        urls_items = []
        urls = [line.rstrip('\n') for line in open('Input.txt', 'r')]
        #urls = lines
        filepath = 'Input.txt'
        for url in urls:
            try:
                yield scrapy.Request(url=str(url), callback=self.parse)
            except Exception as e:
                logging.log(logging.ERROR, e)

    def parse(self, response):
        # time.sleep(180)
        print response.url + '--ResponseStatus('+ str(response.status)+')'
        # f = open('main.html', 'w')
        # f.write(response.text)
        # f.close
        #print response.status
        if not response.status == 200:
            return
        item = AjioItem1()
        try:
            #category = response.meta['category']
            xml = parseString(response.body)
            urlset = xml.getElementsByTagName("urlset")[0]
            urls = urlset.getElementsByTagName("url")
            for url in urls:
                try:
                    data = url.getElementsByTagName('loc')[0].childNodes[0].nodeValue
                    item['Url'] = data
                    print item['Url']
                    item['Status'] = 'Pending'
                    item['Category'] = ''
                    yield item
                except Exception as e:
                    print e
        except Exception as e:
            print e
            logging.log(logging.ERROR, e)

        pass
