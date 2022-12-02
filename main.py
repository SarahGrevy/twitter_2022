import logging
import logging.handlers
import os

import requests

import tweepy
import configparser
import datetime
import pandas as pd
import pytz
import time 
import csv
import pandas as pd

from config import Config
from db_adapter import DbAdapter
from os.path import abspath, dirname, join
from tweets import Tweets

utc=pytz.UTC

CONFIGDIR = join(abspath(dirname(__file__)), 'config')

DB_CONFIG_FILE = join(CONFIGDIR, 'config.cfg')
config = Config('config', CONFIGDIR)
dba = DbAdapter(config.get_property("POSTGRES", "dialect"),
                                config.get_property("POSTGRES", "driver"),
                                config.get_property("POSTGRES", "host"),
                                config.get_property("POSTGRES", "database"),
                                config.get_property("POSTGRES", "username"),
                                config.get_property("POSTGRES", "password"))

# read configs
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

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    "status.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)

try:
    SOME_SECRET = os.environ["SOME_SECRET"]
except KeyError:
    SOME_SECRET = "Token not available!"
    #logger.info("Token not available!")
    #raise


if __name__ == "__main__":
    logger.info(f"Token value: {SOME_SECRET}")

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
                    "followers_count": followers_count

                }

                f = Tweets(**d)
                f.insert(dba)
                time.sleep(1)