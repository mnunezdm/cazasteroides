''' This is the REST implementation of the server,
    has all the REST methods and a Karma Server instance'''

import logging

from flask import Flask, json, make_response, request

from utils import start_timer, stop_timer
import utils.print as print_
from utils import serialize_response
from data.models import db
from data.models.image import Image
from data.models.observation import Observation
from data.models.position import Position
from data.models.puntuation import Puntuation
from data.models.user import User
from data.models.votes import Votes
from data.models.policy import Policy


def create_app():
    ''' App Factory '''
    app = Flask(__name__)
    app.config.from_object('config')
    db.init_app(app)
    return app


def start_server(app, no_stdout, condition=None, host='localhost', port=5000):
    ''' Starts the application passed as parameter '''
    __custom_configuration(app, no_stdout)
    print_.title("Launching Modules")
    import modules
    for module in modules.get_all_modules():
        app.register_blueprint(module)
    print_.title("Starting Server")
    print_.info('INFO', f'Starting Server at {host}:{port}')
    if condition:
        condition.notify()
        condition.release()
    app.run(host=host, port=port)

def __shutdown(app):
    @app.route('/shutdown')
    def __shutdown():
        ''' Shutdown the server '''
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()
        return serialize_response(200, 'OK', 'Server Shutting Down')


def __custom_configuration(app, no_stdout):
    __shutdown(app)
    logging.getLogger('werkzeug').disabled = True
    set_error_handlers(app)
    set_pre_post_requests(app, no_stdout)


def set_error_handlers(app):
    ''' Sets error handlers for the app passed '''
    @app.errorhandler(400)
    def __bad_request(error):
        ''' Bad Request Handler '''
        return make_response(serialize_response(400, 'Bad Request',
                                                error.description), 400)


    @app.errorhandler(404)
    def __not_found(error):
        ''' Not Found Handler '''
        return make_response(serialize_response(404, 'Not Found',
                                                error.description), 404)


    @app.errorhandler(405)
    def __not_allowed(error):
        ''' Not Allowed Handler '''
        return make_response(serialize_response(405, 'Method not allowed',
                                                error.description), 405)


    @app.errorhandler(Exception)
    def __exception(exception):
        return make_response(serialize_response(500, 'Internal Error',
                                                str(exception)), 405)


def set_pre_post_requests(app, no_stdout):
    ''' Sets the functionality for the pre and post request handling '''
    @app.before_request
    def __start_timer():
        request.time_start = start_timer()

    @app.after_request
    def __end_time(response):
        elapsed = stop_timer(request.time_start)
        data = json.loads(response.get_data())
        if not no_stdout:
            print_.http(request.method, request.path, data['code'], data['status'],
                        data['description'], elapsed)
        response.headers["Request-Time"] = f'{elapsed} ns'
        return response
