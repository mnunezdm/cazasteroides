''' Helper for printing debug trace '''
import time

from colorama import Fore, init


def init_terminal_colors():
    ''' Necessary for coloring terminal in windows '''
    init()

def print_info(message_type, message):
    ''' Prints message with type in yellow '''
    print(Fore.YELLOW + '[{}] '.format(message_type) + Fore.RESET + message)

def print_error(message):
    ''' Prints error message with type in red '''
    print(Fore.RED + '[ERROR] ' + Fore.RESET + message)

def print_list(message):
    ''' Prints message in a list '''
    print('\t- ' + message)

def to_string_list(type_name, content):
    ''' Returns a string with the type and content properly formated '''
    return '\t- ' + Fore.CYAN + '{}'.format(type_name) + Fore.RESET + ':\t {} \n'.format(content)

DATA_TAG = Fore.CYAN + '[DATA]' + Fore.RESET

def start_timer():
    ''' Returns the time in ns '''
    return time.clock() * 1000000

def stop_timer(time_start, method):
    ''' Calculates the elapsed time between the actual time and the passed time,
    prints the information, and returns the elapsed time '''
    time_stop = time.clock() * 1000000
    elapsed = round(time_stop - time_start)
    print_info('INFO', 'Elapsed time in {} is {}ns'.format(method, elapsed))
    return elapsed
    