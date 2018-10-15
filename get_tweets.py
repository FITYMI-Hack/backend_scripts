import tweepy
import json
import pandas as pd
import numpy as np
from keys import *

#my api codes are stored in a file called keys that I import above
auth = tweepy.AppAuthHandler(ckey, csecret)
#auth.set_access_token(akey, asecret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True,)
searchQuery = '#impostersyndrome OR imposter syndrome'
max_count = 100000


# I didn't get the cursors working
#tweets = tweepy.Cursor(api.search, q=searchQuery).items(max_count)

# This one worked
tweets = api.search(q = searchQuery, count=max_count)
#
data = pd.DataFrame(data = [tweet.id for tweet in tweets], columns =['t_id'])
data['s_name'] = np.array([tweet.user.screen_name for tweet in tweets])
data['t_text'] = np.array([tweet.text for tweet in tweets])
data['u_location'] = np.array([tweet.user.location for tweet in tweets])
data['image_url'] = np.array([tweet.user.profile_image_url for tweet in tweets])
data['t_date'] = np.array([tweet.created_at for tweet in tweets])

# these did not provide much data
#data['t_coord'] = np.array([tweet.coordinates for tweet in tweets])
#data['t_geo'] = np.array([tweet.geo for tweet in tweets])
#data['t_place'] = np.array([tweet.place for tweet in tweets])

# maybe try with the append option
data.to_csv("mytweets.csv", encoding='utf-8')

# I use this to test the data output from tweepy
# for tweet in tweets[:5]:
#     print(tweet.user.profile_image_url)
#     print()