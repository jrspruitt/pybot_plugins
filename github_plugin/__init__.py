# -*- coding: utf-8 -*-
# vim: set ts=4 et

import requests
import random
import re

from plugin import *

regx = re.compile(r'^https?://(www\.)?github.com/(?P<user>[a-zA-Z0-9_\-]+)/(?P<repo>[a-zA-Z0-9_\-]+)/?.*$')
url_base = 'https://api.github.com/repos/{user}/{repo}'
url_commits = '{0}/commits'.format(url_base)

def get_json(url, user, repo):
    r = requests.get(url.format(user=user, repo=repo))

    if r.status_code not in [200, 301, 304]:
        return None

    return r.json()


def text_encode(text):
    return text.encode('utf-8')


class Plugin(BasePlugin):
    @hook
    def privmsg_command(self, msg):
        if not msg.channel:
            return

        message = msg.param[-1]

        if message.startswith('github help'):
            msg.reply('Parses github repo url and posts description.')
            return

        m = re.match(regx, message)

        if not m:
            return

        try:
            user = m.group('user')
            repo = m.group('repo')
            rinfo = get_json(url_base, user, repo)

            if not rinfo:
                return

            desc = text_encode(rinfo['description'])
            msg.reply(desc)
            return

            # Can't get here, saving code for later functionality
            commits = get_json(url_commits, user, repo)

            if not commits:
                return

            fcommit = text_encode(commits[0]['commit']['message'])
            msg.reply(text_encode('Last commit:{0}').format(fcommit))
        except Exception, e:
            print e
            return
