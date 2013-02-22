import simplejson as json
import logging
log = logging.getLogger(__file__)

from pyramid.response import Response
from pyramid.view import view_config

import ott.wules.services.wules as wules

def do_view_config(config):
    ''' config the different views...
    '''
    config.add_route('default_index',      '/')
    config.add_route('rules_list',         '/rules')
    config.add_route('content_ws',         '/content')

@view_config(route_name='default_index', renderer='index.html')
def index(request):
    return {}

@view_config(route_name='rules_list', renderer='index.html')
def rules_list(request):
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
        ret_val = objects_to_json(rules)
    else:
        ret_val = json_message()

    return ret_val


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


def json_message(msg="Something's wrong...sorry!"):
    return objects_to_json({'error':True, 'msg':msg})


def objects_to_json(obj, wrap_response=True):
    ''' convert obj to json string
    '''
    ret_val = json.dumps(obj, sort_keys=True)
    if wrap_response:
        ret_val = Response(ret_val)
    return ret_val

