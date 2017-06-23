from flask import Blueprint, jsonify, abort, request
from configuration_params import MINIMUM_VOTES, MAXIMUM_VOTES, LOWER_LIMIT, UPPER_LIMIT
from modules.validation.provider import ValidationProvider

validation = Blueprint('validation', __name__,
                       url_prefix='/validation')
VALIDATION_PROVIDER = ValidationProvider(MINIMUM_VOTES, MAXIMUM_VOTES, LOWER_LIMIT,
                                         UPPER_LIMIT)

@validation.route('/vote', methods=['POST'])
def post_vote():
    ''' Updates the info for the observation passed '''
    request_data = request.get_json()
    if not request_data:
        abort(400, 'Empty request')
    result = VALIDATION_PROVIDER.post_vote(request_data)
    if not result:
        abort(400, 'Repeated votation for this user')
    return jsonify(result.serialize())

# localhost:5000/v1/validate/id>
@validation.route('/validate/<string:observation_id>', methods=['GET'])
def get_observation_info(observation_id):
    ''' Returns the information for the id passed '''
    observation = VALIDATION_PROVIDER.get_observation_data(observation_id)
    if not observation:
        abort(404, 'Observation {} not found'.format(observation_id))
    return jsonify(VALIDATION_PROVIDER.get_observation_data(observation_id).serialize())
    