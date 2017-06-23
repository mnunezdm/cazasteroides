from flask import Blueprint, jsonify, abort, request
from configuration_params import MAX_KARMA_LEVEL, MAX_FILTER_LEVEL
from modules.selection.provider import ObservationSelectionProvider
from content_resolver import content_resolver

selection = Blueprint('selection', __name__,
                      url_prefix='/selection')

SELECTION_PROVIDER = ObservationSelectionProvider(MAX_KARMA_LEVEL, MAX_FILTER_LEVEL)

@selection.route('/v1/selection', methods=['GET'])
def get_new_observation():
    ''' Returns the information for the id passed '''
    user_id = request.args.get('user')
    karma_level = request.args.get('karma')
    if user_id and karma_level:
        try:
            karma_level = int(karma_level)
            return jsonify(SELECTION_PROVIDER.get_new_observation(user_id, karma_level))
        except ValueError:
            abort(400, 'Karma must be a number')
    abort(400, 'You have to pass user and karma as url params')
