''' This is the REST implementation of the server,
    has all the REST methods and a Karma Server instance'''
import json
from sys import argv

from flask import Flask, abort, jsonify, make_response, request
from flask_migrate import Migrate

from debugger import (init_terminal_colors, print_error, print_info,
                      start_timer, stop_timer)
from karma_server import KarmaServer
from models import db
from models.image import Image  # necessary for migrate tool detect this table
from models.user import User    # necessary for migrate tool detect this table

init_terminal_colors()

if __name__ == '__main__':
    print_error('Run from manage.py')
    exit(1)

app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)

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

############################################################################
# API Endpoints
# localhost:5000/v1/karma/<int:user_points>
@app.route('/v1/level/<int:user_points>', methods=['GET'])
def get_user_info(user_points):
    ''' Returns karma info for the points passed'''
    result = SERVER.get_karma_for_points(user_points)
    return jsonify(result)

# localhost:5000/v1/karma/info>
@app.route('/v1/level/info', methods=['GET'])
def get_general_info():
    ''' Returns all karma info '''
    return jsonify(SERVER.get_karma_general_info())

# localhost:5000/v1/validate>
@app.route('/v1/validate', methods=['POST'])
def post_vote():
    ''' Updates the info for the observation passed '''
    request_data = request.get_json()
    if not request_data:
        abort(400, 'Empty request')
    result = SERVER.post_vote(request_data)
    if not result:
        abort(400, 'Repeated votation for this user')
    return jsonify(result.serialize())

# localhost:5000/v1/validate/id>
@app.route('/v1/validate/<string:observation_id>', methods=['GET'])
def get_observation_info(observation_id):
    ''' Returns the information for the id passed '''
    observation = SERVER.get_observation_data(observation_id)
    if not observation:
        abort(404, 'Observation {} not found'.format(observation_id))
    return jsonify(SERVER.get_observation_data(observation_id).serialize())

@app.route('/v1/selection', methods=['GET'])
def get_new_observation():
    ''' Returns the information for the id passed '''
    user_id = request.args.get('user')
    karma_level = request.args.get('karma')
    if user_id and karma_level:
        try:
            karma_level = int(karma_level)
            return jsonify(SERVER.get_new_observation(user_id, karma_level))
        except ValueError:
            abort(400, 'Karma must be a number')
    abort(400, 'You have to pass user and karma as url params')

############################################################################
# Error Handlers
@app.errorhandler(400)
def bad_request(error):
    ''' Bad Request Handler '''
    return make_response(serialize_response(400, 'Bad Request', error.description), 400)

@app.errorhandler(404)
def not_found(error):
    ''' Not Found Handler '''
    return make_response(serialize_response(404, 'Not Found', error.description), 404)

@app.errorhandler(405)
def not_allowed(error):
    ''' Not Allowed Handler '''
    return make_response(serialize_response(405, 'Method not allowed', error.description), 405)
############################################################################
def serialize_response(code, status, description, payload=None):
    ''' Generate serialized responses '''
    response = {'code': code, 'status': status, 'description': description}
    if payload:
        response['payload'] = payload
    return jsonify(response)


# Intializing server methods
def instantiate_server(database):
    ''' Instantiate the server '''
    server = KarmaServer(database)
    print_info('INFO', 'Starting REST Server')
    return server

# Main Method
if len(argv) > 1 and 'runserver' in argv[1]:
    SERVER = instantiate_server(db)
