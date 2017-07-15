''' Tester Parent module '''
import sys
import inspect

import tests.level_tester as level
import tests.selection_tester as selection
import tests.validation_tester as validation

import utils.print as print_


def run_all_tests():
    ''' Runs all the test of the system '''
    print_.title('Starting Test Module')
    success = [0] * 3
    total = [0] * 3
    success[0], total[0] = __run_test_bundle(level, 'LevelTests')
    success[1], total[1] = __run_test_bundle(selection, 'SelectionTests')
    success[2], total[2] = __run_test_bundle(validation, 'ValidationTests')
    __check_results(sum(success), sum(total))


def __check_results(success_total, tests_total):
    if success_total != tests_total:
        print_.error(f'{success_total}/{tests_total} completed successfully')
    else:
        print_.success(f'All test were completed successfully ({success_total}/{tests_total})')


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
    return success, number_of_tests
