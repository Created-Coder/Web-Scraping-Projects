import xlrd
import time
from datetime import datetime
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import shutil
from csv import writer
import urllib.request
import csv
import os
import pandas as pd
from csv import DictWriter
from selenium.common.exceptions import TimeoutException
from datetime import date

file = "inputExpedia.xlsx"
book = xlrd.open_workbook(file)

sh = book.sheet_by_index(0)
cols = sh.ncols
# print("Colums" + cols)

rows = sh.nrows
# print("Rowrows)

data = []
for j in range(1, rows):
    date_values = xlrd.xldate_as_tuple(sh.cell(j, 3).value, datemode=book.datemode)
    comp_date_pickup = date_values[:3]

    pickup_year = date_values[:3][0]
    pickup_month = date_values[:3][1]
    pickup_date = date_values[:3][2]

    date_values = xlrd.xldate_as_tuple(sh.cell(j, 4).value, datemode=book.datemode)
    comp_date_dropoff = date_values[:3]

    dropoff_year = date_values[:3][0]
    dropoff_month = date_values[:3][1]
    dropoff_date = date_values[:3][2]

    data.append({
        'Pick Up': sh.cell(j, 0).value,
        "Drop Off": sh.cell(j, 1).value,
        "Pick Up Year": pickup_year,
        "Pick Up Month": pickup_month,
        "Pick Up Date": pickup_date,
        "Drop Off Year": dropoff_year,
        "Drop Off Month": dropoff_month,
        "Drop Off Date": dropoff_date,
        "State": sh.cell(j, 2).value
    })

driver = webdriver.Chrome(executable_path='C:/Users/92324/Downloads/chromedriver/chromedriver.exe')
for i in data:
    pickup = i["Pick Up"]
    pickup_date = i['Pick Up Date']
    pickup_month = i['Pick Up Month']
    pickup_year = i["Pick Up Year"]

    dropoff = i["Drop Off"]
    dropoff_date = i["Drop Off Date"]
    dropoff_month = i["Drop Off Month"]
    dropoff_year = i["Drop Off Year"]

    dropoff_diff = date(dropoff_year, dropoff_month, dropoff_date)
    pickup_diff = date(pickup_year, pickup_month, pickup_date)

    state = i['State']

    url = "https://www.expedia.com/carsearch?locn=" + pickup + "&loc2=" + dropoff + "&date1=" + str(
        pickup_month) + "%2F" + str(pickup_date) + "%2F" + str(pickup_year) + "&date2=" + str(
        dropoff_month) + "%2F" + str(dropoff_date) + "%2F" + str(dropoff_year) + "&d1=" + str(pickup_year) + "-" + str(
        pickup_month) + "-" + str(pickup_date) + "&d2=" + str(dropoff_year) + "-" + str(dropoff_month) + "-" + str(
        dropoff_date) + "&aarpcr=off&vend=&pickupIATACode=&dpln=6339943&returnIATACode=&drid1=6339943&time1=1030AM&time2=1030AM&dagv=1&subm=1&fdrp=0&ttyp=2&acop=2&rdus=10&rdct=1&styp=4"

    driver.get(url)
    current_url = driver.current_url

    flag = True
    while (flag):
        try:
            time.sleep(5)
            mainDIV = driver.find_elements_by_xpath("//li[@class='offer-card-desktop']")

            for i in mainDIV:
                category = i.find_element_by_xpath(".//h3").text

                DIV = i.find_elements_by_xpath(".//div[@role='list']/div")
                carName = DIV[0].text
                capacity = DIV[1].text
                capacity = capacity.split()[1]
                mileage = DIV[2].text
                cleaning = DIV[3].text
                exact_address = i.find_element_by_xpath(".//div[@id='location-sub-info']").text
                price = i.find_element_by_xpath(".//div[@class='per-day-price']").text
                total_price = i.find_element_by_xpath(".//span[@class='total-price']").text
                vendorName = i.find_element_by_xpath(
                    ".//div[@class='uitk-spacing vendor-logo-container uitk-spacing-padding-blockstart-two']/div/img").get_attribute(
                    "alt")
                transmission = i.find_element_by_xpath("(//div[@role='list'])/div[2]/div//span[3]").text
                len_of_rental = dropoff_diff - pickup_diff
                len_of_rental = str(len_of_rental)
                len_of_rental = len_of_rental.split(",")[0]

                print("Pickup Location : " + pickup)
                print("Pickup State : " + state)
                print("Drop Off Location : " + dropoff)
                print("Category : " + category)
                print("Car Name : " + carName)
                print("Capacity : " + capacity)
                print("Mileage : " + mileage)
                print("Cleaning : " + cleaning)
                print("Exact Address : " + exact_address)
                print("Length of Rental : " + len_of_rental)
                print("Price : " + price)
                print("Total Price : " + total_price)
                print("Vendor Name : " + vendorName)
                print("Transmission : " + transmission)
                print("URL : " + current_url)

                with open(os.getcwd() + "/" + str(pickup_date) + "-" + str(pickup_month) + " To " +  str(dropoff_date) + "-" + str(dropoff_month) + ".csv", 'a+', newline='') as write_obj:
                    # Create a writer object from csv module
                    csv_writer = writer(write_obj)
                    # Add contents of list as last row in the csv file
                    csv_writer.writerow(
                        [pickup, state, dropoff, category, carName, vendorName, capacity, transmission, mileage,
                         cleaning, exact_address, price, total_price, len_of_rental, current_url])

                print("------------------------------------------------------")

            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            wait = WebDriverWait(driver, 10)
            element = wait.until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Show more')]"))).click()

        except Exception as e:
            print(e)
            flag = False
            continue