import os
import shutil

from pyramid.config import Configurator
from pyramid.decorator import reify
from pyramid.events import subscriber
from pyramid.events import ApplicationCreated
from pyramid.events import NewRequest

import pyramid_views as views

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

    do_static_config(config)
    views.do_view_config(config)

    config.scan()
    return config.make_wsgi_app()


def do_static_config(config):
    ''' config the static folders
    '''
    cache_age=3600
    config.add_static_view('static', 'static',          cache_max_age=cache_age)
    config.add_static_view('html',   'static',          cache_max_age=cache_age)
    config.add_static_view('js',     'static/js',       cache_max_age=cache_age)
    config.add_static_view('css',    'static/css',      cache_max_age=cache_age)
    config.add_static_view('images', 'static/images',   cache_max_age=cache_age)

    # important ... allow .html extension on mako templates
    config.add_renderer(".html", "pyramid.mako_templating.renderer_factory")


@subscriber(ApplicationCreated)
def application_created_subscriber(event):
    ''' what do i do?
        I'm called at startup of the Pyramid app.  
    '''
    #log.info('Starting pyramid server -- visit me on http://localhost:8080')
    print event

@subscriber(NewRequest)
def new_request_subscriber(event):
    ''' what do i do?
       1. entry point for a new server request
       2. configure the request context object (can insert new things like db connections or authorization to pass around in this given request context)
    '''
    #log.debug("new request called -- request is 'started'")
    request = event.request
    request.BASE_DIR = os.path.dirname(os.path.realpath(__file__))
