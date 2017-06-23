''' EFES Provider module '''
from modules.selection.provider.evaluator import ObservationEvaluator
from modules.selection.provider.filter import ObservationFilter
from modules.selection.provider.eraser import ObservationEraser
from modules.selection.provider.selector import ObservationSelector
from debugger import print_info, print_list, start_timer, stop_timer
from content_resolver import content_resolver
from models.observation import Observation

class ObservationSelectionProviderAbstract:
    ''' Abstract class of the EFES Provider class '''
    def get_observation(self, observation_list, user_id, karma_level):
        ''' Returns the Observation based on the karma_level and the user_id '''
        raise NotImplementedError('Abstract class, this method should have been implemented')

class ObservationSelectionProvider(ObservationSelectionProviderAbstract):
    ''' Implementation of the EFES Provider class '''
    def __init__(self, number_of_karma_levels, number_of_filter_levels):
        print_info('INFO', 'Initializing Observation Selection Provider')
        print_list('{} maximum filter level'.format(number_of_filter_levels))
        self.evaluator = ObservationEvaluator()
        self.filter = ObservationFilter(number_of_karma_levels, number_of_filter_levels)
        self.eraser = ObservationEraser()
        self.selector = ObservationSelector()

    def get_new_observation(self, user_id, karma_level):
        ''' Returns an observation for the user passed '''
        observation_list = content_resolver.get(Observation)
        return self.__get_observation(observation_list, user_id, karma_level)

    def __get_observation(self, observation_list, user_id, karma_level):
        evaluated_observations = self.evaluator.evaluate(observation_list)
        observations_for_level = self.filter.get_observations_for_level(evaluated_observations,
                                                                        karma_level)
        erased__observations = self.eraser.erase(observations_for_level, user_id)
        if erased__observations:
            selected__observation = self.selector.select(erased__observations)
            return selected__observation.serialize(id_position=True)
        else:
            return {
                "nothing": "nothing"
            }
