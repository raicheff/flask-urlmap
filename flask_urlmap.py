#
# Flask-Rev
#
# Copyright (C) 2019 Boris Raicheff
# All rights reserved
#


import logging

import tldextract


logger = logging.getLogger('Flask-URLMap')


class URLMap(object):
    """
    Flask-URLMap

    Refer to http://flask-urlmap.readthedocs.io for more details.

    :param app: Flask app to initialize with. Defaults to `None`
    """

    scheme = None

    domain = None

    map = None

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        config = self.scheme, domain, self.map = tuple(
            app.config.get(name) for name in ('PREFERRED_URL_SCHEME', 'SERVER_NAME', 'URL_MAP')
        )
        if not all(config):
            logger.debug('Flask-URLMap not configured')
            return

        self.domain = tldextract.extract(domain).registered_domain

        def external_url_handler(error, endpoint, values):
            url = self.lookup_url(endpoint, **values)
            if url is None:
                raise error
            return url

        app.url_build_error_handlers.append(external_url_handler)

    def lookup_url(self, endpoint, **values):
        subdomain, func = endpoint.split('.')
        try:
            return f'{self.scheme}://{subdomain}.{self.domain}{self.map[subdomain][func].format(**values)}'
        except KeyError:
            pass


# EOF
