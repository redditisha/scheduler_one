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
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchWindowException
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import os
import glob
import datetime
import re
from ordered_set import OrderedSet
import pandas as pd
import numpy as np
import time  # Removed duplicate import
from googleapiclient.discovery import build
from dateutil import parser
from IPython.display import JSON
import isodate
from datetime import date, datetime
import gspread
from google.oauth2 import service_account
from googleapiclient.errors import HttpError
def convertvaluetoint(jx):
    jx = jx.replace(',', '')
    try:
        if jx[-1] == 'K':
            View = int(float(jx[:-1]) * 1000)
        elif jx[-1] == 'M':
            View = int(float(jx[:-1]) * 1000000)
        elif jx[-1] == 'B':
            View = int(float(jx[:-1]) * 1000000000)
        else:
            View = int(jx)
    except ValueError:
        raise ValueError("Invalid input format")
    return View
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
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
creds = None
creds = service_account.Credentials.from_service_account_info(
    credens, scopes=SCOPES)
def worksheet_update(Channel_Details,sheet_id,worksheet_num,Top_left):
    gc = gspread.service_account_from_dict(credens)
    sheets = gc.open_by_key(str(sheet_id))
    worksheet = sheets.worksheet(worksheet_num)
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
def next_letter(letter,steps):
    ascii_value = ord(letter)
    new_ascii_value = ascii_value + (int(steps)-1)
    
    if letter.islower():
        if new_ascii_value > ord('z'):
            new_ascii_value -= 26
    else:
        if new_ascii_value > ord('Z'):
            new_ascii_value -= 26     
    new_letter = chr(new_ascii_value)
    return new_letter
def get_sheet_id(service, spreadsheet_id, sheet_name):
    spreadsheet_info = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    sheets = spreadsheet_info.get('sheets', [])
    for sheet in sheets:
        if sheet['properties']['title'] == sheet_name:
            return sheet['properties']['sheetId']
    return None

def insert_empty_row(spreadsheet_id, sheet_name, start_index, end_index):
    try:
        service = build('sheets', 'v4', credentials=creds)
        sheet_id = get_sheet_id(service, spreadsheet_id, sheet_name)
        if sheet_id is not None:
            body = {
                'requests': [
                    {
                        "insertDimension": {
                            "range": {
                                "sheetId": sheet_id,
                                "dimension": "ROWS",
                                "startIndex": start_index,
                                "endIndex": end_index
                            },
                            "inheritFromBefore": True
                        }
                    },
                ]
            }

            service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body=body).execute()
        else:
            print(f"Sheet '{sheet_name}' not found in the spreadsheet.")

    except HttpError as error:
        print(f"An error occurred: {error}")
        return error
