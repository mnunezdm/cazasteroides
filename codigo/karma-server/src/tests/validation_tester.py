''' Tester module for testing Validation Provider '''
import threading
import time
from math import floor
from random import random, randint

import requests

from config import ENDPOINT
from tests.test import TestAbstract


class CreateRandomObservationTest(TestAbstract):
    ''' Creates one Observation '''
    def __init__(self):
        self.dictionary = _generate_observation()
        self.error_message = ''

    def run(self):
        status, response, _ = _call_server(self.dictionary)
        if not status:
            self.error_message = response
        return status

    def get_result(self):
        if self.error_message:
            return self.error_message
        return ''


class StressValidationTest(TestAbstract):
    ''' Does 50 random validations '''
    def __init__(self):
        self.result = []
        self.error_message = None

    def run(self):
        threads = self.__get_thread_list()
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        return self.error_message is None

    def __get_thread_list(self):
        threads = []
        for _ in range(10):
            thread = threading.Thread(target=self.__run, args=(2,))
            threads.append(thread)
        return threads

    def get_result(self):
        if self.error_message:
            return self.error_message
        elapsed = floor(sum(self.result)/len(self.result))
        return f'(Average request time {elapsed} ns)'

    def __run(self, number_of_requests):
        cont = 1
        while cont < number_of_requests:
            dictionary = _generate_observation()
            status, response, time_ = _call_server(dictionary)
            if not status:
                self.error_message = response
                return
            self.result.append(time_)
            cont = cont + 1
        if cont != number_of_requests:
            self.error_message = 'Exception in server'


class DoubleUserObservationTest(TestAbstract):
    ''' Sends to repeated votation, must receive a Bad Request (400) in the second one '''
    def __init__(self):
        self.dictionary = _generate_observation()
        self.error_message = ''

    def run(self):
        _call_server(self.dictionary)
        status, response, _ = _call_server(self.dictionary)
        if not status:
            self.error_message = response
        return status and response['code'] == 400

    def get_result(self):
        if self.error_message:
            return self.error_message
        return ''


class MultipleVotesInSameObservationTest(TestAbstract):
    ''' Sends multiple votations to the same observation but different users '''
    def __init__(self):
        self.error_message = ''
        self.observation_id = f'test-{time.time()}'

    def run(self):
        for item in range(10):
            observation = _generate_observation(user_id=f'{self.observation_id}{item}',
                                                obs_id=self.observation_id)
            status, response, _ = _call_server(observation)
            if not status:
                self.error_message = response
                return
        return status

    def get_result(self):
        if self.error_message:
            return self.error_message
        return ''


class NoObservationTest(TestAbstract):
    ''' Sends to repeated votation, must receive a Bad Request (400) in the second one '''
    def __init__(self):
        self.dictionary = _generate_observation()
        self.error_message = ''

    def run(self):
        status, response, _ = _call_server(None)
        if not status:
            self.error_message = response
        return status and response['code'] == 400

    def get_result(self):
        if self.error_message:
            return self.error_message
        return ''


def _call_server(dictionary):
    try:
        response = requests.post(f'{ENDPOINT}/validation/vote',
                                 json=dictionary)
        time_ = float(response.headers['Request-Time'].replace(" ns", ""))
        return True, response.json(), time_
    except requests.exceptions.ConnectionError:
        return False, 'Could not connect to the server', None

def _generate_observation(user_id=None, karma_level=None, vote_type=None, obs_id=None):
    if user_id is None:
        user_id = randint(1, 1000)
    if vote_type is None:
        vote_type = random() < 0.75
    if karma_level is None:
        karma_level = randint(1, 1000)
    if obs_id is None:
        obs_id = randint(1, 1000)
    dictionary = {
        "user_info": {
            "_id": user_id
        },
        "vote_info": {
            "karma_level": karma_level,
            "vote_type": vote_type
        },
        "observation_info": {
            "_id": obs_id,
            "brightness": floor(random() * 20 + 5),
            "image": {
                "_id": floor(random() * 10 - 5),
                "fwhm": floor(random() * 10 - 5),
                "probability": floor(random() * 100),
                "x_size": 100,
                "y_size": 100
            },
            "votes": {
                "upvotes":0,
                "downvotes":0
            },
            "position": {
                "x": 12,
                "y": 15
            }
        }
    }
    return dictionary
