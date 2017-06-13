''' Filter of the EFES Algorithm '''
class ObservationFilterAbstract:
    ''' Abstract class for observation Filter '''

    def get_observations_for_level(self, observation_list, karma_level):
        ''' Gets the observations for the karma level passed '''
        raise NotImplementedError('Abstract class, this method should have been implemented')

class ObservationFilter(ObservationFilterAbstract):
    ''' Implementation of the Filter class '''

    def get_observations_for_level(self, observation_list, karma_level):
        return observation_list
        