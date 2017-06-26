''' Validation module for karma implementations '''
import utils.print as print_
from content_resolver import content_resolver
from models.observation import Observation
from models.image import Image
from models.user import User

class ValidationProviderAbstract:
    ''' Karma Level Provider Abstract, has the methods to validate and notify '''
    def post_vote(self, observation_data):
        ''' Updates observation data with the new vote '''
        raise NotImplementedError('Abstract class, this method should have been implemented')

    def get_observation_data(self, observation_id):
        ''' Returns the observation or nothing '''
        raise NotImplementedError('Abstract class, this method should have been implemented')

    def print_info(self):
        ''' Prints the Provider Configuration '''
        raise NotImplementedError('Abstract class, this method should have been implemented')

class ValidationProvider(ValidationProviderAbstract):
    ''' Karma Level Provider Implementation, has the methods to validate and notify '''
    def __init__(self, minimum_votes, maximum_votes, lower_limit, upper_limit):
        self.minimum_votes = minimum_votes
        self.maximum_votes = maximum_votes
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit
        self.print_info()

    def print_info(self):
        print_.info('INFO', 'Initiating ValidationProvider with:')
        print_.key_value_list('Minimum Votes', self.minimum_votes)
        print_.key_value_list('Maximum Votes', self.maximum_votes)
        print_.key_value_list('Lower Limit', self.lower_limit)
        print_.key_value_list('Upper Limit', self.upper_limit)

    def post_vote(self, observation_data):
        ''' Updates the observation with the data passed, returns the observation updated '''
        user_info = observation_data['user_info']
        user, created = content_resolver.get_or_create_it(User, user_info)

        observation_info = observation_data['observation_info']
        observation, created = content_resolver.get_or_create_it(Observation,
                                                                 observation_info)

        if not observation.user_has_voted(user):

            image_info = observation_info['image']
            image, created = content_resolver.get_or_create_it(Image, image_info)
            if created:
                content_resolver.update(image)

            vote_info = observation_data['vote_info']

            self.__set_points(observation, user, vote_info)
            content_resolver.update(observation)
            return observation
        # If false => user already voted this observation

    def get_observation_data(self, observation_id):
        return _get_observation_or_raise(observation_id)

    def __set_points(self, observation, user, vote_info):
        number_of_votes, certainty = observation.add_vote(vote_info, user)
        change, approved = self.__check_if_change(observation, certainty, number_of_votes)
        if change:
            observation.change_state(approved=approved)
        return True

    def __check_if_change(self, observation, certainty, number_of_votes):
        ''' Checks if the observation can change its status, returns True if change\n
                return[0]: change\n
                return[1]: to_approved '''
        if observation.get_notified():
            return False, False
        if number_of_votes >= self.maximum_votes:
            observation.change_state(approved=True)
            return True, True
        if number_of_votes >= self.minimum_votes:
            if certainty < self.lower_limit:
                return True, False
            elif certainty > self.upper_limit:
                return True, True
        return None, None

def _get_observation_or_raise(observation_id):
    observation = content_resolver.get(Observation, _id=observation_id)
    if not observation:
        raise ObservationNotFoundException
    return observation

class ObservationNotFoundException(Exception):
    pass
