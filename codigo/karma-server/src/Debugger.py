''' Helper for printing debug trace '''
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