SCROLL_PAUSE_TIME=5
#URL_List=[
#{'Name':'English','Post':'https://www.instagram.com/sadhguru/','Reel':'https://www.instagram.com/sadhguru/reels/'}]
URL_List=[
{'Name':'English','Post':'https://www.instagram.com/sadhguru/','Reel':'https://www.instagram.com/sadhguru/reels/'},
#{'Name':'Spanish','Post':'https://www.instagram.com/sadhguruespanol/','Reel':'https://www.instagram.com/sadhguruespanol/reels/'},         
{'Name':'Russian','Post':'https://www.instagram.com/sadhguru.russian/','Reel':'https://www.instagram.com/sadhguru.russian/reels/'},
#{'Name':'French','Post':'https://www.instagram.com/sadhguru.francais/','Reel':'https://www.instagram.com/sadhguru.francais/reels/'},
#{'Name':'German','Post':'https://www.instagram.com/sadhguru.deutsch/','Reel':'https://www.instagram.com/sadhguru.deutsch/reels/'},
#{'Name':'Portuguese','Post':'https://www.instagram.com/sadhguru_portugues/','Reel':'https://www.instagram.com/sadhguru_portugues/reels/'},
#{'Name':'Italian','Post':'https://www.instagram.com/sadhguru.italiano.ufficiale/','Reel':'https://www.instagram.com/sadhguru.italiano.ufficiale/reels/'},
#{'Name':'Indonesian','Post':'https://www.instagram.com/sadhgurubahasaindonesia/','Reel':'https://www.instagram.com/sadhgurubahasaindonesia/reels/'},
#{'Name':'Arabic','Post':'https://www.instagram.com/sadhguru.arabic/','Reel':'https://www.instagram.com/sadhguru.arabic/reels/'},
#{'Name':'Koreyan','Post':'https://www.instagram.com/sadhguru.korea/','Reel':'https://www.instagram.com/sadhguru.korea/reels/'},
#{'Name':'Romanian','Post':'https://www.instagram.com/sadhguru.romana/','Reel':'https://www.instagram.com/sadhguru.romana/reels/'},
##{'Name':'Persian','Post':'https://www.instagram.com/sadhguru_persian/','Reel':'https://www.instagram.com/sadhguru_persian/reels/'},
#{'Name':'T. Chinese','Post':'https://www.instagram.com/sadhguru.traditionalchinese/','Reel':'https://www.instagram.com/sadhguru.traditionalchinese/reels/'},
#{'Name':'Hindi','Post':'https://www.instagram.com/sadhguru.hindiofficial/','Reel':'https://www.instagram.com/sadhguru.hindiofficial/reels/'},
#{'Name':'Telugu','Post':'https://www.instagram.com/sadhgurutelugu/','Reel':'https://www.instagram.com/sadhgurutelugu/reels/'},
#{'Name':'Kannada','Post':'https://www.instagram.com/sadhguru_kannada_official/','Reel':'https://www.instagram.com/sadhguru_kannada_official/reels/'},
#{'Name':'Tamil','Post':'https://www.instagram.com/sadhgurutamil/','Reel':'https://www.instagram.com/sadhgurutamil/reels/'},
#{'Name':'Bangla','Post':'https://www.instagram.com/sadhguru.bangla/','Reel':'https://www.instagram.com/sadhguru.bangla/reels/'},
#{'Name':'Malayalam','Post':'https://www.instagram.com/sadhguru.malayalam/','Reel':'https://www.instagram.com/sadhguru.malayalam/reels/'},
#{'Name':'Marathi','Post':'https://www.instagram.com/sadhguru_marathi_official/','Reel':'https://www.instagram.com/sadhguru_marathi_official/reels/'},
#{'Name':'Gujarati','Post':'https://www.instagram.com/sadhguru.gujarati/','Reel':'https://www.instagram.com/sadhguru.gujarati/reels/'}
]

