import logging
logging.basicConfig()
log = logging.getLogger(__file__)
log.setLevel(logging.INFO)

from pyramid.view import view_config
from pyramid.config import Configurator
from pyramid.session import UnencryptedCookieSessionFactoryConfig


@view_config(route_name='list', renderer='list.mako')
def list_view(request):
    #
    #  view with mako
    #
    log.info("entering list_view")
    return {'tasks': []}


@view_config(route_name='vote')
def vote_view(request):
    #
    #  vote recording via SqlAlchemy
    #
    vote_value = get_first_param(request, 'vote_value')
    user_id = get_first_param(request, 'user_id')
    stop_id = get_first_param(request, 'stop_id')
    log.info("{0}, {1}, {2}".format(vote_value, user_id, stop_id))

    return Response('OK')


@view_config(context='pyramid.exceptions.NotFound', renderer='notfound.mako')
def notfound_view(self):
    #
    #  view with mako
    #
    return {}


def make_views(config):
    # routes setup
    config.add_route('list', '/')
    config.add_route('vote', '/vote')
    config.add_route('new', '/new')
    config.add_route('close', '/close/{id}')
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
