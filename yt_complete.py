from googleapiclient.discovery import build
import re
import pandas as pd
import numpy as np
from googleapiclient.errors import HttpError
from pymongo import MongoClient
import mysql.connector
import streamlit as st
from streamlit_option_menu import option_menu
import seaborn as sns

api_key_1 = "AIzaSyCu13IWqtNlZaQawS526-J7YLymJtj_QWM"
channel_id1 = "UCCezIgC97PvUuR4_gbFUs5g"  # corey
channel_id2 = "UCxX9wt5FWQUAAz4UrysqK9A"  # CS Dojo
channel_id3 = "UC42pOSNg804f1wCcj7qL0mA"  # coding with John
channel_id4 = "UCmtyQOKKmrMVaKuRXz02jbQ"  # Sebastian Lague
channel_id5 = "UCYO_jab_esuFRV4b17AJtAw"  # 3BlueBrown
youtube = build("youtube", "v3", developerKey=api_key_1)


def get_channel_data(youtube, channel_ids):  # channel()
    all_data = []
    request = youtube.channels().list(
        part="snippet, contentDetails, statistics",
        id=channel_ids)
    response = request.execute()

    try:
        for i in range(len(response['items'])):
            data = dict(channel_name=response['items'][i]['snippet']['title'],
                        subscriber=response['items'][i]['statistics']['subscriberCount'],
                        views=response['items'][i]['statistics']['viewCount'],
                        total_video=response['items'][i]['statistics']['videoCount'],
                        playlist_id=response['items'][i]['contentDetails']['relatedPlaylists']['uploads'])
            all_data.append(data)

        return all_data
    except KeyError:
        return False


# print(get_channel_data(youtube, channel_id2))  # ---------------------------------------


def get_video_all_info(youtube, channel_ids):
    request = youtube.channels().list(
        part="snippet, contentDetails, contentDetails",
        id=channel_ids)
    response = request.execute()
    return response


def get_playlist_ids(channel_id):
    playlist_ids = []

    # Retrieve the first page of playlists
    request = youtube.playlists().list(
        part='snippet',
        channelId=channel_id,
        maxResults=50  # Adjust the maximum number of playlists per page if needed
    )
    response = request.execute()

    # Extract the playlist IDs
    for playlist in response['items']:
        playlist_ids.append(playlist['id'])

    # Retrieve additional pages if available
    while 'nextPageToken' in response:
        request = youtube.playlists().list(
            part='snippet',
            channelId=channel_id,
            maxResults=50,
            pageToken=response['nextPageToken']
        )
        response = request.execute()

        # Extract the playlist IDs
        for playlist in response['items']:
            playlist_ids.append(playlist['id'])

    return playlist_ids


# Channel IDs to retrieve playlist IDs from

channel_id1 = "UCCezIgC97PvUuR4_gbFUs5g"  # corey
channel_id2 = "UCxX9wt5FWQUAAz4UrysqK9A"  # CS Dojo
channel_id3 = "UC42pOSNg804f1wCcj7qL0mA"  # coding with John
channel_id4 = "UCmtyQOKKmrMVaKuRXz02jbQ"  # Sebastian Lague
channel_id5 = "UCYO_jab_esuFRV4b17AJtAw"  # 3BlueBrown

# Retrieve playlist IDs for each channel
playlist_ids_1 = get_playlist_ids(channel_id1)
playlist_ids_2 = get_playlist_ids(channel_id2)
playlist_ids_3 = get_playlist_ids(channel_id3)
playlist_ids_4 = get_playlist_ids(channel_id4)
playlist_ids_5 = get_playlist_ids(channel_id5)


def get_video_ids(playlist_id):
    video_ids = []

    # Retrieve the first page of videos in the playlist
    request = youtube.playlistItems().list(
        part='contentDetails',
        playlistId=playlist_id,
        maxResults=50  # Adjust the maximum number of videos per page if needed
    )
    response = request.execute()

    # Extract the video IDs
    for video in response['items']:
        video_ids.append(video['contentDetails']['videoId'])

    # Retrieve additional pages if available
    while 'nextPageToken' in response:
        request = youtube.playlistItems().list(
            part='contentDetails',
            playlistId=playlist_id,
            maxResults=50,
            pageToken=response['nextPageToken']
        )
        response = request.execute()

        # Extract the video IDs
        for video in response['items']:
            video_ids.append(video['contentDetails']['videoId'])

    return video_ids


