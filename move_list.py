import datetime
import time
from turtle import Turtle
import tweepy
from tweepy.api import pagination
from tweepy.client import Response
import config
import csv
from datetime import date
from datetime import datetime
import os.path

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

# fetching the members from list one
# the ID of the Roster list
list_members = []
has_token = True
list_id = '1478967604228276224'
Response = client.get_list_members(list_id)
res_data = Response.data
list_members.extend(res_data)
print(len(list_members))

while has_token:
    if "next_token" in Response.meta:
        print("I will try again")
        next_token = Response.meta["next_token"]
        Response = client.get_list_members(
            list_id, pagination_token=next_token)
        list_members.extend(Response.data)
        print("Current number of members..." + str(len(list_members)))
        time.sleep(2)
    else:
        has_token = False
        print("Final Count of members: " + str(len(list_members)))
        time.sleep(2)
        print("end loop")

print('start list two')


# fetching the members from list two

list_two = '1206660807691526146'
list_two_members = []
res_two = client.get_list_members(list_two)
res_data_two = res_two.data
list_two_members.extend(res_data_two)
list_two_token = True

# handle list two

while list_two_token:
    if "next_token" in res_two.meta:
        next_token_two = res_two.meta["next_token"]
        print(next_token_two)
        res_two = client.get_list_members(
            list_id, pagination_token=next_token_two)
        list_two_members.extend(res_two.data)
        print("Current number of members in list two..." +
              str(len(list_two_members)))
        time.sleep(2)
    else:
        list_two_token = False
        print("Final Count of list two members: " + str(len(list_two_members)))
        time.sleep(2)


# get the full list of members from each list
# find the differences between the two list
# add the missing members to list ID 1206660807691526146

print("Final Count of list one members: " + str(len(list_members)))
print("Final Count of list two members: " + str(len(list_two_members)))

s = set(list_two_members)
list_three = [x for x in list_members if x not in s]
print(len(list_three))
print(list_three)

list(set(list_members) - set(list_two_members))

for x in list_three:
    print(list_three["id"])
    print(list_three["id"])
    print(list_three["id"])
    print(list_three["id"])
    print(list_three["id"])
    print(list_three["id"])
    client.add_list_member(list_two, list_three["id"])
