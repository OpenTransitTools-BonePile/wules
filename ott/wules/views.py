import logging
logging.basicConfig()
log = logging.getLogger(__file__)
log.setLevel(logging.INFO)

from pyramid.view import view_config
from pyramid.config import Configurator
from pyramid.session import UnencryptedCookieSessionFactoryConfig


@view_config(route_name='about', renderer='about.mako')
def about(request):
    '''
      about view with mako
    '''
    log.info("entering about")
    return {}


@view_config(route_name='admin', renderer='admin.mako')
def admin(request):
    '''
      admin view with mako
    '''
    log.info("entering admin")
    return {}


@view_config(route_name='content', renderer='content.mako')
def content(request):
    '''
      content view with mako
    '''
    log.info("entering content")

    id = get_first_param(request, 'id')
    rule = get_first_param(request, 'rule')
    log.info("{0}, {1}".format(id, rule))

    return {}


@view_config(context='pyramid.exceptions.NotFound', renderer='notfound.mako')
def notfound_view(self):
    #
    #  view with mako
    #
    return {}


def make_views(config):
    # routes setup
    config.add_route('about',  '/')
    config.add_route('admin',  '/admin')
    config.add_route('content', '/content')
    config.scan()


def get_first_param(request, name, def_val=None):
    """ 
    """
    ret_val=def_val
    try:
        ret_val = request.params.getone(name)
    except:
        pass

    return ret_val