# List of playlist IDs to retrieve video IDs from
playlist_id1 = playlist_ids_1
playlist_id2 = playlist_ids_2
playlist_id3 = playlist_ids_3
playlist_id4 = playlist_ids_4
playlist_id5 = playlist_ids_5

# Retrieve video IDs for each playlist_1
all_video_ids_1 = []
for playlist_id in playlist_id1:
    video_ids = get_video_ids(playlist_id)
    all_video_ids_1.extend(video_ids)

# Retrieve video IDs for each playlist_2
all_video_ids_2 = []
for playlist_id in playlist_id2:
    video_ids = get_video_ids(playlist_id)
    all_video_ids_2.extend(video_ids)

# Retrieve video IDs for each playlist_3
all_video_ids_3 = []
for playlist_id in playlist_id3:
    video_ids = get_video_ids(playlist_id)
    all_video_ids_3.extend(video_ids)

# Retrieve video IDs for each playlist_4
all_video_ids_4 = []
for playlist_id in playlist_id4:
    video_ids = get_video_ids(playlist_id)
    all_video_ids_4.extend(video_ids)

# Retrieve video IDs for each playlist_5
all_video_ids_5 = []
for playlist_id in playlist_id5:
    video_ids = get_video_ids(playlist_id)
    all_video_ids_5.extend(video_ids)


def get_video_data(video_id):
    request = youtube.videos().list(
        part='snippet,contentDetails, statistics',
        id=video_id
    )
    response = request.execute()

    video_data = dict(video_id=response['items'][0]['id'],
                      channel_id=response['items'][0]['snippet']['channelId'],
                      video_name=response['items'][0]['snippet']['title'],
                      video_description=response['items'][0]['snippet']['description'],
                      channel_title=response['items'][0]['snippet']['channelTitle'],
                      category_id=response['items'][0]['snippet']['categoryId'],
                      view_count=response['items'][0]['statistics']['viewCount'],
                      like_count=response['items'][0]['statistics']['likeCount'],
                      comment_count=response['items'][0]['statistics']['commentCount'],
                      thumbnail=response['items'][0]['snippet']['thumbnails']['default']['url'])

    return video_data


# Retrieve video data for each video ID
video_data_list_1 = []
for i in all_video_ids_1:
    data = get_video_data(i)
    video_data_list_1.append(data)

# Retrieve video data for each video ID
video_data_list_2 = []
for i in all_video_ids_2:
    data = get_video_data(i)
    video_data_list_2.append(data)

# Retrieve video data for each video ID
video_data_list_3 = []
for i in all_video_ids_3:
    data = get_video_data(i)
    video_data_list_3.append(data)

# Retrieve video data for each video ID
video_data_list_4 = []
for i in all_video_ids_4:
    data = get_video_data(i)
    video_data_list_4.append(data)

# Retrieve video data for each video ID
video_data_list_5 = []
for i in all_video_ids_5:
    data = get_video_data(i)
    video_data_list_5.append(data)


def get_comments(video_id):
    comments = []

    # Retrieve the first page of comments
    request = youtube.commentThreads().list(
        part='snippet, replies',
        videoId=video_id,
        maxResults=5 # Adjust the maximum number of comments per page if needed
    )
    response = request.execute()

    # Extract the comments
    for i in range(len(response['items'])):
        data = dict(video_id=response['items'][i]['snippet']['videoId'],
                    comment_id=response['items'][i]['id'],
                    comment_text=response['items'][i]['snippet']['topLevelComment']['snippet']['textDisplay'],
                    comment_author=response['items'][i]['snippet']['topLevelComment']['snippet']['authorDisplayName'],

                    published_date=re.findall(r'(\d{4}-\d{2}-\d{2})',
                                              response['items'][i]['snippet']['topLevelComment']['snippet'][
                                                  'publishedAt'])[0])

        comments.append(data)

    return comments


# List of video IDs to retrieve comments from channel_1
video_ids = all_video_ids_1
# Retrieve comments for each video ID
all_comments_1 = []
try:
    for video_id in video_ids:
        comments = get_comments(video_id)
        all_comments_1.extend(comments)
