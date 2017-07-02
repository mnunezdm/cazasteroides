''' Filter of the EFES Algorithm '''
import math
from models.observation import State


class ObservationFilterAbstract:
    ''' Abstract class for observation Filter '''

    def observations(self, observation_list, karma_level):
        ''' Gets the observations for the karma level passed '''
        raise NotImplementedError('Abstract class, this method should have been implemented')


class ObservationFilter(ObservationFilterAbstract):
    ''' Implementation of the Filter class '''
    def __init__(self, number_of_karma_levels, number_of_filter_levels):
        self.number_of_filter_levels = number_of_filter_levels
        self.karma_per_filter = number_of_karma_levels / number_of_filter_levels

    def observations(self, observation_list, karma_level):
        filter_level = self.__get_filter_level(karma_level)
        filtered_observations = self.__filter_observations(observation_list)
        return self.__get__specific_observations(filtered_observations, filter_level), filter_level

    def __get__specific_observations(self, filtered_observations, filter_level):
        magic_number = math.ceil(filter_level / 2) - 1
        if filter_level % 2 == 0:
            return filtered_observations[magic_number] + filtered_observations[magic_number + 1]
        return filtered_observations[magic_number]

    def __get_filter_level(self, karma_level):
        filter_level = math.ceil(karma_level / self.karma_per_filter)
        if filter_level > self.number_of_filter_levels:
            return self.number_of_filter_levels
        if filter_level == 0:
            return 1
        return filter_level

    def __chunkify(self, list_, number_of_groups):
        return [list_[i::number_of_groups] for i in range(number_of_groups)]

    def __filter_observations(self, observation_list):
        approved = [observation for observation in observation_list
                    if observation.state == State.APPROVED]
        pending = [observation for observation in observation_list
                   if observation.state == State.PENDING]
        disputed = [observation for observation in observation_list
                    if observation.state == State.DISPUTED]
        pending_split = self.__chunkify(pending, 2)
        result = [approved, pending_split[0], disputed + pending_split[1]]
        return result
        