''' Selector of the EFES Algorithm '''
from random import randint

from models.observation import State


class ObservationSelectorAbstract:
    ''' Abstract class for the Selector '''
    def select(self, observation_list):
        ''' Selects an observation from the list '''
        raise NotImplementedError('Abstract class, this method should have been implemented')


class SortedObservationSelector(ObservationSelectorAbstract):
    ''' Implementation of ObservationSelectorAbastract
        returns the observation with higher certainty'''
    def select(self, observation_list):
        if observation_list:
            sorted_list = self.__sort(observation_list)
            return sorted_list[0]

    @staticmethod
    def __sort(observation_list):
        return sorted(observation_list, key=lambda x: x.puntuation.calculate_certainty(),
                      reverse=True)


class RandomObservationSelector(ObservationSelectorAbstract):
    ''' Implementation of ObservationSelectorAbastract
        returns a random observation inside the list passed'''
    def select(self, observation_list):
        if observation_list:
            if observation_list[0].state == State.DISPUTED:
                return observation_list[0]
            index_item = randint(0, len(observation_list) - 1)
            return observation_list[index_item]
            