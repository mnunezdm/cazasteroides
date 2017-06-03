''' Validation module for karma implementations '''
from Validation.Observation import Observation
from Debugger import print_info, print_list

class ValidationProviderAbstract:
    ''' Karma Level Provider Abstract, has the methods to validate and notify '''
    def set_points(self, observation_id, karma_level, vote_type):
        ''' Updates observation data with the new vote '''
        raise NotImplementedError('Abstract class, this method should have been implemented')

    def get_observation_data(self, observation_id):
        ''' Returns the data for the id passed '''
        raise NotImplementedError('Abstract class, this method should have been implemented')

class ValidationProvider(ValidationProviderAbstract):
    ''' Karma Level Provider Implementation, has the methods to validate and notify '''
    def __init__(self, minimum_votes, maximum_votes, lower_limit, upper_limit, database=None):
        self.observations = []
        self.minimum_votes = minimum_votes
        self.maximum_votes = maximum_votes
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit
        self.database = database
        self.__print_info()

    def __print_info(self):
        print_info('INFO', 'Initiating ValidationProvider with:')
        print_list('{} minimum votes'.format(self.minimum_votes))
        print_list('{} maximum votes'.format(self.maximum_votes))
        print_list('{} lower limit'.format(self.lower_limit))
        print_list('{} upper limit'.format(self.upper_limit))

    def set_points(self, observation_id, karma_level, vote_type):
        observation = self.__get_observation_or_create_it(observation_id)
        number_of_votes, certainty = observation.add_vote(karma_level, vote_type)
        if self.__check_if_change(observation, certainty, number_of_votes):
            print_info('OBS{}'.format(observation.observation_id),
                       'state changed to \'{}\''.format(observation.state))
        observation.update_observation_in_db()
        return observation

    def __get_observation_or_create_it(self, observation_id):
        observation = self.__get_observation(observation_id)
        if not observation:
            observation = Observation(observation_id, 0, 0, self.database)
            self.observations.append(observation)
        return observation

    def __get_observation(self, observation_id):
        observation = [observation for observation in self.observations
                       if observation.observation_id == observation_id]
        if observation:
            return observation[0]

    def __check_if_change(self, observation, certainty, number_of_votes):
        ''' Checks if the observation can change its status, returns True if change '''
        if observation.get_notified():
            return False
        if number_of_votes >= self.maximum_votes:
            observation.change_state(True)
            return True
        if number_of_votes >= self.minimum_votes:
            if certainty < self.lower_limit:
                observation.change_state(False)
                return True
            elif certainty > self.upper_limit:
                observation.change_state(True)
                return True

    def get_observation_data(self, observation_id):
        return self.__get_observation(observation_id)
