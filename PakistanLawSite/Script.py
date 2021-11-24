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
from selenium.webdriver.common.action_chains import ActionChains


def listToString(s):
    str1 = " "
    return (str1.join(s))


driver = webdriver.Chrome(executable_path='C:/Users/92324/Downloads/chromedriver/chromedriver.exe')
driver.get("https://www.pakistanlawsite.com/Login/MainPage")
driver.find_element_by_xpath("//input[@id='username']").send_keys("ihcbaisb")
driver.find_element_by_xpath("//input[@id='loginPass']").send_keys("library2626")
driver.find_element_by_xpath("//input[@class='agreeBox']").click()
driver.implicitly_wait(10)
driver.find_element_by_xpath("//button[@class='btn btn-success btn-block login_btn_tablet']").click()
time.sleep(2)
driver.get("https://www.pakistanlawsite.com/Login/TopicPage")
topics = driver.find_elements_by_xpath("//tr[@class='topicType']")
print(len(topics))

for i in range(1, len(driver.find_elements_by_xpath("//tr[@class='topicType']"))):
    try:
        path = "(//tr[@class='topicType'])" + "[" + str(i) + "]"
        topicName = driver.find_element_by_xpath(path).text
        topicName = topicName.split()
        topicName = topicName[1:]
        topicName = listToString(topicName)

        driver.find_element_by_xpath(path).click()
        time.sleep(2)

        sub_topics = driver.find_elements_by_xpath("//tr[@class='subTopicType']")
        #         for j in range(1, len(sub_topics)):
        for j in range(3, 4):
            try:
                sub_path = "(//tr[@class='subTopicType'])" + "[" + str(j) + "]"
                subtopicName = driver.find_element_by_xpath(sub_path).text
                subtopicName = subtopicName.split()
                subtopicName = listToString(subtopicName)

                driver.find_element_by_xpath(sub_path).click()
                time.sleep(2)

                tables = driver.find_elements_by_xpath("//table[@class='table table-striped table-bordered']/tbody")

                if (len(tables) == 0):
                    print("IF TRUE")
                    driver.get("https://www.pakistanlawsite.com/Login/TopicPage")
                    time.sleep(2)
                    btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, path)))
                    driver.execute_script("arguments[0].click();", btn)
                    time.sleep(2)
                    continue


                else:

                    for index in range(1, len(tables)):
                        data_path = "//*[@id='rightmenu']/table" + "[" + str(index) + "]" + "/tbody/tr[1]/td"

                        try:
                            driver.implicitly_wait(10)
                            citationName = driver.find_element_by_xpath(data_path).text
                            citationName = citationName.replace("Citation Name: ", "")
                            if ("Bookmark this Case" in citationName):
                                citationName = citationName.replace("Bookmark this Case", "")

                            print("Topic : " + topicName)
                            print("Sub Topic Name : " + subtopicName)
                            print("Citation Name : " + citationName)

                        except Exception as e:
                            citationName = " "
                            print(e)
                            pass

                        try:
                            companyName = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
                                                                                                          "//*[@id='rightmenu']/table" + "[" + str(
                                                                                                              index) + "]" + "/tbody/tr[2]/td"))).text
                            print("Company Name : " + companyName)

                        except Exception as e:
                            companyName = " "
                            print(e)
                            pass

                        try:
                            driver.implicitly_wait(5)
                            casetype = ""
                            casetype = driver.find_element_by_xpath(
                                "//*[@id='rightmenu']/table" + "[" + str(index) + "]" + "/tbody/tr[3]/td").text

                            print("Case type: " + casetype)



                        except Exception as e:
                            casetype = " "
                            print("Case type: No refer")
                            pass

                        try:
                            description = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
                                                                                                          "//*[@id='rightmenu']/table" + "[" + str(
                                                                                                              index) + "]" + "/tbody/tr[4]/td"))).text
                            print("Description : " + description)

                        except Exception as e:
                            description = " "
                            print(e)
                            pass

                        try:
                            brief_desc = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
                                                                                                         "//*[@id='rightmenu']/table" + "[" + str(
                                                                                                             index) + "]" + "/tbody/tr[5]/td"))).text
                            print("Brief Description : " + brief_desc)


                        except Exception as e:
                            brief_desc = " "
                            print(e)
                            pass

                        try:
                            driver.find_element_by_xpath(
                                "(//input[@value='Head Notes'])" + "[" + str(index) + "]").click()
                            time.sleep(2)
                            headNotes = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.XPATH, "//div[@class='Section1']"))).text
                            print("HeadNotes : " + headNotes)


                        except Exception as e:
                            headNotes = " "
                            print(e)
                            pass

                        try:
                            closebtn = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.XPATH, "//button[@id='TopCloseButtonCreate']")))
                            driver.implicitly_wait(10)
                            ActionChains(driver).move_to_element(closebtn).click(closebtn).perform()
                            time.sleep(2)

                        except:
                            pass

                        try:
                            driver.find_element_by_xpath(
                                "(//input[@value='Case Description'])" + "[" + str(index) + "]").click()
                            time.sleep(2)
                            caseDescription = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.XPATH, "//div[@class='Section1']"))).text
                            print("Case Description : " + caseDescription)


                        except Exception as e:
                            caseDescription = " "
                            print(e)
                            pass

                        try:
                            closebtn = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.XPATH, "//button[@id='TopCloseButtonCreate']")))
                            driver.implicitly_wait(10)
                            ActionChains(driver).move_to_element(closebtn).click(closebtn).perform()
                            time.sleep(2)

                        except:
                            pass

                        print("-------------------------------------------------------------")

                        with open("Data_PakistanLaw.csv", 'a+', newline='', encoding='utf-8-sig') as f:
                            # Create a writer object from csv module
                            csv_writer = writer(f)
                            # Add contents of list as last row in the csv file
                            csv_writer.writerow(
                                [topicName, subtopicName, citationName, companyName, description, brief_desc, headNotes,
                                 caseDescription, casetype])

                    btn = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//button[@class='btn btn-success btn-sm']")))
                    driver.execute_script("arguments[0].click();", btn)
                    time.sleep(5)


            except Exception as e:
                print(e)
                driver.get("https://www.pakistanlawsite.com/Login/TopicPage")
                time.sleep(2)
                btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, path)))
                driver.execute_script("arguments[0].click();", btn)
                time.sleep(2)
                continue

        btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@class='btn btn-success btn-sm']")))
        driver.execute_script("arguments[0].click();", btn)
        time.sleep(5)


    except Exception as e:
        print(e)
        continue

