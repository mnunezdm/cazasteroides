''' This is the REST implementation of the server,
    has all the REST methods and a Karma Server instance'''
from flask import Flask, jsonify, make_response
from KarmaServer import KarmaServer
from ConfigurationFile import MAX_KARMA_LEVEL, POINTS_PER_OBSERVATION
from Debugger import print_info, init_colors

APP = Flask(__name__)

# localhost:5000/v1.0/karma/<int:user_points>
@APP.route('/v1.0/karma/<int:user_points>', methods=['GET'])
def get_user_info(user_points):
    ''' Returns karma info for the points passed'''
    try:
        result = SERVER.get_karma_for_points(user_points)
    except IndexError:
        result = {"karma_level":MAX_KARMA_LEVEL}
    return jsonify(result)

# localhost:5000/v1.0/karma/info>
@APP.route('/v1.0/karma/info', methods=['GET'])
def get_general_info():
    ''' Returns all karma info '''
    return jsonify(SERVER.get_karma_general_info())

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
    print_info('INFO', 'Initiating KarmaServer with {} levels, {} ppo'.format(
        MAX_KARMA_LEVEL, POINTS_PER_OBSERVATION))
    SERVER = KarmaServer(MAX_KARMA_LEVEL, POINTS_PER_OBSERVATION)
    APP.run()
