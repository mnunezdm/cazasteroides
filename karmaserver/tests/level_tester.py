''' Module for Level Tests '''
import json

import requests

from config import ENDPOINT
from tests.test import TestAbstract
from karmaserver.utils import generate_test_name


class CalculateDefaultPolicyTest(TestAbstract):
    ''' Creates one Observation '''
    def __init__(self):
        self.error_message = ''

    def run(self):
        status, response, _ = _call_server_calculate('default', 1000)
        if not response['code'] == 200:
            self.error_message = response['description']
        return status and response['code'] == 200

    def get_result(self):
        if self.error_message:
            return self.error_message
        return ''


class CalculateNonExistingPolicyTest(TestAbstract):
    ''' Creates one Observation '''
    def __init__(self):
        self.error_message = ''
        self.test_name = generate_test_name()

    def run(self):
        status, response, _ = _call_server_calculate(self.test_name, 1000)
        if not response['code'] == 404:
            self.error_message = response['description']
        return status and response['code'] == 404

    def get_result(self):
        if self.error_message:
            return self.error_message
        return ''


class CalculateExistingPolicyTest(TestAbstract):
    ''' Creates one Observation '''
    def __init__(self):
        self.error_message = ''
        self.policy = _get_policy_data('correct')
        self.test_name = generate_test_name()

    def run(self):
        status, response, _ = _call_server_crud('POST', self.test_name, self.policy)
        status, response, _ = _call_server_calculate(self.test_name, 1000)
        if not response['code'] == 200:
            self.error_message = response['description']
        return status and response['code'] == 200

    def get_result(self):
        if self.error_message:
            return self.error_message
        return ''


class CreateCorrectPolicyTest(TestAbstract):
    ''' Creates one Observation '''
    def __init__(self):
        self.error_message = ''
        self.test_name = generate_test_name()
        self.policy = _get_policy_data('correct')

    def run(self):
        status, response, _ = _call_server_crud('POST', self.test_name, self.policy)
        if not response['code'] == 201:
            self.error_message = response['description']
        return status and response['code'] == 201

    def get_result(self):
        if self.error_message:
            return self.error_message
        return ''


class CreateDefaultPolicyTest(TestAbstract):
    ''' Creates one Observation '''
    def __init__(self):
        self.error_message = ''
        self.policy = _get_policy_data('correct')

    def run(self):
        status, response, _ = _call_server_crud('POST', 'default', self.policy)
        if not response['code'] == 400:
            self.error_message = response['description']
        return status and response['code'] == 400

    def get_result(self):
        if self.error_message:
            return self.error_message
        return ''


class CreateEmptyPolicyTest(TestAbstract):
    ''' Creates one Observation '''
    def __init__(self):
        self.error_message = ''
        self.test_name = generate_test_name()
        self.policy = _get_policy_data('empty')

    def run(self):
        status, response, _ = _call_server_crud('POST', self.test_name, self.policy)
        if not response['code'] == 400:
            self.error_message = response['description']
        return status and response['code'] == 400

    def get_result(self):
        if self.error_message:
            return self.error_message
        return ''


class CreateInvalidFormulaPolicyTest(TestAbstract):
    ''' Creates one Observation '''
    def __init__(self):
        self.error_message = ''
        self.test_name = generate_test_name()
        self.policy = _get_policy_data('bad_formula')

    def run(self):
        status, response, _ = _call_server_crud('POST', self.test_name, self.policy)
        if not response['code'] == 400:
            self.error_message = response['description']
        return status and response['code'] == 400

    def get_result(self):
        if self.error_message:
            return self.error_message
        return ''


class CreateInvalidMaxLevelPolicyTest(TestAbstract):
    ''' Creates one Observation '''
    def __init__(self):
        self.error_message = ''
        self.test_name = generate_test_name()
        self.policy = _get_policy_data('nan')

    def run(self):
        status, response, _ = _call_server_crud('POST', self.test_name, self.policy)
        if not response['code'] == 400:
            self.error_message = response['description']
        return status and response['code'] == 400

    def get_result(self):
        if self.error_message:
            return self.error_message
        return ''


class CreateRepeatedPolicyTest(TestAbstract):
    ''' Creates one Observation '''
    def __init__(self):
        self.error_message = ''
        self.test_name = generate_test_name()
        self.policy = _get_policy_data('correct')

    def run(self):
        status, response, _ = _call_server_crud('POST', self.test_name, self.policy)
        status, response, _ = _call_server_crud('POST', self.test_name, self.policy)
        if not response['code'] == 400:
            self.error_message = response['description']
        return status and response['code'] == 400

    def get_result(self):
        if self.error_message:
            return self.error_message
        return ''


class UpdateBadFormulaTest(TestAbstract):
    ''' Creates one Observation '''
    def __init__(self):
        self.error_message = ''
        self.policy = _get_policy_data('only_bad_formula')

    def run(self):
        status, response, _ = _call_server_crud('PUT', 'default', self.policy)
        if not response['code'] == 400:
            self.error_message = response['description']
        return status and response['code'] == 400

    def get_result(self):
        if self.error_message:
            return self.error_message
        return ''


