import os

from pyramid.events import NewRequest
from pyramid.events import subscriber
from pyramid.events import ApplicationCreated

from pyramid.config import Configurator
from pyramid.session import UnencryptedCookieSessionFactoryConfig

from wsgiref.simple_server import make_server
from ott.wules.views import make_views

import logging
logging.basicConfig()
log = logging.getLogger(__file__)
log.setLevel(logging.INFO)


@subscriber(ApplicationCreated)
def application_created_subscriber(event):
    #
    # make the db
    #
    log.info('Starting the system...')


@subscriber(NewRequest)
def new_request_subscriber(event):
    #
    #  connect to db
    #
    request = event.request
    settings = request.registry.settings
    request.add_finished_callback(close_db_connection)


def close_db_connection(request):
    pass


def pyramid_config():
    # configuration settings
    here = os.path.dirname(os.path.abspath(__file__))
    dir = os.path.join(here, 'templates')
    log.info(here + " " + dir)

    settings = {}
    settings['reload_all'] = True
    settings['debug_all'] = True
    settings['mako.directories'] = dir

    # session factory
    session_factory = UnencryptedCookieSessionFactoryConfig('itsaseekreet')

    # configuration setup
    config = Configurator(settings=settings, session_factory=session_factory)
    return config


def main():
    config = pyramid_config()
    make_views(config)

    # serve app
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()


if __name__ == '__main__':
    main()
