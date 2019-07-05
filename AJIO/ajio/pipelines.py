# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
from ajio.items import AjioItem,AjioItem1

from scrapy.contrib.exporter import CsvItemExporter
from scrapy.contrib.exporter import JsonItemExporter

class AjioPipeline(object):

    host = 'localhost'
    user = 'root'
    password = 'moon'
    DB_name = "shein"

    def __init__(self):
        try:
            self.connection = MySQLdb.connect(self.host, self.user, self.password, charset='utf8')
            self.cursor = self.connection.cursor()
            self.cursor.execute('CREATE DATABASE ' + self.DB_name)
        except Exception as e:
            print(str(e))

        try:
            self.connection = MySQLdb.connect(self.host, self.user, self.password, self.DB_name, charset='utf8')
            self.cursor = self.connection.cursor()
            strquery2 = "CREATE TABLE Shein_data""""(Id INT NOT NULL AUTO_INCREMENT,
                                                         Url VARCHAR(250) DEFAULT NULL,
                                                         BrandName longtext DEFAULT NULL,
                                                         Name longtext DEFAULT NULL,
                                                         Standard_Price longtext DEFAULT NULL,
                                                         Actual_Price longtext DEFAULT NULL,
                                                         Discount longtext DEFAULT NULL,
                                                         Images longtext DEFAULT NULL,
                                                         Color longtext DEFAULT NULL,
                                                         OutofStock_Status longtext DEFAULT NULL,                                                                                                                        
                                                         Gender longtext DEFAULT NULL,
                                                         Category longtext DEFAULT NULL,                                                         
                                                         ProductHighlights longtext DEFAULT NULL,
                                                         unique key(`Url`), 
                                                         PRIMARY KEY (`Id`))"""

            self.cursor.execute(strquery2)
        except Exception as e:
            print(str(e))
        try:
            strquery3 = "CREATE TABLE Shein_urls""""(Id INT NOT NULL AUTO_INCREMENT,
                                                       Url VARCHAR(250) DEFAULT NULL,
                                                       Category longtext DEFAULT NULL,
                                                       Status longtext DEFAULT NULL,
                                                       unique key(`Url`), 
                                                       PRIMARY KEY (`Id`))"""
            self.cursor.execute(strquery3)

        except Exception as e:
            print(str(e))

    # def process_item(self, item, spider):
    #     if isinstance(item, AjioItem):
    #         try:
    #             self.connection = MySQLdb.connect(self.host, self.user, self.password, self.DB_name, charset='utf8')
    #             self.cursor = self.connection.cursor()
    #             self.cursor.execute("INSERT INTO Shein_data(Url,BrandName,Name,Standard_Price,Actual_Price,Discount,Images,Color,OutofStock_Status,Gender,Category,ProductHighlights) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(item['Url'],item['BrandName'],item['Name'],item['Standard_Price'],item['Actual_Price'],item['Discount'],item['Images'],item['Color'],item['OutofStock_Status'],item['Gender'],item['Category'],item['ProductHighlights']))
    #             self.connection.commit()
    #
    #             sql1=  "Update Ajio_urls set Status='Done' where Url="+"'"+item['Url']+"'"
    #             self.cursor.execute(sql1)
    #             self.connection.commit()
    #             # print("in pipeline")
    #             # print(item)
    #         except Exception as e:
    #             print e
    #     if isinstance(item, AjioItem1):
    #         try:
    #             self.connection = MySQLdb.connect(self.host, self.user, self.password, self.DB_name, charset='utf8')
    #             self.cursor = self.connection.cursor()
    #             self.cursor.execute("""INSERT INTO Shein_urls (Url,Category,Status)VALUES (%s,%s,%s)""",(item['Url'], item['Category'],item['Status']))
    #             self.connection.commit()
    #             # print("in pipeline")
    #             # print(item)
    #         except Exception as e:
    #             print e
    #
    #     return item


class CsvPipeline(object):

    def __init__(self):
        self.file = open("Shein_data.csv", 'wb')
        self.exporter = CsvItemExporter(self.file,unicode,fields_to_export=['SERIALNUMBER','ProductNAME','CATEGORY','Description','IMAGE','FABRIC','SIZE','COLOUR','color_temp','ProductID','PRICE','WEBSITENAME'])
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


