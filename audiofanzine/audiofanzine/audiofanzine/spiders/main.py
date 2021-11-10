import scrapy
import urllib.request
import os

class MusicaleSpider(scrapy.Spider):
    name = "audio"

    start_urls = ['https://fr.audiofanzine.com/basse/petites-annonces/o.particuliers.html',
                  'https://fr.audiofanzine.com/batterie/petites-annonces/o.particuliers.html',
                  'https://fr.audiofanzine.com/dj/petites-annonces/o.particuliers.html',
                  'https://fr.audiofanzine.com/guitare/petites-annonces/o.particuliers.html',
                  'https://fr.audiofanzine.com/synthetiseur/petites-annonces/o.particuliers.html',
                  'https://fr.audiofanzine.com/sono/petites-annonces/o.particuliers.html',
                  'https://fr.audiofanzine.com/mao/petites-annonces/o.particuliers.html',
                  'https://fr.audiofanzine.com/homestudio/petites-annonces/o.particuliers.html',
                  'https://fr.audiofanzine.com/instrument-musique/petites-annonces/o.particuliers.html',
                  'https://fr.audiofanzine.com/produits-divers/petites-annonces/o.particuliers.html']

    def parse(self, response):
        listing = response.xpath("//a[@class='link-wrapper']/@href").extract()

        for i in listing:
            comp_url = "https://fr.audiofanzine.com" + i

            global pagination_page

            pagination_page = response.xpath("//ul[@class='paginator']//li[2]/a/@href").get()
            pagination_page = pagination_page.split('2')[0]

            yield scrapy.Request(comp_url, self.parse2)

        for i in range(2,51):
            url = pagination_page + str(i) + ".html"
            url = "https://fr.audiofanzine.com" + url
            yield scrapy.Request(url, self.parse)

    def parse2(self, response):
        try:
            current_url = response.url
            prd_title = response.xpath("//h1/text()").get()
            invalid = '<>:"/\|?*, '

            for i in invalid:
                if i in prd_title:
                    prd_title = prd_title.replace(i, " ")

        except:
            prd_title = None


        try:
            category = response.xpath("//nav[@id='breadcrumb']//li[3]//text()").get()

        except:
            category = None

        try:
            price = response.xpath("//div[@class='classified-price']//text()").get()
            price = price.replace("\xa0", " ")

        except:
            price = None

        try:
            address = response.xpath("//div[@class='classified-localization']//text()").get()
            address = address.strip()
            address = " ".join(address.split())

        except:
            address = None

        try:
            date = response.xpath("//div[@class='wrap-subtitle']//text()").get()
            date = date.split("-")[0]
            date = date.replace("Posté le ", "")
            date = date.strip()

        except:
            date = None


        try:
            desc = response.xpath("//div[@class='classified-content-description']//text()").extract()
            desc = '\n '.join([str(elem) for elem in desc])
            desc = desc.replace("Description", "")
            desc = desc.replace("\r\n", "")
            desc = desc.strip()

        except:
            desc = None

        try:
            src =  response.xpath("//div[@class='wrap-classified-image ']//img/@src").get()
            urllib.request.urlretrieve(src, os.getcwd() + "/images/" + prd_title + ".jpg")

        except:
            pass


        yield{
            "title": prd_title,
            "category" : category,
            "price": price,
            "Location": address,
            "Posted date of the ad": date,
            "description": desc,
            "URL of ad" :  current_url,
            "Image URL": src,
            "Image Local Path": os.getcwd() + "/images/" + prd_title + ".jpg"
        }



