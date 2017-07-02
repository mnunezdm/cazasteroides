''' Manage module, provides all the interaction with the server '''
from flask_migrate import MigrateCommand
from flask_script import Manager, Shell

import utils.print as print_
from app import create_app, start_server

print_.init_terminal_colors()
print_.launch_server()
app = create_app()
manager = Manager(app)
manager.add_command("shell", Shell())
manager.add_command("db", MigrateCommand)


@manager.command
def runtests():
    ''' Runs all the configured tests '''
    from tests import run_all_tests
    run_all_tests()


@manager.command
def runserver():
    ''' Runs server with default configuration '''
    start_server(app)


manager.run()
