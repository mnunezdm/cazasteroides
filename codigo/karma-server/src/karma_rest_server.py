''' This is the REST implementation of the server,
    has all the REST methods and a Karma Server instance'''
from flask import Flask, jsonify, make_response, abort, request
from karma_server import KarmaServer
from debugger import print_info, init_colors

APP = Flask(__name__)

# API Endpoints

# localhost:5000/v1.0/karma/<int:user_points>
@APP.route('/v1.0/karma/<int:user_points>', methods=['GET'])
def get_user_info(user_points):
    ''' Returns karma info for the points passed'''
    result = SERVER.get_karma_for_points(user_points)
    return jsonify(result)

# localhost:5000/v1.0/karma/info>
@APP.route('/v1.0/karma/info', methods=['GET'])
def get_general_info():
    ''' Returns all karma info '''
    return jsonify(SERVER.get_karma_general_info())

# localhost:5000/v1.0/karma/info>
@APP.route('/v1.0/validate', methods=['POST'])
def post_vote():
    ''' Updates the info for the observation passed '''
    request_data = request.get_json()
    if request_data:
        result = SERVER.post_vote(request_data)
        if result:
            return jsonify(result.serialize())
    abort(400)

@APP.route('/v1.0/validate/<string:observation_id>', methods=['GET'])
def get_observation(observation_id):
    ''' Returns the information for the id passed '''
    observation = SERVER.get_observation_data(observation_id)
    if not observation:
        abort(404)
    return jsonify(SERVER.get_observation_data(observation_id).serialize())

# Error Handlers
@APP.errorhandler(400)
def bad_request(_):
    ''' Bad Request Handler '''
    return make_response(jsonify({'code':400, 'error': 'Bad Request'}), 400)

@APP.errorhandler(404)
def not_found(_):
    ''' Not Found Handler '''
    return make_response(jsonify({'code':404, 'error': 'Not found'}), 404)

@APP.errorhandler(405)
def not_allowed(_):
    ''' Not Allowed Handler '''
    return make_response(jsonify({'code':405, 'error':'Method not Allowed'}), 404)

# Main Method
if __name__ == '__main__':
    init_colors()
    SERVER = KarmaServer()
    print_info('INFO', 'Starting REST Server')
    APP.run()
