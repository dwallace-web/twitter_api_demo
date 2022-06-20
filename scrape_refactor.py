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

# the ID of the Roster list
list_id = '1478967604228276224'
list_members = []
has_token = True

# fetching the members
Response = client.get_list_members(list_id)
res_data = Response.data
list_members.extend(res_data)
print(len(list_members))


def get_requirements():
    while has_token:
        if "next_token" in Response.meta:
            print("I will try again")
            next_token = Response.meta["next_token"]
            print("Token is " + str(next_token))
            Response = client.get_list_members(
                list_id, pagination_token=next_token)
            # print(Response.data)
            # print(Response.meta)
            list_members.extend(Response.data)
            print("Current number of members..." + str(len(list_members)))
            time.sleep(5)
        else:
            has_token = False
            # print(list_members)
            print("no more tokens")
            print("Final Count of members: " + str(len(list_members)))
            time.sleep(5)
            print("end loop")


def get_data():
    # writing to a dictionary
    for member in list_members:
        # print the follower count for each member
        member_data = api.get_user(user_id=str(member.id))
        time.sleep(4)

        collection = datetime.now()

        member_info = [collection, member_data.screen_name, member_data.id,
                       member_data.followers_count, member_data.verified, list_id]
        print(member_info)


def build_doc(userData):
    # Build CSV File Header
    user_info = ['date', 'username', 'userID',
                 'follower_count', 'verification_status', 'list_id']

    with open("data_{list_id}_v2.csv".format(list_id=list_id), 'a', newline="") as csvfile:
        writer = csv.writer(csvfile)

        # check if csv file has a head
        file_exists = os.path.isfile("data_{list_id}_v2.csv")
        print(file_exists)

        if file_exists is not False:
            writer.writerow(user_info)
            writer.writerow(member_info)
    csvfile.close()
