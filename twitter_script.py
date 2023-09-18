import wait as wait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.action_chains import ScrollOrigin
from selenium.common.exceptions import NoSuchElementException

import os
import datetime
import re
import pandas as pd
# Wait for a fixed amount of time (in seconds)
import time
import wait



# Set the path to a new directory for user data
user_data_dir = os.path.join(os.getcwd(), 'my_selenium_data1')

# Create Chrome Options and set user data directory
chrome_options = Options()
chrome_options.add_argument(f"user-data-dir={user_data_dir}")
chrome_options.add_argument("--headless")
chrome_options.add_argument(" --window-size=1920x1080")
chrome_options.add_argument(" --ignore-certificate-errors")
service = Service(os.getcwd() +"/chromedriver")
#service = Service(chrome_drive)
#driver = webdriver.Chrome(options=chrome_options, service=service)
# Create WebDriver instance with options
try:
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://twitter.com/settings/explore/location')
    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.XPATH, "//span[normalize-space()='Locations']")))
    location='India'
    #location='US'
    element = driver.find_element(By.XPATH, "//span[normalize-space()='Locations']")
    time.sleep(2)
    # create action chain object
    action = ActionChains(driver)
    scroll_origin = ScrollOrigin.from_element(element)
    action.scroll_from_origin(scroll_origin, 0, 20000).perform()
    time.sleep(5)
    action.scroll_from_origin(scroll_origin, 0, 20000).perform()
    time.sleep(2)
    action.scroll_from_origin(scroll_origin, 0, 20000).perform()
    time.sleep(2)
    action.scroll_from_origin(scroll_origin, 0, -20000).perform()
    time.sleep(2)
    action.scroll_from_origin(scroll_origin, 0, 4900).perform()
    time.sleep(2)
    action.scroll_from_origin(scroll_origin, 0, -20000).perform()
    time.sleep(2)
    if location=='India':
        action.scroll_from_origin(scroll_origin, 0, 4400).perform()
        wait.until(EC.presence_of_element_located((By.XPATH, "//span[normalize-space()='India']")))
        elementin=driver.find_element(By.XPATH, "//span[normalize-space()='India']")
        action.move_to_element(elementin).click().perform()
    elif location=='US':
        action.scroll_from_origin(scroll_origin, 0, 9900).perform()
        wait.until(EC.presence_of_element_located((By.XPATH, "//span[normalize-space()='United States']")))
        elementin=driver.find_element(By.XPATH, "//span[normalize-space()='United States']")
        action.move_to_element(elementin).click().perform()
    time.sleep(5)
    driver.get("https://twitter.com/explore/tabs/trending")
    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='css-901oao r-18jsvk2 r-37j5jr r-a023e6 r-b88u0q r-rjixqe r-1bymd8e r-bcqeeo r-qvutc0']")))
    time.sleep(1)
    #driver.execute_script("window.scrollBy(0, 2500);")
    resultsx = driver.find_elements(By.XPATH, "//div[@class='css-1dbjc4n r-16y2uox r-bnwqim']")
    resultab=[]
    for result in resultsx:
        # Use the relative XPATH to find the nested element
        nested_element = result.find_element(By.XPATH, ".//div[@class='css-901oao r-18jsvk2 r-37j5jr r-a023e6 r-b88u0q r-rjixqe r-1bymd8e r-bcqeeo r-qvutc0']")
        #print(nested_element.text)
        try:
            nested_element2 = result.find_element(By.XPATH, ".//div[@class='css-901oao r-14j79pv r-37j5jr r-n6v787 r-16dba41 r-1cwl3u0 r-14gqq1x r-bcqeeo r-qvutc0']")
            #print(nested_element2.text)
            temp={"Tag":str(nested_element.text), "Count":str(nested_element2.text)}
        except NoSuchElementException:
            temp={"Tag":str(nested_element.text), "Count":'No Count'}
        print(temp)
        resultab.append(temp)
    # Close the browser
    driver.quit()
except Exception as error:
    print("An error occurred:", error
    driver.quit()
