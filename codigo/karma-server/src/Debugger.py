''' Helper for printing debug trace '''
from colorama import Fore, init

def init_colors():
    ''' Necessary for coloring terminal in windows '''
    init()

def print_info(message_type, message):
    ''' Prints message with type in yellow '''
    print(Fore.YELLOW + '[{}] '.format(message_type) + Fore.RESET + message)

def print_error(message):
    ''' Prints error message with type in red '''
    print(Fore.RED + '[ERROR] ' + Fore.RESET + message)
