''' Tester Parent module '''
import testers.server_tester as server
import testers.level_tester as level
import testers.selection_tester as selection
import testers.validation_tester as validation

from debugger import print_test_info, print_test_list, print_error, print_success

def run_all_tests():
    ''' Runs all the test of the system '''
    # __run_tests(server.get_all_tests(), 'Server')
    # __run_tests(level.get_all_tests(), 'Level')
    # __run_tests(selection.get_all_tests(), 'Selection')
    __run_tests(validation.get_all_tests(), 'ValidationTests')

def __run_tests(test_list, bundle_test_name):
    if test_list:
        success = 0
        number_of_tests = len(test_list)
        print_test_info(bundle_test_name)
        for test in test_list:
            result = test.run()
            success = success + 1 if result else success
            print_test_list(type(test).__name__, result, test.get_result())
        if success != number_of_tests:
            print_error('{}/{} completed successfully'.format(success, number_of_tests))
        else:
            print_success('All test were completed succesfully ({}/{})'.format(success,
                                                                               number_of_tests))
        