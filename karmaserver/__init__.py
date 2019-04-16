''' This is the REST implementation of the server,
    has all the REST methods and a Karma Server instance'''

import logging

from flask import Flask, json, make_response, request
from karmaserver.data.models import db

from karmaserver.data.models.image import Image
from karmaserver.data.models.observation import Observation
from karmaserver.data.models.policy import Policy
from karmaserver.data.models.position import Position
from karmaserver.data.models.puntuation import Puntuation
from karmaserver.data.models.user import User
from karmaserver.data.models.votes import Votes
from karmaserver.utils import serialize_response, start_timer, stop_timer
import karmaserver.utils.print as print_
import karmaserver.modules


def create_app():
    ''' App Factory '''
    app = Flask(__name__)
    app.config.from_object('karmaserver.constants')
    db.init_app(app)
    return app


def start_server(app, no_stdout, condition=None, host='localhost', port=5000):
    ''' Starts the application passed as parameter '''
    __custom_configuration(app, no_stdout)
    print_.title("Launching Modules")
    for module in karmaserver.modules.get_all_modules():
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
