from flask_script import Manager, Shell, Server
from karma_rest_server import app
from flask_migrate import MigrateCommand

manager = Manager(app)
manager.add_command("shell", Shell())
manager.add_command("db", MigrateCommand)
manager.run()

@manager.option('-p', '--port', dest='port', default='5000')
def runserver(port):
    Server(port=port)
    