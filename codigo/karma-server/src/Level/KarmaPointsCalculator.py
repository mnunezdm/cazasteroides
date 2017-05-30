''' Provides methods to calculate and format Karma Data '''
from math import log

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
    value = round(log((level/3)+1) * 2000)
    return __round_in_hundreds(value)

def __round_in_hundreds(value):
    value = round(value) / 1000
    value = round(value, 1) * 1000
    return round(value)
