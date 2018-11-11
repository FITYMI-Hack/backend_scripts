import tweepy
import json
import pandas as pd
import numpy as np
from collections import namedtuple, Counter
import csv
from keys import *

#my api codes are stored in a file called keys that I import above
auth = tweepy.AppAuthHandler(ckey, csecret)
#auth.set_access_token(akey, asecret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True,)
searchQuery = '#impostersyndrome OR imposter syndrome'
max_count = 500

Tweet = namedtuple('Tweet', 'id name text location img_url date')
def get_tweets():
    for tw in tweepy.Cursor(api.search, q=searchQuery).items(max_count):
        yield Tweet(tw.id_str, tw.user.screen_name, tw.text, tw.user.location, tw.user.profile_image_url, tw.created_at)

tweets = list(get_tweets())
with open("mytweets.csv", 'a', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(tweets)
