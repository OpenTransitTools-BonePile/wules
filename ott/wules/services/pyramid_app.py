import os
import shutil
import simplejson as json

from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.decorator import reify


@view_config(route_name='default_index', renderer='index.html')
def index(request):
    return {'project': 'Wules'}


@view_config(route_name='rule_ws', renderer='json')
def wule_information(request):
    ''' return the latest carshare positions as geojson
    '''
    id  = get_first_param(request, 'id')
    ret_val = None
    if id:
        pass
    else:
        ret_val = json_message('You need to specify an "id" parameter as a request parameter')

    if ret_val is None:
        ret_val = json_message()

    ret_val = Response(ret_val)
    return ret_val


def do_static_config(config):
    ''' config the static folders
    '''
    cache_age=3600
    config.add_static_view('static', 'static',          cache_max_age=cache_age)
    config.add_static_view('js',     'static/js',       cache_max_age=cache_age)
    config.add_static_view('css',    'static/css',      cache_max_age=cache_age)
    config.add_static_view('images', 'static/images',   cache_max_age=cache_age)

    # important ... allow .html extension on mako templates
    config.add_renderer(".html", "pyramid.mako_templating.renderer_factory")


def do_view_config(config):
    ''' config the different views...
    '''
    config.add_route('default_index',      '/')
    config.add_route('rule_ws',            '/rule')


def get_first_param(request, name, def_val=None):
    ''' utility function

        @return the first value of the named http param (remember, http can have multiple values for the same param name), 
        or def_val if that param was not sent via HTTP
    '''
    ret_val=def_val
    try:
        ret_val = request.params.getone(name)
    except:
        pass

    return ret_val


def json_message(msg="Something's wrong...sorry!"):
    return {error:True, msg:msg}

