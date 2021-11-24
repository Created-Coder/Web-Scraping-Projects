import scrapy
import csv


class martSpider(scrapy.Spider):
    name = "bot"

    links_list = []

    with open("G:/downmart/downmart/downmart/spiders/Links.csv", 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            for i in row:
                links_list.append(i)

    new_list = []
    for i in links_list:
        new_list.append(i.replace("https", "http"))

    start_urls = new_list

    # def parse(self,response):
    #     links = response.xpath("//div[@class='grid__cell 1/2--tablet 1/3--lap-and-up']/a/@href").extract()
    #     for i in links:
    #         link = "https://domomart.ie" + i
    #         yield scrapy.Request(url=link, callback=self.parse2)

    def parse(self,response):
        prds = response.xpath("//div[@class='product-item product-item--vertical  1/3--tablet-and-up 1/4--desk']/a/@href").extract()
        for i in prds:
            print("https://domomart.ie" + i)