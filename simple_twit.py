# SimpleTwit.py
# IAE 101, Fall 2019
# Author: Christopher Kane

import tweepy
from tweepy.error import *
import sys, os, json, webbrowser

# CONSTANTS
VERSION = 0.2
CONFIG_FILE = "twitter_bot.config"


# GENERAL FUNCTIONS

def version():
    res = "simple_twit, version: " + str(VERSION)
    print(res)
    return res


def create_api():
    # Authentication Information
    consumer_key = "6ivEf62wQ09Hk9c6LSRCERKRR";
    consumer_secret = "1qLo73OcMylaaWkJ2PdiOi8zpFcpJob6yUN0znu1XWTKO9bEzn"

    access_token = None
    access_token_secret = None
    verify_access = True

    if os.path.exists(CONFIG_FILE):
        print("READING AUTHORIZATION FROM CONFIG FILE")
        f = open(CONFIG_FILE, "r")
        config = json.load(f)
        access_token = config["access_token"]
        access_token_secret = config["access_secret"]
        f.close()
        verify_access = False

    # Authentication Methods
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    if verify_access:
        print("AUTHORIZING THROUGH WEB INTERFACE")
        try:
            redirect_url = auth.get_authorization_url()
        except tweepy.TweepError as e:
            print("REQUEST VERIFIER URL", e)

        print(redirect_url)
        print()
        webbrowser.open(redirect_url)

        verifier = input("Enter Verifier: ")
        try:
            auth.get_access_token(verifier)
        except tweepy.TweepError as e:
            print("REQUEST ACCESS TOKEN", e)

        access_token = auth.access_token
        access_token_secret = auth.access_token_secret
        config = {"access_token": access_token,
                  "access_secret": access_token_secret}
        f = open(CONFIG_FILE, "w")
        json.dump(config, f)
        f.close()

    if access_token != None:
        auth.set_access_token(access_token, access_token_secret)
    else:
        print("AUTHENTICATION FAILED: EXITING PROGRAM!")
        sys.exit()

    # Create API object
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    return api


# end def create_api()

# TWEET FUNCTIONS

def send_tweet(api=None, text=""):
    usage = "USAGE: send_tweet(api <a tweepy api object>, text <a string>)"
    if api == None:
        print("ERROR: You must pass an api object to this function.")
        print(usage)
        return
    if text == "":
        print("ERROR: You must pass a string to this function.")
        print(usage)
        return
    try:
        result = api.update_status(status=text)
    except TweepError as e:
        print(e)
        return
    return result


# end def send_tweet()

def send_media_tweet(api=None, text="", filename=""):
    usage = "USAGE: send_media_tweet(api <a tweepy api object>, text <a string>, filename <a string>)"
    if api == None:
        print("ERROR: You must pass an api object to this function.")
        print(usage)
        return
    if filename == "":
        print("ERROR: you must pass a filename as a string to this function.")
        print(usage)
        return
    try:
        mo = api.media_upload(filename)  # Returns a Media Object
        result = api.update_status(status=text, media_ids=[mo.media_id])
    except TweepError as e:
        print(e)
        return
    return result


# end def send_media_tweet()

def retweet(api=None, id=None):
    usage = "USAGE: retweet(api <a tweepy api object>, id <numerical id of tweet>)"
    if api == None:
        print("ERROR: You must pass an api object to this function.")
        print(usage)
        return
    if id == None:
        print("ERROR: You must pass an numerical status id to this function.")
        print(usage)
        return
    try:
        result = api.retweet(id=id, tweet_mode="extended")
    except TweepError as e:
        print(e)
        return
    return result


# end def retweet()

def get_tweet(api=None, id=None):
    usage = "USAGE: get_tweet(api <a tweepy api object>, id <numerical id of tweet>)"
    if api == None:
        print("ERROR: You must pass an api object to this function.")
        print(usage)
        return
    if id == None:
        print("ERROR: You must pass an numerical status id to this function.")
        print(usage)
        return
    try:
        result = api.get_status(id=id, tweet_mode="extended")
    except TweepError as e:
        print(e)
        return
    return result


# end def get_tweet()

# TIMELINE FUNCTIONS

def get_home_timeline(api=None, count=20):
    usage = "USAGE: get_home_timeline(api <a tweepy api object>, "
    usage += "count <number of tweets to retrieve>)"
    if api == None:
        print("ERROR: You must pass an api object to this function.")
        print(usage)
        return
    if count < 1:
        print("ERROR: count argument must be a positive integer; default = 20.")
        print(usage)
        return
    tweets = []
    print("Entering Cursor")
    try:
        for tweet in tweepy.Cursor(api.home_timeline, tweet_mode="extended").items(count):
            print("Cursor Iterating")
            tweets.append(tweet)
    except TweepError as e:
        print(e)
        return
    return tweets


