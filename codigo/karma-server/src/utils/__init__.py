''' Utils module, provides methods for common tasks '''
import time
from flask import jsonify
import utils.print as print_


def start_timer():
    ''' Returns the time in ns '''
    return __get_time_in_ns()


def stop_timer(time_start, description=None):
    ''' Calculates the elapsed time between the actual time and the passed time,
    prints the information, and returns the elapsed time '''
    time_stop = __get_time_in_ns()
    elapsed = round(time_stop - time_start)
    if description:
        print_.info('INFO', f'{elapsed} ns in {description}')
    return elapsed


def serialize_response(code, status, description, payload=None):
    ''' Generate serialized responses '''
    response = {'code': code, 'status': status, 'description': description}
    if payload:
        response['payload'] = payload
    return jsonify(response)


def __get_time_in_ns():
    return time.time() * pow(10, 7)


def generate_test_name():
    ''' Generates an unique test name with the current time '''
    return f'test-{__get_time_in_ns()}'
