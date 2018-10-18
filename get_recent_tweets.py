import tweepy
# Define ckey and csecret in keys.py with your application's key and secret.
from keys import *  
import numpy as np
import pandas as pd



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
# sinceId = None  ## commented out by abc

## abc: 10/16/18: new code for incremental search of tweets to be added 
## to a possibly existing file tweets.csv
import csv
import os
         
row_number = -1    # The end of the csv file has the most recent tweets with 
                   # the largest set of IDs. We will start searching from the
                   # last row up until we find the most recent.
exists = os.path.isfile(fName)
if exists: 
    with open(fName, 'rt', encoding='utf-8') as f1:
        mycsv = csv.reader(f1)
        mycsv = list(mycsv)
        lastRowId = mycsv[row_number][1]
        print("lastRowId: "+str(lastRowId))
        firstId = mycsv[2][1]
        if firstId > lastRowId:   # if the firstId is bigger that the last one
            sinceId = firstId     # there was only one read of tweets, and the firstId is the largest one.
        else: # find the largest/newest ID.
            row = row_number - 1
            botId = lastRowId
            topId = mycsv[row][1]
            # we loop up from the end of the file until we find the largest ID
            # by falling in the previously read set of tweets.
            while  (topId != "t_id"):
                row = row -1
                botId = topId
                topId = mycsv[row][1]
            sinceId = botId       
            f1.close()   
else:
    sinceId = None

print("sinceId:   "+str(sinceId))

## end of new abc code. 10/16/18

# If results only below a specific ID are, set max_id to that ID.
# else default to no upper limit, start from the most recent tweet matching the search query.
max_id = -1

tweetCount = 0
print("Downloading max {0} tweets".format(maxTweets))
with open(fName, 'a') as f:
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
            data.to_csv(fName, encoding='utf-8-sig',  mode='a')
            tweetCount += len(new_tweets)
#            print("Downloaded {0} tweets".format(tweetCount))
            max_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            # Just exit if any error
            print("some error : " + str(e))
            break

print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, fName))
