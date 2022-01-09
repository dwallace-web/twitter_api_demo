import tweepy
from tweepy.api import pagination
from tweepy.client import Response
import config
import json

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

# fetching the members
Response = client.get_list_members(list_id)
print(Response)


# printing the member screen names
for member in Response.data:
    print("THIS is user ser " + str(member))
    print(member.id)

    '''
    # print the follower count for each member
    member_data = api.get_user(user_id=str(member_id))
    print(member_data.followers_count)
    member_id = member.id
    '''


'''
# print the follower count for each member
    member_data = api.get_user(user_id=str(member_id))
    print(member_data.followers_count)
'''


'''
list_members = []

for member in Response.data:
    list_members.append({"member_username":member.username,"member_id":member.id})
    print(list_members)

print(Response.meta["next_token"])
'''
