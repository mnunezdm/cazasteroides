from math import floor
from random import random
import sys

import requests
from flask import jsonify
from requests.exceptions import ConnectionError

from debugger import print_error, print_info, init_terminal_colors


def __generate_random_observation():
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


result = []
cont = 1
init_terminal_colors()
try:
    while True:
        dictionary = __generate_random_observation()

        jsoned_response = requests.post("http://localhost:5000/v1/validate", json=dictionary).json()

        time = jsoned_response['time']
        result.append(time)
        obs_id = dictionary['observation_info']['_id']
        user_id = dictionary['user_info']['_id']
        print_info('INFO-{}'.format(cont),
                   'Observation {} for user {} time {} ns'.format(obs_id, user_id, time))
        cont = cont + 1
except ConnectionError as exception:
    print_error('Server unreachable, maybe is down?')
finally:
    if result:
        print_info('INFO', 'Average time request {}ns'.format(str(floor(sum(result)/len(result)))))
    else:
        print_error('Exception in Server')
    sys.exit(1)
