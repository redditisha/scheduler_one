from __future__ import print_function
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
from datetime import datetime, timedelta
# from oauth2Client.service_account import ServiceAccountCredentials
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

api_key = 'AIzaSyCchWLLWL152_h1pi7DU5ixBnGabjJ1bZY'
#channel_ids for all SG Channels
channel_details=[
{'Name':'English','channelName': 'Sadhguru', 'channelId': 'UCcYzLCs3zrQIBVHYA1sK2sw'},
{'Name':'Spanish','channelName': 'Sadhguru Español', 'channelId': 'UCJoOIj9Yu71wklP3EFzL8-A'},         
{'Name':'Russian','channelName': 'Садхгуру — официальный канал на русском','channelId': 'UC057NSSVc2663UcpoZ0C6EQ'},
{'Name':'French','channelName': 'Sadhguru Français', 'channelId': 'UCrmjX43WdTRI8RwVuRUACCw'},
{'Name':'German','channelName': 'Sadhguru Deutsch', 'channelId': 'UCLXPrBVzL3sDRJ3HFDq3frw'},
{'Name':'Italian','channelName': 'Sadhguru Italiano', 'channelId': 'UCVoo2xW_PFFpdkh9vjexLTg'},
{'Name':'T. Chinese','channelName':'Sadhguru 繁體中文', 'channelId': 'UCSaNMML9AAXTN4142jD-dxw'},
{'Name':'Simplified Chinese','channelName':'Sadhguru Chinese', 'channelId': 'UC5063zeNwwYYBbjYm1k6aXQ'},
{'Name':'Hindi','channelName': 'Sadhguru Hindi', 'channelId': 'UCJ2KaH9TTjZdmKwwAFwwFkA'},
{'Name':'Telugu','channelName': 'Sadhguru Telugu', 'channelId': 'UCNxOfQA4r5BSJMIQzRPIeQw'},
{'Name':'Kannada','channelName': 'Sadhguru Kannada', 'channelId': 'UC2XEzs5R1mn2wTKgtjuMxiQ'},
{'Name':'Tamil','channelName': 'Sadhguru Tamil', 'channelId': 'UCsVCyZFXPPL_iYD8-O2UvrQ'},
{'Name':'Bangla','channelName': 'Sadhguru Bangla', 'channelId': 'UCj6F6irakw10kKGEe3wZX_A'},
{'Name':'Malayalam','channelName': 'Sadhguru Malayalam','channelId': 'UCIAdGobptLFqTpbDauCnKhw'},
{'Name':'Marathi','channelName': 'Sadhguru Marathi', 'channelId': 'UCIiXzyCf-PL3FHve7ylSCeA'},
{'Name':'Isha Foundation','channelName': 'Isha Foundation', 'channelId': 'UCgaiWfiix1zaQS6Mn5SIw2g'}
]

def get_channel_stats(youtube, channel_ids):

    all_data = []
    
    request = youtube.channels().list(
        part="snippet, contentDetails, statistics",
        id=','.join(channel_ids),
        maxResults=50
    )
    response2 = request.execute ()
    # loop through items
    for item in response2['items']:
        data = {'channelName': item['snippet']['title'],
                'subscribers': item['statistics']['subscriberCount'],
                'views': item['statistics']['viewCount'],
                'totalVideos': item['statistics']['videoCount'],
                'playlistId': item['contentDetails']['relatedPlaylists']['uploads'],
                'channelId':item['id']
               }
        all_data.append(data)
    return(pd.DataFrame(all_data))
def get_video_ids(youtube, playlist_id):
    
    video_ids = []
    
    request = youtube.playlistItems().list(
        part="snippet,contentDetails", 
        playlistId=playlist_id,
        maxResults = 50
    )
    response = request.execute()
    
    for item in response['items']:
        temp={'VideoDate':item['contentDetails']['videoPublishedAt'],'Videoid':item['contentDetails']['videoId']}
        video_ids.append(temp)

    next_page_token = response.get('nextPageToken')
    page=1
    '''while next_page_token is not None:
        request = youtube.playlistItems().list(
                part="snippet,contentDetails", 
                playlistId=playlist_id,
                maxResults = 50,
                pageToken = next_page_token)
        response = request.execute()

        for item in response['items']:
            temp={'VideoDate':item['contentDetails']['videoPublishedAt'],'Videoid':item['contentDetails']['videoId']}
            video_ids.append(temp)
        page=page+1
        if page==2:
            break
    
        next_page_token = response.get('nextPageToken')'''
        
    return video_ids
def dataprocessing(data_frame):
    numeric_cols = ['viewCount', 'likeCount', 'commentCount']
    
    data_frame[numeric_cols] = data_frame[numeric_cols].apply(pd.to_numeric, errors='coerce', axis=1)
    data_frame['publishedAt'] = data_frame['publishedAt'].apply(lambda x: parser.parse(x))
    data_frame['pushblishDayName'] = data_frame['publishedAt'].apply(lambda x: x.strftime("%A"))
    data_frame['durationSecs'] = data_frame['duration'].apply(lambda x: int(isodate.parse_duration(x).total_seconds()))
    data_frame['tagCount'] = data_frame['tags'].apply(lambda x: 0 if x is None else len(x))
    data_frame['description'] = data_frame['description'].str.replace('\n', ' ')
    return data_frame

