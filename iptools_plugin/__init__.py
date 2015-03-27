# -*- coding: utf-8 -*-
# vim: set ts=4 et

import re
import socket
import dns
import dns.resolver
import dns.reversename
from geoip import geolite2
from plugin import *




class Dig(object):
    def __init__(self):
        self._resolver = dns.resolver.Resolver()
        self._ip_only_rtype = ['RLOOKUP', 'REVERSENAME', 'PTR']
        self._sort_on = {'MX':'preference', 'NS':'target'}
        self._rtypes = {'RLOOKUP':None,
                        'REVERSENAME':None,
                        'A':self._address,
                        'AAAA':self._address,
                        'APL':self._apl,
                        'DHCID':self._data,
                        'IPSECKEY':self._ipseckey,
                        'KX':self._exchange,
                        'NAPTR':self._naptr,
                        'NSAP':self._address,
                        'NSAP_PTR':self._target,
                        'PX':self._exchange,
                        'SRV':self._srv,
                        'WKS':self._wks,
                        'AFSDB':self._afsdb,
                        'CERT':self._cert,
                        'CNAME':self._target,
                        'DLV':self._dsbase,
                        'DNAME':self._target,
                        'DNSKEY':self._dnskey,
                        'DS':self._dsbase,
                        'GPOS':self._gpos,
                        'HINFO':self._hinfo,
                        'HIP':self._hip,
                        'ISDN':self._isdn,
                        'LOC':self._loc,
                        'MX':self._exchange,
                        'NS':self._target,
                        'NSEC':self._nsec,
                        'NSEC3':self._nsec3,
                        'NSEC3PARAM':self._nsec3param,
                        'PTR':self._target,
                        'RP':self._rp,
                        'RRSIG':self._rrsig,
                        'RT':self._exchange,
                        'SPF':self._string,
                        'SSHFP':self._sshfp,
                        'SOA':self._soa,
                        'TLSA':self._tlsa,
                        'TXT':self._string,
                        'X25':self._address}

    # Generic type formatting functions

    @staticmethod
    def _address(ans):
        fstr = '{0}'
        return fstr.format(ans.address)

    @staticmethod
    def _data(ans):
        fstr = '{0}'
        return fstr.format(ans.data)

    @staticmethod
    def _dsbase(ans):
        fstr = 'Alogrithm:{0} Digest:{1} DigestType:{2} KeyTag:{3}'
        return fstr.format(ans.alogrithm,
                           ans.digest,
                           ans.digest_type,
                           ans.key_tag)

    @staticmethod
    def _exchange(ans):
        fstr = '{0}: {1}'
        return fstr.format(ans.preference, ans.exchange)

    @staticmethod
    def _string(ans):
        fstr = '{0}'
        return fstr.format(ans)

    @staticmethod
    def _target(ans):
        fstr = '{0}'
        return fstr.format(ans.target)


    # Specifal type formatting functions.
    @staticmethod
    def _afsdb(ans):
        fstr = '{0}: {1}'
        return fstr.format(ans.subtype, ans.hostname)

    @staticmethod
    def _apl(ans):
        fstr = 'Address:{0} Family:{1} Negation:{2} Prefix:{3}'
        return fstr.format(ans.address, ans.family, ans.negation, ans.prefix)

    @staticmethod
    def _cert(ans):
        fstr = 'Algo:{0} CertType: {1} Cert:{2} keyTag:{3}'
        return fstr.format(ans.alogrithm,
                           ans.certificate,
                           ans. certificate_type,
                           ans.key_tag)
    @staticmethod
    def _dnskey(ans):
        fstr = 'Algo:{0} Flags:{1} Key:{2} Protocol:{3}'
        return fstr.format(ans.alogrithm, ans.flags, ans.key, ans.protocol)

    @staticmethod
    def _gpos(ans):
        fstr = 'Altitude:{0} Latitude:{1} Longitude:{2}'
        return fstr.format(ans.altitude, ans.latitude, ans.longitude)

    @staticmethod
    def _hinfo(ans):
        fstr = 'CPU:{0} OS:{1}'
        return fstr.format(ans.cpu, ans.os)

    @staticmethod
    def _hip(ans):
        fstr = 'Alogrithm:{0} HIT:{1} Key:{2} Servers:{3}'
        return fstr.format(ans.alogrithm, ans.hit, ans.key, ans.servers)

    @staticmethod
    def _ipseckey(ans):
        fstr = 'Alogrithm:{0} Gateway:{1} ' \
               'GatewayType:{2} Key:{4} Precedence:{5}'
        return fstr.format(ans.alogrithm,
                           ans.gateway,
                           ans.gateway_type,
                           ans.key,
                           ans.precedence)

    @staticmethod
    def _isdn(ans):
        fstr = 'Address:{0} SubAddress:{1}'
        return fstr.format(ans.address, ans.subaddress)

    @staticmethod
    def _loc(ans):
        fstr = 'Altitude:{0} HorzPrecision:{1} Latitude:{2} Longitude:{3} ' \
               'Size:{4} VertPrecision:{5} GoogleMap:{6}'
        url = googlemap_url(ans.float_latitude, ans.float_longitude)
        return fstr.format(ans.altitude,
                           ans.horizontal_precision,
                           ans.latitude,
                           ans.longitude,
                           ans.size,
                           ans.vertical_precision,
                           url)

    @staticmethod
    def _naptr(ans):
        fstr = 'Flags:{0} Order:{1} Preference:{2} ' \
               'Regexp:{3} Replacement:{4} Service:{5}'
        return fstr.format(ans.flags,
                           ans.order,
                           ans.preference,
                           ans.regexp,
                           ans.replacement,
                           ans.service)

    @staticmethod
    def _nsec(ans):
        fstr = 'Next:{0} Windows:{1}'
        return fstr.format(ans.next, ans.windows)

    @staticmethod
    def _nsec3(ans):
        fstr = 'Alogrithm:{0} Flags:{1} Iterations:{2}' \
               'Next:{3} Salt:{4} Windows:{5}'
        return fstr.format(ans.alogrith,
                           ans.flags,
                           ans.interations,
                           ans.next,
                           ans.salt,
                           ans.windows)

    @staticmethod
    def _nsec3param(ans):
        fstr = 'Alogrithm:{0} Flags:{1} Iterations:{2} Salt:{3}'
        return fstr.format(ans.alogrithm, ans.flags, ans.iterations, ans.salt)

    @staticmethod
    def _px(ans):
        fstr = 'Map822:{0} Mapx400:{1} Preference:{2}'
        return fstr.format(ans.map822, ans.mapx400, ans.preference)

    @staticmethod
    def _rp(ans):
        fstr = 'Mbox:{0} TXT:{1}'
        return fstr.format(ans.mbox, ans.txt)

    @staticmethod
    def _rrsig(ans):
        fstr = 'Alogrithm:{0} Expiration:{1} Inception:{2} KeyTag:{3} ' \
               'Labels:{4} OriginalTTL:{5} Signature:{6} Signer:{7} ' \
               'TypeCovered:{8}'
        return fstr.format(ans.alogrithm,
                           ans.expiration,
                           ans.inception,
                           ans.key_tag,
                           ans.labels,
                           ans.original_ttl,
                           ans.signature,
                           ans.signer,
                           ans.type_covered)

    @staticmethod
    def _soa(ans):
        fstr = 'Expire:{0} Min:{1} Mname:{2} Refresh:{3} ' \
               'Retry:{4} Rname:{5} Serial:{6}'
        return fstr.format(ans.expire,
                           ans.minimum,
                           ans.mname,
                           ans.refresh,
                           ans.retry,
                           ans.rname,
                           ans.serial)

    @staticmethod
    def _srv(ans):
        fstr = 'Port:{0} Priority:{1} Target:{2} Weight:{3}'
        return fstr.format(ans.port, ans.priority, ans.target, ans.weight)

    @staticmethod
    def _sshfp(ans):
        fstr = 'Alogrithm:{0} Fingerprint:{1} FPType:{2}'
        return fstr.format(ans.algorithm, ans.fingerprint, ans.fp_type)

    @staticmethod
    def _tlsa(ans):
        fstr = 'Cert:{0} Mtype:{1} Selector:{2} Usage:{3}'
        return fstr.format(ans.cert, ans.mtype, ans.selector, ans.usage)

    @staticmethod
    def _wks(ans):
        fstr = 'Address:{0} Bitmap:{1} Protocol:{2}'
        return fstr.format(ans.address, ans.bitmap, ans.protocol)

    def help(self):
        fstr = 'Usage: dig [@<ip | domain.name>] <ip | domain.name> <{0}> Returns relevant info.'
        return fstr.format(' | '.join([rec for rec in self._rtypes]))

    def _query(self, url, rtype):
        print url, rtype
        return self._resolver.query(url, rtype)

    def dname_to_ip(self, dname):
        return '{0}'.format(self._query(dname, 'A')[0])

    @staticmethod
    def ip_to_dname(ipaddr):
        return '{0}'.format(dns.reversename.from_address(ipaddr))

    def _get_ns(self, arg):
        if arg.startswith('@'):
            arg = arg[1:]

        if is_ip(arg):
            return '{0}'.format(arg)

        elif is_dn(arg):
            try:
                return self.dname_to_ip(arg)
            except dns.exception.DNSException, err:
                print err
                return 'default'

    def _get_args(self, message):
        args = {'rtype':None, 'ns':None, 'ip':None, 'dn':None}
        cargs = message.upper().split(' ')

        for arg in cargs:
            arg = '{0}'.format(arg)
            if arg in self._rtypes:
                args['rtype'] = arg

            elif arg.startswith('@'):
                args['ns'] = self._get_ns(arg)

            elif is_ip(arg):
                args['ip'] = arg

            elif is_dn(arg):
                args['dn'] = arg

        return args

    def _set_nameserver(self, msg, nserv):
        if nserv == 'default':
            msg.reply('Bad DNS name, using default.')
        elif nserv is not None:
            self._resolver.nameservers = [nserv]

    def process(self, msg):
        message = re.sub(' {2,}', '', msg.param[-1])

        if message.startswith('dig help'):
            msg.reply(self.help())
            return

        args = self._get_args(message)
        self._set_nameserver(msg, args['ns'])

        if args['rtype'] in self._ip_only_rtype:
            if args['ip'] is None:
                msg.reply('{0} requires an IP address'.format(args['rtype']))
                return

            try:
                res = self.ip_to_dname(args['ip'])
            except dns.exception.DNSException, err:
                msg.reply(err)
                return

            if args['rtype'] == 'RLOOKUP':
                args['rtype'] = 'PTR'
            elif args['rtype'] == 'REVERSENAME':
                msg.reply(res)
                return

        else:
            if args['dn'] is None:
                msg.reply('{0} requires a domain name.'.format(args['rtype']))
                return
            res = args['dn']

        try:
            answers = self._query(res, args['rtype'])

            if args['rtype'] in self._sort_on:
                sort_on = self._sort_on[args['rtype']]
                answers = sorted(answers,
                                 key=lambda x: getattr(x, sort_on))

            for ans in answers:
                msg.reply(self._rtypes[args['rtype']](ans))

        except dns.resolver.NoAnswer, err:
            msg.reply('No Answer.')
        except dns.exception.DNSException, err:
            msg.reply(err)

        return

    @staticmethod
    def match(arg):
        if arg.startswith('dig'):
            return True
        return False


