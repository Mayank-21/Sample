# -*- coding: utf-8 -*-
import scrapy
import csv
import logging
import MySQLdb
import os
import traceback
from ajio.items import AjioItem
#import xlsxwriter
import pandas as pd
from pandas import DataFrame
from pandas import ExcelWriter
import json
import math
import json, ast

class AjioDataSpider(scrapy.Spider):
    name = 'ajio_data'
    allowed_domains = ['www.ajio.com']

    def start_requests(self):
        host = 'localhost'
        user = 'root'
        password = 'xbyte'
        DB_name = "ajio"
        db = MySQLdb.connect(host, user, password, DB_name)
        Current_Directory = os.path.dirname(os.path.abspath(__file__))
        try:
            self.connection = MySQLdb.connect(host, user, password, DB_name, charset='utf8')
            self.cursor = self.connection.cursor()
            sql = ("Select * from ajio_urls where Status='Pending' AND ID BETWEEN 1 and 100000")
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
        except Exception as e:
            logging.log(logging.ERROR, e)

        for row in results:
            try:
                ID = str(row[0]).strip()
                print ID
                Url = str(row[1]).strip()
                Category = str(row[2]).strip()
                Status = str(row[3]).strip()
                yield scrapy.FormRequest(str(Url), callback=self.Get_data, method='GET', meta={'Product_link': str(Url), 'category': Category, 'ID': ID})
            except Exception as e:
                logging.log(logging.ERROR, e)


    def Get_data(self, response):
        Current_Directory = os.path.dirname(os.path.abspath(__file__))
        try :
            Url = ''
            BrandName= ''
            Name= ''
            Standard_Price= ''
            Actual_Price= ''
            Discount = ''
            Images = ''
            Color = ''
            OutofStock_Status = ''
            Gender = ''
            Category = ''
            ProductHighlights = ''
            ImagesList = []
            Strhtml = response.text
            item = AjioItem()
        except Exception as e:
            #print e
            logging.log(logging.ERROR, e)

        # --- Url
        try:
            Url = response.url
        except Exception as e:
            logging.log(logging.ERROR, e)

        # --- Scrape Json Project_data
        try:
            MainTag = response.xpath('//script[contains(text(),"window.__PRELOADED_STATE__")]/text()').extract_first()
            #print MainTag
            MainTag = MainTag.replace('window.__PRELOADED_STATE__ =', '')
            while MainTag.endswith(";") or MainTag.endswith(" ") or MainTag.endswith('\n') or MainTag.endswith('\r'):
                MainTag = MainTag[:-1]
            while MainTag.startswith(" ") or MainTag.startswith('\n') or MainTag.startswith('\r'):
                MainTag = MainTag[1:]
            MainTag_json = json.loads(MainTag)
        except Exception as e:
            logging.log(logging.ERROR, e)
        # --- BrandName
        try:
            BrandName = MainTag_json['product']['productDetails']['fnlColorVariantData']['brandName']
        except Exception as e:
            logging.log(logging.ERROR, e)
        # --- Name or Title
        try:
            Name = MainTag_json['product']['productDetails']['name']
        except Exception as e:
            #print e
            logging.log(logging.ERROR, e)
        # --- Standard_Price
        try:
            Standard_Price = MainTag_json['product']['productDetails']['variantOptions'][0]['wasPriceData']['value']
        except Exception as e:
            #print e
            logging.log(logging.ERROR, e)
        # --- Actual_Price
        try:
            Actual_Price = MainTag_json['product']['productDetails']['price']['value']
        except Exception as e:
            #print e
            logging.log(logging.ERROR, e)

        # --- Discount
        try:
            if Standard_Price!='' and Actual_Price!='':
                Discount = str(100 - int(int(Actual_Price) * 100 ) / int(Standard_Price) )+ '%'
            if Discount == '0%':
                Discount = ''
        except Exception as e:
            #print e
            logging.log(logging.ERROR, e)

        # --- Images
        try:
            ImagesList = MainTag_json['product']['productDetails']['images']
            for Image in ImagesList:
                ImageFormat = ''
                ImageFormat = Image['format']
                if ImageFormat == 'superZoomPdp':
                    Images = Image['url']
                    break
            if Images=='':
                for Image in ImagesList:
                    ImageFormat = ''
                    ImageFormat = Image['format']
                    if ImageFormat == 'product' and Image['imageType']=='GALLERY':
                        Images = Image['url']
                        break

        except Exception as e:
            #print e
            logging.log(logging.ERROR, e)
        # --- Color
        try:
            Color = MainTag_json['product']['productDetails']['fnlColorVariantData']['color']
        except Exception as e:
            #print e
            logging.log(logging.ERROR, e)
        # --- OutofStock_Status
        try:
            OutofStock_Status = MainTag_json['product']['productDetails']['variantOptions'][0]['stock']['stockLevelStatus']
        except Exception as e:
            #print e
            logging.log(logging.ERROR, e)
        # --- Gender,Category
        try:
            ItemList = Strhtml.split('itemListElement":', 1)[1].split('</script>', 1)[0].split('"name":"')
            Gender = ItemList[2].split('"', 1)[0]
            for i in range(3, len(ItemList)):
                temp = ''
                temp = ItemList[i].split('"', 1)[0]
                if temp != '':
                    if Category == '':
                        Category = temp
                    else:
                        Category = Category + '/' + temp
        except Exception as e:
            #print e
            logging.log(logging.ERROR, e)

        # --- ProductHighlights_1
        try:
            ProductDetail = ''
            ProductHighlights_Temp = ''
            ProductHighlights_Temp = MainTag_json['product']['productDetails']['featureData']
            for ProductHighlight in ProductHighlights_Temp:
                try:
                    ProductHighlights_Name = ''
                    ProductHighlights_Value = ''
                    ProductHighlights_Name = str(ProductHighlight['name'])
                    ProductHighlights_Value = str(ProductHighlight['featureValues'][0]['value'])
                    if ProductHighlights_Name!='' and ProductHighlights_Value!='':
                        if ProductHighlights =='':
                            ProductHighlights = ProductHighlights_Name + ":" + ProductHighlights_Value
                        else:
                            ProductHighlights =ProductHighlights + "|"+ ProductHighlights_Name + ":" + ProductHighlights_Value
                except Exception as e:
                    #print e
                    logging.log(logging.ERROR, e)
        except Exception as e:
            #print e
            logging.log(logging.ERROR, e)
        # --- ProductHighlights_2
        try:
            ProductHighlights_Name = ''
            ProductHighlights_Value = ''
            ProductHighlights_Temp = ''
            ProductHighlights_Temp = MainTag_json['product']['productDetails']['variantOptions'][0]['mandatoryInfo']
            ProductHighlights_Name = str(ProductHighlights_Temp[0]['key'])
            ProductHighlights_Value = str(ProductHighlights_Temp[0]['title'])
            if ProductHighlights_Name != '' and ProductHighlights_Value != '':
                if ProductHighlights == '':
                    ProductHighlights = ProductHighlights_Name + ":" + ProductHighlights_Value
                else:
                    ProductHighlights = ProductHighlights + "|" + ProductHighlights_Name + ":" + ProductHighlights_Value
        except Exception as e:
            #print e
            logging.log(logging.ERROR, e)
        # --- ProductHighlights_3
        try:
            ProductCode = ''
            ProductHighlights_Name = ''
            ProductHighlights_Value = ''
            ProductCode = str(MainTag_json['product']['productDetails']['variantOptions'][0]['code'])
            ProductHighlights_Name = 'Product Code'
            if ProductCode != '':
                if ProductHighlights == '':
                    ProductHighlights = ProductHighlights_Name + ":" + ProductCode
                else:
                    ProductHighlights = ProductHighlights + "|" + ProductHighlights_Name + ":" + ProductCode
        except Exception as e:
            #print e
            logging.log(logging.ERROR, e)
        # --- ProductHighlights_4
        try:
            ProductHighlights_Name = ''
            ProductHighlights_Value = ''
            ProductHighlights_Temp = ''
            ProductHighlights_Temp = MainTag_json['product']['productDetails']['mandatoryInfo']
            for ProductHighlight in ProductHighlights_Temp:
                try:
                    ProductHighlights_Name = str(ProductHighlight['key'])
                    ProductHighlights_Value = str(ProductHighlight['title'])
                    if ProductHighlights_Name != '' and ProductHighlights_Value != '':
                        if ProductHighlights == '':
                            ProductHighlights = ProductHighlights_Name + ":" + ProductHighlights_Value
                        else:
                            ProductHighlights = ProductHighlights + "|" + ProductHighlights_Name + ":" + ProductHighlights_Value
                except Exception as e:
                    #print e
                    logging.log(logging.ERROR, e)
        except Exception as e:
            #print e
            logging.log(logging.ERROR, e)

        # --- import all data-field into item-dictionary & DataTable
        try:
            item['Url'] = Url
            item['BrandName'] = BrandName
            item['Name'] = Name
            item['Standard_Price'] = Standard_Price
            item['Actual_Price'] = Actual_Price
            item['Discount'] = Discount
            item['Images'] = Images
            item['Color'] = Color
            item['OutofStock_Status'] = OutofStock_Status
            item['Gender'] = Gender
            item['Category'] = Category
            ProductHighlights = str(ast.literal_eval(json.dumps(ProductHighlights))).replace('{','').replace('}','').replace(', ',',').replace(',\'','|\'').replace(': ',':').replace("':'",':').replace("'|'",'|')
            while ProductHighlights.startswith("'"):
                ProductHighlights = ProductHighlights[1:]
            while ProductHighlights.endswith("'"):
                ProductHighlights = ProductHighlights[:-1]
            item['ProductHighlights'] = ProductHighlights
            yield item
        except Exception as e:
            ##print e
            logging.log(logging.ERROR, e)

