import time, tweepy, config, csv, os, requests
from tweepy.api import pagination
from tweepy.client import Response
from datetime import date, datetime

# date
collection = str(date.today())
start_time = str(datetime.now())
print(f'Scrape started at {start_time}')

# SIMPLE STRUCTURE

Client = tweepy.Client(bearer_token=config.BEARER_TOKEN)
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
    ,'url'
    ]
)

following = res.data
following.reverse()

count = 0

total_users = len(following)
data_for_csv = []
retain_api_data = []


def fetch_users():
    global count

    date_tweeted = ''
    tweet_text = ''
    follower_count = 0

    for i in following:
            if count <= 3: 
                fetch = Client.get_users_tweets(i.id, max_results=100,tweet_fields=['created_at','public_metrics'])

                get_recent_tweets = fetch.data
                
                if i.protected is True:
                    date_tweeted = "Unknown Date"
                    tweet_text = "Unknown Tweet"
                else:
                    tweet_text = get_recent_tweets[0].text
                    date_tweeted = get_recent_tweets[0].created_at

                following_info = [
                collection,
                i.id,
                i.username,
                i.verified,
                i.location,
                i.description,
                i.name,
                date_tweeted,
                tweet_text,
                i.public_metrics['following_count'],
                i.public_metrics['followers_count'],
                i.public_metrics['tweet_count'],
                i.url
                ]  

                data_for_csv.append(following_info)

                count+=1
                user_time = str(datetime.now())
                print(f'At {user_time} @{i.username} user {count} of {total_users} was completed, next!')
                # time.sleep(1)
            else:
                continue
    
    end_time = str(datetime.now())
    print(f'Scrape ended at {end_time}')
    write_to_file()

def write_to_file():
    with open(f'data_following_{collection}.csv', 'a', newline="") as csvfile:
        writer = csv.writer(csvfile)

        #header 
        user_info = [
            'collection date',
            'customer id',
            'username',
            'verified',
            'location',
            'bio',
            'display name',
            'tweet date',
            'tweet body',
            'following count',
            'follower count',
            'total tweets',
            'outbound link'
        ]
        writer.writerow(user_info)
        for i in data_for_csv:
            writer.writerow(i)
    csvfile.close()

def store_everything():
    with open(f"store_everything_{collection}.csv", 'a', newline="") as csv_2:
        writer = csv.writer(csv_2)
        for i in retain_api_data:
            writer.writerow(retain_api_data)
    csv_2.close()

fetch_users()
# store_everything()