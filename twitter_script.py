from __future__ import print_function
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
from ordered_set import OrderedSet
import pandas as pd
# Wait for a fixed amount of time (in seconds)
import time
import wait
from googleapiclient.discovery import build
from dateutil import parser
import pandas as pd
from IPython.display import JSON
import numpy as np
import re
import os
import isodate
import datetime
from datetime import date
from datetime import datetime
import gspread
import time
# from oauth2Client.service_account import ServiceAccountCredentials
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'Keys.json'

creds = None
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

credens = {
    "type": "service_account",
    "project_id": "redditbot-363109",
    "private_key_id": "a07629ebcbcecc27e45de1d21e72e065d2f4205a",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDZ+QeKSHucxFTJ\nAhnGyvAaKq0JGejU5D1W8ESt5slAUBVP0JL6p0yMJlcPepveD86DtcQdrO48BfMv\nzJrE0DWpeIi1/qFaG62L+o30p2dtCLqBewzd2pZ2bEPZfyTa+NJU2QzGE9yjiB6B\nEzkLIvYKtNmdHVH/seaSzkXNOgbSXfwKbWbGBmLfuKFLAxWy2jGBUqX1sZaSYRIx\nnlnhvz/cCF8EogIqGYhYs8TK30oUq9Z4Q4LmHauBUbQba+Ga2X29su/KITph/Hg5\nXSs4kiNv/xGX1DUED9/nlevpSXMhNnu0Y8lJAwwp9husRHoL7CJ91QirUf+kms9R\nNHUA5xqNAgMBAAECggEABfSCSrphOi64/Ebk6mP3/FcHJDUDgfF8ZYgp8DBadjnZ\n4zTZFyUD995CSad5Y6893qZUJdVoKtakxr0Jy2++z5L99S7wPJR+ANGHGFSMhFOV\nON1iRBtpOfIKRoJtQNhEctH9QdogEI2y+6bJS68YVsGLIno/F8PF/2PIT2uS7SNc\nSvEVGA8GT/BqQP5UPiSjEtLw6mtF0hPcmpVsMjGwH+v8PMHKGohHxCUb8QrnxrMj\nZncGzNkb5KLcNwKBrLQBiCvWJTkB69NeUuBaaJfRiyS1BMobe3xonxQNR6C0C8IH\nW1x8R1iO0GUVTQoSsmbnsgAoXTKr1Mf107t32RT0wQKBgQDw/jOHz2QsrIUghAyQ\nQQIF5M+wdGZfRZHOfWXIGv2DCc7dtrUIQhp+HPtPdTbhXFdGwBpypOq7Mt1SOeqH\nrnzUd7IhGNknFHdkB4A5s1OPvTmS91O+Rde0vI+1xz+qnopaRSTMXqc3Ng+3yLbn\nx/FcOXOX+BjVruUjsd0+vJ73bQKBgQDni9nJEVp0r6FIGZd6ubUcLOqC7duWnZDB\n9dfy10mFHbNevaiCnhgEqvltzn7B2d7gjtm+tE7te733GIUK075+yLPpfgCjTehI\nj48fkRQ8fOeklnm0fuVw8U7vegr5RWVpgrajuNcyrkjx2OtUkxpJdjqkMUCYM6X/\nvJvUUgkboQKBgQDQ9urB2W/4WMO61SV7tBLH/4ajb9sQw2dR0GQAJn8qL8gDchj5\nhzAnqIO1e2LR+Nroy0xjmmK7XbiRQwz9B6zQItX/Yudwvotj3ikuXzOW0LJqoDEq\nLK+E1XgbXCD1ljFLYucsmuqNsj/g0Zbf1fyQRnTYElWee9/OmrzIWI/S5QKBgFxX\nEYt2ODTAtfki+54d4XRTFVMRuLjgLZKskGpwIQnNRnNJ/6HXmoyCAucfqr10PcYg\nMgYzsiZTavbX+HbQ6u906wr7DRYTQ8dsOQ/Fs+RLi7W/rNmmoanhEjG+4hF283KY\nhm3UkT3M85o/f9pCsAEL/WbtnW0Va+YJObv621cBAoGAcObi0XZxuqVhsCwGTU7V\nu/uORsf1E0LuXeLzNiMBoO84UMhxc+mFO1nurV0RqZ6wAyOELsHJIpWoueSJTWRl\nqw0wQ6y6UTvagGgzC+88SD7jRhJaBrnjsa9IDO98qzfgw/Oxb17611HUiaW/aNUl\nrXOuHaX8vHWS6dCNuvm+7qc=\n-----END PRIVATE KEY-----\n",
    "client_email": "joyfulbot@redditbot-363109.iam.gserviceaccount.com",
    "client_id": "105153036553319946005",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/joyfulbot%40redditbot-363109.iam.gserviceaccount.com"
}
def empty_row(Start_index, Number_of_rows, work_sheet_num, Sheetid):
    try:
        service = build('sheets', 'v4', credentials=creds)
        body = {
            'requests': [
                {
                    "insertDimension": {
                        "range": {
                            "sheetId": work_sheet_num,
                            "dimension": "ROWS",
                            "startIndex": Start_index,
                            "endIndex": Number_of_rows+Start_index
                        },
                        "inheritFromBefore": True
                    }
                },
            ]
        }

        service.spreadsheets().batchUpdate(
            spreadsheetId= Sheetid,
            body=body).execute()

    except HttpError as error:
        print(f"An error occurred: {error}")
        return error
