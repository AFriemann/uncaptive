# -*- coding: utf-8 -*-
"""
.. module: TODO
    :platform: TODO
    :synopsis: TODO

.. moduleauthor:: Aljosha Friemann a.friemann@automate.wtf
"""

import time
import socket
import logging
import requests

from contextlib import closing

from uncaptive.modules import PORTAL_MAP


class CaptiveLoginError(RuntimeError):
    pass


def is_captive():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.settimeout(1)

        return sock.connect_ex(('mail.automate.wtf', 443)) == 0


def effective_url(session=None):
    url = 'http://mail.automate.wtf'

    response = (session or requests).get(url, allow_redirects=False)

    if response.is_redirect:
        return response.headers.get('location')

    return url


def main():
    if is_captive():
        session = requests.session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-GB,de;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'DNT': '1',
        })

        captive_url = effective_url(session)

        if captive_url in PORTAL_MAP:
            PORTAL_MAP[captive_url].login(session, captive_url)
        else:
            CaptiveLoginError('No login method for %s' % captive_url)
    else:
        logging.debug('No captive portal.')


def daemon():
    logging.basicConfig(level=logging.INFO)

    logging.info('Starting uncaptive loop.')

    try:
        while True:
            try:
                main()
            finally:
                time.sleep(10)
    except KeyboardInterrupt:
        exit('Exiting')


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
