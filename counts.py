import datetime
import time
import tweepy
from tweepy.api import pagination
from tweepy.client import Response
import config
import csv
from datetime import date
from datetime import datetime
import os.path


# date
current_date = str(date.today())

# SIMPLE STRUCTURE
my_name = 'dtheblerd'
client = tweepy.Client(bearer_token=config.BEARER_TOKEN)
user = client.get_user(username=my_name)
print(user)
auth = tweepy.OAuthHandler(consumer_key=config.API_KEY,
                           consumer_secret=config.API_KEY_SECRET)

api = tweepy.API(auth)
user2 = api.get_user(screen_name=my_name)
print(user2.followers_count)

counts = client.get_all_tweets_count("#aewdynamite")
print(counts)
