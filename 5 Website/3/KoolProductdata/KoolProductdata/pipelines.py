# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import psycopg2
import logging
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from KoolProductdata.ReusableFunctions import Scrape_BetweenString

class KoolproductdataPipeline(object):
    try:
        f = open('DbDetails.txt', 'r')
        DbDetails = str(f.read())
        f.close()
        dbname = Scrape_BetweenString(DbDetails, "dbname='", "'")
        #tableName =  "kool_corrections_data"
        tableName = dbname + "." + "kool_corrections_data"
        user = Scrape_BetweenString(DbDetails, "user='", "'")
        host = Scrape_BetweenString(DbDetails, "host='", "'")
        password = Scrape_BetweenString(DbDetails, "password='", "'")
    except Exception as e:
        logging.log(logging.ERROR, e)

    def __init__(self):

        try:
            # con = psycopg2.connect(user=user, host=host, password=password)
            con = psycopg2.connect(database = 'postgres',user=self.user, host=self.host, password=self.password)
            con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)  # <-- ADD THIS LINE
            cur = con.cursor()
            #cur.execute("CREATE DATABASE %s  ;" % self.dbname)
            cur.execute("CREATE schema IF NOT EXISTS  %s ;" % self.dbname)
        except Exception as e:
            print e
            logging.log(logging.ERROR, e)
        try:
            conn = psycopg2.connect(database='postgres', user=self.user, password=self.password, host=self.host,port="5432")
            cur = conn.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS """+self.tableName+
                                  """(ID serial PRIMARY KEY NOT NULL, 
                                    Name TEXT DEFAULT NULL,
                                    inmate_number  character(150) UNIQUE,
                                    Start_Date TEXT DEFAULT NULL,
                                    End_Date TEXT DEFAULT NULL,
                                    race TEXT DEFAULT NULL,
                                    gender TEXT DEFAULT NULL,
                                    hair_color TEXT DEFAULT NULL,
                                    eye_color TEXT DEFAULT NULL,
                                    age TEXT DEFAULT NULL,
                                    height TEXT DEFAULT NULL,
                                    weight TEXT DEFAULT NULL,
                                    Risk_Assessment_Rating TEXT DEFAULT NULL,
                                    imgUrl TEXT DEFAULT NULL,
                                    ConvictionInformation TEXT DEFAULT NULL,
                                    payrle_info TEXT DEFAULT NULL,
                                    Location TEXT DEFAULT NULL,
                                    Status VARCHAR(250) DEFAULT 'Done');""")
            conn.commit()  # <--- makes sure the change is shown in the database
            conn.close()
            cur.close()
        except Exception as e:
            print e

    def process_item(self, item, spider):

        try:
            conn = psycopg2.connect(database='postgres', user=self.user, password=self.password, host=self.host,port="5432")
            cur = conn.cursor()
            query = "INSERT INTO " + self.tableName + "(Name,inmate_number,Start_Date,End_Date,race,gender,hair_color,eye_color,age,height,weight,Risk_Assessment_Rating,imgUrl,ConvictionInformation,payrle_info,Location) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            cur.execute(query, (item['Name'], item['inmate_number'], item['Start_Date'], item['End_Date'], item['race'],
                        item['gender'], item['hair_color'], item['eye_color'], item['age'], item['height'],
                        item['weight'], item['Risk_Assessment_Rating'], item['imgUrl'], item['ConvictionInformation'],
                        item['payrle_info'], item['Location']))
            conn.commit()  # <--- makes sure the change is shown in the database
            print "Data Inserted ..."
            conn.close()
            cur.close()
        except Exception as e:
            print e
        return item
