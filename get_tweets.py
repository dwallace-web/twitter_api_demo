import tweepy
from tweepy.api import pagination
from tweepy.client import Response
import config
from datetime import date

# date
current_date = str(date.today())

# SIMPLE STRUCTURE
my_name = 'dtheblerd'
client = tweepy.Client(bearer_token=config.BEARER_TOKEN)
user = client.get_user(username=my_name)
auth = tweepy.OAuthHandler(consumer_key=config.API_KEY,
                           consumer_secret=config.API_KEY_SECRET)
api = tweepy.API(auth)
user2 = api.get_user(screen_name=my_name)

print("% s has % s followers" % (user.data, user2.followers_count))

# How to write a query #dev docs -- https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query
# How to write an academic query -- https://github.com/twitterdev/getting-started-with-the-twitter-api-v2-for-academic-research

query = 'AEW -is:retweet -is:reply is:verified'

Response = client.search_recent_tweets(
    query=query, max_results=10, tweet_fields=['lang', 'created_at', 'public_metrics', 'source'])
print(Response)
# print(Response.data)

for tweet in Response.data:
    print(tweet.text)
    print(tweet.lang)
    print(tweet.created_at)
    print(tweet.public_metrics)
    print(tweet.source)

print('wait')
print('review')
