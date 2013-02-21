import os
import shutil
import simplejson as json
import logging
log = logging.getLogger(__file__)

from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.decorator import reify

import ott.wules.services.wules as wules
import json_utils as json_utils

@view_config(route_name='default_index', renderer='index.html')
def index(request):
    ret_val = {}

    kw = get_kwargs(request)
    rules = wules.find(**kw)
    if rules:
        ret_val['rules'] = rules

    return ret_val


@view_config(route_name='content_ws', renderer='json')
def rules_content(request):
    ''' return the content
    import pdb
    pdb.set_trace()

    '''
    ret_val = None

    kw = get_kwargs(request)
    rules = wules.find(**kw)
    if rules:
        j = json_utils.objects_to_json_string(obj)
        ret_val = Response(j)
    else:
        ret_val = json_utils.json_message()

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
    config.add_route('content_ws',         '/content')


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

def get_header(request, name, def_val=None):
    ''' utility function

        @return the header value...
        @todo: make this work actually...
    '''
    ret_val=def_val
    try:
        ret_val = request.getheader(name)
    except:
        pass

    return ret_val

def get_lang(request, def_val='en'):
    ret_val = def_val
    l = get_header(request, '', def_val)
    if l and len(l) >= 2:
        ret_val = l[:2]
    return ret_val

def get_kwargs(request):
    ''' turn request args into k/v dictionary
        parse out language from HTTP_ACCEPT_LANGUAGE' header
    '''
    ret_val = {}
    lang = get_lang(request)
    ret_val[wules.Rule.LANGUAGE] = lang

    kwargs = request.params.mixed()
    if kwargs:
        ret_val.update(kwargs)

    return ret_val
