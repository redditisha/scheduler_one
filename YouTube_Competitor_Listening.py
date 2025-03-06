from __future__ import print_function
from googleapiclient.discovery import build
from dateutil import parser
import pandas as pd
from IPython.display import JSON
import numpy as np
import re
import os
import json
import isodate
import datetime
from datetime import date
from datetime import datetime, timedelta
import gspread
import time
# from oauth2Client.service_account import ServiceAccountCredentials
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

api_key = os.getenv("YOUTUBE_API_KEY")

google_sheets_credentials_json = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
if not google_sheets_credentials_json:
    raise ValueError("Error: GOOGLE_SHEETS_CREDENTIALS not found. Make sure it is set in GitHub Secrets.")

# Convert JSON string back into a dictionary
credens = json.loads(google_sheets_credentials_json)
print("Google Sheets credentials loaded successfully.")

def empty_row():
    try:
        service = build('sheets', 'v4', credentials=creds)
        body = {
            'requests': [
                {
                    "insertDimension": {
                        "range": {
                            "sheetId": 0,
                            "dimension": "ROWS",
                            "startIndex": 2,
                            "endIndex": 3
                        },
                        "inheritFromBefore": True
                    }
                },
            ]
        }

        service.spreadsheets().batchUpdate(
            spreadsheetId='1UR-Lpp9KYnSD7ah3qhLL4NjMnHzmqDiwpMp71ggyBAg',
            body=body).execute()

    except HttpError as error:
        print(f"An error occurred: {error}")
        return error
def worksheet_update(Channel_Details,sheet_id,worksheet_num,Top_left):
    gc = gspread.service_account_from_dict(credens)
    sheets = gc.open_by_key(str(sheet_id))
    worksheet = sheets.get_worksheet(int(worksheet_num))
    Top_Left_Index=str(Top_left)
    #headers = list(Channel_Details[0].keys())
    Num_In_Details=len(Channel_Details[0])
    Total_Items=len(Channel_Details)*Num_In_Details
    Bottom_Right_Index= next_letter(re.match(r"([A-Za-z]+)(\d+)", Top_Left_Index).group(1).upper(),Num_In_Details).upper()+str(int(re.match(r"([A-Z]+)(\d+)", Top_Left_Index).group(2))+len(Channel_Details)-1)
    Item=[]
    for Rows in Channel_Details:
        temp=[]
        for Column_Values in Rows.values():
            temp.append(Column_Values)
        Item.append(temp)
    worksheet.update(Item, str(Top_Left_Index+':'+Bottom_Right_Index))
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
def get_channel_stats(youtube, channel_ids):
    channel_id_list = [channel["ChannelID"] for channel in channel_ids]
    all_data = []
    # Process channel IDs in chunks of 50
    for i in range(0, len(channel_id_list), 50):
        # Select the current batch of 50 channel IDs
        current_batch = channel_id_list[i:i + 50]
        
        # Make the API request for the current batch
        request = youtube.channels().list(
            part="snippet, contentDetails, statistics",
            id=','.join(current_batch),
            maxResults=50
        )
        
        # Execute the request
        response2 = request.execute()
        
        # Process the response data
        for item in response2['items']:
            data = {
                'subscribers': item['statistics']['subscriberCount'],
                'views': item['statistics']['viewCount'],
                'totalVideos': item['statistics']['videoCount'],
                'playlistId': item['contentDetails']['relatedPlaylists']['uploads'],
                'channelId': item['id'],
                'Run on': str(date.today())
            }
            all_data.append(data)
    df1 = pd.DataFrame(channel_ids)
    df2 = pd.DataFrame(all_data)
    merged_df = df1.merge(df2, left_on="ChannelID", right_on="channelId", how="inner")
    merged_df = merged_df.drop(columns=["channelId"])
    
    # Return the data as a pandas DataFrame
    return merged_df
def get_video_ids(youtube, playlist_id, countof50):
    countof50 = int(countof50)
    video_ids = []
    
    request = youtube.playlistItems().list(
        part="snippet,contentDetails", 
        playlistId=playlist_id,
        maxResults = 50
    )
    response = request.execute()
    
    for item in response['items']:
        video_ids.append(item['contentDetails']['videoId'])

    next_page_token = response.get('nextPageToken')
    if countof50 == 1:
        return video_ids
    elif countof50 > 1:
        page=1
        while next_page_token is not None:
            request = youtube.playlistItems().list(
                    part="snippet,contentDetails", 
                    playlistId=playlist_id,
                    maxResults = 50,
                    pageToken = next_page_token)
            response = request.execute()
    
            for item in response['items']:
                video_ids.append(item['contentDetails']['videoId'])
            page=page+1
            if page==countof50:
                break
        
            next_page_token = response.get('nextPageToken')
            
        return video_ids
    else:
        return []
