# import tweepy
# import configparser
# import datetime
# import pandas as pd
# import pytz
# import time 



# from config import Config
# from db_adapter import DbAdapter
# from os.path import abspath, dirname, join
# from tweets import Tweets
# from get_handles import Twitter_Handle



# utc=pytz.UTC

# CONFIGDIR = join(abspath(dirname(__file__)), 'config')

# DB_CONFIG_FILE = join(CONFIGDIR, 'config.cfg')
# config = Config('config', CONFIGDIR)
# dba = DbAdapter(config.get_property("POSTGRES", "dialect"),
#                                 config.get_property("POSTGRES", "driver"),
#                                 config.get_property("POSTGRES", "host"),
#                                 config.get_property("POSTGRES", "database"),
#                                 config.get_property("POSTGRES", "username"),
#                                 config.get_property("POSTGRES", "password"))


# # read configs
# config = configparser.ConfigParser()
# config.read('config.ini')


# api_key = config['twitter']['api_key']
# api_key_secret = config['twitter']['api_key_secret']

# access_token = config['twitter']['access_token']
# access_token_secret = config['twitter']['access_token_secret']

# # authentication
# auth = tweepy.OAuthHandler(api_key, api_key_secret)
# auth.set_access_token(access_token, access_token_secret)

# api = tweepy.API(auth)

# limit = 10000 

# # list_id = [54340435,535975,1599986,118675725,7070528,41260329,4926685,22866571,53044119,1070,15839982,48978707]
# list_id = [124314, 63288719, 807254657361973248]


# for id in list_id:
#     members = []
#     for page in tweepy.Cursor(api.get_list_members, list_id = id).items():
#             members.append(page)

#     for member in members:
#         twitter_handle = member.screen_name
#         followers_count = member.followers_count
#         user_created_date = member.created_at
#         bio = member.description
#         location = member.location
#         verified = member.verified
    
#         d = {
#             "twitter_handle" : twitter_handle,
#             "list_id": id,
#             "followers_count": followers_count,
#             "user_created_date": user_created_date,
#             "bio": bio,
#             "location": location,
#             'verified': verified
        
#         }

#         f = Twitter_Handle(**d)
#         f.insert(dba)
#         time.sleep(2)
