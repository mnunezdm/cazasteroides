''' Manage module, provides all the interaction with the server '''
import os
import sys
import threading

from flask_script import Manager

import karmaserver.utils.print as print_
from karmaserver import create_app, db, start_server
from karmaserver.utils import check_if_server_up

print_.init_terminal_colors()
print_.launch_server()
app = create_app()
manager = Manager(app)


@manager.command
def runtests():
    ''' Runs all the configured tests '''
    if check_if_server_up('localhost', 5000):
        print_.info('INFO', 'Server Already Up')
        import tests
        result = tests.run_all_tests()
    else:
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
    import tests
    result = tests.run_all_tests()
    condition.release()
    return result


@manager.command
def runserver(no_stdout=False, condition=None):
    ''' Runs server with default configuration '''
    if check_if_server_up('localhost', 5000):
        print_.error('Server Already Running at port 5000')
        sys.exit(-1)
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
