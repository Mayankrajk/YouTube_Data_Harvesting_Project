from googleapiclient.discovery import build
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from googleapiclient.http import BatchHttpRequest
import mysql.connector

api_key = "AIzaSyCpJ27SMPsz9bdtXGMxPNvR1A8Xbj9fuH4"
channel_ids = ["UCBJycsmduvYEL83R_U4JriQ",
               "UCoOHTipX1_cNiC9seIPfUXA"
               ]

youtube = build("youtube", "v3", developerKey=api_key)


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


def get_playlist_id(youtube, channel_ids):  # getting the playlist id
    all_data = []

    request = youtube.channels().list(
        part="snippet, contentDetails, statistics",
        id=','.join(channel_ids))
    response = request.execute()

    for i in range(len(response['items'])):
        playlist_id = response['items'][i]['contentDetails']['relatedPlaylists']['uploads']
        all_data.append(playlist_id)

    return all_data


playlist_ids = ['PL2zq7klxX5ASt4dLSAd2FMoY3Og3V0jZv', 'PL8vL-_f27zDT9iMJKAeReWdAikk5d-TQr']
'''for i in get_playlist_id(youtube, channel_ids):
    playlist_ids.append(i)'''

print(playlist_ids)

api_key = "AIzaSyCpJ27SMPsz9bdtXGMxPNvR1A8Xbj9fuH4"
youtube = build("youtube", "v3", developerKey=api_key)


def get_video_ids(youtube, playlist_ids):
    # video_ids to store the video ids in list
    video_ids = []

    # The next_page_token will help you to paginate through the playlist items if there are more than 50 items in playlist
    next_page_token = None

    while True:
        request = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=','.join(playlist_ids),
            maxResults=50,
            # The page Token will allow us to paginate through the playlist items
            pageToken=next_page_token
        )
        print("Hi ", request)
        # The API request is executed and stored in the response variable
        response = request.execute()
        # From the response, the code retrieves the "items" list using the get() method
        items = response.get('items', [])

        for item in items:
            video_ids.append(item["contentDetails"]['videoId'])
        next_page_token = response.get('nextPageToken')

        if not next_page_token:
            break
    return video_ids


## Creating a variable and storing all the data in the form of the list
videos_ids = get_video_ids(youtube, playlist_ids)


def get_video_details(youtube, videos_ids):
    request = youtube.videos().list(
        part='snippet, statistics',
        id=','.join(videos_ids[:50])
    )
    response = request.execute()
    return response
