''' Utils module, provides methods for common tasks '''
import time
from flask import jsonify
import utils.print as print_


def start_timer():
    ''' Returns the time in ns '''
    return time.clock() * 1000000


def stop_timer(time_start, description=None):
    ''' Calculates the elapsed time between the actual time and the passed time,
    prints the information, and returns the elapsed time '''
    time_stop = time.clock() * 1000000
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