def worksheet_update(Channel_Details,sheet_id,worksheet_num,Top_left):
    gc = gspread.service_account_from_dict(credens)
    sheets = gc.open_by_key(str(sheet_id))
    worksheet = sheets.get_worksheet(int(worksheet_num))
    Top_Left_Index=str(Top_left)
    Num_In_Details=len(Channel_Details[0])
    Total_Items=len(Channel_Details)*Num_In_Details
    Bottom_Right_Index= next_letter(re.match(r"([A-Za-z]+)(\d+)", Top_Left_Index).group(1).upper(),Num_In_Details).upper()+str(int(re.match(r"([A-Z]+)(\d+)", Top_Left_Index).group(2))+len(Channel_Details)-1)
    Item=[]
    for Rows in Channel_Details:
        temp=[]
        for Column_Values in Rows.values():
            temp.append(Column_Values)
        Item.append(temp)
    worksheet.update(str(Top_Left_Index+':'+Bottom_Right_Index), Item)
def next_letter(column_name, steps):
    result = []
    carry = 0

    for char in reversed(column_name):
        if steps == 0 and carry == 0:
            result.append(char)
        else:
            ascii_value = ord(char) - ord('A') + carry
            if steps > 0:
                ascii_value += steps
                steps = 0
            carry = ascii_value // 26
            new_char = chr(ascii_value % 26 + ord('A'))
            result.append(new_char)

    if carry > 0:
        result.append(chr(carry - 1 + ord('A')))

    return ''.join(reversed(result))
    
# Set the path to a new directory for user data
user_data_dir = os.path.join(os.getcwd(), 'my_selenium_data1')

