import time
import tweepy
from tweepy.api import pagination
from tweepy.client import Response
import config
import csv

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
list_id = '1290447421357666311'
list_members = []
has_token = True

# fetching the members
Response = client.get_list_members(list_id)
res_data = Response.data
list_members.extend(res_data)
print(len(list_members))


member_dic = {}

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
        print(len(list_members))
        time.sleep(1)
    else:
        has_token = False
        # print(list_members)
        print("no more tokens")
        print("Final Count" + str(len(list_members)))
        # time.sleep(3)
        print("end loop")

"""
# QA  printing the member screen names an ID
for member in list_members:
    print(str(member) + " | " + str(member.id))
"""


# writing to a dictionary
for member in list_members:
    # print the follower count for each member
    member_data = api.get_user(user_id=str(member.id))
    # print(member_data.verified)
    member_dic.add({"username": member.screen_name, "member_id": member.id,
                   "member_followers": member.followers_count, "verified": member.verified})
print(member_dic)

user_info = ['userID', 'username', 'follower_count', 'verification_status']

# Build CSV File
with open('data.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = user_info)
    writer.writeheader()
    writer.writerows(member_dic)