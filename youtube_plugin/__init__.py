# -*- coding: utf-8 -*-
# vim: set ts=4 et

from plugin import *

import re
import requests

yt_url = 'https://www.googleapis.com/youtube/v3/videos?id=%s&key=%s&part=snippet'
url_re = re.compile(
                    r'^(?:https?://)?(?:www\.)?' + 
                    r'(?:youtu\.be/|youtube\.com' + 
                    r'(?:/embed/|/v/|/watch\?v=|/watch\?.+&v=))' + 
                    r'(?P<id>[\w-]{11})' +
                    r'(?:.+)?$',
                    re.I
                    )

class Plugin(BasePlugin):
    @hook
    def privmsg_command(self, msg):
        if not msg.channel:
            return

        text = msg.param[-1]

        if text.startswith('youtube help'):
            msg.reply('URL Parser returns title of Youtube video.')
            return

        m = url_re.match(text)
        if not m:
            return

        vid =  m.group('id')
        if vid is None:
            return

        try:
            url = yt_url % (vid, self.bot.config['youtube']['apikey'])
            r = requests.get(url)

            if r.status_code not in [200, 301, 304]:
                return

            item = r.json()
            msg.reply(item['items'][0]['snippet']['title'])
        except:
            return