for URL in URL_List:
    k=0
    while True:
        try:
            # Set the path to a new directory for user data
            user_data_dir = os.path.join(os.getcwd(), 'my_selenium_data1')
            # Create Chrome Options and set user data directory
            chrome_options = Options()
            chrome_options.add_argument(f"user-data-dir={user_data_dir}")
            chrome_options.add_argument("--headless")
            chrome_options.add_argument(" --window-size=1920x1080")
            chrome_options.add_argument(" --ignore-certificate-errors")
            service = Service(executable_path = os.getcwd() +"/chromedriver")
            #service = Service(chrome_drive)
            print("loadiing chrome driver")
            #driver = webdriver.Chrome(options=chrome_options)
            driver = webdriver.Chrome(options=chrome_options,service=service)
            url = "https://google.com"
            driver.get(url)
            time.sleep(3)
            driver.get(URL['Post'])
            print('URL Visible: '+URL['Post'])
            last_height = driver.execute_script("return document.body.scrollHeight")
            unique1=[]
            while True:
                html_source = " "
                i = 0
        
                # try to scroll 5 times in case of slow connection
                while i < 5:
        
                    # Scroll down to one page length
                    driver.execute_script("window.scrollBy(0, 1500);")
        
                    # Wait to load page
                    time.sleep(SCROLL_PAUSE_TIME)
                    # get page height in pixels
                    new_height = driver.execute_script("return document.body.scrollHeight")
        
                    # break this loop when you are able to scroll further
                    if new_height != last_height:
                        break
                    i += 1
                flag=False
                while True:
                    try:
                        page_source = driver.page_source
                        #<span class="">10.6K</span>
                        # Parse the page source with BeautifulSoup
                        soup = BeautifulSoup(page_source, 'html.parser')
        
                        # Find the divs with class 'main-page-wrapper'
                        divs = soup.select('div._aabd._aa8k._al3l')
                        wait = WebDriverWait(driver, 10)# Iterate through the divs and find links within them
                        for div in divs:
                            temp = {}
                            links = div.find_all('a')
                            for a in links:
                                href = a.get('href')
                                print(href)
                                text_elements = a.find(class_="x5yr21d xu96u03 x10l6tqk x13vifvy x87ps6o xh8yej3").get('alt')
                                x_path='//a[@href='+'"'+href+'"'+']'
                                try:
                                    t2= driver.find_element(By.XPATH,x_path)
                                    actions = ActionChains(driver)
                                    actions.move_to_element(t2).perform()
                                    wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='_ac2d']")))
                                    Class1= driver.find_element(By.XPATH, "//div[@class='_ac2d']")
                                    Bulk_add3=Class1.find_elements(By.XPATH, ".//span[@class='html-span xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1hl2dhg x16tdsg8 x1vvkbs']")
                                    Likes=convertvaluetoint(Bulk_add3[0].text)
                                    Comments=convertvaluetoint(Bulk_add3[1].text)
                                    temp={'Link':'https://www.instagram.com/p/'+href.split('/')[2],'Likes':Likes,'Comments':Comments,'Alt Text':str(text_elements)}
                                except:
                                    temp={'Link':'https://www.instagram.com/p/'+href.split('/')[2],'Likes':0,'Comments':0,'Alt Text':str(text_elements)}
                                print(str(Likes)+' '+str(Comments))
                                unique1.append(temp)
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
                df = pd.DataFrame(unique1)
                unique_df = df.drop_duplicates()
                unique1 = unique_df.to_dict('records')
                new_height = driver.execute_script("return document.body.scrollHeight")
                if len(unique1)>=20:
                    break
                elif new_height == last_height:
                    break
                print('Total Unique '+str(len(unique1)))
                last_height = new_height
            if flag==True:
                break
            time.sleep(3)
            driver.get(URL['Reel'])
            print('URL Visible: '+URL['Reel'])
            last_height = driver.execute_script("return document.body.scrollHeight")
            unique2=[]
            while True:
                html_source = " "
                i = 0
                # try to scroll 5 times in case of slow connection
                while i < 5:
                    # Scroll down to one page length
                    driver.execute_script("window.scrollBy(0, 1500);")
                    # Wait to load page
                    time.sleep(SCROLL_PAUSE_TIME)
                    # get page height in pixels
                    new_height = driver.execute_script("return document.body.scrollHeight")
        
                    # break this loop when you are able to scroll further
                    if new_height != last_height:
                        break
                    i += 1
                flag=False
                while True:
                    try:
                        # Get the page source after it has loaded
                        page_source = driver.page_source
        
                        # Parse the page source with BeautifulSoup
                        soup = BeautifulSoup(page_source, 'html.parser')
        
                        # Find the divs with class 'main-page-wrapper'
                        divs = soup.find_all(class_='_aajw')
        
                        # Iterate through the divs and find links within them
                        for div in divs:
                            temp = {}
                            links = div.find_all('a')
                            for a in links:
                                href = a.get('href')
                                print(href)
                                spansviews = a.find_all('span', class_='x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye xl565be x1s688f x9bdzbf x1tu3fi x3x7a5m x10wh9bi x1wdrske x8viiok x18hxmgj')[0].text
                                #print(spansviews)
                                Views=convertvaluetoint(spansviews)
                                try:
                                    spanslikes = a.find_all('span', class_='x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye xl565be x1xlr1w8 x9bdzbf x10wh9bi x1wdrske x8viiok x18hxmgj')
                                    likesonpage=spanslikes[0].text
                                    Likes=convertvaluetoint(likesonpage)
                                    commentonpage=spanslikes[1].text
                                    Comments=convertvaluetoint(commentonpage)
                                    temp={'Link':'https://www.instagram.com/p/'+href.split('/')[2],'Views':Views,'Likes':Likes,'Comments':Comments}
                                except IndexError:
                                    temp={'Link':'https://www.instagram.com/p/'+href.split('/')[2],'Views':Views,'Likes':0,'Comments':0}
                                unique2.append(temp)
                                print('Views= '+str(Views)+' '+'Likes= '+str(likesonpage)+' '+'Comments= '+str(commentonpage))
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
                df = pd.DataFrame(unique2)
                unique_df = df.drop_duplicates()
                unique2 = unique_df.to_dict('records')
                new_height = driver.execute_script("return document.body.scrollHeight")
                if len(unique2)>=20:
                    break
                elif new_height == last_height:
                    break
                print('Total Unique '+str(len(unique2)))
                last_height = new_height
            df1 = pd.DataFrame(unique1)
            df2 = pd.DataFrame(unique2)
        
            # Merge DataFrames based on 'Link' column using left join
            merged = pd.merge(left=df1, right=df2, how='left', on='Link')
        
            # Fill NaN values in specific columns with 0
            merged['Views'].fillna(0, inplace=True)
            merged['Likes_y'].fillna(0, inplace=True)
            merged['Comments_y'].fillna(0, inplace=True)
        
            # Use .loc[] for getting and setting values to avoid SettingWithCopyWarning
            merged.loc[merged['Likes_x'] <= merged['Likes_y'], 'Likes_x'] = merged.loc[merged['Likes_x'] <= merged['Likes_y'], 'Likes_y']
            merged.loc[merged['Comments_x'] <= merged['Comments_y'], 'Comments_x'] = merged.loc[merged['Comments_x'] <= merged['Comments_y'], 'Comments_y']
        
            # Drop unnecessary columns and rename columns
            merged.drop(['Likes_y', 'Comments_y'], axis=1, inplace=True)
            merged.rename(columns={'Likes_x': 'Likes', 'Comments_x': 'Comments'}, inplace=True)
            Lists=merged.to_dict(orient='records')
            
            driver.quit()
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument(" --window-size=1920x1080")
            chrome_options.add_argument(" --ignore-certificate-errors")
            service = Service(executable_path = os.getcwd() +"/chromedriver")
            #service = Service(chrome_drive)
            print("loadiing chrome driver")
            #driver = webdriver.Chrome(options=chrome_options)
            driver = webdriver.Chrome(options=chrome_options,service=service)
            i=0
            for x in Lists:
                j=0
                while True:
                    try:
                        driver.get(x['Link'])
                        wait = WebDriverWait(driver, 10)# Iterate through the divs and find links within them
                        wait.until(EC.presence_of_element_located((By.XPATH, "//time[@class='_aaqe']")))
                        # Define the specific span class you want to target
                        page_source = driver.page_source
                        # Parse the page source with BeautifulSoup
                        soup = BeautifulSoup(page_source, 'html.parser')
                        # Find the divs with class 'main-page-wrapper'
                        divs = soup.find_all(class_='_aacl _aaco _aacu _aacx _aad7 _aade')
                        x['Caption'] = divs[0].text
                        pubs = soup.find_all(class_='_aaqe')
                        x['Published On']= pubs[0].get('datetime')
                    except KeyboardInterrupt:
                        flag=True
                        break
                    except Exception as error:
                        print(error)
                        print(x['Link'])
                        x['Caption'] = ''
                        x['Published On']= ''
                        time.sleep(5)
                        j=j+1
                        if j>=5:
                            break
                        else:
                            time.sleep(10)
                            driver.refresh()
                            continue
                    else:
                        break
                if flag==True:
                    break
                i=i+1
                if i % 30 == 0:
                    print("Count: "+ str(i))
            if flag==True:
                break
            i=0
            tobeadded=[]
            while True:
                if i>=(len(Lists)):break
                result_date = (datetime.strptime(str(date.today()), "%Y-%m-%d") - timedelta(days=1)).strftime('%Y-%m-%d')
                if Lists[i]['Published On']=='': 
                    i=i+1
                    continue
                timestamp_object = datetime.fromisoformat(Lists[i]['Published On'][:-1]).strftime('%Y-%m-%d')
        
                if result_date==timestamp_object:
                    #print('Awesome'+' '+str(Lists[i]['Link']))
                    tobeadded.append(Lists[i])
                i=i+1
            i=0
            while True:
                if i>=(len(tobeadded)): break
                desired_order = ['Link', 'Caption', 'Views', 'Published On', 'Likes', 'Comments','Alt Text']
                tobeadded[i] = {key: tobeadded[i][key] for key in desired_order}
                i=i+1
            print('Done')
            insert_empty_row('1_bBS5vcGRRGxWsBz202ohIV5k7x0FNHAJ-2FYD9UTBY', URL['Name'], 1, 1+len(tobeadded))
            Top_left='A2'
            worksheet_update(tobeadded,'1_bBS5vcGRRGxWsBz202ohIV5k7x0FNHAJ-2FYD9UTBY',URL['Name'],Top_left)
            driver.quit()
            time.sleep(3)
        except Exception as error:
            print(error)
            driver.quit()
            k=k+1
            if k>=5:
                print('not added for: '+ URL['Name'])
                break
            else:
                time.sleep(10)
                continue
        else:
            break
