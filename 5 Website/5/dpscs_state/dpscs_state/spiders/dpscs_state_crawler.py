# -*- coding: utf-8 -*-
import scrapy
from dpscs_state.items import DpscsStateItem
from dpscs_state.ReusableFunctions import Replace_ExtraChar,Scrape_BetweenString
from dpscs_state.CreateFolder import FolderCreate
import logging
import datetime
import os
from pathlib import Path
from bs4 import BeautifulSoup
import requests


class DpscsStateCrawlerSpider(scrapy.Spider):
    Current_Project_Path = os.path.dirname(os.path.abspath(__file__))
    timestamp = datetime.datetime.today().strftime('%d_%m_%Y')
    FolderCreate(Current_Project_Path)
    Pageread = False
    PageSave = True
    name = 'dpscs_state_crawler'
    allowed_domains = ['www.dpscs.state.md.us']
    start_urls = ['http://www.dpscs.state.md.us/']

    def parse(self, response):
        #print response.body
        ListSearchvalues = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        #ListSearchvalues = ['Z']
        for SearchValue in ListSearchvalues:
            #SearchValue = 'Z'
            IsNextPage = True
            Offset = 0
            Page = 1
            while IsNextPage == True:
                # ----------------------------Get PageSource of LinkPage
                try:
                    HTML_Save_Path_Link = ""
                    MainLink = 'http://www.dpscs.state.md.us/inmate/search.do?searchType=name&lastnm=&firstnm=' + str(SearchValue) + '&start=' + str(Offset)
                    HTML_Save_Path_Link = self.Current_Project_Path + '\\Htmls\\' + '\\HTML_Link\\' + str(SearchValue) + '_' + str(Page) + '.html'
                    HTML_Save_Path_Link = str(HTML_Save_Path_Link).replace("\\\\", '\\')
                    print str(SearchValue) + '_' + str(Page)
                    filepath = Path(HTML_Save_Path_Link)
                    if filepath.exists() and self.Pageread == True:
                        f = open(HTML_Save_Path_Link, "r")
                        PageSource_Link = f.read()
                        BsObj_Link = BeautifulSoup(PageSource_Link, "lxml")
                    else:
                        r = requests.get(MainLink)
                        PageSource_Link = r.text
                        BsObj_Link = BeautifulSoup(PageSource_Link, "lxml")
                        if self.PageSave == True:
                            f = open(HTML_Save_Path_Link, 'w')
                            f.write(PageSource_Link)
                            f.close()
                    # PageSource_Link_json = json.loads(PageSource_Link)
                except Exception as e:
                    logging.log(logging.ERROR, e)
                TotalInmates = int(Scrape_BetweenString(PageSource_Link, 'Total Inmate Found:', '</td>'))

                try:
                    trTags = BsObj_Link.find_all('tr', class_=['trDataRowEven', 'trDataRowOdd'])
                except Exception as e:
                    logging.log(logging.ERROR, e)
                for trTag in trTags:
                    try:
                        #print trTag
                        tdTags = trTag.find_all('td')
                        Name = ''
                        Dob = ''
                        InmateLink = ''
                        Name = tdTags[1].text
                        Dob = tdTags[2].text
                        InmateLink = 'http://www.dpscs.state.md.us/inmate/' + tdTags[1].find("a")['href']
                    except Exception as e:
                        logging.log(logging.ERROR, e)
                    if InmateLink!='':
                        yield scrapy.FormRequest(str(InmateLink), callback=self.Get_data, method='GET', meta={'Name': str(Name), 'Dob': Dob})

                # ----------------------------check for next page
                try:
                    Offset = Offset + len(trTags)
                    if Offset < TotalInmates:
                        Page = Page + 1
                        IsNextPage = True
                    else:
                        IsNextPage = False
                except Exception as e:
                    logging.log(logging.ERROR, e)
        pass

    def Get_data(self, response):

        if 'class="borderStyle">' in response.text:
            # --- Empty all variables
            try :
                id = ''
                InmateLink = ''
                first_name = ''
                last_name = ''
                inmate_number = ''
                race = ''
                gender = ''
                dob = ''
                incarceration_term = ''
                release_date = ''
                facility = ''
                active = ''
                hair_color = ''
                eye_color = ''
                image = ''
                state = ''
                last_updated = ''
                HTML_Save_Path = ''
                Strhtml = response.text
                item = DpscsStateItem()
                Sid = ''
                MiddleName = ''
            except Exception as e:
                #print e
                logging.log(logging.ERROR, e)
            # --- Url,Name,Dob
            try:
                InmateLink = response.url
                print InmateLink
                Name = response.meta['Name']
                Dob = response.meta['Dob']
                Linkid = InmateLink.split('&id=',1)[1].strip()
            except Exception as e:
                #print e
                logging.log(logging.ERROR, e)
            try:
                PageSource_Data = ''
                BsObj_Data = ''
                HTML_Save_Path_data = ''
                HTML_Save_Path_data = self.Current_Project_Path + '\\Htmls\\' + '\\HTML_DataField\\' + str(Linkid) + '.html'
                HTML_Save_Path_data = str(HTML_Save_Path_data).replace("\\\\", '\\')
                PageSource_Data = response.text
                PageSource_Data = Replace_ExtraChar(PageSource_Data)
                BsObj_Data = BeautifulSoup(PageSource_Data, "lxml")
                if self.PageSave == True:
                    f = open(HTML_Save_Path_data, 'w')
                    f.write(PageSource_Data)
                    f.close()
            except Exception as e:
                #print e
                logging.log(logging.ERROR, e)
            try:
                TableTag = BsObj_Data.find("table", {"class": "borderStyle"})
                TrTags = TableTag.findAll("tr")

                TdTags_1 = TrTags[1].findAll("td")
                Sid = TdTags_1[0].text.strip()
                last_name = TdTags_1[1].text.strip()
                first_name = TdTags_1[2].text.strip()
                MiddleName = TdTags_1[3].text.strip()
                dob = TdTags_1[4].text.strip()

                TdTags_2 = TrTags[3].findAll("td")
                inmate_number = TdTags_2[0].text.strip()
                facility = str(TdTags_2[1])
                facility = facility.replace("&nbsp;", "")
                facility =TdTags_2[1].text.strip()
                facility = facility.replace('\n',';')
                facility = facility.replace('\r', '')
                while ';;' in facility:
                    facility = facility.replace(';;', ';')
            except Exception as e:
                # print e
                logging.log(logging.ERROR, e)

        # --- import all data-field into item-dictionary & DataTable
        try:
            #item['id'] = id
            item['InmateLink'] = InmateLink
            item['first_name'] = first_name
            item['last_name'] = last_name
            item['inmate_number'] = inmate_number
            item['race'] = race
            item['gender'] = gender
            item['dob'] = dob
            item['incarceration_term'] = incarceration_term
            item['release_date'] = release_date
            item['facility'] = facility
            item['active'] = active
            item['hair_color'] = hair_color
            item['eye_color'] = eye_color
            item['image'] = image
            item['state'] = state
            item['last_updated'] = last_updated
            item['Sid'] = Sid
            item['MiddleName'] = MiddleName
            item['HTML_Save_Path_data'] = HTML_Save_Path_data
            yield item
            #Export_csv(Current_Directory)
        except Exception as e:
            ##print e
            logging.log(logging.ERROR, e)


