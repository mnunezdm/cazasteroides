''' Module for Selection Tests '''
import threading
import time
from math import floor
from random import random, randint

import requests

from karmaserver.constants import ENDPOINT
from karmaserver.tests.test import TestAbstract
from karmaserver.data.models.observation import State
from karmaserver.utils import generate_test_name


# Invalid Requests
class EmptyRequestTest(TestAbstract):
    ''' Creates one Observation '''
    def __init__(self):
        self.error_message = ''

    def run(self):
        status, response, code = _call_server()
        if not status or code != 400:
            self.error_message = response
        return status and code == 400

    def get_result(self):
        if self.error_message:
            return self.error_message
        return ''


class NoKarmaTest(TestAbstract):
    ''' Creates one Observation '''
    def __init__(self):
        self.error_message = ''

    def run(self):
        status, response, code = _call_server(user='test')
        if not status or code != 400:
            self.error_message = response
        return status and code == 400

    def get_result(self):
        if self.error_message:
            return self.error_message
        return ''


class InvalidKarmaTest(TestAbstract):
    ''' Creates one Observation '''
    def __init__(self):
        self.error_message = ''

    def run(self):
        status, response, code = _call_server(user='test', karma='test')
        if not status or code != 400:
            self.error_message = response
        return status and code == 400

    def get_result(self):
        if self.error_message:
            return self.error_message
        return ''


class NoUserTest(TestAbstract):
    ''' Creates one Observation '''
    def __init__(self):
        self.error_message = ''

    def run(self):
        status, response, code = _call_server(karma='test')
        if not status or code != 400:
            self.error_message = response
        return status and code == 400

    def get_result(self):
        if self.error_message:
            return self.error_message
        return ''


# Correct Requests
class ApprovedForNewbiesTest(TestAbstract):
    ''' Creates one Observation '''
    def __init__(self):
        self.error_message = ''

    def run(self):
        status, response, code = _call_server(karma=1, user='test')
        if not status or code != 200:
            self.error_message = response
        return status and code == 200 and response['payload']['state'] == State.APPROVED.value

    def get_result(self):
        if self.error_message:
            return self.error_message
        return ''


class DisputedForProsTest(TestAbstract):
    ''' Creates one Observation '''
    def __init__(self):
        self.user_name = generate_test_name()
        self.error_message = ''

    def run(self):
        status, response, code = _call_server(karma=10000, user=self.user_name)
        if not status or code != 200:
            self.error_message = response
        return status and code == 200 and response['payload']['state'] == State.DISPUTED.value

    def get_result(self):
        if self.error_message:
            return self.error_message
        return ''


def _call_server(user=None, karma=None):
    try:
        response = requests.get(f'{ENDPOINT}/selection/vote',
                                params=__generate_query_params(user, karma)).json()
        return True, response, response['code']
    except requests.exceptions.ConnectionError:
        return False, 'Could not connect to the server', None


def __generate_query_params(user, karma):
    return {"user":user, "karma":karma}
