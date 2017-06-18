''' Validation module for karma implementations '''
from debugger import print_info, print_list

class ValidationProviderAbstract:
    ''' Karma Level Provider Abstract, has the methods to validate and notify '''
    def set_points(self, observation, user_info, vote_info):
        ''' Updates observation data with the new vote '''
        raise NotImplementedError('Abstract class, this method should have been implemented')

class ValidationProvider(ValidationProviderAbstract):
    ''' Karma Level Provider Implementation, has the methods to validate and notify '''
    def __init__(self, minimum_votes, maximum_votes, lower_limit, upper_limit):
        self.minimum_votes = minimum_votes
        self.maximum_votes = maximum_votes
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit
        self.__print_info()

    def __print_info(self):
        print_info('INFO', 'Initiating ValidationProvider with:')
        print_list('{} minimum votes'.format(self.minimum_votes))
        print_list('{} maximum votes'.format(self.maximum_votes))
        print_list('{} lower limit'.format(self.lower_limit))
        print_list('{} upper limit'.format(self.upper_limit))

    def set_points(self, observation, user, vote_info):
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
