''' Tester module for testing Validation Provider '''
import threading
from math import floor
from random import random
from config import ENDPOINT

import requests

from testers.tester import Tester

class CreateRandomObservationTest(Tester):
    ''' Creates one Observation '''
    def __init__(self):
        self.dictionary = _generate_observation()
        self.error_message = ''

    def run(self):
        status, response = _call_server(self.dictionary)
        if not status:
            self.error_message = response
        return status

    def get_result(self):
        if self.error_message:
            return self.error_message
        return ''

class StressValidationTest(Tester):
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
        return '(Average request time {} ns)'.format(elapsed)

    def __run(self, number_of_requests):
        cont = 1
        while cont < number_of_requests:
            dictionary = _generate_observation()
            status, response = _call_server(dictionary)
            if not status:
                self.error_message = response
                return
            time = response['time']
            self.result.append(time)
            cont = cont + 1
        if cont != number_of_requests:
            self.error_message = 'Exception in server'

class DoubleUserObservation(Tester):
    ''' Sends to repeated votation, must receive a Bad Request (400) in the second one '''
    def __init__(self):
        self.dictionary = _generate_observation()
        self.error_message = ''

    def run(self):
        _call_server(self.dictionary)
        status, response = _call_server(self.dictionary)
        if not status:
            self.error_message = response
        return status and response['code'] == 400

    def get_result(self):
        if self.error_message:
            return self.error_message
        return ''

def _call_server(dictionary):
    try:
        jsoned = requests.post('{}validation/vote'.format(ENDPOINT),
                               json=dictionary).json()
        return True, jsoned
    except requests.exceptions.ConnectionError:
        return False, 'Could not connect to the server'

def _generate_observation():
    dictionary = {
        "user_info": {
            "_id": str(floor(random() * 30 + 1))
        },
        "vote_info": {
            "karma_level": floor(random() * 20 + 1),
            "vote_type": random() < 0.5
        },
        "observation_info": {
            "_id": str(floor(random() * 1000 + 1)),
            "brightness": floor(random() * 20 + 5),
            "image": {
                "_id": "1",
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

def get_all_tests():
    ''' Returns all tests '''
    return [CreateRandomObservationTest(), StressValidationTest(), DoubleUserObservation()]
