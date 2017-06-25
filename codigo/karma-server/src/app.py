''' This is the REST implementation of the server,
    has all the REST methods and a Karma Server instance'''

import logging

from flask import Flask, json, jsonify, make_response, request
from flask_migrate import Migrate

from utils import start_timer, stop_timer
import utils.print as print_
from utils import serialize_response
from models import db
from models.image import Image
from models.observation import Observation
from models.position import Position
from models.puntuation import Puntuation
from models.user import User
from models.votes import Votes
from models.policy import Policy


def create_app():
    ''' App Factory '''
    app = Flask(__name__)

    app.config.from_object('config')
    set_error_handlers(app)
    set_pre_post_requests(app)
    logging.getLogger('werkzeug').disabled = True

    db.init_app(app)
    Migrate(app, db)
    return app


def start_server(app, host='localhost', port=5000):
    ''' Starts the application passed as parameter '''
    print_.title("Launching Modules")
    import modules
    for module in modules.get_all_modules():
        app.register_blueprint(module)
    print_.title("Starting Server")
    print_.info('INFO', f'Starting Server at {host}:{port}')
    app.run(host=host, port=port)


def set_error_handlers(app):
    ''' Sets error handlers for the app passed '''
    @app.errorhandler(400)
    def bad_request(error):
        ''' Bad Request Handler '''
        return make_response(serialize_response(400, 'Bad Request',
                                                error.description), 400)

    @app.errorhandler(404)
    def not_found(error):
        ''' Not Found Handler '''
        return make_response(serialize_response(404, 'Not Found',
                                                error.description), 404)

    @app.errorhandler(405)
    def not_allowed(error):
        ''' Not Allowed Handler '''
        return make_response(serialize_response(405, 'Method not allowed',
                                                error.description), 405)

def set_pre_post_requests(app):
    @app.before_request
    def __start_timer():
        request.time_start = start_timer()

    @app.after_request
    def __end_time(response):
        elapsed = stop_timer(request.time_start)
        data = json.loads(response.get_data())
        print_.http(request.method, request.path, data['code'], data['status'],
                    data['description'], elapsed)
        response.headers["Request-Time"] = f'{elapsed} ns'
        return response
