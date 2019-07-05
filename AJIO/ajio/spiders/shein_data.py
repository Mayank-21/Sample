# -*- coding: utf-8 -*-
import scrapy
from ajio.items import AjioItem,AjioItem1
import logging
import requests
from xml.dom.minidom import parseString
import time
import csv
import os
import json
import math
import json, ast
from ajio.Createfolder import Create_Folder
from ajio.Extract_Data import Get_ReplaceData,Replace_Junk,Strip_Tag,Get_ReData
Current_Directory = os.path.dirname(os.path.abspath(__file__))

class AjioLinkSpider(scrapy.Spider):
    name = 'shein_data'
    allowed_domains = ['www.shein.in']
    index1 = Current_Directory.rfind("\\")
    HtmlDirectory = Current_Directory
    create_folder = Create_Folder(HtmlDirectory, "")
    # HTML_Path_Main = HtmlDirectory + '\\Html\\' + '\\Main\\' + 'Main_1' + '.html'
    #start_urls = ['https://www.ajio.com/sitemap.xml']

    def start_requests(self):

        #Change - Reading from a csv instead of SQL table(All extracted urls are dumped into a CSV)
        #f = open('shein_urls.csv', 'r')
        f = open('shein_urls_temp.csv', 'r')
        reader = csv.reader(f, delimiter=',')
        next(reader)
        #for row in reader:
        for row in reader:
            try:
                ID = str(row[0]).strip()
                print ID
                Url = str(row[1]).strip()
                #Category = str(row[2]).strip()
                #Status = str(row[3]).strip()
                #yield scrapy.FormRequest(str(Url), callback=self.parse, method='GET', meta={'Product_link': str(Url), 'category': Category, 'ID': ID})
                yield scrapy.FormRequest(str(Url), callback=self.parse, method='GET',
                                         meta={'Product_link': str(Url), 'ID': ID})
            except Exception as e:
                ##print e
                logging.log(logging.ERROR, e)
        # urls_items = []
        # urls = [line.rstrip('\n') for line in open('Input.txt', 'r')]
        # #urls = lines
        # filepath = 'Input.txt'
        # for url in urls:
        #     try:
        #         yield scrapy.Request(url=str(url), callback=self.parse)
        #     except Exception as e:
        #         logging.log(logging.ERROR, e)

    def parse(self, response):
        print response.url + '--ResponseStatus('+ str(response.status)+')'

        SERIALNUMBER = ''
        ProductNAME = ''
        CATEGORY = ''
        Description = ''
        IMAGE = ''
        FABRIC = ''
        SIZE = ''
        COLOUR = ''
        color_temp = ''
        ProductID = ''
        PRICE = ''
        WEBSITENAME = ''

        Strhtml_Data = ''
        try:
            Strhtml_Data = response.text.encode('utf-8')
            WEBSITENAME = response.meta['Product_link']
            ID = response.meta['ID']
            #f = open(Current_Directory +"\Html\Html_data\" ID+".html", "w")
            Html_Data_Path = ''
            Html_Data_Path = Current_Directory+"\Html\Html_data\\"+ID+".html"
            f = open(Html_Data_Path, "w")
            f.write(Strhtml_Data)
            f.close
        except Exception as e:
            ##print e
            logging.log(logging.ERROR, e)
        #SERIALNUMBER
        try:
            SERIALNUMBER = Get_ReData(Strhtml_Data,'class="sku">SKU:','</span>').strip()
        except Exception as e:
            ##print e
            logging.log(logging.ERROR, e)
        # ProductNAME
        try:
            ProductNAME = Get_ReData(Strhtml_Data, 'itemprop="name" content="', '"').strip()
        except Exception as e:
            ##print e
            logging.log(logging.ERROR, e)
        # CATEGORY
        try:
            CATEGORY = Get_ReData(Strhtml_Data, '"category_name":"', '"').strip()
        except Exception as e:
            ##print e
            logging.log(logging.ERROR, e)
        # CATEGORY
        try:
            CATEGORY = Get_ReData(Strhtml_Data, '"category_name":"', '"').strip()
        except Exception as e:
            ##print e
            logging.log(logging.ERROR, e)
        # Description
        try:
            DescriptionTag  = response.xpath('//div[@class="desc-con j-desc-con desc-wrap-default"]').extract_first()
            #DescriptionTag = response.xpath('//script[contains(text(),"window.__PRELOADED_STATE__")]/text()').extract_first()
            replace_value = ['<div class="kv-row">']
            reply_value = ['|']
            Description = Get_ReplaceData(str(DescriptionTag), '', "", replace_value,reply_value)
            #Description = Get_ReData(Strhtml_Data, '"category_name":"', '"').strip()
        except Exception as e:
            ##print e
            logging.log(logging.ERROR, e)
        # # IMAGE
        # try:
        #     IMAGE = 'https:'+Get_ReData(Strhtml_Data, 'property="og:image" content="', '_im_').strip() + '.jpg'
        # except Exception as e:
        #     ##print e
        #     logging.log(logging.ERROR, e)

        # IMAGE
        try:
            IMAGE=''
            Save_Path_Image=''
            IMAGE = 'https:' + Get_ReData(Strhtml_Data, 'property="og:image" content="', '_im_').strip() + '_im_100x100'+'.jpg'
            if IMAGE!='':
                Save_Path_Image = Current_Directory + "\Images\\" + SERIALNUMBER + '.jpeg'
                img_data = requests.get(IMAGE).content
                with open(Save_Path_Image, 'wb') as handler:
                    handler.write(img_data)
        except Exception as e:
            ##print e
            logging.log(logging.ERROR, e)
        # FABRIC
        try:
            FABRIC = ''
            FABRIC_String = ''
            FABRIC = Get_ReData(Strhtml_Data, 'Material:</div>', '</div>').strip()
            if FABRIC!='':
                FABRIC_String = 'Material:'+FABRIC
            while ', ' in FABRIC_String:
                FABRIC_String = FABRIC_String.replace(', ',',')
            Description = Description.replace(FABRIC_String+'|' ,'')
            Description = Description.replace('|'+FABRIC_String, '')
            Description = Description.replace(FABRIC_String, '')
        except Exception as e:
            ##print e
            logging.log(logging.ERROR, e)
        # COLOUR
        try:
            COLOUR = ''
            COLOUR_String = ''
            COLOUR = Get_ReData(Strhtml_Data, 'Color:</div>', '</div>').strip()
            if COLOUR != '':
                COLOUR_String = 'Color:' + COLOUR
            Description = Description.replace(COLOUR_String + '|', '')
            Description = Description.replace('|' + COLOUR_String, '')
            Description = Description.replace(COLOUR_String, '')
        except Exception as e:
            ##print e
            logging.log(logging.ERROR, e)
        # Size
        try:
            Size_all = ''
            TEmp = ''
            MainTag_json = ''
            TEmp = Get_ReData(Strhtml_Data,"gbCommonInfo.pageType = 'goodsDetail'",'</script>')
            TEmp = TEmp.split('var gbProductDetailSsrData = ',1)[1]
            TEmp = Get_ReData(TEmp,'goodsInfo:','gbProductDetailSsrData.language[gbCommonInfo.lang]')
            print TEmp
            while TEmp.endswith(' '):
                TEmp = TEmp[:-1]
            print TEmp
            if TEmp.endswith('}'):
                TEmp = TEmp[:-1]
            MainTag_json = json.loads(TEmp)
            Size_all = MainTag_json['sizeInfoDes']['sizeInfo']
            Size = ''
            for size_item in Size_all:
                if Size == '':
                    Size = size_item['size']
                else:
                    Size = Size +','+ size_item['size']
            SIZE = Size
        except Exception as e:
            ##print e
            logging.log(logging.ERROR, e)

        # Color_all
        try:
            Color_all = MainTag_json['relationProducts']
            color_temp = ''
            color_temp = MainTag_json['detail']['productDetails'][0]['attr_value']
            for color_item in Color_all:
                if color_temp == '':
                    color_temp = color_item['productDetails'][0]['attr_value']
                else:
                    color_temp = color_temp + ',' + color_item['productDetails'][0]['attr_value']
            #color_temp = MainTag_json['detail']['productDetails'][0]['attr_value']
        except Exception as e:
            ##print e
            logging.log(logging.ERROR, e)
        # PRICE
        try:
            PRICE = Get_ReData(Strhtml_Data, ' itemprop="price" content="', '"').strip()
        except Exception as e:
            ##print e
            logging.log(logging.ERROR, e)

        ProductID = SERIALNUMBER
        #print response.status
        if not response.status == 200:
            return
        item = AjioItem()

        try:
            item['SERIALNUMBER'] = SERIALNUMBER
            item['ProductNAME'] = ProductNAME
            item['CATEGORY'] = CATEGORY
            item['Description'] = Description
            item['IMAGE'] = IMAGE
            item['FABRIC'] = FABRIC
            item['SIZE'] = SIZE
            item['COLOUR'] = COLOUR
            item['color_temp'] = color_temp
            item['ProductID'] = ProductID
            item['PRICE'] = PRICE
            item['WEBSITENAME'] = WEBSITENAME
            yield item
        except Exception as e:
            print e
            logging.log(logging.ERROR, e)

        pass
