import scrapy


class DedroneSpider(scrapy.Spider):
    name = "dedrone"

    start_urls = [
        "https://www.dedrone.com/resources/incidents/all"
    ]

    def parse(self, response):
        titles = response.xpath("//p[@class='paragraph incident-table-paragraph incident-name-paragraph']/text()").extract()
        links = response.xpath("//a[@class='paragraph incidents-article-link']/@href").extract()

        for i in range(len(titles)):
            yield{
                "Titles" : titles[i],
                "Links" : links[i]
            }


