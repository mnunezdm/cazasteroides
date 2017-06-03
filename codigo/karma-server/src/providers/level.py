''' Module for Karma Level Provider Class '''
import operator
from math import log
from debugger import print_info, print_list


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
        self.__print_info(max_level, points_per_observation)

    @staticmethod
    def __print_info(max_level, points_per_observation):
        print_info('INFO', 'Initializing KarmaLevelProvider with:')
        print_list('{} Maximum Karma Level'.format(max_level))
        print_list('{} Points per Observation'.format(points_per_observation))

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

def calculate_karma_item(level, total_points, points_per_observation):
    ''' Returns the karma item for the level and points passed '''
    points = __calculate_points(level)
    total_points = total_points + points
    return {
        'karma_level': level,
        'points_to_next': points,
        'total_points_to_next': total_points,
        'observations_to_next': calculate_rounded_observations(points, points_per_observation),
        'total_observations_to_next': calculate_rounded_observations(total_points,
                                                                     points_per_observation)
        }

def calculate_rounded_observations(points, points_per_observation):
    ''' Returns the aproximated rounded value of observations required to obtain next level '''
    return round(points/points_per_observation + 0.5)

def __calculate_points(level):
    value = round(log((level/3)+1) * 350)
    return __round_in_hundreds(value)

def __round_in_hundreds(value):
    value = round(value) / 1000
    value = round(value, 1) * 1000
    return round(value)
