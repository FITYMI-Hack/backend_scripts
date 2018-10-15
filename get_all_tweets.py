import tweepy
from keys import *
import numpy as np
import pandas as pd


# Replace the API_KEY and API_SECRET with your application's key and secret.
auth = tweepy.AppAuthHandler(ckey, csecret)

api = tweepy.API(auth, wait_on_rate_limit=True,
				   wait_on_rate_limit_notify=True)

if (not api):
    print ("Can't Authenticate")
    sys.exit(-1)

import sys
import jsonpickle
import os

searchQuery = '#impostersyndrome OR #impostorsyndrome OR imposter syndrome OR impostor syndrome'  # this is what we're searching for
maxTweets = 10000000 # Some arbitrary large number
tweetsPerQry = 100  # this is the max the API permits
fName = 'tweets.csv' # We'll store the tweets in a text file.


# If results from a specific ID onwards are reqd, set since_id to that ID.
# else default to no lower limit, go as far back as API allows
sinceId = None

# If results only below a specific ID are, set max_id to that ID.
# else default to no upper limit, start from the most recent tweet matching the search query.
max_id = -1

tweetCount = 0
print("Downloading max {0} tweets".format(maxTweets))
with open(fName, 'w') as f:
    while tweetCount < maxTweets:
        try:
            if (max_id <= 0):
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry)
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            since_id=sinceId)
            else:
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            max_id=str(max_id - 1))
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            max_id=str(max_id - 1),
                                            since_id=sinceId)
            if not new_tweets:
                print("No more tweets found")
                break
            # for tweet in new_tweets:
            #     f.write(jsonpickle.encode(tweet._json, unpicklable=False) +
            #             '\n')
            data = pd.DataFrame(data=[tweet.id for tweet in new_tweets], columns=['t_id'])
            data['s_name'] = np.array([tweet.user.screen_name for tweet in new_tweets])
            data['t_text'] = np.array([tweet.text for tweet in new_tweets])
            data['u_location'] = np.array([tweet.user.location for tweet in new_tweets])
            data['image_url'] = np.array([tweet.user.profile_image_url for tweet in new_tweets])
            data['t_date'] = np.array([tweet.created_at for tweet in new_tweets])
            data.to_csv(fName, encoding='utf-8', mode='a')
            tweetCount += len(new_tweets)
            print("Downloaded {0} tweets".format(tweetCount))
            max_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            # Just exit if any error
            print("some error : " + str(e))
            break

print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, fName))