''' Selection Module '''

from flask import Blueprint, jsonify, abort, request
from utils import serialize_response
from config import MAX_KARMA_LEVEL, MAX_FILTER_LEVEL
from modules.selection.provider import ObservationSelectionProvider
from data.content_resolver import content_resolver

selection = Blueprint('selection', __name__,
                      url_prefix='/selection')


SELECTION_PROVIDER = ObservationSelectionProvider(MAX_KARMA_LEVEL, MAX_FILTER_LEVEL)


@selection.route('/discover', methods=['GET'])
def get_observation_for_discovery():
    ''' Returns the information for the id passed '''
    user_id, karma_level = __get_request_args_or_abort()
    observation = SELECTION_PROVIDER.select_observation_for_discover(user_id, karma_level)
    if observation:
        return serialize_response(200, 'OK', 'OK', observation)
    return serialize_response(204, 'No Content', 'No Valid Observation')


@selection.route('/vote', methods=['GET'])
def get_new_observation():
    ''' Returns the information for the id passed '''
    user_id, karma_level = __get_request_args_or_abort()
    observation = SELECTION_PROVIDER.select_observation_for_votation(user_id, karma_level)
    if observation:
        return serialize_response(200, 'OK', 'OK', observation)
    return serialize_response(204, 'No Content', 'No Valid Observation')


def __get_request_args_or_abort():
    user_id = request.args.get('user')
    karma_level = request.args.get('karma')
    if user_id and karma_level:
        try:
            karma_level = int(karma_level)
            return user_id, karma_level
        except ValueError:
            abort(400, 'Karma must be a number')
    abort(400, 'You have to pass user and karma as url params')
