from googleapiclient.discovery import build
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from googleapiclient.errors import HttpError
from googleapiclient.http import BatchHttpRequest
import mysql.connector

api_key_1 = "AIzaSyCpJ27SMPsz9bdtXGMxPNvR1A8Xbj9fuH4"
channel_ids = ["UCBJycsmduvYEL83R_U4JriQ",
               "UCoOHTipX1_cNiC9seIPfUXA"
               ]

youtube = build("youtube", "v3", developerKey=api_key_1)


def get_channel_data(youtube, channel_ids):  # channel()
    all_data = []
    request = youtube.channels().list(
        part="snippet, contentDetails, statistics",
        id=','.join(channel_ids))
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



def get_video_all_info(youtube, channel_ids):
    request = youtube.channels().list(
        part="snippet, contentDetails, contentDetails",
        id=','.join(channel_ids))
    response = request.execute()
    return response


# Function to retrieve playlist IDs for a given channel ID
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
channel_id_1 = 'UCBJycsmduvYEL83R_U4JriQ'
channel_id_2 = 'UCoOHTipX1_cNiC9seIPfUXA'

# Retrieve playlist IDs for each channel
playlist_ids_1 = get_playlist_ids(channel_id_1)
playlist_ids_2 = get_playlist_ids(channel_id_2)


play=playlist_ids_2+playlist_ids_1



# Function to retrieve video IDs for a given playlist ID
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
playlist_ids = play

# Retrieve video IDs for each playlist
all_video_ids = []
for playlist_id in playlist_ids:
    video_ids = get_video_ids(playlist_id)
    all_video_ids.extend(video_ids)




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

# List of video IDs to retrieve video data from


# Retrieve video data for each video ID
video_data_list = []

try:
    for i in all_video_ids:
        data=get_video_data(i)
        video_data_list.append(data)
except:
    pass

print(video_data_list)



