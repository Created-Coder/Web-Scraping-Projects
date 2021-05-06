#importing libraries

from bs4 import BeautifulSoup #to scrape webpage
import requests #to get send request on website and get response
import pandas as pd #to make dataframe

#Getting Website Response
get_website = requests.get("https://www.worldometers.info/coronavirus/")

#Getting Website's Html code as a string
web_html = get_website.text

# Send String Html code in BS4 to parse html
soup = BeautifulSoup(web_html, "html.parser")

# Retreiving table which id is "main_table_countries_today"
table = soup.find("table", {"id": "main_table_countries_today"})


# Getting Heading of table

# Make empty list to append all my heading later
heading = []

# Find all the th tags from our table
head = table.find_all("th")
for i in head:
    heading.append(i.text)

# Find all the tr tags from our table
table_rows = table.find_all('tr')

# Make empty list to append all the data from tr.
res = []

# We are going in every tr by help of loop
for i in table_rows:
    try:
        # Giving every tr tag to bs4
        soup = BeautifulSoup(str(i), "html.parser")

        # We are finding all the td tags in tr with bs4
        td = soup.find_all("td")

        # We make new empty list to append single row of data
        row = []
        for i in td:
            # appending single row data in row list
            row.append(i.text)

        # appending all the rows in our main list where all the rows exists.
        res.append(row)

    except:
        pass

#getting only Countries Data by slicing the list
res = res[9:-9]
# print(res)

# Making dataframe
df = pd.DataFrame(res, columns=heading)

#Set the option to display all the rows
pd.set_option('display.max_rows', None)

df
