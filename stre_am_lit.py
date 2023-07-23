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

df_channel_data_1=pd.read_csv(r"C:\Users\mkolwal\PycharmProjects\YT_Project\df_channel_data_1.csv")
df_channel_data_2=pd.read_csv(r"C:\Users\mkolwal\PycharmProjects\YT_Project\df_channel_data_2.csv")
df_channel_data_3=pd.read_csv(r"C:\Users\mkolwal\PycharmProjects\YT_Project\df_channel_data_3.csv")
df_channel_data_4=pd.read_csv(r"C:\Users\mkolwal\PycharmProjects\YT_Project\df_channel_data_4.csv")
df_channel_data_5=pd.read_csv(r"C:\Users\mkolwal\PycharmProjects\YT_Project\df_channel_data_5.csv")

df_video_data_1=pd.read_csv(r"C:\Users\mkolwal\PycharmProjects\YT_Project\df_video_data_1_csv.csv")
df_video_data_2=pd.read_csv(r"C:\Users\mkolwal\PycharmProjects\YT_Project\df_video_data_2_csv.csv")
df_video_data_3=pd.read_csv(r"C:\Users\mkolwal\PycharmProjects\YT_Project\df_video_data_3_csv.csv")
df_video_data_4=pd.read_csv(r"C:\Users\mkolwal\PycharmProjects\YT_Project\df_video_data_4_csv.csv")
df_video_data_5=pd.read_csv(r"C:\Users\mkolwal\PycharmProjects\YT_Project\df_video_data_5_csv.csv")

df_comment_data_1=pd.read_csv(r"C:\Users\mkolwal\PycharmProjects\YT_Project\df_comment_data_1_csv.csv")
df_comment_data_2=pd.read_csv(r"C:\Users\mkolwal\PycharmProjects\YT_Project\df_comment_data_2_csv.csv")
df_comment_data_3=pd.read_csv(r"C:\Users\mkolwal\PycharmProjects\YT_Project\df_comment_data_3_csv.csv")
df_comment_data_4=pd.read_csv(r"C:\Users\mkolwal\PycharmProjects\YT_Project\df_comment_data_4_csv.csv")
df_comment_data_5=pd.read_csv(r"C:\Users\mkolwal\PycharmProjects\YT_Project\df_comment_data_5_csv.csv")


df_channel_data_all=pd.read_csv(r"C:\Users\mkolwal\PycharmProjects\YT_Project\df_channel_data_all_csv.csv")

df_video_data_all=pd.read_csv(r"C:\Users\mkolwal\PycharmProjects\YT_Project\df_video_data_all_csv.csv")

df_comments_data_all=pd.read_csv(r"C:\Users\mkolwal\PycharmProjects\YT_Project\df_comments_data_all_csv.csv")


















with st.sidebar:
    selected = option_menu(None, ["Home", "Get Data & Transform", "SQL Query"],
                           icons=["house-door-fill", "tools", "card-text"],
                           default_index=0,
                           orientation="vertical",
                           styles={"nav-link": {"font-size": "15px", "text-align": "center", "margin": "0px",
                                                "--hover-color": "#C80101"},
                                   "icon": {"font-size": "5px"},
                                   "container": {"max-width": "4000px"},
                                   "nav-link-selected": {"background-color": "red"}})

if selected == "Home":
    st.balloons()
    st.title(":red[YOUTUBE DATA HARVESTING AND WAREHOUSING]")
    st.markdown("## :green[Domain] : Social Media 💻")
    st.markdown("## :orange[Technologies used] : Python, MongoDB, Youtube Data API, MySql, Streamlit")
    st.markdown(
        "## :blue[Overview] : Retrieving the Youtube channels data from the Google API, storing it in a MongoDB as "
        "data lake, migrating and transforming data into a SQL database, then querying the data and displaying it in "
        "the Streamlit app.")

