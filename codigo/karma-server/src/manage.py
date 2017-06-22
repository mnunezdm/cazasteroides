from flask_script import Manager, Shell, Server
from karma_rest_server import app
from flask_migrate import MigrateCommand

from testers import run_all_tests

manager = Manager(app)
manager.add_command("shell", Shell())
manager.add_command("db", MigrateCommand)

@manager.command
def runtests():
    ''' Runs all the configured tests '''
    run_all_tests()

manager.run()
