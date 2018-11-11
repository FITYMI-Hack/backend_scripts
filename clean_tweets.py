# Script to clean tweets from the USA
import pandas as pd
import numpy as np
import datetime

# get dictionary for converting state names
from state_conversions import *

csv_file = "tweets1018913.csv"

try:
    df = pd.read_csv(csv_file)
except:
    print(f"Unable to read {csv_file}")

# ## What are we looking for?
# Ok, some places are real and some are not. Looking at the data I am going to stick with locations in the USA
# and locations that have been picked via the drop-down menu on twitter. Here is what they look like:

# #### City, State:
# Maplewood, NJ
# #### State, County:
# New Jersey, USA
# #### Country:
# United States
#
# 1. Entries will have a single comma or be "United States"
# 2. Full city name with a state abbriviation
# 3. Full state name with a country abbriviation
# 4. Full country name
#
# #### What we want, is to convert it to one of the following:
#
# Maplewood, New Jersey, USA
#
# New Jersey, USA
#
# USA

# ## Cleaning
# 1. Remove empty location rows
# 2. Convert NJ to New Jersey, USA
# 3. Convert United States to USA
# 4. Keep only fileds that have USA in them
# 5. Removing retweets

# mark if a retweet and then drop
df['get_rt'] = df['t_text'].str.startswith('RT')
df.drop(df[df['get_rt'] == True].index, inplace=True)

# Remove any tweet with no location information
df.dropna(subset=['u_location'], how='all', inplace = True)

# Convert 2 letter abbrv. to State name, USA
# import dictionary from file done at top of script
df['u_location'] = df['u_location'].replace(us_state_abbrev, regex=True)

# mark all with the count of USA and grab those with only one.
usa_counts = df['u_location'].str.count('USA')
df['with_usa'] = np.where((usa_counts == 1),df.u_location, "")

# Must end with USA
end_usa = df['u_location'].str.endswith('USA')
df['with_usa'] = np.where((end_usa == True),df.with_usa, "")

# No junk in the location field
df['with_usa'] = df['with_usa'].str.replace('[^a-zA-Z\s,]', '')

# make sure all fields are populated
df.dropna(inplace = True)

# Drop if no USA
df['usa_count'] = df['with_usa'].str.count('USA')
df.drop(df[df['usa_count'] == 0].index, inplace=True)

# we can only have up to two commas, drop rows with more
comma_counts = df['with_usa'].str.count(',')
df['with_comma'] = np.where((comma_counts <= 2),df.with_usa, "")

# #### Split into three different rows
# I split the location data into three rows with a split in reverse order. This orders the data with a left justify.
# I then strip each row of extra spaces and drop the column we do not need. Finally I write out the new csv file.
# split into three fields

df[['Country', 'State', 'City']] = df['with_comma'].apply(lambda x:pd.Series(x.split(",")[::-1]))

# strip extra spaces
df['Country'] = df['Country'].str.strip()
df['State'] = df['State'].str.strip()
df['City'] = df['City'].str.strip()

# drop unused columns
df.drop(['with_usa', 'usa_count', 'with_comma', 'get_rt'], axis=1, inplace=True)

# write out my file of clean tweets
today = datetime.datetime.today().strftime('%d%m')
myfile = 'tweets_clean_' + today + '.csv'

try:
    df.to_csv(myfile)
except OSError:
    print("unable to write to file")





