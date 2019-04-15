''' Validation Module '''

from flask import Blueprint, abort, jsonify, request

from config import (CERTAINTY_LOWER_LIMIT, CERTAINTY_UPPER_LIMIT,
                    MINIMUM_VOTES, VOTES_TO_DISPUTED,
                    VOTES_TO_MINIMUM_CERTAINTY)
from karmaserver.modules.validation.provider import (ObservationNotFoundException,
                                         ValidationProvider)
from karmaserver.utils import serialize_response

validation = Blueprint('validation', __name__,
                       url_prefix='/validation')
VALIDATION_PROVIDER = ValidationProvider(MINIMUM_VOTES, VOTES_TO_DISPUTED, CERTAINTY_UPPER_LIMIT,
                                         CERTAINTY_LOWER_LIMIT, VOTES_TO_MINIMUM_CERTAINTY)


@validation.route('/vote', methods=['POST'])
def post_vote():
    ''' Updates the info for the observation passed '''
    request_data = request.get_json()
    if not request_data:
        return serialize_response(400, 'BAD REQUEST', 'Empty request')
    result = VALIDATION_PROVIDER.post_vote(request_data)
    if not result:
        return serialize_response(400, 'BAD REQUEST', 'Repeated vote for user')
    return serialize_response(200, 'OK', 'Vote added', result.serialize())


# localhost:5000/v1/validate/id>
@validation.route('/<observation_id>', methods=['GET'])
def get_observation_info(observation_id):
    ''' Returns the information for the id passed '''
    try:
        observation = VALIDATION_PROVIDER.get_observation_data(observation_id)
    except ObservationNotFoundException:
        return serialize_response(404, 'NOT FOUND', f'Observation {observation_id} not found')
    return serialize_response(200, 'OK', f'Observation Fetched Correctly', observation.serialize())
