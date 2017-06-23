''' Helper for printing debug trace '''
import time

from colorama import Fore, init

DATA_TAG = Fore.CYAN + '[DATA]' + Fore.RESET

def init_terminal_colors():
    ''' Necessary for coloring terminal in windows '''
    init()

def print_info(message_type, message):
    ''' Prints message with type in yellow '''
    print(Fore.YELLOW + '[{}] '.format(message_type) + Fore.RESET + message)

def print_error(message):
    ''' Prints error message with type in red '''
    print(Fore.RED + '[ERROR] ' + Fore.RESET + message)

def print_success(message):
    ''' Prints sucess message with type in green '''
    print(Fore.GREEN + '[SUCCESS] ' + Fore.RESET + message)

def print_list(message):
    ''' Prints message in a list '''
    print('\t- ' + message)

def print_test_info(test_type):
    ''' Prints test info message '''
    print('{}[INFO]{} Starting {}:'.format(Fore.YELLOW, Fore.RESET,
                                           Fore.CYAN + test_type + Fore.RESET))

def print_test_list(test_name, success, message):
    ''' Prints message in a list '''
    test_name = __get_formated_test(test_name)
    test_result = __get_formated_test_result(success)
    print('\t-{}: {} {}'.format(test_name, test_result, message))

def __get_formated_test(test_name):
    return Fore.CYAN + test_name + Fore.RESET

def __get_formated_test_result(success):
    if success:
        return Fore.GREEN + 'OK' + Fore.RESET
    return Fore.RED + 'ERROR' + Fore.RESET

def to_string_list(type_name, content):
    ''' Returns a string with the type and content properly formated '''
    return '\t- ' + Fore.CYAN + '{}'.format(type_name) + Fore.RESET + ':\t {} \n'.format(content)

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
