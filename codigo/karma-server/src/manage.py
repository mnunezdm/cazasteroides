''' Manage module, provides all the interaction with the server '''
import os

import utils.print as print_
from flask_script import Manager
from app import create_app, start_server, db

print_.init_terminal_colors()
print_.launch_server()
app = create_app()
manager = Manager(app)


@manager.command
def runtests():
    ''' Runs all the configured tests '''
    from tests import run_all_tests
    run_all_tests()


@manager.command
def runserver():
    ''' Runs server with default configuration '''
    if not os.path.isfile('app.db'):
        initdb()
    start_server(app)


@manager.command
def initdb():
    """Initializes the database."""
    db.create_all()
    print_.info('INFO', 'Database Created')

manager.run()
