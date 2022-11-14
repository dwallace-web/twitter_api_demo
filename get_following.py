import datetime
import time
import tweepy
from tweepy.api import pagination
from tweepy.client import Response
import config
import csv
from datetime import date
from datetime import datetime
import os 

# date
collection = str(date.today())

# SIMPLE STRUCTURE

Client = tweepy.Client(bearer_token=config.BEARER_TOKEN)
auth = tweepy.OAuthHandler(consumer_key=config.API_KEY,
                           consumer_secret=config.API_KEY_SECRET)
api = tweepy.API(auth)

# user = Client.get_user(username=config.MY_USERNAME)
# user2 = api.get_user(screen_name=config.MY_USERNAME)

res = Client.get_users_following(id=user2.id,max_results=1000)
following = res.data

date_tweeted = ''
tweet_text = ''
follower_count = 0

with open(f"data_following_{collection}.csv", 'a', newline="") as csvfile:
    writer = csv.writer(csvfile)

    for i in following:
        
        recent_tweets = Client.get_users_tweets(i.id, max_results=5,tweet_fields=['created_at']).data
        # print the follower count for each member
        recent_user_data = api.get_user(user_id=str(i.id))

        if recent_tweets is not None:
            date_tweeted = recent_tweets[0].created_at
        else:
            date_tweeted = "Unknown Date"
        
        if recent_tweets is not None:
            tweet_text = recent_tweets[0].text
        else:
            tweet_text = "Unknown Tweet"

        if recent_user_data is not None:
            follower_count = recent_user_data.followers_count
        else:
            follower_count = "Unknown Follower Count"

        following_info = [
        collection,
        i.id,
        i.username,
        i.name,
        date_tweeted,
        tweet_text,
        follower_count 
        ]  

        writer.writerow(following_info)

        print(f'{i.username} is complete, next!')
        time.sleep(4)

csvfile.close()