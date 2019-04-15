import math

import karmaserver.utils.validate as validate
from karmaserver.data.models import db
from flask import json


class Policy(db.Model):
    _id = db.Column(db.String(64), primary_key=True)
    __formula = db.Column(db.String(128))
    max_level = db.Column(db.Integer)

    def __init__(self, policy_id, formula, max_level):
        self._id = policy_id
        self.max_level = max_level
        self.set_formula(formula)

    def set_formula(self, formula):
        ''' Sets formula, after checking the format,
            if wrong format InvalidFormulaException is raised '''
        self.__check_formula_or_raise(formula)
        self.__formula = formula

    def __check_formula_or_raise(self, formula):
        errors = validate.formula(formula)
        if errors:
            raise InvalidFormulaException(json.dumps({"errors": errors}))

    def get_level(self, user_points):
        ''' Get the level info for the puntuation passed '''
        level = self.__get_level(user_points, 0, 1)
        level['policy'] = self._id
        return level

    def __get_level(self, user_points, total_points, level):
        if level < self.max_level:
            total_points += self.__calculate_points(level)
            if user_points >= total_points:
                return self.__get_level(user_points, total_points, level + 1)
        return self.__serialize_points(level, total_points - user_points)

    def get_levels(self):
        ''' Get all the levels of this policy '''
        return {'policy': self._id, 'formula': self.__formula, 'max_level':self.max_level, "levels": self.__get_levels([], 0, 1)}

    def __get_levels(self, points_list, total_points, level):
        if level <= self.max_level:
            points_to_next = self.__calculate_points(level)
            points_list.append(self.__serialize_points(level, total_points))
            total_points += points_to_next
            return self.__get_levels(points_list, total_points, level + 1)
        return points_list

    def __calculate_points(self, level):
        ''' Calculates the points necessary to reach the passed level from the previous level '''
        value = eval(self.__formula)
        return _round_in_hundreds(value)


    def __serialize_points(self, level, points):
        if self.max_level == level:
            return {"level": level}
        return {"level": level, "points_to_next": points}


def _round_in_hundreds(value):
    value = round(value) / 1000
    value = round(value, 1) * 1000
    return round(value)


class InvalidFormulaException(Exception):
    pass


class PolicyNotExistsException(Exception):
    pass


class PolicyExistsException(Exception):
    pass
