''' Manage module, provides all the interaction with the server '''
import os
import sys
import threading

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
    condition = threading.Condition()
    thread = ThreadWithReturnValue(target=__call_tests, args=(condition, ))
    thread.start()
    condition.acquire()
    runserver(no_stdout=True, condition=condition)
    result = thread.join()
    if result:
        sys.exit(0)
    else:
        sys.exit(-1)

def __call_tests(condition):
    condition.acquire()
    condition.wait()
    from tests import run_all_tests
    result = run_all_tests()
    condition.release()
    return result


@manager.command
def runserver(no_stdout=False, condition=None):
    ''' Runs server with default configuration '''
    if not os.path.isfile('app.db'):
        initdb()
    start_server(app, no_stdout, condition)


@manager.command
def initdb():
    """Initializes the database."""
    db.create_all()
    print_.info('INFO', 'Database Created')


class ThreadWithReturnValue(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        threading.Thread.__init__(self, group, target, name, args, kwargs, daemon=daemon)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self):
        threading.Thread.join(self)
        return self._return

manager.run()
