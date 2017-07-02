''' Tester Parent module '''
import sys
import inspect

import tests.server_tester as server
import tests.level_tester as level
import tests.selection_tester as selection
import tests.validation_tester as validation

import utils.print as print_


def run_all_tests():
    ''' Runs all the test of the system '''
    print_.title('Starting Test Module')
    # __run_tests(server.get_all_tests(), 'Server')
    # __run_tests(level.get_all_tests(), 'Level')
    # __run_tests(selection.get_all_tests(), 'Selection')
    __run_test_bundle(validation, 'ValidationTests')


def __run_test_bundle(module, bundle_test_name):
    test_list = inspect.getmembers(sys.modules[module.__name__], inspect.isclass)
    success = 0
    number_of_tests = len(test_list)
    print_.test_info(bundle_test_name)
    for test_name, test_class in test_list:
        if 'Abstract' in test_name:
            number_of_tests -= 1
            continue
        test = test_class()
        result = test.run()
        success = success + 1 if result else success
        print_.test_list(test_name, result, test.get_result())
    if success != number_of_tests:
        print_.error(f'{success}/{number_of_tests} completed successfully')
    else:
        print_.success(f'All test were completed successfully ({success}/{number_of_tests})')
