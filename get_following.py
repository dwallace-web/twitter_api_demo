import time
import tweepy
from tweepy.api import pagination
from tweepy.client import Response
import config
import csv
from datetime import date
from datetime import datetime

# date
collection = str(date.today())

start_time = str(datetime.now())
print(f'Scrape started at {start_time}')

# SIMPLE STRUCTURE

Client = tweepy.Client(bearer_token=config.BEARER_TOKEN)
# auth = tweepy.OAuthHandler(consumer_key=config.API_KEY,consumer_secret=config.API_KEY_SECRET)
# api = tweepy.API(auth)

user = Client.get_user(username=config.MY_USERNAME)
# user2 = api.get_user(screen_name=config.MY_USERNAME)

res = Client.get_users_following( 
    id=user[0].id,
    max_results=1000,
    user_fields=[
    'public_metrics'
    ,'protected'
    ,'verified'
    ,'location'
    ,'description'
    ,'created_at'
    ,'withheld'
    ]
)

following = res.data
following.reverse()

date_tweeted = ''
tweet_text = ''
follower_count = 0

with open(f"data_following_{collection}.csv", 'a', newline="") as csvfile:
    writer = csv.writer(csvfile)

    #header 
    user_info = [
        'collection date',
        'customer id',
        'username',
        'verified',
        'bio',
        'display name',
        'tweet date',
        'tweet body',
        'following count',
        'follower count'
    ]
    writer.writerow(user_info)

    #build final csv
    for i in following:
        
        get_recent_tweets = Client.get_users_tweets(i.id, max_results=5,tweet_fields=['created_at','public_metrics']).data

        if get_recent_tweets is not None:
            date_tweeted = get_recent_tweets[0].created_at
        else:
            date_tweeted = "Unknown Date"
        
        if get_recent_tweets is not None:
            tweet_text = get_recent_tweets[0].text
        else:
            tweet_text = "Unknown Tweet"

        following_info = [
        collection,
        i.id,
        i.username,
        i.verified,
        i.description,
        i.name,
        date_tweeted,
        tweet_text,
        i.public_metrics['following_count'],
        i.public_metrics['followers_count']
        ]  

        writer.writerow(following_info)

        # print(f'@{i.username} is complete, next!')
        time.sleep(5)

csvfile.close()

end_time = str(datetime.now())
print(f'Scrape ended at {end_time}')