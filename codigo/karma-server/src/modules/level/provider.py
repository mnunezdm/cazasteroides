''' Module for Karma Level Provider Class '''
import utils.print as print_
from content_resolver import content_resolver
from models.policy import Policy, PolicyNotExistsException

class KarmaLevelProviderAbstract:
    ''' Karma Level Provider Abstract, has the methods to calculate the karma
        levels and to classify user for its points '''

    def print_info(self):
        ''' Prints the Provider Configuration '''
        raise NotImplementedError('Abstract class, this method should have been implemented')

    def get_level(self, policy_id, points):
        ''' Returns the information for the karma level for the points passed '''
        raise NotImplementedError('Abstract class, this method should have been implemented')

    def get_levels(self, policy_id):
        ''' Returns all Karma Data '''
        raise NotImplementedError('Abstract class, this method should have been implemented')

    def create_policy(self, policy_id, formula, max_level):
        ''' Creates new policy '''
        raise NotImplementedError('Abstract class, this method should have been implemented')

class KarmaLevelProvider(KarmaLevelProviderAbstract):
    ''' Implementation of Karma Level Provider '''
    def __init__(self):
        self.print_info()

    def print_info(self):
        print_.initialize_info(self.__class__.__name__, False)

    def get_level(self, policy_id, points):
        policy = self.__get_policy_or_raise(policy_id)
        return policy.get_level(points)

    def get_levels(self, policy_id):
        policy = self.__get_policy_or_raise(policy_id)
        return policy.get_levels()

    def create_policy(self, policy_id, formula, max_level):
        policy = Policy(policy_id, formula, max_level)
        content_resolver.update(policy)

    def update_policy(self, policy_id, formula=None, max_level=None):
        policy = self.__get_policy_or_raise(policy_id)
        if formula:
            policy.set_formula(formula)
        if max_level:
            policy.max_level = max_level
        content_resolver.update(policy)

    def delete_policy(self, policy_id):
        policy = self.__get_policy_or_raise(policy_id)
        content_resolver.delete(policy)

    def __get_policy_or_raise(self, policy_id):
        policy = content_resolver.get(Policy, _id=policy_id)
        if not policy:
            raise PolicyNotExistsException(f'Policy = {policy_id}')
        return policy[0]
    