#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
11 November 2017
.. codeauthor: svitlana vakulenko
    <svitlana.vakulenko@gmail.com>

'''
import sys
import time

from twython import Twython, TwythonRateLimitError
from espeak import ESpeak

from twitter_settings import *


class Twitter_Processor():
    def __init__(self):
        self.twitter_client = self.connect_to_twitter()

    def connect_to_twitter(self):
        return Twython(APP_KEY, APP_SECRET,
                       OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    def tweets_from_list_iterator(self, list_name):
        next_max_id = None
        while True:
            params = {'slug': list_name, 'owner_screen_name': MY_NAME, 'count': 1000000, 'max_id': next_max_id}
            statuses = self.twitter_client.get_list_statuses(**params)
            if statuses:
                # print len(statuses)
                yield statuses
                next_max_id = statuses[-1]['id']
            else:
                next_max_id = None


class Bot():
    def __init__(self, add_rate=-10):
        self.twitter = Twitter_Processor()
        self.speaker = ESpeak()

    def say_hashtags_from_list(self, list_name):
        batches = self.twitter.tweets_from_list_iterator(list_name)
        for tweets in batches:
            hashtags = [hashtag['text'].encode('utf-8') for tweet in tweets for hashtag in tweet['entities']['hashtags']]
            for hashtag in set(hashtags):
                phrase = '#' + hashtag
                delay_print(phrase)
                self.speaker.say(phrase)


def delay_print(s, delay=0.1):
    for c in s:
        sys.stdout.write('%s' % c)
        sys.stdout.flush()
        time.sleep(delay)


def test_delay_print():
    delay_print("hello world")


def test_espeak():
    speaker = ESpeak()
    speaker.say("Hello world.")


def say_hashtags_from_list(list_name):
    myBot = Bot()
    myBot.say_hashtags_from_list(list_name)


if __name__ == '__main__':
    list_name = 'wien'
    say_hashtags_from_list(list_name)
