''' Helper for printing debug trace '''
from colorama import Fore, init

DATA_TAG = Fore.CYAN + '[DATA]' + Fore.RESET


def init_terminal_colors():
    ''' Necessary for coloring terminal in windows '''
    init()


def info(message_type, message):
    ''' Prints message with type in yellow '''
    print(Fore.YELLOW + f'[{message_type}] ' + Fore.RESET + message)


def error(message):
    ''' Prints error message with type in red '''
    print(Fore.RED + '[ERROR] ' + Fore.RESET + message)


def success(message):
    ''' Prints sucess message with type in green '''
    print(Fore.GREEN + '[SUCCESS] ' + Fore.RESET + message)


def key_value_list(key, value):
    ''' Prints message in a list '''
    print(to_string_list(key, value))


def title(message):
    ''' Prints title '''
    print(Fore.GREEN + "#" * 80)
    print("#" * 15, "\t"*2, message, "\t"*2, "#" * 15)
    print("#" * 80 + Fore.RESET)


def test_info(test_type):
    ''' Prints test info message '''
    print(f'{Fore.YELLOW}[INFO]{Fore.RESET} Starting {Fore.CYAN + test_type + Fore.RESET}:')


def test_list(test_name, was_success, message):
    ''' Prints message in a list '''
    test_name = __get_formatted_test(test_name)
    test_result = __get_formated_test_result(was_success)
    print(f'\t - {test_name}: {test_result} {message}')


def __get_formatted_test(test_name):
    return Fore.CYAN + test_name + Fore.RESET


def __get_formated_test_result(was_success):
    if was_success:
        return Fore.GREEN + 'OK' + Fore.RESET
    return Fore.RED + 'ERROR' + Fore.RESET


def to_string_list(key, content):
    ''' Returns a string with the type and content properly formated '''
    key = Fore.CYAN + key + Fore.RESET
    return f'\t- {key}: {content}'


def http(method, path, code, status, description, elapsed):
    ''' Prints the http petition '''
    method = __color_http(method)
    color_status = __color_status(code)

    message = f'{method} {path} {color_status}{code} {status} - {description} '
    message += f'{Fore.RESET}({elapsed} ns)'
    print(message)


def __color_http(method):
    return f'{Fore.CYAN}[{method}]{Fore.RESET}'


def __color_status(code):
    return Fore.GREEN if code < 299 else Fore.RED
