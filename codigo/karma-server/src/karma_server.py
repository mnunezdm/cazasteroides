''' KarmaServerImplementation '''
from configuration_params import (LOWER_LIMIT, MAX_KARMA_LEVEL, MAXIMUM_VOTES,
                                  MINIMUM_VOTES, POINTS_PER_OBSERVATION,
                                  UPPER_LIMIT)
from providers.validation import ValidationProvider
from providers.level import KarmaLevelProvider
from models.observation import get_observation_or_create_it, get_observation

class KarmaServer:
    ''' Class for Server '''
    def __init__(self):
        self.karma_level_provider = KarmaLevelProvider(MAX_KARMA_LEVEL, POINTS_PER_OBSERVATION)
        self.validation_provider = ValidationProvider(MINIMUM_VOTES, MAXIMUM_VOTES, LOWER_LIMIT,
                                                      UPPER_LIMIT, database=None)

    def get_karma_for_points(self, user_points):
        ''' Gets karma data for the user_points passed '''
        try:
            return self.karma_level_provider.get_level_for_points(user_points)
        except IndexError:
            return {"karma_level":MAX_KARMA_LEVEL}

    def get_karma_general_info(self):
        ''' Gets info for the karma '''
        return self.karma_level_provider.get_general_info()

    def post_vote(self, observation_data):
        ''' Updates the observation with the data passed, returns the observation updated '''
        observation_info = observation_data['observation_info']
        observation = get_observation_or_create_it(observation_info)
        vote_info = observation_data['vote_info']
        self.validation_provider.set_points(observation, vote_info)
        return observation

    def get_observation_data(self, observation_id):
        ''' Returns the observation or nothing '''
        return get_observation(observation_id)
