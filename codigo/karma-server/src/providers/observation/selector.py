''' Selector of the EFES Algorithm '''

class ObservationSelectorAbstract:
    ''' Abstract class for the Selector '''
    def select(self, observation_list):
        ''' Selects an observation from the list '''
        raise NotImplementedError('Abstract class, this method should have been implemented')

class ObservationSelector(ObservationSelectorAbstract):
    ''' Implementation of ObservationSelectorAbastract'''
    def select(self, observation_list):
        sorted_list = self.__sort(observation_list)
        if sorted_list:
            return observation_list[0]

    @staticmethod
    def __sort(observation_list):
        return sorted(observation_list, key=lambda x: x.puntuation.calculate_certainty(),
                      reverse=True)
