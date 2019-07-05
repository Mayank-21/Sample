# -*- coding: utf-8 -*-
import scrapy
from kool_data.items import KoolDataItem
import logging

class KoolSpider(scrapy.Spider):
    name = 'kool'
    allowed_domains = ['doc.iowa.gov']
    start_urls = ['https://doc.iowa.gov/offender/search']

    def parse(self, response):
        #print response
        gender = ['M','F']

        combis = [i  for i in [chr(l) for l in range(ord('A'), ord('Z') + 1)]]
        #print(combis)
        for row in combis:
            for gen in gender:

                params = {'first_name':str(row),
                        'middle_name':'',
                        'last_name':'',
                        'dob_after[month]':'1',
                        'dob_after[day]':'1',
                        'dob_after[year]':'1900',
                        'dob_before[month]':'11',
                        'dob_before[day]':'21',
                        'dob_before[year]':'2018',
                        'gender':str(gen),
                        'offender_number':'',
                        'region':'All',
                        'offense':'',
                        'county':'-1',
                        'op':'Find',
                        'form_build_id':'form-mFUNbCb_o4q96KO8M1TnpAgI4H2bdBlDxIW37BTbn8k',
                        'form_id':'iowa_doc_offender_search_form'}
                yield scrapy.FormRequest('https://doc.iowa.gov/offender/search',
                    method='POST',formdata=params, callback=self.Get_link,dont_filter=True)

    def Get_link(self,response):

        All_Data = response.xpath("//table[@class='sticky-enabled']/tbody/tr")

        for j in range(0,len(All_Data)):
            Link_data = All_Data[j].xpath('.//td[1]/a/@href').extract_first()
            Link_data = Link_data.encode('utf8')
            if Link_data!= '':
                Link_data = 'https://doc.iowa.gov'+Link_data

            yield scrapy.FormRequest(Link_data,method='GET',callback=self.get_data)


    def get_data(self,response):
        print(response.url)
        item = KoolDataItem()
        def xpathdemo(xpath):
            Name = response.xpath('//td[contains(text(), "'+str(xpath)+'")]/following::td[1]/text()').extract_first()
            if Name != None:
                Name = str(Name.encode('ascii', 'ignore')).replace('\n', '').replace('\r', '').strip()
            else:
                Name = ''
            return Name
        def checknone(passnone):
            if passnone != None:
                passnone = str(passnone.encode('ascii', 'ignore')).replace('\n', '').replace('\r', '').strip()
            else:
                passnone = ''
            return passnone

        try:

            Name = xpathdemo('Name')
            Offender_Number = xpathdemo('Offender Number')
            Sex = xpathdemo('Sex')
            Birth_Date = xpathdemo('Birth Date')
            Location = xpathdemo('Location')
            Offense = xpathdemo('Offense')
            TDD_SDD = xpathdemo('TDD/SDD *')
            Commitment_Date = xpathdemo('Commitment Date')
            Recall_Date = xpathdemo('Recall Date')
            Mandatory_Minimum = xpathdemo('Mandatory Minimum (if applicable)')

            All_detail = response.xpath('//h3[contains(text(), "Charges")]/following::table/tr')

            for k in range(0,len(All_detail)):
                Supervision_Status = All_detail[k].xpath('.//td[1]/text()').extract_first()
                Supervision_Status = checknone(Supervision_Status)
                Offense_Class = All_detail[k].xpath('.//td[2]/text()').extract_first()
                Offense_Class = checknone(Offense_Class)
                County_of_Commitment = All_detail[k].xpath('.//td[3]/text()').extract_first()
                County_of_Commitment = checknone(County_of_Commitment)
                End_Date = All_detail[k].xpath('.//td[4]/text()').extract_first()
                End_Date = checknone(End_Date)
                item['InmateLink'] = response.url
                item['first_name'] = Name
                item['last_name'] = ''
                item['inmate_number'] = Offender_Number
                item['race'] = ''
                item['gender'] = Sex
                item['dob'] = Birth_Date
                item['incarceration_term'] = ''
                item['release_date'] = ''
                item['facility'] = ''
                item['active'] = ''
                item['hair_color'] = ''
                item['eye_color'] = ''
                item['image'] = ''
                item['state'] = ''
                item['last_updated'] = ''
                item['Location'] = Location
                item['Offense'] = Offense
                item['TDD_SDD'] = TDD_SDD
                item['Commitment_Date'] = Commitment_Date
                item['Recall_Date'] = Recall_Date
                item['Mandatory_Minimum'] = Mandatory_Minimum
                item['Supervision_Status'] = Supervision_Status
                item['Offense_Class'] = Offense_Class
                item['County_of_Commitment'] = County_of_Commitment
                item['End_Date'] = End_Date
                yield item
        except Exception as e:
            logging.log(logging.ERROR, e)





