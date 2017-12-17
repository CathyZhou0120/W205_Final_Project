from __future__ import absolute_import, print_function, unicode_literals

import json

import itertools, time

import tweepy, copy

import Queue, threading

import pandas as pd

from streamparse.spout import Spout



################################################################################

# Twitter credentials

################################################################################

twitter_credentials = {

    "consumer_key"        :  "LmHsZjJZaIWjKrKSKDHdusB99",

    "consumer_secret"     :  "G4fNgo0fLLhFtm9uOk2twO0XAQVjMTjocgCgY7yPXl5N2KJrcl",

    "access_token"        :  "3225709838-a2oXtV8MO4K7OBScOKtpsr3OoWZyw1EDjXMqVGx",

    "access_token_secret" :  "APVVWs4hTnDoyXfHSCoZZ63EixC9uG53edv5ph3AylDo0",

}



def auth_get(auth_key):

    if auth_key in twitter_credentials:

        return twitter_credentials[auth_key]

    return None



################################################################################

# Class to listen and act on the incoming tweets

################################################################################

class TweetStreamListener(tweepy.StreamListener):

    def __init__(self, listener):

        self.listener = listener

        super(self.__class__, self).__init__(listener.tweepy_api())



    def on_status(self, status):
        self.listener.queue().put(json.dumps(status._json), timeout = 0.01)
        return True



    def on_error(self, status_code):

        return True # keep stream alive



    def on_limit(self, track):

        return True # keep stream alive



class Tweets(Spout):



    def initialize(self, stormconf, context):

        self._queue = Queue.Queue(maxsize = 100)



        consumer_key = auth_get("consumer_key")

        consumer_secret = auth_get("consumer_secret")

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)



        if auth_get("access_token") and auth_get("access_token_secret"):

            access_token = auth_get("access_token")

            access_token_secret = auth_get("access_token_secret")

            auth.set_access_token(access_token, access_token_secret)



        self._tweepy_api = tweepy.API(auth)
		
		
		# Create the listener for twitter stream

        listener = TweetStreamListener(self)



        # Create the stream and listen for english tweets

        stream = tweepy.Stream(auth, listener, timeout=None)

        stream.filter(track=["listening to Rockstar", "listening to Havana", "listening to Gucci Gang", "listening to Thunder", "listening to Perfect", "listening to Bodak Yellow", "listening to Too Good At Goodbyes", "listening to Feel It Still", "listening to Sorry Not Sorry", "listening to What Lovers Do", "listening to No Limit", "listening to Mi Gente", "listening to 1-800-273-8255", "listening to Bad At Love", "listening to Bank Account", "listening to I Get The Bag", "listening to MotorSport", "listening to New Rules", "listening to Despacito", "listening to Wolves", "listening to I Fall Apart", "listening to Young Dumb & Broke", "listening to Believer", "listening to Ready For It", "listening to What About Us", "listening to Praying", "listening to Rake It Up", "listening to Unforgettable", "listening to Gummo", "listening to Attention", "listening to Shape Of You", "listening to Thats What I Like", "listening to Theres Nothing Holdin Me Back", "listening to How Long", "listening to Congratulations", "listening to Strip That Down", "listening to The Weekend", "listening to The Way Life Goes", "listening to Slow Hands", "listening to Do Re Mi", "listening to Meant To Be", "listening to Silence", "listening to Look What You Made Me Do", "listening to Greatest Love Story", "listening to Pills And Automobiles", "listening to Echame La Culpa", "listening to Let You Down", "listening to Humble.", "listening to Plain Jane", "listening to When It Rains It Pours", "now playing Rockstar", "now playing Havana", "now playing Gucci Gang", "now playing Thunder", "now playing Perfect", "now playing Bodak Yellow (Money Moves)", "now playing Bodak Yellow", "now playing Too Good At Goodbyes", "now playing Feel It Still", "now playing Sorry Not Sorry", "now playing What Lovers Do", "now playing No Limit", "now playing Mi Gente", "now playing 1-800-273-8255", "now playing Bad At Love", "now playing Bank Account", "now playing I Get The Bag", "now playing MotorSport", "now playing New Rules", "now playing Despacito", "now playing Wolves", "now playing I Fall Apart", "now playing Young Dumb & Broke", "now playing Believer", "now playing Ready For It", "now playing What About Us", "now playing Praying", "now playing Rake It Up", "now playing Unforgettable", "now playing Gummo", "now playing Attention", "now playing Shape Of You", "now playing Thats What I Like", "now playing Theres Nothing Holdin Me Back", "now playing How Long", "now playing Congratulations", "now playing Strip That Down", "now playing The Weekend", "now playing The Way Life Goes", "now playing Love.", "now playing Slow Hands", "now playing Do Re Mi", "now playing Meant To Be", "now playing Silence", "now playing Look What You Made Me Do", "now playing Greatest Love Story", "now playing Pills And Automobiles", "now playing Echame La Culpa", "now playing Let You Down", "now playing Humble", "now playing Plain Jane", "now playing When It Rains It Pours"], async = True)
	
    def queue(self):

        return self._queue



    def tweepy_api(self):

        return self._tweepy_api



    def next_tuple(self):

        try:

            tweet = self.queue().get(timeout = 0.1)

            if tweet:

                self.queue().task_done()

                self.emit([tweet])



        except Queue.Empty:

            self.log("Empty queue exception ")

            time.sleep(0.1)



    def ack(self, tup_id):

        pass  # if a tuple is processed properly, do nothing



    def fail(self, tup_id):

        pass  # if a tuple fails to process, do nothing