def get_video_details(youtube, video_ids):
    all_video_info = []
    
    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
            part = "snippet,contentDetails,statistics",
            #id= video_ids[0:5]
            id = ','.join(video_ids[i:i+50])
        )
        
        response = request.execute()

        for video in response['items']:
            stats_to_keep = {'snippet': ['channelTitle', 'title','description', 'tags', 'publishedAt'],
                             'statistics': ['viewCount', 'likeCount', 'commentCount'],
                             'contentDetails': ['duration']
                            }
            video_info = {}
            video_info['video_id'] = video['id']
            video_info['URL']= 'https://www.youtube.com/watch?v='+video['id']

            for k in stats_to_keep.keys(): 
                for v in stats_to_keep[k]:
                    try:
                        video_info[v] = video[k][v]
                    except:
                        video_info[v] = None
            all_video_info.append(video_info)
            
    return pd.DataFrame(all_video_info)
    #return JSON(response)
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
    for i, row in enumerate(Item):
        for j, val in enumerate(row):
            if isinstance(val, list):
                Item[i][j] = ', '.join(val)  # Convert the list of tags to a comma-separated string
            elif isinstance(val, pd.Timestamp):
                Item[i][j] = val.strftime('%Y-%m-%d %H:%M:%S')
    worksheet.update(range_name=str(Top_Left_Index+':'+Bottom_Right_Index), values=Item)
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

api_service_name = "youtube"
api_version = "v3"
youtube = build(api_service_name, api_version, developerKey=api_key)
channel_details= sorted(channel_details, key=lambda x: x['channelName'])
channel_ids = [item['channelId'] for item in channel_details]
channel_stats = get_channel_stats(youtube, channel_ids)
playlist_details= channel_stats.sort_values(by=['channelName']).reset_index().drop(['index'], axis=1)[['channelName','playlistId','channelId']].to_dict('records')
Total=[]
for x in playlist_details:
    temp={}
    video_ids_temp=[]
    print("Fetching video ids: ", x['channelName'])
    try:
        video_ids_temp = get_video_ids(youtube, x['playlistId'])
    except HttpError:
        #Sadhguru_Turkey has no videos so it will show error
        video_ids_temp=[{'VideoDate':'2023-10-20T06:00:13Z','Videoid':'CqD5xcc5J1A'}]
    #pd.DataFrame(video_ids_temp).to_csv('Old_Video_Ids/'+str(date.today())+'/'+x['channelId']+'_'+str(date.today())+'.csv', header=True, index=False)
    temp={'channelName':x['channelName'],'channelId':x['channelId'],'playlistId':x['playlistId'], 'video_ids':video_ids_temp}
    Total.append(temp)
for x in Total:
    x['Final_vid']=[]
    for y in x['video_ids']:
        result_date = (datetime.strptime(str(date.today()), "%Y-%m-%d") - timedelta(days=1)).strftime('%Y-%m-%d')
        timestamp_object = datetime.fromisoformat(y['VideoDate'][:-1]).strftime('%Y-%m-%d')
        if result_date==timestamp_object:
            #print('Awesome'+' '+str(Lists[i]['Link']))
            x['Final_vid'].append(y['Videoid'])
video_total_df = []
i = 0
#os.makedirs(questions_directory, exist_ok=True)
while i < len(Total):
    try:
        # Check if 'Final_vid' is not empty before processing
        if Total[i]['Final_vid']:
            video_df = get_video_details(youtube, Total[i]['Final_vid'])
            print(Total[i]['channelName'])
            video_df = dataprocessing(video_df)
            video_total_df.append(video_df.to_dict(orient='records'))
        else:
            print(Total[i]['channelName'])
            video_df=[{'video_id': '','URL': '','channelTitle': Total[i]['channelName'],'title': '','description': '','tags': [],'publishedAt': '','viewCount': '','likeCount': '','commentCount': '','duration': '','pushblishDayName': '','durationSecs': '','tagCount': ''}]
            video_total_df.append(video_df)
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"Error processing {Total[i]['channelName']}: {e}")
        # Handle the exception, if required
        pass
    finally:
        i += 1   
j=0
while j<len(video_total_df):
    keys_to_remove = ['pushblishDayName', 'tagCount','tags','channelTitle','duration']
    for d in video_total_df[j]:
        for key in keys_to_remove:
            d.pop(key, None)
    insert_empty_row('1A91g9ZLMDCZniNjslw85XiaRXC8OEPpLHM5NLeRwpXA', channel_details[j]['Name'], 1, 1+len(video_total_df[j]))
    Top_left='A2'
    worksheet_update(video_total_df[j],'1A91g9ZLMDCZniNjslw85XiaRXC8OEPpLHM5NLeRwpXA',channel_details[j]['Name'],Top_left)
    gcx = gspread.service_account_from_dict(credens)
    worksheetx = gcx.open_by_key('1A91g9ZLMDCZniNjslw85XiaRXC8OEPpLHM5NLeRwpXA').worksheet(channel_details[j]['Name'])
    data = worksheetx.get_all_values()
    dfsheet = pd.DataFrame(data[1:], columns=data[0])  # Assumes the first row contains column names
    dfsheet = dfsheet.drop_duplicates(subset='video_id')
    worksheetx.clear()
    header = ['video_id','URL','title','description','publishedAt','viewCount','likeCount','commentCount','durationSecs']
    values = dfsheet.values.tolist()
    worksheetx.insert_rows([header] + values, 1)
    print('Added to the sheet: '+channel_details[j]['Name'])
    time.sleep(3)
    j=j+1
