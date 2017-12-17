from __future__ import absolute_import, print_function, unicode_literals

import json

import itertools, time

import tweepy, copy

import Queue, threading

#import pandas as pd

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
 
	stream.filter(languages = ["en"], track=["listening to Taylor Swift","listening to Pentatonix","listening to Sam Smith","listening to Garth Brooks","listening to Ed Sheeran","listening to Post Malone","listening to P!nk", "listening to Pink","listening to Lil Uzi Vert","listening to Michael Buble","listening to Fabolous & Jadakiss","listening to Chris Brown","listening to Kodak Black","listening to Imagine Dragons","listening to Maroon 5","listening to Kendrick Lamar","listening to 21 Savage, Offset & Metro Boomin","listening to Khalid","listening to Lil Pump","listening to Tim McGraw & Faith Hill","listening to Demi Lovato","listening to Bruno Mars","listening to Halsey","listening to BTS","listening to Camila Cabello","listening to Cardi B","listening to 21 Savage","Taylor Swift","Pentatonix","Sam Smith","Garth Brooks","Ed Sheeran","Post Malone","P!nk", "listening to Pink","Lil Uzi Vert","Lil Uzi","Michael Buble","Fabolous & Jadakiss","Chris Brown","Kodak Black","Imagine Dragons","Maroon 5","Kendrick Lamar","21 Savage, Offset & Metro Boomin","Khalid","Lil Pump","Tim McGraw & Faith Hill","Demi Lovato","Bruno Mars","Halsey","BTS","Camila Cabello","Cardi B","21 Savage", "Reputation by Taylor Swift","A Pentatonix Christmas by Pentatonix","The Thrill Of It All by Sam Smith","The Anthology by Garth Books","Divide by Ed Sheeran","Stoney by Post Malone","Beautiful Trauma by Pink","Beautiful Trauma by Pink","Luv Is Rage by Lil Uzi","Luv Is Rage 2","Christmas by Micheal Bubble","Friday On Elm Street by Fabulous & Jadakiss","Heartbreak On A Full Moon by Chris Brown","Project Baby Two by Kodak Black","Evolve by Imagine Dragons","Red Pill Blues by Maroon 5","DAMN by Kendrick Lamar","Thats Christmas To Me by Pentatonix","Without Warning by 21 Savage, Offset & Metro Boomin","American Teen by Khalid","Lil Pump by Lil Pump","The Rest Of Our Life by Tim McGraw & Faith Hill"], async = True)

	
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

