''' EFES Provider module '''
from modules.selection.provider.evaluator import ObservationEvaluator
from modules.selection.provider.filter import ObservationFilter
from modules.selection.provider.eraser import ObservationEraser
from modules.selection.provider.selector import RandomObservationSelector
import utils.print as print_
from utils import start_timer, stop_timer
from data.content_resolver import content_resolver
from data.models.observation import Observation


class ObservationSelectionProviderAbstract: # pragma: no cover
    ''' Abstract class of the EFES Provider class '''
    def select_observation_for_discover(self, user_id, karma_level):
        ''' Returns the Observation based on the karma_level and the user_id '''
        raise NotImplementedError('Abstract class, this method should have been implemented')

    def select_observation_for_votation(self, user_id, karma_level):
        ''' Returns the Observation based on the karma_level and the user_id '''
        raise NotImplementedError('Abstract class, this method should have been implemented')

    def print_info(self):
        ''' Prints the Provider Configuration '''
        raise NotImplementedError('Abstract class, this method should have been implemented')


class ObservationSelectionProvider(ObservationSelectionProviderAbstract):
    ''' Implementation of the EFES Provider class '''
    def __init__(self, number_of_karma_levels, number_of_filter_levels):
        self.number_of_filter_levels = number_of_filter_levels
        self.evaluator = ObservationEvaluator()
        self.filter = ObservationFilter(number_of_karma_levels, number_of_filter_levels)
        self.eraser = ObservationEraser()
        self.selector = RandomObservationSelector()
        self.print_info()

    def print_info(self):
        print_.initialize_info(self.__class__.__name__, True)
        print_.key_value_list('Maximum Filter Level', self.number_of_filter_levels)

    def select_observation_for_discover(self, user_id, karma_level):
        observation_list = content_resolver.get(Observation)
        return self.__get_observation(observation_list, user_id, karma_level)

    def select_observation_for_votation(self, user_id, karma_level):
        observation_list = content_resolver.get(Observation)
        return self.__get_observation(observation_list, user_id, karma_level)

    def __get_observation(self, observation_list, user_id, karma_level):
        evaluated_observations = self.evaluator.evaluate(observation_list)
        filtered_observations, level = self.filter.observations(evaluated_observations,
                                                                karma_level)
        erased__observations = self.eraser.erase(filtered_observations, user_id)
        selected__observation = self.selector.select(erased__observations)
        if selected__observation:
            serialized = selected__observation.serialize(id_position=True)
            serialized['filter_level'] = level
            return serialized
