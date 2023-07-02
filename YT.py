from googleapiclient.discovery import build
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from googleapiclient.http import BatchHttpRequest
import mysql.connector

api_key = "AIzaSyCpJ27SMPsz9bdtXGMxPNvR1A8Xbj9fuH4"
## Passing the channel ids in the form of list
channel_ids = ["UCoOHTipX1_cNiC9seIPfUXA",
               "UCCezIgC97PvUuR4_gbFUs5g",
               "UCBJycsmduvYEL83R_U4JriQ",
               "UCLt4d8cACHzrVvAz9gtaARA",
               "UC316GY-U17BkwN8D7oKM0iw"
               ]

youtube = build("youtube", "v3", developerKey=api_key)


## Function to extract the channel data from channel_id
# This function takes a service object and a list of channel ids

def get_channel_stats(youtube, channel_ids):
    all_data = []

    request = youtube.channels().list(
        part='snippet, contentDetails, statistics',
        id=','.join(channel_ids))
    response = request.execute()
    # This execute() method is called on the request object sending the api request

    for i in range(len(response['items'])):
        data = dict(channel_name=response['items'][i]['snippet']['title'],
                    subscriber=response['items'][i]['statistics']['subscriberCount'],
                    views=response['items'][i]['statistics']['viewCount'],
                    total_video=response['items'][i]['statistics']['videoCount'],
                    playlist_id=response['items'][i]['contentDetails']['relatedPlaylists']['uploads'])
        all_data.append(data)

    return all_data


## Here we are assigning the new variable to store all the data
channel_statistics = get_channel_stats(youtube, channel_ids)
print("-----------------------")

## Here we are creating a Dataframe using pandas
channel_data = pd.DataFrame(channel_statistics)
# print(channel_data)

## Cheking the data type of the dataframe
# print(channel_data.dtypes)
print()

## We are changing the data format from object to integer type
channel_data["subscriber"] = pd.to_numeric(channel_data["subscriber"])
channel_data["views"] = pd.to_numeric(channel_data["views"])
channel_data["total_video"] = pd.to_numeric(channel_data["total_video"])
# print(channel_data.dtypes)
print()

## Converting the list of dictionary to Dataframe
df = pd.DataFrame(channel_data)
# print(df)

sns.set(rc={'figure.figsize': (7, 7)})

## Create a subplot with 3 plots

# Plot-1: Subscriber Plot
sns.barplot(x='channel_name', y='subscriber', data=df)
plt.xlabel("Channel Name")
plt.ylabel("Subscribers Count")
plt.title("Channel Subscribers Counts")
# plt.show()

# Plot-2: View Count
sns.barplot(x='channel_name', y='views', data=df)
plt.xlabel("Channel Name")
plt.ylabel("Views")
plt.title("Channel Views Counts")
# plt.show()


# Plot-3: total_video Plot
sns.barplot(x='channel_name', y='total_video', data=df)
plt.xlabel("Channel Name")
plt.ylabel("total_video")
plt.title("Channel total_video Counts")
# plt.show()


## get the platlist id of a particular channel

playlist_id = channel_data.loc[channel_data['channel_name'] == 'Corey Schafer', 'playlist_id'].iloc[0]
# print(playlist_id)

## Function to get the Videos details
api_key = "AIzaSyCpJ27SMPsz9bdtXGMxPNvR1A8Xbj9fuH4"
youtube = build("youtube", "v3", developerKey=api_key)


# Defining a function to get the video details -- video ids
def get_video_ids(youtube, playlist_id):
    # video_ids to store the video ids in list
    video_ids = []

    # The next_page_token will help you to paginate through the playlist items if there are more than 50 items in playlist
    next_page_token = None

    while True:
        request = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=playlist_id,
            maxResults=50,
            # The page Token will allow us to paginate through the playlist items
            pageToken=next_page_token
        )
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


playlist_id = playlist_id
video_ids = get_video_ids(youtube, playlist_id)

## Creating a variable and storing all the data in the form of the list
videos_ids = get_video_ids(youtube, playlist_id)
# print(videos_ids)
print()


## Function to get the video details

def get_video_details(youtube, videos_ids):
    request = youtube.videos().list(
        part='snippet, statistics',
        id=','.join(videos_ids[:50])
    )
    response = request.execute()
    return response


# print(get_video_details(youtube, videos_ids))

## Extracting the data of all the videos

def get_video_details(youtube, videos_ids):
    all_videos_stats = []

    for i in range(0, len(videos_ids), 50):
        request = youtube.videos().list(
            part='snippet,statistics',
            id=','.join(videos_ids[i:i + 50]))
        response = request.execute()

        for video in response['items']:
            video_stats = dict(channel_name=video['snippet']['channelTitle'],
                               Title=video['snippet']['title'],
                               published_date=video['snippet']['publishedAt'],
                               views=video['statistics']['viewCount'],
                               likes=video['statistics']['likeCount'],
                               comments=video['statistics']['commentCount'])
            # The video_stats dictionary is appended to the all_videos_stats list.
            all_videos_stats.append(video_stats)
        return all_videos_stats


# print(get_video_details(youtube, videos_ids))

##creating a variable video_details to store the data
video_details = get_video_details(youtube, videos_ids)

## here we are creating a dataframe for video_data
video_data = pd.DataFrame(video_details)

#print(video_data.columns)

# converting the data type of views, like and comments
video_data['views'] = pd.to_numeric(video_data['views'])
video_data['likes'] = pd.to_numeric(video_data['likes'])
video_data['comments'] = pd.to_numeric(video_data['comments'])

#print(video_data.dtypes)

##Finding the top 10 videos

top_10_videos = video_data.sort_values(by = "views", ascending=False,).head(10)
#print(top_10_videos)

size = plt.subplots(figsize=(10,6))
sns.barplot(x='views', y='Title', data=top_10_videos)
#plt.show()


print("-------------------")
print("=====================")

##creating a connection with MySQL

con = mysql.connector.connect(host="localhost", user="root", password="Ashu@123", database="youtube_data")
print(con)
cursor = con.cursor()


def create_table():
    cursor.execute("CREATE TABLE Channel_table("
                 "Channel_ID varchar(50) PRIMARY KEY,"
                 "Channel_Name varchar(50),"
                 "Subscribers int,"
                 "Views int,"
                 "Total_videos int)")
    con.commit()
    cursor.execute("CREATE TABLE Video_table("
                 "Video_ID varchar(50) PRIMARY KEY,"
                 "Channel_Id varchar(50),"
                 "Title varchar(100),"
                 "Description TEXT,"
                 "Published_Date TIMESTAMP,"
                   "View_count int,"
                   "Like_count int,"

                   "Comment_Count int)")

    con.commit()
