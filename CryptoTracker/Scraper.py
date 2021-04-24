from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from firebase import Firebase
import python_jwt
import random
import time
import os
from datetime import datetime
import pytz

def mainCode():

    # Chrome Initialization
    op = webdriver.ChromeOptions()
    op.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    op.add_argument('headless')
    op.add_argument("--no-sandbox")
    op.add_argument("--disable-dev-sh-usage")

    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=op)

    # Ovex.io
    driver.get('https://www.ovex.io/products/arbitrage')
    ovex = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='live_premium']")))
    ovex = ovex.get_attribute("innerHTML")
    ovex = ovex.split()
    ovex = ovex[-1][:-1]
    print(ovex)

    # Arbatunity.com
    driver.get('https://www.arbatunity.com/wwwajax.php')
    arbatunity = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//body/b")))
    arbatunity = arbatunity.get_attribute("innerHTML")
    arbatunity = arbatunity[:-1]
    print(arbatunity)

    # DataBase Appending
    config = {
        "apiKey": "AIzaSyDgm1nCubjtFnec2CyJezEJW4gGP4HjnPE",
        "authDomain": "cryptotracker-2021.firebaseapp.com",
        "databaseURL": "https://cryptotracker-2021-default-rtdb.firebaseio.com",
        "projectId": "cryptotracker-2021",
        "storageBucket": "cryptotracker-2021.appspot.com",
        "messagingSenderId": "655100349264",
        "appId": "1:655100349264:web:8f2a818db1195a5867ba55",
        "measurementId": "G-WMCPZT75G6"
    }

    firebase = Firebase(config)
    db = firebase.database()

    key = db.generate_key()
    key = str(key)

    UTC = pytz.timezone('Africa/Blantyre')
    africa_utc = datetime.now(UTC)
    current_time = africa_utc.strftime("%H:%M:%S")

    data = {
        "arbatunity": arbatunity,
        "ovex": ovex,
        "current_time": current_time
    }

    results = db.child("Crypto Values/" + key).set(data)

    print(results)




while True:
    try:
        mainCode()
        time.sleep(300)
    except:
        mainCode()
