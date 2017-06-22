''' Module for Basic Server Testing '''
from testers.tester import Tester
from debugger import print_info

class ServerTester(Tester):
    ''' Server Tester class '''
    def run(self):
        print_info('INFO', '{}')

    def print_result(self):
        pass


def get_all_tests():
    ''' Returns all tests '''
    return [ServerTester]
