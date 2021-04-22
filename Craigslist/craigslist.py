from selenium import webdriver
import csv

try:
    gig_or_job = str(input("Enter Type (job or gig) : ")).lower()
    keyword = str(input("Enter Keyword : ")).lower()

    if gig_or_job == "job":
        gigjob = gig_or_job
        gig_or_job = "jjj"

    elif gig_or_job == "gig":
        gig_or_job = "ggg"

    else:
        print("Type only job or gig")

    driver = webdriver.Firefox(executable_path='C:/Users/92324/Downloads/geckodriver-v0.26.0-win64/geckodriver.exe')
    my_url = 'https://boston.craigslist.org/'
    driver.get(my_url)
    driver.implicitly_wait(20)
    cities = driver.find_elements_by_xpath("//*[@id='rightbar']/ul/li[2]/ul/li/a")

    for i in cities:
        city = i.get_attribute('innerHTML')
        driver = webdriver.Firefox(executable_path='C:/Users/92324/Downloads/geckodriver-v0.26.0-win64/geckodriver.exe')
        driver.get(i.get_attribute('href') + "search/" + gig_or_job + "?query=" + keyword)
        driver.implicitly_wait(20)
        links = driver.find_elements_by_xpath("//li[@class='result-row']/a")

        for i in links:
            i = i.get_attribute('href')
            with open('links.csv', 'a+', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([i, keyword, gigjob, city])

        try:
            while True:
                next_btn = driver.find_element_by_xpath("//*[@id='searchform']/div[5]/div[3]/span[2]/a[3]").click()
                driver.implicitly_wait(20)
                links = driver.find_elements_by_xpath("//li[@class='result-row']/a")
                for i in links:
                    i = i.get_attribute('href')


        except Exception as e:
            pass

        driver.close()

except Exception as e:
    pass