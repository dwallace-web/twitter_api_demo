import time, tweepy, config, csv, os, requests
import tweepy

from datetime import date, datetime

# date
collection = str(date.today())
print(f'Scrape started at {str(datetime.now())}')
count = 0
data_for_csv = []
res = []

Client = tweepy.Client(bearer_token=config.BEARER_TOKEN)
user = Client.get_user(username=config.USERNAME)

def fetch_users():
    global res

    for response in tweepy.Paginator(Client.get_users_following, id=user[0].id,
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
        ]):
        res.extend(response.data)
        print(response.meta)

# res_og = Client.get_users_following( 
#     id=user[0].id,
#     max_results=1000,
#     user_fields=[
#     'public_metrics'
#     ,'protected'
#     ,'verified'
#     ,'location'
#     ,'description'
#     ,'created_at'
#     ,'withheld'
#     ,'url'
#     ]
#     # ,tweet_fields=['created_at','public_metrics','context_annotations','geo']
# )

def handle_users(x):
    global count

    date_tweeted = ''
    tweet_text = ''

    # total_users = get_stats(x)

    for i in x:
        count+=1
        if i.public_metrics['following_count'] >= 0:
            # time.sleep(3)     
            # get_recent_tweets = fetch_data(i)
            # filtered_data = clean_data(i, get_recent_tweets.data)
            # date_tweeted = filtered_data['date_tweeted']
            # tweet_text = filtered_data['tweet_text']

            following_info = [
            collection,
            i.id,
            i.username,
            i.protected,
            i.verified,
            i.location,
            i.description,
            i.name,
            i.public_metrics['following_count'],
            i.public_metrics['followers_count'],
            i.public_metrics['tweet_count'],
            i.url,
            date_tweeted,
            tweet_text
            ]  

            data_for_csv.append(following_info)
            # notify_admin(i.username, count, total_users)
        else:
            continue
    print(f'Scrape ended at {str(datetime.now())}')
    write_to_file()
    print('Done')



def fetch_data(x):
    fetch = []
    fetch = Client.get_users_tweets(x.id, max_results=5,tweet_fields=['created_at','public_metrics','context_annotations','geo'],exclude=['retweets'])
    return fetch 

def clean_data(user, input):
    output = {}
    date_tweeted = ''
    tweet_text = ''

    if user.protected is True:
        date_tweeted = "Unknown Date"
        tweet_text = "Unknown Tweet"
    elif input is None:
        date_tweeted = "Not Applicable - Public Account with no tweets."
        tweet_text = "Not Applicable - Public Account with no tweets."
    elif len(input) == 0 or None:
        date_tweeted = "Not Applicable - Public Account with no tweets."
        tweet_text = "Not Applicable - Public Account with no tweets."
    else:
        date_tweeted = input[0].created_at
        tweet_text = input[0].text

    output = {
        'date_tweeted': date_tweeted,
        'tweet_text': tweet_text
    }

    return output 

def notify_admin(a,b,c):
    user_time = str(datetime.now())
    print(f'At {user_time} @{a} user {b} of {c} was completed, next!')

def get_stats(x):
    total_users = len(x.data)
    total_unverified = 0
    total_verified = 0
    total_private = 0 

    for a in x.data:
        if a.verified == False:
            total_unverified+=1
    print(f"Total unverified population {total_unverified}")

    for b in x.data:
        if b.verified == True:
            total_verified+=1
    print(f"Total verified population {total_verified}")

    for c in x.data:
        if c.protected == True:
            total_private+=1
    print(f"Total private population {total_private}")

    return total_users

def write_to_file():
    with open(f'data_following_{collection}.csv', 'a', newline="") as csvfile:
        writer = csv.writer(csvfile)
        #header 
        user_info = [
            'collection date',
            'customer id',
            'username',
            'private',
            'verified',
            'location',
            'bio',
            'display name',
            'following count',
            'follower count',
            'total tweets',
            'outbound link',
            'recent tweet date',
            'recent tweet body',
        ]
        writer.writerow(user_info)
        for i in data_for_csv:
            writer.writerow(i)
    csvfile.close()

fetch_users()
handle_users(res)