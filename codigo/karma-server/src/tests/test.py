''' Test module '''


class TestAbstract: # pragma: no cover
    ''' Test class '''
    def run(self):
        ''' Runs the test class '''
        raise NotImplementedError('Abstract method')

    def get_result(self):
        ''' Prints the result of the test class '''
        raise NotImplementedError('Abstract method')
