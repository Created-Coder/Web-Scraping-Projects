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

# Reading Data
file = "inputExpedia.xlsx"
book = xlrd.open_workbook(file)
sh = book.sheet_by_index(0)

data = []
months = {'01': 'Jan',
          '02': 'Feb',
          '03': 'Mar',
          '04': 'Apr',
          '05': 'May',
          '06': 'Jun',
          '07': 'Jul',
          '08': 'Aug',
          '09': 'Sep',
          '10': 'Oct',
          '11': 'Nov',
          '12': 'Dec'
          }

cols = sh.ncols
print("File have " + str(cols) + " Columns")

rows = sh.nrows
print("File have " + str(rows)  + " Rows")


for j in range(1, rows):
    #     PICK UP TIME
    # date_values = xlrd.xldate_as_tuple(sh.cell(j, 4).value, datemode=book.datemode)
    # pickUp_Time = date_values
    # pickUp_Time = pickUp_Time[3:]
    # pickUp_Time = str(pickUp_Time[0]) + ":" + str(pickUp_Time[1])
    # d = datetime.strptime(pickUp_Time, "%H:%M")
    # pickUp_Time = d.strftime("%r")
    # print(pickUp_Time)

    #  DROP OFF TIME
    # date_values = xlrd.xldate_as_tuple(sh.cell(j, 5).value, datemode=book.datemode)
    # dropOff_Time = date_values
    # dropOff_Time = dropOff_Time[3:]
    # dropOff_Time = str(dropOff_Time[0]) + ":" + str(dropOff_Time[1])
    # d = datetime.strptime(dropOff_Time, "%H:%M")
    # dropOff_Time = d.strftime("%r")
    # print(dropOff_Time)

    #  PICKUP DATE
    # date_values = xlrd.xldate_as_tuple(sh.cell(j, 3).value, datemode=book.datemode)
    # mo = months["0" + str(date_values[:3][1])]
    # date = date_values[2]
    # date_pickUp = mo + " " + str(date)
    # print(date_pickUp)

    # DropOff Date
    # date_values = xlrd.xldate_as_tuple(sh.cell(j, 2).value, datemode=book.datemode)
    # mo = months["0" + str(date_values[:3][1])]
    # date = date_values[2]
    # date_dropOff = mo + " " + str(date)
    # print(date_dropOff)

    data.append({
        'Pick Up': sh.cell(j, 0).value,
        "Drop Off": sh.cell(j, 1).value,
        # "Pick Up Date": date_pickUp,
        # "Drop Off Date": date_dropOff,
        # "Pick Up Time ": pickUp_Time,
        # "Drop Off Time": dropOff_Time,
    })

print(data)
filename = "Output.csv"
# filename = input("Enter File Name for saving file, For Example(Data.csv): ")
with open(os.getcwd() + "/" + filename, 'a+', newline='', encoding='utf-8-sig') as f:
    writer_data = writer(f)
    writer_data.writerow(["Category", "Car Name", "Capacity", "Mileage", "Cleaning", "Pickup", "Drop off", "Price"])


driver = webdriver.Chrome(executable_path='C:/Users/92324/Downloads/chromedriver_win32/chromedriver.exe')
driver.get("https://www.expedia.com/Cars")

driver.implicitly_wait(20)
driver.find_element_by_xpath("//button[@aria-label='Pick-up']").click()
driver.implicitly_wait(20)
driver.find_element_by_xpath("//input[@id='location-field-locn']").send_keys(data[0]['Pick Up'])

wait = WebDriverWait(driver, 20)
element = wait.until(EC.element_to_be_clickable(
    (By.XPATH, "//ul[@data-stid='location-field-locn-results']/li[@data-index='0']/button"))).click()

driver.implicitly_wait(20)
driver.find_element_by_xpath("//button[@aria-label='Same as pick-up']").click()
driver.implicitly_wait(20)
driver.find_element_by_xpath("//input[@id='location-field-loc2']").send_keys(data[0]['Drop Off'])

wait = WebDriverWait(driver, 20)
element = wait.until(EC.element_to_be_clickable(
    (By.XPATH, "//ul[@data-stid='location-field-loc2-results']/li[@data-index='0']/button"))).click()

driver.implicitly_wait(20)
driver.find_element_by_xpath("//button[@type='submit']").click()

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
            pickup = i.find_element_by_xpath(".//div[@id='location-sub-info']").text
            dropoff = i.find_element_by_xpath(".//div[contains(text(), 'Drop-off')]/following-sibling::div/div").text
            dropoff = dropoff.replace(",", "")
            price = i.find_element_by_xpath(".//span[@class='total-price']").text

            print("Category : " + category)
            print("Car Name : " + carName)
            print("Capacity : " + capacity)
            print("Mileage : " + mileage)
            print("Cleaning : " + cleaning)
            print("Pickup : " + pickup)
            print("Drop off : " + dropoff)
            print("Price : " + price)

            with open(os.getcwd() + "/" + filename, 'a+', newline='') as write_obj:
                # Create a writer object from csv module
                csv_writer = writer(write_obj)
                # Add contents of list as last row in the csv file
                csv_writer.writerow([category, carName, capacity, mileage, cleaning, pickup, dropoff, price])

            print("------------------------------------------------------")

        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Show more')]"))).click()

    except Exception as e:
        print(e)
        flag = False
        driver.close()