def dataprocessing(data_frame):
    numeric_cols = ['viewCount', 'likeCount', 'commentCount']
    data_frame_mod = data_frame.copy()
    
    # Convert numeric columns to numeric types
    data_frame_mod[numeric_cols] = data_frame[numeric_cols].apply(pd.to_numeric, errors='coerce', axis=1)
    
    # Parse the published date
    data_frame_mod['publishedAt'] = data_frame['publishedAt'].apply(lambda x: parser.parse(x) if pd.notnull(x) else None)
    data_frame_mod['channelTitle'] = data_frame['channelTitle'].apply(lambda x: x.strip())
    
    # Get the day name from the published date
    data_frame_mod['pushblishDayName'] = data_frame_mod['publishedAt'].apply(lambda x: x.strftime("%A") if pd.notnull(x) else None)
    
    # Convert ISO duration to seconds
    data_frame_mod['durationSecs'] = data_frame['duration'].apply(lambda x: isodate.parse_duration(x).total_seconds() if pd.notnull(x) else None)
    
    # Convert published date to a string in the format YYYY-MM-DD
    data_frame_mod['publishedAt'] = pd.to_datetime(data_frame_mod['publishedAt']).dt.strftime("%Y-%m-%d")
    
    # Count the number of tags
    data_frame_mod['tagCount'] = data_frame['tags'].apply(lambda x: 0 if x is None else len(x))
    
    return data_frame_mod
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
            stats_to_keep = {'snippet': ['channelTitle', 'title', 'description','tags', 'publishedAt'],
                             'statistics': ['viewCount', 'likeCount', 'commentCount'],
                             'contentDetails': ['duration']
                            }
            video_info = {}
            video_info['video_id'] = video['id']
            video_info['URL']= 'https://www.youtube.com/watch?v='+video['id']
            video_info['TnURL']='https://img.youtube.com/vi/'+video['id']+'/maxresdefault.jpg'

            for k in stats_to_keep.keys(): 
                for v in stats_to_keep[k]:
                    try:
                        video_info[v] = video[k][v]
                    except:
                        video_info[v] = None
            all_video_info.append(video_info)
            
    return pd.DataFrame(all_video_info)
    #return JSON(response)
def next_index2(index_text,Num_top):
    Top_Left_Index=index_text
    Total_Items=Num_top
    Bottom_Right_Index= re.match(r"([A-Za-z]+)(\d+)", Top_Left_Index).group(1).upper()+str(int(re.match(r"([A-Z]+)(\d+)", Top_Left_Index).group(2))+Total_Items)
    return Bottom_Right_Index
def clear_worksheet(sheet_id, worksheet_num):
    gc = gspread.service_account_from_dict(credens)  # Authenticate
    sheets = gc.open_by_key(sheet_id)  # Open the spreadsheet
    worksheet = sheets.get_worksheet(int(worksheet_num))  # Get the worksheet

    worksheet.clear()
def read_gsheet_to_df(sheet_id, worksheet_num, credens):
    """
    Reads a Google Sheet and returns a Pandas DataFrame.
    
    :param sheet_id: The ID of the Google Sheet.
    :param worksheet_num: The index of the worksheet (starting from 0).
    :return: Pandas DataFrame containing the sheet data.
    """
    # Load credentia
    
    # Authenticate with gspread
    gc = gspread.service_account_from_dict(credens)
    
    # Open the Google Sheet
    sheet = gc.open_by_key(sheet_id)
    worksheet = sheet.get_worksheet(worksheet_num)
    
    # Get all data from the worksheet
    data = worksheet.get_all_values()
    
    # Convert to DataFrame
    df = pd.DataFrame(data[1:], columns=data[0])  # First row as column names
    
    return df
api_service_name = "youtube"
api_version = "v3"

# Get credentials and create an API client
youtube = build(api_service_name, api_version, developerKey=api_key)
#Get Competitor's Details from Sheet, from Competitors Tab
sheet_id = "1OkErK2H6kCxByp0S3YX-M1LeDyEuOHfnGh84NBiT1PE"
worksheet_num = 0
dfchannel = read_gsheet_to_df(sheet_id, worksheet_num, credens)
#df.head()
dfchannel_dict = dfchannel.to_dict(orient='records')[:3]
#dfchannel.head(2)
#Get Existing Data on Sheet, from Masters Tab
sheet_id = "1OkErK2H6kCxByp0S3YX-M1LeDyEuOHfnGh84NBiT1PE"
worksheet_num = 1
dfexisting = read_gsheet_to_df(sheet_id, worksheet_num, credens)
#df.head()
#df_dict = df.to_dict(orient='records')
#dfexisting.head(2)
channel_stats = get_channel_stats(youtube, dfchannel_dict).sort_values(by=['Name']).reset_index().drop(['index'], axis=1).to_dict('records')

