# -*- coding: utf-8 -*-
import scrapy
from maine_gov.items import MaineGovItem
from maine_gov.ReusableFunctions import Replace_ExtraChar,Scrape_BetweenString,Scrape_BetweenStringWithReplace
from maine_gov.CreateFolder import FolderCreate
import logging
import datetime
import os
from pathlib import Path
from bs4 import BeautifulSoup
import requests
import logging
import re



class MaineGovCrawlerSpider(scrapy.Spider):
    Current_Project_Path = os.path.dirname(os.path.abspath(__file__))
    timestamp = datetime.datetime.today().strftime('%d_%m_%Y')
    FolderCreate(Current_Project_Path)
    Pageread = True
    PageSave = True
    name = 'maine_gov_crawler'
    allowed_domains = ['www1.maine.gov']
    start_urls = ['https://www1.maine.gov/']

    def parse(self, response):
        print response.headers
        ListSearchvalues = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        #ListSearchvalues = ['Z']
        for SearchValue in ListSearchvalues:
            #SearchValue = 'Z'
            IsNextPage = True
            Offset = 1
            Page = 1
            while IsNextPage == True:
                # Variable Declaration
                try :
                    MDOCNumber = ''
                    Name = ''
                    Image = ''
                    Status = ''
                    DateofBirth = ''
                    Race_Ethnicity = ''
                    Gender = ''
                    Earliest = ''
                    Possible = ''
                    ReleaseDate = ''
                    Location = ''
                except Exception as e:
                    logging.log(logging.ERROR, e)
                # ----------------------------Get PageSource of LinkPage
                try:
                    HTML_Save_Path_Link = ""
                    MainLink = ''
                    #NextPagelink = ''
                    TotalInmates = 0
                    HTML_Save_Path_Link = self.Current_Project_Path + '\\Htmls\\' + '\\HTML_Link\\' + str(
                        SearchValue) + '_' + str(Page) + '.html'
                    HTML_Save_Path_Link = str(HTML_Save_Path_Link).replace("\\\\", '\\')
                    print str(SearchValue) + '_' + str(Page)
                    filepath = Path(HTML_Save_Path_Link)
                    if filepath.exists() and self.Pageread == True:
                        f = open(HTML_Save_Path_Link, "r")
                        PageSource_Link = f.read()
                        BsObj_Link = BeautifulSoup(PageSource_Link, "lxml")
                    else:
                        if Page == 1:
                            MainLink = 'https://www1.maine.gov/cgi-bin/online/mdoc/search-and-deposit/search.pl?Search=Continue'
                            Headers = {'Host': 'www1.maine.gov',
                                       'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0',
                                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                       'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip, deflate',
                                       'Referer': 'https://www1.maine.gov/cgi-bin/online/mdoc/search-and-deposit/search.pl?Search=Continue',
                                       'Connection': 'keep-alive', 'Content-Type': 'application/x-www-form-urlencoded',
                                       'Content-Length': '221'}
                            data = {'mdoc_number': '', 'first_name': SearchValue, 'middle_name': '', 'last_name': '',
                                    'gender': '',
                                    'age_from': '', 'age_to': '', 'weight_from': '', 'weight_to': '', 'feet_from': '',
                                    'inches_from': '', 'feet_to': '', 'inches_to': '', 'eyecolor': '', 'haircolor': '',
                                    'race': '', 'mark': '', 'status': '', 'location': '', 'mejis_index': '',
                                    'submit': 'Search'}
                            r = requests.post(MainLink, data=data, headers=Headers)
                        else:
                            MainLink = NextPagelink
                            Cookie = ''
                            Cookie = 'mdoc=eyecolor&&status&&age_from&&order_by&mdoc_number&last_name&&mark&&inches_from&&haircolor&&weight_from&&race&&feet_to&&gender&&mejis_index&&location&&feet_from&&inches_to&&middle_name&&age_to&&weight_to&&mdoc_number&&start_limit&'+str(Offset)+'&first_name&' + SearchValue
                            Headers = {'Host': 'www1.maine.gov',
                                       'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0',
                                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                       'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip, deflate',
                                       'Referer': 'https://www1.maine.gov/cgi-bin/online/mdoc/search-and-deposit/search.pl',
                                       'Cookie': Cookie,
                                       'Connection': 'keep-alive'}
                            r = requests.get(MainLink, headers=Headers)

                        PageSource_Link = r.text
                        BsObj_Link = BeautifulSoup(PageSource_Link, "lxml")
                        if self.PageSave == True:
                            f = open(HTML_Save_Path_Link, 'w')
                            f.write(PageSource_Link)
                            f.close()
                    # PageSource_Link_json = json.loads(PageSource_Link)
                except Exception as e:
                    logging.log(logging.ERROR, e)

                # from lxml import html
                # tree = html.fromstring(PageSource_Link)
                # OfficersTitleList = tree.xpath('//td[(@class="OfficeHeld")]//text()')

                try:
                    TotalInmates = int(Scrape_BetweenString(PageSource_Link, '</strong> of <strong>', '</strong> '))
                except Exception as e:
                    logging.log(logging.ERROR, e)

                # ----------- Data extraction code
                try:
                    TableTag  = BsObj_Link.find("table", {"class" : "at-data-table"})
                except Exception as e:
                    logging.log(logging.ERROR, e)

                try:
                    trTags = TableTag.find_all('tr', class_=['at-row-dark', 'at-row-light'])
                except Exception as e:
                    logging.log(logging.ERROR, e)
                for trTag in trTags:
                    # --- Empty all variables
                    try:
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
                        HTML_Save_Path_data = ''
                        Strhtml = response.text
                        item = MaineGovItem()
                        LinkStatus = ''
                        Location = ''
                        Linkid = ''
                        Alias = ''
                        Age = ''
                        Weight_Pounds = ''
                        Height = ''
                        Scars_Marks_Tattoos = ''
                        Convictions = ''
                        ConditionsofSupervision = ''
                    except Exception as e:
                        # print e
                        logging.log(logging.ERROR, e)
                    try:
                        #print trTag
                        tdTags = trTag.find_all('td')
                        InmateLink = ''
                        inmatenumber = ''
                        Name = ''
                        image = ''
                        LinkStatus = ''
                        dob = ''
                        race = ''
                        gender = ''
                        release_date = ''
                        Location = ''
                        first_name = ''
                        last_name =''
                        inmatenumber = tdTags[0].text.strip()
                        InmateLink = 'https://www1.maine.gov/cgi-bin/online/mdoc/search-and-deposit/' + tdTags[0].find("a")['href']
                        Name = tdTags[1].text.strip()
                        if Name!=''  :
                            if ',' in Name:
                                first_name = Name.split(',',1)[1]
                                last_name = Name.split(',',1)[0]
                            else:
                                first_name = Name
                        image = 'https://www1.maine.gov' + tdTags[2].find("img")['src']
                        LinkStatus = tdTags[3].text.strip()
                        dob = tdTags[4].text.strip()
                        race = tdTags[5].text.strip()
                        gender = tdTags[6].text.strip()
                        release_date = tdTags[7].text.strip()
                        Location = tdTags[8].text.strip()

                    except Exception as e:
                        logging.log(logging.ERROR, e)

                    if InmateLink!='':
                        try:
                            print InmateLink
                            #InmateLink='https://www1.maine.gov/cgi-bin/online/mdoc/search-and-deposit/detail.pl?mdoc_number1=76915'
                            Linkid = InmateLink.split('mdoc_number1=', 1)[1]
                        except Exception as e:
                            # print e
                            logging.log(logging.ERROR, e)
                        try:
                            PageSource_Data = ''
                            BsObj_Data = ''
                            HTML_Save_Path_data = ''
                            HTML_Save_Path_data = self.Current_Project_Path + '\\Htmls\\' + '\\HTML_DataField\\' + str(Linkid) + '.html'
                            HTML_Save_Path_data = str(HTML_Save_Path_data).replace("\\\\", '\\')

                            filepath = Path(HTML_Save_Path_data)
                            if filepath.exists() and self.Pageread == True:
                                f = open(HTML_Save_Path_data, "r")
                                PageSource_Data = f.read()
                                BsObj_Data = BeautifulSoup(PageSource_Data, "lxml")
                            else:
                                response = requests.get(InmateLink)
                                PageSource_Data = response.text
                                PageSource_Data = Replace_ExtraChar(PageSource_Data)
                                BsObj_Data = BeautifulSoup(PageSource_Data, "lxml")
                                if self.PageSave == True:
                                    f = open(HTML_Save_Path_data, 'w')
                                    f.write(PageSource_Data)
                                    f.close()
                        except Exception as e:
                            # print e
                            logging.log(logging.ERROR, e)

                        try:
                            Alias = Scrape_BetweenString(PageSource_Data,'Alias or Aliases:</td>','</td>')
                        except Exception as e:
                            logging.log(logging.ERROR, e)
                        try:
                            Age = Scrape_BetweenString(PageSource_Data,'Age (Years):</td>','</td>')
                        except Exception as e:
                            logging.log(logging.ERROR, e)
                        try:
                            Weight_Pounds = Scrape_BetweenString(PageSource_Data,'Weight (Pounds):</td>','</td>')
                        except Exception as e:
                            logging.log(logging.ERROR, e)
                        try:
                            Height = Scrape_BetweenString(PageSource_Data,'Height:</td>','</td>')
                        except Exception as e:
                            logging.log(logging.ERROR, e)
                        try:
                            eye_color = Scrape_BetweenString(PageSource_Data, 'Eye Color:</td>', '</td>')
                        except Exception as e:
                            logging.log(logging.ERROR, e)
                        try:
                            hair_color = Scrape_BetweenString(PageSource_Data, 'Hair Color:</td>', '</td>')
                        except Exception as e:
                            logging.log(logging.ERROR, e)
                        try:
                            Scars_Marks_Tattoos = Scrape_BetweenString(PageSource_Data,'Scars, Marks, Tattoos: </td>','</td>')
                        except Exception as e:
                            logging.log(logging.ERROR, e)
                        try:
                            Temp_All = []
                            Temp_All = BsObj_Data.findAll("table", {"class" : "at-data-table"})
                        except Exception as e:
                            logging.log(logging.ERROR, e)
                        for temp in Temp_All:
                            if 'Convictions</th>' in str(temp) or 'Conditions of Supervision</th>' in str(temp):
                                try:
                                    TrTag_all = str(temp).split('<tr class="at-data-table-title">')
                                except Exception as e:
                                    logging.log(logging.ERROR, e)
                                try:
                                    Input = TrTag_all[2]
                                    Input = Input.replace('</tr>', '|')
                                    Convictions = Scrape_BetweenStringWithReplace(Input)
                                    #print Convictions
                                except Exception as e:
                                    logging.log(logging.ERROR, e)
                                try:
                                    Input = TrTag_all[3]
                                    Input = Input.replace('</td>', '|')
                                    ConditionsofSupervision = Scrape_BetweenStringWithReplace(Input)
                                    #print ConditionsofSupervision
                                except Exception as e:
                                    logging.log(logging.ERROR, e)
                        try:
                             item['id'] = id
                             item['InmateLink'] = InmateLink
                             item['first_name'] = first_name
                             item['last_name'] = last_name
                             item['inmate_number'] = inmatenumber
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
                             item['LinkStatus'] = LinkStatus
                             item['Location'] = Location
                             item['Alias'] = Alias
                             item['Age'] = Age
                             item['Weight_Pounds'] = Weight_Pounds
                             item['Height'] = Height
                             item['Scars_Marks_Tattoos'] = Scars_Marks_Tattoos
                             item['Convictions'] = Convictions
                             item['ConditionsofSupervision'] = ConditionsofSupervision
                             item['HTML_Save_Path_data'] = HTML_Save_Path_data
                             yield item
                        except Exception as e:
                            logging.log(logging.ERROR, e)

                        #yield scrapy.FormRequest(str(InmateLink), callback=self.Get_data, method='GET', meta={'inmatenumber': str(inmatenumber), 'first_name': first_name,'last_name': str(last_name), 'image': image,'LinkStatus': str(LinkStatus), 'dob': dob,'race': str(race), 'gender': gender,'release_date': str(release_date), 'Location': Location})

                #----------------------------check for next page
                try:
                    temp = ''
                    NextPagelink = ''
                    if '>Next' in PageSource_Link and '<a href="results.pl?' in PageSource_Link:
                        temp = PageSource_Link.split('>Next',1)[0].split('<a href="results.pl?')
                        NextPagelink ='https://www1.maine.gov/cgi-bin/online/mdoc/search-and-deposit/results.pl?'+ str(temp[len(temp)-1]).split('">Next',1)[0]
                except Exception as e:
                    logging.log(logging.ERROR, e)
                try:
                    #Offset = Offset + len(trTags)
                    if NextPagelink !='':
                        Page = Page + 1
                        IsNextPage = True
                        if Page > 2:
                            Offset = Offset + 30
                    else:
                        IsNextPage = False
                except Exception as e:
                    logging.log(logging.ERROR, e)
        pass

