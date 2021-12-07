import scrapy
import urllib.request
#from scraper_api import ScraperAPIClient
import os
import re
from datetime import datetime

#client = ScraperAPIClient('eedf935a9a6fec5ad78458600c3442bb')


class EbaySpider(scrapy.Spider):
    name = "ebay"
    start_urls = (
        'https://www.google.com/',
    )

    def parse(self, response):
        url='https://www.ebay-kleinanzeigen.de/s-musikinstrumente/seite:1/c74'
        proxy = 'olivier666:CzsucsMgi2cS8t8y@proxy.packetstream.io:31112'
        yield scrapy.Request(url,meta={'proxy': 'http://{0}'.format(proxy)}, callback=self.parse_main)

    def parse_main(self, response):
        proxy = 'olivier666:CzsucsMgi2cS8t8y@proxy.packetstream.io:31112'
        listing = response.xpath("//a[@class='ellipsis']/@href")
        for i in listing:
            comp_url = "https://www.ebay-kleinanzeigen.de" + i.extract()
            # yield scrapy.Request(client.scrapyGet(url=comp_url), self.parse2)
            yield scrapy.Request(comp_url,meta={'proxy': 'http://{0}'.format(proxy)}, callback=self.parse2)

        for i in range(2, 51):
            url = "https://www.ebay-kleinanzeigen.de/s-musikinstrumente/seite:{0}/c74".format(i)
            # yield scrapy.Request(client.scrapyGet(url=url), self.parse)
            yield scrapy.Request(url,meta={'proxy': 'http://{0}'.format(proxy)}, callback=self.parse_main)

            # next_page = response.xpath("//a[@class='pagination-next']/@href").get()
            # next_page = "https://www.ebay-kleinanzeigen.de" + next_page
            # yield scrapy.Request(client.scrapyGet(url=next_page), self.parse)

    def parse2(self, response):
        proxy = 'olivier666:CzsucsMgi2cS8t8y@proxy.packetstream.io:31112'
        scraping_date = datetime.today().strftime('%Y/%m/%d')

        try:
            prd_title = response.xpath("//*[@id='viewad-title']/text()").get()
            invalid = '<>:"/\|?*., \n'
            for i in invalid:
                if i in prd_title:
                    prd_title = prd_title.replace(i, " ").strip()

        except:
            prd_title = None

        try:
            price_data = response.xpath("//h2[@id='viewad-price']//text()").get()
            if "\n" in price_data:
                price_data = price_data.replace("\n", "")
                price_data = price_data.strip()

            else:
                pass

        except:
            price_data = None

        price=None
        currency=None
        try:
            price_data = price_data.split()
            price = price_data[0]
            currency = price_data[1]
        except:
            yield scrapy.Request(response.url, meta={'proxy': 'http://{0}'.format(proxy)}, callback=self.parse2)

        try:
            address = response.xpath("(//div[@class='boxedarticle--details--full'])[1]//span//text()").extract()
            address = ' '.join([str(elem.replace("\n", "").strip()) for elem in address])

        except:
            address = None

        try:
            date = response.xpath("(//div[@id='viewad-extra-info']//span)[1]//text()").get()
            if "\n" in date:
                date = date.replace("\n", "")
                date = date.strip()

            else:
                pass

        except:
            date = None

        try:
            desc = response.xpath("//div[@id='viewad-description']/div/p//text()").getall()
            desc = '\n '.join([str(elem.replace("\n", "").strip()) for elem in desc])

        except:
            desc = None

        # try:
        #     detail = response.xpath("//span[@class='addetailslist--detail--value']//text()").get()
        #     if "\n" in detail:
        #         detail = detail.replace("\n", "")
        #         detail = detail.strip()
        #
        # except:
        #     detail = None

        try:
            delivery = response.xpath("//li[contains(text(), 'Versand')]/span/text()").get()
            if "\n" in delivery:
                delivery = delivery.replace("\n", "")
                delivery = delivery.strip()

        except:
            delivery = None

        # try:
        #     seller = response.xpath("(//span[contains(text(), 'Nutzer')]/text())[1]").get()
        #     if "\n" in seller:
        #         seller = seller.replace("\n", "")
        #         seller = seller.strip()
        #
        # except:
        #     seller = None

        try:
            dateMembership = response.xpath("(//span[contains(text(), 'Nutzer')]/text())[2]").get()
            dateMembership = dateMembership.replace("Aktiv seit", "")
            if "\n" in dateMembership:
                dateMembership = dateMembership.replace("\n", "")
                dateMembership = dateMembership.strip()

        except:
            dateMembership = None

        try:
            adID = response.xpath("//div[@id='viewad-extra-info']/div[@class='align-right']/text()").get()
            adID = adID.replace("Anzeigennr.:", "")

        except:
            adID = None

        # try:
        #     src = response.xpath("(//img[@id='viewad-image'])[1]/@src").get()
        #     file_path = os.getcwd() + "/images/" + prd_title + ".jpg"
        #     urllib.request.urlretrieve(src, file_path)
        #
        # except:
        #     pass
        if price:
            yield {
                "Scraping Date": scraping_date,
                "title": prd_title,
                "price": price,
                "Currency": currency,
                "address": address,
                "date": date,
                "description": desc,
                'Delivery Option': delivery,
                # "Seller" : seller,
                "Date of Membership": dateMembership,
                "Ad ID": adID,
                "Image URL": '',
                # "Image Local Path" : file_path

            }
            #print(data)

