''' This is the REST implementation of the server,
    has all the REST methods and a Karma Server instance'''
from sys import argv

from flask import Flask, abort, jsonify, make_response, request
from flask_migrate import Migrate
from flask_script import Manager

from debugger import init_terminal_colors, print_error, print_info
from karma_server import KarmaServer
from models import db
from models.image import Image
from models.user import User
import time

init_terminal_colors()

if __name__ == '__main__':
    print_error('Run from manage.py')
    exit(1)

app = Flask(__name__)
app.config.from_object('config')
manager = Manager(app)
db.init_app(app)
migrate = Migrate(app, db)

@app.before_request
def __start_timer():
    global time_start
    time_start = time.clock()*1000000

@app.after_request
def __end_time(response):
    global time_start
    time_end = time.clock()*1000000
    elapsed = time_end - time_start
    print('Request time {}ns'.format(int(round(elapsed))))
    return response

# API Endpoints
# localhost:5000/v1/karma/<int:user_points>
@app.route('/v1/karma/<int:user_points>', methods=['GET'])
def get_user_info(user_points):
    ''' Returns karma info for the points passed'''
    result = SERVER.get_karma_for_points(user_points)
    return jsonify(result)

# localhost:5000/v1/karma/info>
@app.route('/v1/karma/info', methods=['GET'])
def get_general_info():
    ''' Returns all karma info '''
    return jsonify(SERVER.get_karma_general_info())

# localhost:5000/v1/validate>
@app.route('/v1/validate', methods=['POST'])
def post_vote():
    ''' Updates the info for the observation passed '''
    request_data = request.get_json()
    if request_data:
        result = SERVER.post_vote(request_data)
        if result:
            return jsonify(result.serialize())
    abort(400)

# localhost:5000/v1/validate/id>
@app.route('/v1/validate/<string:observation_id>', methods=['GET'])
def get_observation(observation_id):
    ''' Returns the information for the id passed '''
    observation = SERVER.get_observation_data(observation_id)
    if not observation:
        abort(404)
    return jsonify(SERVER.get_observation_data(observation_id).serialize())

# Error Handlers
@app.errorhandler(400)
def bad_request(_):
    ''' Bad Request Handler '''
    return make_response(jsonify({'code':400, 'error': 'Bad Request'}), 400)

@app.errorhandler(404)
def not_found(_):
    ''' Not Found Handler '''
    return make_response(jsonify({'code':404, 'error': 'Not found'}), 404)

@app.errorhandler(405)
def not_allowed(_):
    ''' Not Allowed Handler '''
    return make_response(jsonify({'code':405, 'error':'Method not Allowed'}), 404)

def initiate_server():
    server = KarmaServer()
    print_info('INFO', 'Starting REST Server')
    return server

# Main Method
if len(argv) > 1 and 'runserver' in argv[1]:
    SERVER = initiate_server()
