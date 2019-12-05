# -*- coding: utf-8 -*-
# -*- OVERRIDE RESOLVE DNS -*-

from platformcode import config
from core import support

if config.get_setting('resolver_dns') or config.get_setting('resolver_dns_custom'):
    from lib import dns
    import dns.resolver
    from dns.resolver import override_system_resolver
    import dns.name
    import socket
    import requests

    res = dns.resolver.Resolver(configure=True)

    """
        legge le impostazioni dalla configurazione
        e setta i relativi DNS
    """
    nameservers_dns = config.get_setting('resolver_dns_service')
    support.log("NAME SERVER1: {}".format(nameservers_dns))
    if config.get_setting('resolver_dns_custom') and not config.get_setting('resolver_dns'):
        res.nameservers = [config.get_setting('resolver_dns_custom1'),config.get_setting('resolver_dns_custom2')]
    elif nameservers_dns == 1:# 'Google'
        res.nameservers = ['8.8.8.8', '2001:4860:4860::8888',
                           '8.8.4.4', '2001:4860:4860::8844']
    elif nameservers_dns == 2:#'OpenDns Home ip(v4)':
        res.nameservers = ['208.67.222.222', '208.67.222.220']
    elif nameservers_dns == 3:#'OpenDns Family Shield ip(v4)':
        res.nameservers = ['208.67.222.123', '208.67.220.123']
    elif nameservers_dns == 4:#'OpenDns ip(v6)':
        #https://support.opendns.com/hc/en-us/articles/227986667-Does-OpenDNS-Support-IPv6-
        res.nameservers = ['2620:119:35::35', '2620:119:53::53']
    elif nameservers_dns == 0:#'Cloudflare':
        res.nameservers = ['1.1.1.1', '2606:4700:4700::1111',
                           '1.0.0.1', '2606:4700:4700::1001']

    support.log("NAME SERVER2: {}".format(res.nameservers))

    override_system_resolver(res)