# end def get_home_timeline()

def get_user_timeline(api=None, user="", count=20):
    usage = ("USAGE: get_user_timeline(api <a tweepy api object>, " +
             "user <name of user>, count <number of tweets to retrieve>)")
    if api == None:
        print("ERROR: You must pass an api object to this function.")
        print(usage)
        return
    if user == "":
        print("ERROR: You must pass an user identifier string to this function.")
        print(usage)
        return
    if count < 1:
        print("ERROR: count argument must be a positive integer; default = 20.")
        print(usage)
        return
    tweets = []
    try:
        for tweet in tweepy.Cursor(api.user_timeline, id=user, tweet_mode="extended").items(count):
            tweets.append(tweet)
    except TweepError as e:
        print(e)
        return
    return tweets


# end def get_user_timeline()

# USER FUNCTIONS

def get_user(api=None, user=None):
    usage = "USAGE: get_user(api <a tweepy api object>, user <name of user>)"
    if api == None:
        print("ERROR: You must pass an api object to this function.")
        print(usage)
        return
    if user == "":
        print("ERROR: You must pass a user name or screen name to this function.")
        print(usage)
        return
    try:
        result = api.get_user(id=user, tweet_mode="extended")
    except TweepError as e:
        print(e)
        return
    return result


# end def get_user()

def get_user_friends(api=None, user="", count=100):
    usage = "USAGE: get_user_friends(api <a tweepy api object>, user <name of user>)"
    if api == None:
        print("ERROR: You must pass an api object to this function.")
        print(usage)
        return
    if user == "":
        print("ERROR: You must pass a user name or screen name to this function.")
        print(usage)
        return
    users = []
    try:
        for u in tweepy.Cursor(api.friends, id=user, tweet_mode="extended").items(count):
            users.append(u)
    except TweepError as e:
        print(e)
        return
    return users


# end def get_user_friends()

def get_my_friends(api=None, count=100):
    usage = "USAGE: get_my_friends(api <a tweepy api object>)"
    if api == None:
        print("ERROR: You must pass an api object to this function.")
        print(usage)
        return
    users = []
    try:
        for u in tweepy.Cursor(api.friends, tweet_mode="extended").items(count):
            users.append(u)
    except TweepError as e:
        print(e)
        return
    return users


# end def get_my_friends()

def get_user_followers(api=None, user="", count=100):
    usage = "USAGE: get_user_followers(api <a tweepy api object>, user <name of user>)"
    if api == None:
        print("ERROR: You must pass an api object to this function.")
        print(usage)
        return
    if user == "":
        print("ERROR: You must pass a user name or screen name to this function.")
        print(usage)
        return
    users = []
    try:
        for u in tweepy.Cursor(api.followers, id=user, tweet_mode="extended").items(count):
            users.append(u)
    except TweepError as e:
        print(e)
        return
    return users


# end def get_user_followers()

def get_my_followers(api=None, count=100):
    usage = "USAGE: get_my_followers(api <a tweepy api object>)"
    if api == None:
        print("ERROR: You must pass an api object to this function.")
        print(usage)
        return
    users = []
    try:
        for u in tweepy.Cursor(api.followers, tweet_mode="extended").items(count):
            users.append(u)
    except TweepError as e:
        print(e)
        return
    return users


# end def get_my_followers()

# FOLLOW and UNFOLLOW

def follow_user(api=None, user=""):
    usage = "(USAGE: follow_user(api <a tweepy api object>, user <name of user>)"
    if api == None:
        print("ERROR: You must pass an api object to this function.")
        print(usage)
        return
    if user == "":
        print("ERROR: You must pass a user name or screen name to this function.")
        print(usage)
        return
    try:
        result = api.create_friendship(id=user)
    except TweepError as e:
        print(e)
        return
    return result


# end def follow_user()

def unfollow_user(api=None, user=""):
    usage = "(USAGE: unfollow_user(api <a tweepy api object>, user <name of user>)"
    if api == None:
        print("ERROR: You must pass an api object to this function.")
        print(usage)
        return
    if user == "":
        print("ERROR: You must pass a user name or screen name to this function.")
        print(usage)
        return
    try:
        result = api.destroy_friendship(id=user)
    except TweepError as e:
        print(e)
        return
    return result
# end def follow_user()