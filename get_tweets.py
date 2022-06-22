import tweepy
from tweepy.api import pagination
from tweepy.client import Response
import config
import time
from datetime import date

# date
current_date = str(date.today())

# SIMPLE STRUCTURE
my_name = 'dtheblerd'
client = tweepy.Client(bearer_token=config.BEARER_TOKEN)
self1 = client.get_user(username=my_name)
auth = tweepy.OAuthHandler(consumer_key=config.API_KEY,
                           consumer_secret=config.API_KEY_SECRET)
api = tweepy.API(auth)
self2 = api.get_user(screen_name=my_name)

print("% s has % s followers" % (self1.data, self2.followers_count))

# How to write a query #dev docs -- https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query
# How to write an academic query -- https://github.com/twitterdev/getting-started-with-the-twitter-api-v2-for-academic-research

query = "#aewdynamite -is:retweet -is:reply is:verified -is:reply is:verified lang:en"

res = client.search_recent_tweets(
    query=query,
    max_results=10,
    tweet_fields=['lang',
                  'created_at',
                  'public_metrics',
                  'source',
                  'id',
                  'author_id',
                  'referenced_tweets',
                  'conversation_id',
                  'geo'
                  ],
    place_fields=['country'],
    expansions=['author_id'],
    user_fields=['username',
                 'id',
                 'description',
                 'name']
)
tweets = res.data
users = {u['id']: u for u in res.includes['users']}

for tweet in tweets:
    user = users[tweet.author_id]
    print("This tweet is from @% s using the % s"
          % (user.username, tweet.source))
    print(tweet.text)
