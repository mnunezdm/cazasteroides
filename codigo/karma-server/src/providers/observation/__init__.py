''' EFES Provider module '''
from providers.observation.evaluator import ObservationEvaluator
from providers.observation.filter import ObservationFilter
from providers.observation.eraser import ObservationEraser
from providers.observation.selector import ObservationSelector
from debugger import print_info

class ObservationSelectionProviderAbstract:
    ''' Abstract class of the EFES Provider class '''
    def get_observation(self, observation_list, user_id, karma_level):
        ''' Returns the Observation based on the karma_level and the user_id '''
        raise NotImplementedError('Abstract class, this method should have been implemented')

class ObservationSelectionProvider(ObservationSelectionProviderAbstract):
    ''' Implementation of the EFES Provider class '''
    def __init__(self):
        print_info('INFO', 'Initializing Observation Selection Provider')
        self.evaluator = ObservationEvaluator()
        self.filter = ObservationFilter()
        self.eraser = ObservationEraser()
        self.selector = ObservationSelector()

    def get_observation(self, observation_list, user_id, karma_level):
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
