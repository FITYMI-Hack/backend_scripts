import googlemaps
import pandas as pd
from keys import *
gmaps = googlemaps.Client(key=gmap_key)

# open csv data file
df = pd.read_csv('test_geocode.csv')
# find number of populated fields

# geocode results

for index, row in df.iterrows():
    geocode_result = gmaps.geocode(row['u_location'])
    print(geocode_result)

#pars results and get lat long


# add lat long back to data frame

# write file as geojson file

