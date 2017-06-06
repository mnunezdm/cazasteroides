''' Evaluator of the EFES Algorithm '''
from content_resolver import get_all, update
from models.observation import Observation

class ImageEvaluatorAbstract:
    ''' Abstract class for Image Evaluator '''
    def evaluate(self, images_list, observation_list):
        ''' Evaluate the images passed '''
        raise NotImplementedError('Abstract class, this method should have been implemented')

class ImageEvaluator(ImageEvaluatorAbstract):
    ''' Implementation of the Evaluator class '''
    def evaluate(self, observation_list):
        observation_list = get_all(Observation)
        for observation in observation_list:
            self.__evaluate_observation(observation)
        return observation_list

    def __evaluate_observation(self, observation):
        probability = observation.image.probability 
        fwhm = observation.image.fwhm  * self.fwhm_multiplier
        number_of_votes = observation.votes.number_of_votes()

        probability_points = probability
        fwhm = fwhm  * self.fwhm_multiplier
        state = observation.state

        return 1/probability + fwhm + 1/number_of_votes

    def __get_multiplier_for_observation_state(self, state):
        if 'pending' in state:
            return 0.4
        if 'denyed' in state:
            return 0.1
        if 'approved' in state:
            return 0.7

    def __observations_value(self, observations):
        value = 0
        for observation in observations:
            value = value + observation.get_value(observation)
        return value
        