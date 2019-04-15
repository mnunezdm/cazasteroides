''' Evaluator of the EFES Algorithm '''
from math import exp

from karmaserver.data.models.observation import State


class ObservationEvaluatorAbstract: # pragma: no cover
    ''' Abstract class for Observation Evaluator '''
    def evaluate(self, observation_list):
        ''' Evaluate the observations passed '''
        raise NotImplementedError('Abstract class, this method should have been implemented')


class ObservationEvaluator(ObservationEvaluatorAbstract):
    ''' Implementation of the Evaluator class '''
    def evaluate(self, observation_list):
        for observation in observation_list:
            observation.difficulty = self.__evaluate_observation(observation)
        return observation_list

    def __evaluate_observation(self, observation):
        static = self.__get_static_value(observation)
        dynamic = self.__get_dynamic_value(observation)
        return static - dynamic

    def __get_static_value(self, observation):
        brightness = self.__calculate_bright(observation.brightness)
        probability = self.__calculate_probability(observation.image.probability)
        fwhm = self.__calculate_fwhm(observation.image.fwhm)
        return 1/3 * brightness + 1/3 * probability + 1/3 * fwhm

    def __get_dynamic_value(self, observation):
        multiplier = self.__get_multiplier_for_state(observation.state)
        number_of_votes = observation.votes.number_of_votes()
        return self.__calculate_votes(number_of_votes, multiplier)

    @staticmethod
    def __get_multiplier_for_state(state):
        if State.PENDING == state:
            return 0.5
        if State.APPROVED == state:
            return 1
        if State.DENYED == state:
            return 0.1
        if State.DISPUTED == state:
            return 1

    @staticmethod
    def __calculate_probability(probability):
        return 100 - probability

    @staticmethod
    def __calculate_bright(bright):
        return 100 * (1 / (1 + (pow(exp(1), -(0.6 * (bright - 15))))))

    @staticmethod
    def __calculate_fwhm(fwhm):
        return 200 * (1 / (1 + (pow(exp(1), -(fwhm) + 1))))
    @staticmethod
    def __calculate_votes(number_of_votes, multiplier):
        return number_of_votes * multiplier