class UpdateInvalidMaxLevelTest(TestAbstract):
    ''' Creates one Observation '''
    def __init__(self):
        self.error_message = ''
        self.policy = _get_policy_data('only_bad_level')

    def run(self):
        status, response, _ = _call_server_crud('PUT', 'default', self.policy)
        if not response['code'] == 400:
            self.error_message = response['description']
        return status and response['code'] == 400

    def get_result(self):
        if self.error_message:
            return self.error_message
        return ''


class UpdateMaxLevelTest(TestAbstract):
    ''' Creates one Observation '''
    def __init__(self):
        self.error_message = ''
        self.policy = _get_policy_data('only_level')

    def run(self):
        status, response, _ = _call_server_crud('PUT', 'default', self.policy)
        if not response['code'] == 200:
            self.error_message = response['description']
        return status and response['code'] == 200

    def get_result(self):
        if self.error_message:
            return self.error_message
        return ''


class DeleteNonExistingPolicy(TestAbstract):
    ''' Creates one Observation '''
    def __init__(self):
        self.error_message = ''
        self.test_name = generate_test_name()

    def run(self):
        status, response, _ = _call_server_crud('DELETE', self.test_name)
        if not response['code'] == 404:
            self.error_message = response['description']
        return status and response['code'] == 404

    def get_result(self):
        if self.error_message:
            return self.error_message
        return ''


class DeleteExistingPolicy(TestAbstract):
    ''' Creates one Observation '''
    def __init__(self):
        self.error_message = ''
        self.test_name = generate_test_name()
        self.policy = _get_policy_data('correct')

    def run(self):
        status, response, _ = _call_server_crud('POST', self.test_name, self.policy)
        status, response, _ = _call_server_crud('DELETE', self.test_name)
        if not response['code'] == 200:
            self.error_message = response['description']
        return status

    def get_result(self):
        if self.error_message:
            return self.error_message
        return ''


class GetInfoExistingPolicy(TestAbstract):
    ''' Creates one Observation '''
    def __init__(self):
        self.error_message = ''
        self.test_name = generate_test_name()
        self.policy = _get_policy_data('correct')

    def run(self):
        status, response, _ = _call_server_crud('POST', self.test_name, self.policy)
        status, response, _ = _call_server_crud('GET', self.test_name)
        if not response['code'] == 200:
            self.error_message = response['description']
        return status and response['code'] == 200

    def get_result(self):
        if self.error_message:
            return self.error_message
        return ''


class GetInfoNonExistingPolicy(TestAbstract):
    ''' Creates one Observation '''
    def __init__(self):
        self.error_message = ''
        self.test_name = generate_test_name()

    def run(self):
        status, response, _ = _call_server_crud('GET', self.test_name)
        if not response['code'] == 404:
            self.error_message = response['description']
        return status and response['code'] == 404

    def get_result(self):
        if self.error_message:
            return self.error_message
        return ''


class GetInfoDeletedPolicy(TestAbstract):
    ''' Creates one Observation '''
    def __init__(self):
        self.error_message = ''
        self.test_name = generate_test_name()
        self.policy = _get_policy_data('correct')

    def run(self):
        status, response, _ = _call_server_crud('POST', self.test_name, self.policy)
        status, response, _ = _call_server_crud('DELETE', self.test_name)
        status, response, _ = _call_server_crud('GET', self.test_name)
        if not response['code'] == 404:
            self.error_message = response['description']
        return status and response['code'] == 404

    def get_result(self):
        if self.error_message:
            return self.error_message
        return ''


def _call_server_crud(method, policy_id, policy_data=None):
    try:
        if method == 'POST':
            response = requests.post(f'{ENDPOINT}/level/{policy_id}', json=policy_data)
        if method == 'GET':
            response = requests.get(f'{ENDPOINT}/level/{policy_id}')
        if method == 'PUT':
            response = requests.put(f'{ENDPOINT}/level/{policy_id}', json=policy_data)
        if method == 'DELETE':
            response = requests.delete(f'{ENDPOINT}/level/{policy_id}')
        time_ = float(response.headers['Request-Time'].replace(" ns", ""))
        return True, response.json(), time_
    except requests.exceptions.ConnectionError:
        return False, 'Could not connect to the server', None


def _call_server_calculate(policy_id, points):
    try:
        response = requests.get(f'{ENDPOINT}/level/{policy_id}/{points}')
        time_ = float(response.headers['Request-Time'].replace(" ns", ""))
        return True, response.json(), time_
    except requests.exceptions.ConnectionError:
        return False, 'Could not connect to the server', None


def _get_policy_data(json_name):
    with open(f'examples/level/{json_name}.json') as data_file:
        return json.load(data_file)
