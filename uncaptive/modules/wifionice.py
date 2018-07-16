# -*- coding: utf-8 -*-
"""
.. module: TODO
    :platform: TODO
    :synopsis: TODO

.. moduleauthor:: Aljosha Friemann a.friemann@automate.wtf
"""

import requests

try:
    import ujson as json
except ImportError:
    import json

from lxml import html


def login(session, url):
    def get_csrf_token_from_html(data):
        tree = html.fromstring(data)

        csrf_input_elements = tree.xpath('//div[@class="connectivity"]//form//input[@name="CSRFToken"]')

        if not csrf_input_elements:
            raise CaptiveLoginError('csrf token input field could not be found')
        elif len(csrf_input_elements) > 1:
            raise CaptiveLoginError('found multiple csrf token input fields')

        return csrf_input_elements[0].get('value')

    session = session or requests.session()

    logging.debug('session cookies before connecting: %s', session.cookies)

    response = session.get(url)

    token = get_csrf_token_from_html(response.content)

    if token:
        logging.info('CSRF token on page: %s', token)
    else:
        logging.warning('No CSRF token found on page')

    logging.debug('GET request headers: %s', json.dumps(dict(response.request.headers), indent=4, sort_keys=True))
    logging.debug('GET request headers: %s', json.dumps(dict(response.headers), indent=4, sort_keys=True))

    logging.debug('session cookies before POST: %s', session.cookies)

    response = session.post(url,
        data=dict(connect='', login='true', CSRFToken=token),
        headers={
            'Referer': url,
            'Host': requests.utils.urlparse(url).netloc,
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'csrf=%s' % token,
        }
    )

    logging.debug('session cookies after POST: %s', session.cookies)

    logging.debug('POST request headers: %s', json.dumps(dict(response.request.headers), indent=4, sort_keys=True))
    logging.debug('POST response headers: %s', json.dumps(dict(response.headers), indent=4, sort_keys=True))

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
