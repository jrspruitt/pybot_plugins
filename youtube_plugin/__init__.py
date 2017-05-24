# -*- coding: utf-8 -*-
# vim: set ts=4 et

from plugin import *

import re
import requests

data_url = 'https://www.googleapis.com/youtube/v3/videos?id=%s&key=%s&part=snippet'
url_re = re.compile(
                    r'^(?:https?://)?(?:www\.)?' + 
                    r'(?:youtu\.be/|youtube\.com' + 
                    r'(?:/embed/|/v/|/watch\?v=|/watch\?.+&v=))' + 
                    r'(?P<id>[\w-]{11})' +
                    r'(?:.+)?$',
                    re.I
                    )

class Plugin(BasePlugin):
    @hook('www.youtube.com')
    @hook('youtube.com')
    @hook('youtu.be')
    def youtube_url(self, msg, domain, url):
        m = url_re.match(url)
        if not m:
            return

        vid =  m.group('id')
        if vid is None:
            return

        try:
            url = data_url % (vid, self.bot.config.get('youtube', 'apikey'))
            r = requests.get(url)

            if r.status_code not in [200, 301, 304]:
                return

            item = r.json()
            msg.reply(item['items'][0]['snippet']['title'])
        except:
            return