except:
    pass
# print(all_comments_1)  # ---------------------------------------------------------------------

# List of video IDs to retrieve comments from channel_2
video_ids = all_video_ids_2
# Retrieve comments for each video ID
all_comments_2 = []
try:
    for video_id in video_ids:
        comments = get_comments(video_id)
        all_comments_2.extend(comments)
except:
    pass
# print(all_comments_2)  # ---------------------------------------------------------------------

# List of video IDs to retrieve comments from channel_3
video_ids = all_video_ids_3
# Retrieve comments for each video ID
all_comments_3 = []
try:
    for video_id in video_ids:
        comments = get_comments(video_id)
        all_comments_3.extend(comments)
except:
    pass
# print(all_comments_3)           # ---------------------------------------------------------------------

# List of video IDs to retrieve comments from channel_4
video_ids = all_video_ids_4
# Retrieve comments for each video ID
all_comments_4 = []
try:
    for video_id in video_ids:
        comments = get_comments(video_id)
        all_comments_4.extend(comments)
except:
    pass
# print(all_comments_4)             # ---------------------------------------------------------------------

# List of video IDs to retrieve comments from channel_5
video_ids = all_video_ids_5
# Retrieve comments for each video ID
all_comments_5 = []
try:
    for video_id in video_ids:
        comments = get_comments(video_id)
        all_comments_5.extend(comments)
except:
    pass
# print(all_comments_5)            # ---------------------------------------------------------------------

df_channel_data_1 = pd.DataFrame(get_channel_data(youtube, channel_id1))
df_channel_data_2 = pd.DataFrame(get_channel_data(youtube, channel_id2))
df_channel_data_3 = pd.DataFrame(get_channel_data(youtube, channel_id3))
df_channel_data_4 = pd.DataFrame(get_channel_data(youtube, channel_id4))
df_channel_data_5 = pd.DataFrame(get_channel_data(youtube, channel_id5))
df_video_data_1 = pd.DataFrame(video_data_list_1)
df_video_data_2 = pd.DataFrame(video_data_list_2)
df_video_data_3 = pd.DataFrame(video_data_list_3)
df_video_data_4 = pd.DataFrame(video_data_list_4)
df_video_data_5 = pd.DataFrame(video_data_list_5)
df_comment_data_1 = pd.DataFrame(all_comments_1)
df_comment_data_2 = pd.DataFrame(all_comments_2)
df_comment_data_3 = pd.DataFrame(all_comments_3)
df_comment_data_4 = pd.DataFrame(all_comments_4)
df_comment_data_5 = pd.DataFrame(all_comments_5)

'''df_channel_data_1_csv=df_channel_data_1.to_csv("df_channel_data_1.csv", index=False)
df_channel_data_2_csv=df_channel_data_2.to_csv("df_channel_data_2.csv", index=False)
df_channel_data_3_csv=df_channel_data_3.to_csv("df_channel_data_3.csv", index=False)
df_channel_data_4_csv=df_channel_data_4.to_csv("df_channel_data_4.csv", index=False)
df_channel_data_5_csv=df_channel_data_5.to_csv("df_channel_data_5.csv", index=False)

df_video_data_1_csv=df_video_data_1.to_csv("df_video_data_1_csv.csv", index=False)
df_video_data_2_csv=df_video_data_2.to_csv("df_video_data_2_csv.csv", index=False)
df_video_data_3_csv=df_video_data_3.to_csv("df_video_data_3_csv.csv", index=False)
df_video_data_4_csv=df_video_data_4.to_csv("df_video_data_4_csv.csv", index=False)
df_video_data_5_csv=df_video_data_5.to_csv("df_video_data_5_csv.csv", index=False)

df_comment_data_1_csv=df_comment_data_1.to_csv("df_comment_data_1_csv.csv", index=False)
df_comment_data_2_csv=df_comment_data_2.to_csv("df_comment_data_2_csv.csv", index=False)
df_comment_data_3_csv=df_comment_data_3.to_csv("df_comment_data_3_csv.csv", index=False)
df_comment_data_4_csv=df_comment_data_4.to_csv("df_comment_data_4_csv.csv", index=False)
df_comment_data_5_csv=df_comment_data_5.to_csv("df_comment_data_5_csv.csv", index=False)'''

