''' This is the REST implementation of the server,
    has all the REST methods and a Karma Server instance'''
from flask import Flask, jsonify, make_response, json
from flask_migrate import Migrate

from debugger import (init_terminal_colors, print_error, print_info,
                      start_timer, stop_timer)
from models import db
from models.image import Image
from models.user import User
from models.observation import Observation
from models.puntuation import Puntuation
from models.position import Position
from models.votes import Votes

def create_app():
    init_terminal_colors()
    app = Flask(__name__)
    app.config.from_object('config')
    set_error_handlers(app)
    set_timer(app)
    db.init_app(app)
    Migrate(app, db)
    return app

def start_server(app):
    import modules
    for module in modules.get_all_modules():
        app.register_blueprint(module)
    app.run()

def set_error_handlers(app):
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

    def serialize_response(code, status, description, payload=None):
        ''' Generate serialized responses '''
        response = {'code': code, 'status': status, 'description': description}
        if payload:
            response['payload'] = payload
        return jsonify(response)

def set_timer(app):
    @app.before_request
    def __start_timer():
        global time_start
        time_start = start_timer()

    @app.after_request
    def __end_time(response):
        global time_start
        elapsed = stop_timer(time_start, 'FULL REQUEST')
        data = json.loads(response.get_data())
        data['time'] = elapsed
        response.set_data(json.dumps(data))
        return response
