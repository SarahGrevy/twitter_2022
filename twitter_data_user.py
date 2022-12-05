import tweepy
import configparser
import datetime
import pandas as pd
import pytz
import time 
import csv
import pandas as pd
#check

from config import Config
from db_adapter import DbAdapter
from os.path import abspath, dirname, join
from tweets import Tweets

utc=pytz.UTC

CONFIGDIR = join(abspath(dirname(__file__)), 'config')

project_name = "Twitter"

DB_CONFIG_FILE = join(CONFIGDIR, 'config.cfg')
config = Config('config', CONFIGDIR)
dba = DbAdapter(config.get_property("POSTGRES", "dialect"),
                                config.get_property("POSTGRES", "driver"),
                                config.get_property("POSTGRES", "host"),
                                config.get_property("POSTGRES", "database"),
                                config.get_property("POSTGRES", "username"),
                                config.get_property("POSTGRES", "password"))

# read configs


# cached = Tweets().get_cached_data_by_project(dba, "Twitter")
# cached.extend(Tweets().get_cached_data_by_project(dba, "Twitter"))


config = configparser.ConfigParser()
config.read('config.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']

access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

# authentication
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# user tweets
df = pd.read_csv("combined.csv")
df.columns

startDate = datetime.datetime(2022, 1, 1, 0, 0, 0)
endDate =   datetime.datetime(2023, 1, 1, 0, 0, 0)

startDate= utc.localize(startDate) 
endDate = utc.localize(endDate) 


limit=1000
for user in df['username']:
    tweets = tweepy.Cursor(api.user_timeline, screen_name=user, count=1000, tweet_mode='extended').items(limit)
    for tweet in tweets:
        if tweet.created_at > startDate:
            user = tweet.user.screen_name
            full_text = tweet.full_text
            date = tweet.created_at
            followers_count = tweet.user.followers_count

            d = {
                "username": user,
                "tweet": full_text,
                "date_created": date,
                "followers_count": followers_count,
                'project_name': project_name
            

            }

            f = Tweets(**d)
            f.insert(dba)
            time.sleep(1)

