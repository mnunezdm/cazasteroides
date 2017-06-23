from flask import Blueprint, jsonify
from configuration_params import MAX_KARMA_LEVEL, POINTS_PER_OBSERVATION
from modules.level.provider import KarmaLevelProvider

level = Blueprint('level', __name__,
                  url_prefix='/level')
LEVEL_PROVIDER = KarmaLevelProvider(MAX_KARMA_LEVEL, POINTS_PER_OBSERVATION)

# localhost:5000/karma/info>
@level.route('/<int:user_points>', methods=['GET'])
def get_user_info(user_points):
    ''' Returns karma info for the points passed'''
    result = LEVEL_PROVIDER.get_level_for_points(user_points)
    return jsonify(result)

# localhost:5000/karma/info>
@level.route('/info', methods=['GET'])
def get_general_info():
    ''' Returns all karma info '''
    return jsonify(LEVEL_PROVIDER.get_general_info())
