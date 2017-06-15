''' Filter of the EFES Algorithm '''
import math
from models.observation import State

class ObservationFilterAbstract:
    ''' Abstract class for observation Filter '''

    def get_observations_for_level(self, observation_list, karma_level):
        ''' Gets the observations for the karma level passed '''
        raise NotImplementedError('Abstract class, this method should have been implemented')

class ObservationFilter(ObservationFilterAbstract):
    ''' Implementation of the Filter class '''

    def __init__(self, number_of_karma_levels=50, number_of_humhum_levels=5):
        self.karma_per_humhum = number_of_karma_levels / number_of_humhum_levels

    def get_observations_for_level(self, observation_list, karma_level):
        humhum_level = self.__get_humhum_level(karma_level)
        filtered_observations = self.__filter_observations(observation_list)
        return self.__get__specific_observations(filtered_observations, humhum_level)

    def __get__specific_observations(self, filtered_observations, humhum_level):
        magic_number = math.floor(humhum_level / 2) + 1
        if humhum_level % 2 == 0:
            return filtered_observations[magic_number] + filtered_observations[magic_number + 1]
        return filtered_observations[magic_number]

    def __get_humhum_level(self, karma_level):
        return math.floor(karma_level / self.karma_per_humhum)

    def __chunkify(self, list_, number_of_groups):
        return [list_[i::number_of_groups] for i in range(number_of_groups)]

    def __filter_observations(self, observation_list):
        approved = [observation for observation in observation_list
                    if observation.state == State.APPROVED]
        pending = [observation for observation in observation_list
                   if observation.state == State.PENDING]
        pending_split = self.__chunkify(pending, 2)
        return [approved, pending_split[0], pending_split[1]]
        