''' Module for Karma Level Provider Class '''
import operator
from Level.KarmaPointsCalculator import calculate_karma_item, calculate_rounded_observations

class KarmaLevelProviderAbstract:
    ''' Karma Level Provider Abstract, has the methods to calculate the karma
        levels and to classify user for its points '''

    def get_level_for_points(self, user_points):
        ''' Returns the information for the karma level for the points passed '''
        raise NotImplementedError('Abstract class, this method should have been implemented')

    def get_general_info(self):
        ''' Returns all Karma Data '''
        raise NotImplementedError('Abstract class, this method should have been implemented')


class KarmaLevelProvider(KarmaLevelProviderAbstract):
    ''' Karma Level Provider, has the methods to calculate the karma
        levels and to classify user for its points '''
    def __init__(self, max_level, points_per_observation):
        self.points_per_observation = points_per_observation
        self.karma_data = self.__populate_points([], 1, 0, max_level)

    def __populate_points(self, karma_list, level, total_points, max_level):
        ''' Instantiates the points array '''
        karma_item = calculate_karma_item(level, total_points, self.points_per_observation)
        karma_list.append(karma_item)
        next_total_points = total_points + karma_item['points_to_next']
        if level < max_level:
            return self.__populate_points(karma_list, level + 1, next_total_points, max_level)
        return karma_list

    def get_level_for_points(self, user_points):
        next_level = self.__get_next_level(user_points)
        return self.__specific_next_level(next_level, user_points)

    def __get_next_level(self, user_points):
        next_levels = [karma_item for karma_item in self.karma_data
                       if karma_item['total_points_to_next'] > user_points]
        return sorted(next_levels, key=operator.itemgetter('total_points_to_next'),
                      reverse=False)[0]

    def __specific_next_level(self, next_level, user_points):
        next_level['karma_level'] = next_level['karma_level']
        specific_points_to_next = next_level['total_points_to_next'] - user_points
        next_level['points_to_next'] = specific_points_to_next
        next_level['observations_to_next'] = calculate_rounded_observations(
            specific_points_to_next, self.points_per_observation)
        return next_level

    def get_general_info(self):
        return self.karma_data
        