if selected == "Get Data & Transform":
    tab1, tab2 = st.tabs(["$\huge 📝🎈 GET DATA $", "$\huge 👨🏾‍💻 TRANSFORM TO SQL $"])

    # GET DATA TAB
    with tab1:
        st.markdown("#")
        st.write("### Enter YouTube Channel_ID below :")

        selection = st.selectbox("select the channel", ("Corey Schafer", "CS Dojo", "Coding with John", "Sebastian "
                                                                                                        "Lague",
                                                        "3BlueBrown"))

        if selection == "Corey Schafer":
            st.dataframe(df_channel_data_1)
        elif selection == "CS Dojo":
            st.dataframe(df_channel_data_2)
        if selection == "Coding with John":
            st.dataframe(df_channel_data_3)
        if selection == "Sebastian Lague":
            st.dataframe(df_channel_data_4)
        if selection == "3BlueBrown":
            st.dataframe(df_channel_data_5)

        if st.button("Upload to MongoDB"):
            with st.spinner('Please Wait for it...'):
                st.success("Upload to MogoDB successful !!")

    with tab2:
        st.markdown("#   ")
        st.markdown("### Select a channel to begin Transformation to SQL")

        selection = st.selectbox("select the channel", ("Corey Schafer ", "CS Dojo ", "Coding with John ", "Sebastian "
                                                                                                        "Lague ",
                                                        "3BlueBrown "))

        if st.button("Submit"):
            try:

                st.success("Transformation to MySQL Successful !!")
                st.balloons()

            except:
                st.error("Channel details already transformed !!")

if selected == "SQL Query":
    st.write("## :green[Take your pick from the questions below]")
    questions = st.selectbox('Questions',
                             ['1. What are the names of all the videos and their corresponding channels?',
                              '2. Which channels have the most number of videos, and how many videos do they have?',
                              '3. What are the top 10 most viewed videos and their respective channels?',
                              '4. How many comments were made on each video, and what are their corresponding '
                              'video names?',
                              '5. Which videos have the highest number of likes, and what are their corresponding '
                              'channel names?',
                              '6. What is the total number of likes for each video, and what are '
                              'their corresponding video names?',
                              '7. What is the total number of views for each channel, and what are their '
                              'corresponding channel names?',
                              '8. What are the comments that have published videos in the year 2022?',
                              '9.Which videos have the highest number of comments, and what are their '
                              'corresponding channel names?'])

    if questions == '1. What are the names of all the videos and their corresponding channels?':
        answer_1 = df_video_data_all[['video_name', 'channel_title']]
        st.dataframe(answer_1)

    elif questions == '2. Which channels have the most number of videos, and how many videos do they have?':
        answer_2 = df_channel_data_all[['channel_name', 'total_video']]
        st.dataframe(answer_2)

    elif questions == '3. What are the top 10 most viewed videos and their respective channels?':
        answer_3 = df_video_data_all.sort_values(by='view_count', ascending=False)
        answer_3 = answer_3[['channel_title', 'video_name']]
        answer_3 = answer_3.head(10)
        st.dataframe(answer_3)

    elif questions == '4. How many comments were made on each video, and what are their corresponding video names?':
        answer_4 = df_video_data_all[['video_name', 'comment_count']]
        st.dataframe(answer_4)

    elif questions == '5. Which videos have the highest number of likes, and what are their corresponding channel ' \
                      'names?':
        answer_5 = df_video_data_all.sort_values(by='like_count', ascending=False)
        answer_5 = answer_5[['channel_title', 'like_count']]
        answer_5.head(10)
        st.dataframe(answer_5)

    elif questions == '6. What is the total number of likes for each video, and what are their ' \
                      'corresponding video names?':
        answer_6 = df_video_data_all[['video_name', 'channel_title', 'like_count']]
        st.dataframe(answer_6)

    elif questions == '7. What is the total number of views for each channel, and what are their corresponding ' \
                      'channel names?':
        answer_7 = df_video_data_all[['channel_title', 'view_count']]
        st.dataframe(answer_7)

    elif questions == '8. What are the comments that have published videos in the year 2022?':
        df_comments_data_all['published_date'] = pd.to_datetime(df_comments_data_all['published_date'])
        sorted_df = df_comments_data_all[df_comments_data_all['published_date'].dt.year == 2022].sort_values(
            by='published_date')
        answer_8 = sorted_df
        st.dataframe(answer_8)

    elif questions == '9.Which videos have the highest number of comments, and what are their corresponding channel names?':


        answer_9 = df_video_data_all.sort_values(by='comment_count', ascending=False)

        answer_9 = answer_9[['channel_id', 'video_name', 'comment_count']]

        st.dataframe(answer_9.head(10))

