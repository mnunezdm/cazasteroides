''' Validation module for karma implementations '''
import utils.print as print_
from content_resolver import content_resolver
from models.observation import Observation, State
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
    def __init__(self, minimum_votes, votes_to_disputed, certainty_upper_limit,
                 certainty_lower_limit, votes_to_minimum_certainty):
        self.minimum_votes = minimum_votes
        self.votes_to_disputed = votes_to_disputed
        self.certainty_upper_limit = certainty_upper_limit
        self.certainty_lower_limit = certainty_lower_limit
        self.votes_to_minimum_certainty = votes_to_minimum_certainty
        self.print_info()

    def print_info(self):
        print_.initialize_info(self.__class__.__name__, True)
        print_.key_value_list('Minimum Votes', self.minimum_votes)
        print_.key_value_list('Votes to Minimum Certainty', self.votes_to_disputed)
        print_.key_value_list('Votes to Disputed', self.votes_to_minimum_certainty)
        print_.key_value_list('Certainty Upper Limit', f'±{self.certainty_upper_limit}')
        print_.key_value_list('Certainty Lower Limit', f'±{self.certainty_lower_limit}')

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
        change_to = self.__check_if_change(observation, certainty, number_of_votes)
        if change_to:
            observation.change_state(change_to)
        return True

    def __check_if_change(self, observation, certainty, number_of_votes):
        ''' Checks if the observation can change its status, returns True if change\n
                return[0]: change\n
                return[1]: to_approved '''
        if not observation.get_notified():
            if number_of_votes >= self.minimum_votes:
                certainty_limit = self.__calculate_new_certainty_limit(number_of_votes)
                if certainty < certainty_limit * -1:
                    return State.DENYED
                elif certainty > certainty_limit:
                    return State.APPROVED
                elif number_of_votes >= self.votes_to_disputed:
                    return State.DISPUTED

    def __calculate_new_certainty_limit(self, number_of_votes):
        if number_of_votes >= self.votes_to_minimum_certainty:
            return self.certainty_lower_limit
        elif number_of_votes < self.minimum_votes:
            return self.certainty_upper_limit
        else:
            number_of_votes -= self.minimum_votes
            certainty_difference = self.certainty_upper_limit - self.certainty_lower_limit
            step = certainty_difference / (self.votes_to_minimum_certainty - self.minimum_votes)
            return self.certainty_upper_limit - step * number_of_votes


def _get_observation_or_raise(observation_id):
    observation = content_resolver.get(Observation, _id=observation_id)
    if not observation:
        raise ObservationNotFoundException
    return observation


class ObservationNotFoundException(Exception):
    pass
