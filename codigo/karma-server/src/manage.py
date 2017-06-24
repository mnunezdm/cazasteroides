''' Manage module, provides all the interaction with the server '''
from flask_migrate import MigrateCommand
from flask_script import Manager, Shell

from app import create_app, start_server
from debugger import init_terminal_colors

init_terminal_colors()
app = create_app()
manager = Manager(app)
manager.add_command("shell", Shell())
manager.add_command("db", MigrateCommand)


@manager.command
def runtests():
    ''' Runs all the configured tests '''
    from testers import run_all_tests
    run_all_tests()

@manager.command
def runserver():
    ''' Runs server with default configuration '''
    start_server(app)

manager.run()
