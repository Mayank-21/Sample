# -*- coding: utf-8 -*-
import scrapy
import string
from KoolProductdata.items import KoolproductdataItem

class Spider19Spider(scrapy.Spider):
    name = 'spider19'
    allowed_domains = ['kool.corrections.ky.gov']
    start_urls = ['http://kool.corrections.ky.gov/']

    def parse(self, response):
        # profile = "http://kool.corrections.ky.gov/KOOL/Details/455073"
        # # profile = "http://kool.corrections.ky.gov/KOOL/Details/489024"
        #
        # # profile = "http://kool.corrections.ky.gov/KOOL/Details/263929"
        # yield scrapy.FormRequest(method="GET", url=profile, callback=self.ScrapProfile)
        search_list = list(string.ascii_lowercase)
        try:
            for search in search_list:
                url = "http://kool.corrections.ky.gov/?sortOrder=Last%20Name%2C%20First%20Name&lastName=" + search + "&searchAliases=False&onlyPhotoRecords=False&showAdvancedOptions=False&returnResults=True"
                yield scrapy.FormRequest(url=url, method="GET", callback=self.result, meta={'val': search})
        except Exception as e:
            print e

    def result(self, response):

        pgNum = str(response.xpath("//div[@id='Paging']/span/text()").extract_first()).strip()
        pgNum = pgNum.split(" ")[1]
        # fileName = "HTML\\pages\\" + str(response.meta['val']) + "_" + pgNum + ".html"
        # f = open(fileName, "w")
        # f.write(response.body)
        # f.close()
        # print response

        table = response.xpath("//table[@id = 'searchResults']/tr")
        for tr in table:
            profile = tr.xpath("./td/a/@href").extract_first()
            if profile != None:
                profile = "http://kool.corrections.ky.gov" + profile
                yield scrapy.FormRequest(method="GET", url=profile, callback=self.ScrapProfile)
        try:
            nextPagelist = response.xpath("//span[@id = 'PagingControls']/a")
            for nextPage in nextPagelist:
                tmp_nextPage = str(nextPage.xpath("./text()").extract_first()).lower()
                if "next" in tmp_nextPage:
                    nextPage = "http://kool.corrections.ky.gov" + nextPage.xpath("./@href").extract_first()
                    yield scrapy.FormRequest(url=nextPage, method="GET", callback=self.result, meta=response.meta)
        except Exception as e:
            print e

    def ScrapProfile(self, response):

        item = KoolproductdataItem()

        try:
            # fileName = "HTML\\person\\" + str(response.url).split("/")[-1] + ".html"
            # f = open(fileName, "w")
            # f.write(response.body)
            # f.close()
            # print response

            inmate_Link = response.url

            try:
                Name = response.xpath("//div[@class = 'pageCenteredDiv']/table/tr[1]/td[2]/div/text()").extract_first()
                Name = Name.strip()
                inmate_number = str(response.xpath(
                    "//div[@class = 'pageCenteredDiv']/table/tr[2]/td[2]/div/text()").extract_first()).strip()
                Start_Date = str(response.xpath(
                    "//div[@class = 'pageCenteredDiv']/table/tr[3]/td[2]/div/text()").extract_first()).strip()
                End_Date = str(response.xpath(
                    "//div[@class = 'pageCenteredDiv']/table/tr[4]/td[2]/div/text()").extract_first()).strip()
                if End_Date == '':
                    End_Date = str(response.xpath(
                        "//div[@class = 'pageCenteredDiv']/table/tr[4]/td[2]/div/span/text()").extract_first()).strip()
                race = str(response.xpath(
                    "//tr/td[contains(text(),'Race')]/following-sibling::td/div/text()").extract_first()).strip()
                Location = str(response.xpath(
                    "//tr/td[contains(text(),'Location')]/following-sibling::td/div/text()").extract_first()).strip()
                gender = str(response.xpath(
                    "//tr/td[contains(text(),'Gender')]/following-sibling::td/div/text()").extract_first()).strip()
                hair_color = str(response.xpath(
                    "//tr/td[contains(text(),'Hair Color')]/following-sibling::td/div/text()").extract_first()).strip()
                eye_color = str(response.xpath(
                    "//tr/td[contains(text(),'Eye Color')]/following-sibling::td/div/text()").extract_first()).strip()
                age = str(response.xpath(
                    "//tr/td[contains(text(),'Age')]/following-sibling::td/div/text()").extract_first()).strip()
                height = str(response.xpath(
                    "//tr/td[contains(text(),'Height')]/following-sibling::td/div/text()").extract_first()).strip()
                if "None" not in height:
                    height = str(height).replace("\r\n", "")
                    height = str(height).replace("\\", "")
                    height = str(height).replace('"', "")
                    while "  " in height:
                        height = height.replace("  ", "")
                weight = str(response.xpath(
                    "//tr/td[contains(text(),'Weight')]/following-sibling::td/div/text()").extract_first()).strip()
                Risk_Assessment_Rating = str(response.xpath(
                    "//tr/td[contains(text(),'Risk Assessment Rating')]/following-sibling::td/div/text()").extract_first()).strip()
                imgUrl = str(response.xpath("//div[@id='photoDiv']/div/a/@href").extract_first()).strip()
                if "Content" in imgUrl:
                    imgUrl = "http://kool.corrections.ky.gov" + imgUrl
                else:
                    imgUrl = "No Photo Available"

                ConvictionInformation = []
                aval = response.xpath("//div[@class = 'pageCenteredDiv']/div[2]/table/tr/td").extract_first()

                if "Conviction information unavailable" not in aval:

                    aval = response.xpath("//div[@class = 'pageCenteredDiv']/div[2]/table/tr/td")

                    for ava in aval:
                        dataList = ava.xpath("./text()").extract()
                        for data in dataList:
                            data = str(data).replace("\r\n", "")
                            while "  " in data:
                                data = data.replace("  ", "")
                            if data != "(":
                                if data != " )":
                                    ConvictionInformation.append(data)

                    ConvictionInformation = "|".join(ConvictionInformation)
                else:
                    ConvictionInformation = ""

                payrle_info = []
                payrle = ""
                tmp_payroleinfo = response.xpath("//div[@class = 'pageCenteredDiv']/div[4]/table").extract()
                tmp_payroleinfo = "".join(tmp_payroleinfo)
                if "No parole information found for this offender" not in tmp_payroleinfo:
                    for i in range(1, 6):
                        tmp1 = str(response.xpath("//div[@class = 'pageCenteredDiv']/div[4]/table/tr[1]/th[" + str(
                            i) + "]/text()").extract_first()).strip()
                        tmp2 = str(response.xpath("//div[@class = 'pageCenteredDiv']/div[4]/table/tr[2]/td[" + str(
                            i) + "]/text()").extract_first()).strip()
                        if "None" not in tmp1:
                            if "None" not in tmp2:
                                payrle_info.append(tmp1 + ":" + tmp2)

                    payrle_info = "|".join(payrle_info)

                else:
                    payrle_info = ""

                item['Name'] = Name
                item['inmate_number'] = inmate_number
                item['Start_Date'] = Start_Date
                item['End_Date'] = End_Date
                item['race'] = race
                item['gender'] = gender
                item['hair_color'] = hair_color
                item['eye_color'] = eye_color
                item['age'] = age
                item['height'] = height
                item['weight'] = weight
                item['Risk_Assessment_Rating'] = Risk_Assessment_Rating
                item['imgUrl'] = imgUrl
                item['ConvictionInformation'] = ConvictionInformation
                item['payrle_info'] = payrle_info
                item['Location'] = Location
                yield item
            except Exception as e:
                print e

        except Exception as e:
            print e
