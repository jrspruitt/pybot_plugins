# -*- coding: utf-8 -*-
# vim: set ts=4 et

import re
import config
import random
import tweepy

from plugin import *

apik = config.twitter_apikey
apis = config.twitter_secret
autht = config.twitter_auth_t
authts = config.twitter_auth_ts

def text_cleaner(text, prefix):
    text =  text.replace(prefix, '')
    return text.rstrip(' ').lstrip(' ')


def text_encode(text):
    return text.encode('utf-8')


class Search(object):
    def __init__(self, api):
        self._api = api
        self._prefix = 'twitter search'

    def match(self, text):
        if text.startswith(self._prefix):
            return True
        else:
            return False

    def process(self, text):
            try:
                text = text_cleaner(text, self._prefix)
                cursor = tweepy.Cursor(self._api.search, q=text, rpp=1)

                for c in cursor.items(1):
                    uname = text_encode(c.author.name)
                    ctext = text_encode(c.text)
                    f = text_encode('@{0}: {1}')
                    return f.format(uname, ctext)

                else:
                    return 'No results.'

            except tweepy.TweepError, e:
                print e
                return 'Update failed.'


class Post(object):
    def __init__(self, api):
        self._api = api
        self._prefix = 'twitter post'

    def match(self, text):
        if text.startswith(self._prefix):
            return True
        else:
            return False

    def process(self, text):
            try:
                text = text_cleaner(text, self._prefix)
                self._api.update_status(status=text)
                return 'Updated.'
            except tweepy.TweepError, e:
                print e
                return 'Update failed.'


class User(object):
    def __init__(self, api):
        self._api = api

    def match(self, text):
        if text.startswith('twitter user'):
            return True
        else:
            return False

    def process(self, text):
            text =  text_cleaner(text, 'twitter user')

            try:
                user = self._api.get_user(text)
                return text_encode(user.status.text)
            except tweepy.TweepError, e:
                print e
                return 'No user by that name.'


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

    def process(self, text):
        try:
            if not self._id:
                return 'Bad ID.'

            status = self._api.get_status(self._id)
            self._id = None
            return text_encode(status.text)

        except tweepy.TweepError, e:
            self._id = None
            return 'No Status for that ID.'


class Plugin(BasePlugin):
    def on_load(self, reloading):
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
                rtext = m.process(text).replace('\r', '').replace('\n', ' ')
                msg.reply(rtext)
                #lines = rtext.split('\n')
                #for line in lines:
                #    msg.reply(line)
                #return
            #msg.reply('{0}'.format(user.name))
    