for x in channel_stats:
    video_ids_temp=[]
    #x['video_ids'] = []
    print("Fetching video ids: ", x['Name'])
    try:
        video_ids_temp = get_video_ids(youtube, x['playlistId'],x['CountsOf50'])
    except HttpError:
        #Sadhguru_Turkey has no videos so it will show error
        video_ids_temp=['CqD5xcc5J1A']
    #pd.DataFrame(video_ids_temp).to_csv('Old_Video_Ids/'+str(date.today())+'/'+x['channelId']+'_'+str(date.today())+'.csv', header=True, index=False)
    #temp={'channelName':x['channelName'],'channelId':x['channelId'],'playlistId':x['playlistId'], 'video_ids':video_ids_temp}
    x['video_ids']=video_ids_temp
    
i = 0
all_stats_x = pd.DataFrame()
#os.makedirs(questions_directory, exist_ok=True)

while i < len(channel_stats):
    try:
        # Get video details
        video_df = get_video_details(youtube, channel_stats[i]['video_ids'])
        video_df = dataprocessing(video_df)

        # Add additional details to every row of video_df
        video_df['channelTitle'] = channel_stats[i]['Name']
        video_df['Subscribers'] = int(channel_stats[i]['subscribers'])
        video_df['Category'] = channel_stats[i]['Catagory']
        video_df['Geo'] = channel_stats[i]['Geo']
        if 'tags' in video_df.columns:
            video_df['tags'] = video_df['tags'].apply(lambda x: ", ".join(map(str, x)) if isinstance(x, list) else str(x))

    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"Skipping {channel_stats[i]['Name']} due to error: {e}")
        i += 1
        continue

    print(channel_stats[i]['Name'])

    # Append to all_stats_x
    all_stats_x = pd.concat([all_stats_x, video_df[['video_id', 'URL', 'TnURL', 'channelTitle', 'title', 'publishedAt', 'viewCount', 'likeCount', 'commentCount', 'durationSecs', 'tags','Subscribers', 'Category', 'Geo']]], ignore_index=True)
    
    # Save individual channel data
    #filename = questions_directory + '-'.join(channel_stats[i]['Name'].strip().split(' ')) + '_' + channel_stats[i]['ChannelID'] + '_' + str(date.today()) + '.csv'
    #video_df[['video_id', 'URL', 'TnURL', 'channelTitle', 'title', 'publishedAt', 'viewCount', 'likeCount', 'commentCount', 'durationSecs', 'tags','Subscribers', 'Category', 'Geo']].to_csv(filename, header=True, index=False)
    i += 1
dfexisting = dfexisting.drop(columns=['AvgViews'])
Finalstats= pd.concat([all_stats_x, dfexisting], ignore_index=True)
Finalstats['publishedAt'] = pd.to_datetime(Finalstats['publishedAt'])
cutoff_date = datetime.today() - timedelta(days=45)
df_filtered = Finalstats[Finalstats['publishedAt'] >= cutoff_date]
df_filtered['publishedAt'] = df_filtered['publishedAt'].dt.strftime('%Y-%m-%d')
df_filtered['publishedAt'] = df_filtered['publishedAt'].apply(str)
cols_to_convert = ['viewCount', 'likeCount', 'commentCount','durationSecs','Subscribers']  # List of columns to convert
df_filtered[cols_to_convert] = df_filtered[cols_to_convert].apply(pd.to_numeric, errors='coerce')
df_filtered = df_filtered.sort_values(by=['publishedAt', 'viewCount'], ascending=[False, False]).drop_duplicates(subset='video_id', keep='first')
avg_views_per_channel = df_filtered.groupby('channelTitle')['viewCount'].mean().reset_index()
avg_views_per_channel.rename(columns={'viewCount': 'AvgViews'}, inplace=True)
df_filtered = df_filtered.merge(avg_views_per_channel, on='channelTitle', how='left')
df_filtered['AvgViews'] = df_filtered['AvgViews'].round(0).fillna(0).astype(int)
df_filtered = df_filtered.fillna("")

all_stats_dict = df_filtered.to_dict('records')
temp_dict = {key: key for key in all_stats_dict[0].keys()}
clear_worksheet('1OkErK2H6kCxByp0S3YX-M1LeDyEuOHfnGh84NBiT1PE', 1)
worksheet_update([temp_dict],'1OkErK2H6kCxByp0S3YX-M1LeDyEuOHfnGh84NBiT1PE',1,'A1')
worksheet_update(all_stats_dict,'1OkErK2H6kCxByp0S3YX-M1LeDyEuOHfnGh84NBiT1PE',1,'A2')
