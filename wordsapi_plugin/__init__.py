# -*- coding: utf-8 -*-
# vim: set ts=4 et

from plugin import *
import config

import re
from lxml import etree
import requests

pattern = re.compile(r'^(?P<cmd>[a-zA-Z]*) (?P<word>[A-Za-z_\- \.]+) ?(?P<idx>\d{0,2})$')

class Plugin(BasePlugin):
    def __init__(self, _):
        self._last_cmd = ''
        self._last_word = ''
        self._last_content = ''
        self._api = {'key':None, 'cmd':None, 'url':'', 'idx': 0, 'word':'', 'total':True}

    @hook
    def privmsg_command(self, msg):
        if not msg.channel:
            return
        text = msg.param[-1]

        if text.startswith('wordsapi help'):
            msg.reply('Usage: <define|thes|urband|rhyme> [index], Returns definition, thesaurus, urband dictionary definition, or rhymed words.')
            return

        g = re.search(pattern, text)

        if not g:
            return


        for api in apiservices:
            if g.group('cmd') == api['cmd']:
                self._api = api
                self._api['word'] = g.group('word').rstrip(' ')

                if g.group('idx') and float(g.group('idx')):
                    self._api['idx'] = int(g.group('idx'))
                else:
                    self._api['idx'] = 0
                break
        else:
            return


        if not self._api['key']:
            return

        try:

            if self._last_cmd != self._api['cmd'] or self._last_word != self._api['word']:
                self._last_cmd = self._api['cmd']
                self._last_word = self._api['word']
                content = self._api['func'](self._api)

                if not content:
                    return

                self._last_content = content

            else:
                content = self._last_content


            if self._api['idx'] >= len(content):
               self._api['idx'] = 0

            text = content[self._api['idx']].replace('\n', ' ').replace('\r','')
            text_len = len(text)
            line_len = 386 
            for i in range(0, text_len, line_len):
                msg.reply(text[i:i+line_len])

            if self._api['total']:
                msg.reply('Total Results:%s' % (len(content))) 

            return
        except:
            return


def dt_parser(api):
    rets = []
    try:
        url = api['url'].format(key=api['key'], word=api['word'])
        r = requests.get(url)

        if r.status_code not in [200, 301, 304]:
            return None

        if not r.content:
            return None
        else:
            reps = '<sx>|</sx>|<it>|</it>|<un>|</un>|<vi>|</vi>'
            text = re.sub(reps, '', r.content)
            root = etree.fromstring(text)

            for x in root.iterfind(api['xpath']):
                if api['cmd'] == 'define':
                    rets.append(x.text[1:])
                elif api['cmd'] == 'thes':
                    rets.append(x.find('syn').text)

            return rets
    except:
        return None

def urband_parser(api):
        rets = []
        headers = {'X-Mashape-Key':api['key'], 'Accept':'text/plain'}
        r = requests.get(api['url'].format(word=api['word']), headers=headers)

        if r.status_code not in [200, 301, 304]:
            return None

        item = r.json()
        if not item:
            return None

        for x in item['list']:
            rets.append(x['definition'])

        return rets


def rhyme_parser(api):
        rets = []
        r = requests.get(api['url'].format(word=api['word']))

        if r.status_code not in [200, 301, 304]:
            return None

        items = r.json()

        if not items:
            return None

        rets = [r['word'] for r in items[0:20] if r['score'] >= api['score']]

        return [' '.join(rets)]

mdict = {'cmd':'define',
        'key':config.dict_apikey,
        'url':'http://www.dictionaryapi.com/api/v1/references/collegiate/xml/{word}?key={key}',
        'total':True,
        'xpath':'entry/def/dt',
        'func':dt_parser}

thes = {'cmd':'thes',
        'key':config.thes_apikey,
        'url':'http://www.dictionaryapi.com/api/v1/references/thesaurus/xml/{word}?key={key}',
        'total':True,
        'xpath':'entry/sens',
        'func':dt_parser}

urband = {'cmd':'urband',
        'key':config.urband_apikey,
        'url':'https://mashape-community-urban-dictionary.p.mashape.com/define?term={word}',
        'total':True,
        'func':urband_parser}

rhyme = {'cmd':'rhyme',
        'key':True,
        'url':'http://rhymebrain.com/talk?function=getRhymes&word={word}',
        'score':300,
        'total':False,
        'func':rhyme_parser}

apiservices = [mdict, thes, urband, rhyme]