class Pgeoip(object):
    def __init__(self):
        pass

    @staticmethod
    def help():
        return 'Usage: geoip <ip | domain.name>  Returns Google Maps link.'

    @staticmethod
    def match(arg):
        if arg.startswith('geoip'):
            return True
        return False

    @staticmethod
    def _get_args(message):
        args = {}
        cargs = message.upper().split(' ')
        args['ip'] = None

        if is_ip(cargs[1]):
            args['ip'] = cargs[1]
        elif is_dn(cargs[1]):
            try:
                args['ip'] = '{0}'.format(dns.resolver.query(cargs[1], 'A')[0])
            except dns.resolver.NoAnswer, err:
                print err

        return args

    def process(self, msg):
        message = re.sub(' {2,}', '', msg.param[-1])

        if message.startswith('geoip help'):
            msg.reply(self.help())
            return

        args = self._get_args(message)

        if args['ip'] is None:
            msg.reply('Bad IP address')
            return

        mgeo = geolite2.lookup(args['ip'])

        if mgeo is None:
            msg.reply('Could not locate.')

        elif mgeo.location:
            lat, lon = mgeo.location
            msg.reply('GoogleMap:{0}'.format(googlemap_url(lat, lon)))

        else:
            msg.reply('Locatation not available.')

        return


#bGeneric helpers
def googlemap_url(lat, lon):
    fstr = 'http://maps.google.com/?ie=UTF8&q={0:.5f},' \
           '{1:.5f}&hq=&ll={0:.5f},{1:.5f}&z=13'
    return fstr.format(lat, lon)

def is_ip(arg):
    try:
        socket.inet_pton(socket.AF_INET, arg)
        return True
    except socket.error:
        pass

    try:
        socket.inet_pton(socket.AF_INET6, arg)
        return True
    except socket.error:
        return False

def is_dn(arg):
    regx_dn = re.compile(r'([0-9A-Za-z-_]+\.)+[A-Za-z]{2,}')
    return bool(re.match(regx_dn, arg)) or False

class Plugin(BasePlugin):
    @hook
    def privmsg_command(self, msg):
        if not msg.channel:
            return

        if msg.param[-1].startswith('iptools help'):
            msg.reply('Commands: geoip and dig, use <cmd> help, for further info.')
            return

        for cmd in [Dig(), Pgeoip()]:
            if cmd.match(msg.param[-1]):
                cmd.process(msg)
                return


