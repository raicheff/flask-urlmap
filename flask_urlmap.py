#
# Flask-Rev
#
# Copyright (C) 2019 Boris Raicheff
# All rights reserved
#


import tldextract


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
        self.scheme = app.config.get('PREFERRED_URL_SCHEME')
        self.domain = tldextract.extract(app.config.get('SERVER_NAME')).registered_domain
        self.map = app.config.get('URL_MAP')

        def external_url_handler(error, endpoint, values):
            url = self.lookup_url(endpoint, **values)
            if url is None:
                # External lookup did not have a URL; Re-raise the BuildError, in context of original traceback.
                raise error
            # url_for will use this result, instead of raising BuildError.
            return url

        app.url_build_error_handlers.append(external_url_handler)

    def lookup_url(self, endpoint, **values):
        subdomain, func = endpoint.split('.')
        try:
            return f'{self.scheme}://{subdomain}.{self.domain}{self.map[subdomain][func].format(**values)}'
        except KeyError:
            pass


# EOF
