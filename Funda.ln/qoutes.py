import scrapy
import datetime

from .. import items


class QouteSpider(scrapy.Spider):
    name = "qoutes"
    start_urls = ["https://www.funda.nl/en/koop/amsterdam/"]

    def parse(self, response):

        for i in response.xpath("//div[@class='search-result__header-title-col']/a[1]"):
            links = i.xpath(".//@href").extract()
            global comp_url
            comp_url = "https://www.funda.nl/"+links[0]

            yield response.follow(comp_url , callback=self.parse2)

        for i in range(2,272):
            next_page = ("https://www.funda.nl/en/koop/amsterdam/p{}".format(i))
            yield scrapy.Request(next_page, callback=self.parse)

    def parse2(self,response):

        custom_settings = {
            'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter',
        }

        energy = response.xpath("//dl[@class='object-kenmerken-list'][5]/dd/span/text()")


        yield {
            "Date" : datetime.date.today().strftime("%B %d, %Y"),
            "Url": comp_url,
            "Name": response.xpath("(//h1/span)[1]/text()").extract(),
            "Postal Code" : response.xpath("//h1//span[2]/text()").extract(),
            "City" : "Amsterdam",
            "Address" : list(map(str.strip, response.xpath("//dl[7]/dd[1]/text()").extract())),
            "Price" : response.xpath("//div/strong[@class='object-header__price']/text()").extract(),
            "Type of house" : list(map(str.strip, response.xpath("//dl[2]/dd[1]/text()").extract())),
            "Kind of build" : list(map(str.strip, response.xpath("//dl[2]/dd[2]/text()").extract())),
            "Year of build" : list(map(str.strip, response.xpath("//dl[2]/dd[3]/text()").extract())),
            "Roof kind": list(map(str.strip, response.xpath("//dl[2]/dd[4]/text()").extract())),
            "Living Area": list(map(str.strip, response.xpath("//dl[@class='object-kenmerken-list'][3]/dd//dd[1]/text()").extract())),
            "Outdoor Space": list(map(str.strip, response.xpath("//dl[@class='object-kenmerken-list'][3]/dd//dd[2]/text()").extract())),
            "External Space": list(map(str.strip, response.xpath("//dl[@class='object-kenmerken-list'][3]/dd//dd[3]/text()").extract())),
            "Plot": list(map(str.strip, response.xpath("//dl[@class='object-kenmerken-list'][3]/dd[3]/text()").extract())),
            "Volume": list(map(str.strip, response.xpath("//dl[@class='object-kenmerken-list'][3]/dd[4]/text()").extract())),
            "Rooms" : list(map(str.strip, response.xpath("//dl[@class='object-kenmerken-list'][4]/dd[1]/text()").extract())),
            "Bathrooms": list(map(str.strip, response.xpath("//dl[@class='object-kenmerken-list'][4]/dd[2]/text()").extract())),
            "Bathroom Facilty": list(map(str.strip, response.xpath("//dl[@class='object-kenmerken-list'][4]/dd[3]/text()").extract())),
            "Floors": list(map(str.strip, response.xpath("//dl[@class='object-kenmerken-list'][4]/dd[4]/text()").extract())),
            "Services": list(map(str.strip, response.xpath("//dl[@class='object-kenmerken-list'][4]/dd[5]/text()").extract())),
            "Energy Label" : list(map(str.strip, response.xpath("//dl[@class='object-kenmerken-list'][5]/dd[1]/text()").extract())),
            "Isolation" : list(map(str.strip, response.xpath("//dl[@class='object-kenmerken-list'][5]/dd[2]/text()").extract())),
            "Heating": list(map(str.strip, response.xpath("//dl[@class='object-kenmerken-list'][5]/dd[3]/text()").extract())),
            "Hot Water": list(map(str.strip, response.xpath("//dl[@class='object-kenmerken-list'][5]/dd[4]/text()").extract())),
            "Boiler": list(map(str.strip, response.xpath("//dl[@class='object-kenmerken-list'][5]/dd[5]/text()").extract())),
            "Boiler": list(map(str.strip, response.xpath("//dl[@class='object-kenmerken-list'][6]/dd[1]/text()").extract())),
            "Cadaster Area" : list(map(str.strip, response.xpath("//dl[@class='object-kenmerken-list'][6]/dd[2]/dl/dd[1]/text()").extract())),
            "Charger" : list(map(str.strip, response.xpath("//dl[@class='object-kenmerken-list'][6]/dd[2]/dl/dd[3]/text()").extract())),
            "Location" : list(map(str.strip, response.xpath("//dl[@class='object-kenmerken-list'][6]/dt/div/text()").extract())),
            "Garden" : list(map(str.strip, response.xpath("//dl[@class='object-kenmerken-list'][7]/dd[1]/text()").extract())),
            "Back Yard" : list(map(str.strip, response.xpath("//dl[@class='object-kenmerken-list'][7]/dd[2]/text()").extract())),
            "Garden location": list(map(str.strip, response.xpath("//dl[@class='object-kenmerken-list'][7]/dd[4]/text()").extract())),
            "Balcony" : list(map(str.strip, response.xpath("//dl[@class='object-kenmerken-list'][7]/dd[4]/text()").extract())),
            "Storage" : list(map(str.strip, response.xpath("//dl[@class='object-kenmerken-list'][8]/dd[1]/text()").extract())),
            "Storage Service": list(map(str.strip, response.xpath("//dl[@class='object-kenmerken-list'][8]/dd[2]/text()").extract())),
            "Parking": list(map(str.strip, response.xpath("//dl[@class='object-kenmerken-list'][9]/dd[1]/text()").extract())),
        }