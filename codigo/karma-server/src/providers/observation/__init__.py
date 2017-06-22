''' EFES Provider module '''
from providers.observation.evaluator import ObservationEvaluator
from providers.observation.filter import ObservationFilter
from providers.observation.eraser import ObservationEraser
from providers.observation.selector import ObservationSelector
from debugger import print_info, print_list, start_timer, stop_timer

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

    def get_observation(self, observation_list, user_id, karma_level):
        time_start = start_timer()
        evaluated_observations = self.evaluator.evaluate(observation_list)
        stop_timer(time_start, 'evaluate')
        time_start = start_timer()
        observations_for_level = self.filter.get_observations_for_level(evaluated_observations,
                                                                        karma_level)
        stop_timer(time_start, 'filter')
        time_start = start_timer()
        erased__observations = self.eraser.erase(observations_for_level, user_id)
        stop_timer(time_start, 'erase')
        time_start = start_timer()
        if erased__observations:
            time_start = start_timer()
            selected__observation = self.selector.select(erased__observations)
            stop_timer(time_start, 'select')
            return selected__observation.serialize(id_position=True)
        else:
            return {
                "nothing": "nothing"
            }
