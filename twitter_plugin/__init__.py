# -*- coding: utf-8 -*-
# vim: set ts=4 et

import re
import random
import requests
import tweepy
from html.parser import HTMLParser

from plugin import *

def text_cleaner(text, prefix):
    text =  text.replace(prefix, '')
    return text.rstrip(' ').lstrip(' ')

def tweet_cleaner(text):
    hp = HTMLParser()
    return hp.unescape(text.replace('\n', ' ').replace('\r', ''))

def url_expander(sentence, msg):
    regex_tco = re.compile(r'https?://t.co/.*')
    urls = []
    words = sentence.split()

    for word in words:
        m = re.match(regex_tco, word)

        if m:
            idx = words.index(word)
            r = requests.get(word)

            if r.status_code in [200, 301, 302]:
                msg.reply(r.url)

class Search(object):
    def __init__(self, api):
        self._api = api
        self._prefix = 'twitter search'

    def match(self, text):
        if text.startswith(self._prefix):
            return True
        else:
            return False

    def process(self, text, msg):
        try:
            text = text_cleaner(text, self._prefix)
            cursor = tweepy.Cursor(self._api.search, q=text, rpp=1)

            for c in cursor.items(1):
                uname = c.author.name
                msg.reply('@{0}: {1}'.format(uname, tweet_cleaner(c.text)))
                url_expander(c.text, msg)
                break

            else:
                msg.reply('No results.')

        except tweepy.TweepError as e:
            print(e)
            msg.reply('Update failed.')

        return


class Post(object):
    def __init__(self, api):
        self._api = api
        self._prefix = 'twitter post'

    def match(self, text):
        if text.startswith(self._prefix):
            return True
        else:
            return False

    def process(self, text, msg):
        try:
            text = text_cleaner(text, self._prefix)
            self._api.update_status(status=text)
            msg.reply('Updated.')
        except tweepy.TweepError as e:
            print(e)
            msg.reply('Update failed.')

        return

class User(object):
    def __init__(self, api):
        self._api = api

    def match(self, text):
        if text.startswith('twitter user'):
            return True
        else:
            return False

    def process(self, text, msg):
        text =  text_cleaner(text, 'twitter user')

        try:
            user = self._api.get_user(text)
            msg.reply(tweet_cleaner(user.status.text))
            url_expander(user.status.text, msg)
        except tweepy.TweepError as e:
            print(e)
            msg.reply('No user by that name.')

        return

class Url(object):
    def __init__(self, api):
        self._api = api
        self._id = None
        self._regx = re.compile(r'https?://twitter.com/[a-zA-Z0-9_\-]+/status/(?P<id>[0-9]+)')

    def match(self, text):
        m = re.match(self._regx, text)
        if not m:
            self._id = None
            return False
        else:
            self._id = m.group('id')
            return True

    def process(self, text, msg):
        try:
            if not self._id:
                return 'Bad ID.'

            status = self._api.get_status(self._id)
            self._id = None
            msg.reply(tweet_cleaner(status.text))
            url_expander(status.text, msg)

        except tweepy.TweepError as e:
            self._id = None
            msg.reply('No Status for that ID.')

        return


class Plugin(BasePlugin):
    def on_load(self, reloading):
        apik = self.bot.config[self.name]['apikey']
        apis = self.bot.config[self.name]['secret']
        autht = self.bot.config[self.name]['auth_t']
        authts = self.bot.config[self.name]['auth_ts']
        
        auth = tweepy.OAuthHandler(apik, apis)
        auth.set_access_token(autht, authts)
        api = tweepy.API(auth)
        self._mods = [User(api), Url(api), Search(api)] #, Post(api)]

    @hook
    def privmsg_command(self, msg):
        if not msg.channel:
            return

        text = msg.param[-1]

        if text.startswith('twitter help'):
            msg.reply('Usage: twitter [search|user] <text> Returns most recent or specified by URL Tweet text.')

        for m in self._mods:
            if m.match(text):
                m.process(text, msg)
