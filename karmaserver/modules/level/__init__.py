''' Level Module '''

from flask import Blueprint, jsonify, request, json
from karmaserver.utils import serialize_response
from karmaserver.utils.validate import is_number
from karmaserver.modules.level.provider import KarmaLevelProvider
from karmaserver.data.models.policy import InvalidFormulaException, PolicyNotExistsException, PolicyExistsException
from sqlalchemy.exc import IntegrityError, InvalidRequestError

level = Blueprint('level', __name__,
                  url_prefix='/level')
LEVEL_PROVIDER = KarmaLevelProvider()


@level.route('/<policy>/<int:user_points>', methods=['GET'])
def get_level(policy, user_points):
    ''' Returns karma info for the points passed'''
    try:
        result = LEVEL_PROVIDER.get_level(policy, user_points)
        return serialize_response(200, 'OK', 'Correct', result)
    except PolicyNotExistsException:
        return serialize_response(404, 'NOT FOUND', f'Policy {policy} could not be found')


@level.route('/<policy>', methods=['GET'])
def get_levels(policy):
    ''' Returns all karma info '''
    try:
        result = LEVEL_PROVIDER.get_levels(policy)
        return serialize_response(200, 'OK', 'Correct', result)
    except PolicyNotExistsException:
        return serialize_response(404, 'NOT FOUND', f'Policy {policy} could not be found')


@level.route('/<policy_id>', methods=['POST'])
def create_policy(policy_id):
    ''' Returns all karma info '''
    formula, max_level, errors = __check_request_data(request.get_json())
    if errors:
        return serialize_response(400, 'BAD REQUEST', errors)
    try:
        LEVEL_PROVIDER.create_policy(policy_id, formula, max_level)
        return serialize_response(201, 'CREATED', 'Policy Created Successfully')
    except InvalidFormulaException as exception:
        return serialize_response(400, 'BAD REQUEST', 'Malformed Formula',
                                  json.loads(str(exception))['errors'])
    except PolicyExistsException:
        return serialize_response(400, 'BAD REQUEST', f'Policy {policy_id} Already Exists')


@level.route('/<policy_id>', methods=['PUT'])
def update_policy(policy_id):
    ''' Returns all karma info '''
    formula, max_level, errors = __check_request_data(request.get_json(), update=True)
    if errors:
        return serialize_response(400, 'BAD REQUEST', errors)
    try:
        LEVEL_PROVIDER.update_policy(policy_id, formula=formula, max_level=max_level)
        return serialize_response(200, 'UPDATED', f'Updated policy {policy_id}')
    except PolicyNotExistsException:
        return serialize_response(404, 'NOT FOUND', f'Policy {policy_id} could not be found')
    except InvalidFormulaException as exception:
        return serialize_response(400, 'BAD REQUEST', 'Malformed Formula',
                                  json.loads(str(exception))['errors'])


@level.route('/<policy_id>', methods=['DELETE'])
def delete_policy(policy_id):
    ''' Returns all karma info '''
    try:
        LEVEL_PROVIDER.delete_policy(policy_id)
        return serialize_response(200, 'DELETED', f'Deleted policy {policy_id}')
    except PolicyNotExistsException:
        return serialize_response(404, 'NOT FOUND', f'Policy {policy_id} could not be found')


def __check_request_data(request_data, update=False):
    if not request_data:
        return None, None, 'Empty Request'
    formula = request_data.get('formula')
    max_level = request_data.get('max_level')
    if update and not formula and not max_level:
        return None, None, 'Must unless one of formula or max_level'
    if not update and (not formula or not max_level):
        return None, None, 'Must provide formula and max_level'
    if max_level and not is_number(max_level):
        return None, None, 'max_level must be a number'
    return formula, max_level, None
    