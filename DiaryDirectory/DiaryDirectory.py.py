import scrapy
from selenium import webdriver
import json
import csv
from scrapy.http import FormRequest
import time
from csv import writer
import urllib.request
import os

class DedroneSpider(scrapy.Spider):
    name = "directory"

    links_list = []

    with open('G:/diarydirectory/links_BrandNames.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            for i in row:
                links_list.append(i)

    start_urls = links_list

    def parse(self, response):

        contact_name_1 = None
        contact_sub_title_1 = None
        contact_no_1 = None
        contact_email_1 = None

        contact_name_2 = None
        contact_sub_title_2 = None
        contact_no_2 = None
        contact_email_2 = None

        contact_name_3 = None
        contact_sub_title_3 = None
        contact_no_3 = None
        contact_email_3 = None

        try:
            name = response.xpath("//h3[@class='page-title page-title-text']/text()").get()
            name = name.strip()

        except:
            pass

        # Contact Detail 1
        try:
            contact_name_1 = response.xpath("//div[@class='contact-loop show-contact-loop'][1]//h6/text()").get()

        except Exception as e:
            print(e)
            contact_name_1 = " "
            pass

        try:
            contact_sub_title_1 = response.xpath("//div[@class='contact-loop show-contact-loop'][1]/div/div[1]/p/text()").get()

        except Exception as e:
            print(e)
            contact_sub_title_1 = " "
            pass

        try:
            contact_no_1 = response.xpath("//div[@class='contact-loop show-contact-loop'][1]/div/div[2]/p[1]/a/@href").get()
            contact_no_1 = contact_no_1.split(":")
            contact_no_1 = contact_no_1[1]

        except Exception as e:
            print(e)
            contact_no_1 = " "
            pass

        try:
            contact_email_1 = response.xpath("//div[@class='contact-loop show-contact-loop'][1]/div/div[2]/p[2]/a/@href").get()
            contact_email_1 = contact_email_1.split(":")
            contact_email_1 = contact_email_1[1]

        except Exception as e:
            print(e)
            contact_email_1 = " "
            pass

        # Contact Detail 2

        try:
            contact_name_2 = response.xpath("//div[@class='contact-loop show-contact-loop'][2]//h6/text()").get()

        except Exception as e:
            print(e)
            contact_name_2 = " "
            pass

        try:
            contact_sub_title_2 = response.xpath("//div[@class='contact-loop show-contact-loop'][2]/div/div[1]/p/text()").get()

        except Exception as e:
            print(e)
            contact_sub_title_2 = " "
            pass

        try:
            contact_no_2 = response.xpath("//div[@class='contact-loop show-contact-loop'][2]/div/div[2]/p[1]/a/@href").get()
            contact_no_2 = contact_no_2.split(":")
            contact_no_2 = contact_no_2[1]

        except Exception as e:
            print(e)
            contact_no_2 = " "
            pass

        try:
            contact_email_2 = response.xpath("//div[@class='contact-loop show-contact-loop'][2]/div/div[2]/p[2]/a/@href").get()
            contact_email_2 = contact_email_2.split(":")
            contact_email_2 = contact_email_2[1]

        except Exception as e:
            print(e)
            contact_email_2 = " "
            pass

            # Contact Detail 3

            try:
                contact_name_3 = response.xpath("//div[@class='contact-loop show-contact-loop'][3]//h6/text()").get()

            except Exception as e:
                print(e)
                contact_name_3 = " "
                pass

            try:
                contact_sub_title_3 = response.xpath(
                    "//div[@class='contact-loop show-contact-loop'][3]/div/div[1]/p/text()").get()

            except Exception as e:
                print(e)
                contact_sub_title_3 = " "
                pass

            try:
                contact_no_3 = response.xpath(
                    "//div[@class='contact-loop show-contact-loop'][3]/div/div[2]/p[1]/a/@href").get()
                contact_no_3 = contact_no_3.split(":")
                contact_no_3 = contact_no_3[1]

            except Exception as e:
                print(e)
                contact_no_3 = " "
                pass

            try:
                contact_email_3 = response.xpath(
                    "//div[@class='contact-loop show-contact-loop'][3]/div/div[2]/p[2]/a/@href").get()
                contact_email_3 = contact_email_3.split(":")
                contact_email_3 = contact_email_3[1]

            except Exception as e:
                print(e)
                contact_email_3 = " "
                pass

        yield {
            "Name" : name,

            "Contact Name 1" : contact_name_1,
            "Contact Sub Title 1" : contact_sub_title_1,
            "Contact Number 1" : contact_no_1,
            "Contact Email 1" : contact_email_1,

            "Contact Name 2": contact_name_2,
            "Contact Sub Title 2": contact_sub_title_2,
            "Contact Number 2": contact_no_2,
            "Contact Email 2": contact_email_2,

            "Contact Name 3": contact_name_3,
            "Contact Sub Title 3": contact_sub_title_3,
            "Contact Number 3": contact_no_3,
            "Contact Email 3": contact_email_3
        }

