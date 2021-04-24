from selenium import webdriver
import csv


def mainCode():
    options = webdriver.ChromeOptions();
    options.add_argument('headless');
    driver = webdriver.Chrome(executable_path='C:/Users/92324/Downloads/chromedriver_win32 (3)/chromedriver.exe',
                              options=options)
    driver.get('https://www.soccer24hd.com/home/today.html')

    driver.implicitly_wait(20)
    fields = driver.find_elements_by_xpath("//div[@class='hm_gm_tb_inf1']")

    for field in fields:
        driver.implicitly_wait(20)
        names = field.find_elements_by_class_name("clb_name2")
        match = names[0].get_attribute("innerHTML") + " " + "VS" + " " + names[1].get_attribute("innerHTML")

        driver.implicitly_wait(20)
        time = field.find_element_by_class_name("gmtm223")

        driver.implicitly_wait(20)
        channel = field.find_element_by_xpath("//div[@class='hm_gm_tb_inf1']/div/div[2]/div")

        driver.implicitly_wait(20)
        voice = field.find_element_by_xpath("//div[@class='hm_gm_tb_inf1']/div[2]/div[3]/div")

        driver.implicitly_wait(20)
        league = field.find_element_by_xpath("//div[@class='hm_gm_tb_inf1']/div[2]/div[4]/div")

        driver.implicitly_wait(20)
        link = field.find_element_by_tag_name("a")

        print("Match : " + match)
        print("Time : " + time.get_attribute("innerHTML"))
        print("Channel : " + channel.get_attribute("innerHTML"))
        print("Voice : " + voice.get_attribute("innerHTML"))
        print("League : " + league.get_attribute("innerHTML"))
        print("Link : " + link.get_attribute("href"))

        with open('data.csv', 'a+', newline='') as csvfile:
            fieldnames = ['Match', 'Time', "Channel", "Voice", "League", "Link"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writerow({'Match': match,
                             'Time': time.get_attribute("innerHTML"),
                             "Channel": channel.get_attribute("innerHTML"),
                             "Voice": voice.get_attribute("innerHTML"),
                             "League": league.get_attribute("innerHTML"),
                             "Link": link.get_attribute("href")
                             })

    driver.close()

try:
    mainCode()

except:
    mainCode()