'''print(df_channel_data_1)                        # ---------------------------------------------------------------------
print("=============================")
print(df_channel_data_2)                        # ---------------------------------------------------------------------
print("=============================")

print(df_channel_data_3)                        # ---------------------------------------------------------------------
print("=============================")

print(df_channel_data_4)                        # ---------------------------------------------------------------------
print("=============================")

print(df_channel_data_5)                        # ---------------------------------------------------------------------
print("=============================")'''

'''print(len(df_video_data_1))
print(len(df_video_data_2))
print(len(df_video_data_3))
print(len(df_video_data_4))
print(len(df_video_data_5))
'''
print("=============================")

'''print(len(df_comment_data_1))
print(len(df_comment_data_2))
print(len(df_comment_data_3))
print(len(df_comment_data_4))
print(len(df_comment_data_5))'''

df_channel_data_all = pd.concat(
    [df_channel_data_1, df_channel_data_2, df_channel_data_3, df_channel_data_4, df_channel_data_5])
# print(df_channel_data_all)  #---------------------------------------------------------

df_video_data_all = pd.concat([df_video_data_1, df_video_data_2, df_video_data_3, df_video_data_4, df_video_data_5])
# print(df_video_data_all)         #-----------------------------------------------

df_comments_data_all = pd.concat(
    [df_comment_data_1, df_comment_data_2, df_comment_data_3, df_comment_data_4, df_comment_data_5])
# print(df_comments_data_all)    #---------------------------------------------------------

df_channel_data_all_csv=df_channel_data_all.to_csv("df_channel_data_all_csv.csv", index=False)

df_video_data_all_csv=df_video_data_all.to_csv("df_video_data_all_csv.csv", index=False)

df_comments_data_all_csv=df_comments_data_all.to_csv("df_comments_data_all_csv.csv", index=False)

# =============================================================================#


'''client = MongoClient("mongodb://localhost:27017")
print(client.test)
print(client.list_database_names())
print()'''

'''df_channel_data_all.reset_index(inplace=True)
df_video_data_all.reset_index(inplace=True)
df_comments_data_all.reset_index(inplace=True)'''

'''channel_dict=df_channel_data_all.to_dict('records')
video_dict=df_video_data_all.to_dict('records')
comments_dict=df_comments_data_all.to_dict('records')'''

print("------------")

'''new_db=client['youtube_project']
print(client.list_database_names())'''

'''new_col_channel=new_db['channel_data']
new_col_video=new_db['video_data']
new_col_comments=new_db['comments_data']'''

'''new_col_channel.insert_many(channel_dict)
new_col_video.insert_many(video_dict)
new_col_comments.insert_many(comments_dict)'''

# ================================================================#

'''con = mysql.connector.connect(host="localhost", user="root", password="Ashu@123", database="youtube_project")
print(con)
cursor = con.cursor()'''

# Inserting the channel data to SQL

'''
for row in df_channel_data_all.itertuples(index=False):
    insert_query = "INSERT INTO channel_data (channel_name, subscriber, views, total_video, playlist_id) VALUES (%s, " \
                   "%s, %s, " \
                   "%s, %s)"
    cursor.execute(insert_query, row)
# Commit the changes to the database
con.commit()'''

'''
try:
    for row in df_video_data_all.itertuples(index=False):
        insert_query = "INSERT INTO video_data (video_id, channel_id, video_name, video_description, channel_title, " \
                       "category_id, view_count, like_count, comment_count, thumbnail) VALUES (%s, " \
                       "%s, %s, " \
                       "%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_query, row)
except:
    pass
# Commit the changes to the database
con.commit()
cursor.close()
con.close()
'''

'''
try:
    for row in df_comments_data_all.itertuples(index=False):
        insert_query = "INSERT INTO comments_data (video_id, comment_id, comment_text, comment_author, published_date) " \
                       "VALUES (%s, " \
                       "%s, %s, " \
                       "%s, %s)"
        cursor.execute(insert_query, row)
except:
    pass
# Commit the changes to the database
con.commit()

# Close the cursor and connection
cursor.close()
con.close()

'''

print("Done Migrating the Data.")

# ----------------------------------------------------------------------#
# ----------------------------------------------------------------------#

# ----------------------------------------------------------------------#
# ----------------------------------------------------------------------#
