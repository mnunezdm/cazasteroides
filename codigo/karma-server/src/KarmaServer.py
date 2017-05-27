''' KarmaServerImplementation '''
from KarmaLevelProvider import KarmaLevelProvider

class KarmaServer:
    ''' Class for Server '''
    def __init__(self, max_level, points_per_observation):
        self.database = None
        self.karma_level_provider = KarmaLevelProvider(max_level, points_per_observation)

    def get_karma_for_points(self, user_points):
        ''' Gets karma data for the user_points passed '''
        return self.karma_level_provider.get_level_for_points(user_points)

    def get_karma_general_info(self):
        ''' Gets info for the karma '''
        return self.karma_level_provider.get_general_info()
