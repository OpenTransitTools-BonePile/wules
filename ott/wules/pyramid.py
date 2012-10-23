import os
import logging
import sqlite3

from pyramid.events import NewRequest
from pyramid.events import subscriber
from pyramid.events import ApplicationCreated

from pyramid.exceptions import NotFound
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from pyramid.response import Response


from wsgiref.simple_server import make_server

# vote sql alchemy
from trimet.example.model.vote import Vote
from trimet.example.model.db_controller import DbController

logging.basicConfig()
log = logging.getLogger(__file__)
log.setLevel(logging.INFO)
here = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(here, 'example.db')

@subscriber(ApplicationCreated)
def application_created_subscriber(event):
    #
    # make the db
    #
    log.info('Initializing database...')
    f = open(os.path.join(here, 'schema.sql'), 'r')
    stmt = f.read()
    settings = event.app.registry.settings
    db = sqlite3.connect(db_path)
    db.executescript(stmt)
    db.commit()
    f.close()

    db_ctl = DbController(db_path, True)

@subscriber(NewRequest)
def new_request_subscriber(event):
    #
    #  connect to db
    #
    request = event.request
    settings = request.registry.settings
    request.db = sqlite3.connect(db_path)
    request.add_finished_callback(close_db_connection)

def close_db_connection(request):
    request.db.close()


@view_config(route_name='list', renderer='list.mako')
def list_view(request):
    #
    #  view with mako
    #
    rs = request.db.execute("select id, name from tasks where closed = 0")
    tasks = [dict(id=row[0], name=row[1]) for row in rs.fetchall()]
    return {'tasks': tasks}


@view_config(route_name='new', renderer='new.mako')
def new_view(request):
    #
    #  view with mako
    #
    if request.method == 'POST':
        if request.POST.get('name'):
            request.db.execute('insert into tasks (name, closed) values (?, ?)',
                               [request.POST['name'], 0])
            request.db.commit()
            request.session.flash('New task was successfully added!')
            return HTTPFound(location=request.route_url('list'))
        else:
            request.session.flash('Please enter a name for the task!')
    return {}


@view_config(route_name='close')
def close_view(request):
    #
    #  view with mako
    #
    log.info('ho ho there')
    task_id = int(request.matchdict['id'])
    request.db.execute("update tasks set closed = ? where id = ?", (1, task_id))
    request.db.commit()
    request.session.flash('Task was successfully closed!')
    return HTTPFound(location=request.route_url('list'))


def get_first_param(request, name, def_val=None):
    """ 
    """
    ret_val=def_val
    try:
        ret_val = request.params.getone(name)
    except:
        pass

    return ret_val


@view_config(route_name='vote')
def vote_view(request):
    #
    #  vote recording via SqlAlchemy
    #
    vote_value = get_first_param(request, 'vote_value')
    user_id = get_first_param(request, 'user_id')
    stop_id = get_first_param(request, 'stop_id')
    log.info("{0}, {1}, {2}".format(vote_value, user_id, stop_id))

    v = Vote(vote_value, user_id, stop_id)
    db_ctl = DbController(db_path)
    session = db_ctl.get_session()
    session.add(v)
    session.commit()
    session.flush()

    return Response('OK')


@view_config(context='pyramid.exceptions.NotFound', renderer='notfound.mako')
def notfound_view(self):
    #
    #  view with mako
    #
    return {}


def pyramid_config():
    # configuration settings
    settings = {}
    settings['reload_all'] = True
    settings['debug_all'] = True
    settings['mako.directories'] = os.path.join(here, 'templates')

    # session factory
    session_factory = UnencryptedCookieSessionFactoryConfig('itsaseekreet')

    # configuration setup
    config = Configurator(settings=settings, session_factory=session_factory)
    config.scan()

    return config


def main():
    config = pyramid_config()

    # routes setup
    config.add_route('list', '/')
    config.add_route('vote', '/vote')
    config.add_route('new', '/new')
    config.add_route('close', '/close/{id}')

    # serve app
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()


if __name__ == '__main__':
    main()
