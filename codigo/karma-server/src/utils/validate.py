''' Module to validate '''
import re
import math
from inspect import getmembers

SYMBOLS = {'+', '-', '*', '%', '/', '//', '%', '(', ')'}
MATH_MEMBERS = [o[0] for o in getmembers(math)]


def is_number(item):
    ''' Returns if the item passed is a number or None '''
    try:
        float(item)
        return True
    except ValueError:
        pass


def __is_symbol(item):
    return item in SYMBOLS


def __is_math_function(item):
    if len(re.findall('math.', item)) == 1:
        math_out = re.sub('^math.', '', item)
        return math_out in MATH_MEMBERS


def formula(formula_string):
    ''' Validates the formula passed, returns the tokens with errors '''
    splitted = set(formula_string.split(' '))
    return [item for item in splitted if not is_number(item) and not item == 'level'
            and not __is_symbol(item) and not __is_math_function(item)]
