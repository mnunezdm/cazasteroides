''' KarmaServerImplementation '''
from configuration_params import (LOWER_LIMIT, MAX_KARMA_LEVEL, MAXIMUM_VOTES,
                                  MINIMUM_VOTES, POINTS_PER_OBSERVATION,
                                  UPPER_LIMIT)
from providers.validation import ValidationProvider
from providers.level import KarmaLevelProvider
from providers.observation import ObservationSelectionProvider
# from content_resolver import ThreadedUpdateContentResolver
# from content_resolver import CachedContentResolver
from content_resolver import StaticContentResolver

from models.observation import Observation
from models.user import User
from models.image import Image

class KarmaServer:
    ''' Class for Server '''
    def __init__(self, app, db):
        self.karma_level_provider = KarmaLevelProvider(MAX_KARMA_LEVEL, POINTS_PER_OBSERVATION)
        self.validation_provider = ValidationProvider(MINIMUM_VOTES, MAXIMUM_VOTES, LOWER_LIMIT,
                                                      UPPER_LIMIT)
        self.observation_selection = ObservationSelectionProvider()
        # self.content_resolver = CachedContentResolver(app, db, Observation, User)
        self.content_resolver = StaticContentResolver(db)
        #self.content_resolver = ThreadedUpdateContentResolver(db)

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
        observation = self.content_resolver.get_or_create_it(Observation, observation_info)

        user_info = observation_data['user_info']
        user = self.content_resolver.get_or_create_it(User, user_info)

        image_info = observation_info['image']
        image = self.content_resolver.get_or_create_it(Image, image_info)
        self.content_resolver.update(image)

        vote_info = observation_data['vote_info']

        if not observation.repeated_vote(user):
            self.validation_provider.set_points(observation, user, vote_info)
            self.content_resolver.update(observation)
            return observation
        # If false => user already voted this observation

    def get_observation_data(self, observation_id):
        ''' Returns the observation or nothing '''
        return self.content_resolver.get(Observation, _id=observation_id).first()

    def get_new_observation(self, user_id, karma_level=1):
        ''' Returns an observation for the user passed '''
        observation_list = self.content_resolver.get(Observation)
        return self.observation_selection.get_observation(observation_list, user_id, karma_level)