print(user_data_dir)
# Create Chrome Options and set user data directory
chrome_options = Options()
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
#chrome_options.add_argument("--user-data-dir=./my_selenium_data1")
#chrome_options.add_argument("--user-data-dir=/home/kali/.config/google-chrome")
print(f"user-data-dir={user_data_dir}")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--ignore-certificate-errors")
service = Service(executable_path = os.getcwd() +"/chromedriver")
#service = Service(chrome_drive)
print("loadiing chrome driver")
driver = webdriver.Chrome(options=chrome_options, service=service)
# Create WebDriver instance with options
#driver = webdriver.Chrome(executable_path="linux_chromedriver",options=chrome_options)
print("cheomr driver loaded")
locations=['India','US','UK','Russia','France','Brazil','Portugal', 'Spain', 'Italy','Germany']#Russia, Brazil, Portugal, Spain, Italy, UK, Saudi Arabia 
#location='US'
empty_row(2, 32, 0, '19Feu-nZlE2R5Boe2mdelYoSj5eAAQWHR84LdtoEBWZk')
flag=False
for location in locations:
    while True:
        try:
            driver.get('https://twitter.com/settings/explore/location')
            wait = WebDriverWait(driver, 20)
            wait.until(EC.presence_of_element_located((By.XPATH, "//span[normalize-space()='Locations']")))
            resultab=[]
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
            action.scroll_from_origin(scroll_origin, 0, 20000).perform()
            time.sleep(2)
            action.scroll_from_origin(scroll_origin, 0, -20000).perform()
            time.sleep(2)
            if location=='India':
                action.scroll_from_origin(scroll_origin, 0, 4400).perform()
                wait.until(EC.presence_of_element_located((By.XPATH, "//span[normalize-space()='India']")))
                elementin=driver.find_element(By.XPATH, "//span[normalize-space()='India']")
                time.sleep(2)
                action.move_to_element(elementin).click().perform()
            elif location=='US':
                action.scroll_from_origin(scroll_origin, 0, 9900).perform()
                wait.until(EC.presence_of_element_located((By.XPATH, "//span[normalize-space()='United States']")))
                elementin=driver.find_element(By.XPATH, "//span[normalize-space()='United States']")
                time.sleep(2)
                action.move_to_element(elementin).click().perform()
            elif location=='UK':
                action.scroll_from_origin(scroll_origin, 0, 9900).perform()
                wait.until(EC.presence_of_element_located((By.XPATH, "//span[normalize-space()='United Kingdom']")))
                elementin=driver.find_element(By.XPATH, "//span[normalize-space()='United Kingdom']")
                time.sleep(2)
                action.move_to_element(elementin).click().perform()
            elif location=='Russia':
                action.scroll_from_origin(scroll_origin, 0, 7800).perform()
                wait.until(EC.presence_of_element_located((By.XPATH, "//span[normalize-space()='Russia']")))
                elementin=driver.find_element(By.XPATH, "//span[normalize-space()='Russia']")
                time.sleep(2)
                action.move_to_element(elementin).click().perform()
            elif location=='Saudi Arabia':
                action.scroll_from_origin(scroll_origin, 0, 7800).perform()
                wait.until(EC.presence_of_element_located((By.XPATH, "//span[normalize-space()='Saudi Arabia']")))
                elementin=driver.find_element(By.XPATH, "//span[normalize-space()='Saudi Arabia']")
                action.move_to_element(elementin).click().perform()
            elif location=='Brazil':
                action.scroll_from_origin(scroll_origin, 0, 1200).perform()
                wait.until(EC.presence_of_element_located((By.XPATH, "//span[normalize-space()='Brazil']")))
                elementin=driver.find_element(By.XPATH, "//span[normalize-space()='Brazil']")
                time.sleep(2)
                action.move_to_element(elementin).click().perform()
            elif location=='Portugal':
                action.scroll_from_origin(scroll_origin, 0, 7600).perform()
                wait.until(EC.presence_of_element_located((By.XPATH, "//span[normalize-space()='Portugal']")))
                elementin=driver.find_element(By.XPATH, "//span[normalize-space()='Portugal']")
                time.sleep(2)
                action.move_to_element(elementin).click().perform()
            elif location=='Spain':
                action.scroll_from_origin(scroll_origin, 0, 8500).perform()
                wait.until(EC.presence_of_element_located((By.XPATH, "//span[normalize-space()='Spain']")))
                elementin=driver.find_element(By.XPATH, "//span[normalize-space()='Spain']")
                time.sleep(2)
                action.move_to_element(elementin).click().perform()
            elif location=='Italy':
                action.scroll_from_origin(scroll_origin, 0, 4700).perform()
                wait.until(EC.presence_of_element_located((By.XPATH, "//span[normalize-space()='Italy']")))
                elementin=driver.find_element(By.XPATH, "//span[normalize-space()='Italy']")
                time.sleep(2)
                action.move_to_element(elementin).click().perform()
            elif location=='Germany':
                action.scroll_from_origin(scroll_origin, 0, 3500).perform()
                wait.until(EC.presence_of_element_located((By.XPATH, "//span[normalize-space()='Germany']")))
                elementin=driver.find_element(By.XPATH, "//span[normalize-space()='Germany']")
                time.sleep(2)
                action.move_to_element(elementin).click().perform()
            elif location=='France':
                action.scroll_from_origin(scroll_origin, 0, 3300).perform()
                wait.until(EC.presence_of_element_located((By.XPATH, "//span[normalize-space()='France']")))
                elementin=driver.find_element(By.XPATH, "//span[normalize-space()='France']")
                time.sleep(2)
                action.move_to_element(elementin).click().perform()
            time.sleep(5)
            driver.get("https://twitter.com/explore/tabs/trending")
            time.sleep(3)
            wait = WebDriverWait(driver, 20)
            wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='css-901oao r-18jsvk2 r-37j5jr r-a023e6 r-b88u0q r-rjixqe r-1bymd8e r-bcqeeo r-qvutc0']")))
            time.sleep(1)
            driver.execute_script("window.scrollBy(0, 300);")
            resultsx = driver.find_elements(By.XPATH, "//div[@class='css-1dbjc4n r-16y2uox r-bnwqim']")
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
            if location=='India':
                time_ = [{'date':str(datetime.now().time())}]
                date_ = [{'date':str(str(date.today()))}]
                worksheet_update(time_,'19Feu-nZlE2R5Boe2mdelYoSj5eAAQWHR84LdtoEBWZk',0,'A3')
                worksheet_update(date_,'19Feu-nZlE2R5Boe2mdelYoSj5eAAQWHR84LdtoEBWZk',0,'A4')
                worksheet_update(resultab,'19Feu-nZlE2R5Boe2mdelYoSj5eAAQWHR84LdtoEBWZk',0,'B3')
            elif location=='US':
                time_ = [{'date':str(datetime.now().time())}]
                date_ = [{'date':str(str(date.today()))}]
                worksheet_update(time_,'19Feu-nZlE2R5Boe2mdelYoSj5eAAQWHR84LdtoEBWZk',0,'D3')
                worksheet_update(date_,'19Feu-nZlE2R5Boe2mdelYoSj5eAAQWHR84LdtoEBWZk',0,'D4')
                worksheet_update(resultab,'19Feu-nZlE2R5Boe2mdelYoSj5eAAQWHR84LdtoEBWZk',0,'E3')
            elif location=='UK':
                time_ = [{'date':str(datetime.now().time())}]
                date_ = [{'date':str(str(date.today()))}]
                worksheet_update(time_,'19Feu-nZlE2R5Boe2mdelYoSj5eAAQWHR84LdtoEBWZk',0,'G3')
                worksheet_update(date_,'19Feu-nZlE2R5Boe2mdelYoSj5eAAQWHR84LdtoEBWZk',0,'G4')
                worksheet_update(resultab,'19Feu-nZlE2R5Boe2mdelYoSj5eAAQWHR84LdtoEBWZk',0,'H3')
            elif location=='Russia':
                time_ = [{'date':str(datetime.now().time())}]
                date_ = [{'date':str(str(date.today()))}]
                worksheet_update(time_,'19Feu-nZlE2R5Boe2mdelYoSj5eAAQWHR84LdtoEBWZk',0,'J3')
                worksheet_update(date_,'19Feu-nZlE2R5Boe2mdelYoSj5eAAQWHR84LdtoEBWZk',0,'J4')
                worksheet_update(resultab,'19Feu-nZlE2R5Boe2mdelYoSj5eAAQWHR84LdtoEBWZk',0,'K3')
            elif location=='Brazil':
                time_ = [{'date':str(datetime.now().time())}]
                date_ = [{'date':str(str(date.today()))}]
                worksheet_update(time_,'19Feu-nZlE2R5Boe2mdelYoSj5eAAQWHR84LdtoEBWZk',0,'M3')
                worksheet_update(date_,'19Feu-nZlE2R5Boe2mdelYoSj5eAAQWHR84LdtoEBWZk',0,'M4')
                worksheet_update(resultab,'19Feu-nZlE2R5Boe2mdelYoSj5eAAQWHR84LdtoEBWZk',0,'N3')
            elif location=='Portugal':
                time_ = [{'date':str(datetime.now().time())}]
                date_ = [{'date':str(str(date.today()))}]
                worksheet_update(time_,'19Feu-nZlE2R5Boe2mdelYoSj5eAAQWHR84LdtoEBWZk',0,'P3')
                worksheet_update(date_,'19Feu-nZlE2R5Boe2mdelYoSj5eAAQWHR84LdtoEBWZk',0,'P4')
                worksheet_update(resultab,'19Feu-nZlE2R5Boe2mdelYoSj5eAAQWHR84LdtoEBWZk',0,'Q3')
            elif location=='Spain':
                time_ = [{'date':str(datetime.now().time())}]
                date_ = [{'date':str(str(date.today()))}]
                worksheet_update(time_,'19Feu-nZlE2R5Boe2mdelYoSj5eAAQWHR84LdtoEBWZk',0,'S3')
                worksheet_update(date_,'19Feu-nZlE2R5Boe2mdelYoSj5eAAQWHR84LdtoEBWZk',0,'S4')
                worksheet_update(resultab,'19Feu-nZlE2R5Boe2mdelYoSj5eAAQWHR84LdtoEBWZk',0,'T3')
            elif location=='Italy':
                time_ = [{'date':str(datetime.now().time())}]
                date_ = [{'date':str(str(date.today()))}]
                worksheet_update(time_,'19Feu-nZlE2R5Boe2mdelYoSj5eAAQWHR84LdtoEBWZk',0,'V3')
                worksheet_update(date_,'19Feu-nZlE2R5Boe2mdelYoSj5eAAQWHR84LdtoEBWZk',0,'V4')
                worksheet_update(resultab,'19Feu-nZlE2R5Boe2mdelYoSj5eAAQWHR84LdtoEBWZk',0,'W3')
            elif location=='Germany':
                time_ = [{'date':str(datetime.now().time())}]
                date_ = [{'date':str(str(date.today()))}]
                worksheet_update(time_,'19Feu-nZlE2R5Boe2mdelYoSj5eAAQWHR84LdtoEBWZk',0,'Y3')
                worksheet_update(date_,'19Feu-nZlE2R5Boe2mdelYoSj5eAAQWHR84LdtoEBWZk',0,'Y4')
                worksheet_update(resultab,'19Feu-nZlE2R5Boe2mdelYoSj5eAAQWHR84LdtoEBWZk',0,'Z3')
            elif location=='France':
                time_ = [{'date':str(datetime.now().time())}]
                date_ = [{'date':str(str(date.today()))}]
                worksheet_update(time_,'19Feu-nZlE2R5Boe2mdelYoSj5eAAQWHR84LdtoEBWZk',0,'AB3')
                worksheet_update(date_,'19Feu-nZlE2R5Boe2mdelYoSj5eAAQWHR84LdtoEBWZk',0,'AB4')
                worksheet_update(resultab,'19Feu-nZlE2R5Boe2mdelYoSj5eAAQWHR84LdtoEBWZk',0,'AC3')
            elif location=='Saudi Arabia':
                time_ = [{'date':str(datetime.now().time())}]
                date_ = [{'date':str(str(date.today()))}]
                worksheet_update(time_,'19Feu-nZlE2R5Boe2mdelYoSj5eAAQWHR84LdtoEBWZk',0,'AE3')
                worksheet_update(date_,'19Feu-nZlE2R5Boe2mdelYoSj5eAAQWHR84LdtoEBWZk',0,'AE4')
                worksheet_update(resultab,'19Feu-nZlE2R5Boe2mdelYoSj5eAAQWHR84LdtoEBWZk',0,'AF3')
            time.sleep(3)
        except KeyboardInterrupt:
            flag=True
            break
        except Exception as error:
            print(error)
            time.sleep(5)
            continue
        else:
            break
    if flag==True:
        break
# Close the browser
driver.quit()
