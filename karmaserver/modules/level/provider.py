''' Module for Karma Level Provider Class '''
import karmaserver.utils.print as print_
from karmaserver.data.content_resolver import content_resolver
from karmaserver.data.models.policy import Policy, PolicyNotExistsException, PolicyExistsException
from karmaserver.config import DEFAULT_FORMULA, MAX_KARMA_LEVEL


class KarmaLevelProviderAbstract: # pragma: no cover
    ''' Karma Level Provider Abstract, has the methods to calculate the karma
        levels and to classify user for its points '''

    def print_info(self, default_created):
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

    def update_policy(self, policy_id, formula=None, max_level=None):
        ''' Updates an existing policy '''
        raise NotImplementedError('Abstract class, this method should have been implemented')

    def delete_policy(self, policy_id):
        ''' Deletes an existing policy '''
        raise NotImplementedError('Abstract class, this method should have been implemented')


class KarmaLevelProvider(KarmaLevelProviderAbstract):
    ''' Implementation of Karma Level Provider '''
    def __init__(self):
        default_created = _create_default_policy_if_not()
        self.print_info(default_created)

    def print_info(self, default_created):
        print_.initialize_info(self.__class__.__name__, default_created)
        if default_created:
            print_.info_list('default policy created')

    def get_level(self, policy_id, points):
        policy = self.__get_policy_or_raise(policy_id)
        return policy.get_level(points)

    def get_levels(self, policy_id):
        policy = self.__get_policy_or_raise(policy_id)
        return policy.get_levels()

    def create_policy(self, policy_id, formula, max_level):
        _raise_if_exists(policy_id)
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

    @staticmethod
    def __get_policy_or_raise(policy_id):
        policy = content_resolver.get(Policy, _id=policy_id)
        if not policy:
            raise PolicyNotExistsException(f'Policy = {policy_id}')
        return policy[0]


def _create_default_policy_if_not():
    policy = content_resolver.get(Policy, _id='default')
    if not policy:
        policy = Policy('default', DEFAULT_FORMULA, MAX_KARMA_LEVEL)
        content_resolver.update(policy)
        return True

def _raise_if_exists(policy_id):
    policy = content_resolver.get(Policy, _id=policy_id)
    if policy:
        raise PolicyExistsException
        