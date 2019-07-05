# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dpscs_state.items import DpscsStateItem
from dpscs_state.ReusableFunctions import Scrape_BetweenString




class DpscsStatePipeline(object):

    try:
        f = open('DbDetails.txt', 'r')
        DbDetails = str(f.read())
        f.close()
        dbname = Scrape_BetweenString(DbDetails, "dbname='", "'")
        user = Scrape_BetweenString(DbDetails, "user='", "'")
        host = Scrape_BetweenString(DbDetails, "host='", "'")
        password = Scrape_BetweenString(DbDetails, "password='", "'")
        tableName = dbname + "." + "dpscs_state_Data"
    except Exception as e:
        logging.log(logging.ERROR, e)

    def __init__(self):

        # ------------------Create Database & create table
        try:
            # con = psycopg2.connect(user=user, host=host, password=password)
            con = psycopg2.connect(dbname='postgres', user=self.user, host=self.host, password=self.password)
            con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)  # <-- ADD THIS LINE
            cur = con.cursor()
            #cur.execute("CREATE DATABASE %s  ;" % self.dbname)
            cur.execute("CREATE schema IF NOT EXISTS  %s ;" % self.dbname)
        except Exception as e:
            logging.log(logging.ERROR, e)

        try:
            #conn = psycopg2.connect(database=self.dbname, user=self.user, password=self.password, host=self.host, port="5432")
            conn = psycopg2.connect(database='postgres', user=self.user, password=self.password, host=self.host,port="5432")
            cur = conn.cursor()
            cur.execute('''CREATE TABLE '''+self.tableName+''' 
                                  (ID serial PRIMARY KEY NOT NULL, 
                                  InmateLink VARCHAR(250) UNIQUE DEFAULT NULL,
                                  first_name TEXT DEFAULT NULL,
                                    last_name TEXT DEFAULT NULL,
                                    inmate_number TEXT DEFAULT NULL,
                                    race TEXT DEFAULT NULL,
                                    gender TEXT DEFAULT NULL,
                                    dob TEXT DEFAULT NULL,
                                    incarceration_term TEXT DEFAULT NULL,
                                    release_date TEXT DEFAULT NULL,
                                    facility TEXT DEFAULT NULL,
                                    active TEXT DEFAULT NULL,
                                    hair_color TEXT DEFAULT NULL,
                                    eye_color TEXT DEFAULT NULL,
                                    image TEXT DEFAULT NULL,
                                    state TEXT DEFAULT NULL,
                                    last_updated TEXT DEFAULT NULL, 
                                    Sid TEXT DEFAULT NULL, 
                                    MiddleName TEXT DEFAULT NULL,                                
                                  HTML_Save_Path_data VARCHAR(250) DEFAULT NULL,
                                  Status VARCHAR(250) DEFAULT 'Done');''')
            conn.commit()  # <--- makes sure the change is shown in the database
            conn.close()
            cur.close()
        except Exception as e:
            conn.close()
            cur.close()
            logging.log(logging.ERROR, e)


    def process_item(self, item, spider):
        try:
            #conn = psycopg2.connect(database=self.dbname, user=self.user, password=self.password, host=self.host, port="5432")
            conn = psycopg2.connect(database='postgres', user=self.user, password=self.password, host=self.host,port="5432")
            cur = conn.cursor()
            # sql  = "INSERT INTO dpscs_state_Links (MainLink,Name,Dob,InmateLink,Status) VALUES (%s,%s,%s,%s,%s)",(str(MainLink), str(Name), str(Dob), str(InmateLink), Status)
            # sql = "INSERT INTO dpscs_state_Links (MainLink,Name,Dob,InmateLink,Status) VALUES (str(MainLink), str(Name), str(Dob), str(InmateLink), Status)"
            #sql = "INSERT INTO dpscs_state_Data(id,InmateLink,first_name,last_name,inmate_number,race,gender,dob,incarceration_term,release_date,facility,active,hair_color,eye_color,image,state,last_updated,HTML_Save_Path_data) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(item['id'],item['InmateLink'],item['first_name'],item['last_name'],item['inmate_number'],item['race'],item['gender'],item['dob'],item['incarceration_term'],item['release_date'],item['facility'],item['active'],item['hair_color'],item['eye_color'],item['image'],item['state'],item['last_updated'],item['HTML_Save_Path_data'])
            #sql = "INSERT INTO dpscs_state_Data(InmateLink,first_name,last_name,inmate_number,race,gender,dob,incarceration_term,release_date,facility,active,hair_color,eye_color,image,state,last_updated,HTML_Save_Path_data) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(str(item['InmateLink']),str(item['first_name']),str(item['last_name']),str(item['inmate_number']),str(item['race']),str(item['gender']),str(item['dob']),str(item['incarceration_term']),str(item['release_date']),str(item['facility']),str(item['active']),str(item['hair_color']),str(item['eye_color']),str(item['image']),str(item['state']),str(item['last_updated']),str(item['HTML_Save_Path_data']))
            #cur.execute(sql)
            #cur.execute("INSERT INTO dpscs_state_Links (MainLink,Name,Dob,InmateLink,Status) VALUES (" + "'" + str(MainLink) + "'" + ", " + "'" + str(Name) + "'" + ", " + "'" + str(Dob) + "'" + ", " + "'" + str(InmateLink) + "'" + ", " + "'" + Status + "'" + ")");
            cur.execute("INSERT INTO " + self.tableName + " (InmateLink,first_name,last_name,inmate_number,race,gender,dob,incarceration_term,release_date,facility,active,hair_color,eye_color,image,state,last_updated,Sid,MiddleName,HTML_Save_Path_data) VALUES (" + "'" + str(item['InmateLink']) + "'" + ", " + "'" + str(item['first_name']) + "'" + ", " + "'" + str(item['last_name']) + "'" + "," + "'" + str(item['inmate_number']) + "'" + "," + "'" + str(item['race']) + "'" + "," + "'" + str(item['gender']) + "'" + "," + "'" + str(item['dob']) + "'" + "," + "'" + str(item['incarceration_term']) + "'" + "," + "'" + str(item['release_date']) + "'" + "," + "'" + str(item['facility']) + "'" + "," + "'" + str(item['active']) + "'" + "," + "'" + str(item['hair_color']) + "'" + "," + "'" + str(item['eye_color']) + "'" + "," + "'" + str(item['image']) + "'" + "," + "'" + str(item['state']) + "'" + "," + "'" + str(item['last_updated']) + "'" + "," + "'" + str(item['Sid']) + "'" + "," + "'" + str(item['MiddleName']) + "'" + "," + "'" + item['HTML_Save_Path_data'] + "'" + ")");
            conn.commit()  # <--- makes sure the change is shown in the database
            conn.close()
            cur.close()
        except Exception as e:
            logging.log(logging.ERROR, e)
        return item
